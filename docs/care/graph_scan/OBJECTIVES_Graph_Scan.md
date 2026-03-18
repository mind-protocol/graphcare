# OBJECTIVES — Graph Scan

```
STATUS: DESIGNING
CREATED: 2026-03-18
VERIFIED: —
```

---

## CHAIN

```
THIS:            OBJECTIVES_Graph_Scan.md (you are here - START HERE)
PATTERNS:       ./PATTERNS_Graph_Scan.md
BEHAVIORS:      ./BEHAVIORS_Graph_Scan.md
ALGORITHM:      ./ALGORITHM_Graph_Scan.md
VALIDATION:     ./VALIDATION_Graph_Scan.md
IMPLEMENTATION: ./IMPLEMENTATION_Graph_Scan.md
HEALTH:         ./HEALTH_Graph_Scan.md
SYNC:           ./SYNC_Graph_Scan.md

IMPL:           services/graph_scan/brain_data_extractor.py
```

**Read this chain in order before making changes.** Each doc answers different questions. Skipping ahead means missing context.

---

## PRIMARY OBJECTIVES (ranked)

1. **O1: Make graph state visible** — Turn any graph (L1 citizen brain or L3 universe) into an intuitive 3D visualization. A graph you can't see is a graph you can't reason about. GraphCare diagnoses through topology; this is the diagnostic imaging layer.

2. **O2: Semantic topology** — Nodes positioned by content similarity (TF-IDF + UMAP), NOT by type. Types should mix spatially. The insight is that semantically related nodes from different types cluster together — revealing cross-type structure that type-stratified layouts hide.

3. **O3: All dimensions visible** — Every numeric field from the mind schema mapped to a distinct visual property. 12 node fields, 13 link fields. Nothing invisible. If the physics engine computes it, the scan shows it.

4. **O4: Pre-computed, static** — Generate offline, explore interactively. No animation, no real-time streaming. The temporal layer is a future concern. Static visualization is deterministic, reproducible, and cheap.

5. **O5: Works at both scales** — L1 citizen brains (~220 nodes) and L3 universe graphs (1000+ nodes) use the same positioning pipeline and the same renderer. Two extractors, one renderer.

## NON-OBJECTIVES

- Real-time streaming of graph changes
- Force-directed layout (non-deterministic, expensive, not reproducible)
- Showing text content or synthesis (topology-only — GraphCare reads structure, never content)
- Animation, pulsing, or temporal effects (future layer)
- Editing the graph through the visualization

## TRADEOFFS (canonical decisions)

- When semantic topology conflicts with type stratification, choose semantic topology. Types mix. That's the point.
- When visual clarity conflicts with completeness, choose visual clarity. Some fields may need subtler mappings to avoid clutter.
- When static reproducibility conflicts with live updates, choose static. Generate once, explore many times.
- We accept the cost of TF-IDF (basic text similarity) to preserve the centroid subtraction pattern. Real embeddings (768D all-mpnet) would be better, but TF-IDF works now.

## SUCCESS SIGNALS (observable)

- A 220-node brain produces a navigable 3D HTML in under 10 seconds
- Types are visually interspersed, not clustered into separate regions
- Hovering any node reveals all its physics fields
- Same HTML renderer works for both L1 and L3 JSON
- Screenshots via headless Chrome produce clean PNGs

<!-- @mind:TODO Validate that centroid subtraction actually prevents type clustering on real brains with >100 nodes -->
