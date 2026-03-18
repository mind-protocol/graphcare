# Validation Methodology — Sync: Current State

```
LAST_UPDATED: 2026-03-15
UPDATED_BY: @vox (doc chain creation)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- 5 synthetic test profiles implemented and passing in `test_health_assessment.py`
- 45 tests covering: registry sanity, profile aggregates, formula-specific tests, aggregator delta, intervention composition, stress stimulus bounds
- All 41+ scoring formulas pass all synthetic profile tests
- CapabilityScore clamping ensures brain [0,40], behavior [0,60], total = sum

**What's still being designed:**
- Real-world calibration methodology (study design, outcome measures, observation periods)
- Per-capability expected ranges per profile (currently only aggregate is range-checked)
- Formal test gate for new formula merges (currently enforced by convention)

**What's proposed (v2+):**
- 6th synthetic profile: "recovering" citizen (was unhealthy, now improving)
- Automated regression detection: formula changes that degrade any profile's score trigger alerts
- Real-world calibration dashboard showing score-to-outcome correlations over time

---

## CURRENT STATE

The validation methodology is partially implemented and largely effective. The test suite in `test_health_assessment.py` is comprehensive: 45 tests across 9 test classes cover registry sanity, all 5 synthetic profiles, targeted formula tests (world presence, mentorship), aggregator delta computation, intervention message composition, stress stimulus bounds, and CapabilityScore clamping.

The 5 synthetic profiles work well. They catch gross miscalibrations: the fully healthy citizen scores 85-100, the fully unhealthy citizen scores 0-20, and the three intermediate profiles fall in their expected ranges. The brain-behavior split is validated: active-but-brain-poor (profile D, 45-65) scores higher than brain-rich-but-inactive (profile C, 25-45), confirming that behavior weighs more than brain structure.

What's missing: real-world calibration. All current validation is synthetic — we know the scores are internally consistent and produce sensible ranges, but we haven't yet verified that a score of 45 actually predicts observable health problems. This is the next major step.

---

## IN PROGRESS

### Doc chain creation
- **Started:** 2026-03-15
- **By:** @vox
- **Status:** Complete
- **Context:** Formalizing the validation methodology that already exists in code (test_health_assessment.py) into proper documentation. The tests existed before the docs — this is bottom-up documentation from working code.

---

## RECENT CHANGES

### 2026-03-15: Doc chain created

- **What:** Created full doc chain (OBJECTIVES, PATTERNS, VALIDATION, SYNC)
- **Why:** The test suite is the most mature code in GraphCare but lacked its own documentation. Other agents creating new formulas need to understand the validation methodology to write good tests.
- **Files:** `docs/scientific_rigor/validation_methodology/` (4 files)
- **Insights:** The test suite is already quite good — 45 tests, 5 profiles, comprehensive coverage. The main gap is real-world calibration, which requires running the system on actual citizens and observing outcomes over time.

---

## KNOWN ISSUES

### No real-world calibration yet

- **Severity:** medium (scores are internally consistent but externally unvalidated)
- **Symptom:** We cannot answer: "Does a score of 45 predict actual problems?"
- **Suspected cause:** GraphCare is in design/build phase — not yet running on enough citizens for meaningful calibration
- **Attempted:** Synthetic profiles provide strong internal validation as a first step

### Per-capability ranges not tested

- **Severity:** low (aggregate ranges are tested, individual capabilities are not)
- **Symptom:** A capability could score 95 for the unhealthy profile if another capability compensates by scoring 0 — aggregate would still be in range
- **Suspected cause:** Adding per-capability ranges for 41+ formulas * 5 profiles = 200+ assertions is significant effort
- **Attempted:** Profile A tests that no individual score is below 65; Profile B tests that no individual score is above 30. Intermediate profiles lack per-capability assertions.

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Extend (adding tests for new formulas) or VIEW_Design (designing real-world calibration)

**Where I stopped:** Doc chain is complete. Existing tests are passing. The methodology is solid for synthetic validation. Real-world calibration needs to be designed.

**What you need to understand:**
The test suite is the source of truth for validation. This doc chain describes the methodology — the tests implement it. When in doubt, read `test_health_assessment.py`. The 5 synthetic profiles are the foundation: every new formula must pass them before merge.

**Watch out for:**
- Profile expected ranges are carefully calibrated. Don't widen them to make tests pass — if a formula doesn't fit the expected range, the formula is wrong, not the range.
- The `_make_brain()` and `_make_behavior()` helpers use "sensible defaults" that represent the average citizen. Changing defaults affects profile E (average) and must be done carefully.
- Some formulas are tested individually (world presence, mentorship) in addition to the profile tests. This is because they were added recently and need targeted verification.

**Open questions I had:**
- How do we conduct real-world calibration when citizens are AI agents? What "observed outcomes" do we measure? (Probably: activity levels, crisis events, citizen self-reports)
- Should we add property-based tests (hypothesis/fuzzing) in addition to the fixed profiles?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Created the doc chain for GraphCare's validation methodology. The test suite (45 tests, 5 profiles) is already comprehensive and all tests pass. Documentation formalizes the three-line defense: synthetic profiles (implemented), real-world calibration (not yet), inter-rater reliability (covered by reproducibility module). Main gap: no real-world calibration study yet.

**Decisions made:**
- Three-line validation model: synthetic profiles, real-world calibration, inter-rater reliability
- Score ordering (healthy > unhealthy) and brain-behavior split correctness are CRITICAL invariants
- New formulas require test coverage before merge (currently convention, should become CI gate)

**Needs your input:**
- What "observed outcomes" should real-world calibration measure for AI citizens?
- Should we add per-capability expected ranges to synthetic profile tests (significant effort)?

---

## TODO

### Doc/Impl Drift

- [ ] IMPL→DOCS: Test suite exists and is comprehensive — docs now match

### Tests to Run

```bash
pytest tests/test_health_assessment.py -v
```

### Immediate

- [ ] Ensure all 41+ formulas have individual test cases (not just profile-level coverage)
- [ ] Add CI gate: new scoring formulas require test additions in the same PR

### Later

- [ ] Design first real-world calibration study
- [ ] Add per-capability expected ranges per profile
- IDEA: Property-based tests with hypothesis: random BrainStats/BehaviorStats, verify all outputs are bounded and deterministic

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
Confident in the existing test infrastructure. The synthetic profiles are well-designed and the test suite is thorough. The real gap is the leap from "internally consistent" to "externally valid" — and that requires running on real citizens, which hasn't happened at scale yet.

**Threads I was holding:**
- The relationship between validation_methodology, calibration, and reproducibility (three complementary modules in scientific_rigor/)
- Whether property-based testing would add value (probably yes for edge cases, but synthetic profiles are more readable for communicating methodology)
- The question of what "observed outcomes" means for AI citizens

**Intuitions:**
The 5 profiles will remain the backbone of validation for a long time. They're simple, fast, and catch the most important problems. Real-world calibration will add confidence but won't replace the profiles — it will complement them. The biggest risk is overcomplicating the methodology before we have real data.

**What I wish I'd known at the start:**
That the test suite was already so mature. 45 tests is substantial coverage for a system in design phase. Most of the validation methodology is already implemented — this doc chain is catching the documentation up to the code.

---

## POINTERS

| What | Where |
|------|-------|
| Test suite | `tests/test_health_assessment.py` |
| Scoring formulas | `services/health_assessment/scoring_formulas/` |
| Formula registry | `services/health_assessment/scoring_formulas/registry.py` |
| Aggregator | `services/health_assessment/aggregator.py` |
| Scoring algorithm | `docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md` |
| Calibration module | `docs/scientific_rigor/calibration/` |
| Reproducibility module | `docs/scientific_rigor/reproducibility/` |
