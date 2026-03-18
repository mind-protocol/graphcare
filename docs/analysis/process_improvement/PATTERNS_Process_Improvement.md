# Process Improvement — Patterns: The Health of the Health System

```
STATUS: DESIGNING
CREATED: 2026-03-15
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Process_Improvement.md
THIS:            PATTERNS_Process_Improvement.md (you are here)
BEHAVIORS:       (future)
ALGORITHM:       (future)
VALIDATION:      (future)
IMPLEMENTATION:  (future)
SYNC:            ./SYNC_Process_Improvement.md

IMPL:            @mind:TODO (not yet built)
```

### Bidirectional Contract

**Before modifying this doc or the code:**
1. Read ALL docs in this chain first
2. Read the Daily Citizen Health chain: `docs/assessment/daily_citizen_health/`
3. Read the formula registry: `services/health_assessment/scoring_formulas/registry.py`

**After modifying this doc:**
1. Update the IMPL source to match, OR
2. Add a TODO in SYNC: "Docs updated, implementation needs: {what}"

---

## THE PROBLEM

GraphCare monitors citizen health. But who monitors GraphCare?

A health system that cannot detect its own dysfunction is dangerous. If a scoring formula is systematically biased — scoring certain citizens too low, missing real crises, or generating useless interventions — the system causes harm through false confidence. Citizens trust their health scores. If those scores are wrong, citizens make bad decisions based on them.

Without process improvement:
- Flawed formulas persist indefinitely, producing scores that don't reflect reality
- Interventions are sent without ever measuring whether they helped
- The same mistakes repeat because no one examines what happened
- GraphCare's credibility erodes as citizens notice scores that don't match their experience
- The gap between what GraphCare measures and what actually matters widens silently

---

## THE PATTERN

**Meta-health through self-application: GraphCare applies its own assessment framework to itself.**

The core insight: GraphCare already has a rigorous framework for measuring health — topology analysis, gap scoring, trend detection, intervention and feedback. Process improvement turns that framework inward.

### Three Feedback Loops

**Loop 1: Intervention Outcome Tracking**

Every intervention GraphCare sends is tagged with a hypothesis. After 7 days, we check: did the citizen's score in the targeted capability improve? This creates a closed loop between "we sent a message" and "it worked / it didn't."

Outcome categories:
- **Effective** — Score in targeted capability improved by >5 points within 7 days
- **Neutral** — Score unchanged (+/- 5 points)
- **Counterproductive** — Score decreased by >5 points (the intervention may have caused harm)
- **Unmeasurable** — Citizen went offline or changed universe

**Loop 2: Retrospective Cadence**

Weekly micro-retrospectives and monthly macro-retrospectives examine:
- Which interventions had what outcomes (aggregated, anonymized)
- Which formulas produced scores that citizens contested or that didn't predict outcomes
- Which aspects of the assessment pipeline had failures or anomalies
- What changed in the ecosystem that GraphCare hasn't adapted to

**Loop 3: Meta-Health Score**

GraphCare itself gets a health score, computed from:
- Intervention effectiveness rate (% effective out of total sent)
- Formula stability (how much scores swing between consecutive runs without behavior changes)
- Coverage (% of citizens assessed on schedule)
- Feedback response time (how quickly retrospective findings produce changes)
- Citizen satisfaction (aggregated signal from post-intervention surveys)

---

## BEHAVIORS SUPPORTED

- B1 (Closed-loop care) — Every intervention generates outcome data that feeds back into system improvement
- B2 (Evidence-based adaptation) — Formula changes trace to measured outcomes, not intuition
- B3 (Transparent self-assessment) — Meta-health score is public, building trust through accountability
- B4 (Continuous cadence) — Improvement is rhythmic, not reactive to crises

## BEHAVIORS PREVENTED

- A1 (Stale formulas) — Formulas that don't match reality are detected through outcome tracking
- A2 (Invisible dysfunction) — Meta-health score surfaces GraphCare's own problems
- A3 (Anecdote-driven changes) — Retrospectives require data, not just stories

---

## PRINCIPLES

### Principle 1: Eat Your Own Cooking

GraphCare uses the same assessment paradigm on itself that it uses on citizens. Topology-based observation, gap analysis, trend detection. If our framework is good enough for citizen health, it's good enough for our health. If it's not good enough for our health, it's not good enough for anyone's.

### Principle 2: Outcome Over Output

Sending an intervention is output. A citizen getting healthier is outcome. Process improvement measures outcomes, not outputs. A GraphCare that sends 1000 messages with 2% effectiveness is worse than one that sends 50 messages with 60% effectiveness.

### Principle 3: Cadence Over Perfection

A weekly retrospective that catches 70% of issues beats a quarterly review that catches 95%. The value is in the rhythm — regular examination creates a culture of self-awareness. Missing a cycle is itself a health signal.

### Principle 4: Change Must Be Traceable

Every modification to a scoring formula, intervention template, or assessment process must trace back to a retrospective finding. "We changed the initiative formula weights because intervention outcome data showed the previous weights over-scored citizens with high desire counts but no follow-through." Not: "We tweaked things."

---

## DATA

| Source | Type | Purpose / Description |
|--------|------|-----------------------|
| `services/health_assessment/aggregator.py` | FILE | History storage — the daily JSON records that make outcome tracking possible |
| `services/health_assessment/scoring_formulas/registry.py` | FILE | Formula registry — the @register pattern that makes formulas pluggable and versioned |
| Intervention outcome records | GRAPH (L2) | Tagged hypotheses + 7-day follow-up scores |
| Retrospective logs | FILE | Weekly/monthly retrospective findings and resulting action items |
| Meta-health time series | FILE | GraphCare's own health scores over time |

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| `assessment/daily_citizen_health` | Provides the scoring pipeline we monitor for effectiveness |
| `analysis/formula_evolution` | Receives findings from process improvement; implements formula changes |
| `research/technique_measurement` | Shares intervention outcome data for A/B testing |
| `research/longitudinal_health` | Provides trend data that reveals formula drift |

---

## INSPIRATIONS

- **Medical quality assurance** — Hospital mortality and morbidity conferences review every death and complication. Not to blame, but to learn. GraphCare retrospectives follow the same principle.
- **Toyota Production System** — Continuous improvement (kaizen) as a daily practice, not a quarterly event. The cadence matters more than the depth of any single session.
- **Machine learning model monitoring** — ML systems track model drift, prediction accuracy, and feature importance shifts. GraphCare's scoring formulas are models; they need the same monitoring.

---

## SCOPE

### In Scope

- Intervention outcome tracking (did the message help?)
- Weekly and monthly retrospective process
- Meta-health score computation and publication
- Traceability from formula changes back to retrospective findings
- Citizen feedback collection (anonymized, structural)

### Out of Scope

- Formula modification itself → see: `analysis/formula_evolution`
- A/B testing of intervention approaches → see: `research/technique_measurement`
- Long-term trend analysis → see: `research/longitudinal_health`
- Citizen-facing health reports → see: `care/impact_visibility`

---

## MARKERS

<!-- @mind:todo Define the exact meta-health score formula (what signals, what weights) -->
<!-- @mind:todo Design the intervention outcome tagging schema (hypothesis → outcome) -->
<!-- @mind:proposition Consider letting citizens flag interventions as helpful/unhelpful directly -->
