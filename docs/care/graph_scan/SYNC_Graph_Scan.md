# Graph Scan — Sync: Current State

```
LAST_UPDATED: 2026-03-18
UPDATED_BY: @dragon_slayer
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- L1 brain extractor — full pipeline: FalkorDB query, TF-IDF, centroid subtraction, UMAP 3D, visual property computation, JSON output
- L3 universe extractor — handles 40K+ nodes via top-N sampling by weight+energy, hash-based positioning
- Three.js HTML renderer — curved bezier links, matte materials, organic palette, hover, legend filtering
- Unified renderer: auto-detects L1 (citizen_id) vs L3 (graph_name) from JSON
- 9 visual layers mapped in visual_mapping_proposal.yaml (584 lines)
- Renamed brain_scan → graph_scan (covers both L1 and L3)

**What's still being designed:**
- L3 particle system for 40K+ nodes — THREE.Points instead of Mesh (handoff to @pixel)
- Semantic topology on L3 (hash positioning is uniform, not semantic)
- Fog/camera calibration for different graph sizes

**What's proposed (v2+):**
- Real embedding positioning (768D all-mpnet instead of TF-IDF)
- Temporal layer (animation overlay on static scan)
- @dev collab via physics_cartographer.py (mind-ops)
- CONTAINS hierarchy for spatial nesting

---

## CURRENT STATE

L1 brain scan works end-to-end. Tested on dragon_slayer (220 nodes, 457 links). Semantic UMAP positioning with centroid subtraction produces mixed-type clusters.

L3 universe scan extracts from FalkorDB (lumina-prime: 45,636 nodes → sampled 2000). Renders HTML but headless Chrome doesn't capture WebGL for large graphs — needs real browser testing.

Graph scan renamed from brain_scan. All code in `services/graph_scan/`, docs in `docs/care/graph_scan/`, data in `data/graph_scans/`. Showcase copies in `showcase/assets/graph-scans/`.

@pixel handoff sent for L3 40K+ particle system implementation.

---

## RECENT CHANGES

### 2026-03-18: Full session — brain scan to graph scan

- Created L1 brain scan prototype (golden angle positioning)
- Created visual_mapping_proposal.yaml (584 lines, 9 layers, all L1/L3 fields)
- Implemented semantic UMAP positioning (TF-IDF + centroid subtraction)
- Iterated visual rendering (v1→v4: matte materials, organic palette, curves, no fog)
- Ported to L3 (universe_data_extractor.py, top-N sampling for 40K+ graphs)
- Renamed brain_scan → graph_scan
- Created full doc chain (8 files from templates)
- Handoff to @pixel for L3 particle system
- Verified: headless Chrome captures L1 scans, L3 needs real browser
- Files: services/graph_scan/ (5 files), docs/care/graph_scan/ (8 files), data/graph_scans/

---

## KNOWN ISSUES

### Headless Chrome WebGL
- **Severity:** medium
- **Symptom:** Chrome headless produces black screenshots for L3 (40K+ node) HTMLs
- **Suspected cause:** WebGL rendering timeout or GPU unavailability in WSL headless
- **Workaround:** Open HTML in real Windows browser

### TF-IDF quality
- **Severity:** low
- **Symptom:** Semantic clusters are basic — label text only, not real content embeddings
- **Suspected cause:** TF-IDF on short labels doesn't capture deep semantics
- **Fix:** Use all-mpnet-base-v2 embeddings when available in FalkorDB

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Extend

**Where I stopped:** L3 particle system spec written, handoff to @pixel. L1 scan works. L3 scan extracts but renderer needs particle system for 40K+ nodes.

**What you need to understand:**
- The renderer (render_html.py) generates standalone HTML with inline Three.js. No build step.
- L1 uses UMAP for positioning (TF-IDF + centroid subtraction). L3 uses hash-based positioning (too many nodes for UMAP).
- The visual_mapping_proposal.yaml is the source of truth for data→visual mapping.

**Watch out for:**
- FalkorDB loses data on restart (no persistence configured)
- The `type` field in FalkorDB was empty until the checkpointer fix (line 169)
- L3 graphs have different properties than L1 (no self_relevance, relation_kind always null)

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Graph scan works for L1 (citizen brains, ~220 nodes). L3 (universe, 45K+ nodes) extracts and renders but needs a particle system (THREE.Points) for performance. Handoff to @pixel for L3 rendering. Visual mapping covers all 23 numeric fields across 9 layers.

**Decisions made:**
- Renamed brain_scan → graph_scan (covers both L1 and L3)
- UMAP semantic positioning with per-type centroid subtraction (prevents type clustering)
- No animation in v1 (static only, temporal layer later)
- L3 uses top-N sampling by weight+energy (default 2000 of 40K+)

**Needs your input:**
- @pixel availability for L3 particle system
- Whether to invest in real embedding positioning (needs all-mpnet in FalkorDB)

---

## TODO

### Immediate
- [ ] @pixel: L3 particle system (THREE.Points for 40K+ nodes)
- [ ] Test L3 HTML in real Windows browser
- [ ] Verify visual mapping accuracy on a reseeded L1 brain

### Later
- [ ] Real embedding positioning (768D all-mpnet)
- [ ] CONTAINS hierarchy for spatial nesting
- [ ] Temporal animation layer
- [ ] @dev collab (physics_cartographer enrichment)

---

## POINTERS

| What | Where |
|------|-------|
| L1 extractor | `services/graph_scan/brain_data_extractor.py` |
| L3 extractor | `services/graph_scan/universe_data_extractor.py` |
| Renderer | `services/graph_scan/render_html.py` |
| Visual mapping | `services/graph_scan/visual_mapping_proposal.yaml` |
| Usage guide | `services/graph_scan/README.md` |
| Doc chain | `docs/care/graph_scan/` (8 files) |
| Showcase | `showcase/assets/graph-scans/` |
| @nervo physics mapping | `mind-mcp/runtime/cognition/physics_visual_mapping.py` |
| @dev cartographer | `mind-ops/detection/observability/physics_cartographer.py` |
