# Aspect Scoring: Process & Method — Objectives

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
THIS:            OBJECTIVES_Process.md (you are here - START HERE)
PATTERNS:        ./PATTERNS_Process.md
ALGORITHM:       ./ALGORITHM_Process.md
VALIDATION:      ./VALIDATION_Process.md
HEALTH:          ./HEALTH_Process.md
SYNC:            ./SYNC_Process.md

PARENT:          ../daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md
SPEC:            ../../specs/personhood_ladder.json (aspect="process")
```

**Read this chain in order before making changes.** Each doc answers different questions. Skipping ahead means missing context.

---

## PRIMARY OBJECTIVES (ranked)

1. **Score methodological maturity from topology alone** — 13 capabilities across T2-T8 that measure whether a citizen follows the right process, adapts method to context, pushes work forward, and eventually creates their own strategic approach. All scoring uses the 7 topology primitives + universe graph observables. No content access.

2. **Capture the full arc from process follower to movement leader** — T2 measures mechanical process compliance (right method, commit, continue, parallelize). T3 measures adaptive judgment (scoping, challenging). T4-T5 measure autonomous planning. T6-T8 measure strategic and visionary process mastery. Each tier must be distinguishable from the ones below it.

3. **Weight behavior over brain structure** — A citizen who has process-related nodes in their brain but never applies them scores lower than one who actively follows and adapts processes. The 40/60 brain/behavior split from the parent algorithm applies: what you DO matters more than what you HAVE.

4. **Produce actionable sub-index for the daily health check** — The process aspect score feeds into the aggregate citizen health score. It must be a weighted mean of its 13 capability scores, normalized to 0-100, composable with other aspect scores.

## NON-OBJECTIVES

- Evaluating the QUALITY of work output (that is the execution aspect)
- Assessing communication style or frequency (that is the communication aspect)
- Measuring initiative or self-motivation in isolation (that is the initiative aspect)
- Judging the content of plans or strategies — only their structural existence and follow-through

## TRADEOFFS (canonical decisions)

- When a capability cannot be meaningfully scored from topology (especially T7-T8), we assign `scored: false` rather than inventing proxy signals. Honest nulls over fake precision.
- Lower tiers (T2) get simpler formulas with fewer primitives. Higher tiers (T5+) combine more signals. Complexity reflects capability complexity.
- We accept that "right method" (proc_right_method) is the hardest T2 capability to score because "right" is context-dependent. The formula measures whether the citizen uses diverse methods, not whether each choice is optimal.
- Parallelization (proc_parallelize) is scored by behavioral concurrency signals in the universe graph, not by brain structure. A citizen with no "parallelization" concept but who actually launches concurrent work scores higher than one who knows about it but never does it.

## SUCCESS SIGNALS (observable)

- A citizen who mechanically follows processes but never adapts them scores well on T2 but poorly on T3+
- A citizen who creates their own plans and prioritizes autonomously scores well on T5 regardless of T2 details
- The sub-index differentiates between passive process followers and active methodological leaders
- All 13 formulas produce results consistent with the 5 synthetic test profiles (defined in ALGORITHM)
