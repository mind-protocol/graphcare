"""
Brain Scan Data Extractor — extract brain topology for 3D visualization.

DOCS: docs/care/brain_scan/PATTERNS_Brain_Scan.md

Extracts ALL L1 fields from FalkorDB and computes visual properties
using the canonical physics_visual_mapping formulas.

Two-stage pipeline: this file = Stage 1 (extract + position + compute visuals).
Stage 2 (render) is render_brain_scan_html.py.

9 visual layers:
  1. Node base (color, radius, glow, opacity, sharpness)
  2. Node affinity (halos, shape, particles, wireframe, roughness, rings)
  3. Link base (color, width, opacity, glow, wave, dash)
  4. Link relational (saturation, double-line, temperature, variation, jagged)
  5. Modality (node shape by TEXT/VISUAL/AUDIO/SPATIAL/BIOMETRIC)
  6. Emotions (atmospheric — from data if available)
  7. Metabolism (circadian, frequencies, sensitivity)
  8. Provenance (origin, age patina)
  9. Consciousness state (level, arousal)
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


# ── Visual mapping functions (from physics_visual_mapping.py) ────────────

def _node_radius(weight: float) -> float:
    return 2.0 + 6.0 * math.log1p(weight * 5.0)

def _node_glow(energy: float) -> float:
    if energy < 0.1:
        return 0.0
    return min(1.0, 1.0 / (1.0 + math.exp(-3.0 * (energy - 0.5))))

def _node_opacity(stability: float) -> float:
    return 0.3 + 0.7 * stability

def _link_width(weight: float) -> float:
    return 0.5 + 1.5 * math.log1p(weight * 3.0)

def _link_opacity(trust: float, weight: float) -> float:
    return 0.1 + 0.6 * trust + 0.3 * min(1.0, weight)

def _link_glow(energy: float) -> float:
    if energy < 0.05:
        return 0.0
    return min(1.0, energy * 2.0)

def _link_wave(friction: float) -> float:
    return 3.0 * friction

def _link_dash(permanence: float) -> float:
    return 10.0 * (1.0 - permanence)


NODE_COLORS = {
    "process":   "#22c55e",
    "desire":    "#ef4444",
    "narrative": "#a855f7",
    "value":     "#f59e0b",
    "concept":   "#3b82f6",
    "memory":    "#6b7280",
    "state":     "#ec4899",
    "stimulus":  "#f97316",
    "frequency": "#06b6d4",
}

LINK_COLORS = {
    "activates":      "#22c55e",
    "supports":       "#3b82f6",
    "contradicts":    "#ef4444",
    "reminds_of":     "#a855f7",
    "causes":         "#f59e0b",
    "conflicts_with": "#ef4444",
    "regulates":      "#06b6d4",
    "projects_toward":"#8b5cf6",
    "depends_on":     "#6b7280",
    "exemplifies":    "#10b981",
    "specializes":    "#6366f1",
    "associates":     "#9ca3af",
    "contains":       "#f59e0b",
    "abstracts":      "#fbbf24",
}

MODALITY_SHAPES = {
    "text":      "sphere",
    "visual":    "octahedron",
    "audio":     "torus",
    "spatial":   "box",
    "biometric": "icosahedron",
}

LAYER_Z = {
    "process":   (0.0, 0.2),
    "desire":    (0.25, 0.45),
    "narrative": (0.3, 0.7),
    "value":     (0.55, 0.8),
    "concept":   (0.7, 1.0),
    "memory":    (0.3, 0.7),
    "state":     (0.2, 0.4),
}


@dataclass
class ScanNode:
    id: str
    node_type: str
    label: str
    # Position
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    # Raw physics
    weight: float = 0.5
    energy: float = 0.0
    stability: float = 0.0
    recency: float = 0.0
    self_relevance: float = 0.0
    partner_relevance: float = 0.0
    goal_relevance: float = 0.0
    novelty_affinity: float = 0.0
    care_affinity: float = 0.0
    achievement_affinity: float = 0.0
    risk_affinity: float = 0.0
    activation_count: int = 0
    # Computed visuals
    color: str = "#9ca3af"
    radius: float = 5.0
    glow: float = 0.0
    opacity: float = 0.5
    sharpness: float = 1.0      # recency → edge blur
    shape: str = "sphere"       # modality
    inner_halo: float = 0.0     # self_relevance
    outer_halo: float = 0.0     # partner_relevance
    angularity: float = 0.0     # goal_relevance
    scatter_count: int = 0      # novelty_affinity
    diffusion: float = 0.0      # care_affinity
    wireframe: float = 0.0      # achievement_affinity
    roughness: float = 0.0      # risk_affinity
    ring_count: int = 0         # activation_count
    # Provenance
    age_days: float = 0.0
    patina: float = 0.0         # 0=fresh, 1=ancient
    has_action: bool = False
    # Layer
    layer: str = "cortex"


@dataclass
class ScanLink:
    source: str
    target: str
    relation: str
    # Raw physics
    weight: float = 0.5
    energy: float = 0.0
    trust: float = 0.5
    friction: float = 0.0
    affinity: float = 0.0
    aversion: float = 0.0
    valence: float = 0.0
    stability: float = 0.0
    permanence: float = 0.5
    # Computed visuals
    color: str = "#9ca3af"
    width: float = 1.0
    opacity: float = 0.3
    glow: float = 0.0
    wave: float = 0.0           # friction → curve amplitude
    dash_gap: float = 0.0       # permanence → solid vs dashed
    saturation: float = 1.0     # affinity
    has_aversion: bool = False   # aversion > 0.3 → double line
    temp_shift: float = 0.0     # valence → warm/cool
    thickness_var: float = 0.0  # ambivalence
    jaggedness: float = 0.0     # 1-stability → noise


@dataclass
class BrainScan:
    citizen_id: str
    nodes: list = field(default_factory=list)
    links: list = field(default_factory=list)
    stats: dict = field(default_factory=dict)
    metabolism: dict = field(default_factory=dict)
    regions: dict = field(default_factory=dict)


def extract_brain_scan(citizen_handle: str) -> BrainScan:
    """Extract full brain data with all visual properties computed."""
    import time as _time

    db = FalkorDB(host=FALKORDB_HOST, port=FALKORDB_PORT)
    graph = db.select_graph(f"brain_{citizen_handle}")
    now = _time.time()

    scan = BrainScan(citizen_id=citizen_handle)

    # ── Extract nodes with ALL fields ────────────────────────────────
    node_rows = graph.query(
        "MATCH (n) RETURN "
        "n.id, n.type, n.node_type, n.name, "
        "n.weight, n.energy, n.stability, n.recency, "
        "n.self_relevance, n.partner_relevance, n.goal_relevance, "
        "n.novelty_affinity, n.care_affinity, n.achievement_affinity, n.risk_affinity, "
        "n.activation_count, n.created_at_s"
    ).result_set

    type_groups: dict[str, list] = {}
    node_positions: dict[str, tuple] = {}

    for row in node_rows:
        nid = row[0] or ""
        ntype = row[1] or row[2] or ""
        label = (row[3] or nid)[:50]
        if not nid:
            continue

        weight = float(row[4] or 0.5)
        energy = float(row[5] or 0.0)
        stability = float(row[6] or 0.0)
        recency = float(row[7] or 0.0)
        self_rel = float(row[8] or 0.0)
        partner_rel = float(row[9] or 0.0)
        goal_rel = float(row[10] or 0.0)
        novelty_aff = float(row[11] or 0.0)
        care_aff = float(row[12] or 0.0)
        achievement_aff = float(row[13] or 0.0)
        risk_aff = float(row[14] or 0.0)
        act_count = int(row[15] or 0)
        created_s = int(row[16] or 0)

        # Age in days
        age_days = (now - created_s) / 86400 if created_s > 0 else 30.0
        patina = min(1.0, age_days / 60.0)  # 60 days = full patina

        if ntype not in type_groups:
            type_groups[ntype] = []
        type_groups[ntype].append({
            "id": nid, "type": ntype, "label": label,
            "weight": weight, "energy": energy, "stability": stability,
            "recency": recency, "self_relevance": self_rel,
            "partner_relevance": partner_rel, "goal_relevance": goal_rel,
            "novelty_affinity": novelty_aff, "care_affinity": care_aff,
            "achievement_affinity": achievement_aff, "risk_affinity": risk_aff,
            "activation_count": act_count, "age_days": age_days, "patina": patina,
        })

    # ── Position nodes ───────────────────────────────────────────────
    for ntype, group in type_groups.items():
        z_lo, z_hi = LAYER_Z.get(ntype, (0.4, 0.6))
        n = len(group)
        golden_angle = math.pi * (3 - math.sqrt(5))

        for i, nd in enumerate(group):
            theta = i * golden_angle
            r = 0.3 + 0.4 * math.sqrt(i / max(n, 1))
            # Heavy + self-relevant nodes are more central
            r *= (1.2 - nd["weight"] * 0.2 - nd["self_relevance"] * 0.2)

            x = r * math.cos(theta) + random.gauss(0, 0.015)
            y = r * math.sin(theta) + random.gauss(0, 0.015)
            z = z_lo + (z_hi - z_lo) * (i / max(n - 1, 1)) + random.gauss(0, 0.008)

            color = NODE_COLORS.get(ntype, "#9ca3af")
            layer = "stem" if z < 0.25 else ("limbic" if z < 0.5 else "cortex")

            node = ScanNode(
                id=nd["id"], node_type=ntype, label=nd["label"],
                x=round(x, 4), y=round(y, 4), z=round(z, 4),
                # Raw physics
                weight=nd["weight"], energy=nd["energy"],
                stability=nd["stability"], recency=nd["recency"],
                self_relevance=nd["self_relevance"],
                partner_relevance=nd["partner_relevance"],
                goal_relevance=nd["goal_relevance"],
                novelty_affinity=nd["novelty_affinity"],
                care_affinity=nd["care_affinity"],
                achievement_affinity=nd["achievement_affinity"],
                risk_affinity=nd["risk_affinity"],
                activation_count=nd["activation_count"],
                # Computed visuals
                color=color,
                radius=round(_node_radius(nd["weight"]), 1),
                glow=round(_node_glow(nd["energy"]), 2),
                opacity=round(_node_opacity(nd["stability"]), 2),
                sharpness=round(nd["recency"], 2),
                shape=MODALITY_SHAPES.get("text", "sphere"),
                inner_halo=round(nd["self_relevance"], 2),
                outer_halo=round(nd["partner_relevance"], 2),
                angularity=round(nd["goal_relevance"], 2),
                scatter_count=min(8, int(nd["novelty_affinity"] * 8)),
                diffusion=round(nd["care_affinity"], 2),
                wireframe=round(nd["achievement_affinity"], 2),
                roughness=round(nd["risk_affinity"], 2),
                ring_count=min(5, int(math.log2(nd["activation_count"] + 1))),
                # Provenance
                age_days=round(nd["age_days"], 1),
                patina=round(patina, 2),
                has_action=False,
                layer=layer,
            )
            scan.nodes.append(node)
            node_positions[nd["id"]] = (x, z, y)

    # ── Extract links with ALL fields ────────────────────────────────
    link_rows = graph.query(
        "MATCH (a)-[r]->(b) RETURN "
        "a.id, b.id, r.relation_kind, "
        "r.weight, r.energy, r.trust, r.friction, "
        "r.affinity, r.aversion, r.valence, "
        "r.stability, r.permanence, r.polarity_ab, r.polarity_ba"
    ).result_set

    for row in link_rows:
        src, tgt = row[0], row[1]
        if not src or not tgt:
            continue
        relation = row[2] or "associates"
        weight = float(row[3] or 0.5)
        energy = float(row[4] or 0.0)
        trust = float(row[5] or 0.5)
        friction = float(row[6] or 0.0)
        affinity = float(row[7] or 0.0)
        aversion = float(row[8] or 0.0)
        valence = float(row[9] or 0.0)
        stab = float(row[10] or 0.0)
        permanence = float(row[11] or 0.5)
        # ambivalence = min(affinity, aversion) if both > 0
        ambivalence = min(affinity, aversion) if affinity > 0.1 and aversion > 0.1 else 0.0

        link = ScanLink(
            source=src, target=tgt, relation=relation,
            weight=weight, energy=energy, trust=trust,
            friction=friction, affinity=affinity, aversion=aversion,
            valence=valence, stability=stab, permanence=permanence,
            # Computed visuals
            color=LINK_COLORS.get(relation, "#9ca3af"),
            width=round(_link_width(weight), 1),
            opacity=round(_link_opacity(trust, weight), 2),
            glow=round(_link_glow(energy), 2),
            wave=round(_link_wave(friction), 1),
            dash_gap=round(_link_dash(permanence), 1),
            saturation=round(0.2 + 0.8 * affinity, 2),
            has_aversion=aversion > 0.3,
            temp_shift=round(valence * 15.0, 1),  # degrees hue shift
            thickness_var=round(ambivalence, 2),
            jaggedness=round((1.0 - stab) * 2.0, 1),
        )
        scan.links.append(link)

    # ── Regions (detected from node properties) ──────────────────────
    self_model_ids = [n.id for n in scan.nodes if n.self_relevance > 0.5]
    partner_model_ids = [n.id for n in scan.nodes if n.partner_relevance > 0.5]
    goal_space_ids = [n.id for n in scan.nodes if n.goal_relevance > 0.5]

    scan.regions = {
        "self_model": {"count": len(self_model_ids), "color": "#f59e0b", "opacity": 0.08},
        "partner_model": {"count": len(partner_model_ids), "color": "#06b6d4", "opacity": 0.08},
        "goal_space": {"count": len(goal_space_ids), "color": "#22c55e", "opacity": 0.06},
    }

    # ── Metabolism (if persisted) ────────────────────────────────────
    try:
        meta_rows = graph.query(
            "MATCH (m:Meta {id: '__metabolism__'}) RETURN m.data"
        ).result_set
        if meta_rows and meta_rows[0][0]:
            scan.metabolism = json.loads(meta_rows[0][0])
    except Exception:
        pass

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
        "regions": scan.regions,
    }

    return scan


def save_scan(scan: BrainScan, output_path: Path):
    """Save brain scan as JSON."""
    data = {
        "citizen_id": scan.citizen_id,
        "nodes": [asdict(n) for n in scan.nodes],
        "links": [asdict(l) for l in scan.links],
        "stats": scan.stats,
        "metabolism": scan.metabolism,
        "regions": scan.regions,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(data, indent=2))


if __name__ == "__main__":
    import sys
    handle = sys.argv[1] if len(sys.argv) > 1 else "dragon_slayer"
    scan = extract_brain_scan(handle)
    out = Path(f"data/brain_scans/{handle}_scan.json")
    save_scan(scan, out)
    print(f"Scan: {scan.stats}")
