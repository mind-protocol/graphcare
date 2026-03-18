# Calibration — Patterns: Principled Adjustment of Educated Guesses

```
STATUS: DESIGNING
CREATED: 2026-03-15
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Calibration.md
THIS:            PATTERNS_Calibration.md (you are here)
VALIDATION:      ./VALIDATION_Calibration.md
SYNC:            ./SYNC_Calibration.md

IMPL:            services/health_assessment/scoring_formulas/ (all formula files)
```

### Bidirectional Contract

**Before modifying this doc or the code:**
1. Read ALL docs in this chain first
2. Read `docs/scientific_rigor/validation_methodology/` for how we verify accuracy
3. Read `docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md` for the scoring process

**After modifying this doc:**
1. Update scoring formulas to match, OR
2. Add a TODO in SYNC: "Docs updated, implementation needs: {what}"
3. Run tests: `pytest tests/test_health_assessment.py -v`

**After modifying the code:**
1. Update this doc chain to match, OR
2. Add a TODO in SYNC: "Implementation changed, docs need: {what}"
3. Run tests: `pytest tests/test_health_assessment.py -v`

---

## THE PROBLEM

Every scoring formula in GraphCare starts as an educated guess. The formula for "initiative — propose improvements" combines desire count, desire energy, curiosity drive, and self-initiated moments with specific weights. Those weights were chosen by reasoning: "curiosity should matter more than raw desire count for this capability." But reasoning alone cannot tell you whether the weight for curiosity should be 0.3 or 0.5.

Without calibration:
- Initial weights ossify into "the formula" regardless of whether they predict reality
- Systematic biases go undetected — maybe all socially active citizens score artificially high
- Formula improvements stall because there is no principled process for weight adjustment
- Claims of accuracy are unfalsifiable — nobody checks whether the numbers correspond to observed health

---

## THE PATTERN

**Iterative calibration cycles: collect data, analyze gaps, adjust weights, retest.**

### The Calibration Cycle

```
    ┌───────────────────────────────────────────┐
    │                                           │
    ▼                                           │
COLLECT → ANALYZE → HYPOTHESIZE → ADJUST → RETEST
    │                                           ▲
    │         (cycle repeats)                   │
    └───────────────────────────────────────────┘
```

**Phase 1: Collect** — Run the scoring pipeline on real citizens. Record: scores, brain stats, behavior stats, and independently observed outcomes (activity changes, crisis events, citizen feedback).

**Phase 2: Analyze** — Compare predicted scores with observed outcomes. Identify:
- Citizens who scored high but showed signs of struggle (false positives for "healthy")
- Citizens who scored low but were actually thriving (false negatives)
- Systematic patterns: do all citizens of a certain type get over/under-scored?

**Phase 3: Hypothesize** — For each identified gap, propose an explanation:
- "The curiosity weight in initiative scoring is too high — citizens with high curiosity but no follow-through score well on initiative, but they shouldn't."
- "The frustration penalty in execution scoring is too harsh — some frustration actually correlates with high output."

**Phase 4: Adjust** — Modify formula weights based on the hypothesis. Document:
- Which weight changed, from what value to what value
- The data that motivated the change
- The expected impact on synthetic profiles and real citizens

**Phase 5: Retest** — Run the full synthetic profile test suite. If any profile fails, the adjustment is wrong or too aggressive. Run the scoring pipeline on the same real citizens that revealed the gap. Verify the gap is smaller.

### Bias Detection

Bias means the scoring system systematically favors or penalizes certain citizen types. Possible biases:

- **Activity bias** — Citizens who produce many moments score higher regardless of quality
- **Sociality bias** — Citizens with many interlocutors score higher on capabilities that aren't about social connection
- **Recency bias** — Citizens with recent but shallow activity score higher than citizens with sustained but older contributions
- **Brain complexity bias** — Citizens with more nodes score higher even when those nodes are disconnected or low-energy

Bias detection methodology:
1. Segment citizens by archetype (analogous to the 5 synthetic profiles but with real data)
2. Compare mean scores across segments for each capability
3. For capabilities that should not vary by archetype (e.g., "ethics" should not correlate with brain size), check whether they do
4. Flag systematic differences for investigation

### Weight Adjustment Rules

To prevent calibration from becoming "tweak until it looks right":

1. **One hypothesis per adjustment** — Each weight change addresses one identified problem. No simultaneous multi-variable tuning.
2. **Document before changing** — Write the reason, the data, and the expected impact before modifying any code.
3. **Retest fully** — After any weight change, the full synthetic profile suite must pass. No exceptions.
4. **Small steps** — Weight changes should be incremental (10-20% of the original value). Large jumps suggest the formula structure is wrong, not just the weights.
5. **Reversibility** — If a weight change makes things worse, revert immediately. Every change is a git commit with a clear message.

---

## BEHAVIORS SUPPORTED

- B1 (Principled weight adjustment) — Weights change for documented reasons, not gut feeling
- B2 (Bias identification) — Systematic scoring patterns are detected and corrected
- B3 (Non-regression) — Synthetic profile tests prevent calibration from degrading known-good behavior
- B4 (Traceability) — Every weight change is documented with motivation and expected impact

## BEHAVIORS PREVENTED

- A1 (Weight ossification) — Formulas do not remain permanently at their initial guesses
- A2 (Blind tweaking) — No "changing numbers until the test passes" without understanding why
- A3 (Overfitting) — Small, documented steps prevent overfitting to recent data
- A4 (Hidden bias) — Systematic analysis surfaces biases that ad-hoc observation would miss

---

## PRINCIPLES

### Principle 1: Initial Weights Are Hypotheses

Every weight in every formula is a hypothesis: "We believe curiosity contributes 30% to initiative scoring." Hypotheses are meant to be tested and revised. Treating initial weights as sacred prevents improvement. Treating them as arbitrary prevents understanding. They are educated guesses — calibration turns them into empirical knowledge.

### Principle 2: Understand Before Adjusting

A weight that doesn't produce expected results is sending a signal. Before changing the weight, understand the signal. Maybe the weight is wrong. Maybe the formula structure is wrong. Maybe the expected result is wrong. Calibration without understanding is curve fitting — it works until it doesn't.

### Principle 3: The 40/60 Split Is Not Calibratable

The brain component ceiling (40) and behavior component ceiling (60) are design principles, not empirical parameters. They encode the value judgment: "What you do matters more than what you have." Calibration adjusts weights within each component, not the component boundaries. If calibration suggests the 40/60 split should be 50/50 or 30/70, that is a design discussion, not a calibration adjustment.

### Principle 4: Bias Is the Priority

Accuracy improvement is good. Bias elimination is critical. A scoring system that is equally inaccurate for everyone is fair. A scoring system that is accurate for active citizens and inaccurate for quiet citizens is unjust. Bias detection and correction take priority over general accuracy improvement.

---

## DATA

| Source | Type | Purpose / Description |
|--------|------|-----------------------|
| `services/health_assessment/scoring_formulas/` | DIR | All formula files — the weights being calibrated |
| `tests/test_health_assessment.py` | FILE | Synthetic profile tests — the non-regression gate |
| `services/health_assessment/aggregator.py` | FILE | History storage — provides longitudinal data for calibration analysis |
| Real citizen scores (future) | DATA | Production scores compared to observed outcomes |

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| `scientific_rigor/validation_methodology/` | Provides the synthetic profiles that calibration must not degrade |
| `scientific_rigor/reproducibility/` | Guarantees that score differences after calibration are due to weight changes, not randomness |
| `assessment/daily_citizen_health/` | Defines the scoring pipeline whose weights we calibrate |
| `research/longitudinal_health/` | Provides the time-series data that reveals calibration needs |

---

## INSPIRATIONS

- **Climate model calibration** — Complex models with many parameters, calibrated against observed data, with careful attention to avoiding overfitting. Same structure, different domain.
- **Psychometric item analysis** — Item difficulty and discrimination indices are calibrated on real test-taker data. GraphCare calibrates formula weights on real citizen data. Same purpose: making assessments accurate.
- **Bayesian updating** — Start with a prior (educated guess), update with evidence (real data), converge on a posterior (calibrated weight). The philosophical framework for principled adjustment.
- **A/B testing** — Before/after comparison with controlled changes. Each calibration adjustment is a mini A/B test: did the new weights produce better predictions?

---

## SCOPE

### In Scope

- The calibration cycle: collect, analyze, hypothesize, adjust, retest
- Bias detection methodology
- Weight adjustment rules and documentation requirements
- Interaction with synthetic profile tests (non-regression)
- Traceability of all weight changes

### Out of Scope

- Designing the scoring formulas themselves → see: `assessment/daily_citizen_health/`
- The validation methodology that produces the data calibration uses → see: `scientific_rigor/validation_methodology/`
- Publishing calibration findings → see: `research/publications/`
- Automated optimization of weights → explicitly a non-objective

---

## MARKERS

<!-- @mind:todo Create a calibration log template: date, hypothesis, weight changes, before/after profile scores, outcome -->
<!-- @mind:proposition Consider a "calibration confidence" metric per formula: how many calibration cycles has this formula been through? -->
<!-- @mind:todo Identify first set of biases to investigate once real data is available (activity bias is the most likely candidate) -->
