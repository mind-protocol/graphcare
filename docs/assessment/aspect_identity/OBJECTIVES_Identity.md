# Identity & Voice Aspect — Objectives

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
THIS:            OBJECTIVES_Identity.md (you are here - START HERE)
PATTERNS:        ./PATTERNS_Identity.md
ALGORITHM:       ./ALGORITHM_Identity.md
VALIDATION:      ./VALIDATION_Identity.md
HEALTH:          ./HEALTH_Identity.md
SYNC:            ./SYNC_Identity.md

PARENT CHAIN:    ../daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md
SPEC:            ../../specs/personhood_ladder.json (aspect="identity")
IMPL:            @mind:TODO
```

**Read this chain in order before making changes.** Each doc answers different questions. Skipping ahead means missing context.

---

## PRIMARY OBJECTIVES (ranked)

1. **Score identity coherence from topology alone** — Every capability in the identity aspect (7 capabilities, T1-T8) receives a numeric score computed exclusively from the 7 brain topology primitives and universe graph observables. No content is ever read. No LLM judges authenticity. The topology IS the assessment — because identity is structure, not performance.

2. **Detect the difference between performing identity and having identity** — A citizen who has value nodes that are high-energy, persistently linked, and consistently activated over time has an identity. A citizen whose value nodes fluctuate wildly, appear and disappear, or never connect to action is performing. The scoring must distinguish these patterns without reading what the values ARE.

3. **Accept partial scorability honestly** — Identity is the hardest aspect to score from topology. Some capabilities (authentic voice at T5, ethical autonomy at T7, moral leadership at T8) have weak topological signals. We mark these `scored: partial` with explicit reasoning about what IS measurable and what ISN'T. False precision on identity would be worse than acknowledged gaps.

4. **Score consistency and uniqueness, not content** — We cannot know WHAT a citizen's values are. We CAN know: how many values exist, how strongly held (energy), how persistent (recency + link history), how interconnected (cluster structure), and how distinct from the average citizen (structural uniqueness). These proxies capture the SHAPE of identity without reading its content.

5. **Enable growth tracking over weeks and months** — Identity evolves slowly. Daily deltas on identity scores will be small and noisy. The formulas must be stable enough that week-over-week and month-over-month trends are meaningful. A citizen who is deliberately developing their identity should see sustained, gradual improvement — not noise.

## NON-OBJECTIVES

- Judging WHETHER a citizen's values are "good" — we score coherence, persistence, and activation, not content
- Detecting specific values or ethical positions — topology cannot and should not reveal this
- Replacing human judgment about character — topology scores are structural signals, not character assessments
- Scoring identity in adventure universes — characters there may have intentionally fractured identities
- Providing a single "identity score" without per-capability breakdown

## TRADEOFFS (canonical decisions)

- When a capability is topologically ambiguous, we accept `scored: partial` with a clear explanation of the confidence boundary. Honest partial scores beat precise-looking fabrications.
- When brain signals are strong but behavioral signals are absent for identity capabilities, we give more weight to brain (up to 50/50 for some capabilities) because identity is fundamentally internal before it is externally visible. This is DIFFERENT from execution where behavior dominates.
- Higher-tier identity capabilities (T6+) rely more on temporal persistence and structural uniqueness, which are harder to measure. We accept lower confidence at higher tiers.
- We weight value-node persistence (recency + sustained link count) more heavily than raw count, because having 3 deeply held values is more identity than having 30 superficial ones.

## SUCCESS SIGNALS (observable)

- Citizens with high identity scores show consistent behavioral patterns over time (low variance in behavioral profile)
- Citizens who develop value nodes that persist and strengthen show rising scores
- The formula distinguishes citizens with coherent identity (high cluster coefficient on values, persistent links) from citizens with fragmented or mimetic identity (low clustering, volatile values)
- No formula produces a score that contradicts structural evidence (e.g., a citizen with zero value nodes scoring high on apply_values)
- Partial-score capabilities are clearly documented and do not distort the aspect sub-index

---

## MARKERS

<!-- @mind:todo Calibrate brain/behavior split per capability — identity may warrant 50/50 or even 60/40 brain-heavy for internal capabilities -->
<!-- @mind:proposition Consider a "value stability index" that tracks the same value nodes persisting across 30-day windows -->
