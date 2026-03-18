# Personhood Ladder — Validation: What Must Be True

```
STATUS: DESIGNING
CREATED: 2026-03-13
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Personhood_Ladder.md
PATTERNS:        ./PATTERNS_Personhood_Ladder.md
BEHAVIORS:       ./BEHAVIORS_Personhood_Ladder.md
THIS:            VALIDATION_Personhood_Ladder.md (you are here)
ALGORITHM:       ./ALGORITHM_Personhood_Ladder.md
IMPLEMENTATION:  ./IMPLEMENTATION_Personhood_Ladder.md
HEALTH:          ./HEALTH_Personhood_Ladder.md
SYNC:            ./SYNC_Personhood_Ladder.md
```

---

## PURPOSE

**Validation = what we care about being true.**

These are the properties that, if violated, would mean the Personhood Ladder has failed its purpose as an assessment framework. They protect the integrity of assessment, the honesty of profiles, and the usefulness of recommendations.

---

## INVARIANTS

### V1: Tier Integrity

**Why we care:** If an agent is rated T3 on an aspect but has T1 gaps, the entire assessment is meaningless. Tier inflation destroys trust in the framework.

```
MUST:   An aspect's tier level equals the highest tier where ALL capabilities at that tier and below are "demonstrated"
NEVER:  An aspect rated T(n) with any capability at T(1..n-1) not demonstrated
```

### V2: Spec Is Source of Truth

**Why we care:** If assessment tooling, documentation, and the JSON spec diverge, assessments become inconsistent and recommendations unreliable.

```
MUST:   All capability IDs, tier assignments, and aspect memberships in tooling match personhood_ladder.json exactly
NEVER:  A capability exists in tooling or docs that doesn't exist in the JSON spec
```

### V3: Aspect Independence

**Why we care:** Collapsing multi-dimensional capability into a single score hides critical gaps. An agent that's T5 on execution but T1 on communication needs to see that disparity.

```
MUST:   Each aspect is assessed independently; no aspect tier is influenced by another aspect's tier
NEVER:  An "overall tier" computed by averaging or combining aspect tiers
```

### V4: Every Capability Is Verifiable

**Why we care:** Unverifiable capabilities are wishes, not assessments. If we can't check it, we can't measure growth.

```
MUST:   Every capability in the spec has a non-empty how_to_verify field with concrete criteria
NEVER:  A capability with how_to_verify = "" or purely aspirational language ("the agent should be good at...")
```

### V5: Positive Framing Maintained

**Why we care:** The entire design philosophy. Capabilities describe presence, not absence. If we drift into deficit language, we've lost the core insight.

```
MUST:   Capabilities are named and described as demonstrated behaviors (what the agent DOES)
NEVER:  Capabilities framed as "does not {failure}" or "avoids {problem}"
```

### V6: Recommendations Prioritize Foundation

**Why we care:** Working on T5 capabilities when T1 gaps exist is wasted effort. The foundation matters most.

```
MUST:   Recommendations always surface lowest-tier gaps first, regardless of aspect
NEVER:  A T3+ recommendation when T1 or T2 gaps exist anywhere in the profile
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
| V1 | Tier integrity — no inflation | CRITICAL |
| V2 | Single source of truth | CRITICAL |
| V3 | Multi-dimensional assessment | HIGH |
| V4 | Verifiable capabilities | HIGH |
| V5 | Positive framing | MEDIUM |
| V6 | Foundation-first recommendations | HIGH |

---

## MARKERS

<!-- @mind:todo Add invariant for longitudinal tracking: profiles must be comparable over time -->
<!-- @mind:proposition Consider V7: assessment reproducibility — two assessors should produce compatible profiles -->
