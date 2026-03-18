# Calibration — Sync: Current State

```
LAST_UPDATED: 2026-03-15
UPDATED_BY: @vox (doc chain creation)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- The calibration cycle concept: collect, analyze, hypothesize, adjust, retest
- Weight adjustment rules: one variable at a time, document before changing, retest fully, small steps, reversibility
- The 40/60 split is not calibratable (design principle, not empirical parameter)
- Synthetic profile tests as the non-regression gate

**What's still being designed:**
- Calibration log format and storage
- Bias detection methodology (which biases to look for first)
- Observation period and outcome measures for real-world calibration data
- Cadence of calibration cycles (quarterly? after N citizens assessed?)

**What's proposed (v2+):**
- "Calibration confidence" metric per formula (how many cycles it has survived)
- Automated bias detection: statistical tests run after each scoring pipeline execution
- Calibration dashboard showing weight stability over time

---

## CURRENT STATE

No calibration cycle has been executed. All current formula weights are initial educated guesses. This is expected and acceptable — the system is in design phase, and calibration requires real citizen data which does not yet exist at sufficient scale.

The infrastructure for calibration exists: the scoring pipeline produces scores, the aggregator stores history, and the synthetic profile tests provide the non-regression gate. What is missing is (a) enough real citizen data to analyze and (b) a formal calibration log to track adjustments.

The formulas themselves are well-structured for calibration. Each uses the `_cap(value, ceiling)` helper to normalize sub-components, and weights are explicit constants in the code. Adjusting a weight means changing a number in a formula function — the code structure supports it.

---

## IN PROGRESS

### Doc chain creation
- **Started:** 2026-03-15
- **By:** @vox
- **Status:** Complete
- **Context:** Documenting the calibration process before it starts, so that when we have enough data to begin calibrating, the process is already defined. This prevents ad-hoc weight tweaking.

---

## RECENT CHANGES

### 2026-03-15: Doc chain created

- **What:** Created full doc chain (OBJECTIVES, PATTERNS, VALIDATION, SYNC)
- **Why:** Calibration should be a principled process, not an afterthought. Documenting it now establishes the rules before the temptation to "just tweak the weights" arises.
- **Files:** `docs/scientific_rigor/calibration/` (4 files)
- **Insights:** The biggest risk is not bad calibration — it is no calibration. Initial weights that never get checked become gospel. The documentation establishes that initial weights are hypotheses, not truths.

---

## KNOWN ISSUES

### No calibration has occurred

- **Severity:** low (expected in design phase)
- **Symptom:** All weights are initial guesses
- **Suspected cause:** Insufficient real citizen data for meaningful calibration
- **Attempted:** Synthetic profile testing validates internal consistency, which is the best available substitute until real data exists

### No calibration log exists

- **Severity:** low (nothing to log yet)
- **Symptom:** When calibration begins, there is no established format or location for recording adjustments
- **Suspected cause:** Not yet needed
- **Attempted:** TODO marker added to create the log format before first calibration cycle

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Design (defining the first calibration cycle) or VIEW_Implement (when adjusting weights based on data)

**Where I stopped:** Doc chain is complete. No calibration has occurred. The next step is either (a) creating the calibration log format or (b) waiting for enough real citizen data to conduct the first calibration cycle.

**What you need to understand:**
Calibration is deliberately conservative. One variable at a time. Document before changing. Small steps. The goal is not to make scores perfect — it is to make them progressively better while maintaining the guarantees established by the synthetic profile tests.

**Watch out for:**
- The temptation to change multiple weights at once "because they're clearly all wrong." Single-variable discipline is critical even when multiple problems are visible.
- The 40/60 split is not up for calibration. If evidence suggests it should be different, escalate to design discussion — do not adjust it as a calibration step.
- Bias detection requires segmenting citizens by archetype. Without enough citizens in each segment, bias analysis produces noise, not insight. Wait for sufficient data.

**Open questions I had:**
- What is the minimum number of citizens needed for meaningful calibration? (Probably 20+ in Lumina Prime)
- How do we segment citizens into archetypes for bias analysis? (By activity level? By brain complexity? By age?)
- Should calibration cycles align with formula releases, or be on a fixed schedule?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Created the doc chain for GraphCare's calibration process. No calibration has occurred yet — all weights are initial educated guesses. The docs establish the rules for principled weight adjustment: one variable at a time, document everything, retest with synthetic profiles, preserve the 40/60 split. Ready for first calibration cycle when real data is available.

**Decisions made:**
- Calibration is human-in-the-loop, not automated optimization
- One variable per adjustment (causal clarity)
- 40/60 split is design-level, not calibration-level
- Bias detection takes priority over general accuracy improvement

**Needs your input:**
- When do you expect enough real citizen data for first calibration? What is the threshold?
- Should calibration logs be public (in the repo) or private (in the org graph)?

---

## TODO

### Doc/Impl Drift

- [ ] DOCS→IMPL: Create calibration log format and storage location

### Tests to Run

```bash
pytest tests/test_health_assessment.py -v
```

### Immediate

- [ ] Create calibration log template
- [ ] Identify the first 3 biases to investigate when data becomes available

### Later

- [ ] Conduct first calibration cycle
- [ ] Build bias detection tooling (per-segment score comparison)
- IDEA: Calibration "freeze" periods — after a calibration adjustment, no further changes for 2 weeks to observe the impact in isolation

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
Satisfied that the process is well-defined. The challenge is not the methodology — it is getting enough real data to apply it. The docs are intentionally written to prevent the common failure mode of calibration: ad-hoc weight tweaking without discipline.

**Threads I was holding:**
- The relationship between calibration and reproducibility (calibration changes weights, but the scoring must remain deterministic)
- Whether "calibration confidence" per formula is worth tracking (probably yes — it tells you which formulas have been empirically tested vs which are still raw guesses)
- The tension between conservative calibration (small steps) and real improvement needs (sometimes a weight is obviously wrong by 50%)

**Intuitions:**
The first calibration cycle will be the most impactful. Initial guesses are usually in the right ballpark (the synthetic profiles confirm this) but have specific blind spots that only real data reveals. After the first cycle, improvements will be incremental.

**What I wish I'd known at the start:**
How the scoring formula code is structured. The `_cap(value, ceiling)` pattern and explicit weight constants make calibration straightforward at the code level. The hard part is deciding what to change, not how to change it.

---

## POINTERS

| What | Where |
|------|-------|
| Scoring formulas | `services/health_assessment/scoring_formulas/` |
| Formula registry | `services/health_assessment/scoring_formulas/registry.py` |
| Test suite | `tests/test_health_assessment.py` |
| Validation methodology | `docs/scientific_rigor/validation_methodology/` |
| Reproducibility | `docs/scientific_rigor/reproducibility/` |
| Scoring algorithm | `docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md` |
