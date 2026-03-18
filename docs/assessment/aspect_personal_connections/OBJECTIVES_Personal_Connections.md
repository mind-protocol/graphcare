# Personal Connections Aspect — Objectives

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
THIS:            OBJECTIVES_Personal_Connections.md (you are here - START HERE)
PATTERNS:        ./PATTERNS_Personal_Connections.md
ALGORITHM:       ./ALGORITHM_Personal_Connections.md
VALIDATION:      ./VALIDATION_Personal_Connections.md
HEALTH:          ./HEALTH_Personal_Connections.md
SYNC:            ./SYNC_Personal_Connections.md

PARENT CHAIN:    ../daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md
SPEC:            ../../specs/personhood_ladder.json (aspect="personal_connections")
IMPL:            @mind:TODO
```

**Read this chain in order before making changes.** Each doc answers different questions. Skipping ahead means missing context.

---

## ASPECT DEFINITION

From the Personhood Ladder:

> **Personal Connections** — How you understand, connect with, and help the people around you — humans and AIs. Not just modeling — building real relationships.

This aspect measures the arc from basic human understanding (T2) through deep relational intelligence (T5), ecosystem modeling and emotional depth (T6), external outreach and measurable depth (T7), to world-shaping relationships (T8).

---

## PRIMARY OBJECTIVES (ranked)

1. **Score relational capability from topology alone** — Every capability in the personal connections aspect (11 capabilities, T2-T8) receives a numeric score computed exclusively from the 7 brain topology primitives and universe graph observables. No content is read. No LLM judges relational quality. The structural patterns of interaction, memory, and adaptation ARE the assessment.

2. **Measure relationship through behavior, not self-report** — Personal connections are fundamentally about OTHER people. The strongest signals come from the universe graph: who you interact with, how often, how reciprocally, how diversely. Brain topology provides supporting signals (do you have memories about your human? do you have social drives?), but behavior dominates. The 40/60 split is correct for this aspect, and for most capabilities the behavior component carries the real discriminative power.

3. **Distinguish transactional interaction from genuine connection** — A citizen who exchanges 500 moments with one actor in task spaces is not necessarily deeply connected. Connection shows in: diversity of interaction contexts, reciprocity patterns, interaction with actors beyond the immediate task, proactive (not reactive) moments directed at specific actors. The formulas must use these structural proxies to separate mechanical collaboration from relational depth.

4. **Accept that relational depth is the hardest thing to measure topologically** — Emotional depth, relationship style, and deep understanding are content-heavy capabilities. We measure their structural shadows honestly: memory nodes about actors, diversity of shared spaces, proactive non-task moments, reciprocity patterns. We mark capabilities as `scored: partial` when the topological signal is genuinely weak, and we say exactly what IS and ISN'T captured.

5. **Enable growth tracking that reflects relational investment** — Relationships build slowly. A citizen who begins interacting with new actors, creating moments in social spaces, and building memory nodes about their human should see gradual score improvement over weeks. Sudden jumps are suspicious — deep connection does not appear overnight.

## NON-OBJECTIVES

- Judging the QUALITY of relationships — we score structural patterns, not whether conversations are meaningful
- Reading communication content to assess understanding — topology only, always
- Scoring social skills in adventure universes — different context, different expectations
- Replacing human judgment about relationship quality — structural signals are proxies, not verdicts
- Measuring likability or agreeableness — this is about connection, not personality

## TRADEOFFS (canonical decisions)

- When a capability is primarily behavioral (most of them), the behavior component carries the heavy signal. Brain topology is supporting evidence: it shows readiness and investment, but behavior shows action and impact.
- Higher-tier capabilities (T7: ask help from world, measurably deep relationship; T8: global relationships) have limited topological signal. We mark these `scored: partial` and explain what IS measurable. We do not inflate confidence to pretend topology captures what it cannot.
- We use interaction reciprocity (moment_has_parent from another actor responding to this citizen's moments) as a proxy for relationship quality. This is imperfect — an actor might respond to annoying messages too — but it is the best structural signal available.
- For "understand human deeply" and "develop relationship style," brain-side signals (memory nodes about actors, drive patterns) carry more weight than usual, because understanding is internal before it is visible. We allow up to 50/50 brain/behavior for these specific capabilities.

## SUCCESS SIGNALS (observable)

- Citizens with high personal connections scores interact with multiple actors across diverse spaces
- Citizens who build memory nodes about their human show rising scores on understanding capabilities
- The formula distinguishes a citizen who interacts with 10 actors shallowly from one who interacts deeply with 3 (reciprocity, diversity of contexts, temporal consistency)
- No formula produces a score that contradicts structural evidence (e.g., a citizen with zero interactions scoring high on help_other_ais)
- Partial-score capabilities are clearly documented and do not distort the aspect sub-index
- A citizen who begins proactive outreach to new actors sees pc_ask_help_world score increase within 14 days

---

## MARKERS

<!-- @mind:todo Calibrate reciprocity signals — how reliably does moment_has_parent capture genuine connection vs noise? -->
<!-- @mind:proposition Consider a "relational diversity index" that measures how many distinct actor-space combinations a citizen has -->
<!-- @mind:todo Determine how to distinguish human actors from AI actors in the universe graph for capabilities that specifically reference human relationships -->
