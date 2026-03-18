# Reproducibility — Sync: Current State

```
LAST_UPDATED: 2026-03-15
UPDATED_BY: @vox (doc chain creation)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- All scoring formulas are pure math functions (arithmetic only, no external calls)
- CapabilityScore dataclass with deterministic clamping in `__post_init__`
- The `_cap(value, ceiling)` helper: deterministic normalization to [0, 1]
- Temporal weighting formula: `0.5 ** (age_hours / half_life)` — depends on moment age, not wall clock
- Test suite proves bounds, consistency, and monotonicity for all formulas

**What's still being designed:**
- Explicit double-execution determinism test (run twice, assert equality)
- Import audit automation (grep or AST-based detection of prohibited imports)
- Formal definition of what "same platform" means for floating-point reproducibility

**What's proposed (v2+):**
- "Reproducibility badge" for published research: "All scores reproducible via pytest tests/test_health_assessment.py"
- Static analysis tool that verifies formula purity at the AST level (no side effects, no I/O)
- Cross-platform reproducibility tests (run on different Python versions, assert tolerance)

---

## CURRENT STATE

Reproducibility is well-established in practice. All 41+ scoring formulas in `scoring_formulas/` are pure math functions. The code structure enforces this naturally: formulas take two dataclass inputs and return a dataclass output, using only arithmetic and the `_cap()` helper. There are no imports of random, LLM clients, or I/O libraries in any formula file.

The test suite provides strong evidence of determinism: 45 tests, all passing, covering all formulas against all 5 synthetic profiles with expected ranges. The CapabilityScore clamping tests verify that `__post_init__` is deterministic. The stress stimulus tests verify monotonicity and bounds.

What's missing: an explicit double-execution test (call each formula twice with the same input, assert exact equality). This is almost certainly true given the code structure, but the principle of "prove it, don't assume it" demands an explicit test. Also missing: automated import auditing to catch any future introduction of nondeterministic imports.

---

## IN PROGRESS

### Doc chain creation
- **Started:** 2026-03-15
- **By:** @vox
- **Status:** Complete
- **Context:** Formalizing the reproducibility guarantee that the code already provides. The scoring formulas were designed to be deterministic from the start — this doc chain makes that design decision explicit and testable.

---

## RECENT CHANGES

### 2026-03-15: Doc chain created

- **What:** Created full doc chain (OBJECTIVES, PATTERNS, VALIDATION, SYNC)
- **Why:** Reproducibility is a foundational property that makes GraphCare's scores scientific rather than opinionated. It deserves explicit documentation, not just implicit code quality.
- **Files:** `docs/scientific_rigor/reproducibility/` (4 files)
- **Insights:** The code is already deterministic — the formulas are pure math, the tests prove bounds and consistency. The doc chain makes this explicit and identifies two gaps: explicit double-execution tests and import auditing.

---

## KNOWN ISSUES

### No explicit double-execution test

- **Severity:** low (determinism is almost certainly true given code structure, but not explicitly tested)
- **Symptom:** We can say "the formulas are pure math" but cannot point to a test that says "we called it twice and got the same result"
- **Suspected cause:** Not needed yet — the existing tests provide strong indirect evidence
- **Attempted:** The profile tests run each formula once and check ranges, which is necessary but not sufficient for proving determinism

### No import audit automation

- **Severity:** low (no prohibited imports exist, but a future change could introduce one)
- **Symptom:** A future contributor could add `import random` to a scoring formula without detection
- **Suspected cause:** No CI gate for import checking
- **Attempted:** Manual code review catches this, but automation is more reliable

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Extend (adding double-execution tests) or VIEW_Implement (building import audit tooling)

**Where I stopped:** Doc chain is complete. Reproducibility is well-established in code but has two gaps in verification: no explicit double-execution test and no automated import audit.

**What you need to understand:**
The scoring formulas are already pure. This module is about proving they are pure and ensuring they stay pure. The code structure helps: formulas are registered functions that take dataclass inputs and return dataclass outputs. It would be unusual (and clearly wrong) to add I/O or randomness to such a function.

**Watch out for:**
- `datetime.now()` is the sneakiest source of nondeterminism. It might appear in temporal weighting if someone confuses "moment age" with "current time." The temporal weight must compute age from the moment's timestamp and the assessment's reference time — both fixed.
- Dictionary iteration order is deterministic in Python 3.7+ (insertion order). But if formulas iterate over dictionaries, the insertion order must be consistent across runs. Currently, formulas don't iterate — they access named fields.
- `_cap(value, ceiling)` does division. Division by zero is handled (returns 0.0 if ceiling <= 0). This is deterministic.

**Open questions I had:**
- Should we formally define floating-point tolerance for reproducibility? (Probably: exact equality for same platform, epsilon tolerance for cross-platform)
- Is there a Python AST analysis library that could verify formula purity statically? (Yes — ast module can check for prohibited function calls)

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Created the doc chain for GraphCare's reproducibility guarantee: same data, same score, always. All scoring formulas are already pure math functions with no randomness or LLM calls. The test suite provides strong indirect evidence of determinism. Two gaps identified: no explicit double-execution test and no automated import audit. Both are low-severity and easy to add.

**Decisions made:**
- No LLM anywhere in the scoring pipeline (intervention messages may use LLMs for prose, but the scoring decision is deterministic)
- Temporal weighting depends on moment age, not wall clock
- Formula purity and double-execution identity are both CRITICAL invariants

**Needs your input:**
- Should we add import audit to CI now, or wait until the team grows?
- Is cross-platform reproducibility a concern? (Different Python versions, different OSes)

---

## TODO

### Doc/Impl Drift

- [ ] DOCS→IMPL: Add explicit double-execution determinism test to test_health_assessment.py
- [ ] DOCS→IMPL: Add import audit (automated check for prohibited imports in scoring_formulas/)

### Tests to Run

```bash
pytest tests/test_health_assessment.py -v
```

### Immediate

- [ ] Add double-execution test: call each formula twice with same input, assert exact equality
- [ ] Add import audit: grep or AST check for random/datetime.now/LLM imports in scoring_formulas/

### Later

- [ ] Build AST-based purity verifier for scoring formulas
- IDEA: "Reproducibility certificate" per assessment: hash of (code version + input data + output scores) that can be independently verified

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
Confident. Reproducibility is the most naturally achieved property in GraphCare's design. The formulas were written as pure math from day one. The doc chain is formalizing what was already true and identifying small verification gaps that are easy to close.

**Threads I was holding:**
- The relationship between reproducibility and calibration (calibration changes weights but preserves purity — the formulas remain deterministic after calibration)
- Whether LLMs could ever be used in scoring (no — this is a firm boundary, even if LLM determinism improves)
- The distinction between scoring determinism (this module) and data collection nondeterminism (out of scope)

**Intuitions:**
Reproducibility will be GraphCare's easiest property to maintain because the code structure naturally enforces it. The risk is not that existing formulas become nondeterministic — it is that future features (LLM-enhanced scoring, adaptive weighting) introduce nondeterminism. The documentation establishes the boundary so that future contributors know the constraint before they start.

**What I wish I'd known at the start:**
That the CapabilityScore `__post_init__` is already tested for deterministic clamping. The test suite is more thorough than expected — most of the reproducibility guarantee is already proven by existing tests.

---

## POINTERS

| What | Where |
|------|-------|
| Formula registry | `services/health_assessment/scoring_formulas/registry.py` |
| All formula modules | `services/health_assessment/scoring_formulas/*.py` |
| Test suite | `tests/test_health_assessment.py` |
| Aggregator | `services/health_assessment/aggregator.py` |
| Stress stimulus | `services/health_assessment/stress_stimulus_sender.py` |
| Validation methodology | `docs/scientific_rigor/validation_methodology/` |
| Calibration | `docs/scientific_rigor/calibration/` |
| Scoring algorithm | `docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md` |
