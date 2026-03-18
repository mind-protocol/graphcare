"""
Universe Scan Data Extractor — extract L3 universe graph for 3D visualization.

DOCS: docs/care/graph_scan/PATTERNS_Graph_Scan.md

Port of graph_scan_data_extractor for L3 (universe-level) graphs.
Same pipeline: FalkorDB → semantic positioning (UMAP) → visual properties → JSON.

Key L3 differences from L1:
  - 5 universal node types: actor, moment, narrative, space, thing
  - relation_kind is always NULL — link meaning from 13 dimensions
  - No limbic system, no emotions, no drives
  - Larger scale (potentially thousands of nodes)
  - Trust is the primary relational signal (not self_relevance)
  - Hierarchy dimension matters (contains/extends/peers)
"""

import json
import logging
import math
import random
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

from falkordb import FalkorDB

logger = logging.getLogger("graphcare.universe_scan")

FALKORDB_HOST = "localhost"
FALKORDB_PORT = 6379

# L3 node type → color (organic palette, distinct from L1)
L3_COLORS = {
    "actor":     "#c4a040",  # old gold — entities that act
    "moment":    "#c47058",  # terracotta — events
    "narrative": "#8a6ab0",  # lavender — interpretive structure
    "space":     "#5a8a6a",  # sage — containers
    "thing":     "#5878a0",  # steel blue — objects/abstractions
}

# Link semantics: since relation_kind is null, color from hierarchy
def _link_color_from_hierarchy(hierarchy: float, valence: float) -> int:
    if hierarchy < -0.5:
        return 0x5a8a6a   # sage — containment
    elif hierarchy > 0.5:
        return 0x8a6ab0   # lavender — elaboration
    elif valence > 0.3:
        return 0x5878a0   # steel — constructive
    elif valence < -0.3:
        return 0xc47058   # terracotta — destructive
    else:
        return 0x484850   # neutral gray


def _node_radius(weight: float) -> float:
    # L3 needs bigger radius than L1 — more nodes, need visibility
    return 2.0 + 3.0 * math.log1p(weight * 3.0)

def _node_glow(energy: float) -> float:
    if energy < 0.1:
        return 0.0
    return min(1.0, 1.0 / (1.0 + math.exp(-3.0 * (energy - 0.5))))

def _node_opacity(stability: float) -> float:
    return 0.3 + 0.7 * stability

def _link_opacity(trust: float, weight: float) -> float:
    return 0.1 + 0.6 * trust + 0.3 * min(1.0, weight)


@dataclass
class ScanNode:
    id: str
    node_type: str
    label: str
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    weight: float = 0.5
    energy: float = 0.0
    stability: float = 0.0
    recency: float = 0.0
    color: str = "#484850"
    radius: float = 3.0
    glow: float = 0.0
    opacity: float = 0.5


@dataclass
class ScanLink:
    source: str
    target: str
    weight: float = 0.5
    energy: float = 0.0
    trust: float = 0.5
    friction: float = 0.0
    hierarchy: float = 0.0
    permanence: float = 0.5
    valence: float = 0.0
    affinity: float = 0.0
    aversion: float = 0.0
    color: str = "#484850"
    opacity: float = 0.3
    glow: float = 0.0


@dataclass
class UniverseScan:
    graph_name: str
    nodes: list = field(default_factory=list)
    links: list = field(default_factory=list)
    stats: dict = field(default_factory=dict)


def extract_universe_scan(graph_name: str, max_nodes: int = 2000) -> UniverseScan:
    """Extract L3 universe graph with visual properties.

    Args:
        graph_name: FalkorDB graph name
        max_nodes: Maximum nodes to include. For large graphs (40K+),
                   we take the top N by weight. Links only between included nodes.
                   Default 2000 — good balance of detail vs performance.
    """
    import numpy as np

    db = FalkorDB(host=FALKORDB_HOST, port=FALKORDB_PORT)
    graph = db.select_graph(graph_name)

    scan = UniverseScan(graph_name=graph_name)

    # ── Count total ──────────────────────────────────────────────────
    total_rows = graph.query("MATCH (n) RETURN count(n)").result_set
    total_count = total_rows[0][0] if total_rows else 0
    logger.info(f"{graph_name}: {total_count} total nodes")

    # ── Extract nodes (top N by weight if graph is large) ────────────
    if total_count > max_nodes:
        # Sample: top N by weight + energy (most important nodes)
        node_rows = graph.query(
            "MATCH (n) RETURN "
            "n.id, n.node_type, n.type, n.name, n.synthesis, "
            "n.weight, n.energy, n.stability, n.recency "
            f"ORDER BY COALESCE(n.weight, 0) + COALESCE(n.energy, 0) DESC "
            f"LIMIT {max_nodes}"
        ).result_set
        logger.info(f"Sampled top {max_nodes} of {total_count} nodes by weight+energy")
    else:
        node_rows = graph.query(
            "MATCH (n) RETURN "
            "n.id, n.node_type, n.type, n.name, n.synthesis, "
            "n.weight, n.energy, n.stability, n.recency"
        ).result_set

    all_nodes = []
    for row in node_rows:
        nid = row[0] or ""
        ntype = row[1] or row[2] or ""
        label = (row[3] or row[4] or nid)[:60]
        if not nid:
            continue

        weight = float(row[5] or 1.0)
        energy = float(row[6] or 0.3)
        stability = float(row[7] or 0.6)
        recency = float(row[8] or 0.5)

        all_nodes.append({
            "id": nid, "type": ntype, "label": label,
            "weight": weight, "energy": energy,
            "stability": stability, "recency": recency,
        })

    # ── Semantic positioning ─────────────────────────────────────────
    positions = _compute_positions(all_nodes)

    for i, nd in enumerate(all_nodes):
        x, y, z = positions[i]
        ntype = nd["type"]
        color = L3_COLORS.get(ntype, "#484850")

        scan.nodes.append(ScanNode(
            id=nd["id"], node_type=ntype, label=nd["label"],
            x=round(x, 4), y=round(y, 4), z=round(z, 4),
            weight=nd["weight"], energy=nd["energy"],
            stability=nd["stability"], recency=nd["recency"],
            color=color,
            radius=round(_node_radius(nd["weight"]), 1),
            glow=round(_node_glow(nd["energy"]), 2),
            opacity=round(_node_opacity(nd["stability"]), 2),
        ))

    # ── Extract links ────────────────────────────────────────────────
    link_rows = graph.query(
        "MATCH (a)-[r]->(b) RETURN "
        "a.id, b.id, "
        "r.weight, r.energy, r.trust, r.friction, "
        "r.hierarchy, r.permanence, r.valence, "
        "r.affinity, r.aversion"
    ).result_set

    node_ids = {n.id for n in scan.nodes}
    for row in link_rows:
        src, tgt = row[0], row[1]
        if not src or not tgt or src not in node_ids or tgt not in node_ids:
            continue

        weight = float(row[2] or 0.5)
        energy = float(row[3] or 0.0)
        trust = float(row[4] or 0.5)
        friction = float(row[5] or 0.0)
        hierarchy = float(row[6] or 0.0)
        permanence = float(row[7] or 0.5)
        valence = float(row[8] or 0.0)
        affinity = float(row[9] or 0.0)
        aversion = float(row[10] or 0.0)

        color_hex = _link_color_from_hierarchy(hierarchy, valence)
        color_str = f"#{color_hex:06x}"

        scan.links.append(ScanLink(
            source=src, target=tgt,
            weight=weight, energy=energy, trust=trust,
            friction=friction, hierarchy=hierarchy,
            permanence=permanence, valence=valence,
            affinity=affinity, aversion=aversion,
            color=color_str,
            opacity=round(_link_opacity(trust, weight), 2),
            glow=round(min(1.0, energy * 2.0), 2),
        ))

    # ── Stats ────────────────────────────────────────────────────────
    type_counts = {}
    for n in scan.nodes:
        t = n.node_type
        type_counts[t] = type_counts.get(t, 0) + 1

    scan.stats = {
        "total_nodes": len(scan.nodes),
        "total_links": len(scan.links),
        "total_in_graph": total_count,
        "sampled": total_count > max_nodes,
        "type_counts": type_counts,
    }

    return scan


def _compute_positions(nodes: list[dict]) -> list[tuple]:
    """Compute 3D positions. Same UMAP approach, adapted for L3 scale."""
    import numpy as np

    if len(nodes) < 5:
        golden = math.pi * (3 - math.sqrt(5))
        return [
            (round(0.4 * math.sin(math.acos(1-2*(i+0.5)/max(len(nodes),1))) * math.cos(i*golden), 4),
             round(0.4 * math.sin(math.acos(1-2*(i+0.5)/max(len(nodes),1))) * math.sin(i*golden), 4),
             round(0.4 * math.cos(math.acos(1-2*(i+0.5)/max(len(nodes),1))) + 0.4, 4))
            for i in range(len(nodes))
        ]

    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        import umap

        # Use label + id for semantic signal (strip type to prevent clustering)
        contents = []
        for nd in nodes:
            text = nd["id"].replace(":", " ").replace("_", " ") + " " + nd["label"]
            # Strip type prefix
            text = text.replace(nd["type"], "").strip()
            contents.append(text if text.strip() else nd["id"])

        tfidf = TfidfVectorizer(max_features=300, stop_words='english')
        X = tfidf.fit_transform(contents).toarray()

        # Subtract per-type centroid
        type_indices: dict[str, list[int]] = {}
        for i, nd in enumerate(nodes):
            t = nd["type"]
            if t not in type_indices:
                type_indices[t] = []
            type_indices[t].append(i)

        for t, indices in type_indices.items():
            if len(indices) > 1:
                centroid = np.mean(X[indices], axis=0)
                for idx in indices:
                    X[idx] -= centroid

        n_neighbors = min(20, len(nodes) - 1)
        reducer = umap.UMAP(
            n_components=3, n_neighbors=n_neighbors,
            min_dist=0.05, spread=0.8, metric='cosine', random_state=42,
        )
        coords = reducer.fit_transform(X)

        # Normalize
        for dim in range(3):
            col = coords[:, dim]
            mn, mx = col.min(), col.max()
            if mx - mn > 0:
                coords[:, dim] = (col - mn) / (mx - mn) * 0.8 - 0.4

        positions = []
        for i, nd in enumerate(nodes):
            x, y, z = coords[i]
            # Weight pulls toward center
            pull = 1.0 - nd["weight"] * 0.2
            x *= pull
            y *= pull
            z = z * pull + 0.4
            positions.append((round(float(x), 4), round(float(y), 4), round(float(z), 4)))
        return positions

    except Exception as e:
        logger.warning(f"UMAP failed for universe scan: {e}")
        golden = math.pi * (3 - math.sqrt(5))
        n = len(nodes)
        return [
            (round(0.5 * math.sin(math.acos(1-2*(i+0.5)/max(n,1))) * math.cos(i*golden), 4),
             round(0.5 * math.sin(math.acos(1-2*(i+0.5)/max(n,1))) * math.sin(i*golden), 4),
             round(0.5 * math.cos(math.acos(1-2*(i+0.5)/max(n,1))) + 0.4, 4))
            for i in range(n)
        ]


def save_scan(scan: UniverseScan, output_path: Path):
    data = {
        "graph_name": scan.graph_name,
        "scan_type": "universe_l3",
        "nodes": [asdict(n) for n in scan.nodes],
        "links": [asdict(l) for l in scan.links],
        "stats": scan.stats,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(data, indent=2))


if __name__ == "__main__":
    import sys
    graph_name = sys.argv[1] if len(sys.argv) > 1 else "lumina_prime"
    max_n = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
    scan = extract_universe_scan(graph_name, max_nodes=max_n)
    out = Path(f"data/graph_scans/{graph_name}_universe_scan.json")
    save_scan(scan, out)
    print(f"Universe scan: {scan.stats}")
