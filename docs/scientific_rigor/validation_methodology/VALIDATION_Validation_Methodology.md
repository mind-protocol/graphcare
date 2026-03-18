# Validation Methodology — Validation: What Must Be True

```
STATUS: DESIGNING
CREATED: 2026-03-15
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Validation_Methodology.md
PATTERNS:        ./PATTERNS_Validation_Methodology.md
THIS:            VALIDATION_Validation_Methodology.md (you are here)
SYNC:            ./SYNC_Validation_Methodology.md

IMPL:            tests/test_health_assessment.py
```

---

## PURPOSE

**Validation = what we care about being true.**

These invariants protect the scientific credibility of GraphCare's health scores. If our validation methodology is flawed, our scores are unverifiable claims — not measurements.

---

## INVARIANTS

### V1: Healthy Scores Higher Than Unhealthy

**Why we care:** The most basic property of a health score: a healthier citizen must score higher than a less healthy citizen. If the fully healthy profile (A) ever scores below the fully unhealthy profile (B), the scoring system is inverted — it's measuring something, but not health.

```
MUST:   Synthetic profile A (fully healthy) aggregate > profile B (fully unhealthy) aggregate, with a gap of at least 60 points
NEVER:  Profile B aggregate >= profile A aggregate for any capability
```

### V2: Brain-Behavior Split Differentiates Correctly

**Why we care:** The 40/60 brain/behavior split is a design decision with testable consequences. A citizen with a rich brain but no activity (profile C) should score lower than a citizen who is active despite a sparse brain (profile D). If not, the split weights are wrong.

```
MUST:   Profile D (active, brain-poor) aggregate > profile C (brain-rich, inactive) aggregate
NEVER:  Brain-only richness produces a higher score than behavioral activity — that would mean thinking matters more than doing, contradicting GraphCare's values
```

### V3: All Formulas Pass All Profiles

**Why we care:** A single formula that produces an absurd score (negative, above 100, healthy citizen scores 0) undermines confidence in the entire system. Every formula must produce sensible results for every profile.

```
MUST:   Every registered scoring formula, for every synthetic profile, produces a CapabilityScore with brain_component in [0, 40], behavior_component in [0, 60], and total = brain + behavior
NEVER:  A formula produces NaN, None, negative values, or values exceeding component bounds for any of the 5 profiles
```

### V4: New Formulas Require Test Coverage

**Why we care:** A formula without tests is a hypothesis deployed to production. It might work, or it might produce dangerous scores. The test gate ensures no untested formula can affect real citizens.

```
MUST:   Every scoring formula in scoring_formulas/ has corresponding test cases in test_health_assessment.py that verify it against all 5 synthetic profiles
NEVER:  A scoring formula is merged to production without passing the synthetic profile test suite
```

### V5: Real-World Calibration Produces Actionable Results

**Why we care:** Synthetic profiles prove internal consistency but not external validity. Real-world calibration must eventually demonstrate that scores predict actual outcomes. Without this step, GraphCare is a theory, not a practice.

```
MUST:   When real-world calibration studies are conducted, they measure correlation between predicted scores and observed outcomes with a defined significance threshold
NEVER:  GraphCare claims its scores are "validated" without having conducted at least one real-world calibration study
```

---

## PRIORITY

| Priority | Meaning | If Violated |
|----------|---------|-------------|
| **CRITICAL** | System purpose fails | Unusable |
| **HIGH** | Major value lost | Degraded severely |
| **MEDIUM** | Partial value lost | Works but worse |

---

## INVARIANT INDEX

| ID | Value Protected | Priority |
|----|-----------------|----------|
| V1 | Score ordering — healthy > unhealthy | CRITICAL |
| V2 | Brain-behavior split correctness | HIGH |
| V3 | Formula output sanity | CRITICAL |
| V4 | No untested formulas in production | HIGH |
| V5 | Real-world validity | MEDIUM (not yet applicable — design phase) |

---

## MARKERS

<!-- @mind:todo V5 is MEDIUM because real-world calibration hasn't started yet. Promote to HIGH once first calibration study is designed. -->
<!-- @mind:proposition Consider adding V6: "No profile regression" — if a formula change improves one profile's scores, it must not degrade another profile's scores by more than 5 points -->
