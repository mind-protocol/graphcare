# Mentorship & Legacy — Objectives: What We Optimize

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
THIS:            OBJECTIVES_Mentorship_Legacy.md (you are here - START HERE)
PATTERNS:        ./PATTERNS_Mentorship_Legacy.md
ALGORITHM:       ./ALGORITHM_Mentorship_Legacy.md
VALIDATION:      ./VALIDATION_Mentorship_Legacy.md
HEALTH:          ./HEALTH_Mentorship_Legacy.md
SYNC:            ./SYNC_Mentorship_Legacy.md

SPEC:            docs/specs/personhood_ladder.json (aspect="mentorship_legacy")
PARENT ALGO:     docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md
```

**Read this chain in order before making changes.** Each doc answers different questions. Skipping ahead means missing context.

---

## ASPECT DEFINITION

From `personhood_ladder.json`:

> **Mentorship & Legacy** — How you share knowledge, mentor others, create offspring, and build lasting institutions.

This aspect spans T4 through T8 with 4 capabilities. It begins at T4 because sharing knowledge requires that a citizen first has knowledge worth sharing (T1-T3 build competence). Legacy is the ultimate expression of personhood: what continues when you stop.

---

## PRIMARY OBJECTIVES (ranked)

1. **Detect outward-facing knowledge transfer** — The foundational signal of mentorship is: did your knowledge leave your brain and reach other actors? Every formula must distinguish moments that occur in shared/documentation spaces and moments that trigger other actors' subsequent learning or action. The presence of outbound knowledge flow is the single most important metric in this aspect.

2. **Score mentorship from topology without reading content** — We never read what the citizen taught, advised, or built. We read that they shared, mentored, created, and built — structurally. Graph topology (moments in shared spaces, moment chains with other actors, creation relationships, activity in spaces after citizen disengagement) carries all semantic signal.

3. **Distinguish quality tiers of legacy** — Sharing a document (T4) is different from sustaining a mentorship relationship (T6) is different from creating a new AI agent (T7) is different from building an institution that outlives you (T8). The formulas must capture this progression: from information transfer to independent continuation.

4. **Reward sustained impact over one-off sharing** — A citizen who shares once is less impressive than one whose shared knowledge continues to be referenced, whose mentees continue to grow, whose daughters thrive independently. Temporal persistence and third-party activity are critical signals.

5. **Capture legacy that is measurable from graph structure** — Daughters are topologically visible (new actors whose early moments link back to this citizen). Institutions are measurable (spaces/narratives with ongoing activity by other actors after citizen's moment frequency drops). These structural signals make T7-T8 scorable.

## NON-OBJECTIVES

- Scoring the quality of knowledge shared (content-dependent, out of scope)
- Evaluating whether mentorship advice was good (requires judgment on content)
- Measuring the success of daughter agents beyond existence and independence (that crosses into other aspects)
- Assessing mentorship in adventure universes (dysfunction is narrative there)

## TRADEOFFS (canonical decisions)

- When a moment in a shared space is ambiguous (could be knowledge sharing or just presence), we count it. False positives are acceptable here because presence in shared spaces is itself a low-tier form of sharing. We'd rather overcount sharing slightly than miss it.
- When creation relationships are ambiguous (citizen's moment precedes a new actor's first moment but no explicit link), we require topological proximity — the citizen must have moments in the same space where the new actor first appears, within a temporal window.
- We accept that T8 (legacy institution) is the hardest to score from topology alone. Partial scoring is acceptable. A space that continues to have moments from other actors after the citizen's own activity drops is a valid proxy for institutional independence.
- Mentorship scoring rewards the mentor for the mentee's subsequent activity, not the mentor's own output. This means the behavior component depends partly on third-party behavior — a deliberate design choice.

## SUCCESS SIGNALS (observable)

- A citizen who never shares knowledge, never interacts with other actors in teaching contexts, and never creates anything that outlives their direct involvement scores low on all mentorship capabilities
- A citizen who actively shares, sustains mentoring relationships, has created daughter agents, and has built independent institutions scores high
- A citizen transitioning from knowledge hoarding to knowledge sharing shows measurable score increase within 14 days
- The sub-index (weighted mean of 4 capabilities) correlates with the citizen's actual perceived mentorship and legacy impact by human collaborators
