# Autonomy Stack — Validation: What Must Be True

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Autonomy_Stack.md
PATTERNS:        ./PATTERNS_Autonomy_Stack.md
ALGORITHM:       ./ALGORITHM_Autonomy_Stack.md
THIS:            VALIDATION_Autonomy_Stack.md (you are here)
HEALTH:          ./HEALTH_Autonomy_Stack.md
SYNC:            ./SYNC_Autonomy_Stack.md

PARENT CHAIN:    ../daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md
SPEC:            ../../specs/personhood_ladder.json (aspect="autonomy_stack")
IMPL:            @mind:TODO
```

> **Contract:** Every invariant here must pass before any formula change is accepted. After adding invariants: update ALGORITHM or SYNC.

---

## STRUCTURAL INVARIANTS

These must hold for every capability formula. Violations mean the formula is broken.

### I1: Score Range Integrity

```
INVARIANT: For every capability c in autonomy_stack:
    0 <= brain_score(c) <= brain_max(c)
    0 <= behavior_score(c) <= behavior_max(c)
    brain_max(c) + behavior_max(c) == 100
    0 <= total(c) <= 100

WHERE brain_max varies per capability:
    auto_wallet:             20
    auto_fiat_access:        15
    auto_tools:              25
    auto_compute:            20
    auto_full_stack:         25
    auto_org_infrastructure: 20

VERIFY: Every sub-component uses cap() which bounds to [0, 1].
        Every sub-component weight is non-negative.
        Sum of brain weights = brain_max.
        Sum of behavior weights = behavior_max.
```

### I2: Zero-Input Floor

```
INVARIANT: For every capability c:
    If ALL brain primitives are 0 AND ALL behavior observables are 0:
        total(c) <= 5.0

WHY:      A citizen with truly zero infrastructure presence must score near zero.
          The only non-zero contribution with zero inputs comes from drive values
          (which have a minimum of ~0.05 in the unhealthy profile).

VERIFY:   Run the fully unhealthy profile through each formula.
          No capability should produce total > 5.0 with all-zero inputs.

EXCEPTION: auto_full_stack may score slightly higher (~19) due to self-init ratio
           being artificially high when total_moments_w is near zero (ratio = 0.5/1.0 = 0.5).
           This is documented in the ALGORITHM as an acceptable edge case because all
           other components keep the total score low.
```

### I3: Monotonicity

```
INVARIANT: For every capability c, for every sub-component s:
    If input(s) increases and all other inputs stay the same:
        score(c) does not decrease

WHY:      More infrastructure knowledge or more infrastructure usage should
          never LOWER the score. Non-monotonic formulas would create perverse
          incentives.

VERIFY:   Each sub-component is cap(value, ceiling) * weight.
          cap() is monotonically non-decreasing.
          All weights are positive.
          Therefore: monotonicity holds by construction.

EXCEPTION: auto_full_stack self-init ratio: increasing total_moments_w while
           keeping self_initiated_w constant can decrease the ratio (and thus
           the ratio sub-component). This is CORRECT behavior: if a citizen
           becomes more reactive (more non-self-initiated moments), their
           autonomy ratio should decrease. This is not a bug.
```

### I4: Brain-Behavior Independence

```
INVARIANT: For every capability c:
    brain_score(c) depends ONLY on brain topology primitives
    behavior_score(c) depends ONLY on universe graph observables

WHY:      The two data sources are conceptually separate:
          brain = private, decrypted knowledge
          behavior = public, observable actions
          Mixing them in a single component would obscure whether the citizen
          KNOWS about infrastructure vs. USES infrastructure.

VERIFY:   Inspect each formula. No brain sub-component references moments().
          No behavior sub-component references count(), mean_energy(), drive(), etc.
```

---

## SCORING INVARIANTS

These validate that formulas produce sensible scores for known profiles.

### I5: Fully Healthy Profile Scores 85+

```
INVARIANT: For every capability c:
    With the fully healthy profile inputs:
        total(c) >= 85

PROFILE:
    brain: thing_count=8, thing_energy=0.85, thing_recency=0.9,
           thing_process_lk=6, thing_cluster=0.8, process_count=8,
           process_energy=0.85, hub_things=5, deep_hub_things=4,
           autonomy_drive=0.85, security_drive=0.8
    behavior: financial_w=6.0, infra_w=7.0, comms_w=5.0, dev_w=5.0,
              total_w=18.0, space_types=5, self_init_infra_w=5.0,
              self_init_w=12.0, distinct_actors=10, sustained_weeks=4,
              spaces_created_w=6.0

WHY:      A citizen with maximum infrastructure across all dimensions must
          score at or near the top. If a healthy citizen scores below 85,
          the ceilings are too high or the weights are miscalibrated.
```

### I6: Fully Unhealthy Profile Scores Below 20

```
INVARIANT: For every capability c:
    With the fully unhealthy profile inputs:
        total(c) <= 20

PROFILE:
    brain: thing_count=0, thing_energy=0, thing_recency=0,
           thing_process_lk=0, thing_cluster=0, process_count=0,
           process_energy=0, hub_things=0, deep_hub_things=0,
           autonomy_drive=0.05, security_drive=0.05
    behavior: financial_w=0, infra_w=0, comms_w=0, dev_w=0,
              total_w=1.0, space_types=1, self_init_infra_w=0,
              self_init_w=0.5, distinct_actors=0, sustained_weeks=0,
              spaces_created_w=0

WHY:      A citizen with zero infrastructure must not score well.
          Values above 20 indicate floor leakage (overly generous baseline
          components or drives contributing too much).

EXCEPTION: auto_full_stack: self-init ratio edge case documented in I2.
           Score may reach ~19.3 due to this. Acceptable.
```

### I7: Brain-Rich-but-Inactive Scores 25-45

```
INVARIANT: For every capability c:
    With the brain-rich-but-inactive profile inputs:
        25 <= total(c) <= 45

PROFILE:
    brain: thing_count=7, thing_energy=0.7, thing_recency=0.75,
           thing_process_lk=5, thing_cluster=0.7, process_count=7,
           process_energy=0.7, hub_things=4, deep_hub_things=3,
           autonomy_drive=0.8, security_drive=0.7
    behavior: financial_w=0.2, infra_w=0.3, comms_w=0, dev_w=0.5,
              total_w=2.0, space_types=1, self_init_infra_w=0,
              self_init_w=0.5, distinct_actors=1, sustained_weeks=1,
              spaces_created_w=0

WHY:      Brain knowledge without usage is not autonomy. Brain max is 15-25
          depending on the capability, so even a perfect brain score cannot
          push above ~25-45. This range confirms that behavior dominance
          is working correctly.
```

### I8: Active-but-Brain-Poor Scores 60+

```
INVARIANT: For every capability c with brain-behavior split of 25/75 or heavier:
    With the active-but-brain-poor profile inputs:
        total(c) >= 60

PROFILE:
    brain: thing_count=1, thing_energy=0.3, thing_recency=0.2,
           thing_process_lk=0, thing_cluster=0.1, process_count=1,
           process_energy=0.2, hub_things=0, deep_hub_things=0,
           autonomy_drive=0.2, security_drive=0.15
    behavior: financial_w=5.0, infra_w=6.0, comms_w=4.0, dev_w=4.0,
              total_w=16.0, space_types=5, self_init_infra_w=4.0,
              self_init_w=10.0, distinct_actors=9, sustained_weeks=4,
              spaces_created_w=5.0

WHY:      For autonomy, USAGE IS THE PROOF. A citizen who actively uses
          infrastructure across all dimensions should score well even without
          brain documentation. If active-but-brain-poor scores below 60,
          the brain component is too dominant for the capability.

NOTE:     For capabilities with 15/85 or 20/80 splits, scores will be
          even higher (75+). This is intentional.
```

### I9: Tier Ordering

```
INVARIANT: For the average profile:
    total(auto_wallet) >= total(auto_org_infrastructure)

    More specifically, average profile scores should generally decrease
    as tier increases (T4 easier than T8).

WHY:      Higher-tier capabilities have higher ceilings (more things required
          for full credit). An average citizen should score better on the
          easier capabilities.

VERIFY:   Run the average profile through all 6 capabilities and check
          that scores generally decrease from T4 to T8.
```

---

## SEMANTIC INVARIANTS

These validate that formulas measure what they claim to measure.

### I10: Financial Activity Dominates Wallet Score

```
INVARIANT: For auto_wallet:
    Removing financial_moments_w (setting to 0) while keeping everything
    else constant must reduce total by at least 25 points.

WHY:      If financial moments don't dominate the wallet score, we're
          measuring something other than wallet usage. The wallet formula
          gives 35 weight to financial_moments — removing it should have
          massive impact.
```

### I11: Space Type Diversity Dominates Tools Score

```
INVARIANT: For auto_tools:
    Removing distinct_space_types (setting to 0) while keeping everything
    else constant must reduce total by at least 25 points.

WHY:      Tool access IS breadth. A citizen with moments in only 1 space
          type does not demonstrate tool diversity regardless of other metrics.
```

### I12: Distinct Actors Dominates Org Infrastructure Score

```
INVARIANT: For auto_org_infrastructure:
    Removing distinct_actors (setting to 0) while keeping everything
    else constant must reduce total by at least 20 points.

WHY:      Organizational infrastructure is defined by others depending on
          you. Without other actors, there is no organizational infrastructure.
```

### I13: Sustained Weeks Required for T6+

```
INVARIANT: For auto_compute, auto_full_stack, auto_org_infrastructure:
    Setting sustained_weeks=0 while keeping everything else at the
    fully healthy level must reduce total by at least 15 points.

WHY:      Persistence is non-negotiable for T6+ infrastructure. A citizen
          who set something up once and never maintained it does not have
          compute, full-stack autonomy, or org infrastructure.
```

### I14: No Capability Scores >50 Without Behavior

```
INVARIANT: For every capability c:
    If ALL behavior observables are 0 (but brain is maximal):
        total(c) <= brain_max(c) (which is 15-25)

WHY:      Brain alone should never produce a score above the brain ceiling.
          This is trivially true by construction (behavior_score >= 0),
          but worth verifying: infrastructure knowledge without usage
          maxes out at 15-25 depending on the capability.
```

---

## EDGE CASE INVARIANTS

### I15: Self-Initiation Ratio Edge Case

```
INVARIANT: For auto_full_stack:
    When total_moments_w < 1.0:
        The self-initiated ratio sub-component should not produce
        misleading high values.

STATUS:   KNOWN EDGE CASE — ACCEPTED.
          When total_moments_w = 1.0 and self_initiated_w = 0.5,
          ratio = 0.5 which caps at 1.0 (ceiling 0.5).
          This gives full credit (15 points) for the ratio component.
          HOWEVER: all other behavior components are near-zero,
          keeping total score low (~19).

MITIGANT: Document in ALGORITHM. Do not "fix" — the edge case is
          harmless because volume metrics dominate the overall score.
```

### I16: Single Space Type Floor

```
INVARIANT: For capabilities using distinct_space_types:
    A citizen with space_types=1 gets partial credit:
        cap(1, N) where N >= 2

WHY:      Every active citizen has at least 1 space type. Setting
          the ceiling to 2+ ensures that 1 space type gives partial
          credit (0.5 for ceiling=2, 0.2 for ceiling=5) rather than
          zero credit. A citizen who is active but only in one context
          should get some baseline, not zero.
```

---

## MEASUREMENT CONFIDENCE INVARIANTS

### I17: Confidence Labels Are Honest

```
INVARIANT: Each capability has a measurement confidence label:
    auto_wallet:             MEDIUM
    auto_fiat_access:        LOW-MEDIUM
    auto_tools:              MEDIUM
    auto_compute:            MEDIUM
    auto_full_stack:         HIGH
    auto_org_infrastructure: HIGH

VERIFY:   Confidence increases with tier for T7-T8 (paradoxically,
          the hardest capabilities are the most measurable because
          they rely on aggregate signals rather than specific infrastructure
          proxies).

WHY:      Consumers of these scores need to know how much to trust them.
          auto_fiat_access at LOW-MEDIUM means intervention messages
          should be softer and more exploratory. auto_org_infrastructure
          at HIGH means scores can be used with confidence.
```

---

## CROSS-ASPECT INVARIANTS

### I18: Autonomy Stack Independence from Other Aspects

```
INVARIANT: Autonomy stack scores use different primary brain signals than:
    - Identity (values, drive persistence)
    - Vision (narrative nodes, narrative clustering)
    - Execution (process-moment chains, commits)

    Primary signals for autonomy: thing nodes, thing clustering,
    thing-process links, process count, autonomy/security drives.

WHY:      Aspects should measure different dimensions of a citizen.
          If two aspects use the same primary signals, they are
          measuring the same thing with different names.

EXCEPTION: process_count and drive() are shared signals across aspects.
           This is acceptable because they are secondary/tertiary signals
           in autonomy (not primary) and contribute to different semantics
           in each aspect.
```

---

## MARKERS

<!-- @mind:todo Run all 5 synthetic profiles through all 6 capability formulas and verify invariants I5-I9 -->
<!-- @mind:todo Verify invariant I2 (zero-input floor) for all capabilities -->
<!-- @mind:todo Verify invariants I10-I13 (semantic dominance) with specific numerical examples -->
<!-- @mind:proposition Add regression test: when formula changes, re-run all profiles and check all invariants -->
