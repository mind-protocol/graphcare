# Brain Scan — Behaviors: Observable Effects of Topology Visualization

```
STATUS: DESIGNING
CREATED: 2026-03-18
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Brain_Scan.md
THIS:            BEHAVIORS_Brain_Scan.md (you are here)
PATTERNS:        ./PATTERNS_Brain_Scan.md
ALGORITHM:       ./ALGORITHM_Brain_Scan.md
VALIDATION:      ./VALIDATION_Brain_Scan.md
HEALTH:          ./HEALTH_Brain_Scan.md
IMPLEMENTATION:  ./IMPLEMENTATION_Brain_Scan.md
SYNC:            ./SYNC_Brain_Scan.md

IMPL:            services/brain_scan/brain_scan_data_extractor.py
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## BEHAVIORS

### B1: Brain Topology Becomes Visible

**Why:** A brain graph in FalkorDB is raw data — node IDs, types, edge tuples. Hundreds of them. No human or agent can understand the structure by reading rows. This behavior transforms that raw graph into a JSON file with 3D coordinates for every node, making the topology renderable as a spatial object. Without this, health scores are opaque numbers with no visual explanation. (Serves O1, O3)

```
GIVEN:  A citizen's brain graph exists in FalkorDB with > 0 nodes
WHEN:   extract_brain_scan(citizen_handle) is called
THEN:   A BrainScan object is returned containing every node with valid (x, y, z) coordinates
AND:    Every link is captured with source, target, relation, and visual properties
AND:    Stats are computed (total_nodes, total_links, type_counts, layer_counts)
```

### B2: Anatomy Layers Separate

**Why:** Flat positioning would pile all 220 nodes into an undifferentiated cloud. The anatomy-layer pattern assigns z-bands by semantic type, creating visible vertical separation between processes (bottom), desires/narratives (middle), and values/concepts (top). This makes it possible to see brain composition at a glance — where the mass concentrates, which layers are dense, which are sparse. (Serves O2)

```
GIVEN:  Nodes with types (process, desire, narrative, value, concept)
WHEN:   Nodes are positioned during extract_brain_scan()
THEN:   Process nodes are placed in z=0.0-0.2 (stem)
AND:    Desire nodes are placed in z=0.25-0.45 (limbic)
AND:    Narrative nodes are placed in z=0.3-0.7 (distributed)
AND:    Value nodes are placed in z=0.55-0.8 (cortex)
AND:    Concept nodes are placed in z=0.7-1.0 (cortex)
```

### B3: Interactive Exploration

**Why:** A static image of 220 nodes is still hard to read — occlusion, overlap, hidden backside structure. Interactive 3D allows the viewer to rotate the brain to see it from every angle, zoom into dense regions, toggle layers on/off to isolate regions, and filter by type. The interaction is what turns a picture into an instrument of understanding. (Serves O1, O3)

```
GIVEN:  A rendered HTML brain scan is open in a browser
WHEN:   User clicks and drags to rotate
THEN:   The 3D brain rotates smoothly around its center with damped inertia
AND:    User can scroll to zoom in/out
AND:    Layer toggles (stem/limbic/cortex) show or hide corresponding nodes
AND:    Type legend items toggle visibility of that node type
AND:    A "Show links" checkbox toggles link visibility
```

### B4: Node Hover Reveals Identity

**Why:** The visual properties (color, size, glow) communicate type, weight, and energy, but sometimes you need the specific label and numbers. Hovering a node reveals its identity without requiring content access — just the topology metadata. This bridges the gap between visual pattern and specific data point. (Serves O3)

```
GIVEN:  A rendered HTML brain scan is open with visible nodes
WHEN:   User moves mouse over a node
THEN:   A tooltip displays: node type (colored), label, weight, energy, and layer
AND:    The tooltip disappears when the mouse moves away from all nodes
```

---

## OBJECTIVES SERVED

| Behavior ID | Objective | Why It Matters |
|-------------|-----------|----------------|
| B1 | O1 (Make brain state visible) | Transforms raw graph into positioned 3D data |
| B2 | O2 (Anatomy-based layering) | Creates spatial separation by semantic type |
| B3 | O1, O3 (Visible + actionable) | Enables free exploration of brain structure |
| B4 | O3 (Actionable insight) | Connects visual patterns to specific data points |

---

## INPUTS / OUTPUTS

### Primary Function: `extract_brain_scan()`

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| citizen_handle | str | The citizen's handle (e.g., "dragon_slayer"), used to select the FalkorDB graph `brain_{handle}` |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| scan | BrainScan | Dataclass with citizen_id, list of ScanNode (with 3D positions), list of ScanLink, and stats dict |

**Side Effects:**

- Reads from FalkorDB (two queries: nodes and links). Read-only, no writes.
- When called via `__main__`, writes JSON to `data/brain_scans/{handle}_scan.json`

### Secondary Function: `render_html()`

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| scan_path | Path | Path to the JSON scan file produced by Stage 1 |
| output_path | Path | Path where the HTML file should be written |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| (none) | void | Writes HTML file to output_path |

**Side Effects:**

- Writes a standalone HTML file to disk
- Prints the output path and file:// URL to stdout

---

## EDGE CASES

### E1: Empty Brain Graph

```
GIVEN:  A citizen's brain graph exists but has 0 nodes
THEN:   extract_brain_scan() returns a BrainScan with empty nodes, empty links, and stats showing all zeros
AND:    render_html() produces a valid HTML file showing an empty 3D scene with the info panel displaying "Nodes: 0"
```

### E2: Unknown Node Type

```
GIVEN:  A node has a type not in the LAYER_Z mapping (e.g., "stimulus", "frequency", or a new type)
THEN:   The node is positioned in the default z-band (0.4-0.6) with gray color (#9ca3af)
AND:    It appears in the cortex-like middle area rather than being dropped
```

### E3: FalkorDB Unreachable

```
GIVEN:  FalkorDB is not running or the graph name doesn't exist
THEN:   extract_brain_scan() raises a connection error (no fallback, no fake data)
```

### E4: Missing Node Fields

```
GIVEN:  A node row has None for weight or energy
THEN:   Defaults are used: weight=0.5, energy=0.0
AND:    The node is still positioned and rendered normally
```

---

## ANTI-BEHAVIORS

What should NOT happen:

### A1: Content Leakage

```
GIVEN:   A brain graph contains nodes with content and synthesis fields
WHEN:    extract_brain_scan() queries FalkorDB
MUST NOT: Read, store, or transmit content or synthesis fields
INSTEAD:  Query only: id, type, node_type, name, weight, energy for nodes; id, relation_kind, weight, energy, trust for links
```

### A2: Graph Modification

```
GIVEN:   A citizen's brain graph is being scanned
WHEN:    extract_brain_scan() or render_html() runs
MUST NOT: Write, update, or delete any data in FalkorDB
INSTEAD:  All operations are read-only. The scan is an observation, not an intervention.
```

### A3: External Dependency at Render Time

```
GIVEN:   A rendered HTML file is opened in a browser
WHEN:    The page loads
MUST NOT: Make any requests to FalkorDB or any backend API
INSTEAD:  All data is embedded in the HTML as JSON literals. Only external requests are CDN loads for Three.js.
```

---

## MARKERS

<!-- @mind:todo Define behavior for very large brains (>1000 nodes) — potential LOD or clustering needed -->
<!-- @mind:proposition Add B5: Temporal comparison — show two brain scans side by side to visualize evolution over time -->
