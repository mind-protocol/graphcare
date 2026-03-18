# Communication & Coordination — Validation: What Must Be True

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Communication.md
PATTERNS:        ./PATTERNS_Communication.md
ALGORITHM:       ./ALGORITHM_Communication.md
THIS:            VALIDATION_Communication.md (you are here)
HEALTH:          ./HEALTH_Communication.md
SYNC:            ./SYNC_Communication.md

IMPL:            @mind:TODO
```

---

## PURPOSE

These invariants protect the integrity of the communication scoring formulas. If violated, scores become unreliable, privacy is breached, or recommendations mislead citizens.

---

## INVARIANTS

### V1: Formulas Use Only Primitives

**Why we care:** If a formula sneaks in a custom query or content read, it can't be audited and violates the privacy guarantee.

```
MUST:   Every formula in this doc uses exclusively: count, mean_energy, link_count, min_links,
        cluster_coefficient, drive, recency (brain) + moments, moment_has_parent,
        first_moment_in_space, distinct_actors_in_shared_spaces (universe)
NEVER:  A custom Cypher query, LLM call, embedding comparison, content field access,
        or synthesis field access in any formula
```

### V2: Brain 0-40, Behavior 0-60, Total 0-100

**Why we care:** The 40/60 split is a design contract. If a formula exceeds its range, aggregate scores become meaningless.

```
MUST:   For every capability formula:
        - sum of brain sub-signal weights = 40
        - sum of behavior sub-signal weights = 60
        - every sub-signal normalized to [0, 1] before weighting
        - total = brain + behavior, always in [0, 100]
NEVER:  A formula where weights sum to != 40 (brain) or != 60 (behavior)
```

### V3: Cap Function Prevents Unbounded Signals

**Why we care:** Without caps, a citizen with 1000 process nodes would get the same brain score as one with 5. Caps normalize inputs to a meaningful range.

```
MUST:   Every raw primitive value (count, link_count, etc.) is passed through cap(x, c)
        before weighting. Drive values and coefficients naturally in [0,1] don't need caps.
NEVER:  A raw count used directly as a multiplier without normalization
```

### V4: All 11 Capabilities Covered

**Why we care:** Missing a capability means a gap in the communication sub-index. Every capability must have a formula or an explicit `scored: false` with reasoning.

```
MUST:   The ALGORITHM doc contains a formula for every capability in:
        comm_update_journal, comm_update_sync, comm_notify_stakeholders,
        comm_ask_for_help, comm_participate_collective, comm_lead_coordination,
        comm_regular_interactions, comm_inspire, comm_network_mind_protocol,
        comm_network_global, comm_global_influence
NEVER:  A capability silently omitted
```

### V5: Recommendations Are Structural, Not Content-Based

**Why we care:** Recommendations derived from formulas must reference the same structural signals the formulas use. A recommendation that says "improve the quality of your journal entries" requires reading content, which we don't do.

```
MUST:   Every recommendation template references only: counts, drives, regularity scores,
        interlocutor counts, moment counts, space counts, temporal weights
NEVER:  A recommendation that references content, quality, tone, or substance of any moment
```

### V6: Tier Weights Decrease Monotonically

**Why we care:** The sub-index must weight foundations heavier than pinnacles. If T8 weighs more than T2, a citizen failing basic journaling could compensate with global influence.

```
MUST:   In the comm_index weighted mean, weights satisfy:
        weight(T2) >= weight(T3) >= weight(T4) >= weight(T5) >= weight(T6) >= weight(T7) >= weight(T8)
NEVER:  A higher-tier weight exceeds a lower-tier weight
```

### V7: Synthetic Test Profile Ranges

**Why we care:** Formulas must produce sensible scores for archetypal profiles. If a "fully healthy" synthetic profile scores 50, the formula is miscalibrated.

```
MUST:   For each formula, the 5 synthetic test profiles produce scores in these ranges:
        - Fully healthy: 85-100
        - Fully unhealthy: 0-20
        - Brain-rich but inactive: 25-45
        - Active but brain-poor: 45-65
        - Average citizen: 50-75
NEVER:  A formula where a fully healthy profile scores below 80 or a fully unhealthy profile scores above 25
```

### V8: Regularity Score Is Bounded

**Why we care:** regularity_score divides by window_days. If window_days is 0 or if the function misbehaves, it corrupts every formula that uses it.

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
| **CRITICAL** | Scoring integrity or privacy fails | Formulas must be rejected |
| **HIGH** | Scores become unreliable or misleading | Requires fix before deployment |
| **MEDIUM** | Partial value lost or edge cases fail | Works but needs improvement |

---

## INVARIANT INDEX

| ID | Value Protected | Priority |
|----|-----------------|----------|
| V1 | Privacy — only primitives in formulas | CRITICAL |
| V2 | Range — 40/60/100 split maintained | CRITICAL |
| V3 | Normalization — caps prevent unbounded inputs | HIGH |
| V4 | Coverage — all 11 capabilities scored or explicitly excluded | HIGH |
| V5 | Structural recommendations — no content leakage | HIGH |
| V6 | Tier weight ordering — foundations heavier than pinnacles | MEDIUM |
| V7 | Calibration — synthetic profiles in expected ranges | HIGH |
| V8 | Regularity bounds — helper function always in [0, 1] | HIGH |

---

## MARKERS

<!-- @mind:todo Build automated invariant checker for V1 (static analysis of formula code) -->
<!-- @mind:todo Build weight-sum checker for V2 (verify each formula's weights sum correctly) -->
<!-- @mind:proposition Consider V9: temporal stability — same brain state on consecutive days should produce scores within 5 points -->
