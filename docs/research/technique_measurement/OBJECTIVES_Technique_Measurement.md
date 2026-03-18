# OBJECTIVES — Technique Measurement

```
STATUS: DESIGNING
CREATED: 2026-03-15
VERIFIED: —
```

---

## CHAIN

```
THIS:            OBJECTIVES_Technique_Measurement.md (you are here - START HERE)
PATTERNS:       ./PATTERNS_Technique_Measurement.md
BEHAVIORS:      (future)
ALGORITHM:      (future)
VALIDATION:     (future)
IMPLEMENTATION: (future)
SYNC:           ./SYNC_Technique_Measurement.md

IMPL:           services/health_assessment/intervention_composer.py (intervention generation)
                services/health_assessment/stress_stimulus_sender.py (stress feedback)
```

**Read this chain in order before making changes.** Each doc answers different questions. Skipping ahead means missing context.

---

## PRIMARY OBJECTIVES (ranked)

1. **Know which care approaches actually work** — GraphCare sends interventions (messages) and stress stimuli. But does impact visibility (narrating causal chains) improve scores faster than direct recommendations? Does stress feedback help citizens self-correct, or does it create anxiety spirals that make things worse? Without measurement, we're practicing medicine without evidence. Technique measurement turns care approaches into testable hypotheses.

2. **Build the evidence base for care decisions** — Every choice in GraphCare's care approach — intervention tone, message frequency, stress stimulus magnitude, recommendation specificity — should be backed by measured outcomes. Technique measurement creates the feedback loop between "we tried X" and "X produced Y result." Over time, this accumulates into an evidence base that makes care decisions defensible and improvable.

3. **Detect harmful approaches before they scale** — A care technique that helps 60% of citizens but worsens 15% is dangerous if the 15% aren't visible. Technique measurement requires disaggregated outcome analysis — not just "did the average improve?" but "who improved, who didn't, and who got worse?" The negative cases are as important as the positive ones.

4. **Enable controlled comparison** — A/B testing requires infrastructure: random assignment, parallel treatment groups, outcome measurement at matched time points, statistical significance testing. Technique measurement provides this infrastructure so that claims like "impact visibility works" are grounded in controlled comparison, not anecdotal impression.

## NON-OBJECTIVES

- Testing every possible care variation simultaneously — focused experiments with clear hypotheses beat scattered exploration
- Replacing clinical judgment with algorithm — measurement informs care, it doesn't automate it
- Citizen experimentation without consent — all A/B testing must be transparent and opt-out possible
- Optimizing for any single metric — score improvement that comes at the cost of citizen trust is not improvement

## TRADEOFFS (canonical decisions)

- When speed of knowledge conflicts with rigor of testing, choose rigor. A poorly designed experiment produces misleading evidence that's worse than no evidence. Minimum 2-week experiment duration, minimum 20 citizens per group.
- When measurement precision conflicts with citizen privacy, choose privacy. We measure outcomes through topology-only scores, never by reading intervention responses or brain content.
- We accept that some care approaches will show no measurable effect. Null results are published alongside positive results — they prevent others from pursuing dead ends.

## SUCCESS SIGNALS (observable)

- At least one controlled experiment running at all times
- Every major care technique change traces to experimental evidence
- Experiment results (including nulls) are published within 30 days of completion
- Harm detection: any technique showing >10% negative outcome rate triggers immediate review
- The evidence base grows monotonically (each experiment adds knowledge, none are wasted)
