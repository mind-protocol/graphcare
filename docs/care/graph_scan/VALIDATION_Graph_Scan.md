# Graph Scan — Validation: What Must Be True

```
STATUS: DESIGNING
CREATED: 2026-03-18
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Graph_Scan.md
PATTERNS:        ./PATTERNS_Graph_Scan.md
BEHAVIORS:       ./BEHAVIORS_Graph_Scan.md
THIS:            VALIDATION_Graph_Scan.md (you are here)
ALGORITHM:       ./ALGORITHM_Graph_Scan.md (HOW — mechanisms go here)
IMPLEMENTATION:  ./IMPLEMENTATION_Graph_Scan.md
HEALTH:          ./HEALTH_Graph_Scan.md
SYNC:            ./SYNC_Graph_Scan.md
```

---

## PURPOSE

**Validation = what we care about being true.**

Not mechanisms. Not test paths. Not how things work.

What properties, if violated, would mean Graph Scan has failed its purpose?

These invariants protect the core promises: topology-only observation, spatial mixing across types, valid 3D output, and scale-agnostic rendering.

---

## INVARIANTS

### V1: Topology-Only — Content Never Exposed

**Why we care:** GraphCare's fundamental contract is that it reads structure, never content. If content or synthesis text appears anywhere in the scan output or HTML, the privacy boundary is violated. This is the kidney metaphor — we monitor the filter, we don't read what passes through it.

```
MUST:   Node content and synthesis fields are NEVER queried from FalkorDB
MUST:   The output JSON contains no content or synthesis text
MUST:   The rendered HTML displays only structural fields (type, label, physics numbers)
NEVER:  content or synthesis fields appear in any Cypher RETURN clause
NEVER:  Content text is embedded in the HTML or JSON output
```

### V2: Types Mix Spatially

**Why we care:** If types cluster into separate spatial regions, the visualization gives a false impression of separation. The whole point of centroid subtraction is to force types to overlap, revealing cross-type semantic structure. If this fails, we're showing a category diagram, not a topology.

```
MUST:   After centroid subtraction + UMAP, nodes of different types are spatially interspersed
MUST:   No single type occupies a spatially contiguous region disjoint from other types
NEVER:  Types form visually distinct, separated clusters (beyond what content similarity dictates)
```

### V3: Valid 3D Positions

**Why we care:** NaN or unbounded positions would crash the renderer or produce invisible/offscreen nodes. Every node must have finite, bounded coordinates for the visualization to be navigable.

```
MUST:   All node positions (x, y, z) are finite floats
MUST:   Positions are bounded approximately within [-1, 1] after normalization and center pull
NEVER:  NaN, Infinity, or None appears in any position field
NEVER:  Positions exceed [-2, 2] in any dimension (would be offscreen)
```

### V4: L1 and L3 Produce Compatible JSON

**Why we care:** The architecture depends on one renderer consuming output from two extractors. If the JSON formats diverge, the renderer breaks or silently produces wrong output. The contract is: both extractors produce JSON with nodes[{id, x, y, z, color, radius, ...}] and links[{source, target, color, opacity, ...}].

```
MUST:   Both extractors produce JSON with nodes[] and links[] arrays
MUST:   Each node has at minimum: id, node_type, label, x, y, z, color, radius, opacity
MUST:   Each link has at minimum: source, target, color, opacity
MUST:   The renderer produces valid HTML from either extractor's output
NEVER:  The renderer crashes or produces empty scene from valid extractor output
```

### V5: Visual Properties Reflect Physics Accurately

**Why we care:** If the mapping from physics fields to visual properties is wrong (e.g., high energy shows as no glow, or high weight shows as tiny radius), the visualization lies about the graph state. Diagnostic decisions based on the visualization would be wrong.

```
MUST:   Node radius increases monotonically with weight
MUST:   Node glow increases monotonically with energy (above threshold 0.1)
MUST:   Node opacity increases monotonically with stability
MUST:   Link opacity increases monotonically with trust
NEVER:  A high-energy node appears without glow
NEVER:  A high-weight node appears smaller than a low-weight node
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
| V1 | Privacy: topology-only, content never exposed | CRITICAL |
| V2 | Semantic topology: types mix spatially | HIGH |
| V3 | Rendering integrity: valid 3D positions | HIGH |
| V4 | Scale-agnostic: L1/L3 JSON compatible with one renderer | MEDIUM |
| V5 | Diagnostic accuracy: visual properties reflect physics | MEDIUM |

---

## MARKERS

<!-- @mind:TODO Write automated test for V1 — grep extractor Cypher queries to confirm content/synthesis never in RETURN clause -->
<!-- @mind:TODO Write test for V3 — run extractor on a real brain, assert no NaN/Infinity in positions -->
<!-- @mind:proposition V2 is hard to test automatically (requires spatial statistics). Consider measuring type-conditional nearest-neighbor distances. -->
