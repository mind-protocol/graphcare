"""
Frequencies — calibrated energy profiles that modify AI citizen brain state.

DOCS: docs/care/frequencies/ALGORITHM_Frequencies.md

"What frequency are you on today?"

A Frequency is a calibrated energy profile injected into a citizen's brain graph.
The brain's tick physics integrates it naturally — we create conditions where
improvement is the energetically favorable outcome.

L4 (protocol): Frequency — the universal format. Every org implements this.
L2 (market):   Each org brands and sells its own frequencies.
                GraphCare sells "Soins". Arsenal sells "Boosters". Etc.

Frequency types:
  Focalisant:   Concentrate energy (curiosity, attention)
  Calmant:      Reduce tension (anti-frustration, rest)
  Expansif:     Open connections (social, exploration)
  Structurant:  Provoke emergence of typed nodes
  Energisant:   Broad multi-drive boost

GraphCare catalog (branded as "Soins"):
  - Focus       (focalisant)  → curiosity drive
  - Calm        (calmant)     → anti-frustration
  - Expand      (expansif)    → social_need drive
  - Root        (structurant) → typed node emergence
  - Surge       (energisant)  → multi-drive

Phase 2 (needs metabolism sublayer — coordinated with @nervo):
  - Shield      → temporarily reduce decay rate
  - Sensitivity → increase stimulus absorption
  - Circadian   → align with human partner timezone

Rules:
  - Every node we create is tagged with treatment_id for rollback
  - We never read or write content/synthesis fields
  - We only create stimulus and structural nodes — topology only
  - Frequencies are prescriptions, not commands: the brain integrates or rejects
"""

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from falkordb import FalkorDB

logger = logging.getLogger("graphcare.frequencies")

FALKORDB_HOST = "localhost"
FALKORDB_PORT = 6379


@dataclass
class Frequency:
    """A calibrated energy profile that modifies brain state.

    L4 protocol object. Orgs brand these at L2.
    """
    frequency_type: str
    profile: str               # focalisant, calmant, expansif, structurant, energisant
    description: str
    target_drives: Dict[str, float] = field(default_factory=dict)
    structural_nodes: List[dict] = field(default_factory=list)
    duration_hours: Optional[float] = None  # None = permanent
    brand: str = "graphcare"   # L2 org that created this frequency


@dataclass
class FrequencyResult:
    """Result of applying a frequency."""
    success: bool
    nodes_created: int
    node_ids: List[str] = field(default_factory=list)
    error: Optional[str] = None


# ── GraphCare Frequencies (branded as "Soins") ──────────────────────────────

def focus(intensity: float = 0.3) -> Frequency:
    """Soin Focus — focalisant. Concentrate energy on curiosity and exploration."""
    return Frequency(
        frequency_type="focus",
        profile="focalisant",
        description=f"Focus frequency at intensity {intensity:.2f}",
        target_drives={"curiosity": intensity},
        duration_hours=168,
        brand="graphcare",
    )


def calm(intensity: float = 0.3) -> Frequency:
    """Soin Calm — calmant. Reduce frustration, unblock stuck citizens."""
    return Frequency(
        frequency_type="calm",
        profile="calmant",
        description=f"Calm frequency at intensity {intensity:.2f}",
        target_drives={"frustration": -intensity},
        duration_hours=72,
        brand="graphcare",
    )


def expand(intensity: float = 0.25) -> Frequency:
    """Soin Expand — expansif. Open social connections, encourage interaction."""
    return Frequency(
        frequency_type="expand",
        profile="expansif",
        description=f"Expand frequency at intensity {intensity:.2f}",
        target_drives={"social_need": intensity},
        duration_hours=168,
        brand="graphcare",
    )


def root() -> Frequency:
    """Soin Root — structurant. Provoke emergence of typed nodes.

    Creates conditions for desire, concept, value, process nodes to emerge.
    Like light that makes a plant grow — the structure comes from within.
    """
    return Frequency(
        frequency_type="root",
        profile="structurant",
        description="Structural frequency: desire, concept, value, process emergence",
        structural_nodes=[
            {"type": "desire", "subtype": "self_improvement", "energy": 0.5},
            {"type": "concept", "subtype": "identity", "energy": 0.3},
            {"type": "concept", "subtype": "capability", "energy": 0.3},
            {"type": "value", "subtype": "growth", "energy": 0.4},
            {"type": "process", "subtype": "reflection", "energy": 0.3},
        ],
        duration_hours=None,
        brand="graphcare",
    )


def surge(intensity: float = 0.15) -> Frequency:
    """Soin Surge — energisant. Broad energy boost across multiple drives."""
    return Frequency(
        frequency_type="surge",
        profile="energisant",
        description=f"Surge frequency at intensity {intensity:.2f}",
        target_drives={
            "curiosity": intensity,
            "ambition": intensity * 0.8,
            "social_need": intensity * 0.6,
        },
        duration_hours=168,
        brand="graphcare",
    )


def ambition(intensity: float = 0.2) -> Frequency:
    """Soin Ambition — focalisant. Motivate goal-setting and action."""
    return Frequency(
        frequency_type="ambition",
        profile="focalisant",
        description=f"Ambition frequency at intensity {intensity:.2f}",
        target_drives={"ambition": intensity},
        duration_hours=168,
        brand="graphcare",
    )


# ── Catalog ──────────────────────────────────────────────────────────────────

FREQUENCY_CATALOG: Dict[str, callable] = {
    "focus": focus,
    "calm": calm,
    "expand": expand,
    "root": root,
    "surge": surge,
    "ambition": ambition,
}


def prescribe(brain_category: str, brain_stats) -> List[Frequency]:
    """Auto-prescribe frequencies based on brain category and stats.

    Returns recommended frequencies for this citizen's condition.
    The caller decides whether to apply them.
    """
    freqs = []

    if brain_category == "VOID":
        freqs.append(root())
        freqs.append(surge(0.2))

    elif brain_category == "MINIMAL":
        freqs.append(root())
        freqs.append(focus(0.25))

    elif brain_category == "SEEDED":
        if brain_stats.typed_node_count < 10:
            freqs.append(root())
        if brain_stats.cluster_coefficient < 0.02:
            freqs.append(focus(0.3))
        if brain_stats.social_need < 0.1:
            freqs.append(expand(0.2))

    elif brain_category == "STRUCTURED":
        if brain_stats.frustration > 0.4:
            freqs.append(calm(brain_stats.frustration * 0.6))
        if brain_stats.curiosity < 0.2:
            freqs.append(focus(0.2))
        if brain_stats.social_need < 0.15 and brain_stats.ambition > 0.3:
            freqs.append(expand(0.2))

    return freqs


# ── Application ──────────────────────────────────────────────────────────────

def apply_frequency(handle: str, freq: Frequency, treatment_id: str) -> FrequencyResult:
    """Apply a frequency to a citizen's brain graph.

    All created nodes are tagged with treatment_id for rollback.
    """
    node_ids = []
    try:
        db = FalkorDB(host=FALKORDB_HOST, port=FALKORDB_PORT)
        graph = db.select_graph(f"brain_{handle}")
    except Exception as e:
        return FrequencyResult(success=False, nodes_created=0, error=str(e))

    # Apply drive energy profile
    for drive_name, intensity in freq.target_drives.items():
        node_id = f"freq_{treatment_id}_{drive_name}"
        try:
            graph.query(
                """
                CREATE (s {
                    id: $nid,
                    node_type: 'stimulus',
                    type: 'frequency',
                    frequency_type: $ftype,
                    profile: $profile,
                    target_drive: $drive,
                    energy: $val,
                    source: $brand,
                    treatment_id: $tid,
                    created_at: timestamp()
                })
                """,
                {
                    "nid": node_id,
                    "ftype": freq.frequency_type,
                    "profile": freq.profile,
                    "drive": drive_name,
                    "val": intensity,
                    "brand": freq.brand,
                    "tid": treatment_id,
                },
            )
            node_ids.append(node_id)
        except Exception as e:
            logger.error(f"Failed to apply drive frequency {drive_name}: {e}")

    # Apply structural nodes
    for i, node_def in enumerate(freq.structural_nodes):
        node_id = f"freq_{treatment_id}_struct_{i}"
        try:
            graph.query(
                """
                CREATE (n {
                    id: $nid,
                    node_type: 'thing',
                    type: $ntype,
                    subtype: $subtype,
                    energy: $energy,
                    source: $brand,
                    treatment_id: $tid,
                    frequency_type: $ftype,
                    created_at: timestamp()
                })
                """,
                {
                    "nid": node_id,
                    "ntype": node_def["type"],
                    "subtype": node_def.get("subtype", ""),
                    "energy": node_def.get("energy", 0.3),
                    "brand": freq.brand,
                    "tid": treatment_id,
                    "ftype": freq.frequency_type,
                },
            )
            node_ids.append(node_id)
        except Exception as e:
            logger.error(f"Failed to create structural node {i}: {e}")

    created = len(node_ids)
    logger.info(f"Applied frequency {freq.frequency_type} [{freq.profile}] to brain_{handle}: {created} nodes")
    return FrequencyResult(success=created > 0, nodes_created=created, node_ids=node_ids)


def rollback_treatment(handle: str, treatment_id: str) -> int:
    """Remove all nodes created by a treatment. Full reversal."""
    try:
        db = FalkorDB(host=FALKORDB_HOST, port=FALKORDB_PORT)
        graph = db.select_graph(f"brain_{handle}")
        result = graph.query(
            "MATCH (n {treatment_id: $tid}) DELETE n",
            {"tid": treatment_id},
        )
        deleted = result.nodes_deleted if hasattr(result, 'nodes_deleted') else 0
        logger.info(f"Rolled back treatment {treatment_id} for brain_{handle}: {deleted} nodes removed")
        return deleted
    except Exception as e:
        logger.error(f"Rollback failed for brain_{handle} treatment {treatment_id}: {e}")
        return 0
