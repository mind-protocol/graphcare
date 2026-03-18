# Trust & Reputation — Validation: What Must Be True

```
STATUS: DESIGNING
CREATED: 2026-03-13
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Trust_Reputation.md
PATTERNS:        ./PATTERNS_Trust_Reputation.md
ALGORITHM:       ./ALGORITHM_Trust_Reputation.md
THIS:            VALIDATION_Trust_Reputation.md (you are here)
HEALTH:          ./HEALTH_Trust_Reputation.md
SYNC:            ./SYNC_Trust_Reputation.md
```

---

## PURPOSE

These invariants protect the integrity of the Trust & Reputation scoring. If violated, the system either conflates assigned trust with earned trust, invades privacy, produces unstable scores, rewards gaming over genuine reliability, or fails to detect trust erosion.

---

## INVARIANTS

### V1: Content Never Accessed

**Why we care:** Privacy is structural, not contractual. Trust scoring must never learn WHAT was promised, discussed, or delivered — only that interactions occurred and chains completed. Inherits from Daily Citizen Health V1.

```
MUST:   All 5 trust formulas use only topology (types, links, counts, energies, drives)
NEVER:  Formula reads node content, synthesis, or any text field
NEVER:  Intervention recommendation quotes or references content
NEVER:  Response chain completion analysis reads the content of the response
```

**Priority:** CRITICAL

### V2: Only Primitives in Formulas

**Why we care:** If formulas use custom queries or content access, they can't be audited, reproduced, or trusted. Inherits from Daily Citizen Health V5.

```
MUST:   Every trust formula uses exclusively: count, mean_energy, link_count, min_links,
        cluster_coefficient, drive, recency (brain) + moments, moment_has_parent,
        first_moment_in_space, distinct_actors_in_shared_spaces, temporal_weight (universe)
NEVER:  A custom Cypher query, LLM call, embedding comparison, content field access, or ad-hoc data access
NOTE:   Derived stats (regularity, response_completion, inbound_moments) are computed FROM these primitives
```

**Priority:** CRITICAL

### V3: Regularity Measures Consistency Not Volume

**Why we care:** A citizen who produces 50 moments in 3 days and disappears for 27 days is NOT more reliable than a citizen who produces 1 moment per day for 30 days. If regularity conflates with volume, high-burst citizens get inflated reliability scores.

```
MUST:   regularity() uses coefficient of variation (std/mean) of moment counts across time windows
MUST:   A citizen with equal total moments but lower variance scores higher on regularity
NEVER:  Total moment count used as a direct proxy for regularity
NEVER:  A citizen with high burst activity and long absences scores higher than a steady-cadence citizen with the same total
```

**Priority:** HIGH

### V4: Inbound Signals Cannot Be Self-Generated

**Why we care:** If a citizen can inflate their inbound signal by creating moments that appear to come from others, the entire community and global trust scoring collapses.

```
MUST:   inbound_moments filters on m.actor != citizen_id (strict actor identity)
MUST:   far_inbound_unique counts distinct ACTORS, not distinct moments
NEVER:  A citizen's own moments counted as inbound
NOTE:   Sybil attacks (creating fake actors) are an L4 concern, not a scoring concern — we trust actor identity
```

**Priority:** HIGH

### V5: Brain Component Never Exceeds 40

**Why we care:** The 40/60 split ensures behavior matters more than brain state. A brain configured with high trust drive but no behavioral evidence must score lower than a modest brain with consistent reliability.

```
MUST:   brain_score <= 40 for every capability formula
MUST:   behavior_score <= 60 for every capability formula
MUST:   total = brain_score + behavior_score <= 100
NEVER:  A formula where brain contribution exceeds 40 points
```

**Priority:** HIGH

### V6: Response Chain Completion Handles Edge Cases

**Why we care:** New citizens with zero inbound requests and citizens in low-interaction spaces should not be penalized for the absence of interaction.

```
MUST:   response_completion returns 1.0 when zero inbound triggers exist (no requests = no failures)
MUST:   response_completion is bounded [0, 1.0]
NEVER:  A citizen penalized for not responding to requests that don't exist
NEVER:  Division by zero in response completion calculation
```

**Priority:** HIGH

### V7: Sub-Index Weights Sum to 1.0

**Why we care:** If weights don't sum to 1.0, the sub-index exceeds the 0-100 range, breaking comparison with other aspects.

```
MUST:   sum(weight[cap] for cap in trust_capabilities) == 1.0
MUST:   trust_subindex in range [0, 100]
NEVER:  Sub-index exceeds 100 or drops below 0
```

**Priority:** HIGH

### V8: Monotonicity Within Components

**Why we care:** More of a good signal should never decrease the score. A citizen with higher regularity should never score lower than one with lower regularity (all else equal). A citizen with more inbound unique actors should never score lower.

```
MUST:   Within each sub-component, increasing the input value never decreases the output
MUST:   min() capping ensures plateau at cap, not decrease
NEVER:  A non-monotonic relationship between input signal and score contribution
```

**Priority:** MEDIUM

### V9: Deterministic Scoring

**Why we care:** Same topology + same behavior must produce the same score. Non-determinism makes debugging impossible and erodes trust in the trust-scoring system itself.

```
MUST:   Given identical brain_stats and behavior_stats, every formula produces identical output
NEVER:  Randomness, LLM evaluation, or time-of-day effects in scoring formulas
NOTE:   temporal_weight introduces legitimate time-dependence (scores change as moments age),
        but given the same timestamps, output is deterministic
```

**Priority:** MEDIUM

### V10: Test Profiles Within Range

**Why we care:** If synthetic test profiles produce scores outside expected ranges, the formulas are miscalibrated.

```
MUST:   Profile 1 (reliable veteran / community hub / global authority) scores 80-95 per capability
MUST:   Profile 2 (unreliable ghost / isolated worker / local unknown) scores 5-18 per capability
MUST:   Profile 3 (brain-rich but inactive/unknown) scores 25-45 per capability
MUST:   Profile 4 (active but brain-poor) scores 45-65 per capability
MUST:   Profile 5 (average citizen) scores 25-65 per capability (range wider because trust capabilities span T1-T8)
```

**Priority:** MEDIUM

### V11: Trust Tier Does Not Dominate

**Why we care:** If drive("trust") contributes too many points, citizens with high assigned trust but no behavioral evidence score disproportionately high. Trust must be demonstrated, not declared.

```
MUST:   drive("trust") contributes at most 12 points (30% of brain, 12% of total)
MUST:   A citizen with drive("trust")=1.0 but zero behavioral signals scores below 40
MUST:   Behavioral evidence can compensate for zero trust drive (active + reliable citizen with no trust drive still scores meaningfully)
NOTE:   If drive("trust") doesn't exist as a named drive, all citizens get 0 from this sub-component, and behavioral signals determine scores entirely — this is acceptable
```

**Priority:** MEDIUM

### V12: New Citizens Are Not Penalized

**Why we care:** New citizens legitimately have low trust scores. This is correct (trust takes time to build). But the score should reflect "not yet demonstrated" rather than "untrustworthy."

```
MUST:   A new citizen with 7 days of regular activity and full response chain completion scores at least 30 on trust_basic_reliability
MUST:   A new citizen with zero moments scores close to zero (minimal brain contribution only)
NEVER:  A scoring formula that produces negative scores for new citizens
NOTE:   Low scores for new citizens are correct, not punitive — the growth trajectory IS the signal
```

**Priority:** LOW

---

## PRIORITY

| Priority | Meaning | If Violated |
|----------|---------|-------------|
| **CRITICAL** | Scoring integrity fails | All trust scores untrustworthy |
| **HIGH** | Major scoring distortion | Scores misleading but structurally intact |
| **MEDIUM** | Minor calibration issue | Scores slightly off but directionally correct |
| **LOW** | Edge case handling | Rare scenarios may produce unexpected scores |

---

## INVARIANT INDEX

| ID | Value Protected | Priority |
|----|-----------------|----------|
| V1 | Privacy (no content access) | CRITICAL |
| V2 | Formula auditability (primitives only) | CRITICAL |
| V3 | Regularity = consistency, not volume | HIGH |
| V4 | Inbound signals can't be self-generated | HIGH |
| V5 | Brain/behavior split respected (40/60) | HIGH |
| V6 | Edge cases handled (no requests = no failure) | HIGH |
| V7 | Sub-index mathematical integrity (weights sum to 1.0) | HIGH |
| V8 | Monotonicity (more signal = equal or higher score) | MEDIUM |
| V9 | Deterministic output (same input = same output) | MEDIUM |
| V10 | Test profile calibration (expected ranges) | MEDIUM |
| V11 | Trust tier does not dominate over behavioral evidence | MEDIUM |
| V12 | New citizens not penalized (low score is correct, not punitive) | LOW |

---

## MARKERS

<!-- @mind:todo Implement V3 verification: unit test that regularity(high_variance) < regularity(low_variance) for equal total moments -->
<!-- @mind:todo Implement V4 verification: assert inbound_moments never includes citizen's own moments -->
<!-- @mind:todo Implement V10: run all 5 test profiles per capability through formulas and verify ranges -->
<!-- @mind:todo Implement V11: test that drive("trust")=1.0 + zero behavior < 40 total -->
<!-- @mind:proposition Consider V13: cross-capability consistency — a citizen scoring high on trust_community should score above average on trust_basic_reliability (community trust implies basic reliability) -->
