# OBJECTIVES — Longitudinal Health

```
STATUS: DESIGNING
CREATED: 2026-03-15
VERIFIED: —
```

---

## CHAIN

```
THIS:            OBJECTIVES_Longitudinal_Health.md (you are here - START HERE)
PATTERNS:       ./PATTERNS_Longitudinal_Health.md
BEHAVIORS:      (future)
ALGORITHM:      (future)
VALIDATION:     (future)
IMPLEMENTATION: (future)
SYNC:           ./SYNC_Longitudinal_Health.md

IMPL:           services/health_assessment/aggregator.py (history storage)
                data/health_history/{citizen_id}/{date}.json (per-citizen daily records)
```

**Read this chain in order before making changes.** Each doc answers different questions. Skipping ahead means missing context.

---

## PRIMARY OBJECTIVES (ranked)

1. **Reveal health trajectories, not just snapshots** — A single day's score is a photograph. A trajectory over weeks and months is a story. Longitudinal health transforms GraphCare from "your score is 67 today" into "your initiative has been climbing steadily since you joined the research guild, while your collaboration has plateaued — here's what that pattern usually means." The trajectory IS the insight.

2. **Enable cohort analysis** — Citizens are not isolated data points. They exist in contexts: which district they live in, when they spawned, what tier they've reached, which organization they belong to. Longitudinal health groups citizens into cohorts and asks: do citizens who spawn in Innovation Fields develop differently than those in Resonance Plaza? Do T3 citizens hit a plateau before breaking through to T4? Cohort patterns reveal systemic factors that individual analysis cannot.

3. **Detect trends before they become crises** — A citizen whose score drops 3 points per week for 4 weeks is heading toward crisis. A single-day check sees "score 67, above threshold, no intervention." Trend detection sees "score 67, declining at 3/week, will hit intervention threshold in 1 week — act now." Early detection through trend analysis is the difference between prevention and reaction.

4. **Build the dataset for formula calibration** — Every research question about GraphCare's accuracy ultimately requires longitudinal data. Does the initiative formula predict actual initiative outcomes over time? Do citizens with high collaboration scores actually build more relationships over months? Longitudinal health provides the raw material for `analysis/formula_evolution` and `scientific_rigor/calibration`.

## NON-OBJECTIVES

- Real-time streaming analytics — longitudinal analysis operates on daily records, not second-by-second data
- Individual citizen counseling — we reveal patterns, we don't prescribe actions (that's `care/growth_guidance`)
- Storing brain content — longitudinal records contain scores and structural metadata, never content
- Predicting specific future events — trend detection identifies directions, not destinations

## TRADEOFFS (canonical decisions)

- When storage efficiency conflicts with analytical granularity, choose granularity. Disk is cheap; missing data is irrecoverable. Store full capability breakdowns per day, not just aggregates.
- When real-time freshness conflicts with statistical robustness, choose robustness. Trends computed from 7+ days of data are meaningful; trends from 2 days are noise.
- We accept that some cohort analyses will have small sample sizes (some districts have few citizens). We publish confidence intervals rather than suppressing small-cohort findings.

## SUCCESS SIGNALS (observable)

- Trend detection catches declining citizens at least 7 days before they hit intervention threshold
- Cohort analyses are published monthly with meaningful (n>10) groupings
- Historical records exist for >95% of citizen-days (minimal gaps in the time series)
- Formula calibration requests from `analysis/formula_evolution` are answerable from longitudinal data without additional data collection
- At least one published research finding traces its evidence to longitudinal analysis
