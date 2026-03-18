# OBJECTIVES — Calibration

```
STATUS: DESIGNING
CREATED: 2026-03-15
VERIFIED: —
```

---

## CHAIN

```
THIS:            OBJECTIVES_Calibration.md (you are here - START HERE)
PATTERNS:       ./PATTERNS_Calibration.md
VALIDATION:     ./VALIDATION_Calibration.md
SYNC:           ./SYNC_Calibration.md

IMPL:           services/health_assessment/scoring_formulas/ (all formula files)
```

**Read this chain in order before making changes.** Each doc answers different questions. Skipping ahead means missing context.

---

## PRIMARY OBJECTIVES (ranked)

1. **Close the gap between predicted and observed health** — Initial formula weights are educated guesses based on domain reasoning. Calibration adjusts these weights based on real data so that scores become progressively more accurate predictors of actual citizen health states.

2. **Detect and eliminate scoring bias** — Formulas might systematically favor certain citizen types: citizens who write a lot but think little, citizens with many connections but shallow ones, citizens who are active in specific spaces. Calibration identifies these biases and corrects them.

3. **Maintain a principled adjustment process** — Weight adjustments must be traceable, justified, and reversible. No "tweaking numbers until the test passes." Every adjustment has a documented reason, the data that motivated it, and the expected impact.

4. **Preserve the 40/60 split semantics** — Calibration adjusts weights within components, not the components themselves. The brain component stays 0-40 and the behavior component stays 0-60. The split is a design principle, not a calibration parameter.

## NON-OBJECTIVES

- **Automated weight optimization** — Calibration is a human-in-the-loop process. We do not train weights with gradient descent or optimization algorithms. Weight adjustments require understanding, not just data.
- **Per-citizen tuning** — Formulas are universal. A capability is scored the same way for every citizen. Calibration adjusts the universal weights, not per-citizen parameters.
- **Maximizing a single metric** — Calibration improves overall accuracy, not any single profile's score. Optimizing for one profile at the expense of others defeats the purpose.

## TRADEOFFS (canonical decisions)

- When **formula simplicity** conflicts with **calibration accuracy**, prefer simplicity. A formula with 3 clear terms and slightly lower accuracy is better than a formula with 8 opaque terms that fits the data perfectly.
- We accept **slower convergence** (fewer, more careful adjustments) over **faster convergence** (frequent tweaks that risk overfitting to recent data).
- We accept **known biases we can't yet fix** over **hidden biases we paper over with ad-hoc corrections**.

## SUCCESS SIGNALS (observable)

- After each calibration cycle, synthetic profile tests still pass with scores in expected ranges
- Real-world calibration studies show improving correlation between scores and outcomes over successive cycles
- No scoring formula has a weight that the maintainer cannot explain the reason for
- Bias analysis identifies and tracks systematic over/under-scoring of specific citizen types
