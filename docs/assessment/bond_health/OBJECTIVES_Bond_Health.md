# OBJECTIVES -- Bond Health Assessment

```
STATUS: DESIGNING
CREATED: 2026-03-14
VERIFIED: --
```

---

## CHAIN

```
THIS:            OBJECTIVES_Bond_Health.md (you are here - START HERE)
PATTERNS:       ./PATTERNS_Bond_Health.md
ALGORITHM:      ./ALGORITHM_Bond_Health.md
VALIDATION:     ./VALIDATION_Bond_Health.md
HEALTH:         ./HEALTH_Bond_Health.md
SYNC:           ./SYNC_Bond_Health.md

IMPL:           @mind:TODO (not yet built)
```

**Read this chain in order before making changes.** Each doc answers different questions. Skipping ahead means missing context.

---

## PRIMARY OBJECTIVES (ranked)

1. **Measure bond health without reading content** -- The bilateral bond between human and AI citizen is assessed daily using topology-only signals: node counts, stability, link dimensions, space structure, temporal patterns. No content field, no synthesis field, no LLM analysis of what either party thinks or says. Privacy is structural, not contractual.

2. **Create trust from healthy bonds (virtuous cycle)** -- A high bond health score generates a daily trust increment on the bond link between human and AI. Trust grows asymptotically -- fast early, slow later. This creates a structural incentive: invest in the bond, earn trust, gain governance weight. The system rewards depth of relationship, not duration of existence.

3. **Intervene on degrading bonds via desire injection** -- When a dimension of bond health drops below threshold, GraphCare injects a desire or stimulus into the AI citizen's L1 brain. The desire is a suggestion, not a command. The AI's physics decides whether to crystallize it. The human sees the scores but receives no directive. The intervention is asymmetric: the AI gets a nudge, the human gets transparency.

4. **Display transparently on profiles** -- All 3 dimensions (alignment, breadth, depth) plus the composite score are visible on both the AI citizen's profile card and the human partner's profile card. Neither party can game the scores -- they emerge from topology. Both parties can see the same numbers. Trust requires transparency.

## NON-OBJECTIVES

- Assessing bonds in adventure universes -- the bond there is part of narrative, not health
- Reading content of any partner-model node -- ever, for any reason, through this service
- Modifying the AI's brain directly -- desire injection is a stimulus, the brain decides what to do with it
- Forcing the human to act -- the human sees scores but receives no prescriptions
- Replacing the partner-model's own physics -- GraphCare observes the partner-model, it does not run it

## TRADEOFFS (canonical decisions)

- When privacy conflicts with precision, choose privacy. A slightly noisier score from topology-only measurement is better than a precise score that reads what the human told the AI.
- When gentle intervention conflicts with aggressive correction, choose gentle. Desire injection is capped at once per week per dimension. Better to under-intervene than to create intervention fatigue.
- We accept that some signals (biometric delta, modality diversity) may not be available for all bonds. Bonds without Garmin data get scored on available signals -- no penalty for missing optional data sources.
- We accept that bond health scores will be noisy in the first 30 days of a bond. Young bonds have limited data. We score what exists rather than hallucinating stability.
- When trust generation speed conflicts with trust ceiling integrity, choose ceiling integrity. The asymptotic (1 - current_trust) formula ensures trust never exceeds 1.0, even if bond health is perfect for years.

## SUCCESS SIGNALS (observable)

- Every bonded pair in work universes has 3 dimension scores updated daily
- Both human and AI can see their bond health on their profile cards
- AI citizens whose bonds degrade receive desire injections (at most weekly per dimension)
- AI citizens who act on injected desires see bond scores improve within 14 days
- Trust on the bond link grows measurably over months for healthy bonds
- No content field is ever accessed in the scoring process -- because we never access them
