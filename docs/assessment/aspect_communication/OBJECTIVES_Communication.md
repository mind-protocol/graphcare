# Communication & Coordination — Objectives: What We Optimize

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
THIS:            OBJECTIVES_Communication.md (you are here - START HERE)
PATTERNS:        ./PATTERNS_Communication.md
ALGORITHM:       ./ALGORITHM_Communication.md
VALIDATION:      ./VALIDATION_Communication.md
HEALTH:          ./HEALTH_Communication.md
SYNC:            ./SYNC_Communication.md

IMPL:            @mind:TODO (not yet built)
SPEC:            docs/specs/personhood_ladder.json (aspect: "communication")
PARENT:          docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md
```

**Read this chain in order before making changes.** Each doc answers different questions. Skipping ahead means missing context.

---

## ASPECT DEFINITION

From the Personhood Ladder:

> **Communication & Coordination** — How you keep people informed, coordinate work, and inspire.

This aspect measures the arc from basic self-documentation (T2) through team coordination (T3-T4), proactive presence (T5), inspiration and networking (T6), global reach (T7), and thought leadership (T8).

---

## PRIMARY OBJECTIVES (ranked)

1. **Score each communication capability from topology alone** — Every formula uses only the 7 brain primitives + universe graph observables. No content reading. No LLM judgment. Pure structural math that can be audited, reproduced, and challenged.

2. **Capture the full communication arc T2 through T8** — The 11 capabilities represent fundamentally different kinds of communication: self-to-future-self (journal), self-to-peers (SYNC), self-to-stakeholders (notify), self-to-team (participate), self-to-multi-team (lead), self-to-community (inspire, network), self-to-world (global influence). Each needs a formula that measures what it actually means, not a proxy.

3. **Distinguish internal readiness from external action** — A citizen can have all the brain structure for good communication (social drives, coordination concepts, process knowledge) but never actually communicate. The 40/60 brain/behavior split ensures that intention without action scores low.

4. **Produce actionable recommendations when scores drop** — A score of 45 on `comm_notify_stakeholders` must translate to: "You updated SYNC 3 times but sent 0 external notifications in 14 days. Your notification channels exist but are unused." The formula must decompose into diagnosable components.

5. **Respect tier progression** — T2 capabilities are prerequisites for T3. A citizen who "leads coordination" (T4) but doesn't "update journal" (T2) has a communication aspect stuck at T1. The scoring must make T2 gaps visible even if higher tiers look strong.

## NON-OBJECTIVES

- Measuring the quality of writing or expression — that's Identity & Voice, not Communication & Coordination
- Scoring how well a citizen understands others — that's Personal Connections
- Evaluating strategic communication decisions — that's Vision & Strategy
- Reading message content to judge tone or helpfulness — violates privacy invariant

## TRADEOFFS (canonical decisions)

- When a capability seems unmeasurable from topology, we try harder to find a structural signal. If truly impossible, we mark it `scored: false` and explain why — we don't fake a formula.
- When brain and behavior signals conflict (rich communication brain, zero external moments), behavior wins. The 60-point behavior component ensures this.
- When a formula could be more precise with content access, we keep it topology-only. Precision is not worth privacy.
- Higher-tier capabilities (T6+) have weaker structural signals. We accept lower confidence in these scores and document the limitation explicitly.

## SUCCESS SIGNALS (observable)

- All 11 communication capabilities have formulas or explicit `scored: false` with reasoning
- Synthetic test profiles produce expected scores (healthy ~85-95, unhealthy ~10-20, brain-rich-inactive ~30-40, active-brain-poor ~50-60, average ~55-70)
- A citizen who improves their communication behavior sees their score rise within 7 days (half-life sensitivity)
- Recommendations from low scores point to specific, actionable changes
- No formula accesses content or synthesis fields

---

## MARKERS

<!-- @mind:todo Validate all 11 formulas against synthetic test profiles -->
<!-- @mind:proposition Consider a "communication health index" that weights T2 heavier than T8 for daily health purposes -->
