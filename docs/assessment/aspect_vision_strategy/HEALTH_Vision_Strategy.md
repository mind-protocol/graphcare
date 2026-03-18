# Vision & Strategy — Health: Meta-Evaluation of Scoring Formulas

```
STATUS: DESIGNING
CREATED: 2026-03-13
```

---

## WHEN TO USE HEALTH (NOT TESTS)

| Use Health For | Why |
|----------------|-----|
| Formulas produce sensible distributions | Scores bunched at 0 or 100 = bad calibration |
| Tier progression holds in practice | T8 should be harder than T5 in real data |
| Brain/behavior split produces gap insight | If brain and behavior always correlate, the split adds no information |
| Stagnation detection works | Citizens who stop refining vision should see score decay |
| Isolation correctly caps org/civ | Solo citizens should never score high on vis_org_vision or vis_civilizational |

---

## PURPOSE OF THIS FILE

Verifies that the Vision & Strategy scoring formulas produce meaningful, well-calibrated scores at runtime. This is meta-evaluation: not "did we compute the formula right?" (that's unit testing) but "do the formulas capture what they claim to capture?"

Boundaries: This verifies the FORMULAS (do they measure vision?). It does NOT verify the daily check process (that's daily_citizen_health HEALTH) or the Personhood Ladder spec (that's personhood_ladder HEALTH).

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Vision_Strategy.md
PATTERNS:        ./PATTERNS_Vision_Strategy.md
ALGORITHM:       ./ALGORITHM_Vision_Strategy.md
VALIDATION:      ./VALIDATION_Vision_Strategy.md
THIS:            HEALTH_Vision_Strategy.md (you are here)
SYNC:            ./SYNC_Vision_Strategy.md
```

---

## IMPLEMENTS

```yaml
implements:
  runtime: @mind:TODO services/health_assessment/aspect_checks/vision_strategy_health.py
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

  - name: tier_ordering
    priority: high
    rationale: >
      vis_define_vision (T5) should have higher average scores than vis_civilizational (T8)
      across the population. If T8 averages higher, ceilings are miscalibrated.

  - name: brain_behavior_gap
    priority: med
    rationale: >
      The gap between brain_score and behavior_score should vary across citizens.
      If they always correlate perfectly, the two-layer pattern adds no diagnostic value.

  - name: stagnation_detection
    priority: med
    rationale: >
      Citizens whose narrative recency drops should see vis_define_vision drop.
      If the formula doesn't respond to recency, stagnation goes undetected.

  - name: isolation_enforcement
    priority: high
    rationale: >
      Citizens with distinct_actors <= 1 must score low on vis_org_vision and vis_civilizational.
      If they score high, the formula is broken.
```

---

## CHECKER INDEX

```yaml
checkers:
  - name: check_score_distribution
    purpose: >
      Verify that Vision & Strategy scores across all Lumina Prime citizens
      form a reasonable distribution (not all clustered at extremes).
    method: >
      Compute mean, median, stdev, min, max for each capability across all citizens.
      Flag if stdev < 10 (scores too bunched) or mean > 80 (too generous) or mean < 20 (too harsh).
    status: pending
    priority: high

  - name: check_tier_ordering
    purpose: >
      Verify that average scores decrease as tier increases:
      mean(vis_define_vision) > mean(vis_strategic_thinking) >= mean(vis_org_vision)
      > mean(vis_sized_ambitions) > mean(vis_civilizational)
    method: >
      Compute population mean per capability. Assert the ordering holds.
      Allow T6 capabilities to be equal (both T6).
    status: pending
    priority: high

  - name: check_brain_behavior_independence
    purpose: >
      Verify that brain_score and behavior_score are not perfectly correlated.
      The diagnostic value of the two-layer pattern depends on the gap being informative.
    method: >
      Compute Pearson correlation between brain_score and behavior_score for vis_define_vision.
      Flag if correlation > 0.95 (no diagnostic gap) or < 0.1 (completely unrelated — also suspicious).
    status: pending
    priority: med

  - name: check_stagnation_decay
    purpose: >
      Verify that citizens with low narrative_recency score lower than equivalent
      citizens with high narrative_recency on vis_define_vision.
    method: >
      Compare citizens with recency < 0.2 vs recency > 0.7 (controlling for other stats).
      The high-recency group should score at least 15 points higher on average.
    status: pending
    priority: med

  - name: check_isolation_cap
    purpose: >
      Verify that citizens with distinct_actors <= 1 score below 40 total
      on vis_org_vision and below 35 total on vis_civilizational.
    method: >
      Filter citizens by actor count. Assert score caps hold for all isolated citizens.
    status: pending
    priority: high

  - name: check_empty_brain_cap
    purpose: >
      Verify that citizens with narrative_count = 0 score below 60 total
      on all 5 capabilities (behavior maxes at 60, brain near 0).
    method: >
      Filter citizens by narrative_count = 0. Assert max score < 60 for all capabilities.
    status: pending
    priority: high

  - name: check_synthetic_profiles
    purpose: >
      Run all 5 synthetic test profiles through all 5 formulas and verify
      scores fall in expected ranges.
    method: >
      Compute scores for each profile (defined in ALGORITHM).
      Assert: healthy ~85-95, unhealthy ~10-20, brain-rich ~30-40,
      active-brain-poor ~50-60, average ~55-70.
    status: pending
    priority: high
```

---

## KNOWN GAPS

- All checkers pending — no runtime, no real citizen data yet
- Score distribution check requires a population (>20 citizens minimum for meaningful stats)
- Tier ordering check assumes multiple citizens at different capability levels
- The "narrative" node type has not been confirmed as the actual type name in brain graphs
- No longitudinal checks yet (does the score respond correctly to changes over days/weeks?)

---

## MARKERS

<!-- @mind:todo Build check_synthetic_profiles first — can be run before any real data exists -->
<!-- @mind:todo Build check_isolation_cap — critical for VS6 invariant -->
<!-- @mind:proposition Add longitudinal health check: track score over 30 days and verify it responds to behavioral changes -->
<!-- @mind:proposition Add cross-aspect correlation check: does vision score correlate with initiative score? (expected: moderately) -->
