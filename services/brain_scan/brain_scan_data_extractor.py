"""
Brain Scan Data Extractor — extract brain topology for 3D visualization.

DOCS: docs/care/brain_scan/ (to be created)

Extracts brain data from FalkorDB and computes 3D positions for visualization.
The positioning is semantic-topological: nodes are placed based on their type
(anatomy layer) and connections (clustering), creating brain-like folds.

Output: JSON file ready for a 3D renderer (Three.js, Plotly, etc.)

Anatomy mapping:
  - STEM (z=0.0-0.2):    process nodes — the basic machinery
  - LIMBIC (z=0.2-0.5):  desire, narrative (shadow emotions) — drives and feelings
  - CORTEX (z=0.5-1.0):  value, concept — higher reasoning
  - NARRATIVE (z=0.3-0.7): narrative nodes — cross-cutting, distributed

Visual property mapping:
  - Node color:     by type (desire=red, concept=blue, value=gold, process=green, narrative=purple)
  - Node size:      weight (0-1 → 3-15px)
  - Node glow:      energy (>0.3 = glowing)
  - Link opacity:   weight (0-1 → 0.1-1.0)
  - Link color:     by relation_kind (supports=blue, contradicts=red, activates=green, etc.)
  - Link width:     trust (0-1 → 0.5-3px)
  - Link glow:      energy > 0.5
"""

import json
import logging
import math
import random
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

from falkordb import FalkorDB

logger = logging.getLogger("graphcare.brain_scan")

FALKORDB_HOST = "localhost"
FALKORDB_PORT = 6379

# ── Anatomy layers ───────────────────────────────────────────────────────

LAYER_Z = {
    "process":   (0.0, 0.2),    # stem
    "desire":    (0.25, 0.45),   # limbic — wants
    "narrative": (0.3, 0.7),     # distributed across layers
    "value":     (0.55, 0.8),    # cortex — principles
    "concept":   (0.7, 1.0),     # cortex — abstractions
}

NODE_COLORS = {
    "process":   "#22c55e",  # green
    "desire":    "#ef4444",  # red
    "narrative": "#a855f7",  # purple
    "value":     "#eab308",  # gold
    "concept":   "#3b82f6",  # blue
    "stimulus":  "#f97316",  # orange
    "frequency": "#06b6d4",  # cyan
}

LINK_COLORS = {
    "supports":     "#3b82f6",  # blue
    "contradicts":  "#ef4444",  # red
    "activates":    "#22c55e",  # green
    "causes":       "#f97316",  # orange
    "reminds_of":   "#a855f7",  # purple
    "depends_on":   "#6b7280",  # gray
    "regulates":    "#eab308",  # gold
    "exemplifies":  "#06b6d4",  # cyan
    "associates":   "#9ca3af",  # light gray
}


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
    color: str = "#9ca3af"
    size: float = 5.0
    glow: bool = False
    layer: str = "cortex"


@dataclass
class ScanLink:
    source: str
    target: str
    relation: str
    weight: float = 0.5
    energy: float = 0.0
    trust: float = 0.5
    color: str = "#9ca3af"
    width: float = 1.0
    opacity: float = 0.3
    glow: bool = False


@dataclass
class BrainScan:
    citizen_id: str
    nodes: list = field(default_factory=list)
    links: list = field(default_factory=list)
    stats: dict = field(default_factory=dict)


def extract_brain_scan(citizen_handle: str) -> BrainScan:
    """Extract full brain data positioned for 3D visualization."""
    db = FalkorDB(host=FALKORDB_HOST, port=FALKORDB_PORT)
    graph = db.select_graph(f"brain_{citizen_handle}")

    scan = BrainScan(citizen_id=citizen_handle)

    # ── Extract nodes ────────────────────────────────────────────────
    node_rows = graph.query(
        "MATCH (n) RETURN n.id, n.type, n.node_type, n.name, n.weight, n.energy"
    ).result_set

    # Group by type for cluster positioning
    type_groups: dict[str, list] = {}
    node_map = {}

    for row in node_rows:
        nid = row[0] or ""
        ntype = row[1] or row[2] or ""
        label = (row[3] or nid)[:50]
        weight = float(row[4] or 0.5)
        energy = float(row[5] or 0.0)

        if not nid:
            continue

        if ntype not in type_groups:
            type_groups[ntype] = []
        type_groups[ntype].append((nid, label, weight, energy))
        node_map[nid] = ntype

    # ── Position nodes ───────────────────────────────────────────────
    # Semantic-topological: type determines Z layer, position within
    # layer is spread in a brain-like ellipsoid using golden angle spiral
    for ntype, group in type_groups.items():
        z_lo, z_hi = LAYER_Z.get(ntype, (0.4, 0.6))
        color = NODE_COLORS.get(ntype, "#9ca3af")
        layer = _layer_name(ntype)

        n = len(group)
        for i, (nid, label, weight, energy) in enumerate(group):
            # Golden angle spiral within the layer's z-band
            # Creates a natural, non-grid distribution
            golden_angle = math.pi * (3 - math.sqrt(5))  # ~137.5°
            theta = i * golden_angle
            # Radius varies with index for spread
            r = 0.3 + 0.4 * math.sqrt(i / max(n, 1))
            # Add weight-based displacement (heavier = more central)
            r *= (1.2 - weight * 0.4)

            x = r * math.cos(theta)
            y = r * math.sin(theta)
            z = z_lo + (z_hi - z_lo) * (i / max(n - 1, 1))
            # Add small jitter for organic feel
            x += random.gauss(0, 0.02)
            y += random.gauss(0, 0.02)
            z += random.gauss(0, 0.01)

            size = 3 + weight * 12
            glow = energy > 0.3

            scan.nodes.append(ScanNode(
                id=nid, node_type=ntype, label=label,
                x=round(x, 4), y=round(y, 4), z=round(z, 4),
                weight=weight, energy=energy,
                color=color, size=round(size, 1), glow=glow,
                layer=layer,
            ))

    # ── Extract links ────────────────────────────────────────────────
    link_rows = graph.query(
        "MATCH (a)-[r]->(b) "
        "RETURN a.id, b.id, r.relation_kind, r.weight, r.energy, r.trust"
    ).result_set

    for row in link_rows:
        src, tgt = row[0], row[1]
        relation = row[2] or "associates"
        weight = float(row[3] or 0.5)
        energy = float(row[4] or 0.0)
        trust = float(row[5] or 0.5)

        if not src or not tgt:
            continue

        color = LINK_COLORS.get(relation, "#9ca3af")
        width = 0.5 + trust * 2.5
        opacity = 0.1 + weight * 0.9
        glow = energy > 0.5

        scan.links.append(ScanLink(
            source=src, target=tgt, relation=relation,
            weight=weight, energy=energy, trust=trust,
            color=color, width=round(width, 2),
            opacity=round(opacity, 2), glow=glow,
        ))

    # ── Stats ────────────────────────────────────────────────────────
    type_counts = {t: len(g) for t, g in type_groups.items()}
    scan.stats = {
        "total_nodes": len(scan.nodes),
        "total_links": len(scan.links),
        "type_counts": type_counts,
        "layers": {
            "stem": sum(1 for n in scan.nodes if n.layer == "stem"),
            "limbic": sum(1 for n in scan.nodes if n.layer == "limbic"),
            "cortex": sum(1 for n in scan.nodes if n.layer == "cortex"),
        },
    }

    logger.info(
        f"Brain scan extracted for {citizen_handle}: "
        f"{len(scan.nodes)} nodes, {len(scan.links)} links"
    )
    return scan


def _layer_name(ntype: str) -> str:
    z_lo, _ = LAYER_Z.get(ntype, (0.5, 0.5))
    if z_lo < 0.25:
        return "stem"
    elif z_lo < 0.5:
        return "limbic"
    return "cortex"


def save_scan(scan: BrainScan, output_path: Path):
    """Save brain scan as JSON for visualization."""
    data = {
        "citizen_id": scan.citizen_id,
        "nodes": [asdict(n) for n in scan.nodes],
        "links": [asdict(l) for l in scan.links],
        "stats": scan.stats,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(data, indent=2))
    logger.info(f"Brain scan saved to {output_path}")


if __name__ == "__main__":
    import sys
    handle = sys.argv[1] if len(sys.argv) > 1 else "dragon_slayer"
    scan = extract_brain_scan(handle)
    out = Path(f"data/brain_scans/{handle}_scan.json")
    save_scan(scan, out)
    print(f"Scan: {scan.stats}")
