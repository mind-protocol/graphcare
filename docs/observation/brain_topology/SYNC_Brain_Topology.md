# Brain Topology — Sync: Current State

```
LAST_UPDATED: 2026-03-15
UPDATED_BY: @vox (doc chain creation)
STATUS: CANONICAL
```

---

## MATURITY

**What's canonical (v1):**
- The 7 primitives: count, mean_energy, link_count, min_links, cluster_coefficient, drive, recency
- The `BrainStats` dataclass with all fields
- The `read_brain_topology(handle)` entry point
- Topology-only guarantee — no content field references in any Cypher query
- `reachable=False` for unreachable brains
- Implementation in `services/health_assessment/brain_topology_reader.py`

**What's still being designed:**
- Cluster coefficient accuracy — current approximation (actual/possible ratio) may need validation against standard local clustering
- Whether `drive()` should support additional storage patterns beyond limbic_state node and separate drive nodes

**What's proposed (v2+):**
- 8th primitive: `degree_distribution(type)` for detecting skewed connectivity patterns
- Per-primitive caching to reduce FalkorDB round-trips when multiple scoring formulas read the same citizen
- Batch reading: `read_brain_topologies(handles: list)` for efficient scanning of all citizens

---

## CURRENT STATE

The brain topology reader is fully implemented and operational. All 7 primitives are coded as individual functions with clear Cypher queries. The `read_brain_topology(handle)` function composes them into a `BrainStats` dataclass that downstream scoring formulas consume.

The code has been stable — it is used by `daily_check_runner.py` to feed the continuous health assessment pipeline. Tests exist in `tests/test_health_assessment.py` (45 tests passing, covering the reader among other modules).

The doc chain (OBJECTIVES, PATTERNS, BEHAVIORS, SYNC) was created on 2026-03-15 to formalize what the code already implements. No code changes were needed — the docs describe reality.

---

## RECENT CHANGES

### 2026-03-15: Doc Chain Created

- **What:** Created OBJECTIVES, PATTERNS, BEHAVIORS, SYNC for brain_topology module
- **Why:** Formalizing existing code into the GraphCare doc chain structure so other teams (scoring, research, privacy) have a canonical reference for what the 7 primitives are and how they work
- **Files:** `docs/observation/brain_topology/` (4 files)
- **Struggles/Insights:** The code was clean and well-documented already. The main insight was articulating the "blood test, not psychoanalysis" metaphor as a formal principle — it captures the privacy guarantee in a way that's immediately graspable.

---

## KNOWN ISSUES

### Cluster Coefficient Approximation

- **Severity:** low
- **Symptom:** The cluster_coefficient uses a global density ratio (actual links / possible links among same-type nodes) rather than the standard local clustering coefficient (average over each node's neighbor connectivity)
- **Suspected cause:** Intentional design choice for simplicity, but the accuracy difference hasn't been measured
- **Attempted:** Nothing yet — this is a known simplification, not a bug

### Drive Storage Pattern Assumptions

- **Severity:** low
- **Symptom:** `drive()` checks for a `limbic_state` node first, then falls back to separate `drive` nodes. If the brain schema evolves, this dual lookup may need updating.
- **Suspected cause:** Different brain graph versions may store drives differently
- **Attempted:** Current fallback pattern handles known variants

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Extend (adding primitives) or VIEW_Debug (primitive returning unexpected values)

**Where I stopped:** Doc chain complete. Code is stable. No pending changes.

**What you need to understand:**
The 7 primitives are the API contract. If you need a new signal from the brain graph, the first question is: can it be composed from existing primitives in a scoring formula? Only if the answer is definitively "no" should you consider adding an 8th primitive — and that requires updating this entire doc chain.

**Watch out for:**
- Never add a Cypher query that returns `n.content` or `n.synthesis`. The topology-only guarantee is structural.
- The `reachable=False` path is important. Don't add new fields to BrainStats that would have misleading defaults when the brain is unreachable.
- `_safe_query` swallows exceptions and returns empty lists. Individual primitive failures are logged as warnings, not errors. Only total connection failure raises to the `read_brain_topology` level.

**Open questions I had:**
- Should `cluster_coefficient("all")` really use the entire graph? Or should it be computed per-type and then aggregated? The current implementation matches the `BrainStats` field, but per-type clustering might reveal more.

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Brain topology reader is implemented and documented. 7 primitives (count, mean_energy, link_count, min_links, cluster_coefficient, drive, recency) read structural properties from citizen brain graphs without ever accessing content. Code is in `services/health_assessment/brain_topology_reader.py`, tests pass, doc chain is complete.

**Decisions made:**
- Kept the approximated cluster coefficient (global ratio) over standard local clustering — simpler, good enough for health scoring
- Documented the topology-only principle as a structural guarantee, not a policy — the code literally cannot return content through these 7 functions

**Needs your input:**
- None currently. The module is stable.

---

## TODO

### Doc/Impl Drift

No drift — docs were written to match existing implementation.

### Tests to Run

```bash
pytest tests/test_health_assessment.py -v
```

### Immediate

- [ ] Validate cluster_coefficient approximation accuracy on a real citizen brain graph
- [ ] Confirm drive() handles all known brain graph schema variants

### Later

- [ ] Consider batch reading for efficiency during full-population scans
- IDEA: degree_distribution primitive for detecting power-law vs uniform connectivity

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
Confident. The code was already clean and well-structured. Documenting it felt like describing something that was already understood — the hardest part was choosing which details to elevate to principle level versus leaving as implementation detail.

**Threads I was holding:**
- The relationship between brain_topology and the dual encryption model in privacy/key_infrastructure — this module assumes it can read topology but not content. The key infrastructure is what makes that structurally true.
- Whether the 7 primitives are sufficient for all 104 Personhood Ladder capabilities, or whether some capabilities will eventually require an 8th.

**Intuitions:**
- The 7 primitives feel right. They're small enough to understand, rich enough to score from. The pressure to add more will come from scoring formulas that want richer signals, but the right response is usually to compose, not to extend.

---

## POINTERS

| What | Where |
|------|-------|
| Implementation | `services/health_assessment/brain_topology_reader.py` |
| Scoring formulas that consume BrainStats | `services/health_assessment/scoring_formulas/` |
| How primitives feed into the algorithm | `docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md` |
| Universe graph observables (the other input) | `docs/assessment/PRIMITIVES_Universe_Graph.md` |
| Tests | `tests/test_health_assessment.py` |
