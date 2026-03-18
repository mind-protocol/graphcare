# Personal Connections Aspect — Health: Meta-Evaluation of Scoring Formulas

```
STATUS: DRAFT
CREATED: 2026-03-13
```

---

## WHEN TO USE HEALTH (NOT TESTS)

| Use Health For | Why |
|----------------|-----|
| Formulas produce expected score distributions | If healthy citizens score low or unhealthy score high, the formulas are miscalibrated |
| Reciprocity signal actually correlates with connection | If reciprocity is noise, every formula using it is degraded |
| Partial scoring acknowledgments remain accurate | If we claim `scored: partial` but actually measure nothing useful, the disclaimer is false |
| Caps reflect real citizen populations | If caps are too high (nobody reaches 1.0) or too low (everyone is capped), the formulas lose discrimination |

---

## PURPOSE OF THIS FILE

Verifies that the personal connections scoring formulas are THEMSELVES healthy: producing meaningful scores, using signals that actually correlate with relational capability, calibrated to real citizen populations, and honest about their limits.

This is meta-evaluation — evaluating the evaluation. It does NOT test individual citizen scores (that's runtime). It tests whether the FORMULAS are well-designed.

Boundaries: This verifies the scoring formulas. It does NOT verify the daily runner (that's daily_citizen_health HEALTH), the Personhood Ladder spec (that's personhood_ladder HEALTH), or the brain topology reader (separate module).

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Personal_Connections.md
PATTERNS:        ./PATTERNS_Personal_Connections.md
ALGORITHM:       ./ALGORITHM_Personal_Connections.md
VALIDATION:      ./VALIDATION_Personal_Connections.md
THIS:            HEALTH_Personal_Connections.md (you are here)
SYNC:            ./SYNC_Personal_Connections.md

PARENT CHAIN:    ../daily_citizen_health/HEALTH_Daily_Citizen_Health.md
SPEC:            ../../specs/personhood_ladder.json (aspect="personal_connections")
IMPL:            @mind:TODO
```

---

## IMPLEMENTS

```yaml
implements:
  runtime: @mind:TODO services/health_assessment/aspect_personal_connections_health.py
  decorator: @check
```

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: score_distribution_validity
    priority: high
    rationale: If all citizens score 90 or all score 10, the formulas lack discrimination.
  - name: synthetic_profile_accuracy
    priority: high
    rationale: The 5 synthetic profiles per capability are the ground truth. If formula outputs deviate from expected ranges, the formula is broken.
  - name: reciprocity_signal_validity
    priority: high
    rationale: Reciprocity is used in 6 of 11 formulas. If it doesn't correlate with relational quality, half the scoring is degraded.
  - name: cap_calibration
    priority: med
    rationale: Caps determine where scores saturate. Miscalibrated caps either compress everyone to max or prevent anyone from reaching it.
  - name: partial_score_honesty
    priority: med
    rationale: 7 of 11 capabilities are `scored: partial`. If the partial acknowledgments are inaccurate (claiming partial when it's really useless, or claiming partial when it's actually full), trust erodes.
  - name: brain_behavior_discrimination
    priority: high
    rationale: The brain-rich/inactive and active/brain-poor synthetic profiles must produce distinct scores. If they don't, the brain/behavior split adds no information.
  - name: volume_independence
    priority: high
    rationale: V2 invariant requires that volume alone cannot produce high scores. This must hold across all 11 formulas.
```

---

## CHECKER INDEX

```yaml
checkers:
  - name: check_synthetic_profiles
    purpose: Run all 55 synthetic test profiles (5 per capability * 11 capabilities) and verify outputs match expected ranges (within +/- 5 points)
    status: pending
    priority: high
    method: |
      For each capability:
        For each of 5 profiles (healthy, unhealthy, brain-rich/inactive, active/brain-poor, average):
          Compute score using formula
          Assert score within expected range from ALGORITHM doc
      Fail conditions: any score deviates by more than 5 points from documented expectation

  - name: check_brain_behavior_separation
    purpose: Verify that brain-rich/inactive profiles score differently from active/brain-poor profiles across all capabilities
    status: pending
    priority: high
    method: |
      For each capability:
        brain_rich_score = compute(brain_rich_inactive_profile)
        active_poor_score = compute(active_brain_poor_profile)
        Assert brain_rich_score and active_poor_score are in different ranges
        Assert neither profile scores above 70 (both are imbalanced)
      Fail conditions: profiles produce similar scores, or imbalanced profile scores above 70

  - name: check_volume_independence
    purpose: Verify V2 — that high moment volume alone cannot produce high behavior scores
    status: pending
    priority: high
    method: |
      For each capability:
        Create profile: shared_moments_w = cap * 2, but reciprocal_ratio = 0, space_types = 1, distinct_actors = 1, proactive_w = 0
        Assert behavior_score < 50% of behavior_component max
      Fail conditions: any capability allows volume alone to exceed 50% of behavior max

  - name: check_zero_interaction_floor
    purpose: Verify V5 — zero behavioral input produces behavior_component < 5
    status: pending
    priority: high
    method: |
      For each capability:
        Set all behavioral inputs to 0 (shared_moments_w=0, proactive_w=0, reciprocal_ratio=0, etc.)
        Assert behavior_component < 5
      Fail conditions: any capability produces behavior_component >= 5 with zero input

  - name: check_cap_distribution
    purpose: Verify caps produce reasonable score distributions across a population
    status: pending
    priority: med
    method: |
      Generate 100 synthetic citizen profiles with normally distributed inputs
      For each capability:
        Compute all 100 scores
        Assert mean is between 40-65 (not too easy, not too hard)
        Assert std_dev is between 15-30 (meaningful discrimination)
        Assert min < 20 and max > 75 (full range used)
      Fail conditions: distribution is compressed (std_dev < 10) or extreme (mean < 30 or > 80)

  - name: check_reciprocity_not_self_referential
    purpose: Verify V7 — reciprocal_ratio computation excludes self-responses
    status: pending
    priority: high
    method: |
      Create test case: citizen creates 10 moments, responds to 5 of their own moments, 0 external responses
      Assert reciprocal_ratio = 0
      Create test case: 10 moments, 3 external responses
      Assert reciprocal_ratio = 0.3

  - name: check_tier_cap_progression
    purpose: Verify V8 — shared signals have equal or higher caps at higher tiers
    status: pending
    priority: med
    method: |
      Extract all cap values per shared signal per capability
      For signals used across tiers (actor_count, shared_moments_w, space_types):
        Assert cap(T_n) <= cap(T_m) when T_n < T_m
      Fail conditions: any lower-tier cap exceeds a higher-tier cap for the same signal

  - name: check_partial_score_range
    purpose: Verify partial-scored capabilities produce meaningful ranges (not noise)
    status: pending
    priority: med
    method: |
      For each `scored: partial` capability:
        Run 50 varied synthetic profiles
        Assert score range (max - min) > 40 (formulas actually discriminate)
        Assert correlation between input quality and score > 0.5 (scores track input)
      Fail conditions: range < 40 (no discrimination) or correlation < 0.5 (random output)

  - name: check_t6_multi_actor_requirement
    purpose: Verify V6 — T6+ capabilities cannot score high with single actor
    status: pending
    priority: high
    method: |
      For pc_model_full_team, pc_help_other_ais, pc_ask_help_world, pc_relationship_depth_measurable, pc_global_relationships:
        Create profile: all brain maxed, but distinct_actors = 1, all other behavior signals strong
        Assert behavior_score < 30
      Fail conditions: any T6+ capability behavior_score >= 30 with single actor
```

---

## META-EVALUATION: FORMULA DESIGN QUALITY

Beyond individual checkers, these questions evaluate whether the formula DESIGN is sound:

### Q1: Do the formulas capture what the capability descriptions say?

For each capability, compare:
- The capability description from personhood_ladder.json
- The how_to_verify criteria
- The signals chosen in the formula

If the formula signals don't map to what the capability claims to measure, the formula is answering the wrong question.

### Q2: Are the signal weights defensible?

Each signal has a point allocation. The question: if you could ONLY see one signal, which would tell you most about this capability? That signal should have the highest weight. Verify this for each capability.

### Q3: Do brain and behavior components tell different stories?

The brain component should answer: "Is this citizen EQUIPPED for this relational capability?"
The behavior component should answer: "Does this citizen DEMONSTRATE this relational capability?"

If both components measure the same thing (e.g., both just count moments), the split adds no diagnostic value.

### Q4: Are recommendations actionable and structural?

Every recommendation should point to a specific structural change the citizen can make:
- Increase X (create more moments in Y type of space)
- Diversify Z (interact with more actors)
- Build W (create memory nodes about team members)

If a recommendation is vague ("be more connected"), it fails the actionability test.

---

## KNOWN GAPS

- All checkers pending — no runtime yet
- Cap calibration requires real citizen data (currently using educated estimates from synthetic profiles)
- Reciprocity signal validation requires longitudinal data — we don't yet know if high reciprocal_ratio actually correlates with relationships that humans would rate as "deep"
- Actor type distinction (human vs AI) is assumed but not yet verified in the universe graph schema
- The 50/50 split for pc_understand_human_deep and pc_relationship_style is a design hypothesis — needs validation against real scoring distributions

---

## MARKERS

<!-- @mind:todo Build check_synthetic_profiles first — validates all formula math -->
<!-- @mind:todo Design longitudinal reciprocity validation: track citizens over 30 days, compare reciprocity scores with human-rated relationship quality -->
<!-- @mind:todo Build check_volume_independence — critical V2 validation -->
<!-- @mind:proposition Automated regression: run all 55 synthetic profiles on every formula change to catch regressions -->
<!-- @mind:proposition Consider a "formula health dashboard" that shows score distributions across all Lumina Prime citizens per capability -->
