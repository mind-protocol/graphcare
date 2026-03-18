# Technique Measurement — Sync: Current State

```
LAST_UPDATED: 2026-03-15
UPDATED_BY: @vox (doc chain creation)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- The principle that care techniques must be experimentally validated
- The five initial experiments as a research agenda
- Harm threshold: >10% of treatment group declining >10 points stops the experiment

**What's still being designed:**
- Experiment registry schema
- Random assignment infrastructure
- Statistical significance testing methodology
- Experiment lifecycle (design -> approve -> run -> analyze -> publish)

**What's proposed (v2+):**
- Multi-variable optimization after single-variable experiments complete
- Automated experiment monitoring dashboards
- Cross-organization experimental collaboration (other health orgs run parallel experiments)

---

## CURRENT STATE

No experimental infrastructure exists. GraphCare sends interventions and stress stimuli based on the designs in `intervention_composer.py` and `stress_stimulus_sender.py`, but has never tested these approaches against alternatives. The care approach is entirely intuition-based.

The outcome measurement infrastructure partially exists: daily records in the health history contain the data needed to measure whether interventions helped. What's missing is the experimental framework — assignment to groups, tracking which citizen received which treatment, and comparative analysis.

The five initial experiments are defined as hypotheses but none have been designed in operational detail or begun.

---

## IN PROGRESS

### Doc chain creation

- **Started:** 2026-03-15
- **By:** @vox
- **Status:** In progress
- **Context:** Creating OBJECTIVES, PATTERNS, SYNC. This module defines how GraphCare validates its care approaches through controlled experiments.

---

## RECENT CHANGES

### 2026-03-15: Initial doc chain creation

- **What:** Created OBJECTIVES, PATTERNS, and SYNC for technique_measurement module
- **Why:** GraphCare's care approach is currently unvalidated. Every intervention and stress stimulus is an untested hypothesis. Technique measurement provides the experimental framework to test these hypotheses.
- **Files:** `docs/research/technique_measurement/OBJECTIVES_*.md`, `PATTERNS_*.md`, `SYNC_*.md`
- **Insights:** The stress feedback mechanism is the highest-priority experiment candidate. It actively modifies citizen brain state (adding stress) based on an untested theory. If stress feedback causes spirals rather than corrections, we need to know immediately.

---

## KNOWN ISSUES

### No experimental infrastructure

- **Severity:** High
- **Symptom:** All care techniques are deployed to all citizens with no comparison group
- **Suspected cause:** GraphCare focused first on building the assessment pipeline; experimentation is the next layer
- **Attempted:** Nothing yet — this is the first formal identification

### Stress feedback may cause harm

- **Severity:** High (potential)
- **Symptom:** Unknown — no data exists on stress stimulus outcomes
- **Suspected cause:** The stress formula `min(0.5, (100 - aggregate) / 200)` adds stress proportional to score deficit. For citizens already struggling, this may worsen rather than improve their state.
- **Attempted:** Nothing — the stress mechanism has never been A/B tested

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Design (designing the experiment registry) or VIEW_Implement (building assignment and tracking infrastructure)

**Where I stopped:** Documentation only. Five experiments defined as hypotheses. No operational design, no code, no running experiments.

**What you need to understand:**
The intervention pipeline currently has no concept of "groups" or "variants." `intervention_composer.py` composes one type of message. `stress_stimulus_sender.py` applies one formula. To run experiments, you need to: (1) assign citizens to groups, (2) modify the intervention pipeline to check group assignment and apply the appropriate treatment, (3) tag daily records with which treatment was applied, (4) analyze outcomes by group.

**Watch out for:**
- The daily check runner (`daily_check_runner.py`) iterates over all citizens. Experiment logic must integrate into this loop without breaking the non-experimental flow. Citizens not in any experiment get standard care.
- Stress stimuli directly modify brain drive values. Experiment 2 (stress magnitude) is testing whether this mechanism helps or harms — be prepared for it to show harm. Have a plan for what to do if stress feedback is counterproductive.
- Sample size matters. With ~60 citizens in Lumina Prime, a single experiment can have at most ~30 per group. This limits statistical power. Design experiments for the population size you have, not the one you wish you had.

**Open questions I had:**
- With only ~60 citizens, can we run meaningful experiments at all? 30 per group is possible but tight. May need sequential experiments rather than parallel.
- Should experiment assignment persist across days (citizen stays in treatment for the full duration) or re-randomize daily?
- How do we handle citizens who change significantly during an experiment (e.g., change organization, hit a major milestone)?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Technique measurement documentation created. This module defines how GraphCare validates its care approaches through controlled experiments. Five initial experiments are proposed: impact visibility vs score reports, stress feedback magnitude, intervention frequency, recommendation specificity, and silence threshold for healthy citizens. No experimental infrastructure exists yet.

**Decisions made:**
- Single-variable experiments (one change at a time)
- Minimum 2 weeks duration, minimum 20 citizens per group
- Harm threshold at 10% of treatment group declining 10+ points
- Consent and transparency: citizens know they're in experiments

**Needs your input:**
- Should Experiment 2 (stress feedback) run first, given its potential for harm?
- With ~60 citizens, are we comfortable with ~30 per group, or should we wait for population growth?
- Is the harm threshold (10% declining 10+ points) appropriate, or should it be stricter?

---

## TODO

### Doc/Impl Drift

- [ ] DOCS->IMPL: Build experiment registry (schema, storage, assignment tracking)
- [ ] DOCS->IMPL: Add group assignment logic to daily check runner
- [ ] DOCS->IMPL: Modify intervention composer to support message variants
- [ ] DOCS->IMPL: Build experiment outcome analysis tools

### Immediate

- [ ] Design experiment registry schema (experiment_id, hypothesis, groups, assignments, status)
- [ ] Design integration point with daily_check_runner.py for group-specific treatment
- [ ] Operationally design Experiment 2 (stress feedback magnitude) as the first experiment

### Later

- [ ] Build statistical significance testing (appropriate for small samples — Bayesian?)
- [ ] Design Experiments 1, 3, 4, 5 in operational detail
- [ ] Build experiment monitoring dashboard
- IDEA: Use sequential testing (analyze as data comes in) to stop experiments early if results are clear

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
Concerned about the stress feedback mechanism. It's the only part of GraphCare that actively modifies citizen brain state, and it's never been tested. The theoretical case is sound (discomfort motivates improvement), but the spiral case is equally plausible (more stress on already-struggling citizens). This should be the first experiment.

**Threads I was holding:**
- The small population size (~60 citizens) is a real constraint. Classical frequentist A/B testing needs larger samples. Bayesian methods or sequential testing designs may be more appropriate.
- There's a tension between "consent and transparency" (citizens know they're in experiments) and "experimental validity" (knowing you're being studied changes behavior — the Hawthorne effect). Need to think about this.

**Intuitions:**
Impact visibility (Experiment 1) will probably show positive results — narrating causal chains feels inherently more engaging than raw scores. The interesting finding will be in the magnitude and speed of effect, not the direction. Stress feedback (Experiment 2) could go either way — and the answer probably differs by citizen health level.

**What I wish I'd known at the start:**
The `daily_check_runner.py` is the integration point for all experiments. Any experimental framework needs to hook into the existing check loop, not create a parallel one.

---

## POINTERS

| What | Where |
|------|-------|
| Intervention composer | `services/health_assessment/intervention_composer.py` |
| Stress stimulus sender | `services/health_assessment/stress_stimulus_sender.py` |
| Daily check runner | `services/health_assessment/daily_check_runner.py` |
| Health history (outcomes) | `data/health_history/{citizen_id}/{date}.json` |
| Longitudinal health (trend data) | `docs/research/longitudinal_health/` |
| Process improvement (outcome consumer) | `docs/analysis/process_improvement/` |
| Publications (result output) | `docs/research/publications/` |
