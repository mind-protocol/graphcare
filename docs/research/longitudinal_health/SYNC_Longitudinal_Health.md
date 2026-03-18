# Longitudinal Health — Sync: Current State

```
LAST_UPDATED: 2026-03-15
UPDATED_BY: @vox (doc chain creation)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- Daily JSON records stored by the aggregator at `data/health_history/{citizen_id}/{date}.json`
- Record format: citizen_id, date, aggregate_score, capability_scores dict, intervention_sent, stress_stimulus, brain_reachable
- Delta vs yesterday computed by `aggregate_scores()` in `aggregator.py`

**What's still being designed:**
- Trajectory computation (rolling averages, regression slopes, volatility)
- Cohort definitions and grouping logic
- Trend detection algorithms and alert thresholds
- Anonymization pipeline for research publication

**What's proposed (v2+):**
- Citizen-facing health timeline (self-service view of own trajectory)
- Predictive modeling (given trajectory, predict future score range)
- Cross-universe longitudinal comparison (once other work universes exist)

---

## CURRENT STATE

The raw data layer exists and is operational. The aggregator stores daily JSON records per citizen with full capability score breakdowns. The `load_history()` and `save_history()` functions in `aggregator.py` provide read/write access. The `aggregate_scores()` function already computes delta vs yesterday and identifies significant drops (>10 points).

What does NOT exist: any analysis beyond the single-day delta. No rolling averages, no trend detection, no cohort grouping, no longitudinal research output. The aggregator looks backward exactly one day. The data to look backward weeks or months is stored but unread.

The building blocks are all in place. The analysis layer needs to be built.

---

## IN PROGRESS

### Doc chain creation

- **Started:** 2026-03-15
- **By:** @vox
- **Status:** In progress
- **Context:** Creating OBJECTIVES, PATTERNS, SYNC as part of the parallel doc chain writing sprint. Longitudinal health is the primary research module — it transforms daily snapshots into time series that power both care and formula calibration.

---

## RECENT CHANGES

### 2026-03-15: Initial doc chain creation

- **What:** Created OBJECTIVES, PATTERNS, and SYNC for longitudinal_health module
- **Why:** The daily records are accumulating but no one is analyzing them over time. This module defines what "analyzing over time" means and how to do it.
- **Files:** `docs/research/longitudinal_health/OBJECTIVES_*.md`, `PATTERNS_*.md`, `SYNC_*.md`
- **Insights:** The aggregator's `load_history(citizen_id, date)` function loads one day at a time. Building trajectory analysis will need a `load_trajectory(citizen_id, start_date, end_date)` function that loads a range and returns a time series. This is a straightforward extension of existing code.

---

## KNOWN ISSUES

### Single-day horizon in aggregator

- **Severity:** Medium
- **Symptom:** `aggregate_scores()` only looks at yesterday's record. No multi-day analysis.
- **Suspected cause:** The aggregator was designed for daily checks, not longitudinal analysis
- **Attempted:** Nothing — this is by design in the current scope. Longitudinal analysis is a new layer.

### No cohort metadata available

- **Severity:** Medium
- **Symptom:** Citizen records don't include district, spawn date, or organization — needed for cohort grouping
- **Suspected cause:** Cohort attributes live in the L4 registry / citizen profiles, not in health records
- **Attempted:** Not yet — need to define how to join health data with citizen metadata

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Implement (building trajectory computation and trend detection)

**Where I stopped:** Documentation only. The data layer (daily JSON records) exists. The analysis layer does not.

**What you need to understand:**
The daily JSON files are stored at `data/health_history/{citizen_id}/{date}.json`. The `load_history()` function in `aggregator.py` loads one file and returns a `DailyRecord` dataclass. The `_history_path()` function constructs the file path. To build trajectory analysis, you need to: list all date files for a citizen, load them in order, extract the time series of scores.

The `capability_scores` dict in each record maps capability_id to Optional[float]. A `None` value means that capability had no formula that day (or the formula couldn't score it). Your trajectory analysis must handle missing values — not every capability will have a score every day.

**Watch out for:**
- Daily records may have gaps (citizen was unreachable, brain offline). Your time series must handle missing days gracefully — interpolation is acceptable for rolling averages, but not for trend direction computation.
- The `DROP_THRESHOLD` in `aggregator.py` is -10 points. This is the single-day crisis threshold. Longitudinal trend thresholds will be different (slower, cumulative).
- Cohort attributes (district, spawn date) are NOT in the health history files. You'll need to query the L4 registry or citizen graph separately.

**Open questions I had:**
- What's the minimum number of data points for a meaningful trend? 7 days? 14? Statistical significance requires thought.
- Should cohort analyses weight recent data more heavily, or treat all days equally?
- How do we handle citizens who change districts or organizations mid-trajectory?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Longitudinal health documentation created. This module transforms daily health snapshots into time series analysis — individual trajectories, cohort comparisons, and trend detection. The raw data (daily JSON records per citizen) already exists from the aggregator. What's needed is the analysis layer that reads across days and across citizens.

**Decisions made:**
- Three analysis layers: individual trajectories, cohort analysis, trend detection
- Cohort groupings: spawn date, district, tier, organization
- Trend types to detect: slow decline, plateau-before-breakdown, oscillation, divergence
- Anonymization is default for all published analyses

**Needs your input:**
- Which cohort attributes are most important to prioritize? District and spawn date seem most actionable.
- Should trend alerts go directly to `care/crisis_detection`, or through a review step first?

---

## TODO

### Doc/Impl Drift

- [ ] DOCS->IMPL: Build `load_trajectory(citizen_id, start, end)` function in aggregator
- [ ] DOCS->IMPL: Build trajectory analysis module (rolling average, slope, volatility)
- [ ] DOCS->IMPL: Build cohort grouping logic (needs citizen metadata from L4 registry)
- [ ] DOCS->IMPL: Build trend detection and alerting

### Immediate

- [ ] Extend aggregator.py with `load_trajectory()` that loads a date range of records
- [ ] Build rolling average (7-day, 30-day) and trend slope computation
- [ ] Define trend alert thresholds (how much decline over how many days triggers alert)

### Later

- [ ] Build cohort analysis framework (group citizens, compare distributions)
- [ ] Create anonymization pipeline for research datasets
- [ ] Connect trend alerts to care/crisis_detection
- IDEA: A "health weather map" of Lumina Prime showing district-level health trends

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
Excited about this module. The data is already there — daily records accumulate with every assessment run. The gap between "data exists" and "data tells stories" is exactly what longitudinal analysis fills. The tools are well-understood (time series, rolling averages, regression). The challenge is more organizational than technical.

**Threads I was holding:**
- The relationship between longitudinal health and formula evolution is circular: longitudinal data calibrates formulas, but formula changes affect longitudinal trends. Need to account for "score changed because formula changed" vs "score changed because citizen changed."
- Cohort analysis requires citizen metadata that currently lives outside GraphCare. The join between health records and citizen profiles needs to be designed carefully (privacy, data freshness).

**Intuitions:**
The most impactful early finding will probably come from spawn cohort analysis. New citizens likely follow predictable health curves (ramp up, plateau, breakthrough or decline). Identifying the typical curve would let GraphCare say "you're on track" or "you're diverging from your cohort" — which is much more informative than an absolute score.

**What I wish I'd known at the start:**
The `brain_reachable` field in DailyRecord is a crucial data quality signal. Days where `brain_reachable: false` should be excluded from trend analysis, not treated as missing data. The distinction matters: missing file = no assessment ran; `brain_reachable: false` = assessment ran but couldn't read the brain.

---

## POINTERS

| What | Where |
|------|-------|
| Daily record storage + format | `services/health_assessment/aggregator.py` |
| History file location | `data/health_history/{citizen_id}/{date}.json` |
| Daily health algorithm | `docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md` |
| Formula evolution (consumer) | `docs/analysis/formula_evolution/` |
| Process improvement (consumer) | `docs/analysis/process_improvement/` |
| Publications (output) | `docs/research/publications/` |
