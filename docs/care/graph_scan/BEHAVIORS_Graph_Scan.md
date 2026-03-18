# Graph Scan — Behaviors: Observable Effects of Graph Visualization

```
STATUS: DESIGNING
CREATED: 2026-03-18
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Graph_Scan.md
THIS:            BEHAVIORS_Graph_Scan.md (you are here)
PATTERNS:        ./PATTERNS_Graph_Scan.md
ALGORITHM:       ./ALGORITHM_Graph_Scan.md
VALIDATION:      ./VALIDATION_Graph_Scan.md
HEALTH:          ./HEALTH_Graph_Scan.md
IMPLEMENTATION:  ./IMPLEMENTATION_Graph_Scan.md
SYNC:            ./SYNC_Graph_Scan.md

IMPL:            services/graph_scan/brain_data_extractor.py
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## BEHAVIORS

### B1: Any Graph Becomes a 3D Visualization

**Why:** This is the core purpose of the module. Without it, graph state is invisible — just numbers in a database. GraphCare needs to see topology to diagnose health.

```
GIVEN:  A graph exists in FalkorDB (either brain_{handle} for L1 or {universe} for L3)
WHEN:   The appropriate extractor runs (brain_data_extractor.py or universe_data_extractor.py)
THEN:   A JSON file is produced containing positioned nodes with visual properties
AND:    Running render_html.py on that JSON produces an interactive HTML file
```

### B2: Types Mix Spatially

**Why:** Type-stratified layouts hide the most interesting structure — cross-type connections. A brain where "desires" and "values" and "concepts" overlap reveals how those cognitive domains actually relate. Separate clusters would be a lie.

```
GIVEN:  Nodes of different types (e.g., desire, concept, value for L1 or actor, space, thing for L3)
WHEN:   Positioned by UMAP with per-type centroid subtraction
THEN:   Types are NOT stratified into separate spatial regions
AND:    Semantically similar nodes cluster regardless of type
```

### B3: L1 and L3 Use Same Renderer

**Why:** Maintaining two renderers would be wasteful and lead to visual inconsistency. The JSON intermediate format decouples extraction from rendering. The renderer doesn't need to know the graph's origin.

```
GIVEN:  JSON output from either brain_data_extractor or universe_data_extractor
WHEN:   render_html.py processes the JSON
THEN:   A valid interactive HTML file is produced with Three.js 3D scene
AND:    The HTML works identically regardless of which extractor produced the JSON
```

### B4: Hover Reveals Physics

**Why:** The visualization needs to support both overview (seeing the shape) and detail (inspecting individual nodes). All numeric fields should be accessible on hover so nothing is hidden.

```
GIVEN:  A rendered HTML file open in a browser
WHEN:   User hovers over a node
THEN:   A panel displays all numeric physics fields for that node
AND:    Fields include weight, energy, stability, recency, self_relevance (L1), goal_relevance (L1), etc.
```

### B5: Headless Screenshot Works

**Why:** Automated reporting needs image export. A scan generated in a CI pipeline or by an agent should produce a PNG without human interaction.

```
GIVEN:  A rendered HTML file
WHEN:   google-chrome --headless --screenshot runs on it
THEN:   A PNG file is exported at the specified resolution
AND:    The PNG shows the 3D scene from the default camera angle
```

---

## OBJECTIVES SERVED

| Behavior ID | Objective | Why It Matters |
|-------------|-----------|----------------|
| B1 | O1: Make graph state visible | Core conversion from data to visualization |
| B2 | O2: Semantic topology | Centroid subtraction prevents type clustering |
| B3 | O5: Works at both scales | Same renderer for L1 and L3 |
| B4 | O3: All dimensions visible | Hover exposes every physics field |
| B5 | O4: Pre-computed, static | Offline generation, headless export |

---

## INPUTS / OUTPUTS

### Primary Function: `extract_graph_scan()` (L1)

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| citizen_handle | str | The citizen's handle (e.g., "dragon_slayer") — used to select `brain_{handle}` graph |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| scan | BrainScan | Dataclass with nodes (ScanNode[]), links (ScanLink[]), stats, metabolism, regions |

**Side Effects:**

- Reads from FalkorDB (read-only)
- No graph mutations, no writes to FalkorDB

### Primary Function: `extract_universe_scan()` (L3)

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| graph_name | str | The graph name (e.g., "lumina_prime") — used to select the L3 graph |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| scan | UniverseScan | Dataclass with nodes (ScanNode[]), links (ScanLink[]), stats |

**Side Effects:**

- Reads from FalkorDB (read-only)

### Primary Function: `render_html()`

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| scan_path | Path | Path to the JSON scan file |
| output_path | Path | Path for the output HTML file |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| (none) | void | Writes HTML file to output_path |

**Side Effects:**

- Creates directories if needed (mkdir parents=True)
- Writes HTML file to filesystem

---

## EDGE CASES

### E1: Graph With Fewer Than 5 Nodes

```
GIVEN:  A graph with fewer than 5 nodes (too few for UMAP)
THEN:   Nodes are positioned using golden angle sphere distribution
AND:    The visualization still renders correctly
```

### E2: UMAP Fails

```
GIVEN:  UMAP or scikit-learn raises an exception during positioning
THEN:   Fallback to golden angle sphere distribution
AND:    A warning is logged
AND:    The visualization still renders (just without semantic positioning)
```

### E3: Empty Graph

```
GIVEN:  A graph with 0 nodes
THEN:   An empty scan is produced (nodes=[], links=[], stats show 0)
AND:    The HTML renders with an empty scene
```

### E4: L3 Graph With Null relation_kind

```
GIVEN:  All links in an L3 graph have relation_kind = NULL
THEN:   Link color is derived from hierarchy and valence dimensions instead
AND:    No error is raised about missing relation labels
```

---

## ANTI-BEHAVIORS

### A1: Never Read Content or Synthesis

```
GIVEN:   Any graph query
WHEN:    Extracting node data
MUST NOT: Read or store the content or synthesis fields from nodes
INSTEAD:  Use only structural/physics fields (weight, energy, stability, etc.) and label/name
```

### A2: Never Modify the Graph

```
GIVEN:   Any extractor execution
WHEN:    Querying FalkorDB
MUST NOT: Execute CREATE, SET, DELETE, or MERGE queries
INSTEAD:  Only MATCH...RETURN queries (read-only)
```

### A3: Never Animate

```
GIVEN:   The rendered HTML
WHEN:    Displaying the visualization
MUST NOT: Include animated transitions, pulsing, blinking, or temporal effects
INSTEAD:  Static geometry with orbit controls only (user-driven camera movement)
```

---

## MARKERS

<!-- @mind:TODO The renderer currently hardcodes citizen_id from scan JSON — needs to also handle graph_name for L3 scans -->
<!-- @mind:proposition Add link hover info showing all 13 link physics fields, not just node hover -->
