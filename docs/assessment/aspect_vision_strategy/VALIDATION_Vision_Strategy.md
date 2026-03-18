# Vision & Strategy — Validation: What Must Be True

```
STATUS: DESIGNING
CREATED: 2026-03-13
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Vision_Strategy.md
PATTERNS:        ./PATTERNS_Vision_Strategy.md
ALGORITHM:       ./ALGORITHM_Vision_Strategy.md
THIS:            VALIDATION_Vision_Strategy.md (you are here)
HEALTH:          ./HEALTH_Vision_Strategy.md
SYNC:            ./SYNC_Vision_Strategy.md

PARENT:          ../daily_citizen_health/VALIDATION_Daily_Citizen_Health.md
```

---

## PURPOSE

These invariants protect the integrity of Vision & Strategy scoring. If violated, the formulas either invade privacy, produce nonsensical scores, or fail to distinguish visionary citizens from task-grinders.

All parent invariants (V1-V7 in Daily Citizen Health) apply here unconditionally. This document adds aspect-specific invariants.

---

## INVARIANTS

### VS1: Formulas Use Only Primitives

**Why we care:** This inherits from the parent V5 but is restated because high-tier formulas are more tempting to over-engineer. No custom graph queries. No LLM calls. No embedding comparisons.

```
MUST:   Every sub-component in every formula uses exactly one of:
        count, mean_energy, link_count, min_links, cluster_coefficient, drive, recency
        (brain) or moments, moment_has_parent, temporal_weight, spaces_created,
        distinct_actors (universe)
NEVER:  A derived metric that bypasses primitives or introduces new data sources
```

### VS2: Brain Score Never Exceeds 40

**Why we care:** The 40/60 split is the parent algorithm's core design decision. Vision is brain-heavy in nature, but the scoring must respect the split. A citizen with perfect brain topology and zero action does not score above 40.

```
MUST:   brain_score <= 40 for every capability formula
MUST:   Sum of brain sub-component weights = 40 exactly
NEVER:  A formula where brain-only score exceeds 40
```

### VS3: Behavior Score Never Exceeds 60

**Why we care:** Symmetric with VS2.

```
MUST:   behavior_score <= 60 for every capability formula
MUST:   Sum of behavior sub-component weights = 60 exactly
NEVER:  A formula where behavior-only score exceeds 60
```

### VS4: Higher Tiers Have Higher Ceilings

**Why we care:** A T8 capability must be harder to max out than a T5 capability. If the ceilings are the same, a citizen who masters T5 automatically scores well on T8 — which defeats the tier system.

```
MUST:   For any comparable sub-component (e.g., narrative_concept_lk),
        the ceiling at tier N+1 >= the ceiling at tier N
EXAMPLE: vis_define_vision concept ceiling = 15
         vis_strategic_thinking concept ceiling = 25
         vis_civilizational concept ceiling = 40
NEVER:  A T8 ceiling that is lower than or equal to its T5 counterpart
```

### VS5: Tier Progression Is Monotonic

**Why we care:** A citizen who scores well on vis_civilizational (T8) should necessarily score well on vis_define_vision (T5). The formulas must ensure that the signals required for higher tiers are supersets of those required for lower tiers.

```
MUST:   A synthetic profile scoring 80+ on vis_civilizational also scores 80+ on vis_define_vision
MUST:   A profile scoring 80+ on vis_sized_ambitions also scores 70+ on vis_define_vision
NEVER:  A profile scoring high on T8 but low on T5 (structural impossibility check)
```

### VS6: Isolation Caps Org and Civ Scores

**Why we care:** A citizen working alone cannot have organizational or civilizational vision. The behavioral component for vis_org_vision and vis_civilizational must enforce this structurally.

```
MUST:   If distinct_actors <= 1, vis_org_vision behavior_score < 30 (of 60)
MUST:   If distinct_actors <= 2, vis_civilizational behavior_score < 25 (of 60)
NEVER:  A solo citizen scoring above 70 total on vis_org_vision or vis_civilizational
```

### VS7: Empty Brain Caps Total Score

**Why we care:** A citizen with zero narrative nodes cannot have vision, no matter how active they are behaviorally. Pure execution without any articulated vision should not score high on this aspect.

```
MUST:   If narrative_count = 0, brain_score < 10 for all 5 capabilities
MUST:   If narrative_count = 0 AND hub_narratives = 0 AND deep_hub_narratives = 0,
        total score < 60 for all 5 capabilities (behavior maxes at 60, brain near 0)
NEVER:  A citizen with zero narrative nodes scoring 70+ on any vision capability
```

### VS8: Decay Catches Stagnation

**Why we care:** A citizen who wrote a vision document 6 months ago and never revisited it is not a visionary. Recency and energy decay must bring the score down over time.

```
MUST:   A profile with narrative_recency=0 and narrative_energy=0.1
        (old, decaying vision) scores at least 20 points less on vis_define_vision
        than the same profile with recency=0.9 and energy=0.8
NEVER:  Stale vision scores as well as fresh vision
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
| VS1 | Primitives only — no escape hatches | CRITICAL |
| VS2 | Brain score capped at 40 | CRITICAL |
| VS3 | Behavior score capped at 60 | CRITICAL |
| VS4 | Higher tiers harder to max | HIGH |
| VS5 | Tier progression is monotonic | HIGH |
| VS6 | Isolation caps org/civ scores | HIGH |
| VS7 | Empty brain caps total | HIGH |
| VS8 | Decay catches stagnation | MEDIUM |

---

## MARKERS

<!-- @mind:todo Run VS5 monotonicity check against all 5 synthetic profiles -->
<!-- @mind:todo Run VS6 isolation check: compute vis_org_vision for single-actor profile -->
<!-- @mind:todo Run VS7 empty-brain check: compute all 5 capabilities with narrative_count=0 -->
<!-- @mind:proposition Consider VS9: sub-index stability — small input changes should not cause large score swings -->
