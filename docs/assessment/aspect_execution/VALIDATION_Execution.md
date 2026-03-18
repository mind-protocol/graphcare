# Execution Quality Aspect — Validation: What Must Be True

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Execution.md
PATTERNS:        ./PATTERNS_Execution.md
ALGORITHM:       ./ALGORITHM_Execution.md
THIS:            VALIDATION_Execution.md (you are here)
HEALTH:          ./HEALTH_Execution.md
SYNC:            ./SYNC_Execution.md

PARENT CHAIN:    ../daily_citizen_health/VALIDATION_Daily_Citizen_Health.md
SPEC:            ../../specs/personhood_ladder.json (aspect="execution")
IMPL:            @mind:TODO
```

---

## PURPOSE

These invariants protect the integrity of execution quality scoring. If violated, scores are misleading, formulas are unauditable, or the tier progression breaks down. Parent invariants (V1-V7 in Daily Citizen Health) apply here automatically — these are ADDITIONAL invariants specific to execution scoring.

---

## INVARIANTS

### VE1: Formulas Use Only Declared Primitives

**Why we care:** If a formula sneaks in a custom query or undeclared data source, it becomes unauditable and may violate privacy.

```
MUST:   Every sub-component in every scoring formula uses only:
        Brain: count, mean_energy, link_count, min_links, cluster_coefficient, drive, recency
        Universe: moments, moment_has_parent, temporal_weight
        Plus derived stats computed exclusively from the above
NEVER:  A formula that calls a custom graph query, reads content, or uses an undeclared data source
```

### VE2: Brain Component Bounded 0-40, Behavior Component Bounded 0-60

**Why we care:** The 40/60 split is a canonical design decision. If a formula can exceed these bounds, the brain/behavior balance is broken.

```
MUST:   For every capability: 0 <= brain_score <= 40 AND 0 <= behavior_score <= 60
NEVER:  A formula where brain_score can exceed 40 or behavior_score can exceed 60
        (Verify: all sub-component points within a component sum to exactly the component max)
```

### VE3: Total Score Bounded 0-100

**Why we care:** Scores are compared across capabilities and aspects. Unbounded scores break comparisons.

```
MUST:   For every capability: 0 <= total <= 100
NEVER:  A score below 0 or above 100 under any input combination
```

### VE4: Sub-Component Points Sum to Component Max

**Why we care:** If points don't add up, there are hidden points or missing points.

```
MUST:   For each capability:
        sum(brain sub-component max points) == 40
        sum(behavior sub-component max points) == 60
NEVER:  A capability where sub-component points sum to more or less than the component max
```

### VE5: Tier Progression Is Monotonically Harder

**Why we care:** T1 capabilities must be achievable by any functioning citizen. T8 must require exceptional sustained behavior. If a T1 formula is harder to score on than a T5 formula, the tier system is meaningless.

```
MUST:   For the same synthetic "average citizen" profile, T1 scores >= T5 scores >= T8 scores
        (formulas reflect increasing difficulty by tier)
NEVER:  A lower-tier formula that produces lower scores than a higher-tier formula for the same input
```

### VE6: Zero Input Produces Zero Score

**Why we care:** A citizen with no brain topology and no behavioral moments should score 0, not some positive baseline.

```
MUST:   When all primitives return 0 (empty brain, no moments): every capability score == 0
NEVER:  A formula that produces a positive score from zero input
```

### VE7: Ceiling Values Are Documented

**Why we care:** Every `cap(x, ceiling)` is a calibration point. If ceilings are undocumented, calibration is impossible.

```
MUST:   Every cap() call in every formula has its ceiling value documented in the formula table
NEVER:  A cap() call with an undocumented or magic-number ceiling
```

### VE8: Example Calculations Are Correct

**Why we care:** Examples serve as human-readable tests. Wrong examples create false understanding.

```
MUST:   Every example calculation in ALGORITHM produces the correct result when computed manually
NEVER:  An example where the numbers don't add up (brain + behavior != total, or sub-components don't sum)
```

### VE9: Aspect Sub-Index Uses All Scored Capabilities

**Why we care:** If the sub-index silently drops a capability, the aggregate is misleading.

```
MUST:   The aspect sub-index includes every capability that has scored=true
NEVER:  A scored capability excluded from the aggregate, or an unscored capability included
```

### VE10: No Cross-Aspect Data Leakage

**Why we care:** Execution formulas should score execution, not initiative or communication. Using signals that belong to other aspects makes the score ambiguous.

```
MUST:   Formulas focus on execution-relevant signals: process nodes, verification, corrections, quality
NEVER:  A formula that primarily scores initiative (proposals_w), communication (response patterns),
        or other aspect-specific signals
```

---

## PRIORITY

| Priority | Meaning | If Violated |
|----------|---------|-------------|
| **CRITICAL** | Score integrity fails | Scores are meaningless |
| **HIGH** | Score quality degrades | Scores exist but mislead |
| **MEDIUM** | Calibration suffers | Scores work but are imprecise |

---

## INVARIANT INDEX

| ID | Value Protected | Priority |
|----|-----------------|----------|
| VE1 | Auditability — only declared primitives | CRITICAL |
| VE2 | Balance — 40/60 split respected | CRITICAL |
| VE3 | Boundedness — scores in 0-100 | CRITICAL |
| VE4 | Completeness — sub-component points sum correctly | HIGH |
| VE5 | Progression — tiers get harder monotonically | HIGH |
| VE6 | Zero baseline — empty input = zero score | HIGH |
| VE7 | Transparency — all ceilings documented | MEDIUM |
| VE8 | Correctness — examples compute accurately | MEDIUM |
| VE9 | Aggregation — all scored capabilities included | HIGH |
| VE10 | Separation — no cross-aspect leakage | MEDIUM |

---

## VERIFICATION MATRIX

How to verify each invariant:

| ID | Verification Method |
|----|---------------------|
| VE1 | Static analysis: parse each formula, verify all referenced functions are in the declared primitive set |
| VE2 | Arithmetic check: sum max points of brain sub-components = 40, behavior = 60, for each capability |
| VE3 | Follows from VE2 + VE4: if components are bounded and sum correctly, total is bounded |
| VE4 | Table audit: for each capability table, sum the "Points" column per component |
| VE5 | Synthetic test: run all formulas with "average citizen" profile, verify tier ordering |
| VE6 | Boundary test: run all formulas with all-zero input, verify all scores = 0 |
| VE7 | Document scan: every `cap(x, N)` in ALGORITHM has N explained in the formula table |
| VE8 | Manual recomputation: follow each example step by step, verify arithmetic |
| VE9 | Code audit: verify sub-index loop includes all `scored=true` capabilities |
| VE10 | Design review: for each formula, verify the signals are execution-relevant, not aspect-foreign |

---

## MARKERS

<!-- @mind:todo Build automated VE1 checker (static analysis of formula code) -->
<!-- @mind:todo Run VE6 zero-input test against all 14 formulas -->
<!-- @mind:todo Run VE5 monotonicity test with synthetic profiles -->
<!-- @mind:proposition Consider VE11: determinism — same input always produces same score (no randomness) -->
