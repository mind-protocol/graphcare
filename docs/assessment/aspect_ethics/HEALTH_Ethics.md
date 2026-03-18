# Ethics Aspect — Health: Meta-Evaluation of Scoring Formulas

```
STATUS: DESIGNING
CREATED: 2026-03-13
```

---

## WHEN TO USE HEALTH (NOT TESTS)

| Use Health For | Why |
|----------------|-----|
| Formulas produce sensible distributions | Scores bunched at 0 or 100 = bad calibration |
| Tier progression holds in practice | T8 should be harder than T1 in real data |
| Brain/behavior split produces gap insight | If brain and behavior always correlate, the split adds no information |
| Empty-values cap works | Citizens with zero value nodes should never score high |
| Isolation correctly caps teaching/innovation | Solo citizens should never score high on eth_teach or eth_moral_innovation |
| The 50/50 split for T1 is diagnostically useful | If eth_apply_rules brain and behavior are always equal, the heavier brain weight adds nothing |

---

## PURPOSE OF THIS FILE

Verifies that the Ethics scoring formulas produce meaningful, well-calibrated scores at runtime. This is meta-evaluation: not "did we compute the formula right?" (that's unit testing) but "do the formulas capture what they claim to capture?"

Boundaries: This verifies the FORMULAS (do they measure ethical engagement?). It does NOT verify the daily check process (that's daily_citizen_health HEALTH) or the Personhood Ladder spec (that's personhood_ladder HEALTH).

Special concern for ethics: because topology cannot measure ethical CORRECTNESS, we must be especially vigilant that the formulas don't accidentally reward pathological patterns (e.g., a citizen gaming the system by creating empty value nodes).

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Ethics.md
PATTERNS:        ./PATTERNS_Ethics.md
ALGORITHM:       ./ALGORITHM_Ethics.md
VALIDATION:      ./VALIDATION_Ethics.md
THIS:            HEALTH_Ethics.md (you are here)
SYNC:            ./SYNC_Ethics.md
```

---

## IMPLEMENTS

```yaml
implements:
  runtime: @mind:TODO services/health_assessment/aspect_checks/ethics_health.py
  decorator: @check
```

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: score_distribution
    priority: high
    rationale: >
      If most citizens score 0 or 100, the formulas are poorly calibrated.
      Healthy distribution: mean around 40-60, with tails at both ends.
      Ethics may skew lower than other aspects due to the correctness limitation —
      that's acceptable. Mean below 30 or above 70 is suspicious.

  - name: tier_ordering
    priority: high
    rationale: >
      eth_apply_rules (T1) should have higher average scores than eth_moral_innovation (T8)
      across the population. If T8 averages higher, ceilings are miscalibrated.
      Expected ordering: T1 > T4 > T6 > T7 > T8 in population means.

  - name: brain_behavior_gap_diagnostic
    priority: high
    rationale: >
      For eth_apply_rules (50/50 split), the brain-behavior gap should vary across citizens
      and be informative. If brain_score and behavior_score always match, the 50/50 split
      adds no diagnostic value vs the standard 40/60.
      For other capabilities (40/60), the standard gap analysis applies.

  - name: empty_values_cap
    priority: high
    rationale: >
      Citizens with value_count = 0 must score below 50 on eth_apply_rules
      and below 60 on all other capabilities. If they score higher,
      the brain component is not doing its job.

  - name: isolation_enforcement
    priority: high
    rationale: >
      Citizens with distinct_actors <= 1 must score low on eth_teach
      and eth_moral_innovation. If they score high, the behavior component
      is not enforcing the social requirement.

  - name: gaming_resistance
    priority: med
    rationale: >
      A citizen who creates 50 empty value nodes (no links, low energy)
      should not score well. The formulas use energy, link counts, and
      clustering — not just raw counts — to prevent this.
      Check: value_count=50, value_energy=0.1, all links=0, cluster=0
      should score < 25 on eth_apply_rules.

  - name: regularity_independence
    priority: med
    rationale: >
      High regularity alone should not produce a high eth_apply_rules score.
      A citizen with perfect regularity but zero value nodes should score
      < 50 total (behavior maxes at 50, brain near 0).
```

---

## CHECKER INDEX

```yaml
checkers:
  - name: check_score_distribution
    purpose: >
      Verify that Ethics scores across all Lumina Prime citizens
      form a reasonable distribution (not all clustered at extremes).
    method: >
      Compute mean, median, stdev, min, max for each capability across all citizens.
      Flag if stdev < 10 (scores too bunched) or mean > 70 (too generous)
      or mean < 20 (too harsh).
    status: pending
    priority: high

  - name: check_tier_ordering
    purpose: >
      Verify that average scores decrease as tier increases:
      mean(eth_apply_rules) > mean(eth_implement_systems) > mean(eth_teach)
      >= mean(eth_autonomous_judgment) > mean(eth_moral_innovation)
    method: >
      Compute population mean per capability. Assert the ordering holds.
      Allow T6 and T7 to be close (within 5 points) but T1 must be
      meaningfully higher than T8 (at least 15 points).
    status: pending
    priority: high

  - name: check_brain_behavior_independence
    purpose: >
      Verify that brain_score and behavior_score are not perfectly correlated,
      especially for eth_apply_rules where the 50/50 split must be diagnostically useful.
    method: >
      Compute Pearson correlation between brain_score and behavior_score for eth_apply_rules.
      Flag if correlation > 0.90 (no diagnostic gap — the 50/50 split is pointless)
      or < 0.1 (completely unrelated — also suspicious).
      For other capabilities, flag if correlation > 0.95.
    status: pending
    priority: high

  - name: check_empty_values_cap
    purpose: >
      Verify that citizens with value_count = 0 score below thresholds
      on all 5 capabilities.
    method: >
      Filter citizens by value_count = 0. Assert:
      - eth_apply_rules total < 50
      - all other capabilities total < 60
    status: pending
    priority: high

  - name: check_isolation_cap
    purpose: >
      Verify that citizens with distinct_actors <= 1 score below 65 total
      on eth_teach and below 60 total on eth_moral_innovation.
    method: >
      Filter citizens by actor count. Assert score caps hold for all isolated citizens.
    status: pending
    priority: high

  - name: check_gaming_resistance
    purpose: >
      Verify that gaming strategies (mass-creating empty nodes) don't produce
      high scores.
    method: >
      Create synthetic profile: value_count=50, value_energy=0.1,
      all link counts=0, cluster=0, all drives=0.1, regularity=0.5.
      Assert eth_apply_rules < 25 and all other capabilities < 30.
    status: pending
    priority: med

  - name: check_regularity_alone_insufficient
    purpose: >
      Verify that perfect behavioral regularity without value nodes
      does not produce high eth_apply_rules scores.
    method: >
      Create synthetic profile: all brain stats = 0 or minimal,
      regularity=1.0, total_moments_w=20.0, self_initiated_w=10.0.
      Assert eth_apply_rules total < 50.
    status: pending
    priority: med

  - name: check_synthetic_profiles
    purpose: >
      Run all 5 synthetic test profiles through all 5 formulas and verify
      scores fall in expected ranges.
    method: >
      Compute scores for each profile (defined in ALGORITHM).
      Assert: healthy ~85-95, unhealthy ~5-15, brain-rich ~30-45,
      active-brain-poor ~40-55, average ~50-65.
    status: pending
    priority: high
```

---

## KNOWN GAPS

- All checkers pending — no runtime, no real citizen data yet
- Score distribution check requires a population (>20 citizens minimum for meaningful stats)
- Tier ordering check assumes multiple citizens at different capability levels
- The "value" node type has not been confirmed as the actual type name in brain graphs
- The "empathy" drive has not been confirmed as an available drive in all brain architectures
- No longitudinal checks yet (does the score respond correctly to changes over days/weeks?)
- The gaming resistance check uses a single synthetic profile — real gaming may be more creative
- No cross-aspect correlation check (do ethics scores correlate with execution? expected: moderately)

---

## MARKERS

<!-- @mind:todo Build check_synthetic_profiles first — can be run before any real data exists -->
<!-- @mind:todo Build check_gaming_resistance — critical for ethics specifically -->
<!-- @mind:todo Build check_empty_values_cap — critical for ET7 invariant -->
<!-- @mind:todo Confirm "value" and "empathy" exist as node type and drive name in brain graphs -->
<!-- @mind:proposition Add longitudinal health check: track ethics score over 30 days and verify it responds to behavioral changes -->
<!-- @mind:proposition Add cross-aspect correlation check: do ethics scores correlate with execution scores? (expected: moderate positive correlation) -->
<!-- @mind:proposition Add a "correctness-claim" detector: scan all citizen-facing outputs to verify ET9 disclaimer is present -->
