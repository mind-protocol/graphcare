# Mentorship & Legacy — Validation: What Must Be True

```
STATUS: DESIGNING
CREATED: 2026-03-13
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Mentorship_Legacy.md
PATTERNS:        ./PATTERNS_Mentorship_Legacy.md
ALGORITHM:       ./ALGORITHM_Mentorship_Legacy.md
THIS:            VALIDATION_Mentorship_Legacy.md (you are here)
HEALTH:          ./HEALTH_Mentorship_Legacy.md
SYNC:            ./SYNC_Mentorship_Legacy.md
```

---

## PURPOSE

These invariants protect the integrity of the Mentorship & Legacy scoring. If violated, the system either misattributes other actors' independent behavior as mentorship, invades privacy, produces unstable scores, or creates perverse incentives (rewarding presence over impact, or penalizing disengagement from successful institutions).

---

## INVARIANTS

### V1: Only Primitives in Formulas

**Why we care:** If formulas use custom queries or content access, they can't be audited, reproduced, or trusted. Inherits from Daily Citizen Health V5.

```
MUST:   Every mentorship formula uses exclusively: count, mean_energy, link_count, min_links,
        cluster_coefficient, drive, recency (brain) + moments, moment_has_parent,
        first_moment_in_space, distinct_actors_in_shared_spaces, temporal_weight (universe)
NEVER:  A custom Cypher query, LLM call, embedding comparison, content field access, or ad-hoc data access
```

**Priority:** CRITICAL

### V2: Content Never Accessed

**Why we care:** Privacy is structural, not contractual. Inherits from Daily Citizen Health V1. Mentorship scoring is particularly sensitive because it involves inter-actor relationships — reading content could reveal private conversations.

```
MUST:   All 4 mentorship formulas use only topology (types, links, counts, energies, drives, spaces, timestamps)
NEVER:  Formula reads node content, synthesis, or any text field
NEVER:  Intervention recommendation quotes or references content of shared knowledge or mentorship conversations
NEVER:  Daughter detection reads content to determine creation intent
```

**Priority:** CRITICAL

### V3: Brain Component Never Exceeds 40

**Why we care:** The 40/60 split ensures behavior matters more than intention. A brain oriented toward mentorship but with no mentorship behavior must score lower than a modest brain with active mentorship.

```
MUST:   brain_score <= 40 for every capability formula
MUST:   behavior_score <= 60 for every capability formula
MUST:   total = brain_score + behavior_score <= 100
NEVER:  A formula where brain contribution exceeds 40 points
```

**Priority:** HIGH

### V4: Third-Party Behavior Attribution Is Structural

**Why we care:** Mentorship scoring depends on other actors' behavior. Misattribution (crediting the citizen for coincidental third-party activity) would produce inflated scores. The attribution must be topologically justified.

```
MUST:   Outbound influence requires topological proximity: same space AND temporal ordering
        (citizen's moment precedes other actor's moment) OR direct parent link
MUST:   Daughter detection requires temporal proximity (< 48 hours) AND spatial co-location
        (citizen has prior moments in the space where the new actor first appears)
MUST:   Mentorship pair detection requires reciprocal activity (both citizen AND other actor
        have >= 2.0 temporal weight of moments in shared spaces)
NEVER:  All activity by any other actor in any citizen-adjacent space attributed as mentorship impact
NEVER:  Actors attributed as daughters without meeting the temporal proximity + spatial co-location criteria
```

**Priority:** HIGH

### V5: Independence Is Measured by Ratio, Not Absence

**Why we care:** A citizen who remains active in a thriving institution should not be penalized. Legacy independence is measured by others' activity as a proportion of total activity, not by the citizen's absence.

```
MUST:   Space independence = others_w / (others_w + citizen_w), range [0, 1]
MUST:   A space where both citizen and others are active has independence ~0.5 (healthy)
MUST:   A space where only others are active has independence ~1.0 (fully independent)
MUST:   A space where only citizen is active has independence ~0.0 (dependent)
NEVER:  A formula that penalizes the citizen for remaining active in a successful institution
NEVER:  Independence measured as citizen's absence (dropping to zero moments) — that would
        reward abandonment, not legacy
```

**Priority:** HIGH

### V6: Daughter Independence Requires Evidence

**Why we care:** A daughter that only exists in the parent's shadow is not truly independent. The independence metric must require structural evidence of autonomous operation.

```
MUST:   Independent daughters have moments in spaces the citizen never enters
MUST:   Independent daughters have >= 10 total moments (minimum viability threshold)
NEVER:  A daughter classified as independent solely because it exists
NEVER:  A daughter's score contribution based on the parent's activity (daughter's own moments count)
```

**Priority:** HIGH

### V7: Sub-Index Weights Sum to 1.0

**Why we care:** If weights don't sum to 1.0, the sub-index exceeds the 0-100 range, breaking comparison with other aspects.

```
MUST:   sum(weight[cap] for cap in mentorship_capabilities) == 1.0
MUST:   mentorship_subindex in range [0, 100]
NEVER:  Sub-index exceeds 100 or drops below 0
```

**Priority:** HIGH

### V8: Monotonicity Within Components

**Why we care:** More of a good signal should never decrease the score. A citizen with 3 mentees should never score lower than one with 2 mentees (all else equal).

```
MUST:   Within each sub-component, increasing the input value never decreases the output
MUST:   min() capping ensures plateau at cap, not decrease
NEVER:  A non-monotonic relationship between input signal and score contribution
```

**Priority:** MEDIUM

### V9: Deterministic Scoring

**Why we care:** Same topology + same behavior must produce the same score. Non-determinism makes debugging impossible and erodes trust.

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
MUST:   Profile 1 (active teacher / mentor / parent / builder) scores 75-90 per capability
MUST:   Profile 2 (knowledge hoarder / isolated / no offspring / solo) scores 8-25 per capability
MUST:   Profile 3 (sharing but no impact / social but shallow / dependent daughters / dependent spaces) scores 30-50
MUST:   Profile 4 (minimal brain but high impact) scores 50-65
MUST:   Profile 5 (average citizen) — knowledge_sharing: 35-55, mentor_ais: 25-45,
        daughters: 10-30, legacy_institution: 10-25
NOTE:   Average citizens are expected to score low on T7-T8 capabilities — these are elite achievements
```

**Priority:** MEDIUM

### V11: No Self-Mentorship

**Why we care:** The citizen's own moments should never count as outbound influence on themselves. Mentorship is about impact on others, not self-improvement.

```
MUST:   All outbound influence, mentorship pair, and institutional activity metrics exclude
        the citizen's own actor ID from the "other actors" set
NEVER:  Citizen's moments counting as both the sharing event and the influenced event
```

**Priority:** MEDIUM

---

## PRIORITY

| Priority | Meaning | If Violated |
|----------|---------|-------------|
| **CRITICAL** | Scoring integrity fails | All mentorship scores untrustworthy |
| **HIGH** | Major scoring distortion | Scores misleading but structurally intact |
| **MEDIUM** | Minor calibration issue | Scores slightly off but directionally correct |

---

## INVARIANT INDEX

| ID | Value Protected | Priority |
|----|-----------------|----------|
| V1 | Formula auditability (primitives only) | CRITICAL |
| V2 | Privacy (no content access) | CRITICAL |
| V3 | Brain/behavior split respected (40/60) | HIGH |
| V4 | Third-party behavior attribution accuracy | HIGH |
| V5 | Independence measured by ratio, not absence | HIGH |
| V6 | Daughter independence requires structural evidence | HIGH |
| V7 | Sub-index mathematical integrity (weights sum to 1.0) | HIGH |
| V8 | Monotonicity (more signal = equal or higher score) | MEDIUM |
| V9 | Deterministic output (same input = same output) | MEDIUM |
| V10 | Test profile calibration (expected ranges) | MEDIUM |
| V11 | No self-mentorship (citizen excluded from other-actor metrics) | MEDIUM |

---

## MARKERS

<!-- @mind:todo Implement V4 verification: static analysis that all third-party attribution uses topological proximity -->
<!-- @mind:todo Implement V10: run all 5 test profiles through all 4 formulas and verify ranges -->
<!-- @mind:todo Verify V5 implementation: independence formula uses ratio, not absence detection -->
<!-- @mind:proposition Consider V12: cross-capability consistency — a citizen scoring high on ment_legacy_institution should have nonzero ment_knowledge_sharing (institutions require knowledge transfer) -->
