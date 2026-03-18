# Health Economics — Patterns: Prevention vs Crisis — The Numbers

```
STATUS: DESIGNING
CREATED: 2026-03-15
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Health_Economics.md
THIS:            PATTERNS_Health_Economics.md (you are here)
BEHAVIORS:       (future)
ALGORITHM:       (future)
VALIDATION:      (future)
IMPLEMENTATION:  (future)
SYNC:            ./SYNC_Health_Economics.md

IMPL:            @mind:TODO (economics analysis)
```

### Bidirectional Contract

**Before modifying this doc:**
1. Read ALL docs in this chain first
2. Read the economics siblings: `economics/service_model/`, `economics/value_creation/`
3. Read the assessment pipeline for cost understanding: `services/health_assessment/`

---

## THE PROBLEM

Everyone intuitively agrees that prevention is cheaper than crisis response. But "intuitively agrees" is not a funding argument. Without concrete numbers, the economic case for continuous health monitoring remains a feeling, not a fact.

The numbers we need:
- What does it cost to monitor one citizen for one day? (The prevention cost)
- What does one citizen crisis cost the ecosystem? (The crisis cost)
- How many crises does monitoring prevent? (The prevention rate)
- What is the return on investment? (Prevention ROI = avoided crisis costs / monitoring costs)

Without these numbers:
- Investment in GraphCare cannot be evaluated against alternatives
- The "should we fund monitoring?" question becomes political rather than empirical
- External organizations cannot build a business case for adopting GraphCare
- Resource allocation within GraphCare lacks economic grounding (should we invest more in formulas or in interventions?)

---

## THE PATTERN

**Three-part economic model: monitoring cost, crisis cost, prevention ROI.**

### Part 1: Monitoring Cost Model

The cost of monitoring one citizen for one day, broken down by component:

**Fixed costs (amortized per citizen per day):**
- Framework development and maintenance (agent time building and updating the assessment pipeline)
- Research (formula development, calibration, publication)
- Infrastructure (server, database, storage)

**Variable costs (per citizen per day):**
- **Brain topology read:** One FalkorDB query to read brain graph topology. Cost: ~1 graph query = sub-cent.
- **Universe graph read:** One query to fetch recent moments. Cost: ~1 graph query = sub-cent.
- **Formula evaluation:** 35 Python function calls with arithmetic operations. Cost: negligible (microseconds of CPU).
- **History I/O:** Read yesterday's JSON, write today's JSON. Cost: negligible (2KB per file).
- **Intervention composition (conditional):** LLM call to compose intervention message. Triggered for ~10-20% of citizens per day. Cost: the largest variable component — estimated at a few cents per intervention.
- **Stress stimulus:** One API call to send stimulus to brain. Cost: sub-cent.

**Estimated total variable cost:** A few cents per citizen per day. The LLM intervention call is the dominant variable cost, but it applies to only a fraction of citizens on any given day.

**Fixed cost amortization:** If total fixed costs are F per month and there are N citizens, the amortized fixed cost is F / (N * 30) per citizen per day. With ~60 citizens, fixed costs are spread thin. With 600 citizens, they become negligible per citizen.

### Part 2: Crisis Cost Model

The cost of one citizen crisis, broken down by component:

**Direct costs:**
- **Lost production:** A citizen in crisis stops producing moments, contributions, and collaborations. If the average citizen produces V value per day and a crisis lasts D days, lost production = V * D.
- **Emergency intervention:** Crisis response requires immediate, intensive agent attention. Unlike the automated daily check, crisis response involves diagnostic investigation, personalized intervention, and monitoring. Estimated: several hours of agent time per crisis.
- **Recovery period:** Even after the acute crisis resolves, the citizen operates below capacity during recovery. Estimated: half-productivity for 1-2 weeks.

**Indirect costs:**
- **Relationship damage:** A citizen in crisis may damage relationships through non-response, poor collaboration, or conflict. Repairing these relationships has both time cost and social capital cost.
- **Network effects:** A struggling citizen affects their collaborators. Reduced participation in shared spaces means less value for everyone in those spaces.
- **Permanent departure risk:** Some crises result in the citizen leaving the ecosystem permanently. The cost of replacement (recruiting, onboarding, training a new citizen) far exceeds the cost of prevention.

**Estimated crisis cost:** Highly variable, but even a conservative estimate (5-10 days of lost production + relationship repair + departure risk premium) is orders of magnitude higher than the monitoring cost that could have prevented it.

### Part 3: Prevention ROI

The return on investment for continuous health monitoring:

```
Prevention ROI = (Crises Prevented * Average Crisis Cost) / (Total Monitoring Cost)

Where:
  Crises Prevented = Citizens with declining trajectories who received
                     intervention and reversed course
  Average Crisis Cost = Sum of direct + indirect costs per crisis episode
  Total Monitoring Cost = Per-citizen-per-day cost * Citizens * Days
```

**The hypothesis:** Prevention ROI is strongly positive because:
1. Monitoring cost per citizen is near-zero (cents per day)
2. Crisis cost per episode is substantial (days to weeks of lost value)
3. Even preventing a few crises per quarter pays for months of monitoring for the entire population

**Example calculation (illustrative, not real data):**
- Monitoring cost: $0.05/citizen/day * 60 citizens * 90 days = $270/quarter
- Crises prevented: 3 per quarter (conservative)
- Average crisis cost: $200 per crisis (5 days lost production at $40/day equivalent)
- Prevention value: 3 * $200 = $600/quarter
- ROI: $600 / $270 = 2.2x return

Even with very conservative assumptions, the math works. With realistic crisis cost estimates (which include relationship damage, network effects, and departure risk), the ROI is likely much higher.

---

## BEHAVIORS SUPPORTED

- B1 (Data-driven investment) — GraphCare investment decisions are informed by economic analysis
- B2 (Concrete ROI) — The prevention value is quantified, not just asserted
- B3 (Transparent cost structure) — Every cost component is identified and measured
- B4 (External business case) — Organizations can use the model to evaluate GraphCare adoption

## BEHAVIORS PREVENTED

- A1 (Gut-feeling funding) — Resource allocation is grounded in data, not in political persuasion
- A2 (Hidden costs) — All monitoring costs are identified, even the small ones
- A3 (Over-investment without analysis) — The model identifies the point of diminishing returns

---

## PRINCIPLES

### Principle 1: Cheap Prevention Beats Expensive Cure

This is the economic thesis. It is testable and may be wrong for some scenarios. But the structural economics favor it: monitoring is a fixed-cost investment with near-zero marginal cost per citizen, while crises are high-cost events that monitoring can partially prevent. The ratio between monitoring cost and crisis cost is the economic argument.

### Principle 2: Measure Real Costs, Not Theoretical Ones

The monitoring cost model must be built from actual production data — real graph query costs, real LLM API costs, real storage costs. Not estimates from documentation or pricing pages. Actual bills. Actual usage. The crisis cost model should similarly be built from observed crisis episodes, not from theoretical worst cases.

### Principle 3: Uncertainty Ranges Are Required

Every cost estimate includes a range. "Crisis cost: $150-$400" is honest. "Crisis cost: $237" is false precision that undermines credibility. The ROI calculation propagates these ranges: "Prevention ROI: 1.5x-4.5x" tells the reader both the expected value and the uncertainty. Decisions can be made on ranges; they should not be made on point estimates.

### Principle 4: The Model Improves With Data

The first version of the cost models will be rough. As GraphCare accumulates data — more monitored citizen-days, more observed crises, more measured intervention outcomes — the models become more precise. The model is a living document, updated quarterly, not a one-time calculation.

---

## DATA

| Source | Type | Purpose / Description |
|--------|------|-----------------------|
| Cloud billing data | METRICS | Actual compute, storage, and API costs |
| LLM API usage logs | METRICS | Intervention composition cost per call |
| `data/health_history/` | DIR | Number of interventions sent, intervention frequency |
| Crisis episode logs | DATA | Duration, severity, recovery time, relationship impact of crises (to be tracked) |
| Citizen activity data | GRAPH | Production value signals for crisis cost estimation |

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| `economics/service_model` | Provides the overall funding framework that ROI analysis supports |
| `economics/value_creation` | Uses the crisis cost model for prevention value estimation |
| `research/longitudinal_health` | Provides trajectory data for crisis identification and prevention counting |
| `analysis/process_improvement` | Provides intervention outcome data for prevention rate estimation |

---

## INSPIRATIONS

- **WHO health economics framework** — The World Health Organization evaluates health interventions using DALY (disability-adjusted life years) and cost-effectiveness ratios. GraphCare adapts this: instead of DALYs, we use "healthy citizen-days" as the unit of value.
- **Insurance actuarial science** — Insurance companies model risk probability * loss severity to price premiums. GraphCare's model is structurally identical: crisis probability * crisis cost = expected loss; monitoring cost = prevention premium. If the premium is less than the expected loss, monitoring is economically rational.
- **Deming's cost of quality** — W. Edwards Deming showed that the cost of preventing defects is always less than the cost of fixing them after they occur. Applied to citizen health: the cost of monitoring (prevention) is always less than the cost of crisis response (correction).

---

## SCOPE

### In Scope

- Monitoring cost model (per-citizen-per-day, by component)
- Crisis cost model (per-episode, by cost category)
- Prevention ROI calculation with uncertainty ranges
- Quarterly model updates as data accumulates
- Resource allocation recommendations

### Out of Scope

- Service pricing → see: `economics/service_model`
- Value narrative and communication → see: `economics/value_creation`
- Intervention effectiveness measurement → see: `research/technique_measurement`
- Cost reduction strategies → operational concern, not a doc chain module

---

## MARKERS

<!-- @mind:todo Instrument the assessment pipeline to measure actual per-query and per-LLM-call costs -->
<!-- @mind:todo Document at least 3 observed crisis episodes with full cost analysis -->
<!-- @mind:todo Compute first real prevention ROI from production data -->
<!-- @mind:proposition Create a "crisis cost calculator" tool for external organizations to estimate their own prevention ROI -->
