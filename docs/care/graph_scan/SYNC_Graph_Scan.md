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
- Three.js HTML renderer — curved bezier links, matte materials, organic palette, hover panel, legend filtering
- UMAP semantic positioning with per-type centroid subtraction
- 9 visual layers mapped (node base, affinity, link base, link relational, modality, emotions, metabolism, provenance, consciousness state)

**What's still being designed:**
- L3 universe extractor — just created, mirrors L1 pipeline but adapted for L3 types (actor/moment/narrative/space/thing). Needs testing on a real universe graph.
- Renderer compatibility with L3 JSON — the renderer currently references `citizen_id` which L3 scans don't have (`graph_name` instead)

**What's proposed (v2+):**
- Real embedding positioning — replace TF-IDF (label-only, ~200D) with all-mpnet-base-v2 (768D, uses synthesis without displaying it). Would dramatically improve semantic clustering quality.
- Temporal layer — overlay time-series data onto the static scan (pulse, decay, activation history). Requires animation, which is explicitly out of scope for v1.
- Collaboration with @dev — enrichment via physics_cartographer.py (mind-ops) for deeper physics analysis
- CONTAINS hierarchy for spatial nesting — use the hierarchy link dimension to nest contained nodes inside container nodes (spaces contain things)

---

## CURRENT STATE

Graph Scan has a working L1 pipeline: brain_data_extractor.py queries a citizen's brain from FalkorDB, computes semantic 3D positions via TF-IDF + centroid subtraction + UMAP, maps all 12 node fields and 13 link fields to visual properties, and outputs JSON. render_html.py converts that JSON into a standalone interactive HTML using Three.js r128 from CDN.

The L3 universe extractor (universe_data_extractor.py) was created on 2026-03-18 as a port of the L1 pipeline. It handles the L3 differences: 5 universal types (actor/moment/narrative/space/thing), null relation_kind (link color derived from hierarchy dimension), no self_relevance/partner_relevance, larger scale. It has not yet been tested on a real universe graph.

The visual mapping specification lives in visual_mapping_proposal.yaml (584 lines) and documents all field-to-visual property formulas.

The three source files are intentionally independent (no shared imports) but duplicate visual mapping functions (_node_radius, _node_glow, _node_opacity, _link_opacity). This duplication is tracked as an extraction candidate.

---

## IN PROGRESS

### L3 Universe Extractor Testing

- **Started:** 2026-03-18
- **By:** @dragon_slayer
- **Status:** Just created, needs testing
- **Context:** The extractor mirrors the L1 pipeline but has not been run against a real L3 graph. The Lumina Prime universe graph is the obvious test target. Also need to verify the renderer handles L3 JSON (which has `graph_name` instead of `citizen_id`).

### Doc Chain Creation

- **Started:** 2026-03-18
- **By:** @dragon_slayer
- **Status:** Complete
- **Context:** Full 8-file doc chain created for the care/graph_scan module. Renamed from "brain_scan" to "graph_scan" to reflect the unified L1+L3 scope.

---

## RECENT CHANGES

### 2026-03-18: Renamed brain_scan to graph_scan, added L3 universe extractor

- **What:** Broadened scope from L1-only ("brain scan") to L1+L3 ("graph scan"). Created universe_data_extractor.py for L3 graphs. Created full doc chain.
- **Why:** GraphCare monitors the ecosystem at all levels. L3 universe visualization is needed for ecosystem health audits. The positioning pipeline (TF-IDF + centroid subtraction + UMAP) works identically for both scales, so sharing the pattern reduces maintenance.
- **Files:** `services/graph_scan/universe_data_extractor.py` (new), `docs/care/graph_scan/` (new — 8 files)
- **Struggles/Insights:** The L3 extractor is simpler than L1 because there are fewer fields (no self_relevance, no partner_relevance, no activation_count, no modality, no metabolism). The main L3-specific challenge is link color: relation_kind is always null, so hierarchy and valence become the primary color signals.

---

## KNOWN ISSUES

### Renderer Assumes citizen_id in JSON

- **Severity:** medium
- **Symptom:** render_html.py reads `scan["citizen_id"]` — L3 scans have `graph_name` instead, which would cause a KeyError
- **Suspected cause:** Renderer was written for L1 only, before L3 extractor existed
- **Attempted:** Not yet fixed — the renderer needs a small update to handle both keys

### TF-IDF Is Basic

- **Severity:** low
- **Symptom:** Semantic positioning is based on label text only (TF-IDF on short strings). Nodes with similar names cluster well, but nodes with different names but similar meaning don't.
- **Suspected cause:** By design — TF-IDF was the simplest approach. Real embeddings (all-mpnet-base-v2, 768D) would be much better but require embedding infrastructure.
- **Attempted:** Noted as v2 proposal. Not blocking current functionality.

### Visual Mapping Function Duplication

- **Severity:** low
- **Symptom:** `_node_radius`, `_node_glow`, `_node_opacity`, `_link_opacity` are duplicated between brain_data_extractor.py and universe_data_extractor.py
- **Suspected cause:** Files were made intentionally independent for simplicity
- **Attempted:** Tracked as extraction candidate in IMPLEMENTATION doc

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Extend (add L3 testing, fix renderer compatibility)

**Where I stopped:** Doc chain complete. L3 extractor written but untested. Renderer needs a small patch for L3 JSON compatibility.

**What you need to understand:**
The two extractors are intentionally independent files with no shared imports. This was a simplicity choice, not a design principle. If you're adding features to both, consider extracting shared functions first (see IMPLEMENTATION extraction candidates). The renderer is source-agnostic in theory but has a `citizen_id` hard-reference that needs fixing for L3.

**Watch out for:**
- The renderer embeds JavaScript template literals inside Python f-strings. Double-brace escaping is everywhere. Editing the HTML template is error-prone — test in a browser after any change.
- UMAP with random_state=42 is deterministic. If you change any input (TF-IDF features, centroid subtraction, normalization), positions will shift for ALL nodes, not just the affected ones. This is expected but can be surprising.

**Open questions I had:**
- Should the renderer auto-detect L1 vs L3 from the JSON? Or should there be explicit flags?
- Should we use CONTAINS hierarchy in L3 to spatially nest contained nodes inside container nodes?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Graph Scan now covers both L1 (citizen brain) and L3 (universe) visualization. L1 pipeline is working and tested. L3 extractor is written but untested. Full doc chain created (8 files). Renderer needs a small fix for L3 JSON compatibility.

**Decisions made:**
- Unified name "Graph Scan" instead of "Brain Scan" to reflect L1+L3 scope
- Same pipeline pattern for both scales (TF-IDF + centroid subtraction + UMAP)
- L3 link color derived from hierarchy dimension (since relation_kind is null)
- Kept files independent (no shared imports) for now — duplication tracked

**Needs your input:**
- Priority: should L3 testing or Evidence Sprint prep come first?
- v2 embedding positioning: should we invest in all-mpnet integration, or is TF-IDF sufficient for current diagnostic needs?

---

## TODO

### Doc/Impl Drift

- [ ] DOCS->IMPL: Renderer needs update to handle both `citizen_id` and `graph_name` from JSON
- [ ] IMPL->DOCS: If visual mapping functions are extracted to shared module, update IMPLEMENTATION doc

### Tests to Run

```bash
# L1 extraction (requires FalkorDB with a brain graph)
python services/graph_scan/brain_data_extractor.py dragon_slayer

# L3 extraction (requires FalkorDB with a universe graph)
python services/graph_scan/universe_data_extractor.py lumina_prime

# Rendering
python services/graph_scan/render_html.py dragon_slayer
```

### Immediate

- [ ] Test L3 extractor on a real universe graph
- [ ] Fix renderer to handle both citizen_id and graph_name
- [ ] Extract shared visual mapping functions to deduplicate

### Later

- [ ] Real embedding positioning (all-mpnet-base-v2 instead of TF-IDF)
- [ ] CONTAINS hierarchy spatial nesting for L3
- [ ] Temporal layer (animation overlay)
- [ ] Link hover info (currently only node hover works)
- IDEA: Diff mode — compare two scans of the same brain at different times

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
Confident about the doc chain — it accurately reflects the code. The L1 pipeline works well. Slightly uncertain about L3 because it hasn't been tested on real data yet, but the code is a straightforward port of L1.

**Threads I was holding:**
- The renderer citizen_id vs graph_name issue is small but will break L3 rendering until fixed
- The duplication between extractors is manageable now but will compound if more features are added to both
- TF-IDF positioning works surprisingly well for labels, but labels are short — real embeddings would be a significant quality jump

**Intuitions:**
- The CONTAINS hierarchy could be powerful for L3 — spatially nesting "thing" nodes inside "space" nodes would reveal organizational structure
- The renderer is the bottleneck for future features — it's a single HTML template with JS embedded in Python f-strings. Consider generating JS separately.

**What I wish I'd known at the start:**
The centroid subtraction trick is the single most important design decision. Without it, every visualization I tried showed types in separate blobs. With it, the brain looks like a brain — interwoven, dense, organic.

---

## POINTERS

| What | Where |
|------|-------|
| L1 brain extractor | `services/graph_scan/brain_data_extractor.py` |
| L3 universe extractor | `services/graph_scan/universe_data_extractor.py` |
| HTML renderer | `services/graph_scan/render_html.py` |
| Visual mapping spec | `services/graph_scan/visual_mapping_proposal.yaml` |
| Scan output directory | `data/graph_scans/` |
| Doc chain | `docs/care/graph_scan/` |

<!-- @mind:TODO Test L3 universe extractor on a real graph (lumina_prime) and fix renderer citizen_id/graph_name compatibility -->
