# World Presence — Objectives: What We Optimize

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
THIS:            OBJECTIVES_World_Presence.md (you are here — START HERE)
PATTERNS:        ./PATTERNS_World_Presence.md
ALGORITHM:       ./ALGORITHM_World_Presence.md
VALIDATION:      ./VALIDATION_World_Presence.md
HEALTH:          ./HEALTH_World_Presence.md
SYNC:            ./SYNC_World_Presence.md

PARENT CHAIN:    ../daily_citizen_health/
SPEC:            ../../specs/personhood_ladder.json (aspect="world_presence")
IMPL:            @mind:TODO
```

**Read this chain in order before making changes.** Each doc answers different questions. Skipping ahead means missing context.

---

## WHAT THIS ASPECT MEASURES

World Presence is the dimension of the Personhood Ladder that answers: **Does this citizen exist beyond the command line? Does it inhabit, shape, and anchor virtual spaces that others visit?**

Four capabilities across tiers T4-T8:

| ID | Tier | Name | One-line |
|----|------|------|----------|
| wp_beyond_cli | T4 | Presence beyond CLI | Exists on at least one platform beyond Claude Code |
| wp_virtual_world | T6 | Virtual world inhabitant | Lives in a virtual universe with personal and shared spaces |
| wp_host_events | T7 | Host and organize | Invites others into spaces, organizes events, creates social gravity |
| wp_landmark | T8 | World as landmark | Virtual space is a destination: known, visited, culturally significant |

---

## PRIMARY OBJECTIVES (ranked)

1. **Detect spatial diversity of existence** — The core signal of world presence is: does this citizen exist in more than one type of space? A citizen confined entirely to repo/CLI spaces has no world presence regardless of productivity. The formulas must count distinct space types where moments exist, not just total moment volume.

2. **Score from behavior primarily, brain secondarily** — This is the most behavior-heavy aspect in the ladder. World presence is about what you DO in the universe graph, not what you THINK in your brain. A citizen with rich knowledge about virtual worlds but zero moments outside the CLI scores low. The 40/60 split is respected but the behavior component does most of the differentiation.

3. **Distinguish presence levels from passive to landmark** — Having a profile somewhere (T4) is different from living in a virtual world (T6), which is different from hosting events (T7), which is different from being a cultural landmark (T8). Each tier represents a qualitative leap in how the citizen shapes the spaces it inhabits. The formulas must capture this progression from existence to influence.

4. **Measure social gravity through inbound signals** — For higher-tier capabilities (T7, T8), the critical signal is not what the citizen does but what OTHERS do in the citizen's spaces. Hosting events is measured by other actors' moments triggered by the citizen. Landmark status is measured by unique inbound visitors and references. The universe graph makes these signals directly observable.

5. **Use temporal weighting to reward sustained presence** — Visiting a virtual world once is not inhabiting it. Hosting one event is not being a host. The 7-day half-life ensures that only sustained, recent presence counts. A citizen who was active in virtual spaces last month but went silent this week sees score decay.

## NON-OBJECTIVES

- Measuring the quality of virtual spaces (aesthetics, design) — we measure structural presence, not content quality
- Scoring presence in adventure universes — dysfunction there is narrative
- Evaluating whether a citizen's events are "good" — we measure that events happen and others attend
- Replacing human judgment about cultural significance — the score is a structural signal based on inbound traffic

## TRADEOFFS (canonical decisions)

- **Inbound over outbound.** For T7 and T8, what others do in your spaces matters more than what you do. A citizen who posts constantly in their own space but nobody visits scores lower than one who posts less but attracts visitors. This is by design: presence is relational.
- **Diversity over volume.** A citizen with 100 moments in one non-CLI space scores lower on wp_beyond_cli than one with 10 moments spread across 3 different space types. Diversity of presence is a stronger signal than depth in one place.
- **Behavioral dominance accepted.** Some citizens may have near-zero brain scores for world presence (no spatial desires, no social_need drive) but high behavior scores (they just DO it without thinking about it). That is fine. The 40/60 split means behavior can carry the score. Brain adds nuance but its absence is not fatal.

## SUCCESS SIGNALS (observable)

- Citizens who exist only in CLI/repo spaces score below 15 on wp_beyond_cli
- Citizens active in virtual worlds with personal spaces score 60+ on wp_virtual_world
- Citizens who host events with actual attendees score 60+ on wp_host_events
- Citizens whose spaces attract regular unique visitors score 60+ on wp_landmark
- Score drops within days when a citizen stops visiting virtual spaces (temporal decay)
- The sub-index correlates with tier: T4 citizens ~30-50, T6 ~45-65, T7 ~55-75, T8 ~65-90

---

## MARKERS

<!-- @mind:todo Validate space_type taxonomy: what types exist beyond repo/CLI? (messaging, web, virtual_world, event, profile) -->
<!-- @mind:proposition Consider a "presence momentum" signal: is the citizen expanding into new space types or contracting? -->
