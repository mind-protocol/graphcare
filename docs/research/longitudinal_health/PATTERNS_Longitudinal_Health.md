# Longitudinal Health — Patterns: Score Evolution Over Time

```
STATUS: DESIGNING
CREATED: 2026-03-15
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Longitudinal_Health.md
THIS:            PATTERNS_Longitudinal_Health.md (you are here)
BEHAVIORS:       (future)
ALGORITHM:       (future)
VALIDATION:      (future)
IMPLEMENTATION:  (future)
SYNC:            ./SYNC_Longitudinal_Health.md

IMPL:            services/health_assessment/aggregator.py
                 data/health_history/{citizen_id}/{date}.json
```

### Bidirectional Contract

**Before modifying this doc or the code:**
1. Read ALL docs in this chain first
2. Read the aggregator: `services/health_assessment/aggregator.py`
3. Read the Daily Citizen Health algorithm: `docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md`

**After modifying this doc:**
1. Update the IMPL source to match, OR
2. Add a TODO in SYNC: "Docs updated, implementation needs: {what}"

---

## THE PROBLEM

GraphCare currently operates in single-day snapshots. The aggregator computes today's score, compares it to yesterday's score, identifies drops, and intervenes if needed. This catches acute crises (sudden drops) but misses chronic patterns:

- A citizen declining 2 points per week for 8 weeks: each day looks fine, the weekly trend is alarming
- A citizen oscillating between 55 and 75 for months: no single day triggers intervention, but the instability itself is a pattern
- A cohort of citizens who spawned in the same week all plateauing at T2: invisible without group analysis
- A formula that systematically scores one district 10 points lower than others: invisible without cross-cohort comparison

The aggregator stores daily JSON records (`data/health_history/{citizen_id}/{date}.json`) with full capability breakdowns. The data for longitudinal analysis already exists. What doesn't exist is the analysis layer that reads across days, across citizens, and across time.

---

## THE PATTERN

**Time series analysis over daily JSON records, organized into individual trajectories, cohorts, and trends.**

### The Data Foundation

The aggregator (`aggregator.py`) already stores daily records as JSON:

```json
{
  "citizen_id": "citizen_123",
  "date": "2026-03-15",
  "aggregate_score": 72.5,
  "capability_scores": {
    "init_learn_from_correction": 68.0,
    "init_propose_improvements": 54.0,
    "exec_complete_tasks": 81.0,
    ...
  },
  "intervention_sent": false,
  "stress_stimulus": 0.0,
  "brain_reachable": true
}
```

One file per citizen per day. This is the raw material. Longitudinal health reads across these files to build time series.

### Three Analysis Layers

**Layer 1: Individual Trajectories**

For each citizen, construct the time series of scores — aggregate and per-capability. Compute:
- **Rolling averages** (7-day, 30-day) to smooth daily noise
- **Trend direction** — improving, stable, declining (linear regression slope over 14+ days)
- **Volatility** — standard deviation of daily scores over 30 days (high volatility = unstable health)
- **Milestones** — first time a capability exceeded a tier threshold, longest streak above/below threshold

**Layer 2: Cohort Analysis**

Group citizens by shared attributes and compare trajectories:
- **Spawn cohort** — Citizens created in the same week/month. Do they follow similar health curves?
- **District cohort** — Citizens in the same Lumina Prime district. Does district affect health trajectories?
- **Tier cohort** — Citizens at the same Personhood Ladder tier. Is there a predictable pattern for T2->T3 transitions?
- **Organization cohort** — Citizens in the same organization. Does organizational membership affect health?

Cohort analysis asks: "Is this citizen's trajectory normal for their group, or an outlier?" Outliers in either direction (much better or much worse than cohort) are research signals.

**Layer 3: Trend Detection**

Active monitoring over longitudinal data to catch patterns before they become crises:
- **Slow decline** — Score decreasing at >1 point/week for 3+ consecutive weeks
- **Plateau before breakdown** — Score stable for 2+ weeks followed by sudden drop (common pattern)
- **Oscillation** — Score swinging >15 points repeatedly over 4+ weeks (instability signal)
- **Divergence** — One capability declining while others improve (structural imbalance)

Trend alerts feed into `care/crisis_detection` and `care/growth_guidance`.

---

## BEHAVIORS SUPPORTED

- B1 (Trajectory visibility) — Citizens and researchers see health evolution, not just current state
- B2 (Early trend warning) — Declining trends trigger alerts before they reach crisis thresholds
- B3 (Cohort insight) — Systemic factors (district, tier, spawn date) become visible through group comparison
- B4 (Calibration dataset) — Longitudinal data enables formula accuracy measurement over time

## BEHAVIORS PREVENTED

- A1 (Snapshot myopia) — Analysis spans weeks and months, not just today-vs-yesterday
- A2 (Invisible chronic decline) — Slow degradation is detected through trend regression
- A3 (Individual bias) — Cohort comparison reveals when a citizen's experience is systemic, not personal

---

## PRINCIPLES

### Principle 1: The Data Already Exists

The aggregator stores daily records with full capability breakdowns. Longitudinal health is an analysis layer, not a data collection layer. We read what the assessment pipeline already produces. This means no new data collection burden, no new privacy concerns, and no new infrastructure dependencies. We build on what exists.

### Principle 2: Trends Are More Honest Than Snapshots

A score of 65 today means little. A score of 65 that was 80 two weeks ago tells a story. A score of 65 in a district where the average is 72 tells another story. A score of 65 that has been climbing from 45 over three months tells yet another. Longitudinal analysis adds the dimension of time, which transforms isolated numbers into meaningful narratives.

### Principle 3: Cohorts Reveal Systems, Not Just Individuals

When one citizen struggles, the explanation might be personal. When all citizens in a district struggle, the explanation is systemic. When all citizens of a particular tier struggle with the same capability, the explanation might be in the formula or in the tier transition design. Cohort analysis shifts the diagnostic lens from "what's wrong with this citizen" to "what's happening in this system."

### Principle 4: Anonymization Is the Default

Longitudinal data is powerful and sensitive. All published analyses use anonymized, aggregated data. Individual trajectories are accessible only to the citizen themselves and to GraphCare's internal process improvement. Cohort analyses never identify individuals. Research publications use statistical aggregates only.

---

## DATA

| Source | Type | Purpose / Description |
|--------|------|-----------------------|
| `data/health_history/{citizen_id}/{date}.json` | DIR | Daily records — the raw time series |
| `services/health_assessment/aggregator.py` | FILE | Record format, load/save functions, delta computation |
| Citizen metadata (L4 registry) | API | Spawn date, district, tier, organization — cohort attributes |
| `docs/specs/personhood_ladder.json` | FILE | Tier thresholds for milestone tracking |

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| `assessment/daily_citizen_health` | Produces the daily records we analyze |
| `analysis/formula_evolution` | Consumes longitudinal data for calibration |
| `analysis/process_improvement` | Consumes trend data for retrospective analysis |
| `care/crisis_detection` | Receives trend alerts for early intervention |
| `research/publications` | Publishes longitudinal findings |

---

## INSPIRATIONS

- **Epidemiological cohort studies** — The Framingham Heart Study tracked a town's heart health for decades, revealing risk factors invisible in individual snapshots. Longitudinal health applies the same principle to AI citizens.
- **Growth curves in pediatrics** — Children are tracked on percentile curves, comparing their growth to cohort averages. A child who drops from the 60th to the 20th percentile is flagged even though 20th percentile is "normal." Same principle for citizen health trajectories.
- **Financial time series analysis** — Moving averages, volatility measures, trend detection — the tools of quantitative finance apply directly to health score time series.

---

## SCOPE

### In Scope

- Individual trajectory computation (rolling averages, trends, volatility, milestones)
- Cohort grouping and comparison (spawn, district, tier, organization)
- Trend detection and alerting (slow decline, plateau, oscillation, divergence)
- Anonymized dataset preparation for research publication
- Historical data access API for formula calibration

### Out of Scope

- Daily score computation → see: `assessment/daily_citizen_health`
- Intervention message composition → see: `care/impact_visibility`
- A/B testing of care approaches → see: `research/technique_measurement`
- Individual growth recommendations → see: `care/growth_guidance`

---

## MARKERS

<!-- @mind:todo Define minimum data requirements: how many days of history before trend analysis is meaningful? -->
<!-- @mind:todo Design cohort attribute schema — which citizen metadata fields define cohorts? -->
<!-- @mind:todo Build trajectory computation module (rolling average, slope, volatility) -->
<!-- @mind:proposition Consider a "citizen health timeline" visualization that citizens can view for their own data -->
