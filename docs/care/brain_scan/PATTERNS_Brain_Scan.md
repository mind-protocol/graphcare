# Brain Scan — Patterns: Two-Stage Pipeline with Brain Anatomy Metaphor

```
STATUS: DESIGNING
CREATED: 2026-03-18
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Brain_Scan.md
BEHAVIORS:      ./BEHAVIORS_Brain_Scan.md
THIS:            PATTERNS_Brain_Scan.md (you are here)
ALGORITHM:       ./ALGORITHM_Brain_Scan.md
VALIDATION:      ./VALIDATION_Brain_Scan.md
HEALTH:          ./HEALTH_Brain_Scan.md
IMPLEMENTATION:  ./IMPLEMENTATION_Brain_Scan.md
SYNC:            ./SYNC_Brain_Scan.md

IMPL:            services/brain_scan/brain_scan_data_extractor.py
```

### Bidirectional Contract

**Before modifying this doc or the code:**
1. Read ALL docs in this chain first
2. Read the linked IMPL source file

**After modifying this doc:**
1. Update the IMPL source file to match, OR
2. Add a TODO in SYNC_Brain_Scan.md: "Docs updated, implementation needs: {what}"
3. Run tests: `python -m pytest tests/care/brain_scan/ -v`

**After modifying the code:**
1. Update this doc chain to match, OR
2. Add a TODO in SYNC_Brain_Scan.md: "Implementation changed, docs need: {what}"
3. Run tests: `python -m pytest tests/care/brain_scan/ -v`

---

## THE PROBLEM

A citizen's brain graph contains 220+ nodes and 457+ links. As raw data — whether JSON, Cypher results, or tabular output — this is incomprehensible. You cannot read 220 nodes and understand what they mean. You cannot look at a health score of 23/100 and know why it's low.

Without visualization, brain topology is opaque. GraphCare health assessments produce scores, but scores without spatial context are abstract. "Low connectivity in cortex" means nothing until you can see a cortex with sparse links hanging in space while the stem below is dense and tangled. The structural story is invisible in numbers.

The problem is not rendering — it's legibility. The challenge is turning a flat graph into a spatial metaphor that humans and agents can navigate, where position encodes meaning and visual properties encode data.

---

## THE PATTERN

**Two-stage pipeline: Extract+Position, then Render.**

Stage 1 (`brain_scan_data_extractor.py`): Connect to FalkorDB, query all nodes and links (topology only — never content), group nodes by semantic type, position each group in its anatomy layer using a golden angle spiral, map visual properties from data, and output a `BrainScan` dataclass as JSON.

Stage 2 (`render_brain_scan_html.py`): Load the JSON, generate a standalone HTML file with embedded Three.js that renders the pre-computed positions as an interactive 3D brain. No further database access. No live computation. Just load and render.

**The key insight:** Semantic type determines spatial position. A `process` node is always in the stem. A `concept` node is always in the cortex. This is not arbitrary — it mirrors how brain anatomy works, where lower structures handle primitive processing and higher structures handle abstraction. The metaphor is the interface.

---

## BEHAVIORS SUPPORTED

- **B1** (Brain Topology Becomes Visible) — the pipeline transforms raw graph data into positioned 3D nodes
- **B2** (Anatomy Layers Separate) — the golden angle spiral within z-bands creates distinct visual layers
- **B3** (Interactive Exploration) — standalone HTML with OrbitControls enables rotation, zoom, layer toggles
- **B4** (Node Hover Reveals Identity) — raycasting on pre-computed meshes shows type, label, weight, energy

## BEHAVIORS PREVENTED

- **A1** (Content leakage) — the Cypher query never selects `content` or `synthesis` fields. Only topology.
- **A2** (Graph modification) — the pipeline is read-only. No writes to FalkorDB, ever.

---

## PRINCIPLES

### Principle 1: Anatomy Layers

Nodes are positioned in z-bands that correspond to brain anatomy: stem (z=0.0-0.2) for processes, limbic (z=0.2-0.5) for desires and narratives, cortex (z=0.5-1.0) for values and concepts. The z-axis is the vertical axis in the rendered scene, creating a visual bottom-to-top progression from primitive to abstract.

This matters because position should encode meaning. A viewer can immediately see where mass concentrates — a bottom-heavy brain is process-dominated, a top-heavy brain is concept-rich. Imbalances become visible patterns rather than statistical summaries.

### Principle 2: Golden Angle Spiral

Within each layer's z-band, nodes are distributed using the golden angle (~137.5 degrees). Each successive node rotates by this angle, and its radius grows with `sqrt(index/total)`, creating a sunflower-like spread. Weight modulates radius: heavier nodes are more central, lighter nodes drift outward. Small Gaussian jitter adds organic texture.

This matters because the golden angle avoids grid patterns and clustering artifacts. It produces natural, non-repeating distributions that look organic — brain-like rather than spreadsheet-like. The math is simple but the visual result is rich.

### Principle 3: Visual Properties from Data

Every visual property maps to a data property with no ambiguity:
- **Color** from `type` (desire=red, concept=blue, value=gold, process=green, narrative=purple)
- **Size** from `weight` (0-1 maps to 3-15px radius)
- **Glow** from `energy` (threshold >0.3 for nodes, >0.5 for links)
- **Link opacity** from `weight` (0-1 maps to 0.1-1.0)
- **Link color** from `relation_kind` (supports=blue, contradicts=red, activates=green, etc.)
- **Link width** from `trust` (0-1 maps to 0.5-3px)

This matters because visual properties that encode data allow pattern recognition without reading text. A cluster of large, glowing red nodes in the limbic layer tells a story: strong, energized desires. You don't need to hover to get the gist.

### Principle 4: Pre-Compute Everything, Interact After

All positioning, coloring, sizing, and property mapping happens in Stage 1. Stage 2 merely renders the pre-computed JSON. The HTML file has zero database dependencies at runtime — it loads from CDN Three.js and embedded JSON data.

This matters because it decouples exploration from extraction. A scan can be generated once and shared as a file. Multiple people can explore the same brain state. FalkorDB is not loaded during interaction. The scan becomes an artifact, not a live view.

---

## DATA

| Source | Type | Purpose / Description |
|--------|------|-----------------------|
| `brain_{handle}` (FalkorDB graph) | DB | The citizen's brain graph — source of all topology data |
| `data/brain_scans/{handle}_scan.json` | FILE | Extracted scan with 3D positions — Stage 1 output |
| `data/brain_scans/{handle}_brain.html` | FILE | Standalone interactive HTML — Stage 2 output |
| `https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js` | URL | Three.js core library for 3D rendering |
| `https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js` | URL | Camera orbit controls for mouse interaction |

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| `falkordb` (Python client) | Querying brain graphs in Stage 1 |
| `Three.js r128` (CDN) | 3D rendering in the standalone HTML |
| Mind Protocol brain graph schema | Defines node_type, weight, energy, relation_kind fields we query |

---

## INSPIRATIONS

- **fMRI brain mapping** — the anatomy-layer metaphor comes from functional neuroimaging, where brain regions have spatial locations tied to function
- **Semantic embedding spaces** — the idea that position encodes meaning, where nearby things are related
- **Three.js particle systems** — lightweight rendering of thousands of points with per-point properties (color, size, glow)
- **Phyllotaxis / golden angle spirals** — from botany (sunflower seed patterns), adapted for non-grid organic distribution

---

## SCOPE

### In Scope

- Extracting brain topology from FalkorDB (nodes: id, type, weight, energy; links: source, target, relation_kind, weight, energy, trust)
- Computing 3D positions for every node based on type and anatomy layers
- Mapping visual properties (color, size, glow, opacity, width) from data properties
- Generating standalone HTML with interactive 3D visualization
- Layer toggles, type filters, hover info

### Out of Scope

- Health score computation — see: `services/health_assessment/`
- Content or synthesis access — topology only, by design
- Live streaming of brain changes — the scan is a snapshot
- Semantic embedding-based positioning (UMAP, t-SNE) — proposed for v2
- Force-directed graph layout — we use anatomy layers, not spring physics
- Video export or animation recording — proposed for v2

---

## MARKERS

<!-- @mind:todo Investigate collaboration with @dev's physics_cartographer.py from mind-ops for enriched positioning data -->
<!-- @mind:proposition Consider UMAP-based positioning using node embeddings for a semantic layout mode alongside the anatomy mode -->
