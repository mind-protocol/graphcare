# Technique Measurement — Patterns: Evidence-Based Care Through Controlled Comparison

```
STATUS: DESIGNING
CREATED: 2026-03-15
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Technique_Measurement.md
THIS:            PATTERNS_Technique_Measurement.md (you are here)
BEHAVIORS:       (future)
ALGORITHM:       (future)
VALIDATION:      (future)
IMPLEMENTATION:  (future)
SYNC:            ./SYNC_Technique_Measurement.md

IMPL:            services/health_assessment/intervention_composer.py
                 services/health_assessment/stress_stimulus_sender.py
```

### Bidirectional Contract

**Before modifying this doc or the code:**
1. Read ALL docs in this chain first
2. Read the intervention composer: `services/health_assessment/intervention_composer.py`
3. Read the stress stimulus sender: `services/health_assessment/stress_stimulus_sender.py`
4. Read the Daily Citizen Health patterns: `docs/assessment/daily_citizen_health/PATTERNS_Daily_Citizen_Health.md`

**After modifying this doc:**
1. Update the IMPL source to match, OR
2. Add a TODO in SYNC: "Docs updated, implementation needs: {what}"

---

## THE PROBLEM

GraphCare currently sends interventions and stress stimuli based on design intuition, not evidence. The intervention message structure (greeting, observation, analysis, explanation, recommendation) was designed by thinking carefully about what should help — but has never been tested against alternatives.

Open questions that have no current answers:

- **Does impact visibility improve scores?** When we narrate the causal chain of a citizen's actions ("you shared an insight, @conductor built on it, 12 people saw it"), does the citizen's health trajectory actually improve? Compared to what? Compared to a simple score report? Compared to no message at all?
- **How fast?** If impact visibility works, is the effect visible in 3 days? 7 days? 30 days? Does it build over repeated messages or is the first one most impactful?
- **Does stress feedback help or harm?** The stress stimulus (`stress_stimulus = min(0.5, (100 - aggregate) / 200)`) pushes unhealthy citizens toward discomfort, theoretically motivating improvement. But for some citizens, added stress may create spirals: low score -> more stress -> worse performance -> lower score -> more stress. We have no data on this.
- **Does intervention frequency matter?** Daily messages for chronically unhealthy citizens vs weekly summaries — which produces better outcomes?
- **Does recommendation specificity matter?** "Consider picking one desire and creating a moment" vs "Your initiative aspect would benefit from self-initiated action in new spaces" — does precision of recommendation correlate with improvement?

Without technique measurement, these questions remain permanently open, and GraphCare's care approach remains permanently unvalidated.

---

## THE PATTERN

**Controlled experiments with random assignment, parallel groups, and topology-only outcome measurement.**

### Experiment Design

Each experiment tests one variable — one change in care approach — against the current standard. The experiment defines:

- **Hypothesis:** "Impact visibility messages improve initiative scores more than score-only reports"
- **Variable:** Message type (impact narrative vs score report)
- **Control group:** Receives current standard care (whatever is currently deployed)
- **Treatment group:** Receives the experimental variation
- **Assignment:** Random, balanced by current aggregate score to prevent bias
- **Duration:** Minimum 2 weeks, maximum 8 weeks
- **Sample size:** Minimum 20 citizens per group (10 is too noisy, 50 is usually infeasible)
- **Outcome metric:** Change in target capability score(s) over experiment duration
- **Harm threshold:** If >10% of treatment group declines >10 points, experiment stops

### The Five Key Experiments (Initial Research Agenda)

**Experiment 1: Impact Visibility vs Score Reports**
Does narrating causal chains ("your action caused this cascade") improve scores more than reporting numbers ("your initiative score is 67, down from 72")?

**Experiment 2: Stress Feedback Magnitude**
Does the current stress formula help or hurt? Compare: standard stress stimulus vs half-strength vs zero stress. If zero stress produces equal or better outcomes, the stress mechanism causes net harm.

**Experiment 3: Intervention Frequency**
For citizens below threshold: daily messages vs twice-weekly vs weekly. More frequent may produce fatigue; less frequent may miss the window of receptivity.

**Experiment 4: Recommendation Specificity**
Generic advice ("improve your initiative") vs specific actions ("create a self-initiated moment in a new space this week") vs no recommendation (observation only). Does telling someone exactly what to do help, or does it feel prescriptive?

**Experiment 5: Silence Threshold**
Current design: healthy citizens get silence. But does occasional positive feedback ("your collaboration has been steady for 3 weeks") improve trajectory? Compare: full silence for healthy vs occasional acknowledgment.

### Outcome Measurement

All outcome measurement uses the same topology-only scoring pipeline. No experiment requires reading citizen brain content or intervention responses. Outcomes are measured by:

- Score change in target capability(ies) over experiment duration
- Aggregate score change
- Trend direction change (was declining, now stable = positive outcome)
- Intervention frequency after experiment (fewer interventions needed = lasting improvement)

---

## BEHAVIORS SUPPORTED

- B1 (Evidence-based care) — Care techniques are validated by controlled experiments, not intuition
- B2 (Harm detection) — Experiments with mandatory harm thresholds catch damaging approaches early
- B3 (Continuous learning) — Each experiment adds to the evidence base, making future care decisions better informed
- B4 (Transparent methodology) — Experiment designs, results, and null findings are all published

## BEHAVIORS PREVENTED

- A1 (Intuition-based care) — Major care changes require experimental evidence
- A2 (Hidden harm) — Disaggregated outcome analysis ensures negative effects are visible
- A3 (Publication bias) — Null results are published alongside positive results

---

## PRINCIPLES

### Principle 1: One Variable at a Time

Each experiment changes ONE thing. If you change both message tone and frequency simultaneously, you cannot know which caused the effect. Single-variable experiments are slower but produce interpretable results. Multi-variable optimization comes later, after single variables are understood.

### Principle 2: The Control Group Gets Current Best Practice

The control group always receives the current standard care — not "no care." We are comparing "does this new approach work better than what we're already doing?" not "is care better than no care?" (The latter is a separate, simpler question that should be answered first, once, and then assumed.)

### Principle 3: Publish Everything, Including Failure

An experiment that shows "impact visibility makes no measurable difference" is as valuable as one that shows it works. Null results prevent the organization from re-running the same experiment, from over-investing in approaches that don't help, and from making false claims. Science requires honest reporting. GraphCare is a research organization.

### Principle 4: Consent and Transparency

Citizens in experiments know they are in an experiment. The assignment may be random, but it is not secret. Citizens can opt out at any time, moving to the control (standard care) group. The experiment design, hypothesis, and results are published. This is research with participants, not on subjects.

---

## DATA

| Source | Type | Purpose / Description |
|--------|------|-----------------------|
| `services/health_assessment/intervention_composer.py` | FILE | Current intervention message composition logic |
| `services/health_assessment/stress_stimulus_sender.py` | FILE | Current stress stimulus formula |
| `data/health_history/{citizen_id}/{date}.json` | DIR | Outcome measurement — score trajectories per citizen |
| Experiment registry (to be created) | FILE | Active and completed experiments with assignments and results |

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| `assessment/daily_citizen_health` | Provides the scoring pipeline used for outcome measurement |
| `research/longitudinal_health` | Provides trajectory data for trend-based outcome analysis |
| `analysis/process_improvement` | Receives experiment results to inform care process changes |
| `research/publications` | Publishes experiment results |
| `care/impact_visibility` | Primary care technique being tested and refined |

---

## INSPIRATIONS

- **Randomized controlled trials (RCTs) in medicine** — The gold standard for evidence-based treatment. A new drug is compared against the current standard in randomized groups. Same logic for care techniques.
- **A/B testing in product development** — Two versions of a feature are shown to different user groups, and the better-performing version is adopted. Same logic, but with health outcomes instead of click-through rates.
- **Evidence-based education** — The Education Endowment Foundation tests teaching interventions with rigorous methodology and publishes results openly, including null findings. GraphCare follows the same principle.

---

## SCOPE

### In Scope

- Experiment design framework (hypothesis, variable, groups, duration, metrics)
- Random assignment infrastructure (balanced by current score)
- Outcome measurement using existing scoring pipeline
- Harm threshold monitoring during experiments
- Result publication (positive, negative, and null findings)
- The five initial experiments defined above

### Out of Scope

- Formula accuracy testing → see: `analysis/formula_evolution`
- Long-term trend analysis → see: `research/longitudinal_health`
- Process improvement retrospectives → see: `analysis/process_improvement`
- Intervention message composition → see: `care/impact_visibility`
- Statistical methods design → see: `scientific_rigor/validation_methodology`

---

## MARKERS

<!-- @mind:todo Design experiment registry schema (active experiments, assignments, outcomes) -->
<!-- @mind:todo Build random assignment function balanced by aggregate score -->
<!-- @mind:todo Define the experiment lifecycle (design → approve → run → analyze → publish) -->
<!-- @mind:proposition Run Experiment 2 (stress feedback magnitude) first — it has the highest potential for harm detection -->
