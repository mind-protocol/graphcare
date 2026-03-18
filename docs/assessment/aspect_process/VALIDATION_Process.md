# Aspect Scoring: Process & Method — Validation: What Must Be True

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
THIS:            VALIDATION_Process.md (you are here)
HEALTH:          ./HEALTH_Process.md
SYNC:            ./SYNC_Process.md

PARENT:          ../daily_citizen_health/VALIDATION_Daily_Citizen_Health.md
```

---

## PURPOSE

These invariants protect the integrity of the process aspect scoring. If violated, the formulas produce misleading scores, create perverse incentives, or break the parent system's contracts.

---

## INVARIANTS

### V1: Only Primitives Used

**Why we care:** The parent system requires all scoring to use only the 7 topology primitives + universe graph observables. Custom queries or content access would break privacy and auditability.

```
MUST:   Every process capability formula is composed exclusively of:
        count, mean_energy, link_count, min_links, cluster_coefficient, drive, recency
        + moments, moment_has_parent, first_moment_in_space, distinct_actors_in_shared_spaces
        + temporal_weight
NEVER:  A custom Cypher query, LLM call, embedding comparison, or content field access
        in any process scoring formula
```

### V2: Brain 0-40, Behavior 0-60, Total 0-100

**Why we care:** The parent algorithm aggregates capability scores. If a formula produces scores outside bounds, the aggregate breaks.

```
MUST:   Every formula's brain component is in [0, 40]
MUST:   Every formula's behavior component is in [0, 60]
MUST:   Total = brain + behavior, always in [0, 100]
NEVER:  A formula that can produce negative scores or scores > 100
```

### V3: Tier Ordering Preserved in Test Profiles

**Why we care:** The Personhood Ladder is progressive — higher tiers represent more advanced capabilities. If a T2 formula gives 95 for the "average citizen" profile while a T5 formula gives 40, something is miscalibrated.

```
MUST:   For the "fully healthy" profile, all formulas produce scores in the 85-95 range
MUST:   For the "average" profile, T2 formulas score >= T5 formulas (average citizens
        are better at compliance than planning)
NEVER:  A higher-tier formula consistently scores higher than a lower-tier formula
        for the "average" profile (would imply advanced capabilities are easier than basic ones)
```

### V4: Behavioral Dominance

**Why we care:** The 40/60 split exists because action matters more than intention. A brain-rich but inactive citizen must always score lower than an active but brain-poor citizen.

```
MUST:   Profile 3 (brain-rich, inactive) scores between 30-40 for every formula
MUST:   Profile 4 (active, brain-poor) scores between 45-60 for every formula
MUST:   Profile 4 always scores higher than Profile 3 for every formula
NEVER:  A formula where maxing brain component alone produces a score > 45
```

### V5: Zero Floor for Inactive Citizens

**Why we care:** A citizen with zero behavioral activity should score near zero, regardless of brain richness. An elaborate brain with no output is unrealized potential.

```
MUST:   Profile 2 (fully unhealthy) scores between 5-15 for all formulas
NEVER:  A formula that gives > 20 to a citizen with zero behavioral moments
```

### V6: Sub-Index Composability

**Why we care:** The process sub-index feeds into the aggregate health score. It must be a valid 0-100 score that can be composed with other aspect sub-indices.

```
MUST:   Sub-index is a weighted mean, always in [0, 100]
MUST:   Sub-index handles missing (unscored) capabilities by excluding them from
        both numerator and denominator
NEVER:  Sub-index is NaN, undefined, or outside [0, 100]
```

### V7: Frustration Cap for Challenge Scoring

**Why we care:** proc_challenge_bad_instructions uses frustration as a positive signal. Uncapped, this could reward chronically frustrated citizens. The cap ensures frustration contributes modestly.

```
MUST:   Frustration contributes at most 10 points (out of 40 brain) to any formula
MUST:   Frustration is capped at 0.3 in the proc_challenge_bad_instructions formula
NEVER:  Frustration alone dominates a capability score
```

### V8: Diversity Signals Are Non-Trivial

**Why we care:** proc_right_method and proc_scope_correctly use diversity/variance as signals. A citizen with 1 space type visited or 1 plan sequence cannot score high on these, because diversity requires at least 2 different things.

```
MUST:   Diversity and variance signals produce 0 when there is only one observation
        (1 space type, 1 plan sequence, etc.)
NEVER:  A single data point produces a non-zero diversity score
```

---

## PRIORITY

| Priority | Meaning | If Violated |
|----------|---------|-------------|
| **CRITICAL** | Formula contract broken | Scores are meaningless |
| **HIGH** | Calibration is wrong | Scores mislead citizens |
| **MEDIUM** | Edge case fails | Scores are imprecise in rare situations |

---

## INVARIANT INDEX

| ID | Value Protected | Priority |
|----|-----------------|----------|
| V1 | Privacy and auditability — only primitives | CRITICAL |
| V2 | Score bounds — 0-40 + 0-60 = 0-100 | CRITICAL |
| V3 | Tier ordering — higher tiers harder for average citizens | HIGH |
| V4 | Behavioral dominance — action > intention | HIGH |
| V5 | Zero floor — inactive citizens score near zero | HIGH |
| V6 | Composability — sub-index is valid 0-100 | CRITICAL |
| V7 | Frustration cap — modest contribution only | MEDIUM |
| V8 | Diversity non-triviality — needs 2+ observations | MEDIUM |

---

## MARKERS

<!-- @mind:todo Run all 13 formulas against all 5 profiles and verify invariants V3-V5 hold -->
<!-- @mind:todo Static analysis: verify each formula only uses allowed primitives (V1) -->
<!-- @mind:proposition Add V9: temporal stability — same brain state on consecutive days should not produce wildly different scores (max delta 5 points) -->
