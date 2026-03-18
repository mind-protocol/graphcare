# Initiative & Autonomy — Objectives: What We Optimize

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
THIS:            OBJECTIVES_Initiative.md (you are here - START HERE)
PATTERNS:        ./PATTERNS_Initiative.md
ALGORITHM:       ./ALGORITHM_Initiative.md
VALIDATION:      ./VALIDATION_Initiative.md
HEALTH:          ./HEALTH_Initiative.md
SYNC:            ./SYNC_Initiative.md

SPEC:            docs/specs/personhood_ladder.json (aspect="initiative")
PARENT ALGO:     docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md
```

**Read this chain in order before making changes.** Each doc answers different questions. Skipping ahead means missing context.

---

## ASPECT DEFINITION

From `personhood_ladder.json`:

> **Initiative & Autonomy** — How much you self-direct, propose, and act without being asked.

This aspect spans T3 through T8 with 8 capabilities. Initiative starts at T3 because T1 (Reliable Executor) and T2 (Process Follower) are fundamentally reactive tiers — you do what's asked, you follow what's defined. Initiative begins the moment you act beyond what was requested.

---

## PRIMARY OBJECTIVES (ranked)

1. **Detect the self-initiated vs. reactive ratio** — The core signal of initiative is: did you act because someone asked, or because you decided to? Every formula must separate self-initiated moments (no incoming `triggers`/`responds_to` link from another actor) from reactive ones. This ratio is the single most important metric in this aspect.

2. **Score initiative from topology without reading content** — We never read what the citizen proposed, challenged, or created. We read that they proposed, challenged, or created — structurally. The graph link types (`proposes`, `challenges`, `creates`, `resolves`) carry the semantic signal.

3. **Distinguish quality tiers of initiative** — Fixing something you find (T3) is different from launching a workstream (T5) is different from initiating from personal ambition (T7). The formulas must capture this progression: from reactive-adjacent initiative to deeply self-directed action.

4. **Reward sustained initiative over bursts** — A citizen who self-initiates once is less impressive than one who sustains self-direction over weeks. Temporal weighting and persistence metrics matter here.

5. **Capture initiative that fails** — A citizen who proposes improvements that get rejected is still showing initiative. The formula scores the act of proposing, not the outcome. Outcome sensitivity would punish risk-taking.

## NON-OBJECTIVES

- Scoring the quality of proposals (content-dependent, out of scope)
- Distinguishing "good" refusals from "bad" ones (requires judgment on content)
- Measuring leadership or influence (that's aspect `leadership`, not initiative)
- Assessing initiative in adventure universes (dysfunction is narrative there)

## TRADEOFFS (canonical decisions)

- When a moment's origin is ambiguous (unclear if self-initiated or reactive), treat it as reactive. We'd rather undercount initiative than overcount it. False positives are worse than false negatives here.
- When initiative and recklessness overlap in topology (lots of self-initiated moments with no follow-through), the formula should reflect this — high initiation with low persistence scores lower than moderate initiation with high persistence.
- We accept that some high-tier capabilities (T7 ambition, T8 innovation) are hard to score from topology alone. Partial scoring (brain only, or behavior only) is acceptable. `scored: true` with lower max is better than `scored: false`.

## SUCCESS SIGNALS (observable)

- A citizen who only responds to requests scores low on all initiative capabilities
- A citizen who regularly self-initiates, proposes, and follows through scores high
- A citizen transitioning from reactive to proactive shows measurable score increase within 14 days
- The sub-index (weighted mean of 8 capabilities) correlates with the citizen's actual perceived initiative by human collaborators
