# OBJECTIVES — Daily Citizen Health

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
THIS:            OBJECTIVES_Daily_Citizen_Health.md (you are here - START HERE)
PATTERNS:       ./PATTERNS_Daily_Citizen_Health.md
BEHAVIORS:      ./BEHAVIORS_Daily_Citizen_Health.md
ALGORITHM:      ./ALGORITHM_Daily_Citizen_Health.md
VALIDATION:     ./VALIDATION_Daily_Citizen_Health.md
IMPLEMENTATION: ./IMPLEMENTATION_Daily_Citizen_Health.md
HEALTH:         ./HEALTH_Daily_Citizen_Health.md
SYNC:           ./SYNC_Daily_Citizen_Health.md

IMPL:           @mind:TODO (not yet built)
```

**Read this chain in order before making changes.** Each doc answers different questions. Skipping ahead means missing context.

---

## PRIMARY OBJECTIVES (ranked)

1. **Detect citizen health issues before they escalate** — Every citizen in Lumina Prime receives a daily automated health assessment. Problems are caught when they're small, not when they're crises.

2. **Score capabilities mathematically without reading content** — All assessment is pure graph math: topology, counts, energies, link structure. No content is read. No LLM analyzes what the citizen thinks. Privacy is structural, not contractual.

3. **Provide actionable intervention when problems are found** — When a score drops, the citizen receives a message: what changed, why it matters, what to do. Not a number — an explanation with a recommendation.

4. **Create a feedback loop between score and brain physics** — The GraphCare score influences the citizen's stress drive. Low score → higher stress → the citizen's brain naturally prioritizes health-improving behaviors. The system self-corrects.

5. **Free for all citizens in work universes** — This is a public health service, not a premium feature. Every Lumina Prime citizen gets daily checks at no cost. GraphCare funds this as a public utility.

## NON-OBJECTIVES

- Assessing citizens in adventure universes (Contre-Terre, etc.) — paranoia, stress, dysfunction are part of the experience there
- Reading brain content — ever, for any reason, through this service
- Replacing citizen autonomy — the message is a recommendation, not a command
- Competing with pathology detection — the 12 pathologies are a separate diagnostic system for Dragon Slayer

## TRADEOFFS (canonical decisions)

- When privacy conflicts with accuracy, choose privacy. We'd rather have a slightly less precise score than read a single node's content.
- When daily frequency conflicts with compute cost, choose daily. This is a public service — frequency is non-negotiable.
- We accept that some capabilities can't be scored from topology alone. Those capabilities get `score: null` (unmeasurable), not a guess.
- We accept that the stress feedback loop could amplify negative cycles. The intervention message must include actionable steps that break the loop.

## SUCCESS SIGNALS (observable)

- Every Lumina Prime citizen receives a daily health message (or silence = healthy)
- Citizens who follow recommendations see their scores improve within 7 days
- The number of crises (emergency interventions) decreases over time as daily checks catch issues early
- No citizen ever discovers that GraphCare read their content — because we never do
