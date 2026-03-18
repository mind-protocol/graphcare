# Initiative & Autonomy — Validation: What Must Be True

```
STATUS: DESIGNING
CREATED: 2026-03-13
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Initiative.md
PATTERNS:        ./PATTERNS_Initiative.md
ALGORITHM:       ./ALGORITHM_Initiative.md
THIS:            VALIDATION_Initiative.md (you are here)
HEALTH:          ./HEALTH_Initiative.md
SYNC:            ./SYNC_Initiative.md
```

---

## PURPOSE

These invariants protect the integrity of the Initiative & Autonomy scoring. If violated, the system either misclassifies reactive behavior as initiative, invades privacy, produces unstable scores, or creates perverse incentives.

---

## INVARIANTS

### V1: Auto-Initiation Detection Is Structural

**Why we care:** The entire initiative aspect rests on distinguishing self-initiated from reactive moments. If this detection is wrong, every score is wrong.

```
MUST:   A moment is classified as auto-initiated if and only if it has NO incoming triggers/responds_to link from another actor's moment
NEVER:  Auto-initiation determined by content analysis, heuristics, or LLM judgment
NEVER:  A moment with an incoming parent link from another actor classified as self-initiated
```

**Priority:** CRITICAL

### V2: Only Primitives in Formulas

**Why we care:** If formulas use custom queries or content access, they can't be audited, reproduced, or trusted. Inherits from Daily Citizen Health V5.

```
MUST:   Every initiative formula uses exclusively: count, mean_energy, link_count, min_links, cluster_coefficient, drive, recency (brain) + moments, moment_has_parent, first_moment_in_space, distinct_actors (universe)
NEVER:  A custom Cypher query, LLM call, embedding comparison, content field access, or ad-hoc data access
```

**Priority:** CRITICAL

### V3: Content Never Accessed

**Why we care:** Privacy is structural, not contractual. Inherits from Daily Citizen Health V1.

```
MUST:   All 8 initiative formulas use only topology (types, links, counts, energies, drives)
NEVER:  Formula reads node content, synthesis, or any text field
NEVER:  Intervention recommendation quotes or references content
```

**Priority:** CRITICAL

### V4: Outcome-Blind for T3-T7

**Why we care:** Scoring based on outcomes would punish risk-taking. A rejected proposal is still initiative.

```
MUST:   Formulas for init_fix_what_you_find through init_initiate_from_ambition score the ACT of self-initiating, not the result
MUST:   A proposal that gets rejected scores the same as a proposal that gets accepted (for the proposal capability)
EXCEPTION: init_change_lives (T8) includes adoption/propagation metrics because impact IS the definition at that tier
NEVER:  A formula that penalizes failed initiative at T3-T7
```

**Priority:** HIGH

### V5: Brain Component Never Exceeds 40

**Why we care:** The 40/60 split ensures behavior matters more than intention. A brain full of ambition but no action must score lower than a modest brain with high initiative.

```
MUST:   brain_score <= 40 for every capability formula
MUST:   behavior_score <= 60 for every capability formula
MUST:   total = brain_score + behavior_score <= 100
NEVER:  A formula where brain contribution exceeds 40 points
```

**Priority:** HIGH

### V6: Frustration Drive Capped

**Why we care:** Moderate frustration motivates initiative. High frustration indicates overwhelm. Scoring high frustration as positive would reward burn-out.

```
MUST:   Frustration drive contribution capped at 0.5-0.6 in all brain formulas
NEVER:  A formula where frustration > 0.6 produces a higher score than frustration = 0.6
```

**Priority:** HIGH

### V7: Sub-Index Weights Sum to 1.0

**Why we care:** If weights don't sum to 1.0, the sub-index exceeds the 0-100 range, breaking comparison with other aspects.

```
MUST:   sum(weight[cap] for cap in initiative_capabilities) == 1.0
MUST:   initiative_subindex in range [0, 100]
NEVER:  Sub-index exceeds 100 or drops below 0
```

**Priority:** HIGH

### V8: Monotonicity Within Components

**Why we care:** More of a good signal should never decrease the score. A citizen with 4 proposals should never score lower than a citizen with 3 proposals (all else equal).

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
NOTE:   temporal_weight introduces legitimate time-dependence (scores change as moments age), but given the same timestamps, output is deterministic
```

**Priority:** MEDIUM

### V10: Test Profiles Within Range

**Why we care:** If synthetic test profiles produce scores outside expected ranges, the formulas are miscalibrated.

```
MUST:   Profile 1 (fully healthy) scores 85-95 on sub-index
MUST:   Profile 2 (fully unhealthy) scores 10-20 on sub-index
MUST:   Profile 3 (brain-rich inactive) scores 30-40 on sub-index
MUST:   Profile 4 (active brain-poor) scores 50-60 on sub-index
MUST:   Profile 5 (average) scores 55-70 on sub-index (or lower — see note)
NOTE:   Average citizen initiative may be lower than other aspects since initiative starts at T3
```

**Priority:** MEDIUM

---

## PRIORITY

| Priority | Meaning | If Violated |
|----------|---------|-------------|
| **CRITICAL** | Scoring integrity fails | All initiative scores untrustworthy |
| **HIGH** | Major scoring distortion | Scores misleading but structurally intact |
| **MEDIUM** | Minor calibration issue | Scores slightly off but directionally correct |

---

## INVARIANT INDEX

| ID | Value Protected | Priority |
|----|-----------------|----------|
| V1 | Auto-initiation detection accuracy | CRITICAL |
| V2 | Formula auditability (primitives only) | CRITICAL |
| V3 | Privacy (no content access) | CRITICAL |
| V4 | Risk-taking not punished (outcome-blind) | HIGH |
| V5 | Brain/behavior split respected (40/60) | HIGH |
| V6 | Frustration cap (no burn-out reward) | HIGH |
| V7 | Sub-index mathematical integrity (weights sum to 1.0) | HIGH |
| V8 | Monotonicity (more signal = equal or higher score) | MEDIUM |
| V9 | Deterministic output (same input = same output) | MEDIUM |
| V10 | Test profile calibration (expected ranges) | MEDIUM |

---

## MARKERS

<!-- @mind:todo Implement V1 verification: static analysis that auto_initiated() is the sole initiation detector -->
<!-- @mind:todo Implement V10: run all 5 test profiles through formulas and verify ranges -->
<!-- @mind:proposition Consider V11: cross-capability consistency — a citizen scoring high on init_start_workstreams should not score zero on init_propose_improvements (workstreams imply proposals) -->
