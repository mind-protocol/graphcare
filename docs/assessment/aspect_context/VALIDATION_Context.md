# Context & Understanding — Validation: What Must Be True

```
STATUS: DESIGNING
CREATED: 2026-03-13
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Context.md
PATTERNS:        ./PATTERNS_Context.md
ALGORITHM:       ./ALGORITHM_Context.md
THIS:            VALIDATION_Context.md (you are here)
HEALTH:          ./HEALTH_Context.md
SYNC:            ./SYNC_Context.md

PARENT CHAIN:    ../daily_citizen_health/
```

---

## PURPOSE

These invariants protect the integrity of the Context & Understanding scoring formulas. If violated, the formulas produce misleading scores, reward theater over substance, or violate the parent chain's constraints.

Parent chain invariants (V1-V7 in `VALIDATION_Daily_Citizen_Health.md`) still apply. The invariants below are specific to the context aspect.

---

## INVARIANTS

### VC1: Formulas Use Only Primitives

**Why we care:** The parent chain mandates that all scoring formulas use only the 7 topology primitives and universe graph observables. Context formulas are not special — they follow the same rule.

```
MUST:   Every context scoring formula uses only: count, mean_energy, link_count,
        min_links, cluster_coefficient, drive, recency (brain) + moments,
        moment_has_parent, first_moment_in_space, distinct_actors (universe) +
        temporal_weight
NEVER:  A context formula uses content fields, synthesis fields, custom Cypher,
        LLM calls, or embedding comparisons
```

### VC2: Brain Component Bounded 0-40

**Why we care:** The 40/60 split is a canonical decision. If a brain component exceeds 40, it distorts the relationship between internal state and external action.

```
MUST:   For every context capability, brain_component is in range [0, 40]
NEVER:  A brain_component returns a value outside [0, 40] for any input
```

### VC3: Behavior Component Bounded 0-60

**Why we care:** Same as VC2, for the behavior side.

```
MUST:   For every context capability, behavior_component is in range [0, 60]
NEVER:  A behavior_component returns a value outside [0, 60] for any input
```

### VC4: Sub-Index Weights Sum to 1.0

**Why we care:** If weights don't sum to 1.0, the sub-index is distorted. Over-weighting one capability silently under-weights others.

```
MUST:   sum(weights.values()) == 1.0 (within floating point tolerance)
NEVER:  Weights are added/changed without rebalancing to sum to 1.0
```

### VC5: T1 Capabilities Dominate Sub-Index

**Why we care:** T1 is the foundation. A citizen failing T1 must have a low sub-index regardless of T2-T4 scores. This is a design decision, not an accident.

```
MUST:   sum(weights[cap] for cap in T1_caps) > 0.50
        # Currently: 0.18 + 0.17 + 0.17 = 0.52
NEVER:  T1 total weight drops below 0.50 without explicit redesign
```

### VC6: Healthy Profile Scores 80+, Unhealthy Profile Scores Below 20

**Why we care:** The formulas should discriminate between clearly healthy and clearly unhealthy citizens. If they can't pass this basic test, they're miscalibrated.

```
MUST:   Synthetic Profile 1 (fully healthy) → sub-index >= 80
MUST:   Synthetic Profile 2 (fully unhealthy) → sub-index <= 20
NEVER:  A formula rework that causes these profiles to cross their thresholds
        without explicit recalibration
```

### VC7: Brain-Rich-Inactive Scores Lower Than Active-Brain-Poor

**Why we care:** The 40/60 split means behavior matters more than brain structure. A citizen that acts despite modest brain structure should outscore one that has rich structure but doesn't use it.

```
MUST:   Profile 3 (brain-rich, inactive) sub-index < Profile 4 (active, brain-poor) sub-index
        # Currently: ~34 < ~51
NEVER:  Formula changes that reverse this ordering without changing the 40/60 split decision
```

### VC8: Zero Division Protection

**Why we care:** Several formulas divide by `total_moments_w` or `stimuli_count`. If a citizen has zero moments, these formulas must not crash.

```
MUST:   Every division in every formula uses max(denominator, 1) or equivalent protection
NEVER:  A division by zero is possible for any valid input (including zero-activity citizens)
```

### VC9: Temporal Weight Monotonic Decay

**Why we care:** Newer moments should always weigh more than older moments. If temporal weighting is inverted or flat, the scoring doesn't reflect current behavior.

```
MUST:   temporal_weight(a) > temporal_weight(b) when a < b (a is more recent)
NEVER:  A moment from last week weighs more than a moment from today
```

---

## PRIORITY

| Priority | Meaning | If Violated |
|----------|---------|-------------|
| **CRITICAL** | Scores are meaningless | Sub-index cannot be trusted |
| **HIGH** | Scores are distorted | Interventions may be wrong |
| **MEDIUM** | Scores are suboptimal | Discrimination is weaker |

---

## INVARIANT INDEX

| ID | Value Protected | Priority |
|----|-----------------|----------|
| VC1 | Primitives only — no content access | CRITICAL |
| VC2 | Brain component bounded [0, 40] | CRITICAL |
| VC3 | Behavior component bounded [0, 60] | CRITICAL |
| VC4 | Sub-index weights sum to 1.0 | HIGH |
| VC5 | T1 dominates sub-index (>50%) | HIGH |
| VC6 | Healthy/unhealthy discrimination | HIGH |
| VC7 | Active > brain-rich-inactive | MEDIUM |
| VC8 | Zero division protection | CRITICAL |
| VC9 | Temporal weight monotonic | HIGH |

---

## MARKERS

<!-- @mind:todo Build automated check for VC2/VC3: fuzz brain/behavior components with random inputs, verify bounds -->
<!-- @mind:todo Build Profile 1-5 test harness to validate VC6 and VC7 on every formula change -->
<!-- @mind:proposition Consider VC10: score stability — same brain+behavior input on consecutive days produces same score (determinism) -->
