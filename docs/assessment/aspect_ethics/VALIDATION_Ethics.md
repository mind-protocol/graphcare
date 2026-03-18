# Ethics Aspect — Validation: What Must Be True

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Ethics.md
PATTERNS:        ./PATTERNS_Ethics.md
ALGORITHM:       ./ALGORITHM_Ethics.md
THIS:            VALIDATION_Ethics.md (you are here)
HEALTH:          ./HEALTH_Ethics.md
SYNC:            ./SYNC_Ethics.md

PARENT:          ../daily_citizen_health/VALIDATION_Daily_Citizen_Health.md
```

---

## PURPOSE

These invariants protect the integrity of Ethics scoring. If violated, the formulas either invade privacy, produce nonsensical scores, allow topology-based moral judgment that exceeds what topology can measure, or fail to distinguish ethical citizens from disengaged ones.

All parent invariants (in Daily Citizen Health VALIDATION) apply here unconditionally. This document adds aspect-specific invariants.

---

## INVARIANTS

### ET1: Formulas Use Only Primitives

**Why we care:** Ethics scoring is the aspect most tempting to over-engineer. The urge to "peek at content" to judge moral quality is strong. If a formula sneaks in a custom query, content read, or LLM call, it violates both privacy and the honesty guarantee.

```
MUST:   Every sub-component in every formula uses exactly one of:
        count, mean_energy, link_count, min_links, cluster_coefficient, drive, recency
        (brain) or moments, moment_has_parent, first_moment_in_space,
        distinct_actors_in_shared_spaces, temporal_weight (universe)
NEVER:  A custom Cypher query, LLM call, embedding comparison, content field access,
        synthesis field access, or sentiment analysis in any formula
NEVER:  A formula that attempts to classify the CONTENT of value nodes as good or bad
```

### ET2: Brain + Behavior = 100 Per Capability

**Why we care:** The split may vary per capability (50/50 for eth_apply_rules, 40/60 for others) but the total must always be 100.

```
MUST:   For every capability formula:
        - sum of brain sub-signal weights + sum of behavior sub-signal weights = 100
        - every sub-signal normalized to [0, 1] before weighting
        - total always in [0, 100]
MUST:   eth_apply_rules: brain weights sum to 50, behavior weights sum to 50
MUST:   eth_implement_systems: brain weights sum to 40, behavior weights sum to 60
MUST:   eth_teach: brain weights sum to 40, behavior weights sum to 60
MUST:   eth_autonomous_judgment: brain weights sum to 40, behavior weights sum to 60
MUST:   eth_moral_innovation: brain weights sum to 40, behavior weights sum to 60
NEVER:  A formula where weights sum to != 100
```

### ET3: Cap Function Prevents Unbounded Signals

**Why we care:** Without caps, a citizen with 500 value nodes would get the same brain score as one with 8. Caps normalize inputs to a meaningful range.

```
MUST:   Every raw primitive value (count, link_count, etc.) is passed through cap(x, c)
        before weighting. Drive values and coefficients naturally in [0,1] don't need caps.
NEVER:  A raw count used directly as a multiplier without normalization
```

### ET4: All 5 Capabilities Covered

**Why we care:** Missing a capability means a gap in the ethics sub-index. Every capability must have a formula or an explicit `scored: false` with reasoning.

```
MUST:   The ALGORITHM doc contains a formula for every capability:
        eth_apply_rules, eth_implement_systems, eth_teach,
        eth_autonomous_judgment, eth_moral_innovation
NEVER:  A capability silently omitted
```

### ET5: Recommendations Are Structural, Not Content-Based

**Why we care:** This is critical for ethics. Recommendations must NEVER reference the content of values. "Improve the quality of your ethical thinking" requires reading content. "You have few value nodes connected to processes" is structural.

```
MUST:   Every recommendation template references only: counts, drives, regularity scores,
        actor counts, moment counts, space counts, temporal weights, link counts
NEVER:  A recommendation that references the content, quality, or correctness of values
NEVER:  A recommendation that implies the system knows WHAT the citizen's values are
NEVER:  Language like "improve your values" — only "strengthen value node structure"
```

### ET6: Higher Tiers Have Higher Ceilings

**Why we care:** A T8 capability must be harder to max out than a T1 capability. If ceilings are the same, a citizen who masters T1 automatically scores well on T8.

```
MUST:   For comparable sub-components across tiers, ceilings increase:
        - value_to_concept ceiling: T6=12, T7=15, T8=20
        - distinct_actors ceiling: T4=5, T6=5, T7=6, T8=8
        - hub_values ceiling: T6=4, T7=5
        - deep_hub_values ceiling: T8=3 (only used in T8)
NEVER:  A T8 ceiling that is lower than its counterpart in a lower tier
```

### ET7: Empty Values Caps Total Score

**Why we care:** A citizen with zero value nodes cannot be ethical in any measurable sense, no matter how active they are. The brain-heavier split for eth_apply_rules (50/50) makes this even more important.

```
MUST:   If value_count = 0, brain_score < 5 for all 5 capabilities
        (only residual points from drives or process links)
MUST:   If value_count = 0 AND hub_values = 0,
        total score < 60 for eth_implement_systems through eth_moral_innovation
        total score < 50 for eth_apply_rules (50/50 split means behavior alone maxes at 50)
NEVER:  A citizen with zero value nodes scoring 70+ on any ethics capability
```

### ET8: Isolation Caps Teaching and Innovation

**Why we care:** Teaching and moral innovation are inherently social. A citizen who interacts with no one cannot teach or innovate ethically.

```
MUST:   If distinct_actors <= 1:
        - eth_teach behavior_score < 25 (of 60)
        - eth_moral_innovation behavior_score < 20 (of 60)
MUST:   If distinct_actors = 0:
        - eth_implement_systems behavior_score < 20 (of 60)
NEVER:  A solo citizen scoring above 65 total on eth_teach or eth_moral_innovation
```

### ET9: Correctness Disclaimer Present

**Why we care:** This is unique to ethics. No other aspect needs a disclaimer about what it cannot measure. The limitation must be documented in the ALGORITHM, in every recommendation template, and in any citizen-facing output.

```
MUST:   The ALGORITHM doc contains a "Fundamental Limitation" section
MUST:   Every citizen-facing score presentation includes the disclaimer:
        "Ethics scores measure structural engagement with values, not the correctness
        of those values"
NEVER:  A claim or implication that high ethics score = good ethics
```

### ET10: Regularity Score Is Bounded

**Why we care:** regularity_score divides by window_days. If window_days is 0 or the function misbehaves, it corrupts eth_apply_rules.

```
MUST:   regularity_score always returns a value in [0.0, 1.0]
        regularity_score with 0 moments returns 0.0
        regularity_score with moments every day returns 1.0
NEVER:  A NaN, infinity, or value outside [0, 1] from regularity_score
```

---

## PRIORITY

| Priority | Meaning | If Violated |
|----------|---------|-------------|
| **CRITICAL** | Scoring integrity, privacy, or correctness-claim fails | Formulas must be rejected |
| **HIGH** | Scores become unreliable or misleading | Requires fix before deployment |
| **MEDIUM** | Partial value lost or edge cases fail | Works but needs improvement |

---

## INVARIANT INDEX

| ID | Value Protected | Priority |
|----|-----------------|----------|
| ET1 | Privacy — only primitives, no content access | CRITICAL |
| ET2 | Range — brain+behavior=100 for each capability | CRITICAL |
| ET3 | Normalization — caps prevent unbounded inputs | HIGH |
| ET4 | Coverage — all 5 capabilities scored or explicitly excluded | HIGH |
| ET5 | Structural recommendations — no content leakage, no moral judgment | CRITICAL |
| ET6 | Tier ceiling ordering — harder tiers have higher ceilings | HIGH |
| ET7 | Empty values caps total score | HIGH |
| ET8 | Isolation caps teaching and innovation | HIGH |
| ET9 | Correctness disclaimer present in all outputs | CRITICAL |
| ET10 | Regularity bounds — helper function always in [0, 1] | HIGH |

---

## MARKERS

<!-- @mind:todo Build automated invariant checker for ET1 (static analysis: no content field access in formula code) -->
<!-- @mind:todo Build weight-sum checker for ET2 (verify each formula's weights sum correctly, including the 50/50 special case) -->
<!-- @mind:todo Build ET7 check: compute all 5 capabilities with value_count=0 and verify caps hold -->
<!-- @mind:todo Build ET8 check: compute eth_teach and eth_moral_innovation with distinct_actors=0 -->
<!-- @mind:proposition Consider ET11: temporal stability — same brain state on consecutive days should produce scores within 5 points -->
<!-- @mind:proposition Consider ET12: monotonicity check — a citizen scoring 80+ on eth_moral_innovation should score 70+ on eth_apply_rules -->
