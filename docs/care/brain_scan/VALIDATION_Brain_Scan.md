# Brain Scan — Validation: What Must Be True

```
STATUS: DESIGNING
CREATED: 2026-03-18
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Brain_Scan.md
PATTERNS:        ./PATTERNS_Brain_Scan.md
BEHAVIORS:       ./BEHAVIORS_Brain_Scan.md
THIS:            VALIDATION_Brain_Scan.md (you are here)
ALGORITHM:       ./ALGORITHM_Brain_Scan.md (HOW — mechanisms go here)
IMPLEMENTATION:  ./IMPLEMENTATION_Brain_Scan.md
HEALTH:          ./HEALTH_Brain_Scan.md
SYNC:            ./SYNC_Brain_Scan.md
```

---

## PURPOSE

**Validation = what we care about being true.**

Not mechanisms. Not test paths. Not how things work.

What properties, if violated, would mean the brain scan has failed its purpose?

These are the value-producing invariants — the things that make the module worth building.

---

## INVARIANTS

### V1: Privacy Through Topology

**Why we care:** GraphCare's foundational promise is the kidney metaphor — we read structure, never content. If content or synthesis fields are accessed during a brain scan, we have violated the core trust contract. A single leak would invalidate the entire approach. This is not a feature — it is the ethical foundation.

```
MUST:   Only query topology fields: id, type, node_type, name, weight, energy (nodes); id, relation_kind, weight, energy, trust (links)
NEVER:  Read, store, transmit, or embed the content or synthesis fields from any node or link
```

### V2: Every Node Gets a Valid Position

**Why we care:** A node without a valid 3D position will not render, creating a gap in the visualization. Invisible nodes mean invisible structure — the scan would lie by omission. NaN coordinates would crash Three.js. Positions outside bounds would place nodes outside the viewable area.

```
MUST:   Every node in the scan has finite x, y, z values (no NaN, no Infinity)
MUST:   All coordinates fall within approximately [-1.0, 1.0] for x/y and [0.0, 1.0] for z
NEVER:  Produce a ScanNode with NaN, None, or Infinity in any coordinate
```

### V3: Anatomy Layers Are Correct

**Why we care:** The anatomy-layer metaphor is the primary interface for understanding brain structure. If process nodes appear in the cortex or concept nodes appear in the stem, the visual metaphor lies. The viewer would form incorrect intuitions about brain composition. The spatial encoding only works if it's faithful to the type-to-layer mapping.

```
MUST:   Process nodes are positioned with z in [0.0, 0.2] (stem)
MUST:   Desire nodes are positioned with z in [0.25, 0.45] (limbic)
MUST:   Value nodes are positioned with z in [0.55, 0.8] (cortex)
MUST:   Concept nodes are positioned with z in [0.7, 1.0] (cortex)
NEVER:  A node's z-coordinate falls outside its type's defined z-band (before jitter)
```

### V4: Visual Properties Map Accurately

**Why we care:** Visual properties are the scan's data language. If color doesn't match type, or size doesn't match weight, the viewer reads false signals. A small node should mean low weight. A red node should mean desire. If these mappings are wrong, the visualization misleads rather than reveals.

```
MUST:   Node color matches the NODE_COLORS mapping for its type
MUST:   Node size = 3 + weight * 12 (within rounding tolerance)
MUST:   Node glow = True when energy > 0.3, False otherwise
MUST:   Link color matches the LINK_COLORS mapping for its relation
MUST:   Link opacity = 0.1 + weight * 0.9 (within rounding tolerance)
NEVER:  A visual property contradicts its source data field
```

### V5: Standalone HTML Renders

**Why we care:** The HTML file is the deliverable — the thing a human opens and explores. If it fails to render because of missing dependencies, broken JavaScript, or malformed JSON embedding, the entire pipeline produced nothing useful. The scan must be self-contained except for CDN Three.js.

```
MUST:   The generated HTML file is valid HTML5 that opens in any modern browser
MUST:   The only external dependencies are Three.js r128 and OrbitControls.js from CDN
MUST:   All scan data is embedded as JSON literals within <script> tags
NEVER:  Require a local server, backend API, or FalkorDB connection to view the rendered scan
```

---

## PRIORITY

| Priority | Meaning | If Violated |
|----------|---------|-------------|
| **CRITICAL** | System purpose fails | Unusable |
| **HIGH** | Major value lost | Degraded severely |
| **MEDIUM** | Partial value lost | Works but worse |

---

## INVARIANT INDEX

| ID | Value Protected | Priority |
|----|-----------------|----------|
| V1 | Privacy through topology — content/synthesis never accessed | CRITICAL |
| V2 | Every node gets a valid 3D position — no NaN, within bounds | HIGH |
| V3 | Anatomy layers are correct — types placed in right z-bands | HIGH |
| V4 | Visual properties map accurately — color/size/glow match data | MEDIUM |
| V5 | Standalone HTML renders — no backend dependencies | MEDIUM |

---

## MARKERS

<!-- @mind:todo Write automated test that grep-checks Cypher queries for absence of content/synthesis fields (V1 verification) -->
<!-- @mind:proposition Add V6: Scan reproducibility — same brain state should produce same positions (requires seeded RNG) -->
