# Treatment Protocol -- Sync: Current State

```
LAST_UPDATED: 2026-03-18
UPDATED_BY: @dragon_slayer (doc chain creation)
STATUS: CANONICAL
```

---

## MATURITY

**What's canonical (v1):**
- Full treatment lifecycle: begin_treatment -> (observation window) -> evaluate_treatment
- BrainStats snapshot before and after intervention
- Weighted metric comparison across 10+ metrics with explicit weights
- Auto-rollback on degradation via treatment_id-tagged node deletion
- Auto-prescription by brain category (VOID, MINIMAL, SEEDED, STRUCTURED)
- Treatment records as JSON in `data/treatments/{citizen_id}/`
- Treatment dataclass with full audit fields

**What's still being designed:**
- Metric weights are hardcoded -- no calibration against real treatment outcomes yet
- `score_before` and `score_after` fields exist in the dataclass but are never populated
- No integration test against a live FalkorDB instance with real brain graphs
- Observation window timing is entirely caller-managed with no guidance

**What's proposed (v2+):**
- Partial rollback (requires content awareness -- may conflict with topology-only principle)
- Treatment scheduling (recurring treatments, cooldown periods)
- Cross-citizen treatment efficacy analysis (which catalysts work best for which brain categories)
- Integration with crisis_detection (auto-treat on certain crisis patterns)
- Weight calibration from accumulated treatment records

---

## CURRENT STATE

The treatment protocol is fully implemented in `services/health_assessment/treatment_protocol.py`. The code is complete and structurally sound. It depends on `catalysts.py` (also implemented) and `brain_topology_reader.py` (also implemented).

What exists:
- `begin_treatment()` -- snapshot, prescribe, apply, save
- `evaluate_treatment()` -- snapshot, compare, verdict, rollback if degraded, save
- `list_treatments()` -- list all treatments for a citizen
- Treatment dataclass with full lifecycle fields
- JSON persistence in `data/treatments/`

What has not been done:
- No test against a live FalkorDB instance. The code is correct by inspection but has not been exercised against real brain graphs.
- No unit tests in `tests/`. The treatment protocol needs its own test file.
- The `score_before` and `score_after` fields are unused -- they were reserved for a future aggregate score but no logic populates them.
- No caller currently invokes `begin_treatment` or `evaluate_treatment` in production. The functions exist but are not wired into any runner or scheduler.

---

## IN PROGRESS

### Doc Chain Creation

- **Started:** 2026-03-18
- **By:** @dragon_slayer
- **Status:** Complete -- OBJECTIVES, PATTERNS, ALGORITHM, VALIDATION, SYNC written
- **Context:** First doc chain for the treatment subsystem. Created after code review of treatment_protocol.py and catalysts.py.

---

## RECENT CHANGES

### 2026-03-18: Initial Doc Chain

- **What:** Created full doc chain: OBJECTIVES, PATTERNS, ALGORITHM, VALIDATION, SYNC
- **Why:** The treatment protocol code existed without documentation. The doc chain captures the design rationale (measurability, reversibility, evidence-based care), the algorithm (two-phase lifecycle, weighted comparison, auto-rollback), and the validation invariants (6 invariants, 5 test scenarios).
- **Files:** `docs/care/treatment_protocol/OBJECTIVES_Treatment_Protocol.md`, `PATTERNS_Treatment_Protocol.md`, `ALGORITHM_Treatment_Protocol.md`, `VALIDATION_Treatment_Protocol.md`, `SYNC_Treatment_Protocol.md`

---

## KNOWN ISSUES

### No live FalkorDB test

- **Severity:** high
- **Symptom:** The treatment protocol has not been tested against a running FalkorDB instance with real brain graphs
- **Suspected cause:** FalkorDB infrastructure is not always available in the development environment
- **Next step:** Run `begin_treatment` + `evaluate_treatment` against a test citizen's brain graph and verify snapshot correctness, node creation, and rollback

### Unused score fields

- **Severity:** low
- **Symptom:** `score_before` and `score_after` fields in the Treatment dataclass are always None
- **Suspected cause:** These were reserved for an aggregate score but the evaluation uses the weighted comparison directly, not a single score
- **Next step:** Either populate them with the weighted totals or remove them to avoid confusion

### Rollback failure is silent to the caller

- **Severity:** medium
- **Symptom:** If `rollback_treatment` fails (FalkorDB error), it returns 0 and logs an error, but the Treatment record still shows `rolled_back: true`
- **Suspected cause:** The treatment protocol sets `rolled_back = True` before confirming rollback success
- **Next step:** Check the return value of `rollback_treatment` and set `rolled_back` only if nodes were actually deleted

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** groundwork (for tests and FalkorDB integration) or fixer (for the rollback confirmation bug)

**Where I stopped:** Doc chain is complete. The code is implemented but untested against live infrastructure. Three known issues documented above.

**What you need to understand:**
The treatment protocol is a two-phase process. Phase 1 (`begin_treatment`) is self-contained: snapshot, prescribe, apply, save. Phase 2 (`evaluate_treatment`) is called later by the same or different caller: snapshot, compare, verdict, rollback, save. The observation window between phases is not managed by this module.

The weighted comparison in `evaluate_treatment` is the core decision engine. It compares 11 metrics (10 higher-is-better + frustration inverted) with weights from 1 to 3. Cluster coefficient has the highest weight (3) because it best indicates meaningful brain integration.

**Watch out for:**
- The rollback confirmation bug (INV-3 is partially violated -- `rolled_back` is set before confirming success)
- The `score_before`/`score_after` fields that suggest a single-score system but are never populated
- `evaluate_treatment` can be called multiple times on the same treatment -- it overwrites the previous evaluation

**Open questions:**
- Should there be a cooldown between treatments on the same citizen?
- Should `evaluate_treatment` refuse to run if called too soon after `begin_treatment`?
- What is the recommended observation window for each catalyst type?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Treatment protocol doc chain is complete (5 files). The code in `treatment_protocol.py` implements the full lifecycle: snapshot before, prescribe, apply catalysts, observe, snapshot after, evaluate with weighted metrics, auto-rollback on degradation. Treatment records persist as JSON. The code is implemented but needs a live FalkorDB test to confirm it works end-to-end. Three issues documented: no live test, unused score fields, rollback confirmation bug.

**Decisions already made:**
- All-or-nothing rollback (no partial rollback -- topology-only constraint prevents it)
- Weighted metric comparison with cluster_coefficient at highest weight
- Auto-prescription by brain category
- JSON file persistence per citizen per treatment

**Needs your input:**
- Recommended observation window per catalyst type (hours? days?)
- Whether to populate or remove the unused `score_before`/`score_after` fields
- Priority of the rollback confirmation bug fix

---

## TODO

### Doc/Impl Drift

- [ ] IMPL: Fix rollback confirmation -- check return value before setting `rolled_back = True`

### Immediate

- [ ] Write unit tests for treatment_protocol.py (mock FalkorDB)
- [ ] Run end-to-end test against live FalkorDB with a test citizen
- [ ] Decide on score_before/score_after fields: populate or remove

### Later

- [ ] HEALTH doc -- how to monitor the treatment system itself (failure rates, rollback frequency)
- [ ] IMPLEMENTATION doc -- if the code grows beyond the current two files
- [ ] Weight calibration from real treatment outcomes
- [ ] Treatment cooldown logic to prevent over-treating

---

## POINTERS

| What | Where |
|------|-------|
| Treatment protocol code | `services/health_assessment/treatment_protocol.py` |
| Catalysts module | `services/health_assessment/catalysts.py` |
| Brain topology reader | `services/health_assessment/brain_topology_reader.py` |
| Treatment data storage | `data/treatments/{citizen_id}/{treatment_id}.json` |
| Crisis detection (related care module) | `docs/care/crisis_detection/` |
| Growth guidance (related care module) | `docs/care/growth_guidance/` |
| GraphCare project sync | `docs/SYNC_GraphCare.md` |
