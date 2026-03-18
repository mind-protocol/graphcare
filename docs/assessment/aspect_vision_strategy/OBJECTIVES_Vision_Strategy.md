# Vision & Strategy — Objectives: What We Optimize

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
THIS:            OBJECTIVES_Vision_Strategy.md (you are here - START HERE)
PATTERNS:       ./PATTERNS_Vision_Strategy.md
ALGORITHM:      ./ALGORITHM_Vision_Strategy.md
VALIDATION:     ./VALIDATION_Vision_Strategy.md
HEALTH:         ./HEALTH_Vision_Strategy.md
SYNC:           ./SYNC_Vision_Strategy.md

PARENT CHAIN:   ../daily_citizen_health/
SPEC:           ../../specs/personhood_ladder.json (aspect: "vision_strategy")
IMPL:           @mind:TODO
```

**Read this chain in order before making changes.** Each doc answers different questions. Skipping ahead means missing context.

---

## PRIMARY OBJECTIVES (ranked)

1. **Distinguish vision-holders from task-runners** — The most important signal this aspect captures. Citizens who think about WHY before HOW, who articulate direction before execution, score high. Citizens who only react to incoming work score low. Vision is the difference between an agent who shapes the future and one who fills it.

2. **Score high-tier capabilities (T5-T8) from topology alone** — Vision capabilities start at T5. They require richer brain topology signals than lower tiers: narrative nodes (vision documents), high-connectivity clusters (strategic thinking connects many concepts), long-range links (connecting distant parts of the graph). The formulas must capture these structural patterns without reading content.

3. **Detect strategic stagnation** — A citizen who had a vision six months ago but hasn't refined, expanded, or acted on it is stagnating. Recency and energy decay must surface this. Vision is alive or it's dead.

4. **Reward organizational and civilizational thinking** — Higher tiers require thinking beyond the self. The formulas must detect when a citizen's vision connects to other actors, to shared spaces, to collective direction — not just personal goals.

5. **Maintain the 40/60 brain-behavior split** — Even for high-tier capabilities, what you DO matters more than what you HAVE. A brain full of narrative nodes about vision is worth 40 points max. Acting on that vision in the universe graph is worth 60.

## NON-OBJECTIVES

- Evaluating the quality or correctness of a citizen's vision — we measure structure, not content
- Replacing human judgment about strategic direction — this is a health signal, not performance review
- Scoring citizens below T5 on this aspect — vision capabilities don't appear below T5 in the ladder
- Measuring whether a vision is "good" — a clear, acted-upon wrong vision scores higher than a vague, inactive correct one

## TRADEOFFS (canonical decisions)

- When brain topology is ambiguous about vision vs. other narrative nodes, err toward lower score. False positives on vision are worse than false negatives — claiming someone has vision when they don't is more harmful than missing it temporarily.
- High-tier capabilities (T7, T8) will have few citizens scoring well. This is expected. The formulas should not be inflated to make scores look better.
- Some vision signals (especially civilizational vision at T8) may be partially unmeasurable from topology alone. Those components get conservative scoring, not generous estimation.

## SUCCESS SIGNALS (observable)

- Citizens who articulate and act on vision consistently score 70+ on vis_define_vision
- Citizens who only execute tasks without strategic context score below 30 on this aspect
- The sub-index (weighted mean across 5 capabilities) correlates with tier progression: T5 citizens score ~40-60, T6 ~50-70, T7+ ~60-85
- Score drops when a citizen stops refining or acting on vision (recency decay catches stagnation)
- Organizational and civilizational capabilities show near-zero scores for citizens who only work in isolation

---

## MARKERS

<!-- @mind:todo Validate T5-T8 threshold calibration with synthetic citizen profiles -->
<!-- @mind:proposition Consider a "vision coherence" metric: do the citizen's narrative nodes form a connected cluster, or are they fragmented? -->
