"""
Brain Topology Reader — fetch + compute 7 primitives from citizen brain graph.

DOCS: docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md

Reads ONLY topology: types, links, counts, energies, drives.
Content fields (content, synthesis) are NEVER accessed.

7 primitives:
    count(type)               → int
    mean_energy(type)         → float
    link_count(src, tgt)      → int
    min_links(type, n)        → int
    cluster_coefficient(type) → float
    drive(name)               → float
    recency(type)             → float
"""

import logging
import math
import time
from dataclasses import dataclass, field
from typing import Optional

from falkordb import FalkorDB

logger = logging.getLogger("graphcare.health.brain")

FALKORDB_HOST = "localhost"
FALKORDB_PORT = 6379


@dataclass
class BrainStats:
    """Topology-only brain statistics. No content ever."""

    # Original 7-primitive derived fields
    desire_count: int = 0
    desire_energy: float = 0.0
    desire_moment_ratio: float = 0.0
    desire_persistence: float = 0.0
    concept_count: int = 0
    process_count: int = 0
    value_count: int = 0
    memory_count: int = 0
    cluster_coefficient: float = 0.0
    curiosity: float = 0.0
    frustration: float = 0.0
    ambition: float = 0.0
    social_need: float = 0.0
    recency_desire: float = 0.0
    recency_moment: float = 0.0
    reachable: bool = True

    # Raw topology — what actually exists in the graph
    total_nodes: int = 0
    total_links: int = 0
    link_density: float = 0.0          # links / nodes (0 if no nodes)
    type_distribution: dict = field(default_factory=dict)  # {type_str: count}
    typed_node_count: int = 0          # nodes with a non-empty type
    untyped_node_count: int = 0        # nodes with type="" or no type
    has_backstory: bool = False
    has_personality: bool = False
    has_health_feedback: bool = False
    health_feedback_count: int = 0
    mean_energy_all: float = 0.0       # average energy across all nodes
    newest_node_age_hours: float = -1  # age of most recent node (-1 = unknown)

    @property
    def brain_category(self) -> str:
        """Categorize brain state based on raw topology."""
        if self.total_nodes == 0:
            return "VOID"
        if self.total_nodes <= 10 and self.total_links == 0:
            return "MINIMAL"
        if self.typed_node_count > 10 and self.curiosity + self.ambition + self.social_need > 0:
            return "STRUCTURED"
        if self.total_nodes > 50:
            return "SEEDED"
        return "MINIMAL"


def _get_graph(handle: str):
    """Get FalkorDB graph for citizen brain."""
    db = FalkorDB(host=FALKORDB_HOST, port=FALKORDB_PORT)
    graph_name = f"brain_{handle}"
    return db.select_graph(graph_name)


def _safe_query(graph, cypher: str, params: Optional[dict] = None) -> list:
    """Execute Cypher, return result rows or empty list on error."""
    try:
        result = graph.query(cypher, params or {})
        return result.result_set if result.result_set else []
    except Exception as e:
        logger.warning(f"Cypher failed: {e}")
        return []


# ── 7 Primitives ─────────────────────────────────────────────────────────────


def count(graph, node_type: str) -> int:
    """Count nodes of a given type. Primitive 1."""
    if node_type == "all":
        rows = _safe_query(graph, "MATCH (n) RETURN count(n)")
    else:
        rows = _safe_query(
            graph,
            "MATCH (n) WHERE n.type = $t RETURN count(n)",
            {"t": node_type},
        )
    return rows[0][0] if rows else 0


def mean_energy(graph, node_type: str) -> float:
    """Average energy of nodes of a type. Primitive 2."""
    if node_type == "all":
        rows = _safe_query(graph, "MATCH (n) WHERE n.energy IS NOT NULL RETURN avg(n.energy)")
    else:
        rows = _safe_query(
            graph,
            "MATCH (n) WHERE n.type = $t AND n.energy IS NOT NULL RETURN avg(n.energy)",
            {"t": node_type},
        )
    val = rows[0][0] if rows else None
    return float(val) if val is not None else 0.0


def link_count(graph, src_type: str, tgt_type: str) -> int:
    """Count links from src type to tgt type. Primitive 3."""
    rows = _safe_query(
        graph,
        "MATCH (a)-[]->(b) WHERE a.type = $s AND b.type = $t RETURN count(*)",
        {"s": src_type, "t": tgt_type},
    )
    return rows[0][0] if rows else 0


def min_links(graph, node_type: str, n: int) -> int:
    """Count nodes of a type with at least n outgoing links. Primitive 4."""
    rows = _safe_query(
        graph,
        """
        MATCH (a) WHERE a.type = $t
        OPTIONAL MATCH (a)-[r]->()
        WITH a, count(r) AS degree
        WHERE degree >= $n
        RETURN count(a)
        """,
        {"t": node_type, "n": n},
    )
    return rows[0][0] if rows else 0


def cluster_coefficient(graph, node_type: str) -> float:
    """Internal connectivity of subgraph. Primitive 5.

    Approximation: ratio of actual links to possible links among nodes of this type.
    """
    if node_type == "all":
        type_filter = ""
        params = {}
    else:
        type_filter = "WHERE n.type = $t AND m.type = $t"
        params = {"t": node_type}

    # Count nodes
    if node_type == "all":
        n_rows = _safe_query(graph, "MATCH (n) RETURN count(n)")
    else:
        n_rows = _safe_query(graph, "MATCH (n) WHERE n.type = $t RETURN count(n)", {"t": node_type})
    n_count = n_rows[0][0] if n_rows else 0
    if n_count < 2:
        return 0.0

    # Count links within type
    if node_type == "all":
        e_rows = _safe_query(graph, "MATCH (n)-[r]->(m) RETURN count(r)")
    else:
        e_rows = _safe_query(
            graph,
            "MATCH (n)-[r]->(m) WHERE n.type = $t AND m.type = $t RETURN count(r)",
            {"t": node_type},
        )
    e_count = e_rows[0][0] if e_rows else 0

    possible = n_count * (n_count - 1)
    return min(1.0, e_count / possible) if possible > 0 else 0.0


def drive(graph, drive_name: str) -> float:
    """Get drive value by name from limbic state. Primitive 6."""
    # Drives are stored as properties on a limbic/state node, or as separate nodes
    # Try property on state node first
    rows = _safe_query(
        graph,
        "MATCH (n) WHERE n.type = 'limbic_state' RETURN n",
    )
    if rows:
        node = rows[0][0]
        props = node.properties if hasattr(node, "properties") else {}
        val = props.get(drive_name, props.get(f"drive_{drive_name}", 0.0))
        return float(val) if val is not None else 0.0

    # Fallback: drive as a separate node
    rows = _safe_query(
        graph,
        "MATCH (n) WHERE n.type = 'drive' AND n.name = $d RETURN n.intensity",
        {"d": drive_name},
    )
    return float(rows[0][0]) if rows and rows[0][0] is not None else 0.0


def recency(graph, node_type: str) -> float:
    """Freshness score based on newest nodes. Primitive 7.

    Returns 0-1: 1.0 = created within last hour, decays with 7-day half-life.
    """
    rows = _safe_query(
        graph,
        "MATCH (n) WHERE n.type = $t AND n.created_at IS NOT NULL "
        "RETURN max(n.created_at)",
        {"t": node_type},
    )
    if not rows or rows[0][0] is None:
        return 0.0

    newest_ts = rows[0][0]
    # Handle both epoch seconds and ISO strings
    if isinstance(newest_ts, str):
        try:
            from datetime import datetime, timezone

            dt = datetime.fromisoformat(newest_ts.replace("Z", "+00:00"))
            newest_epoch = dt.timestamp()
        except Exception:
            return 0.0
    else:
        newest_epoch = float(newest_ts)

    age_hours = (time.time() - newest_epoch) / 3600
    half_life = 168  # 7 days
    return max(0.0, min(1.0, 0.5 ** (age_hours / half_life)))


# ── High-Level: Read Brain Stats ─────────────────────────────────────────────


def _read_raw_topology(graph) -> dict:
    """Read raw topology stats. What actually exists, not what we wish existed."""
    total_nodes = count(graph, "all")
    total_links_rows = _safe_query(graph, "MATCH ()-[r]->() RETURN count(r)")
    total_links = total_links_rows[0][0] if total_links_rows else 0

    # Type distribution — what types actually exist
    type_rows = _safe_query(
        graph,
        "MATCH (n) RETURN COALESCE(n.type, '') AS t, count(n) AS c ORDER BY c DESC",
    )
    type_dist = {}
    typed = 0
    untyped = 0
    for row in type_rows:
        t, c = row[0], row[1]
        if t and t.strip():
            type_dist[t] = c
            typed += c
        else:
            untyped += c

    # Mean energy across ALL nodes
    energy_all = mean_energy(graph, "all")

    # Newest node age
    newest_rows = _safe_query(
        graph,
        "MATCH (n) WHERE n.created_at IS NOT NULL RETURN max(n.created_at)",
    )
    newest_age = -1.0
    if newest_rows and newest_rows[0][0] is not None:
        ts = newest_rows[0][0]
        if isinstance(ts, str):
            try:
                from datetime import datetime
                dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                newest_age = (time.time() - dt.timestamp()) / 3600
            except Exception:
                pass
        else:
            newest_age = (time.time() - float(ts)) / 3600

    return {
        "total_nodes": total_nodes,
        "total_links": total_links,
        "link_density": total_links / max(total_nodes, 1),
        "type_distribution": type_dist,
        "typed_node_count": typed,
        "untyped_node_count": untyped,
        "has_backstory": "backstory" in type_dist,
        "has_personality": "personality" in type_dist,
        "has_health_feedback": "health_feedback" in type_dist,
        "health_feedback_count": type_dist.get("health_feedback", 0),
        "mean_energy_all": energy_all,
        "newest_node_age_hours": newest_age,
    }


def read_brain_topology(handle: str) -> BrainStats:
    """Compute all brain stats for a citizen. Topology only, never content."""
    try:
        graph = _get_graph(handle)
    except Exception as e:
        logger.error(f"Cannot reach brain graph for {handle}: {e}")
        return BrainStats(reachable=False)

    desire_ct = count(graph, "desire")
    desire_with_links = min_links(graph, "desire", 1)
    desire_with_3links = min_links(graph, "desire", 3)

    raw = _read_raw_topology(graph)

    return BrainStats(
        desire_count=desire_ct,
        desire_energy=mean_energy(graph, "desire"),
        desire_moment_ratio=desire_with_links / max(desire_ct, 1),
        desire_persistence=desire_with_3links / max(desire_with_links, 1),
        concept_count=count(graph, "concept"),
        process_count=count(graph, "process"),
        value_count=count(graph, "value"),
        memory_count=count(graph, "memory"),
        cluster_coefficient=cluster_coefficient(graph, "all"),
        curiosity=drive(graph, "curiosity"),
        frustration=drive(graph, "frustration"),
        ambition=drive(graph, "ambition"),
        social_need=drive(graph, "social_need"),
        recency_desire=recency(graph, "desire"),
        recency_moment=recency(graph, "moment"),
        reachable=True,
        **raw,
    )
