# Brain Scan — Sync: Current State

```
LAST_UPDATED: 2026-03-18
UPDATED_BY: @dragon_slayer
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- Data extraction pipeline: FalkorDB query -> BrainScan dataclass -> JSON
- Golden angle spiral positioning within anatomy z-bands
- Visual property mapping (color from type, size from weight, glow from energy)
- HTML renderer with Three.js: OrbitControls, layer toggles, type filters, hover info
- Three data structures: ScanNode, ScanLink, BrainScan

**What's still being designed:**
- Semantic positioning via UMAP on node embeddings (alternative to anatomy-only layout)
- Temporal animation (showing brain evolution over time)
- Collaboration with @dev's physics_cartographer.py from mind-ops for enriched positioning data
- Health checks runtime (services/brain_scan/health_checks.py — specified in HEALTH doc, not yet implemented)

**What's proposed (v2+):**
- Query-based filtering ("show me the governance cluster", "highlight desires connected to values")
- Video export / animation recording of brain rotation
- physics_cartographer integration for gravity-based layout
- Dual-scan comparison mode (before/after, two citizens side by side)
- LOD (Level of Detail) for brains with >1000 nodes

---

## CURRENT STATE

The brain scan module exists as a working two-stage pipeline. Stage 1 (`brain_scan_data_extractor.py`, ~260 lines) connects to FalkorDB, extracts all nodes and links from a citizen's brain graph, positions them in anatomy-based z-layers using a golden angle spiral, maps visual properties from data fields, and outputs a BrainScan dataclass that can be serialized to JSON. Stage 2 (`render_brain_scan_html.py`, ~248 lines) loads the JSON and generates a standalone HTML file with Three.js 3D rendering, complete with OrbitControls, layer toggles, type legend filters, and node hover tooltips.

The pipeline is topology-only by design — Cypher queries never access content or synthesis fields. This aligns with GraphCare's kidney metaphor.

Both files are healthy sizes (under 400 lines each). The code is clean, well-commented, and follows dataclass patterns. No tests exist yet.

---

## IN PROGRESS

### Doc Chain Creation

- **Started:** 2026-03-18
- **By:** @dragon_slayer
- **Status:** Complete
- **Context:** Full 8-file doc chain created from templates. The code existed first, docs were written to match the existing implementation. All docs are at STATUS: DESIGNING.

---

## RECENT CHANGES

### 2026-03-18: Prototype Created

- **What:** Initial implementation of brain_scan_data_extractor.py and render_brain_scan_html.py, plus complete doc chain
- **Why:** GraphCare needs to visualize brain topology to make health scores actionable. A score of 23/100 is meaningless without seeing the structural reasons. The brain scan is the bridge between data and understanding.
- **Files:** `services/brain_scan/brain_scan_data_extractor.py`, `services/brain_scan/render_brain_scan_html.py`, `docs/care/brain_scan/` (8 files)
- **Struggles/Insights:** The golden angle spiral produces surprisingly good visual results for something so simple. The anatomy metaphor (stem/limbic/cortex) maps naturally to bottom-to-top vertical layout. The z/y swap in Three.js (mesh.position.set(n.x, n.z, n.y)) is easy to forget but critical for correct vertical orientation.

---

## KNOWN ISSUES

### FalkorDB Data Loss on Restart

- **Severity:** high
- **Symptom:** Brain graphs may be empty after FalkorDB restarts
- **Suspected cause:** FalkorDB persistence configuration — known infra issue, not a brain scan bug
- **Attempted:** Not a brain scan concern — tracked at infrastructure level

### No Tests

- **Severity:** medium
- **Symptom:** No automated verification that the pipeline works correctly
- **Suspected cause:** Prototype stage — tests not yet written
- **Attempted:** Doc chain created with clear validation invariants (V1-V5) to guide test creation

### Random Jitter Not Seeded

- **Severity:** low
- **Symptom:** Same brain graph produces slightly different positions each time due to `random.gauss()` jitter
- **Suspected cause:** By design for organic feel, but prevents exact reproducibility
- **Attempted:** Not addressed yet — decision needed on whether to seed

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Extend (add semantic positioning, @dev collab, or tests) or VIEW_Debug (if scans fail)

**Where I stopped:** Doc chain complete. Code is working prototype. No tests, no health checks runtime.

**What you need to understand:**
The pipeline is intentionally simple — two files, two stages, one intermediate format (JSON). The complexity is in the positioning algorithm (golden angle spiral within anatomy z-bands) and the visual property mappings. Both are well-documented in ALGORITHM_Brain_Scan.md. The Three.js rendering is a single f-string template — no template engine, no build step.

**Watch out for:**
- The z/y axis swap in render_html: `mesh.position.set(n.x, n.z, n.y)` — Three.js uses y-up, our data uses z-up
- FalkorDB checks both `n.type` and `n.node_type` because the field name varies by backend config
- The Gaussian jitter means positions are not reproducible between runs (see known issue)
- NODE_COLORS and LINK_COLORS are duplicated conceptually in the HTML template — the Python dicts generate JSON that's embedded in the HTML

**Open questions I had:**
- Should the golden angle spiral be seeded for reproducibility, or is the organic randomness desirable?
- Should LAYER_Z handle `stimulus` and `frequency` types explicitly, or is the default band sufficient?
- How will this integrate with @dev's physics_cartographer once it exists?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Brain scan module is a working prototype — two Python files that extract brain topology from FalkorDB and render it as an interactive 3D HTML visualization. Full 8-file doc chain is created. No tests yet. The pipeline is topology-only (never reads content fields), pre-computed (no live DB access from the browser), and produces standalone HTML files.

**Decisions made:**
- Anatomy metaphor (stem/limbic/cortex) for vertical layering — brain regions map to semantic types
- Golden angle spiral for within-layer positioning — organic, non-grid distribution
- CDN Three.js (not bundled) — standalone HTML, no build step, requires internet to view
- No content access — Cypher queries explicitly exclude content and synthesis fields

**Needs your input:**
- Should golden angle jitter be seeded for reproducibility?
- Priority of @dev collaboration on physics_cartographer integration
- When to invest in tests vs continue prototyping new features

---

## TODO

### Doc/Impl Drift

- [ ] IMPL->DOCS: Update DOCS comment in brain_scan_data_extractor.py line 4 (currently says "to be created", docs now exist)

### Tests to Run

```bash
# No tests exist yet
python -m pytest tests/care/brain_scan/ -v  # (to be created)
```

### Immediate

- [ ] Write unit tests for extract_brain_scan() with mocked FalkorDB
- [ ] Write unit test verifying Cypher queries contain no content/synthesis fields (V1)
- [ ] Implement health_checks.py with falkordb_connectivity, scan_completeness, position_validity

### Later

- [ ] Investigate UMAP-based semantic positioning as alternative layout mode
- [ ] Explore @dev's physics_cartographer.py for enriched data collaboration
- IDEA: Dual-scan comparison view to show brain evolution over time
- IDEA: Query-based highlighting ("show governance cluster") using graph traversal

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
Confident about the pipeline design. The two-stage pattern is clean and the code is straightforward. The doc chain captures the full reasoning. The main uncertainty is around future directions — semantic positioning, @dev collaboration, and test priorities.

**Threads I was holding:**
- The kidney metaphor is fundamental — topology only, never content. This must be defended in every future change.
- FalkorDB instability is a real constraint that affects brain scan reliability. Health checks are specified but not yet implemented.
- The golden angle spiral is elegant for small brains but may need LOD for large ones (>1000 nodes).

**Intuitions:**
- The UMAP-based semantic layout will be more informative than anatomy-only, but it requires embeddings that may not exist yet for all nodes.
- The brain scan could become the primary debugging interface for GraphCare health assessments — "show me why this score is low."
- Video export would be valuable for reports and presentations, but it's a rabbit hole — defer it.

**What I wish I'd known at the start:**
The Three.js z/y axis convention. Spent time confused about why anatomy layers were horizontal instead of vertical until realizing the coordinate swap was needed.

---

## POINTERS

| What | Where |
|------|-------|
| Stage 1: Data Extraction | `services/brain_scan/brain_scan_data_extractor.py` |
| Stage 2: HTML Renderer | `services/brain_scan/render_brain_scan_html.py` |
| Output: Scan JSON | `data/brain_scans/{handle}_scan.json` |
| Output: Brain HTML | `data/brain_scans/{handle}_brain.html` |
| Doc Chain | `docs/care/brain_scan/` (this directory) |
| Health Checks (to be created) | `services/brain_scan/health_checks.py` |
| FalkorDB brain graphs | FalkorDB `brain_{handle}` |
| @dev's physics_cartographer | `mind-ops` repo (external) |
