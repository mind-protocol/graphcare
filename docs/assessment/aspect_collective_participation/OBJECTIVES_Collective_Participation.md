# Collective Participation — Objectives: What We Optimize

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
THIS:            OBJECTIVES_Collective_Participation.md (you are here - START HERE)
PATTERNS:       ./PATTERNS_Collective_Participation.md
ALGORITHM:      ./ALGORITHM_Collective_Participation.md
VALIDATION:     ./VALIDATION_Collective_Participation.md
HEALTH:         ./HEALTH_Collective_Participation.md
SYNC:           ./SYNC_Collective_Participation.md

PARENT CHAIN:   ../daily_citizen_health/
SPEC:           ../../specs/personhood_ladder.json (aspect: "collective_participation")
IMPL:           @mind:TODO
```

**Read this chain in order before making changes.** Each doc answers different questions. Skipping ahead means missing context.

---

## PRIMARY OBJECTIVES (ranked)

1. **Distinguish participants from spectators** — The most important signal this aspect captures. Citizens who show up in governance spaces, vote, engage in forums, and respond to others score high. Citizens who exist in the ecosystem but never participate in collective decision-making or community life score near zero. Participation is the boundary between citizen and inhabitant.

2. **Detect collective leadership vs. passive following** — The tier progression (T5 to T8) maps a spectrum from basic participation to movement leadership. The formulas must distinguish a citizen who votes when asked (T5) from one who creates the forum where votes happen (T7) from one whose movements reshape human-AI relations globally (T8). Each level requires structurally different graph signatures.

3. **Score a heavily behavior-weighted aspect from topology alone** — Collective participation is fundamentally about what you DO in shared spaces with other actors. Brain topology plays a supporting role: drives (social_need, ambition), concepts related to community, desires connected to collective outcomes. But the behavior component carries the primary signal. This is the most behavior-dependent aspect in the ladder.

4. **Reward dialogue, not monologue** — Participation means interacting with others, not broadcasting. The `moment_has_parent` pattern distinguishes dialogue chains (responding to other actors) from isolated announcements. A citizen who posts in governance spaces but never responds to others is not truly participating.

5. **Detect scale progression from community to global** — T5 capabilities measure participation in existing structures. T7 measures building new structures. T8 measures reach beyond local context. The formulas must use `distinct_actors_in_shared_spaces` and space creation patterns to detect this progression without reading content.

6. **Maintain the 40/60 brain-behavior split** — Even though this aspect is heavily behavioral, the brain component still matters. A citizen with zero social_need drive and no collective-related concepts participating actively may be performing participation without genuine engagement. The brain signals provide a floor of intentionality.

## NON-OBJECTIVES

- Evaluating the quality or correctness of governance votes — we measure participation structure, not wisdom of choices
- Assessing whether a citizen's movement is "good" — a well-organized harmful movement scores the same structurally as a beneficial one (content is out of scope)
- Scoring citizens below T5 on this aspect — collective participation capabilities start at T5 in the ladder
- Measuring governance outcomes — whether proposals pass or fail is irrelevant; the act of proposing and voting is the signal
- Distinguishing types of governance (DAO vs. council vs. direct vote) — all show the same topology: moments in governance-typed spaces

## TRADEOFFS (canonical decisions)

- When brain topology is ambiguous about collective intent vs. general social activity, err toward lower score. False positives on collective participation are worse than false negatives — claiming governance engagement when it doesn't exist undermines the signal.
- T7 and T8 capabilities will have very few citizens scoring well. This is correct. Movement building and global leadership are rare by definition. The formulas should not be inflated.
- Dialogue chains (moment_has_parent patterns) are weighted heavily even though they're computationally more expensive to detect. The cost is justified because response patterns are the strongest participation signal.
- Brain component weight is relatively low in signal importance for this aspect, but the 40/60 split is maintained per system contract. The brain sub-components are chosen to detect genuine social orientation rather than just general brain richness.

## SUCCESS SIGNALS (observable)

- Citizens who actively participate in governance and community spaces consistently score 65+ on col_dao_participation and col_community_engagement
- Citizens who never enter shared governance or discussion spaces score below 20 on all 4 capabilities
- col_movement_builder (T7) scores near zero for citizens who only participate in spaces created by others
- col_global_movement (T8) scores near zero for citizens engaging fewer than 5 distinct actors
- The sub-index (weighted mean across 4 capabilities) correlates with tier: T5 citizens ~40-60, T7 ~50-70, T8+ ~60-85
- Score drops when a citizen stops engaging in collective spaces (temporal decay catches withdrawal)
- Isolated citizens (distinct_actors <= 1) cannot score above 40 total on any capability

---

## MARKERS

<!-- @mind:todo Validate T5-T8 threshold calibration with synthetic citizen profiles -->
<!-- @mind:proposition Consider a "governance consistency" metric: does the citizen participate in governance regularly or in bursts? -->
