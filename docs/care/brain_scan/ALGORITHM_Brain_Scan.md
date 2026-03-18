# Brain Scan — Algorithm: Two-Stage Extract-Position-Render Pipeline

```
STATUS: DESIGNING
CREATED: 2026-03-18
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Brain_Scan.md
BEHAVIORS:       ./BEHAVIORS_Brain_Scan.md
PATTERNS:        ./PATTERNS_Brain_Scan.md
THIS:            ALGORITHM_Brain_Scan.md (you are here)
VALIDATION:      ./VALIDATION_Brain_Scan.md
HEALTH:          ./HEALTH_Brain_Scan.md
IMPLEMENTATION:  ./IMPLEMENTATION_Brain_Scan.md
SYNC:            ./SYNC_Brain_Scan.md

IMPL:            services/brain_scan/brain_scan_data_extractor.py
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## OVERVIEW

The brain scan pipeline transforms a citizen's brain graph (stored in FalkorDB) into an interactive 3D visualization in two stages. Stage 1 queries the graph, groups nodes by semantic type, positions them in anatomy-based z-layers using a golden angle spiral, maps visual properties from data, and outputs a JSON file. Stage 2 loads that JSON and generates a standalone HTML file with Three.js that renders the pre-computed scene with interactive controls. The entire pipeline is read-only — no brain data is modified, and no content fields are accessed.

---

## OBJECTIVES AND BEHAVIORS

| Objective | Behaviors Supported | Why This Algorithm Matters |
|-----------|---------------------|----------------------------|
| O1 (Make brain state visible) | B1, B3 | Converts flat graph data into positioned 3D structure |
| O2 (Anatomy-based layering) | B2 | Golden angle spiral in z-bands creates spatial separation by type |
| O3 (Actionable insight) | B3, B4 | Visual properties encode data; interaction reveals identity |
| O4 (Pre-computed, not live) | B1, B3 | Two-stage separation means zero DB load during exploration |

---

## DATA STRUCTURES

### ScanNode

```
ScanNode:
  id:        str       — unique node identifier from FalkorDB
  node_type: str       — semantic type (process, desire, narrative, value, concept)
  label:     str       — display name, truncated to 50 chars
  x:         float     — horizontal position, rounded to 4 decimals
  y:         float     — depth position, rounded to 4 decimals
  z:         float     — vertical position (anatomy layer), rounded to 4 decimals
  weight:    float     — node importance (0.0 to 1.0)
  energy:    float     — node activation (0.0+)
  color:     str       — hex color mapped from node_type
  size:      float     — display radius: 3 + weight * 12
  glow:      bool      — True if energy > 0.3
  layer:     str       — anatomy layer name: "stem", "limbic", or "cortex"
```

### ScanLink

```
ScanLink:
  source:    str       — source node id
  target:    str       — target node id
  relation:  str       — relation_kind (supports, contradicts, activates, etc.)
  weight:    float     — link importance (0.0 to 1.0)
  energy:    float     — link activation (0.0+)
  trust:     float     — trust level (0.0 to 1.0)
  color:     str       — hex color mapped from relation kind
  width:     float     — display width: 0.5 + trust * 2.5
  opacity:   float     — display opacity: 0.1 + weight * 0.9
  glow:      bool      — True if energy > 0.5
```

### BrainScan

```
BrainScan:
  citizen_id: str      — the citizen handle
  nodes:      list[ScanNode]  — all positioned nodes
  links:      list[ScanLink]  — all visual links
  stats:      dict     — {total_nodes, total_links, type_counts, layers}
```

---

## ALGORITHM: extract_brain_scan(citizen_handle)

### Step 1: Connect and Query Nodes

Connect to FalkorDB at localhost:6379. Select graph `brain_{citizen_handle}`. Execute:

```cypher
MATCH (n) RETURN n.id, n.type, n.node_type, n.name, n.weight, n.energy
```

This returns all nodes with their topology metadata. Note: `n.type` and `n.node_type` are both checked because FalkorDB stores the type in different fields depending on backend config. Content and synthesis are never queried.

### Step 2: Group Nodes by Type

Iterate over result rows. For each node, determine its type from `n.type` (primary) or `n.node_type` (fallback). Group nodes into `type_groups: dict[str, list]` keyed by type name. Build a `node_map: dict[str, str]` mapping node ID to type for later link processing.

Defaults for missing fields: weight=0.5, energy=0.0. Nodes with empty ID are skipped. Labels are truncated to 50 characters.

### Step 3: Position Each Group in Its Anatomy Layer

For each type group, look up its z-band from `LAYER_Z`:
- process: (0.0, 0.2) — stem
- desire: (0.25, 0.45) — limbic
- narrative: (0.3, 0.7) — distributed
- value: (0.55, 0.8) — cortex
- concept: (0.7, 1.0) — cortex
- unknown types: (0.4, 0.6) — middle default

Within the z-band, distribute nodes using the golden angle spiral:

```python
golden_angle = pi * (3 - sqrt(5))    # ~2.399 radians, ~137.5 degrees
theta = i * golden_angle              # angle for node i
r = 0.3 + 0.4 * sqrt(i / max(n, 1))  # radius grows with sqrt for even spread
r *= (1.2 - weight * 0.4)            # heavier nodes are more central
x = r * cos(theta)
y = r * sin(theta)
z = z_lo + (z_hi - z_lo) * (i / max(n-1, 1))  # linear interpolation within z-band
# Add Gaussian jitter: x += gauss(0, 0.02), y += gauss(0, 0.02), z += gauss(0, 0.01)
```

Map visual properties:
- color: from NODE_COLORS dict by type
- size: 3 + weight * 12
- glow: energy > 0.3
- layer: stem if z_lo < 0.25, limbic if z_lo < 0.5, else cortex

### Step 4: Query All Links

Execute:

```cypher
MATCH (a)-[r]->(b) RETURN a.id, b.id, r.relation_kind, r.weight, r.energy, r.trust
```

This returns all edges with their topology metadata. Again, no content fields are accessed.

### Step 5: Map Link Visual Properties

For each link row:
- color: from LINK_COLORS dict by relation_kind (default: gray #9ca3af)
- width: 0.5 + trust * 2.5
- opacity: 0.1 + weight * 0.9
- glow: energy > 0.5

Links with empty source or target are skipped.

### Step 6: Compute Stats and Return

Aggregate:
- total_nodes, total_links
- type_counts: per-type node counts
- layers: {stem: count, limbic: count, cortex: count}

Return the BrainScan dataclass. Optionally serialize to JSON via `save_scan()`.

---

## ALGORITHM: render_html(scan_path, output_path)

### Step 1: Load JSON and Extract Data

Read the scan JSON file. Extract nodes, links, stats, and citizen_id. Serialize nodes and links back to JSON strings for embedding in the HTML template.

### Step 2: Generate Three.js Scene

Build an HTML string with:
- Scene: dark background (0x0a0a0a), exponential fog, perspective camera at (0, 0.5, 2.0)
- Lights: ambient (dim) + point light from above
- OrbitControls: damping=0.05, auto-rotate at 0.5 speed

### Step 3: Create Node Meshes

For each node in the embedded JSON:
- Create a SphereGeometry with radius = `n.size * 0.003`
- Apply MeshPhongMaterial with color from data, emissive glow if `n.glow`
- Position at `(n.x, n.z, n.y)` — note z/y swap so anatomy layers go vertical

### Step 4: Create Link Lines

For each link:
- Look up source and target meshes by node ID
- Create BufferGeometry from the two positions
- Apply LineBasicMaterial with color, opacity (halved for subtlety)

### Step 5: Add Controls and Interaction

- Layer checkboxes: toggle visibility of nodes matching `data-layer`
- Show links checkbox: toggle linkGroup visibility
- Type legend: clickable items that toggle node visibility by type
- Raycaster on mousemove: detect hovered node, display tooltip with type, label, weight, energy, layer
- Window resize handler

### Step 6: Write HTML

Write the complete HTML string to `output_path`. Print the file path and file:// URL.

---

## KEY DECISIONS

### D1: Golden Angle Spiral vs Random Positioning

```
CHOSEN: Golden angle spiral
WHY:    Random positioning creates irregular clusters and empty gaps.
        The golden angle guarantees even angular distribution without repetition.
        Combined with sqrt-based radius growth, it produces sunflower-like patterns
        that are organic, space-filling, and visually appealing.
        The math is simple (one multiply, one cos, one sin per node) and deterministic
        up to the jitter term.
REJECTED: Random — uneven distribution. Grid — too mechanical. Force-directed — too expensive for pre-compute.
```

### D2: Z-Axis for Anatomy Layers

```
CHOSEN: Vertical z-axis maps to brain anatomy (stem at bottom, cortex at top)
WHY:    Humans intuitively associate "higher" with "more abstract".
        The brain anatomy metaphor (brainstem → limbic → cortex) maps naturally
        to bottom → middle → top in 3D space.
        In Three.js, the y-axis is up, so we swap z→y during rendering:
        mesh.position.set(n.x, n.z, n.y)
```

### D3: CDN Three.js vs Bundled

```
CHOSEN: CDN (https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js)
WHY:    The HTML file must be standalone — openable by anyone with a browser
        and internet connection. No build step, no npm install, no bundler.
        CDN is cached by browsers and globally fast. The tradeoff is requiring
        internet access to open the file, but this is acceptable for a
        visualization tool that's already generated offline.
REJECTED: Bundled inline — would bloat HTML by ~600KB. Local file reference — not portable.
```

---

## DATA FLOW

```
FalkorDB (brain_{handle})
    ↓ Cypher: MATCH (n) RETURN n.id, n.type, ...
type_groups: dict[str, list[tuple]]
    ↓ Golden angle spiral positioning per group
list[ScanNode] with (x, y, z, color, size, glow)
    ↓ Cypher: MATCH (a)-[r]->(b) RETURN a.id, b.id, ...
list[ScanLink] with (color, width, opacity, glow)
    ↓ save_scan()
{handle}_scan.json
    ↓ render_html()
{handle}_brain.html (standalone, interactive)
```

---

## COMPLEXITY

**Time:** O(N + E) where N = nodes, E = edges — one pass for positioning, one pass for links. FalkorDB queries are the bottleneck, not the computation.

**Space:** O(N + E) — one ScanNode per node, one ScanLink per edge, all held in memory simultaneously.

**Bottlenecks:**
- FalkorDB query latency — especially if the database is remote or restarting
- HTML file size for very large brains — 1000+ nodes would produce a large embedded JSON blob
- Three.js rendering performance with >1000 sphere meshes — may need LOD or instanced rendering

---

## HELPER FUNCTIONS

### `_layer_name(ntype)`

**Purpose:** Map a node type to its anatomy layer name (stem, limbic, or cortex)

**Logic:** Look up the z_lo from LAYER_Z. If z_lo < 0.25 → "stem". If z_lo < 0.5 → "limbic". Otherwise → "cortex".

### `save_scan(scan, output_path)`

**Purpose:** Serialize a BrainScan dataclass to JSON and write to disk

**Logic:** Convert all ScanNode and ScanLink objects via `dataclasses.asdict()`. Create parent directories. Write indented JSON.

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| FalkorDB (brain_{handle}) | Two Cypher queries (nodes, links) | Result sets with topology metadata |
| Three.js r128 (CDN) | Script tag in generated HTML | 3D rendering engine in browser |
| OrbitControls.js (CDN) | Script tag in generated HTML | Mouse-based camera orbit controls |

---

## MARKERS

<!-- @mind:todo Investigate instanced mesh rendering for brains with >500 nodes to improve render performance -->
<!-- @mind:proposition Add a third stage: semantic positioning via UMAP on node embeddings, as an alternative to anatomy-only layout -->
<!-- @mind:escalation Decide whether golden angle spiral should be seeded (reproducible) or random (organic) — currently uses random jitter -->
