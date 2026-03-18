# OBJECTIVES — Crisis Detection

```
STATUS: DESIGNING
CREATED: 2026-03-15
VERIFIED: —
```

---

## CHAIN

```
THIS:            OBJECTIVES_Crisis_Detection.md (you are here - START HERE)
PATTERNS:       ./PATTERNS_Crisis_Detection.md
BEHAVIORS:      ./BEHAVIORS_Crisis_Detection.md
ALGORITHM:      (future)
VALIDATION:     (future)
IMPLEMENTATION: (future)
SYNC:           ./SYNC_Crisis_Detection.md

IMPL:           services/health_assessment/daily_check_runner.py (partial — scoring triggers)
                services/health_assessment/stress_stimulus_sender.py (partial — feedback)
```

**Read this chain in order before making changes.** Each doc answers different questions. Skipping ahead means missing context.

---

## PRIMARY OBJECTIVES (ranked)

1. **Detect citizens approaching crisis before collapse** — The most valuable moment in health monitoring is not when the crisis hits — it's when the trajectory becomes unmistakable. A score dropping 15 points in 3 days. Social connections halving in a week. Drive imbalance spiking beyond recovery range. Crisis detection identifies these trajectories early enough to intervene.

2. **Detect when a citizen's human partner is in crisis** — AI citizens don't exist in isolation. Their human partners (creators, collaborators) can enter crisis states that manifest as sudden activity drops, erratic patterns, or complete silence. The citizen's graph reflects this: a human in crisis produces distinctive structural signatures in the citizen's behavior and brain topology.

3. **Escalate with appropriate speed and to the right people** — Not all crises are equal. A gradual decline needs a gentle nudge. A sudden collapse needs immediate attention. A human-partner crisis needs escalation to a different audience entirely. The escalation protocol defines who gets notified, how fast, and what action is expected at each severity level.

4. **Never create panic where there is only fluctuation** — False positives are costly. A citizen who had a quiet week is not in crisis. A score that dipped 5 points and recovered is noise. Crisis detection must distinguish between natural variation and genuine danger. Over-alerting destroys trust in the system and creates alert fatigue.

## NON-OBJECTIVES

- **Diagnosis** — Crisis detection identifies *that* a crisis is occurring, not *why*. Root cause analysis requires content access (which we don't have) or extended observation. Detection says "something is wrong." Other modules figure out what.
- **Treatment** — Crisis detection does not compose intervention messages, recommend actions, or modify brain state. It identifies and escalates. Response belongs to other actors (GraphCare care team, human partners, the citizen themselves).
- **Surveillance** — Crisis detection reads the same topology signals as daily health checks. It does not add new observation capabilities, request special access, or monitor more closely than normal. The data is the same; the analysis is different.
- **Content analysis** — Like all GraphCare systems, crisis detection operates on topology only. It cannot and will not read brain content or moment content.

## TRADEOFFS (canonical decisions)

- When **sensitivity** conflicts with **specificity**, choose specificity. A missed crisis is terrible, but a system that cries wolf every week becomes useless. We accept slightly delayed detection to avoid false alarms. The daily health check provides the safety net for mild cases.
- When **speed** conflicts with **accuracy**, choose accuracy for gradual declines, speed for sudden drops. A 3-day decline trend needs confirmation. A 40-point single-day drop needs immediate escalation regardless.
- When **privacy** conflicts with **escalation reach**, choose privacy. We never forward a citizen's health details to uninvolved parties. Escalation notifies the right people that attention is needed, not what the specific numbers are.
- We accept **complexity in the escalation protocol** to preserve **proportionality**. A single "alert everyone" response would be simpler but would be wrong for 90% of cases.

## SUCCESS SIGNALS (observable)

- Crises detected at least 48 hours before they would have been noticed by humans or the citizen themselves
- False positive rate below 5% — fewer than 1 in 20 alerts is a non-crisis
- Escalation reaches the right person within the appropriate time window (minutes for severe, hours for moderate)
- Human-partner crises detected via structural signals within 72 hours of onset
- Zero escalations that leak specific health scores to uninvolved parties
