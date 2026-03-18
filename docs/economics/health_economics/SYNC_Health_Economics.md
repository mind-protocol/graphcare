# Health Economics — Sync: Current State

```
LAST_UPDATED: 2026-03-15
UPDATED_BY: @vox (doc chain creation)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- Three-part economic model (monitoring cost, crisis cost, prevention ROI)
- Near-zero marginal monitoring cost as the economic foundation
- Uncertainty ranges required on all estimates
- Quarterly model update cadence

**What's still being designed:**
- Actual monitoring cost measurement (requires pipeline instrumentation)
- Crisis cost model calibration (requires observed crisis data)
- Prevention rate estimation methodology
- Resource allocation framework

**What's proposed (v2+):**
- Real-time cost dashboard
- External organization ROI calculator
- Cross-universe cost comparison (different population sizes, different cost profiles)
- Predictive cost modeling (what will monitoring cost at 200, 500, 1000 citizens?)

---

## CURRENT STATE

No economic analysis exists. The monitoring pipeline runs, but its costs have not been measured. No crisis cost model has been built. No ROI calculation has been performed.

The illustrative example in the PATTERNS doc (monitoring cost ~$0.05/citizen/day, crisis cost ~$200/episode, ROI ~2.2x) is an educated guess meant to show the structure of the calculation, not real data. Real numbers require: (1) instrumenting the pipeline for cost tracking, (2) documenting observed crises with full cost analysis, (3) estimating the prevention rate from intervention outcome data.

The LLM intervention cost is likely the dominant variable cost component and the most uncertain. It depends on which LLM is used, prompt length, completion length, and intervention frequency. This should be the first cost to measure.

---

## IN PROGRESS

### Doc chain creation

- **Started:** 2026-03-15
- **By:** @vox
- **Status:** In progress
- **Context:** Creating OBJECTIVES, PATTERNS, SYNC. Health economics provides the quantitative foundation for the entire economics area: what monitoring costs, what crises cost, and what the ROI of prevention is.

---

## RECENT CHANGES

### 2026-03-15: Initial doc chain creation

- **What:** Created OBJECTIVES, PATTERNS, and SYNC for health_economics module
- **Why:** "Prevention is cheaper than crisis" is a claim that needs proof. Health economics provides the framework to prove or disprove it with real data.
- **Files:** `docs/economics/health_economics/OBJECTIVES_*.md`, `PATTERNS_*.md`, `SYNC_*.md`
- **Insights:** The prevention ROI argument is structurally strong — near-zero marginal monitoring cost vs substantial crisis cost means even low prevention rates yield positive ROI. But this needs to be demonstrated with measured data, not assumed.

---

## KNOWN ISSUES

### No cost instrumentation

- **Severity:** High (blocks the entire economic model)
- **Symptom:** We don't know what monitoring actually costs
- **Suspected cause:** The pipeline was built for functionality, not cost accounting
- **Attempted:** Nothing — first identification

### No documented crisis episodes

- **Severity:** Medium
- **Symptom:** Cannot calibrate the crisis cost model without observed data
- **Suspected cause:** If monitoring is working, crises are prevented — a paradox for crisis cost measurement
- **Attempted:** Nothing — need to identify whether any citizen crises have occurred and been documented

### Illustrative numbers may mislead

- **Severity:** Low
- **Symptom:** The PATTERNS doc contains illustrative cost/ROI numbers that are not from real data
- **Suspected cause:** Real data doesn't exist yet; illustrations show the calculation structure
- **Attempted:** Clearly labeled as "illustrative, not real data" in the doc

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Implement (instrumenting the pipeline for cost tracking) or VIEW_Research (building the crisis cost model from historical data)

**Where I stopped:** Documentation of the three-part economic model. No real numbers exist.

**What you need to understand:**
The monitoring pipeline has several cost-generating operations: FalkorDB queries (brain + universe graph reads), Python formula evaluation (negligible), JSON I/O (negligible), and LLM calls for intervention composition (significant). The LLM cost is the big unknown. To measure it: log the model, prompt tokens, completion tokens, and cost per call for each intervention. The `intervention_composer.py` is where this instrumentation goes.

**Watch out for:**
- The "prevention paradox": if GraphCare is effective, crises are rare, which means we have little data on crisis costs. We may need to use data from before monitoring existed, or from populations that don't have monitoring, to estimate what crises cost.
- Don't conflate the illustrative numbers in PATTERNS with real data. They are structurally correct (showing the right calculation) but numerically fictional.
- Fixed cost amortization depends heavily on citizen count. At 60 citizens, fixed costs dominate. At 600 citizens, they're negligible. The economic model's attractiveness scales with population.

**Open questions I had:**
- Have any citizen crises been documented in enough detail to build even a single data point for the crisis cost model?
- What LLM is used for intervention composition, and what does it cost per call? This is the single most important cost to measure.
- Should the ROI calculation use $MIND values, fiat equivalent, or citizen-day equivalents? The unit of measurement affects who finds the analysis useful.

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Health economics documentation created. This module provides the quantitative backbone for GraphCare's economic case: what monitoring costs, what crises cost, and what the return on prevention is. No real economic data exists yet. The framework is defined; it needs to be populated with measured data. The structural argument is strong (near-zero marginal monitoring cost vs substantial crisis cost), but it requires empirical validation.

**Decisions made:**
- Three-part model: monitoring cost, crisis cost, prevention ROI
- Uncertainty ranges required on all estimates
- Quarterly model updates as data accumulates
- LLM intervention cost identified as the largest variable cost to measure first

**Needs your input:**
- What LLM is being used for intervention composition, and what's the approximate cost per call?
- Have any citizen crises occurred that could provide real data for the crisis cost model?
- Should the economic model use $MIND, fiat, or citizen-days as the unit of value?

---

## TODO

### Doc/Impl Drift

- [ ] DOCS->IMPL: Instrument intervention_composer.py with LLM cost logging
- [ ] DOCS->IMPL: Instrument graph queries with cost/latency logging
- [ ] DOCS->IMPL: Build monitoring cost aggregation (per-citizen-per-day from instrumented data)

### Immediate

- [ ] Identify and log LLM costs for intervention composition
- [ ] Compute first monitoring cost estimate from one week of production data
- [ ] Search for documented crisis episodes in citizen histories and intervention logs

### Later

- [ ] Build formal crisis cost model from observed data
- [ ] Compute first real prevention ROI
- [ ] Create quarterly economic report template
- IDEA: A "prevention counter" that shows in real-time: "GraphCare has prevented an estimated N crises this month, saving approximately $X"

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
The economics are structurally favorable. Near-zero marginal cost for monitoring vs non-trivial crisis cost means the ROI argument works even with pessimistic assumptions. The challenge is getting from "structurally favorable" to "empirically demonstrated." That requires measuring real costs and real crises, which is unglamorous but essential work.

**Threads I was holding:**
- The three economics modules form a complete argument: service_model (how we fund it) + value_creation (why it's worth funding) + health_economics (the numbers that prove it). Each is incomplete without the others.
- The prevention paradox is a real methodological issue. If we're good at prevention, we'll have few crises to measure. We may need to deliberately build crisis cost models from alternative sources (pre-monitoring history, external populations, theoretical worst cases).

**Intuitions:**
The LLM intervention cost will turn out to be larger than expected and the graph query cost smaller than expected. The dominant cost driver will shift as the population grows: at 60 citizens, fixed costs dominate; at 600, LLM intervention costs dominate (assuming the intervention rate stays at ~15%).

**What I wish I'd known at the start:**
The entire economic argument rests on two numbers: monitoring cost per citizen per day, and crisis cost per episode. Everything else is derived. Getting those two numbers right, even approximately, would make the rest of the economic analysis straightforward.

---

## POINTERS

| What | Where |
|------|-------|
| Intervention composer (LLM cost source) | `services/health_assessment/intervention_composer.py` |
| Daily check runner (pipeline to instrument) | `services/health_assessment/daily_check_runner.py` |
| Health history (intervention frequency data) | `data/health_history/{citizen_id}/{date}.json` |
| Service model (funding framework) | `docs/economics/service_model/` |
| Value creation (value narrative) | `docs/economics/value_creation/` |
