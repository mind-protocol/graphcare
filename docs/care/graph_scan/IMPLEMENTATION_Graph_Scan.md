# Graph Scan — Implementation: Code Architecture and Structure

```
STATUS: DESIGNING
CREATED: 2026-03-18
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Graph_Scan.md
BEHAVIORS:       ./BEHAVIORS_Graph_Scan.md
PATTERNS:        ./PATTERNS_Graph_Scan.md
ALGORITHM:       ./ALGORITHM_Graph_Scan.md
VALIDATION:      ./VALIDATION_Graph_Scan.md
THIS:            IMPLEMENTATION_Graph_Scan.md (you are here)
HEALTH:          ./HEALTH_Graph_Scan.md
SYNC:            ./SYNC_Graph_Scan.md

IMPL:            services/graph_scan/brain_data_extractor.py
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## CODE STRUCTURE

```
services/graph_scan/
├── brain_data_extractor.py      # L1: FalkorDB brain → positioned JSON
├── universe_data_extractor.py   # L3: FalkorDB universe → positioned JSON
├── render_html.py               # Three.js renderer: JSON → standalone HTML
├── visual_mapping_proposal.yaml # Full mapping spec (all fields to visuals)
└── README.md                    # Usage guide
```

### File Responsibilities

| File | Purpose | Key Functions/Classes | Lines | Status |
|------|---------|----------------------|-------|--------|
| `brain_data_extractor.py` | L1 brain extraction: query FalkorDB, TF-IDF, centroid subtraction, UMAP 3D, visual properties | `extract_graph_scan()`, `save_scan()`, `_compute_semantic_positions()`, `ScanNode`, `ScanLink`, `BrainScan` | ~525 | WATCH |
| `universe_data_extractor.py` | L3 universe extraction: same pipeline adapted for L3 types and fields | `extract_universe_scan()`, `save_scan()`, `_compute_positions()`, `ScanNode`, `ScanLink`, `UniverseScan` | ~322 | OK |
| `render_html.py` | HTML generation: JSON to Three.js scene with curved links, matte nodes, hover panel | `render_html()` | ~338 | OK |
| `visual_mapping_proposal.yaml` | Specification of all field-to-visual mappings | (YAML spec, not executable) | ~584 | OK |

**Size Thresholds:**
- **OK** (<400 lines): Healthy size, easy to understand
- **WATCH** (400-700 lines): Getting large, consider extraction opportunities
- **SPLIT** (>700 lines): Too large, must split before adding more code

---

## DESIGN PATTERNS

### Architecture Pattern

**Pattern:** Pipeline (Extract → Position → Render)

**Why this pattern:** Each stage has a clear boundary. Extractors produce JSON; the renderer consumes JSON. The JSON intermediate format decouples extraction from rendering, allowing two extractors to share one renderer. Stages can be run independently (extract once, render many times with different settings).

### Code Patterns in Use

| Pattern | Applied To | Purpose |
|---------|------------|---------|
| Dataclass | `ScanNode`, `ScanLink`, `BrainScan`, `UniverseScan` | Structured data with defaults, easy serialization via `asdict()` |
| Lookup Table | `NODE_COLORS`, `LINK_COLORS`, `L3_COLORS`, `MODALITY_SHAPES` | Type-to-visual property mapping without conditionals |
| Fallback Strategy | `_compute_semantic_positions()` | If UMAP fails or <5 nodes, fall back to golden angle sphere |

### Anti-Patterns to Avoid

- **Shared mutable state**: Extractors should not share FalkorDB connections or cache state between runs
- **God Object**: brain_data_extractor.py is at WATCH (525 lines) — visual mapping functions could be extracted to a shared module
- **Renderer knowing about L1 vs L3**: The renderer should stay source-agnostic — it reads JSON, it doesn't import extractor types

### Boundaries

| Boundary | Inside | Outside | Interface |
|----------|--------|---------|-----------|
| Extractor | FalkorDB queries, TF-IDF, UMAP, visual computation | Rendering, file I/O format | `BrainScan`/`UniverseScan` dataclass → `save_scan()` → JSON |
| Renderer | HTML generation, Three.js scene construction | Data extraction, positioning | `render_html(scan_path, output_path)` |

---

## SCHEMA

### Scan JSON (output format)

```yaml
ScanJSON:
  required:
    - citizen_id: str          # (L1) or graph_name: str (L3)
    - nodes: list[ScanNodeJSON] # Positioned nodes with visual properties
    - links: list[ScanLinkJSON] # Links with visual properties
    - stats: dict              # Counts and type breakdown
  optional:
    - metabolism: dict         # L1 only: from __metabolism__ meta node
    - regions: dict            # L1 only: self_model, partner_model, goal_space
    - scan_type: str           # "universe_l3" for L3 scans
  constraints:
    - All node positions must be finite floats
    - All nodes must have id, node_type, label, x, y, z, color, radius, opacity
```

### ScanNodeJSON (minimum compatible fields)

```yaml
ScanNodeJSON:
  required:
    - id: str
    - node_type: str
    - label: str
    - x: float
    - y: float
    - z: float
    - color: str (hex)
    - radius: float
    - opacity: float
  optional:
    - glow: float
    - weight: float
    - energy: float
    - stability: float
    - recency: float
    - self_relevance: float    # L1 only
    - partner_relevance: float # L1 only
    - goal_relevance: float    # L1 only
    - patina: float            # L1 only
    - inner_halo: float        # L1 only
    - shape: str               # L1 only
```

---

## ENTRY POINTS

| Entry Point | File:Line | Triggered By |
|-------------|-----------|--------------|
| `extract_graph_scan()` | `brain_data_extractor.py:309` | CLI (`python brain_data_extractor.py {handle}`), agent scripts |
| `extract_universe_scan()` | `universe_data_extractor.py:115` | CLI (`python universe_data_extractor.py {graph_name}`), agent scripts |
| `render_html()` | `render_html.py:13` | CLI (`python render_html.py {handle}`), agent scripts |

---

## DATA FLOW AND DOCKING (FLOW-BY-FLOW)

### L1 Brain Scan: FalkorDB Brain to Interactive HTML

Explains the end-to-end flow for L1 citizen brain visualization. This is the primary flow — it transforms a citizen's brain graph into a navigable 3D HTML.

```yaml
flow:
  name: l1_brain_scan
  purpose: Convert L1 citizen brain to positioned 3D visualization
  scope: FalkorDB brain_{handle} → JSON → HTML
  steps:
    - id: query_nodes
      description: Query all node fields from FalkorDB brain graph
      file: services/graph_scan/brain_data_extractor.py
      function: extract_graph_scan
      input: citizen_handle (str)
      output: list[dict] (raw node rows)
      trigger: CLI or agent invocation
      side_effects: FalkorDB read
    - id: query_links
      description: Query all link fields from FalkorDB
      file: services/graph_scan/brain_data_extractor.py
      function: extract_graph_scan
      input: FalkorDB graph handle
      output: list[dict] (raw link rows)
      trigger: Follows query_nodes in same function
      side_effects: FalkorDB read
    - id: compute_positions
      description: TF-IDF + centroid subtraction + UMAP 3D positioning
      file: services/graph_scan/brain_data_extractor.py
      function: _compute_semantic_positions
      input: list[dict] (nodes with labels)
      output: list[tuple(x,y,z)]
      trigger: Called by extract_graph_scan
      side_effects: none
    - id: compute_visuals
      description: Map physics fields to visual properties
      file: services/graph_scan/brain_data_extractor.py
      function: extract_graph_scan (inline)
      input: raw fields + positions
      output: list[ScanNode], list[ScanLink]
      trigger: Follows positioning
      side_effects: none
    - id: save_json
      description: Serialize BrainScan to JSON file
      file: services/graph_scan/brain_data_extractor.py
      function: save_scan
      input: BrainScan
      output: JSON file at data/graph_scans/{handle}_scan.json
      trigger: Follows visual computation
      side_effects: filesystem write
    - id: render
      description: Generate Three.js HTML from JSON
      file: services/graph_scan/render_html.py
      function: render_html
      input: scan JSON path
      output: HTML file at data/graph_scans/{handle}_brain.html
      trigger: CLI or agent invocation (separate step)
      side_effects: filesystem write
  docking_points:
    guidance:
      include_when: Transformative steps that change data shape or cross boundaries
      omit_when: Internal variable assignments, trivial pass-throughs
      selection_notes: FalkorDB reads and file writes are the main boundary crossings
    available:
      - id: dock_falkordb_read
        type: db
        direction: input
        file: services/graph_scan/brain_data_extractor.py
        function: extract_graph_scan
        trigger: FalkorDB graph.query()
        payload: Cypher result sets (node rows, link rows)
        async_hook: not_applicable
        needs: none
        notes: Read-only queries. V1 invariant lives here — content/synthesis must never appear in RETURN.
      - id: dock_json_output
        type: file
        direction: output
        file: services/graph_scan/brain_data_extractor.py
        function: save_scan
        trigger: Path.write_text()
        payload: JSON with nodes[], links[], stats
        async_hook: not_applicable
        needs: none
        notes: Intermediate format. V3 (valid positions) and V4 (compatible format) can be verified here.
      - id: dock_html_output
        type: file
        direction: output
        file: services/graph_scan/render_html.py
        function: render_html
        trigger: Path.write_text()
        payload: HTML string with embedded Three.js scene
        async_hook: not_applicable
        needs: none
        notes: Final output. V1 can be re-verified here (no content in HTML).
    health_recommended:
      - dock_id: dock_falkordb_read
        reason: V1 (topology-only) is enforced at the query level — verify content/synthesis never in RETURN
      - dock_id: dock_json_output
        reason: V3 (valid positions) and V4 (compatible format) can be verified on the JSON output
```

---

## LOGIC CHAINS

### LC1: L1 Brain Extraction

**Purpose:** Convert a citizen's brain graph into positioned, visually-mapped JSON.

```
citizen_handle (str)
  -> extract_graph_scan()              # entry point
    -> FalkorDB.select_graph()         # connect to brain_{handle}
    -> graph.query() [nodes]           # all node fields
    -> graph.query() [links]           # all link fields
    -> _compute_semantic_positions()   # TF-IDF + centroid subtraction + UMAP
    -> visual property computation     # inline in extract_graph_scan
    -> BrainScan (dataclass)
  -> save_scan()                       # serialize to JSON
    -> JSON file
```

**Data transformation:**
- Input: `str` (citizen handle)
- After query: `list[list]` (raw FalkorDB result rows)
- After positioning: `list[tuple(float,float,float)]` (3D coordinates)
- After visuals: `BrainScan` (dataclass with ScanNode[], ScanLink[])
- Output: `JSON file` (serialized scan)

### LC2: Rendering

**Purpose:** Convert positioned JSON to interactive HTML.

```
scan_path (Path)
  -> json.loads()                      # parse scan JSON
  -> HTML template formatting          # embed nodes/links as JS
  -> Three.js scene (nodes, links, UI) # inline in template
  -> output_path.write_text()          # save HTML
```

---

## MODULE DEPENDENCIES

### Internal Dependencies

```
brain_data_extractor.py
    └── (standalone — no internal imports)
universe_data_extractor.py
    └── (standalone — no internal imports)
render_html.py
    └── (standalone — no internal imports)
```

Note: The three files are intentionally independent. They share no code, though brain_data_extractor and universe_data_extractor duplicate visual mapping functions (_node_radius, _node_glow, etc.).

### External Dependencies

| Package | Used For | Imported By |
|---------|----------|-------------|
| `falkordb` | FalkorDB client for graph queries | `brain_data_extractor.py`, `universe_data_extractor.py` |
| `umap-learn` | UMAP dimensionality reduction (3D positioning) | `brain_data_extractor.py`, `universe_data_extractor.py` |
| `scikit-learn` | TfidfVectorizer for text-to-vector conversion | `brain_data_extractor.py`, `universe_data_extractor.py` |
| `numpy` | Array operations for centroid subtraction and normalization | `brain_data_extractor.py`, `universe_data_extractor.py` |
| Three.js r128 | 3D rendering in browser (loaded via CDN) | `render_html.py` (embedded in HTML output) |

---

## STATE MANAGEMENT

### Where State Lives

| State | Location | Scope | Lifecycle |
|-------|----------|-------|-----------|
| FalkorDB connection | `extract_graph_scan()` local | function | Created per invocation, no pooling |
| Scan data | `BrainScan`/`UniverseScan` dataclass | function return | Created during extraction, serialized to JSON |
| JSON scan file | `data/graph_scans/{name}_scan.json` | filesystem | Persists until overwritten by next extraction |
| HTML file | `data/graph_scans/{name}_brain.html` | filesystem | Persists until overwritten |

### State Transitions

```
(no state) ──extract──> BrainScan (in memory) ──save──> JSON (on disk) ──render──> HTML (on disk)
```

---

## RUNTIME BEHAVIOR

### Initialization

```
1. Connect to FalkorDB (localhost:6379)
2. Select graph (brain_{handle} or {universe_name})
3. No warm-up, no caching, no persistent state
```

### Main Execution (CLI)

```
1. Parse CLI arg (handle or graph_name)
2. Run extractor (query + position + visual computation)
3. Save JSON
4. Print stats
5. (Optional separate step) Run renderer on JSON
```

### Shutdown

```
1. FalkorDB connection closed implicitly (no explicit cleanup)
2. No persistent state to clean up
```

---

## CONFIGURATION

| Config | Location | Default | Description |
|--------|----------|---------|-------------|
| `FALKORDB_HOST` | `brain_data_extractor.py:37` | `"localhost"` | FalkorDB host |
| `FALKORDB_PORT` | `brain_data_extractor.py:38` | `6379` | FalkorDB port |
| `TF-IDF max_features` | `brain_data_extractor.py:241` | `200` (L1), `300` (L3) | Feature count for vectorization |
| `UMAP n_neighbors` | `brain_data_extractor.py:259` | `min(20, n-1)` | UMAP neighborhood size |
| `UMAP random_state` | `brain_data_extractor.py:263` | `42` | Deterministic seed |

---

## BIDIRECTIONAL LINKS

### Code -> Docs

Files that reference this documentation:

| File | Line | Reference |
|------|------|-----------|
| `services/graph_scan/brain_data_extractor.py` | 4 | `# DOCS: docs/care/graph_scan/PATTERNS_Graph_Scan.md` |
| `services/graph_scan/universe_data_extractor.py` | 3 | `# DOCS: docs/care/graph_scan/PATTERNS_Graph_Scan.md` |

### Docs -> Code

| Doc Section | Implemented In |
|-------------|----------------|
| ALGORITHM step 1 (query) | `brain_data_extractor.py:extract_graph_scan` |
| ALGORITHM step 3 (TF-IDF) | `brain_data_extractor.py:_compute_semantic_positions` |
| ALGORITHM step 4 (centroid subtraction) | `brain_data_extractor.py:_compute_semantic_positions` |
| ALGORITHM step 5 (UMAP) | `brain_data_extractor.py:_compute_semantic_positions` |
| ALGORITHM rendering | `render_html.py:render_html` |
| BEHAVIOR B1 | `brain_data_extractor.py:extract_graph_scan` + `render_html.py:render_html` |
| BEHAVIOR B2 | `brain_data_extractor.py:_compute_semantic_positions` (centroid subtraction) |
| VALIDATION V1 | Cypher queries in `brain_data_extractor.py:320-327` and `universe_data_extractor.py:126-130` |

---

## EXTRACTION CANDIDATES

Files approaching WATCH/SPLIT status — identify what can be extracted:

| File | Current | Target | Extract To | What to Move |
|------|---------|--------|------------|--------------|
| `brain_data_extractor.py` | ~525L | <400L | `shared_visual_mapping.py` | `_node_radius`, `_node_glow`, `_node_opacity`, `_link_width`, `_link_opacity`, `_link_glow`, `_link_wave`, `_link_dash`, color lookup tables |

---

## MARKERS

<!-- @mind:TODO Extract shared visual mapping functions into a common module to deduplicate between L1 and L3 extractors -->
<!-- @mind:proposition Add a universe renderer mode that handles graph_name instead of citizen_id in the HTML template -->
