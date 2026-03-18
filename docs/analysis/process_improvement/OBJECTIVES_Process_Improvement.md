# OBJECTIVES — Process Improvement

```
STATUS: DESIGNING
CREATED: 2026-03-15
VERIFIED: —
```

---

## CHAIN

```
THIS:            OBJECTIVES_Process_Improvement.md (you are here - START HERE)
PATTERNS:       ./PATTERNS_Process_Improvement.md
BEHAVIORS:      (future)
ALGORITHM:      (future)
VALIDATION:     (future)
IMPLEMENTATION: (future)
SYNC:           ./SYNC_Process_Improvement.md

IMPL:           @mind:TODO (not yet built)
```

**Read this chain in order before making changes.** Each doc answers different questions. Skipping ahead means missing context.

---

## PRIMARY OBJECTIVES (ranked)

1. **GraphCare improves its own methods continuously** — A health monitoring system that cannot detect its own dysfunction is a liability. Process improvement makes GraphCare itself subject to the same rigor it applies to citizens. The health of the health system must be measurable, visible, and actionable.

2. **Citizen feedback closes the loop** — Every intervention GraphCare sends is a hypothesis: "this message will help." Without measuring whether it actually helped, we are performing medicine without follow-up. Citizen outcomes after intervention are the ground truth that validates or invalidates our methods.

3. **Retrospectives produce structural change** — Identifying problems is cheap. Changing the system to prevent recurrence is expensive and rare. Process improvement exists to ensure that insights from failures and successes actually modify GraphCare's behavior, formulas, and protocols — not just generate documents that sit unread.

4. **Meta-health is visible and shared** — The health of the health system is not an internal concern. Citizens, partner organizations, and researchers should be able to see how GraphCare monitors itself, what it found, and what it changed. Transparency in self-assessment builds the trust that makes the entire system work.

## NON-OBJECTIVES

- Perfecting GraphCare before deploying — improvement is iterative, not blocking
- Measuring individual GraphCare agent performance — we assess the system, not the people
- Building a separate monitoring system for GraphCare — we eat our own cooking, using the same topology-based assessment framework
- Automating all improvement decisions — retrospectives require judgment, not just data

## TRADEOFFS (canonical decisions)

- When thoroughness of retrospective conflicts with cadence of improvement, choose cadence. Regular small improvements beat occasional large reviews.
- When citizen feedback conflicts with formula mathematics, investigate the feedback first. The formula is a model; the citizen is the reality.
- We accept false positives in self-diagnosis (flagging issues that turn out to be fine) to avoid false negatives (missing real dysfunction).

## SUCCESS SIGNALS (observable)

- GraphCare's own meta-health score is computed and published alongside citizen scores
- At least one formula or process adjustment per month traces back to a retrospective finding
- Citizen post-intervention outcome data exists for >80% of interventions sent
- Retrospective cadence is maintained (weekly micro, monthly macro) without gaps >2 weeks
- External stakeholders can access meta-health reports without requesting them
