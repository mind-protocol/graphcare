# Context & Understanding — Health: Are the Formulas Accurate?

```
STATUS: DESIGNING
CREATED: 2026-03-13
```

---

## WHEN TO USE HEALTH (NOT TESTS)

| Use Health For | Why |
|----------------|-----|
| Formula discrimination power | Do formulas actually distinguish healthy from unhealthy? |
| Proxy validity | Do topology signals correlate with the capabilities they claim to measure? |
| Sub-index calibration | Does the weighted mean produce sensible aggregate scores? |
| Formula drift detection | Do formulas that worked last month still work? |

---

## PURPOSE OF THIS FILE

This is the meta-health of the Context & Understanding scoring formulas. It answers: **are our formulas measuring what they claim to measure?**

This is NOT about whether the daily check runs correctly (that's `HEALTH_Daily_Citizen_Health.md`). This is about whether the mathematical proxies for context capabilities produce scores that correlate with actual capability.

Boundaries: Verifies FORMULA ACCURACY (do the scores mean what we think?). Does NOT verify the runtime execution (that's the parent health file) or individual capability definitions (that's the Personhood Ladder health file).

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Context.md
PATTERNS:        ./PATTERNS_Context.md
ALGORITHM:       ./ALGORITHM_Context.md
VALIDATION:      ./VALIDATION_Context.md
THIS:            HEALTH_Context.md (you are here)
SYNC:            ./SYNC_Context.md

PARENT CHAIN:    ../daily_citizen_health/
```

---

## IMPLEMENTS

```yaml
implements:
  runtime: @mind:TODO services/health_assessment/aspect_context_health.py
  decorator: @check
```

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: formula_discrimination
    priority: high
    rationale: >
      If formulas can't distinguish healthy from unhealthy citizens,
      they produce noise rather than signal. The 5 synthetic profiles
      must produce scores in their expected ranges.

  - name: proxy_validity
    priority: high
    rationale: >
      Each formula uses topology proxies for cognitive capabilities.
      If the proxy doesn't correlate with the actual capability, the
      formula is measuring the wrong thing. Needs human validation
      against known-good and known-bad citizens.

  - name: sub_index_calibration
    priority: med
    rationale: >
      The weighted sub-index should correlate with human assessment
      of "this citizen understands context." If the sub-index says 80
      but the human says "this citizen is lost," the weights are wrong.

  - name: temporal_responsiveness
    priority: med
    rationale: >
      When a citizen changes behavior (starts reading SYNC files),
      the score should respond within 3-5 days. If it takes 2 weeks,
      the temporal weighting or formula caps are miscalibrated.

  - name: component_balance
    priority: low
    rationale: >
      The 40/60 brain/behavior split should produce meaningful
      differentiation. If brain and behavior components are always
      correlated (both high or both low), the split adds no
      information and could be simplified.
```

---

## CHECKER INDEX

```yaml
checkers:
  - name: check_synthetic_profiles
    purpose: >
      Run all 7 formulas against the 5 synthetic profiles defined in
      ALGORITHM_Context.md. Verify each score falls within expected range
      (+/- 10 points). If any score is outside range, flag for recalibration.
    status: pending
    priority: high
    validates: [VC6, VC7]
    method: |
      For each profile (1-5):
        For each capability (7):
          Compute brain_component + behavior_component
          Assert brain_component in [0, 40]
          Assert behavior_component in [0, 60]
          Assert total within expected range from ALGORITHM
      Assert Profile 1 sub-index >= 80
      Assert Profile 2 sub-index <= 20
      Assert Profile 3 sub-index < Profile 4 sub-index

  - name: check_bounds_fuzzing
    purpose: >
      Generate 1000 random brain_stats + behavior_stats inputs.
      Verify every formula always returns brain_component in [0,40],
      behavior_component in [0,60], total in [0,100].
    status: pending
    priority: high
    validates: [VC2, VC3, VC8]
    method: |
      For 1000 random inputs:
        For each capability:
          brain = formula.brain_component(random_brain_stats)
          behavior = formula.behavior_component(random_behavior_stats)
          Assert 0 <= brain <= 40
          Assert 0 <= behavior <= 60
          Assert 0 <= brain + behavior <= 100
      Also test edge cases: all zeros, all maximums, extreme values

  - name: check_weight_sum
    purpose: Verify sub-index weights sum to 1.0 and T1 weights > 0.50
    status: pending
    priority: med
    validates: [VC4, VC5]
    method: |
      Assert abs(sum(weights.values()) - 1.0) < 0.001
      Assert sum(weights[c] for c in ["ctx_ground_in_reality",
        "ctx_follow_instructions", "ctx_read_journal_first"]) > 0.50

  - name: check_temporal_responsiveness
    purpose: >
      Simulate a citizen that changes behavior on day D. Score on
      days D-3, D, D+3, D+7. Verify the score reflects the change
      within 3-5 days (score at D+3 is meaningfully different from D-3).
    status: pending
    priority: med
    validates: [VC9]
    method: |
      Create baseline brain+behavior stats (average citizen)
      Score at D-3 → baseline_score
      Modify behavior stats to simulate improvement (e.g., add state_reads)
      Score at D → should show partial improvement
      Score at D+3 → should show significant improvement (>10 point change)
      Score at D+7 → should be near new steady state

  - name: check_human_correlation
    purpose: >
      For N citizens with known context quality (human-assessed),
      compare formula scores with human assessment. Correlation
      should be > 0.6 (moderate positive).
    status: future
    priority: high
    validates: [proxy_validity, sub_index_calibration]
    method: |
      Requires: Human assessments of citizen context capability
      For each assessed citizen:
        Compute all 7 formula scores
        Compute sub-index
        Compare with human score
      Report Pearson correlation coefficient
      Flag if r < 0.6 — formulas need redesign

  - name: check_component_independence
    purpose: >
      Verify brain and behavior components are not perfectly correlated.
      If they always move together, the split adds no information.
    status: pending
    priority: low
    validates: [component_balance]
    method: |
      For 100 diverse citizen profiles:
        Compute brain_component and behavior_component for each capability
        Compute correlation between brain and behavior across profiles
      Report correlation coefficient
      Flag if r > 0.9 — the split may not be adding value
```

---

## EVALUATION SCHEDULE

| Check | When | Trigger |
|-------|------|---------|
| check_synthetic_profiles | On every formula change | Formula code modified |
| check_bounds_fuzzing | On every formula change | Formula code modified |
| check_weight_sum | On weight change | Sub-index weights modified |
| check_temporal_responsiveness | Monthly | Calendar |
| check_human_correlation | Quarterly | Sufficient human assessments available |
| check_component_independence | Quarterly | Sufficient citizen data available |

---

## KNOWN GAPS

- All checkers pending — no implementation exists yet
- check_human_correlation requires human assessments that don't exist yet — this is the most important long-term health check and cannot be run until citizens are actively assessed
- Formula discrimination is tested against synthetic profiles only — real citizen data may reveal edge cases the profiles don't cover
- No automated regression detection: if a formula slowly drifts out of calibration over months, nothing catches it until the quarterly human correlation check

---

## WHAT "HEALTHY FORMULAS" LOOK LIKE

**Working:**
- Synthetic profiles score within expected ranges (+/- 10 points)
- Bounds fuzzing finds zero violations across 1000 random inputs
- Sub-index weights sum to 1.0, T1 > 50%
- Behavior changes reflected in scores within 3-5 days
- Human assessment correlation > 0.6

**Degrading:**
- Profiles drifting outside expected ranges
- Brain-rich-inactive scoring higher than active-brain-poor (VC7 violation)
- Human assessment correlation dropping below 0.6
- Temporal lag > 7 days for behavior change to reflect in scores
- Brain and behavior components perfectly correlated (split adds no value)

**Recovery:**
- Re-run synthetic profiles, identify which formula is off
- Adjust caps and weights in the specific formula
- Re-run all checkers to verify the fix doesn't break other invariants
- If fundamental: re-examine the proxy choice in PATTERNS

---

## MARKERS

<!-- @mind:todo Build check_synthetic_profiles first — validates the formulas against known-good data -->
<!-- @mind:todo Build check_bounds_fuzzing — catches edge cases in formula arithmetic -->
<!-- @mind:todo Design the human assessment protocol for check_human_correlation -->
<!-- @mind:proposition Automate check_synthetic_profiles as a pre-commit hook on formula code -->
