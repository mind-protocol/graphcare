# Brain Scan — Implementation: Code Architecture and Structure

```
STATUS: DESIGNING
CREATED: 2026-03-18
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Brain_Scan.md
BEHAVIORS:       ./BEHAVIORS_Brain_Scan.md
PATTERNS:        ./PATTERNS_Brain_Scan.md
ALGORITHM:       ./ALGORITHM_Brain_Scan.md
VALIDATION:      ./VALIDATION_Brain_Scan.md
THIS:            IMPLEMENTATION_Brain_Scan.md (you are here)
HEALTH:          ./HEALTH_Brain_Scan.md
SYNC:            ./SYNC_Brain_Scan.md

IMPL:            services/brain_scan/brain_scan_data_extractor.py
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## CODE STRUCTURE

```
services/brain_scan/
├── brain_scan_data_extractor.py    # Stage 1: FalkorDB → JSON (260 lines)
└── render_brain_scan_html.py       # Stage 2: JSON → HTML (248 lines)
```

Output:
```
data/brain_scans/
├── {handle}_scan.json              # Extracted scan data with 3D positions
└── {handle}_brain.html             # Standalone interactive visualization
```

### File Responsibilities

| File | Purpose | Key Functions/Classes | Lines | Status |
|------|---------|----------------------|-------|--------|
| `brain_scan_data_extractor.py` | Extract brain topology from FalkorDB, compute 3D positions, map visual properties | `extract_brain_scan()`, `save_scan()`, `ScanNode`, `ScanLink`, `BrainScan` | ~260 | OK |
| `render_brain_scan_html.py` | Generate standalone HTML with Three.js from scan JSON | `render_html()` | ~248 | OK |

**Size Thresholds:**
- **OK** (<400 lines): Healthy size, easy to understand
- **WATCH** (400-700 lines): Getting large, consider extraction opportunities
- **SPLIT** (>700 lines): Too large, must split before adding more code

---

## DESIGN PATTERNS

### Architecture Pattern

**Pattern:** Pipeline (two-stage)

**Why this pattern:** The brain scan is a data transformation pipeline. Stage 1 transforms graph data into positioned JSON. Stage 2 transforms JSON into HTML. Each stage is independently runnable, testable, and replaceable. The JSON intermediate format is the contract between stages — change one stage without touching the other.

### Code Patterns in Use

| Pattern | Applied To | Purpose |
|---------|------------|---------|
| Dataclass | `ScanNode`, `ScanLink`, `BrainScan` | Typed data containers with default values, serializable via `asdict()` |
| Lookup Tables | `LAYER_Z`, `NODE_COLORS`, `LINK_COLORS` | Centralized mapping from semantic type to visual property — single source of truth |
| Template String | `render_html()` | HTML generation via f-string with embedded JSON — no template engine dependency |

### Anti-Patterns to Avoid

- **Content Access Creep**: Tempting to add content preview to hover tooltips — violates V1. Never query content fields.
- **Live DB in Renderer**: Tempting to add "refresh" to the HTML that re-queries FalkorDB — violates O4 and V5. The HTML is a static artifact.
- **God File**: If either file approaches 400 lines, extract data structures or constants into a shared module.

### Boundaries

| Boundary | Inside | Outside | Interface |
|----------|--------|---------|-----------|
| Stage 1 (extractor) | FalkorDB queries, positioning, visual mapping | HTML rendering, browser interaction | `BrainScan` dataclass / JSON file |
| Stage 2 (renderer) | HTML generation, Three.js scene composition | Database access, positioning logic | JSON file input, HTML file output |

---

## SCHEMA

### ScanNode

```yaml
ScanNode:
  required:
    - id: str                # unique node identifier
    - node_type: str         # semantic type (process, desire, etc.)
    - label: str             # display name (max 50 chars)
    - x: float               # horizontal position
    - y: float               # depth position
    - z: float               # vertical position (anatomy layer)
  optional:
    - weight: float          # default 0.5
    - energy: float          # default 0.0
    - color: str             # default "#9ca3af"
    - size: float            # default 5.0
    - glow: bool             # default False
    - layer: str             # default "cortex"
  constraints:
    - x, y in approximately [-1.0, 1.0]
    - z in [0.0, 1.0]
    - no NaN or Infinity in coordinates
```

### ScanLink

```yaml
ScanLink:
  required:
    - source: str            # source node id
    - target: str            # target node id
    - relation: str          # relation kind
  optional:
    - weight: float          # default 0.5
    - energy: float          # default 0.0
    - trust: float           # default 0.5
    - color: str             # default "#9ca3af"
    - width: float           # default 1.0
    - opacity: float         # default 0.3
    - glow: bool             # default False
  constraints:
    - source and target must reference existing node IDs
```

### BrainScan

```yaml
BrainScan:
  required:
    - citizen_id: str        # citizen handle
  optional:
    - nodes: list[ScanNode]  # default empty
    - links: list[ScanLink]  # default empty
    - stats: dict            # default empty
  relationships:
    - nodes: contains ScanNode instances
    - links: contains ScanLink instances referencing nodes by ID
```

---

## ENTRY POINTS

| Entry Point | File:Line | Triggered By |
|-------------|-----------|--------------|
| `extract_brain_scan(handle)` | `brain_scan_data_extractor.py:114` | CLI (`__main__`), or called by health assessment pipeline |
| `save_scan(scan, path)` | `brain_scan_data_extractor.py:240` | Called after `extract_brain_scan()` to persist results |
| `render_html(scan_path, output_path)` | `render_brain_scan_html.py:21` | CLI (`__main__`), or called after scan extraction |

---

## DATA FLOW AND DOCKING (FLOW-BY-FLOW)

### Brain Scan Extraction: FalkorDB to Interactive HTML

Explain what this flow covers: The complete pipeline from querying a citizen's brain graph to producing a viewable HTML brain scan. This is the primary (and currently only) flow in the module. It crosses the FalkorDB boundary (read-only), the filesystem boundary (write JSON + HTML), and the CDN boundary (Three.js at render time). It matters because it's the entire value delivery path.

```yaml
flow:
  name: brain_scan_extraction
  purpose: Transform brain graph topology into interactive 3D visualization
  scope: FalkorDB read → JSON output → HTML output
  steps:
    - id: step_1_query_nodes
      description: Query all nodes from citizen's brain graph
      file: services/brain_scan/brain_scan_data_extractor.py
      function: extract_brain_scan()
      input: citizen_handle (str)
      output: node_rows (list[tuple])
      trigger: CLI invocation or pipeline call
      side_effects: FalkorDB read (2 Cypher queries)
    - id: step_2_position_nodes
      description: Group by type, position in anatomy layers via golden angle spiral
      file: services/brain_scan/brain_scan_data_extractor.py
      function: extract_brain_scan() (inline)
      input: type_groups (dict[str, list])
      output: list[ScanNode] with x,y,z coordinates
      trigger: Follows step_1
      side_effects: none
    - id: step_3_query_links
      description: Query all links from brain graph
      file: services/brain_scan/brain_scan_data_extractor.py
      function: extract_brain_scan() (inline)
      input: graph handle
      output: link_rows (list[tuple])
      trigger: Follows step_2
      side_effects: FalkorDB read
    - id: step_4_save_json
      description: Serialize BrainScan to JSON file
      file: services/brain_scan/brain_scan_data_extractor.py
      function: save_scan()
      input: BrainScan dataclass
      output: JSON file at data/brain_scans/{handle}_scan.json
      trigger: Follows step_3
      side_effects: File write
    - id: step_5_render_html
      description: Load JSON, generate Three.js HTML
      file: services/brain_scan/render_brain_scan_html.py
      function: render_html()
      input: scan JSON path
      output: HTML file at data/brain_scans/{handle}_brain.html
      trigger: CLI invocation or pipeline call
      side_effects: File write
  docking_points:
    guidance:
      include_when: Boundary crossing (DB read, file write), data transformation
      omit_when: Internal variable assignments, loop iterations
      selection_notes: Focus on the DB boundary and the two file outputs
    available:
      - id: dock_falkordb_read
        type: db
        direction: input
        file: services/brain_scan/brain_scan_data_extractor.py
        function: extract_brain_scan()
        trigger: FalkorDB graph.query()
        payload: Result sets (node_rows, link_rows)
        async_hook: not_applicable
        needs: none
        notes: Read-only. Two queries per scan. Connection failure raises exception.
      - id: dock_json_output
        type: file
        direction: output
        file: services/brain_scan/brain_scan_data_extractor.py
        function: save_scan()
        trigger: Called after extraction
        payload: JSON file with nodes[], links[], stats
        async_hook: not_applicable
        needs: none
        notes: Creates parent dirs. Overwrites existing file.
      - id: dock_html_output
        type: file
        direction: output
        file: services/brain_scan/render_brain_scan_html.py
        function: render_html()
        trigger: Called with scan path
        payload: Standalone HTML file
        async_hook: not_applicable
        needs: none
        notes: Creates parent dirs. Requires CDN access at view time.
    health_recommended:
      - dock_id: dock_falkordb_read
        reason: FalkorDB connectivity is the primary failure mode (crashes under load, data loss on restart)
      - dock_id: dock_json_output
        reason: Verifying scan completeness (>0 nodes, valid positions) catches extraction failures
```

---

## LOGIC CHAINS

### LC1: Extract and Render

**Purpose:** End-to-end brain scan production

```
citizen_handle (str)
  → extract_brain_scan()         # Query FalkorDB, position nodes, map visual props
    → save_scan()                # Serialize BrainScan to JSON
      → render_html()            # Load JSON, generate Three.js HTML
        → {handle}_brain.html    # Standalone interactive file
```

**Data transformation:**
- Input: `str` — citizen handle
- After step 1: `BrainScan` — nodes with 3D positions, links with visual props, stats
- After step 2: `JSON file` — serialized scan at data/brain_scans/
- Output: `HTML file` — standalone Three.js visualization

---

## MODULE DEPENDENCIES

### Internal Dependencies

```
brain_scan_data_extractor.py
    └── imports → json, math, random, dataclasses, pathlib, logging
    └── imports → falkordb (external)

render_brain_scan_html.py
    └── imports → json, sys, pathlib
    └── references → Three.js r128 (CDN, in generated HTML)
    └── references → OrbitControls.js (CDN, in generated HTML)
```

### External Dependencies

| Package | Used For | Imported By |
|---------|----------|-------------|
| `falkordb` | Python client for FalkorDB graph database | `brain_scan_data_extractor.py` |
| `Three.js r128` | 3D rendering in browser (loaded via CDN) | `render_brain_scan_html.py` (embedded in output) |
| `OrbitControls.js` | Mouse orbit camera controls (loaded via CDN) | `render_brain_scan_html.py` (embedded in output) |

---

## STATE MANAGEMENT

### Where State Lives

| State | Location | Scope | Lifecycle |
|-------|----------|-------|-----------|
| Brain graph data | FalkorDB `brain_{handle}` | External, persistent | Created by mind-mcp, read-only by brain scan |
| Scan JSON | `data/brain_scans/{handle}_scan.json` | File, per-citizen | Created per extraction, overwritten on re-scan |
| Scan HTML | `data/brain_scans/{handle}_brain.html` | File, per-citizen | Created per render, overwritten on re-render |

### State Transitions

```
No brain scan ──extract_brain_scan()──▶ JSON exists ──render_html()──▶ HTML exists
                                         ↑                              ↑
                                    (re-extract overwrites)       (re-render overwrites)
```

---

## RUNTIME BEHAVIOR

### Initialization

```
1. Import falkordb, connect to localhost:6379
2. Select graph brain_{handle}
3. Ready to query
```

### Main Loop / Request Cycle

```
1. extract_brain_scan(handle) — query nodes, position, query links, map visual props
2. save_scan(scan, path) — serialize to JSON
3. render_html(scan_path, output_path) — generate HTML from JSON
4. User opens HTML in browser — Three.js renders pre-computed scene
```

### Shutdown

```
1. FalkorDB connection is implicit (per-query), no persistent connection to close
2. Files are written and closed within function scope
```

---

## CONCURRENCY MODEL

| Component | Model | Notes |
|-----------|-------|-------|
| Data extraction | Synchronous | Single-threaded. FalkorDB client is synchronous. |
| HTML rendering | Synchronous | Pure string generation, no I/O during render. |
| Browser visualization | Event-driven (requestAnimationFrame) | Three.js render loop in browser, unrelated to Python. |

---

## CONFIGURATION

| Config | Location | Default | Description |
|--------|----------|---------|-------------|
| `FALKORDB_HOST` | `brain_scan_data_extractor.py:40` | `"localhost"` | FalkorDB server hostname |
| `FALKORDB_PORT` | `brain_scan_data_extractor.py:41` | `6379` | FalkorDB server port |
| Three.js version | `render_brain_scan_html.py:85` | `r128` | Three.js CDN version |
| Output directory | CLI `__main__` blocks | `data/brain_scans/` | Where scan files are written |

---

## BIDIRECTIONAL LINKS

### Code → Docs

Files that reference this documentation:

| File | Line | Reference |
|------|------|-----------|
| `services/brain_scan/brain_scan_data_extractor.py` | 4 | `DOCS: docs/care/brain_scan/ (to be created)` |

### Docs → Code

| Doc Section | Implemented In |
|-------------|----------------|
| ALGORITHM Step 1 (Query Nodes) | `brain_scan_data_extractor.py:extract_brain_scan()` line 122 |
| ALGORITHM Step 3 (Position Nodes) | `brain_scan_data_extractor.py:extract_brain_scan()` lines 148-181 |
| ALGORITHM Step 4 (Query Links) | `brain_scan_data_extractor.py:extract_brain_scan()` lines 184-209 |
| ALGORITHM render_html | `render_brain_scan_html.py:render_html()` line 21 |
| BEHAVIOR B1 | `brain_scan_data_extractor.py:extract_brain_scan()` |
| BEHAVIOR B2 | `brain_scan_data_extractor.py` lines 148-166 (LAYER_Z + spiral) |
| BEHAVIOR B3 | `render_brain_scan_html.py` (OrbitControls, layer toggles) |
| BEHAVIOR B4 | `render_brain_scan_html.py` (raycaster + hover-info div) |
| VALIDATION V1 | `brain_scan_data_extractor.py` lines 122-123 (Cypher query — no content fields) |

---

## EXTRACTION CANDIDATES

No files are currently approaching WATCH/SPLIT status. Both files are well under 400 lines.

| File | Current | Target | Extract To | What to Move |
|------|---------|--------|------------|--------------|
| (none needed) | — | — | — | — |

---

## MARKERS

<!-- @mind:todo Update the DOCS comment in brain_scan_data_extractor.py line 4 to point to the now-created doc chain -->
<!-- @mind:proposition Extract LAYER_Z, NODE_COLORS, LINK_COLORS into a shared constants module if other brain_scan tools need them -->
