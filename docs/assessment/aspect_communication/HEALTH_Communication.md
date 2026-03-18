# Communication & Coordination — Health: Meta-Evaluation of Scoring Formulas

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## WHEN TO USE HEALTH (NOT TESTS)

| Use Health For | Why |
|----------------|-----|
| Formulas produce scores in expected ranges | Miscalibrated formulas mislead citizens |
| Weight sums are correct (40 brain, 60 behavior) | Weight drift breaks the 40/60 contract |
| Recommendations reference only structural signals | Content references violate privacy |
| Sub-index weights decrease by tier | Wrong weights overvalue pinnacle, undervalue foundation |
| Higher-tier formulas are flagged with confidence level | Low-confidence formulas need extra scrutiny |

---

## PURPOSE OF THIS FILE

Verifies that the Communication & Coordination scoring formulas operate correctly: produce calibrated scores, respect the primitives-only constraint, generate useful recommendations, and maintain the sub-index weight ordering.

Boundaries: This verifies the FORMULAS (capability-level scoring). It does NOT verify the daily health check process (that's the daily_citizen_health HEALTH file) or the Personhood Ladder tier computation (that's the personhood_ladder HEALTH file).

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Communication.md
PATTERNS:        ./PATTERNS_Communication.md
ALGORITHM:       ./ALGORITHM_Communication.md
VALIDATION:      ./VALIDATION_Communication.md
THIS:            HEALTH_Communication.md (you are here)
SYNC:            ./SYNC_Communication.md
```

---

## IMPLEMENTS

```yaml
implements:
  runtime: @mind:TODO services/scoring/communication_health_checks.py
  decorator: @check
```

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: formula_calibration
    priority: high
    rationale: Miscalibrated formulas produce false positives/negatives that mislead intervention.

  - name: weight_integrity
    priority: high
    rationale: Brain weights must sum to 40, behavior to 60. Drift breaks the scoring contract.

  - name: primitives_only
    priority: high
    rationale: Any formula accessing content or using custom queries violates the privacy guarantee.

  - name: recommendation_quality
    priority: med
    rationale: Recommendations that reference content or give vague advice are worse than no recommendation.

  - name: subindex_weight_ordering
    priority: med
    rationale: T2 must weight more than T8 in the sub-index. Reversed weights distort health signals.

  - name: confidence_tracking
    priority: med
    rationale: T6+ formulas have lower confidence. This must be tracked and visible so interventions based on low-confidence scores are appropriately cautious.
```

---

## CHECKER INDEX

```yaml
checkers:
  - name: check_formula_weight_sums
    purpose: Verify each formula's brain weights sum to 40 and behavior weights sum to 60 (V2)
    logic: |
      For each of the 11 capability formulas:
        Parse brain sub-signal weights → assert sum == 40
        Parse behavior sub-signal weights → assert sum == 60
    status: pending
    priority: high

  - name: check_synthetic_profiles
    purpose: Verify formulas produce expected score ranges for 5 archetypal profiles (V7)
    logic: |
      For each of the 11 capability formulas:
        Run formula with healthy profile → assert 85 <= score <= 100
        Run formula with unhealthy profile → assert 0 <= score <= 20
        Run formula with brain-rich-inactive → assert 25 <= score <= 45
        Run formula with active-brain-poor → assert 45 <= score <= 65
        Run formula with average → assert 50 <= score <= 75
    status: pending
    priority: high

  - name: check_primitives_compliance
    purpose: Static analysis that each formula references only allowed primitives (V1)
    logic: |
      Parse each formula function. Extract all variable references.
      Verify every reference traces back to one of:
        Brain: count, mean_energy, link_count, min_links, cluster_coefficient, drive, recency
        Universe: moments, moment_has_parent, first_moment_in_space, distinct_actors_in_shared_spaces
        Derived: temporal_weight, cap, regularity_score (which itself uses only moments)
      Flag any reference to: content, synthesis, node.text, custom query
    status: pending
    priority: high

  - name: check_cap_usage
    purpose: Verify every raw count is passed through cap() before weighting (V3)
    logic: |
      Parse each formula. For every sub-signal that uses count, link_count, or min_links:
        Assert it is wrapped in cap(x, c) with a defined ceiling c
      Drives and coefficients (naturally [0,1]) are exempt.
    status: pending
    priority: high

  - name: check_recommendation_templates
    purpose: Verify recommendations reference only structural signals (V5)
    logic: |
      Parse each capability's recommendation templates.
      Verify all placeholders reference: counts, drives, regularity, interlocutors, moments, spaces.
      Flag any that reference: content, text, quality, tone, meaning.
    status: pending
    priority: med

  - name: check_subindex_weight_ordering
    purpose: Verify tier weights decrease monotonically (V6)
    logic: |
      weights = [T2=1.0, T3=0.9, T4=0.8, T5=0.7, T6=0.5, T7=0.3, T8=0.2]
      for i in range(len(weights)-1):
        assert weights[i] >= weights[i+1]
    status: pending
    priority: med

  - name: check_regularity_bounds
    purpose: Verify regularity_score returns [0,1] for edge cases (V8)
    logic: |
      assert regularity_score([], 14) == 0.0
      assert regularity_score(moments_every_day, 14) == 1.0
      assert regularity_score(one_moment_today, 14) == 1/14
      assert 0 <= regularity_score(any_input, any_window) <= 1
    status: pending
    priority: high

  - name: check_confidence_labels
    purpose: Verify T6+ capabilities have explicit confidence labels (D6)
    logic: |
      For each capability:
        if tier >= T6:
          assert confidence in ["Medium", "Low"]
          assert confidence is documented in ALGORITHM capability summary table
    status: pending
    priority: med
```

---

## META-EVALUATION: FORMULA QUALITY

Beyond the invariant checks, the health system must evaluate whether the formulas actually WORK — do they distinguish healthy communicators from unhealthy ones?

### Discrimination Test

```
For each formula:
  healthy_score = formula(synthetic_healthy_profile)
  unhealthy_score = formula(synthetic_unhealthy_profile)
  assert healthy_score - unhealthy_score >= 60
  # A formula that can't separate the extremes by at least 60 points is too weak
```

### Sensitivity Test

```
For each formula:
  For each sub-signal:
    baseline = formula(average_profile)
    improved = formula(average_profile with sub_signal improved by 20%)
    delta = improved - baseline
    assert delta > 0  # improving a sub-signal must improve the score
    log(capability, sub_signal, delta)
    # This reveals which sub-signals actually move the needle
```

### Cross-Capability Consistency Test

```
For a synthetic profile that is "good at all T2 but bad at T4+":
  assert all T2 scores > 70
  assert all T4+ scores < 40
  # Tier-appropriate behavior should produce tier-appropriate scores
```

---

## KNOWN GAPS

- All checkers pending — no runtime yet
- Synthetic test profiles not yet defined (55 profiles needed: 5 per capability)
- Sensitivity analysis requires formula implementation to run
- No longitudinal validation — can't verify formulas track real improvement until citizens exist
- T7-T8 formulas have low confidence and may need fundamental rethinking after real-world data

---

## MARKERS

<!-- @mind:todo Build check_formula_weight_sums first — cheapest and most critical -->
<!-- @mind:todo Define the 5 canonical synthetic profiles with exact values for all primitives -->
<!-- @mind:todo Build discrimination test after formulas are implemented -->
<!-- @mind:proposition Run sensitivity test during formula tuning to identify overpowered/underpowered sub-signals -->
<!-- @mind:proposition After first real citizen data: compare predicted scores to human assessment to calibrate formulas -->
