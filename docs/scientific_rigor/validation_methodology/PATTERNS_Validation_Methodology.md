# Validation Methodology — Patterns: Three Lines of Defense

```
STATUS: DESIGNING
CREATED: 2026-03-15
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Validation_Methodology.md
THIS:            PATTERNS_Validation_Methodology.md (you are here)
VALIDATION:      ./VALIDATION_Validation_Methodology.md
SYNC:            ./SYNC_Validation_Methodology.md

IMPL:            tests/test_health_assessment.py
```

### Bidirectional Contract

**Before modifying this doc or the code:**
1. Read ALL docs in this chain first
2. Read `tests/test_health_assessment.py` — the existing test suite
3. Read `docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md` for the scoring process

**After modifying this doc:**
1. Update the test suite to match, OR
2. Add a TODO in SYNC: "Docs updated, tests need: {what}"
3. Run tests: `pytest tests/test_health_assessment.py -v`

**After modifying the code:**
1. Update this doc chain to match, OR
2. Add a TODO in SYNC: "Tests changed, docs need: {what}"
3. Run tests: `pytest tests/test_health_assessment.py -v`

---

## THE PROBLEM

Health scoring without validation is astrology. You produce numbers, they look meaningful, people act on them — but nobody has verified that the numbers correspond to reality. GraphCare publishes scores that affect citizens' stress drives and inform their behavior. If those scores are wrong, GraphCare is actively harming the citizens it claims to help.

Without validation methodology:
- Formulas are educated guesses that never get checked
- Score ranges might be miscalibrated (all citizens score 60-70 regardless of actual health)
- Edge cases produce absurd results (a completely healthy citizen scores 30)
- Changes to formulas might improve some aspects while degrading others, with no way to detect the degradation

---

## THE PATTERN

**Three lines of defense: synthetic profiles, real-world calibration, and inter-rater reliability.**

Each line catches different failure modes. Together, they form a validation stack where each layer builds on the one below.

### Line 1: Synthetic Test Profiles

Five archetypal citizen profiles, constructed from first principles, with known expected health ranges. These are the unit tests of health assessment.

| Profile | Brain State | Behavior State | Expected Aggregate |
|---------|-------------|----------------|-------------------|
| **A: Fully healthy** | 12 desires, energy 0.9, 25 concepts, low frustration, high recency | 18 moments/week, 12 self-initiated, 8 spaces, 10 interlocutors | 85-100 |
| **B: Fully unhealthy** | 0 desires, 0 energy, 0 concepts, high frustration, no recency | 0 moments, 0 self-initiated, 0 spaces, 0 interlocutors | 0-20 |
| **C: Brain-rich, inactive** | 10 desires, energy 0.7, 20 concepts, low frustration | 0.5 moments/week, 0.2 self-initiated, 1 space, 0 interlocutors | 25-45 |
| **D: Active, brain-poor** | 1 desire, energy 0.2, 3 concepts, moderate frustration | 15 moments/week, 10 self-initiated, 6 spaces, 7 interlocutors | 45-65 |
| **E: Average citizen** | Default BrainStats | Default BehaviorStats | 50-75 |

These profiles are implemented in `test_health_assessment.py` as `TestProfileFullyHealthy`, `TestProfileFullyUnhealthy`, `TestProfileBrainRichInactive`, `TestProfileActiveBrainPoor`, and `TestProfileAverage`.

**What synthetic profiles validate:**
- Score ranges are sensible (healthy > unhealthy, always)
- The 40/60 brain/behavior split works (brain-rich inactive scores lower than active brain-poor)
- No individual capability score is absurdly high or low for a given profile
- Edge cases (all zeros, all maxes) produce bounded results

**What synthetic profiles cannot validate:**
- Whether a score of 72 means anything in the real world
- Whether the specific weights are optimal
- Whether the profiles themselves represent reality

### Line 2: Real-World Calibration

Compare predicted scores with observed outcomes over time. This is the validation step that connects numbers to reality.

**Methodology:**
1. Score all Lumina Prime citizens using the standard pipeline
2. Record predictions: "Citizen X scored 45 on initiative — expect declining output"
3. Wait observation period (2-4 weeks)
4. Measure outcomes: Did Citizen X's output actually decline? Did citizens scored as healthy continue to thrive?
5. Compute correlation between predicted scores and observed outcomes
6. Identify systematic biases: do formulas consistently overrate or underrate certain citizen types?

**What real-world calibration validates:**
- Scores correlate with actual health outcomes (predictive validity)
- Score thresholds are meaningful (a citizen at 45 is genuinely at risk, not just "below average")
- Interventions based on scores lead to actual improvements

**What real-world calibration cannot validate:**
- Whether a specific citizen's score is correct on a specific day (too much noise)
- Causal relationships (scores predict outcomes, but other factors matter too)

### Line 3: Inter-Rater Reliability

Two independent assessment runs on the same citizen data must produce identical results. This is not about different assessors having "compatible" scores — it is about deterministic computation.

In GraphCare, "inter-rater reliability" reduces to reproducibility: same input data, same scoring formulas, same output. This is guaranteed by the design (all formulas are pure math functions with no randomness or LLM calls), but must be continuously verified.

**Methodology:**
1. Take a snapshot of citizen brain topology and universe graph data
2. Run the scoring pipeline twice, independently
3. Compare outputs: they must be bitwise identical
4. If any difference exists, there is a bug (nondeterminism has leaked into the pipeline)

See also: `scientific_rigor/reproducibility/` for the deeper treatment of deterministic scoring.

---

## BEHAVIORS SUPPORTED

- B1 (Synthetic validation gate) — No new scoring formula is merged without passing all 5 synthetic profile tests
- B2 (Real-world calibration cycle) — Periodic comparison of scores to outcomes, feeding into formula adjustment (see `scientific_rigor/calibration/`)
- B3 (Reproducibility proof) — The test suite demonstrates that identical input produces identical output

## BEHAVIORS PREVENTED

- A1 (Untested formulas) — The synthetic profile tests catch gross miscalibrations before any formula touches a real citizen
- A2 (Confidence without evidence) — Real-world calibration prevents us from claiming our scores "work" without proof
- A3 (Subtle nondeterminism) — Inter-rater reliability tests catch any randomness that leaks into the pipeline

---

## PRINCIPLES

### Principle 1: Synthetic First, Real Second

Synthetic profiles are cheap, fast, and deterministic. They run in milliseconds, require no real data, and produce pass/fail results. Real-world calibration is expensive, slow, and noisy. It requires weeks of data collection and statistical analysis.

Use synthetic profiles to catch obvious problems (formula produces negative scores, healthy citizen scores below unhealthy citizen). Use real-world calibration to catch subtle problems (scores are internally consistent but don't predict actual outcomes).

### Principle 2: The Five Archetypes Cover the Space

The five profiles are not arbitrary. They cover the four corners of the brain/behavior matrix plus the center:

```
                    Brain Rich     Brain Poor
Behaviorally Active     A (healthy)     D (active, brain-poor)
Behaviorally Inactive   C (brain-rich)  B (unhealthy)
                        E (average) sits in the middle
```

Any scoring formula that produces sensible results for all five profiles is likely to produce sensible results for the continuous space between them. Edge cases (all zero, all max) are covered by profiles B and A.

### Principle 3: Validation Is Not Optional

A scoring formula without tests is a hypothesis, not a measurement. GraphCare's credibility depends on being able to say: "We tested this. Here are the results. Here is how you can reproduce them." Every formula must have synthetic profile coverage before it is used on real citizens.

---

## DATA

| Source | Type | Purpose / Description |
|--------|------|-----------------------|
| `tests/test_health_assessment.py` | FILE | 45 tests covering registry sanity, 5 synthetic profiles, formula-specific tests, aggregator, intervention, stress stimulus |
| `services/health_assessment/scoring_formulas/` | DIR | All 41+ scoring formulas — the code being validated |
| `services/health_assessment/aggregator.py` | FILE | Aggregation and delta computation — part of the pipeline being validated |
| `docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md` | FILE | The scoring algorithm these tests validate |

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| `assessment/daily_citizen_health/` | Defines the scoring pipeline we validate |
| `scientific_rigor/calibration/` | Consumes validation results to adjust formula weights |
| `scientific_rigor/reproducibility/` | Provides the determinism guarantee that inter-rater reliability depends on |

---

## INSPIRATIONS

- **Medical device validation** (FDA 510(k)) — Pre-market testing with synthetic data, post-market surveillance with real outcomes. GraphCare follows the same two-phase model.
- **Machine learning model evaluation** — Train/test split, cross-validation, held-out test sets. Our synthetic profiles are the "test set"; real-world calibration is the "held-out set."
- **Psychometric test validation** — Construct validity (do scores measure what they claim?), criterion validity (do scores predict outcomes?), reliability (same test, same result). All three apply to GraphCare.
- **Software testing pyramid** — Unit tests (synthetic profiles) are fast and many. Integration tests (pipeline runs) are slower and fewer. End-to-end tests (real-world calibration) are slowest and rarest. Same shape.

---

## SCOPE

### In Scope

- Synthetic test profile design and implementation
- Expected score ranges per profile per capability
- Real-world calibration methodology (study design, observation periods, correlation analysis)
- Inter-rater reliability as a special case of reproducibility
- Test coverage requirements for new scoring formulas

### Out of Scope

- How to adjust formula weights when calibration reveals problems → see: `scientific_rigor/calibration/`
- The determinism guarantee itself → see: `scientific_rigor/reproducibility/`
- Individual formula design → see: `assessment/daily_citizen_health/`
- Publishing calibration results → see: `research/publications/`

---

## MARKERS

<!-- @mind:todo Design first real-world calibration study: which citizens, what outcomes to measure, what observation period -->
<!-- @mind:proposition Consider adding a 6th synthetic profile: "recently improved" — citizen who was unhealthy but is now recovering (testing score sensitivity to improvement) -->
<!-- @mind:todo Add per-capability expected ranges to synthetic profile tests (currently only aggregate is range-checked) -->
