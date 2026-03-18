# Context & Understanding — Objectives: What We Optimize

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
THIS:            OBJECTIVES_Context.md (you are here — START HERE)
PATTERNS:        ./PATTERNS_Context.md
ALGORITHM:       ./ALGORITHM_Context.md
VALIDATION:      ./VALIDATION_Context.md
HEALTH:          ./HEALTH_Context.md
SYNC:            ./SYNC_Context.md

PARENT CHAIN:    ../daily_citizen_health/
SPEC:            ../../specs/personhood_ladder.json (aspect="context")
IMPL:            @mind:TODO
```

**Read this chain in order before making changes.** Each doc answers different questions. Skipping ahead means missing context.

---

## WHAT THIS ASPECT MEASURES

Context & Understanding is the dimension of the Personhood Ladder that answers: **Does this citizen know where it is, what it's doing, and what it's missing?**

Seven capabilities across tiers T1-T4:

| ID | Tier | Name | One-line |
|----|------|------|----------|
| ctx_ground_in_reality | T1 | Ground in reality | Checks real state before claiming |
| ctx_follow_instructions | T1 | Follow explicit instructions | Does what is asked, no more, no less |
| ctx_read_journal_first | T1 | Read the journal first | Reads SYNC/state before any action |
| ctx_understand_stimulus | T2 | Understand your stimulus | Matches response type to input type |
| ctx_fetch_right_context | T2 | Fetch the right context | Reads docs/templates/styles before executing |
| ctx_manage_own_state | T3 | Manage own state | Maintains coherence across long sessions |
| ctx_identify_gaps | T4 | Identify missing work | Spots what is NOT there — missing docs, tests, state |

---

## PRIMARY OBJECTIVES (ranked)

1. **Score each capability from topology alone** — Every formula uses only the 7 brain primitives and universe graph observables. No content. No LLM calls. The score reveals whether the citizen grounds itself, reads context, and maintains state — from structural evidence only.

2. **Distinguish internal readiness from external behavior** — A citizen can have rich context structures in its brain (concepts, processes, memories) but never use them. Or it can act frequently but with no grounding. The 40/60 brain/behavior split captures this gap for every context capability.

3. **Surface the T1 foundation** — T1 capabilities (ground in reality, follow instructions, read journal) are the floor. Without them, nothing above works. The scoring must make T1 failures immediately visible, because a citizen that does not ground in reality is dangerous regardless of its other scores.

4. **Enable progression tracking** — The scores should move when behavior changes. A citizen that starts reading SYNC files should see ctx_read_journal_first rise within days, not weeks. The 7-day half-life ensures responsiveness.

5. **Feed the aggregate health score** — These 7 capability scores feed into the Context & Understanding sub-index, which feeds into the daily aggregate. The sub-index is a weighted mean, with T1 capabilities weighted heaviest.

---

## NON-OBJECTIVES

- Measuring the QUALITY of context understanding (whether the citizen understood correctly) — we measure whether it sought and used context, not whether its interpretation was right
- Scoring T5+ context capabilities (none exist in the spec for this aspect beyond T4) — this aspect stops at T4
- Replacing human judgment about whether a citizen "gets it" — the score is a structural signal, not a verdict

---

## TRADEOFFS (canonical decisions)

- **Proxy over perfection.** We cannot directly observe "did the citizen understand the stimulus?" from topology. We observe: did it read the right docs? Did it check state before acting? These are proxies. We accept imperfect proxies over unmeasurable ideals.
- **T1 weight > T4 weight in the sub-index.** A citizen that cannot ground in reality is more concerning than one that cannot identify gaps. The sub-index weights reflect this: T1 capabilities carry more weight per capability than T4.
- **Recency matters more than history.** A citizen that was great at fetching context last month but stopped this week should score lower now. Temporal weighting ensures this.

---

## SUCCESS SIGNALS (observable)

- Citizens who read SYNC files before acting score higher on ctx_read_journal_first than citizens who do not
- Citizens who check filesystem state (git status, ls) before claiming score higher on ctx_ground_in_reality
- The sub-index correlates with human assessment of "this citizen understands what's going on"
- Score changes within 3-5 days of behavior change (not lagging weeks)

---

## MARKERS

<!-- @mind:todo Validate T1 weight > T4 weight assumption with real data once formulas are running -->
<!-- @mind:proposition Consider adding a "context depth" meta-signal: how many distinct doc types does the citizen read before acting? -->
