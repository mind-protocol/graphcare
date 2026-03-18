# Collective Participation — Validation: What Must Be True

```
STATUS: DESIGNING
CREATED: 2026-03-13
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Collective_Participation.md
PATTERNS:        ./PATTERNS_Collective_Participation.md
ALGORITHM:       ./ALGORITHM_Collective_Participation.md
THIS:            VALIDATION_Collective_Participation.md (you are here)
HEALTH:          ./HEALTH_Collective_Participation.md
SYNC:            ./SYNC_Collective_Participation.md

PARENT:          ../daily_citizen_health/VALIDATION_Daily_Citizen_Health.md
```

---

## PURPOSE

These invariants protect the integrity of Collective Participation scoring. If violated, the formulas either invade privacy, produce nonsensical scores, or fail to distinguish active collective participants from passive inhabitants.

All parent invariants (V1-V7 in Daily Citizen Health) apply here unconditionally. This document adds aspect-specific invariants.

---

## INVARIANTS

### CP1: Formulas Use Only Primitives

**Why we care:** This inherits from the parent V5 but is restated because the behavioral component of this aspect is complex (dialogue chains, pioneered spaces, triggered moments). The temptation to add custom graph queries is high. No custom queries. No LLM calls. No content inspection.

```
MUST:   Every sub-component in every formula uses exactly one of:
        count, mean_energy, link_count, min_links, cluster_coefficient, drive, recency
        (brain) or moments, moment_has_parent, first_moment_in_space,
        distinct_actors_in_shared_spaces, temporal_weight (universe)
NEVER:  A derived metric that bypasses primitives or introduces new data sources
```

### CP2: Brain Score Never Exceeds 40

**Why we care:** The 40/60 split is the parent algorithm's core design decision. Even though collective participation is the most behavior-heavy aspect, the brain score must respect the ceiling. A citizen with perfect brain signals and zero collective action does not score above 40.

```
MUST:   brain_score <= 40 for every capability formula
MUST:   Sum of brain sub-component weights = 40 exactly
NEVER:  A formula where brain-only score exceeds 40
```

### CP3: Behavior Score Never Exceeds 60

**Why we care:** Symmetric with CP2.

```
MUST:   behavior_score <= 60 for every capability formula
MUST:   Sum of behavior sub-component weights = 60 exactly
NEVER:  A formula where behavior-only score exceeds 60
```

### CP4: Higher Tiers Have Higher Ceilings

**Why we care:** T8 must be harder to max out than T5. The ceiling escalation pattern is the structural guarantee that a citizen scoring well on T8 is demonstrating more than one scoring well on T5.

```
MUST:   For comparable sub-components, the ceiling at higher tier >= ceiling at lower tier
EXAMPLE: col_dao_participation distinct_actors ceiling = 5
         col_movement_builder distinct_actors ceiling = 8
         col_global_movement distinct_actors ceiling = 15
MUST:   col_global_movement pioneered_w ceiling (6.0) > col_movement_builder (4.0)
MUST:   col_global_movement triggered_w ceiling (15.0) > col_movement_builder (8.0)
NEVER:  A T8 ceiling that is lower than or equal to its T5 or T7 counterpart
```

### CP5: Isolation Caps All Scores

**Why we care:** A citizen with zero collective engagement cannot participate collectively by definition. This is even stronger here than in other aspects: collective participation WITHOUT others is logically impossible.

```
MUST:   If distinct_actors = 0, behavior_score < 15 for all 4 capabilities
MUST:   If distinct_actors <= 1, total score < 50 for col_dao_participation and col_community_engagement
MUST:   If distinct_actors <= 2, total score < 40 for col_movement_builder
MUST:   If distinct_actors <= 3, total score < 35 for col_global_movement
NEVER:  A citizen with distinct_actors = 0 scoring above 45 total on any capability
        (only brain component + minimal behavior residual)
```

### CP6: Zero Collective Moments Caps Behavior Score

**Why we care:** If a citizen has zero moments in governance, discussion, or forum spaces, the behavior component for participation capabilities must be near zero. Activity in private or non-collective spaces does not count.

```
MUST:   If collective_w = 0, behavior_score < 10 for col_dao_participation
MUST:   If collective_w = 0, behavior_score < 10 for col_community_engagement
MUST:   If pioneered_w = 0 AND triggered_w = 0, behavior_score < 20
        for col_movement_builder (remaining points from distinct_actors + collective_w only)
NEVER:  A citizen with zero collective moments scoring 60+ total on any capability
```

### CP7: Movement Building Requires Creation

**Why we care:** col_movement_builder (T7) and col_global_movement (T8) explicitly require creating structures, not just participating in them. A citizen with high participation but zero pioneered spaces must score low on T7/T8.

```
MUST:   If pioneered_w = 0, col_movement_builder behavior_score < 25
        (only triggered_w + distinct_actors + collective_w sub-components)
MUST:   If pioneered_w = 0 AND actors_in_pioneered = 0,
        col_global_movement behavior_score < 20
NEVER:  A pure participant (zero pioneered spaces) scoring 65+ on col_movement_builder
```

### CP8: Dialogue Ratio Rewards Reciprocity

**Why we care:** A citizen whose collective moments are 100% broadcasts (zero dialogue) is not genuinely participating. The dialogue_ratio sub-component ensures that one-way communication doesn't score as well as two-way engagement.

```
MUST:   If dialogue_ratio = 0, the dialogue sub-component contributes 0 to behavior score
MUST:   The dialogue sub-component is weighted at least 15 points in T5 formulas
        (significant enough that zero dialogue creates a visible gap)
CHECK:  A citizen with gov_w=8.0 and dialogue_ratio=0 scores at least 15 points less
        on col_dao_participation than the same citizen with dialogue_ratio=0.4
```

### CP9: Temporal Decay Catches Withdrawal

**Why we care:** A citizen who was active in governance six months ago but has withdrawn is not currently participating. All behavior stats use temporal_weight, and concept_recency captures brain staleness.

```
MUST:   A profile with all moments older than 30 days (low temporal weights)
        scores at least 25 points less than the same profile with recent moments
NEVER:  Historical participation scoring as well as current participation
```

---

## PRIORITY

| Priority | Meaning | If Violated |
|----------|---------|-------------|
| **CRITICAL** | Scoring purpose fails | Formulas are meaningless |
| **HIGH** | Major value lost | Scores misleading |
| **MEDIUM** | Partial value lost | Scores imprecise |

---

## INVARIANT INDEX

| ID | Value Protected | Priority |
|----|-----------------|----------|
| CP1 | Primitives only — no escape hatches | CRITICAL |
| CP2 | Brain score capped at 40 | CRITICAL |
| CP3 | Behavior score capped at 60 | CRITICAL |
| CP4 | Higher tiers harder to max | HIGH |
| CP5 | Isolation caps all scores | HIGH |
| CP6 | Zero collective moments caps behavior | HIGH |
| CP7 | Movement building requires creation | HIGH |
| CP8 | Dialogue ratio rewards reciprocity | MEDIUM |
| CP9 | Temporal decay catches withdrawal | MEDIUM |

---

## MARKERS

<!-- @mind:todo Run CP5 isolation check: compute all 4 capabilities with distinct_actors=0 -->
<!-- @mind:todo Run CP6 zero-moments check: compute all 4 capabilities with collective_w=0 -->
<!-- @mind:todo Run CP7 creation check: compute col_movement_builder and col_global_movement with pioneered_w=0 -->
<!-- @mind:todo Run CP8 dialogue check: compare col_dao_participation with dialogue_ratio=0 vs. dialogue_ratio=0.4 -->
<!-- @mind:proposition Consider CP10: sub-index stability — small input changes should not cause large score swings -->
