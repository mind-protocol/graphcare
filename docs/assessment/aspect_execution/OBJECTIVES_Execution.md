# Execution Quality Aspect — Objectives

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
THIS:            OBJECTIVES_Execution.md (you are here - START HERE)
PATTERNS:        ./PATTERNS_Execution.md
ALGORITHM:       ./ALGORITHM_Execution.md
VALIDATION:      ./VALIDATION_Execution.md
HEALTH:          ./HEALTH_Execution.md
SYNC:            ./SYNC_Execution.md

PARENT CHAIN:    ../daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md
SPEC:            ../../specs/personhood_ladder.json (aspect="execution")
IMPL:            @mind:TODO
```

**Read this chain in order before making changes.** Each doc answers different questions. Skipping ahead means missing context.

---

## PRIMARY OBJECTIVES (ranked)

1. **Score execution quality from topology alone** — Every capability in the execution aspect (14 capabilities, T1-T8) receives a numeric score computed exclusively from the 7 brain topology primitives and universe graph observables. No content is ever read. No LLM judges quality. The math IS the assessment.

2. **Distinguish intention from action** — A citizen who knows the rules (brain has process nodes, value nodes) but doesn't follow them (no behavioral evidence) must score lower than a citizen who acts correctly. The 40/60 brain/behavior split enforces this: doing matters more than knowing.

3. **Produce actionable scores per capability** — Each capability has its own score (0-100). The aspect sub-index is a weighted mean. When a citizen's `exec_verify_before_claim` drops, the intervention message names THAT capability and recommends a specific corrective action — not a vague "execution quality is low."

4. **Scale from foundational (T1) to transcendent (T8)** — T1 capabilities are the floor: read before edit, verify before claim, no duplication. T8 is world-class execution. The scoring formulas must reflect this progression — T1 scores should be achievable by any functioning citizen, T8 scores should require exceptional sustained behavior.

5. **Enable trend detection across days and weeks** — Scores are comparable day over day. Same brain topology + same behavioral history = same score. Deterministic formulas enable meaningful deltas and trend analysis.

## NON-OBJECTIVES

- Judging the QUALITY of code output (we cannot read content — we score the process, not the artifact)
- Replacing code review or human evaluation of work quality
- Scoring execution in adventure universes (dysfunction is narrative there)
- Providing a single "execution score" without per-capability breakdown

## TRADEOFFS (canonical decisions)

- When a capability seems unscorable from topology, we accept `scored: false` rather than inventing a proxy that could mislead. Honest gaps beat false precision.
- When brain signals and behavior signals conflict (high brain, low behavior), behavior wins (60 > 40). What you do defines you more than what you know.
- T1 capabilities are weighted more heavily in the aspect sub-index because they are foundational — a citizen cannot meaningfully score on T5 if T1 is broken.
- We accept that some higher-tier capabilities (T7: quality as identity, T8: world-class) may have weaker behavioral signals and rely more on sustained consistency over time.

## SUCCESS SIGNALS (observable)

- Citizens with high execution scores produce fewer corrections per session (measured by correction moments in universe graph)
- Citizens who follow execution-related recommendations show score improvement within 7 days
- The formula ranking of citizens matches human intuition about who executes well (calibration check)
- No formula produces a score that contradicts observable behavior (e.g., a citizen who never verifies scoring 90 on verify_before_claim)
