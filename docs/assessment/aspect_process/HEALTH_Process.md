# Aspect Scoring: Process & Method — Health: Meta-Evaluation of Formulas

```
STATUS: DESIGNING
CREATED: 2026-03-13
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Process.md
PATTERNS:        ./PATTERNS_Process.md
ALGORITHM:       ./ALGORITHM_Process.md
VALIDATION:      ./VALIDATION_Process.md
THIS:            HEALTH_Process.md (you are here)
SYNC:            ./SYNC_Process.md

PARENT:          ../daily_citizen_health/HEALTH_Daily_Citizen_Health.md
```

---

## WHEN TO USE HEALTH (NOT TESTS)

| Use Health For | Why |
|----------------|-----|
| Formula calibration against synthetic profiles | Ensures formulas produce expected ranges |
| Primitive-only audit on each formula | Privacy violation = trust collapse |
| Score distribution analysis across real citizens | Detects degenerate formulas (all citizens get 50) |
| Tier ordering verification | Higher-tier formulas should be harder for average citizens |

---

## PURPOSE OF THIS FILE

Verifies that the 13 process capability scoring formulas are well-calibrated, use only allowed primitives, produce meaningful score distributions, and create correct tier ordering. This is the meta-evaluation layer — it evaluates the formulas themselves, not the citizens they score.

**Boundaries:** This verifies the FORMULAS (are they well-designed?). It does NOT verify the daily runner (that's the parent HEALTH file) or the Personhood Ladder definitions (that's the personhood_ladder chain).

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: primitive_compliance
    priority: high
    rationale: If a formula accesses content or uses custom queries, privacy is broken.

  - name: score_bounds
    priority: high
    rationale: If a formula can produce scores outside [0, 100], aggregation breaks.

  - name: profile_calibration
    priority: high
    rationale: If formulas don't match expected ranges for synthetic profiles, they're miscalibrated.

  - name: tier_ordering
    priority: med
    rationale: If T2 formulas are harder than T5 for average citizens, the ladder is inverted.

  - name: behavioral_dominance
    priority: med
    rationale: Profile 4 (active, brain-poor) must always outscore Profile 3 (brain-rich, inactive).

  - name: distribution_health
    priority: med
    rationale: If all citizens get the same score, the formula is degenerate and useless.

  - name: temporal_stability
    priority: low
    rationale: Same brain state on consecutive days shouldn't swing more than 5 points.
```

---

## CHECKER INDEX

```yaml
checkers:
  - name: check_primitive_compliance
    purpose: Static analysis — verify each formula uses only allowed primitives (V1)
    method: |
      For each of the 13 formulas:
        1. Extract all data access calls
        2. Verify each call is one of: count, mean_energy, link_count, min_links,
           cluster_coefficient, drive, recency, moments, moment_has_parent,
           first_moment_in_space, distinct_actors_in_shared_spaces, temporal_weight
        3. FAIL if any other data access found
    status: pending
    priority: high

  - name: check_score_bounds
    purpose: Verify brain in [0,40], behavior in [0,60], total in [0,100] for all formulas (V2)
    method: |
      For each of the 13 formulas:
        1. Run formula with all-zero inputs → verify total >= 0
        2. Run formula with all-max inputs → verify brain <= 40, behavior <= 60, total <= 100
        3. Run formula with 100 random input combinations → verify bounds hold
    status: pending
    priority: high

  - name: check_profile_calibration
    purpose: Verify all formulas produce expected ranges for 5 synthetic profiles (V3, V4, V5)
    method: |
      For each of the 13 formulas, for each of the 5 profiles:
        1. Compute score
        2. Verify score is within expected range:
           - Profile 1 (healthy): 85-95
           - Profile 2 (unhealthy): 5-15
           - Profile 3 (brain-rich, inactive): 30-40
           - Profile 4 (active, brain-poor): 45-60
           - Profile 5 (average): 50-70
        3. FAIL if any score outside expected range
    status: pending
    priority: high

  - name: check_tier_ordering
    purpose: Verify tier ordering for average profile (V3)
    method: |
      Compute all 13 scores for Profile 5 (average):
        1. Group by tier
        2. Compute mean score per tier
        3. Verify: mean(T2) >= mean(T3) >= mean(T4) >= mean(T5) >= mean(T6) >= mean(T7) >= mean(T8)
        4. FAIL if ordering is violated
      Note: T7/T8 may score very low for average citizens — this is expected.
    status: pending
    priority: med

  - name: check_behavioral_dominance
    purpose: Verify Profile 4 always outscores Profile 3 (V4)
    method: |
      For each of the 13 formulas:
        1. Compute score for Profile 3 (brain-rich, inactive)
        2. Compute score for Profile 4 (active, brain-poor)
        3. Verify: score_profile_4 > score_profile_3
        4. FAIL if any formula violates this
    status: pending
    priority: med

  - name: check_distribution_health
    purpose: Verify formulas produce meaningful variance across a population
    method: |
      Generate 50 randomized citizen profiles with varied brain and behavior stats.
      For each of the 13 formulas:
        1. Compute scores for all 50 citizens
        2. Compute standard deviation
        3. Verify stdev > 10 (on a 0-100 scale)
        4. FAIL if stdev < 10 (formula is degenerate — doesn't differentiate citizens)
      Also check:
        - No formula produces the same score for > 30% of citizens (clustering)
        - Score distribution covers at least 60% of the 0-100 range
    status: pending
    priority: med

  - name: check_temporal_stability
    purpose: Verify same brain state produces stable scores across days
    method: |
      For each of the 13 formulas:
        1. Create a fixed brain profile
        2. Create a behavior profile that shifts slightly (moments age by 24h)
        3. Compute scores for day N and day N+1
        4. Verify: |score_N - score_N+1| < 5
        5. FAIL if delta exceeds 5 for any formula
      Exception: behavior-heavy formulas may legitimately shift if a burst of activity
      enters or leaves the temporal window. Acceptable delta: 8 for these cases.
    status: pending
    priority: low
```

---

## FORMULA-SPECIFIC HEALTH CONCERNS

### proc_right_method — Diversity Proxy Risk

**Concern:** Space type diversity is used as a proxy for method diversity. But a citizen could visit many space types while using the same method (e.g., "just code everything" in repo, docs, and other spaces).

**Mitigation:** Brain component (40%) checks for actual process node diversity. If the citizen has diverse space activity but no process nodes, brain score is low, capping the total at ~60.

**Health check:** Verify that Profile 4 (active, brain-poor) scores 45-60, not 70+.

### proc_scope_correctly — Variance Instability

**Concern:** Sequence length variance can be noisy with few sequences. A citizen with 2 sequences of lengths 1 and 10 gets high variance; one with 2 sequences of lengths 5 and 6 gets low variance. Both could be correctly scoping.

**Mitigation:** Combined with plan_sequences_w and isolated_ratio for triangulation. Variance alone is only 25/60 of the behavior component.

**Health check:** Run 100 random profiles with 2-3 sequences. Verify variance score doesn't dominate the behavior component.

### proc_challenge_bad_instructions — Rewarding Friction

**Concern:** Could reward contrarian citizens who challenge everything, not just bad instructions.

**Mitigation:** Escalation cap is low (2 weighted). Proposal follow-through (15 points) ensures challenges are constructive. Brain frustration is capped at 10 points.

**Health check:** Create a "serial contrarian" profile (high escalations_w=10, low proposal_follow_ratio=0.1). Verify total score is below 60 (contrarian without constructive proposals should not score well).

### proc_prioritize_autonomously — Impact Proxy Risk

**Concern:** "High-energy desire action ratio" assumes desire energy correlates with importance. But a citizen could have high-energy desires for trivial things.

**Mitigation:** Desire energy is set by brain physics, not by the citizen's self-assessment. High-energy desires are those that have been reinforced through action and feedback — making energy a reasonable proxy for importance.

**Health check:** Verify the formula is sensitive to the ratio, not just to absolute counts. A citizen with 10 moments on high-energy desires and 10 on low-energy ones should score differently from one with 18 on high and 2 on low.

### proc_movement_scale_projects (T8) — Quantity Over Quality

**Concern:** The formula rewards many spaces, many actors, and high activity. A citizen who creates 10 empty spaces and has superficial interactions with 15 actors could score well without genuine movement-scale impact.

**Mitigation:** Self-initiated sequences in new spaces (15 points) requires follow-through. But the formula cannot assess qualitative significance — this is an acknowledged limitation.

**Health check:** Create a "superficial scaler" profile (many spaces, many actors, low plan_sequences). Verify score is below 70.

---

## KNOWN GAPS

- All checkers pending — no runtime yet, no real citizen data
- Derived stats (plan_sequences_w, concurrent_moments_w, sequence_lengths) need exact detection algorithms before formulas can be implemented
- Real-world calibration is impossible until citizens exist in Lumina Prime — current calibration is purely theoretical based on synthetic profiles
- Cross-formula correlation analysis not yet defined (do formulas that should be independent actually produce independent scores?)

---

## MARKERS

<!-- @mind:todo Build check_primitive_compliance first — most critical, can be done as static analysis of formula code -->
<!-- @mind:todo Design exact algorithms for plan_sequences_w and concurrent_moments_w detection from raw timestamps -->
<!-- @mind:todo Create the "serial contrarian" test profile and verify proc_challenge_bad_instructions handles it correctly -->
<!-- @mind:proposition When real citizen data exists, run distribution_health checker and recalibrate caps that produce degenerate distributions -->
<!-- @mind:proposition Consider cross-formula correlation analysis: if proc_commit_push and proc_continue_plan are >0.95 correlated, one may be redundant -->
