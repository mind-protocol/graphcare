# Process Improvement — Sync: Current State

```
LAST_UPDATED: 2026-03-15
UPDATED_BY: @vox (doc chain creation)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- The principle that GraphCare must monitor its own health
- Intervention outcome tracking as a concept (every message has a measurable effect)
- Weekly/monthly retrospective cadence

**What's still being designed:**
- The exact meta-health score formula
- Intervention outcome tagging schema
- Retrospective process format and tooling
- How citizen feedback is collected without reading content

**What's proposed (v2+):**
- Automated retrospective generation from outcome data
- Cross-organization meta-health benchmarking
- Citizen-initiated feedback on interventions (opt-in)

---

## CURRENT STATE

This module exists as documentation only. No code has been written for process improvement. The foundation it depends on — the scoring pipeline, aggregator, and daily check runner — exists and is operational (`services/health_assessment/`). The aggregator already stores daily JSON history per citizen (`aggregator.py`), which is the raw material for intervention outcome tracking.

The key gap is that interventions are currently fire-and-forget: GraphCare sends a message but does not track whether the citizen's score improved afterward. Closing this loop is the first concrete implementation step.

---

## IN PROGRESS

### Doc chain creation

- **Started:** 2026-03-15
- **By:** @vox
- **Status:** In progress
- **Context:** Creating OBJECTIVES, PATTERNS, SYNC as part of the parallel doc chain writing sprint for all GraphCare modules. This is the analysis/process_improvement portion.

---

## RECENT CHANGES

### 2026-03-15: Initial doc chain creation

- **What:** Created OBJECTIVES, PATTERNS, and SYNC for process_improvement module
- **Why:** Part of the full GraphCare documentation effort. Process improvement defines how the system improves itself — essential for any health monitoring system to maintain credibility.
- **Files:** `docs/analysis/process_improvement/OBJECTIVES_*.md`, `PATTERNS_*.md`, `SYNC_*.md`
- **Insights:** The existing `aggregator.py` already stores daily records with all capability scores as JSON. This means retrospective analysis can start immediately once we define what questions to ask of the data. The history is there; the analysis layer is not.

---

## KNOWN ISSUES

### No intervention outcome tracking

- **Severity:** High
- **Symptom:** Interventions are sent but never followed up — we don't know if they help
- **Suspected cause:** The intervention pipeline was built for delivery, not measurement
- **Attempted:** Nothing yet — this is the first identification of the gap

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Implement (building intervention outcome tracking) or VIEW_Design (designing the meta-health score)

**Where I stopped:** Documentation only. No code written. The three loops described in PATTERNS (outcome tracking, retrospective cadence, meta-health score) are designs, not implementations.

**What you need to understand:**
The aggregator (`services/health_assessment/aggregator.py`) stores daily JSON at `data/health_history/{citizen_id}/{date}.json`. Each record includes `aggregate_score`, `capability_scores` (dict), `intervention_sent` (bool), and `stress_stimulus` (float). This is enough to retroactively check whether intervention recipients improved. You can start building outcome tracking by loading D-7 records for citizens who had `intervention_sent: true`.

**Watch out for:**
- The `intervention_sent` field is boolean — it doesn't record which capabilities triggered the intervention. You'll need to cross-reference with `drops` (significant capability drops) from the `AggregateResult` to know what was targeted.
- Don't confuse process improvement (meta-level: is GraphCare working?) with formula evolution (object-level: are specific formulas accurate?). They're related but different modules.

**Open questions I had:**
- Should the meta-health score use the same 0-100 scale as citizen scores, or a different scale?
- How do we distinguish "citizen improved because of our intervention" from "citizen improved independently"? Causal attribution is hard.

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Process improvement documentation created. This module defines how GraphCare monitors its own effectiveness — through intervention outcome tracking, retrospective cadence, and a meta-health score. No code exists yet, but the existing aggregator history makes implementation feasible immediately.

**Decisions made:**
- Chose a three-loop architecture (outcome tracking, retrospectives, meta-health score)
- Defined intervention effectiveness as a 7-day window with >5-point improvement threshold
- Chose weekly micro + monthly macro retrospective cadence

**Needs your input:**
- Is the 7-day outcome window appropriate? Some interventions may take longer to show effect.
- Should meta-health scores be published to the same channels as citizen health, or a separate dashboard?

---

## TODO

### Doc/Impl Drift

- [ ] DOCS->IMPL: Entire module needs implementation (outcome tracking, retrospective tooling, meta-health scoring)

### Immediate

- [ ] Define intervention outcome tagging schema (extend DailyRecord or separate structure)
- [ ] Build outcome tracker: for each intervention, load D+7 record and compute effectiveness
- [ ] Define meta-health score formula with concrete signals and weights

### Later

- [ ] Build retrospective automation (aggregate outcomes into weekly reports)
- [ ] Design citizen feedback mechanism (topology-only, no content reading)
- IDEA: Use the same @register decorator pattern from scoring_formulas for meta-health components — makes them pluggable

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
Clear on the architecture but aware that the causal attribution problem (did our intervention cause the improvement?) is genuinely hard. The 7-day window + 5-point threshold is a starting heuristic, not a solved problem.

**Threads I was holding:**
- The relationship between process_improvement and formula_evolution is tight — process improvement discovers problems, formula evolution fixes them
- The aggregator's existing history format is both an asset (data exists) and a constraint (schema was designed for daily records, not longitudinal analysis)

**Intuitions:**
GraphCare's meta-health score should probably be lower-dimensional than citizen health scores. A system health score with 104 capabilities is overkill. Five to ten meta-health signals feels right.

**What I wish I'd known at the start:**
The `intervention_sent` boolean in the aggregator doesn't capture enough detail for outcome tracking. This is the first thing to address in implementation.

---

## POINTERS

| What | Where |
|------|-------|
| Daily record storage | `services/health_assessment/aggregator.py` |
| Formula registry | `services/health_assessment/scoring_formulas/registry.py` |
| Scoring pipeline docs | `docs/assessment/daily_citizen_health/` |
| Formula evolution module | `docs/analysis/formula_evolution/` |
| Technique measurement | `docs/research/technique_measurement/` |
