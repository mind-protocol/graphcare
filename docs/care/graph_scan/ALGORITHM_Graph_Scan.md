# Graph Scan — Algorithm: Two-Stage Extract-Position-Render Pipeline

```
STATUS: DESIGNING
CREATED: 2026-03-18
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Graph_Scan.md
BEHAVIORS:       ./BEHAVIORS_Graph_Scan.md
PATTERNS:        ./PATTERNS_Graph_Scan.md
THIS:            ALGORITHM_Graph_Scan.md (you are here)
VALIDATION:      ./VALIDATION_Graph_Scan.md
HEALTH:          ./HEALTH_Graph_Scan.md
IMPLEMENTATION:  ./IMPLEMENTATION_Graph_Scan.md
SYNC:            ./SYNC_Graph_Scan.md

IMPL:            services/graph_scan/brain_data_extractor.py
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## OVERVIEW

Graph Scan is a two-stage pipeline: **extract+position** (Python) then **render** (HTML/JS). Two extractors exist — one for L1 citizen brains, one for L3 universe graphs — but they share the same pattern: query FalkorDB for all fields, compute TF-IDF on node labels, subtract per-type centroids, run UMAP to 3D, compute visual properties from physics fields, output JSON. The renderer consumes JSON from either extractor and produces a standalone interactive HTML using Three.js.

---

## OBJECTIVES AND BEHAVIORS

| Objective | Behaviors Supported | Why This Algorithm Matters |
|-----------|---------------------|----------------------------|
| O1: Make graph state visible | B1 | End-to-end pipeline from FalkorDB to interactive HTML |
| O2: Semantic topology | B2 | TF-IDF + centroid subtraction + UMAP prevents type clustering |
| O3: All dimensions visible | B4 | Visual property computation maps every physics field |
| O5: Works at both scales | B3 | Two extractors, one renderer, JSON intermediate format |

---

## DATA STRUCTURES

### ScanNode (L1 — brain_data_extractor.py)

```
ScanNode:
  id: str                    # Node ID from FalkorDB
  node_type: str             # Cognitive type (process/desire/narrative/value/concept/memory/state/stimulus/frequency)
  label: str                 # Truncated name (50 chars)
  x, y, z: float             # UMAP-computed 3D position, normalized to ~[-0.4, 0.4]
  # Raw physics (12 fields)
  weight, energy, stability, recency: float
  self_relevance, partner_relevance, goal_relevance: float
  novelty_affinity, care_affinity, achievement_affinity, risk_affinity: float
  activation_count: int
  # Computed visuals (14 properties)
  color: str (hex)           # From NODE_COLORS by type
  radius: float              # log1p(weight * 3.0)
  glow: float                # sigmoid(energy)
  opacity: float             # 0.3 + 0.7 * stability
  sharpness: float           # recency direct
  shape: str                 # Modality (sphere/octahedron/torus/box/icosahedron)
  inner_halo: float          # self_relevance
  outer_halo: float          # partner_relevance
  angularity: float          # goal_relevance
  scatter_count: int         # novelty_affinity * 8 (max 8)
  diffusion: float           # care_affinity
  wireframe: float           # achievement_affinity
  roughness: float           # risk_affinity
  ring_count: int            # log2(activation_count + 1) (max 5)
  # Provenance
  age_days: float            # (now - created_at_s) / 86400
  patina: float              # min(1.0, age_days / 60.0) — 60 days = full patina
  layer: str                 # stem (<0.25 z) / limbic (0.25-0.5) / cortex (>0.5)
```

### ScanNode (L3 — universe_data_extractor.py)

```
ScanNode:
  id: str                    # Node ID
  node_type: str             # Universal type (actor/moment/narrative/space/thing)
  label: str                 # Truncated name (60 chars)
  x, y, z: float             # UMAP 3D position
  weight, energy, stability, recency: float
  color: str (hex)           # From L3_COLORS by type
  radius: float              # log1p(weight * 3.0)
  glow: float                # sigmoid(energy)
  opacity: float             # 0.3 + 0.7 * stability
```

### ScanLink (L1)

```
ScanLink:
  source, target: str        # Node IDs
  relation: str              # relation_kind from FalkorDB
  # Raw physics (9 fields)
  weight, energy, trust, friction: float
  affinity, aversion, valence, stability, permanence: float
  # Computed visuals (10 properties)
  color: str (hex)           # From LINK_COLORS by relation
  width: float               # 0.5 + 1.5 * log1p(weight * 3.0)
  opacity: float             # 0.1 + 0.6 * trust + 0.3 * min(1, weight)
  glow: float                # min(1.0, energy * 2.0)
  wave: float                # 3.0 * friction (bezier control point amplitude)
  dash_gap: float            # 10.0 * (1 - permanence)
  saturation: float          # 0.2 + 0.8 * affinity
  has_aversion: bool         # aversion > 0.3
  temp_shift: float          # valence * 15.0 (hue degrees)
  thickness_var: float       # min(affinity, aversion) if both > 0.1, else 0
  jaggedness: float          # (1 - stability) * 2.0
```

### ScanLink (L3)

```
ScanLink:
  source, target: str
  weight, energy, trust, friction: float
  hierarchy, permanence, valence: float
  affinity, aversion: float
  color: str (hex)           # From _link_color_from_hierarchy(hierarchy, valence)
  opacity: float             # 0.1 + 0.6 * trust + 0.3 * min(1, weight)
  glow: float                # min(1.0, energy * 2.0)
```

### BrainScan / UniverseScan (top-level containers)

```
BrainScan:
  citizen_id: str
  nodes: list[ScanNode]
  links: list[ScanLink]
  stats: dict                # total_nodes, total_links, type_counts, layers, regions
  metabolism: dict            # From __metabolism__ meta node if present
  regions: dict              # self_model, partner_model, goal_space (detected from relevance > 0.5)

UniverseScan:
  graph_name: str
  nodes: list[ScanNode]
  links: list[ScanLink]
  stats: dict                # total_nodes, total_links, type_counts
```

---

## ALGORITHM: Extraction + Positioning (shared by L1 and L3)

### Step 1: Query All Fields

Query FalkorDB for all node fields and all link fields using MATCH...RETURN. No content or synthesis fields are queried. For L1, this includes 12 numeric node fields + created_at_s. For L3, a smaller set (weight, energy, stability, recency) plus node_type and name.

```
MATCH (n) RETURN n.id, n.type, n.name, n.weight, n.energy, ...
MATCH (a)-[r]->(b) RETURN a.id, b.id, r.weight, r.energy, r.trust, ...
```

### Step 2: Build Text for TF-IDF

For each node, construct a text string from its ID and label (NOT its type). The type name is explicitly stripped from the text to prevent UMAP from clustering by type.

```
text = id.replace(":", " ") + " " + label
text = text.replace(type_name, "")  # Remove type signal
```

### Step 3: TF-IDF Vectorization

Use scikit-learn TfidfVectorizer (max_features=200 for L1, 300 for L3) to convert text to vectors. This produces a sparse matrix of shape (n_nodes, n_features).

### Step 4: Per-Type Centroid Subtraction

For each node type, compute the centroid (mean vector) of all nodes of that type. Subtract it from each node's vector. This removes the type-specific signal, forcing the embedding space to reflect content similarity rather than type membership.

```
for type in types:
    indices = nodes_of_type[type]
    centroid = mean(X[indices])
    for i in indices:
        X[i] -= centroid
```

### Step 5: UMAP to 3D

Run UMAP with n_components=3, cosine metric, n_neighbors=min(20, n-1), min_dist=0.05, spread=0.8, random_state=42. Normalize output to [-0.4, 0.4] range.

### Step 6: Weight-Based Center Pull

Higher-weight nodes are pulled toward the center (spatial importance). For L1, self_relevance also contributes to center pull.

```
center_pull = 1.0 - weight * 0.25 - self_relevance * 0.1  # L1
center_pull = 1.0 - weight * 0.2                           # L3
x *= center_pull; y *= center_pull; z = z * center_pull + 0.4
```

### Step 7: Compute Visual Properties

Map each physics field to a visual property using the formulas in the data structures section above. Colors from type lookup tables, radius from log1p, glow from sigmoid, etc.

---

## ALGORITHM: Rendering (render_html.py)

### Step 1: Load JSON

Parse the scan JSON file. Extract nodes and links arrays, citizen_id/graph_name, stats.

### Step 2: Generate Three.js Scene

Embed nodes_json and links_json directly into the HTML template. Create:
- Scene with dark background (#06060c) and exponential fog
- PerspectiveCamera at (0.3, 0.5, 0.8) looking at (0, 0.3, 0)
- OrbitControls with damping
- Ambient + 3 point lights (key warm, rim cool, fill warm)

### Step 3: Render Nodes

For each node: SphereGeometry(radius * 0.003), MeshStandardMaterial with roughness=0.95, patina-lerped color, emissive glow. Inner halos for self_relevance > 0.8.

### Step 4: Render Links (All Curved)

For each link: compute midpoint, perpendicular vector, control point offset from friction + hash. QuadraticBezierCurve3 with 8 segments. LineBasicMaterial with trust-based opacity. Optional glow duplicate for energy > 0.1.

### Step 5: UI Overlays

Legend with type color dots (clickable to filter). Hover panel showing all physics fields. Checkbox controls for link and halo visibility.

---

## KEY DECISIONS

### D1: UMAP Over Force-Directed Layout

```
WHY UMAP:
    Deterministic (random_state=42) — same input, same output
    Pre-computed — no iterative settling, no "wait for convergence"
    Preserves local structure while allowing global mixing
    Handles 1000+ nodes without performance issues

WHY NOT force-directed:
    Non-deterministic — different runs produce different layouts
    Requires convergence time — not pre-computable
    Tends to produce uniform density — hides clusters
    Poor at preventing type stratification without explicit constraints
```

### D2: Centroid Subtraction Per Type

```
WHY:
    Without it, TF-IDF vectors of same-type nodes share common terms
    UMAP would cluster them together (all "concepts" in one region)
    Subtracting the type centroid removes this shared signal
    Result: positions driven by unique content, not type membership

RISK:
    If a type has very few nodes (1-2), centroid subtraction has minimal effect
    If all nodes of a type have identical labels, subtraction zeros them out
```

### D3: CDN Three.js (Standalone HTML)

```
WHY CDN:
    HTML files are self-contained — open in any browser without a build step
    No node_modules, no webpack, no npm install required
    Can be shared as a single file (email, Slack, etc.)
    Three.js r128 is stable and widely cached

COST:
    Requires internet to load (no offline support)
    Pinned to r128 — no automatic updates
```

---

## DATA FLOW

```
FalkorDB (brain_{handle} or {universe})
    |
    v
Extractor (brain_data_extractor.py or universe_data_extractor.py)
    | MATCH queries (read-only)
    v
Raw node/link data (Python dicts)
    |
    v
TF-IDF Vectorizer (scikit-learn)
    |
    v
TF-IDF matrix (n_nodes x n_features)
    |
    v
Centroid subtraction (per type)
    |
    v
UMAP 3D projection
    |
    v
Normalized positions + visual property computation
    |
    v
JSON file (data/graph_scans/{name}_scan.json)
    |
    v
Renderer (render_html.py)
    |
    v
Standalone HTML (data/graph_scans/{name}_brain.html or {name}_universe.html)
```

---

## COMPLEXITY

**Time:** O(n * f + n * log(n)) — TF-IDF is O(n * f) where f = max_features, UMAP is approximately O(n * log(n)) with the default NN-descent algorithm.

**Space:** O(n * f) — the TF-IDF matrix dominates. For 1000 nodes with 300 features, this is ~1.2MB.

**Bottlenecks:**
- UMAP fitting is the slowest step (~2-5 seconds for 220 nodes, ~10-20 seconds for 1000+ nodes)
- FalkorDB queries are fast (<100ms for 220 nodes)
- HTML rendering is instant (string formatting)

---

## HELPER FUNCTIONS

### `_node_radius(weight)`

**Purpose:** Convert weight to visual radius using log scale.

**Logic:** `0.4 + 1.0 * log1p(weight * 3.0)` — logarithmic so heavy nodes don't dominate visually.

### `_node_glow(energy)`

**Purpose:** Convert energy to emissive glow intensity.

**Logic:** Sigmoid centered at 0.5 with steepness 3.0. Below 0.1 = no glow. Produces smooth activation effect.

### `_node_opacity(stability)`

**Purpose:** Convert stability to opacity.

**Logic:** `0.3 + 0.7 * stability` — fragile nodes are translucent, stable nodes are solid. Minimum 0.3 so nothing disappears entirely.

### `_link_color_from_hierarchy(hierarchy, valence)` (L3 only)

**Purpose:** Determine link color when relation_kind is null.

**Logic:** hierarchy < -0.5 = sage (containment), > 0.5 = lavender (elaboration), valence > 0.3 = steel (constructive), valence < -0.3 = terracotta (destructive), else neutral gray.

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| FalkorDB | `graph.query("MATCH (n) RETURN ...")` | Node rows with all physics fields |
| FalkorDB | `graph.query("MATCH (a)-[r]->(b) RETURN ...")` | Link rows with all physics fields |
| scikit-learn | `TfidfVectorizer.fit_transform()` | Sparse TF-IDF matrix |
| umap-learn | `UMAP.fit_transform()` | 3D coordinate array |

---

## MARKERS

<!-- @mind:TODO Profile UMAP performance on a 1000+ node L3 graph — may need to tune n_neighbors or use approximate NN -->
<!-- @mind:proposition Use pre-computed embeddings from the mind-mcp synthesis field (768D all-mpnet) instead of TF-IDF on labels. Would give much better semantic positioning without reading content at render time. -->
