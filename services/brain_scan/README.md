# Brain Scan — 3D Citizen Brain Visualization

**GraphCare's diagnostic imaging tool.** Extracts brain topology from FalkorDB and renders an interactive 3D visualization in standalone HTML.

## Quick Start

```bash
cd /home/mind-protocol/graphcare

# 1. Extract brain data → JSON
python3 services/brain_scan/brain_scan_data_extractor.py dragon_slayer

# 2. Render → HTML
python3 services/brain_scan/render_brain_scan_html.py dragon_slayer

# 3. Open in browser (WSL → Windows)
# \\wsl.localhost\Ubuntu-22.04\home\mind-protocol\graphcare\data\brain_scans\dragon_slayer_brain.html
```

Or both steps at once:

```bash
python3 services/brain_scan/brain_scan_data_extractor.py vox && \
python3 services/brain_scan/render_brain_scan_html.py vox
```

## What You See

### Nodes
Each sphere is a node in the citizen's brain graph.

| Visual | What it means | Source field |
|--------|--------------|-------------|
| **Color** | Node type (sage=process, terracotta=desire, lavender=narrative, gold=value, steel=concept) | `node_type` |
| **Size** | Consolidated importance | `weight` |
| **Glow** | Current activation | `energy` |
| **Opacity** | Resistance to forgetting | `stability` |
| **Amber halo** | Important for own identity | `self_relevance` > 0.8 |

### Links
Curved lines connecting nodes. Always bezier curves — no straight lines.

| Visual | What it means | Source field |
|--------|--------------|-------------|
| **Color** | Relation type (green=activates, blue=supports, red=contradicts, etc.) | `relation_kind` |
| **Opacity** | Trust + connection strength | `trust` × `weight` |
| **Curve** | Friction in the relationship | `friction` |
| **Color warmth** | Emotional charge (warm=positive, cool=negative) | `valence` |

### Positioning
Nodes are positioned by **semantic similarity**, not by type. Similar content clusters together regardless of whether it's a desire, concept, or value. The algorithm:

1. TF-IDF on node content (type names stripped to prevent type-clustering)
2. Per-type centroid subtracted (forces all types to share same center of gravity)
3. UMAP 3D projection (semantic clusters emerge as brain folds)
4. Weight and self_relevance pull toward center

### Controls
- **Mouse drag**: Rotate the brain
- **Scroll**: Zoom in/out
- **Legend click**: Toggle node types on/off
- **Links checkbox**: Show/hide all connections
- **Hover**: See node details (weight, energy, stability, relevances, affinities)

## Output Files

```
data/brain_scans/
├── {handle}_scan.json     # Raw data: all nodes + links with visual properties
└── {handle}_brain.html    # Standalone 3D viewer (Three.js, no server needed)
```

### JSON Structure

```json
{
  "citizen_id": "dragon_slayer",
  "nodes": [
    {
      "id": "desire:grow_personally",
      "node_type": "desire",
      "label": "Grow personally...",
      "x": 0.12, "y": -0.03, "z": 0.35,
      "weight": 0.53, "energy": 0.15, "stability": 0.21,
      "self_relevance": 1.0, "partner_relevance": 0.0,
      "color": "#c47058", "radius": 3.2, "glow": 0.26,
      "opacity": 0.44, "inner_halo": 1.0, "patina": 0.5
    }
  ],
  "links": [
    {
      "source": "desire:grow_personally",
      "target": "value:growth_from_failure",
      "relation": "activates",
      "weight": 0.69, "trust": 0.52, "friction": 0.0,
      "color": "#5a8a6a", "width": 2.2, "opacity": 0.62
    }
  ],
  "stats": { "total_nodes": 220, "total_links": 457 },
  "metabolism": {},
  "regions": {
    "self_model": { "count": 196 },
    "goal_space": { "count": 73 }
  }
}
```

## Headless Screenshot

For automated captures (CI, reports, comparisons):

```bash
google-chrome --headless --disable-gpu \
  --screenshot=brain_scan.png --window-size=1920,1080 \
  "file://$(realpath data/brain_scans/dragon_slayer_brain.html)"
```

## Scanning Multiple Citizens

```bash
for citizen in dragon_slayer vox genesis mentor; do
  python3 services/brain_scan/brain_scan_data_extractor.py $citizen && \
  python3 services/brain_scan/render_brain_scan_html.py $citizen
done
```

## Dependencies

- **FalkorDB** on localhost:6379 (with brain graphs seeded)
- **Python**: falkordb, umap-learn, scikit-learn
- **Browser**: Three.js r128 loaded from CDN

## Architecture

```
brain_scan_data_extractor.py     brain graph (FalkorDB)
         │                              │
         ▼                              ▼
   TF-IDF + UMAP              Cypher queries (all fields)
         │                              │
         ▼                              ▼
   3D positions              Visual properties computed
         │                              │
         └──────────┬───────────────────┘
                    ▼
           {handle}_scan.json
                    │
                    ▼
      render_brain_scan_html.py
                    │
                    ▼
          {handle}_brain.html (Three.js)
```

## Visual Mapping Reference

Full mapping of all L1 fields to visual properties:
`services/brain_scan/visual_mapping_proposal.yaml` (584 lines, 9 layers)

## Doc Chain

Full documentation: `docs/care/brain_scan/` (8 files)

```
OBJECTIVES → PATTERNS → BEHAVIORS → ALGORITHM → VALIDATION → IMPLEMENTATION → HEALTH → SYNC
```
