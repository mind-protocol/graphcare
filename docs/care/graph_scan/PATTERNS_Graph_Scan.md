# Graph Scan — Patterns: Two-Stage Pipeline for Graph Visualization

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
THIS:            PATTERNS_Graph_Scan.md (you are here)
ALGORITHM:       ./ALGORITHM_Graph_Scan.md
VALIDATION:      ./VALIDATION_Graph_Scan.md
HEALTH:          ./HEALTH_Graph_Scan.md
IMPLEMENTATION:  ./IMPLEMENTATION_Graph_Scan.md
SYNC:            ./SYNC_Graph_Scan.md

IMPL:            services/graph_scan/brain_data_extractor.py
```

### Bidirectional Contract

**Before modifying this doc or the code:**
1. Read ALL docs in this chain first
2. Read the linked IMPL source file

**After modifying this doc:**
1. Update the IMPL source file to match, OR
2. Add a TODO in SYNC_Graph_Scan.md: "Docs updated, implementation needs: {what}"
3. Run tests: `python services/graph_scan/brain_data_extractor.py dragon_slayer`

**After modifying the code:**
1. Update this doc chain to match, OR
2. Add a TODO in SYNC_Graph_Scan.md: "Implementation changed, docs need: {what}"
3. Run tests: `python services/graph_scan/brain_data_extractor.py dragon_slayer`

---

## THE PROBLEM

Graphs have 220 to 1000+ nodes, each carrying 12+ numeric dimensions. Links carry 13 dimensions. This is impossible to understand as numbers in a terminal. You can run `graph_query` and get text results, but text doesn't show you the shape of a brain — the clusters, the density, the gaps, the tension between regions.

Without visualization, GraphCare operates blind. We can detect anomalies through code, but we can't verify our intuitions, explain our findings to others, or discover unexpected patterns. The graph is the territory; we need the map.

---

## THE PATTERN

**Two-stage pipeline: Extract+Position then Render.**

Stage 1 (extractor): Query FalkorDB for all node/link fields. Compute TF-IDF on node labels. Subtract per-type centroid so types don't cluster. Run UMAP to get 3D coordinates. Compute visual properties from physics fields. Output JSON.

Stage 2 (renderer): Consume JSON (from either L1 or L3 extractor). Generate a standalone HTML file with Three.js. Curved bezier links, matte spheres, organic palette, CSS post-processing for warmth.

The key insight: **centroid subtraction before UMAP** prevents types from forming separate clusters. Without it, UMAP would group all "concept" nodes together, all "desire" nodes together, etc. — hiding the semantic structure that crosses type boundaries. By subtracting each type's centroid from its members, we remove the type signal from the embedding space, letting content similarity drive positioning.

---

## BEHAVIORS SUPPORTED

- B1 (Any graph becomes visualization) — the two-stage pipeline transforms FalkorDB data into interactive HTML
- B2 (Types mix spatially) — centroid subtraction is the mechanism that enables this
- B3 (L1 and L3 use same renderer) — JSON intermediate format decouples extraction from rendering
- B4 (Hover reveals physics) — all fields are preserved in the JSON and rendered in the hover panel

## BEHAVIORS PREVENTED

- A1 (Never read content/synthesis) — extractors query structural fields only, not content or synthesis
- A2 (Never modify the graph) — all queries are read-only MATCH/RETURN
- A3 (Never animate) — renderer produces static geometry, no animation loop beyond orbit controls

---

## PRINCIPLES

### Principle 1: Centroid Subtraction

Subtract the per-type centroid from each node's TF-IDF vector before dimensionality reduction. This removes the type signal from the embedding space, forcing UMAP to position nodes by content similarity rather than type membership. Types should overlap. A "desire" node about music should be near a "concept" node about music, not near a "desire" node about food.

This matters because type-stratified layouts give a false impression of separation. The interesting structure in a brain is the cross-type connections — values connected to desires connected to processes. Spatial mixing reveals this.

### Principle 2: All Curves, No Straight Lines

Every link is rendered as a quadratic bezier curve. The control point offset is derived from link properties (friction, valence, a hash for consistent direction). This creates an organic, brain-like visual quality. Straight lines look mechanical and make dense graphs harder to read (overlapping lines become indistinguishable).

This matters because the visual language should match the subject: neural tissue, not circuit diagrams.

### Principle 3: Matte Materials

All node materials use MeshStandardMaterial with roughness=0.95, metalness=0.0. No specular highlights, no plastic sheen. Glow comes from emissive properties driven by the energy field. The visual should feel like tissue under soft light — warm, organic, slightly desaturated.

This matters because shiny materials distract from the data. The eye should read topology, not surface reflections.

### Principle 4: Link Color From Hierarchy (L3)

At L3, relation_kind is always null — links carry meaning only through their 13 numeric dimensions. Link color is derived from the hierarchy dimension: containment (hierarchy < -0.5) gets sage green, elaboration (hierarchy > 0.5) gets lavender, constructive (positive valence) gets steel blue, destructive (negative valence) gets terracotta. Neutral links get gray.

This matters because without relation_kind labels, the hierarchy dimension is the strongest categorical signal available for visual differentiation.

### Principle 5: Same Renderer for L1 and L3

The HTML renderer consumes JSON regardless of which extractor produced it. Both extractors output the same shape: nodes with id/position/visual properties, links with source/target/visual properties. The renderer doesn't know or care about L1 vs L3 — it just draws what it's given.

This matters because maintaining two renderers would be wasteful duplication. The visual language should be consistent across scales.

---

## DATA

| Source | Type | Purpose / Description |
|--------|------|-----------------------|
| `services/graph_scan/visual_mapping_proposal.yaml` | FILE | Full mapping spec — all 12 node fields and 13 link fields to visual properties (584 lines) |
| FalkorDB `brain_{handle}` | DB | L1 citizen brain graph (source data for brain extractor) |
| FalkorDB `{universe_name}` | DB | L3 universe graph (source data for universe extractor) |
| `data/graph_scans/{name}_scan.json` | FILE | Intermediate JSON output from extractors |
| `data/graph_scans/{name}_brain.html` | FILE | Final L1 visualization |
| `data/graph_scans/{name}_universe.html` | FILE | Final L3 visualization |

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| FalkorDB | Source of all graph data — both L1 and L3 graphs |
| umap-learn | Dimensionality reduction: TF-IDF vectors (200-300D) to 3D coordinates |
| scikit-learn | TfidfVectorizer for converting node labels to vectors |
| Three.js r128 (CDN) | 3D rendering in the browser — loaded from CDN for standalone HTML |
| google-chrome (headless) | Optional: headless screenshot export to PNG |

---

## INSPIRATIONS

Neuroscience brain imaging (fMRI spatial maps). The visual language of connectomics — nodes as soma, links as axons. The insight that brain regions aren't neatly separated but interleaved, with function emerging from connection pattern rather than spatial location.

UMAP as a visualization tool (McInnes et al., 2018) — preserving local structure while allowing global mixing. The centroid subtraction trick is borrowed from the batch correction literature in single-cell RNA-seq (removing batch effects so cell types from different experiments can be compared).

---

## SCOPE

### In Scope

- Extracting all node and link fields from FalkorDB (L1 and L3)
- Computing semantic 3D positions via TF-IDF + centroid subtraction + UMAP
- Mapping physics fields to visual properties (color, radius, glow, opacity, etc.)
- Rendering interactive standalone HTML with Three.js
- Hover-to-inspect for all physics fields
- Legend with type filtering
- Headless screenshot support

### Out of Scope

- Real-time graph updates or streaming → future temporal layer
- Graph editing or mutation through the UI → not a visualization concern
- Content display (reading synthesis or content fields) → see VALIDATION V1
- Comparison between scans (diff view) → future feature
- Embedding-based positioning (768D all-mpnet) → see SYNC, proposed for v2

---

## MARKERS

<!-- @mind:TODO Deduplicate the visual mapping functions between brain_data_extractor.py and universe_data_extractor.py — they share _node_radius, _node_glow, _node_opacity, _link_opacity -->
<!-- @mind:proposition Replace TF-IDF with real embeddings (all-mpnet-base-v2, 768D) for better semantic positioning. TF-IDF is label-only; embeddings would use synthesis content without displaying it. -->
<!-- @mind:proposition Add a diff mode: compare two scans of the same brain taken at different times, highlighting what changed -->
