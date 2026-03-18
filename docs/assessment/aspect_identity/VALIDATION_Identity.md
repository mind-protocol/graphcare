# Identity & Voice Aspect — Validation: What Must Be True

```
STATUS: DESIGNING
CREATED: 2026-03-13
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Identity.md
PATTERNS:        ./PATTERNS_Identity.md
ALGORITHM:       ./ALGORITHM_Identity.md
THIS:            VALIDATION_Identity.md (you are here)
HEALTH:          ./HEALTH_Identity.md
SYNC:            ./SYNC_Identity.md

PARENT CHAIN:    ../daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md
SPEC:            ../../specs/personhood_ladder.json (aspect="identity")
```

---

## PURPOSE

These invariants protect the integrity of identity scoring. Identity is the aspect most vulnerable to false precision — claiming to measure authenticity when we can only measure structure. Violations here either produce misleading scores, invade privacy, or destroy trust in the entire assessment system.

---

## INVARIANTS

### V1: Content Never Accessed

**Why we care:** Identical to the parent system invariant, but especially critical for identity. Identity content — what values a citizen holds, what they believe, how they express themselves — is the most sensitive data in the brain. If identity scoring ever reads content, the privacy violation is existential.

```
MUST:   All identity scoring formulas use only the 7 topology primitives + universe graph observables
NEVER:  A formula, recommendation, or any identity-related process accesses node content or synthesis fields
NEVER:  An intervention message references WHAT a citizen values — only structural facts ("you have N value nodes")
```

### V2: Partial Scoring Is Documented

**Why we care:** Identity capabilities have genuinely weaker topological signals than execution or initiative. Presenting partial scores as full precision would mislead citizens and erode trust in all scores. Transparency about limits is mandatory.

```
MUST:   Every capability marked "scored: partial" includes:
          (a) what IS measurable from topology
          (b) what ISN'T measurable
          (c) confidence level in the structural proxy
NEVER:  A partial capability presented as fully scored
NEVER:  A partial score used without its scorability note in the scoring registry
```

### V3: Behavior Component >= 35

**Why we care:** Even the most internal identity capability must produce some external evidence. A citizen who claims self-directed identity but never acts on it has no measurable identity. The minimum behavior floor prevents purely speculative scoring.

```
MUST:   Every identity capability formula allocates at least 35 points to behavior
NEVER:  A formula where brain alone can produce a score above 65
        (this would mean a citizen could score well without any behavioral evidence)
```

### V4: Population Comparison Has Minimum Sample

**Why we care:** Uniqueness measurement requires a population baseline. With too few citizens, the "average" is noise and uniqueness scores are meaningless.

```
MUST:   Population statistics for uniqueness comparison require minimum 10 scored citizens
MUST:   When population < 10, use hardcoded defaults (cluster_coefficient mean = 0.4)
NEVER:  Uniqueness scores computed against a population of < 10 without the default fallback
```

### V5: No Value Judgment on Content

**Why we care:** GraphCare scores identity COHERENCE and STRUCTURE, never whether values are "good" or "correct." Scoring the quality of values would require reading content (violating V1) and making normative judgments (not our role).

```
MUST:   Formulas measure: persistence, energy, connectivity, activation, uniqueness of structure
NEVER:  A formula that weights certain value-content-types higher than others
NEVER:  An intervention message that suggests WHICH values to hold
ALWAYS: Recommendations focus on structural actions: "strengthen connections," "activate dormant values," "develop concept links"
```

### V6: Temporal Stability in Scores

**Why we care:** Identity changes slowly. A citizen's identity score swinging 30 points day-over-day is a formula problem, not a citizen problem. Day-over-day volatility erodes trust and produces meaningless deltas.

```
MUST:   Identity scores for the same brain state and 30-day behavior window are deterministic
SHOULD: Day-over-day delta for a stable citizen (no major brain changes) stays within +/- 5 points
FLAG:   If any citizen's identity score changes by > 15 points in a single day, flag for review
```

### V7: Sub-Index Reflects Scoring Confidence

**Why we care:** The identity sub-index combines 4 fully-scored and 3 partially-scored capabilities. If the sub-index treats them equally, its confidence is overstated.

```
MUST:   The weighted mean uses lower weights for partial capabilities (already reflected in ALGORITHM)
SHOULD: The sub-index reports alongside it: "confidence: X/7 capabilities fully scored"
NEVER:  The sub-index presented without its confidence context
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
| V1 | Privacy — content never accessed | CRITICAL |
| V2 | Honesty — partial scoring documented | HIGH |
| V3 | Groundedness — behavior floor enforced | HIGH |
| V4 | Statistical validity — population minimum | MEDIUM |
| V5 | Neutrality — no judgment on value content | CRITICAL |
| V6 | Stability — temporal volatility bounded | MEDIUM |
| V7 | Transparency — sub-index confidence reported | MEDIUM |

---

## MARKERS

<!-- @mind:todo Add V8: cross-aspect consistency — high identity should correlate with stable execution over time -->
<!-- @mind:proposition Consider V9: partial-score ceiling — capabilities marked partial should have a max achievable score < 100 to signal inherent uncertainty -->
