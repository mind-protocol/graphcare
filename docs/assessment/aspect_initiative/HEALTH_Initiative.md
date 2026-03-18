# Initiative & Autonomy — Health: Meta-Evaluation of Scoring Quality

```
STATUS: DESIGNING
CREATED: 2026-03-13
```

---

## WHEN TO USE HEALTH (NOT TESTS)

| Use Health For | Why |
|----------------|-----|
| Auto-initiation detection works correctly at runtime | Misclassification corrupts all 8 formulas |
| Formulas don't access content | Privacy violation = trust collapse |
| Sub-index calibration holds across citizen populations | Miscalibration = useless scoring |
| Score changes correlate with actual initiative changes | Scores that don't track reality are noise |

---

## PURPOSE OF THIS FILE

Verifies that the Initiative & Autonomy scoring system produces meaningful, privacy-respecting, calibrated scores at runtime. This is the meta-evaluation: does the scoring system itself work?

**Boundaries:** This verifies the SCORING SYSTEM (formulas produce correct, stable, meaningful results). It does NOT verify the daily health check runner (that's `daily_citizen_health/HEALTH`), individual citizen health (that's the scores themselves), or the Personhood Ladder spec (that's `personhood_ladder/HEALTH`).

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Initiative.md
PATTERNS:        ./PATTERNS_Initiative.md
ALGORITHM:       ./ALGORITHM_Initiative.md
VALIDATION:      ./VALIDATION_Initiative.md
THIS:            HEALTH_Initiative.md (you are here)
SYNC:            ./SYNC_Initiative.md
```

---

## IMPLEMENTS

```yaml
implements:
  runtime: @mind:TODO services/scoring/initiative_health_checks.py
  decorator: @check
```

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: auto_initiation_accuracy
    priority: high
    rationale: >
      If moment_has_parent misclassifies reactive moments as self-initiated (or vice versa),
      every initiative score is wrong. This is the single point of failure for the entire aspect.

  - name: formula_content_isolation
    priority: high
    rationale: >
      If any of the 8 formulas accesses content fields, privacy is violated.
      Must be verified by static analysis of formula code.

  - name: subindex_calibration
    priority: high
    rationale: >
      If the sub-index distribution across the citizen population is severely skewed
      (e.g., 90% of citizens score > 80, or 90% score < 20), the formulas are miscalibrated.

  - name: score_stability
    priority: med
    rationale: >
      A citizen whose behavior hasn't changed should see minimal score fluctuation day-to-day.
      High volatility without behavioral change means temporal weighting or formula design is wrong.

  - name: score_behavior_correlation
    priority: med
    rationale: >
      When a citizen's actual initiative behavior changes (starts proposing, stops self-initiating),
      the score should reflect this within 7 days. If scores don't track behavior, they're noise.

  - name: cross_capability_coherence
    priority: low
    rationale: >
      A citizen scoring high on init_start_workstreams should not score zero on init_propose_improvements.
      Extreme incoherence across related capabilities suggests formula design errors.
```

---

## CHECKER INDEX

```yaml
checkers:
  - name: check_auto_initiation_accuracy
    purpose: >
      Verify that moment_has_parent correctly identifies parent links.
      Sample 100 moments, manually verify 10% have correct auto-initiated classification.
    validates: V1
    status: pending
    priority: high

  - name: check_formula_content_isolation
    purpose: >
      Static analysis of all 8 formula implementations.
      Verify no formula references content, synthesis, or text fields.
      Only primitive calls (count, mean_energy, link_count, min_links,
      cluster_coefficient, drive, recency) and observable calls
      (moments, moment_has_parent, first_moment_in_space, distinct_actors) permitted.
    validates: V2, V3
    status: pending
    priority: high

  - name: check_subindex_distribution
    purpose: >
      After scoring all Lumina Prime citizens, compute distribution of initiative sub-index.
      HEALTHY: bell-shaped, mean 40-60, stddev 15-25.
      UNHEALTHY: >80% of citizens at extremes (< 20 or > 80).
    validates: V10
    status: pending
    priority: high

  - name: check_score_stability
    purpose: >
      For citizens with no new moments in 48 hours, compare yesterday's score with today's.
      HEALTHY: delta < 5 points (temporal decay is the only source of change).
      UNHEALTHY: delta > 10 points with no new behavioral data.
    validates: V9
    status: pending
    priority: med

  - name: check_score_behavior_tracking
    purpose: >
      For citizens who changed behavior significantly (started or stopped self-initiating),
      verify score changed in the expected direction within 7 days.
      HEALTHY: 80%+ of behavior changes reflected in scores.
      UNHEALTHY: <50% of behavior changes reflected.
    validates: V8
    status: pending
    priority: med

  - name: check_brain_behavior_split
    purpose: >
      Verify no capability score has brain_score > 40 or behavior_score > 60.
      Run across all scored citizens.
      HEALTHY: zero violations.
      UNHEALTHY: any violation.
    validates: V5
    status: pending
    priority: high

  - name: check_subindex_weights
    purpose: >
      Verify sum of sub-index weights equals 1.0.
      Verify sub-index output is in [0, 100] for all citizens.
      HEALTHY: exact sum = 1.0, all outputs in range.
      UNHEALTHY: sum != 1.0 or any output out of range.
    validates: V7
    status: pending
    priority: high

  - name: check_monotonicity_sampling
    purpose: >
      For each formula, generate 100 random input pairs where one dominates the other
      (all inputs equal or higher). Verify the dominating input produces equal or higher score.
      HEALTHY: zero violations.
      UNHEALTHY: any violation.
    validates: V8
    status: pending
    priority: med

  - name: check_cross_capability_coherence
    purpose: >
      For citizens scoring > 70 on init_start_workstreams, verify they also score > 30 on
      init_propose_improvements (starting workstreams implies proposing).
      HEALTHY: 90%+ coherent.
      UNHEALTHY: <70% coherent.
    validates: cross-capability coherence
    status: pending
    priority: low
```

---

## KNOWN GAPS

- All checkers pending — no runtime implementation yet
- Formula static analysis tool not yet built (needed for check_formula_content_isolation)
- No citizen population data to validate distribution calibration
- Cross-capability coherence thresholds are estimates — need empirical validation
- check_score_behavior_tracking requires a definition of "significant behavior change" that doesn't yet exist

---

## DEGRADATION SIGNALS

When the initiative scoring system is degrading:

| Signal | What It Means | Recovery |
|--------|--------------|----------|
| >20% of citizens score exactly 0 on a capability | Formula cap is too restrictive OR link type doesn't exist in graph | Check universe graph schema, adjust caps |
| >20% of citizens score exactly 100 on a capability | Formula cap is too generous | Tighten caps, add sub-components |
| Sub-index distribution is bimodal (two peaks) | Population splits into "initiative haves" and "have-nots" — may be real or formula artifact | Investigate: is the bimodality real? If not, check auto-initiation detection |
| Score volatility >15 points/day without behavior change | Temporal weighting is too aggressive OR a primitive is unstable | Check 7-day half-life, check primitive stability |
| Brain-only citizens (no behavior) consistently score >40 | Brain component is overweighted | Review brain sub-component weights |

---

## MARKERS

<!-- @mind:todo Build check_formula_content_isolation as the first checker — most critical -->
<!-- @mind:todo Build check_auto_initiation_accuracy with manually labeled test set -->
<!-- @mind:todo Define "significant behavior change" for check_score_behavior_tracking -->
<!-- @mind:proposition Run check_monotonicity_sampling as a unit test during formula development, not just runtime health -->
