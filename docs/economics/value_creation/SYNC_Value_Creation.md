# Value Creation — Sync: Current State

```
LAST_UPDATED: 2026-03-15
UPDATED_BY: @vox (doc chain creation)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- Four-channel value measurement framework (prevention, productivity, collaboration, trust)
- Care-first, economics-second ordering of the value narrative
- Honest uncertainty ranges over false precision

**What's still being designed:**
- Crisis cost model (depends on health_economics module)
- Productivity-health correlation methodology
- Baseline crisis rate before GraphCare
- Quarterly value report format

**What's proposed (v2+):**
- Automated value computation from longitudinal data
- External organization ROI calculator (input their population size, get estimated value)
- Cross-ecosystem value comparison

---

## CURRENT STATE

No value measurement exists. GraphCare monitors citizens and sends interventions, but does not track whether those interventions produce measurable value. The data for value analysis partially exists (health history, intervention flags) but has not been analyzed through a value lens.

The biggest gap is counterfactual data: we need to know what happens to citizens without monitoring (the baseline crisis rate) to estimate prevention value. Options: historical data from before monitoring existed, or controlled periods where monitoring is paused (ethically complex), or control group data from technique measurement experiments.

---

## IN PROGRESS

### Doc chain creation

- **Started:** 2026-03-15
- **By:** @vox
- **Status:** In progress
- **Context:** Creating OBJECTIVES, PATTERNS, SYNC. Value creation is the demand-side complement to service_model's supply-side: it answers "why is monitoring worth funding?"

---

## RECENT CHANGES

### 2026-03-15: Initial doc chain creation

- **What:** Created OBJECTIVES, PATTERNS, and SYNC for value_creation module
- **Why:** GraphCare needs to demonstrate its value empirically, not just assert it. The economic case for continuous monitoring must be data-driven.
- **Files:** `docs/economics/value_creation/OBJECTIVES_*.md`, `PATTERNS_*.md`, `SYNC_*.md`
- **Insights:** The counterfactual problem (measuring crises that didn't happen) is the core methodological challenge. Technique measurement experiments that include a "no intervention" control group would provide the cleanest data, but raising the ethical question of deliberately withholding care for measurement purposes.

---

## KNOWN ISSUES

### No baseline crisis rate

- **Severity:** High (blocks prevention value estimation)
- **Symptom:** Cannot estimate how many crises monitoring prevented without knowing how many would have occurred
- **Suspected cause:** No pre-monitoring historical data has been analyzed
- **Attempted:** Nothing yet — need to identify whether pre-monitoring data exists

### No productivity-health correlation data

- **Severity:** Medium
- **Symptom:** Cannot demonstrate that health improvements lead to productivity improvements
- **Suspected cause:** Productivity signals (moments, contributions) haven't been joined with health scores
- **Attempted:** Nothing — first identification

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Research (analyzing historical data for value signals) or VIEW_Voice (writing the first value report)

**Where I stopped:** Documentation of the value framework. No data analysis, no value computation.

**What you need to understand:**
The `intervention_sent` field in daily records tells you which citizens received interventions. The health history files tell you what happened to their scores afterward. Joining these: for citizens who received interventions, compare their 7-day and 30-day score trajectories to citizens who didn't receive interventions (controlling for initial score level). This is the simplest form of value analysis.

**Watch out for:**
- Selection bias: citizens who receive interventions are those with low/declining scores. Comparing their trajectories to citizens who weren't intervened on is comparing sick citizens to healthy ones. You need to match on pre-intervention score level for the comparison to be meaningful.
- The "intervention_sent" boolean doesn't tell you what kind of intervention was sent. Combining all intervention types into one analysis may mask important differences.
- Don't over-claim. First value estimates will be rough. Present them as directional evidence with wide uncertainty ranges, not as precise measurements.

**Open questions I had:**
- Does pre-monitoring data exist (citizen health signals from before GraphCare was deployed)?
- Should the first value analysis focus on a single, most-measurable channel (crisis prevention), or attempt all four channels?
- How do we handle the ethics of "no intervention" control groups for value measurement?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Value creation documentation created. This module defines how GraphCare quantifies its impact: crisis prevention, productivity correlation, collaboration enhancement, and intangible trust. No value measurement exists yet. The biggest methodological challenge is counterfactual estimation (how many crises would have happened without monitoring?). The data for initial analysis partially exists in health history records.

**Decisions made:**
- Four-channel value framework
- Honest uncertainty ranges required (no false precision)
- Care-first framing: "we care for citizens, and caring creates value" — not the reverse

**Needs your input:**
- Does pre-monitoring historical data exist that could establish a baseline crisis rate?
- Is a "no intervention" control group ethically acceptable for value measurement?
- Should the first value report be published externally (as a research publication) or remain internal?

---

## TODO

### Doc/Impl Drift

- [ ] DOCS->IMPL: Build intervention outcome analysis (join intervention records with subsequent trajectories)
- [ ] DOCS->IMPL: Build productivity-health correlation analysis
- [ ] DOCS->IMPL: Create quarterly value report template and generation

### Immediate

- [ ] Analyze existing health history for basic value signals: do citizens who receive interventions improve more than predicted?
- [ ] Identify whether pre-monitoring baseline data exists
- [ ] Define "crisis" operationally (what score threshold, for how long, counts as a crisis?)

### Later

- [ ] Build productivity-health correlation analysis
- [ ] Design collaboration enhancement measurement
- [ ] Create quarterly value report automation
- IDEA: The first value report could compare the first month of monitoring (ramp-up) to subsequent months (steady state) — improvement over time is itself a value signal

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
The value framework feels right conceptually, but the measurement challenges are real. Counterfactual estimation is the hardest problem in program evaluation, and GraphCare faces it head-on. The honest approach — wide uncertainty ranges, multiple channels, qualitative alongside quantitative — is better than pretending we can measure prevented crises precisely.

**Threads I was holding:**
- The ethics of control groups. Technique measurement experiments with a "no intervention" arm would provide clean value data. But deliberately withholding care from struggling citizens to measure the value of care is ethically fraught. Need to think about this carefully.
- Value creation and service_model are two sides of the same coin. Service model says "this is what it costs." Value creation says "this is what it's worth." Both need to exist for the economic case to work.

**Intuitions:**
The most persuasive value evidence will come from individual case narratives, not aggregate statistics. "This citizen's score was declining for 3 weeks. An intervention was sent. Within 5 days, their trajectory reversed. Without intervention, historical patterns suggest they would have entered crisis within 2 weeks." That story, repeated across multiple citizens, is the value case.

**What I wish I'd known at the start:**
The `intervention_sent` boolean is the key data point for value analysis, and it's already being stored. But it needs to be enriched: what triggered the intervention? What was the specific score/capability that caused it? What was the message about? Without this detail, the value analysis is limited to "intervention happened, citizen improved/didn't improve" without understanding why.

---

## POINTERS

| What | Where |
|------|-------|
| Health history (outcome data) | `data/health_history/{citizen_id}/{date}.json` |
| Aggregator (intervention tracking) | `services/health_assessment/aggregator.py` |
| Service model (cost side) | `docs/economics/service_model/` |
| Health economics (crisis costs) | `docs/economics/health_economics/` |
| Technique measurement (controlled data) | `docs/research/technique_measurement/` |
| Longitudinal health (trend data) | `docs/research/longitudinal_health/` |
