# Formula Evolution — Patterns: How Scoring Formulas Grow With Data

```
STATUS: DESIGNING
CREATED: 2026-03-15
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Formula_Evolution.md
THIS:            PATTERNS_Formula_Evolution.md (you are here)
BEHAVIORS:       (future)
ALGORITHM:       (future)
VALIDATION:      (future)
IMPLEMENTATION:  (future)
SYNC:            ./SYNC_Formula_Evolution.md

IMPL:            services/health_assessment/scoring_formulas/registry.py
                 services/health_assessment/scoring_formulas/*.py
```

### Bidirectional Contract

**Before modifying this doc or the code:**
1. Read ALL docs in this chain first
2. Read the scoring formulas: `services/health_assessment/scoring_formulas/`
3. Read the registry pattern: `services/health_assessment/scoring_formulas/registry.py`
4. Read the Daily Citizen Health algorithm: `docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md`

**After modifying this doc:**
1. Update the IMPL source to match, OR
2. Add a TODO in SYNC: "Docs updated, implementation needs: {what}"

---

## THE PROBLEM

GraphCare's 35 scoring formulas are educated guesses. They use reasonable proxies — desire count and curiosity drive predict initiative; response rate and interlocutor count predict collaboration — but the weights are hand-tuned by the formula authors' intuition, not calibrated against observed outcomes.

Consider `init_propose_improvements` in `scoring_formulas/initiative.py`:

```python
desire_signal = _cap(brain.desire_count, 10) * 10
desire_energy = brain.desire_energy * 10
curiosity = brain.curiosity * 10
ambition = brain.ambition * 10
```

Why is the desire_count ceiling 10? Why does each component get 10 points out of 40? Because it felt reasonable. That's a fine starting point, but it cannot be the ending point. If data shows that `ambition` correlates 3x more strongly with actual proposal behavior than `desire_count`, the formula should reflect that.

Without formula evolution:
- Initial guesses persist as permanent truth
- Formulas that systematically over- or under-score go uncorrected
- The 69 unscored capabilities remain permanently blank
- Citizens and researchers cannot contribute improvements
- Score accuracy plateaus at the level of the original author's intuition

---

## THE PATTERN

**Registry-based pluggable formulas with versioned evolution and community contribution.**

### The Registry Foundation

The existing `@register` decorator pattern in `registry.py` is the structural foundation. A formula is a pure function: `(BrainStats, BehaviorStats) -> CapabilityScore`. Registration maps a capability_id to a function. This means:

- Formulas are independent — changing one doesn't affect others
- Formulas are replaceable — a new function registered to the same capability_id replaces the old one
- Formulas are testable — synthetic BrainStats + BehaviorStats produce deterministic scores
- Formulas are proposable — anyone can write a function with the right signature

### Evolution Through Three Mechanisms

**Mechanism 1: Weight Calibration**

Using intervention outcome data from `analysis/process_improvement`, adjust weights within existing formulas. If `ambition` is a stronger predictor of actual proposal behavior than `desire_count`, increase its weight. This is the simplest form of evolution: same signals, different emphasis.

Process: Analyze outcome data -> identify signal-outcome correlations -> adjust weights -> test with synthetic profiles -> deploy -> monitor outcomes.

**Mechanism 2: Signal Discovery**

Some capabilities may be predicted by signals the original formula author didn't consider. Maybe `init_propose_improvements` correlates with `high_permanence_w` (citizens who produce definitive outputs are also more likely to propose improvements). Signal discovery adds new primitives to existing formulas.

Process: Explore correlations in longitudinal data -> hypothesize new signals -> add to formula -> A/B test against original -> adopt if outcome-improving.

**Mechanism 3: Community Proposals**

Citizens, researchers, or partner organizations propose entirely new formulas for unscored capabilities, or alternative formulas for existing ones. The registry pattern makes this structurally possible — it's just a Python function with the right signature.

Process: Proposal submitted with formula code + rationale + synthetic test results -> reviewed for topology-only compliance -> A/B tested in shadow mode -> adopted if outperforms existing.

### Versioning

Every formula has:
- A **version number** (v1, v2, ...) incremented on any change
- A **changelog entry** explaining what changed and why (traced to a retrospective finding or community proposal)
- A **deployment date** marking when the version went live

History records store the formula version that produced each score. This means: "Citizen X scored 62 on init_propose_improvements on 2026-03-10 using formula v2" is always recoverable.

---

## BEHAVIORS SUPPORTED

- B1 (Convergent accuracy) — Formulas get measurably better over time through calibration and signal discovery
- B2 (Reproducible scoring) — Any historical score can be attributed to the exact formula version that produced it
- B3 (Open contribution) — The registry pattern makes community proposals structurally possible
- B4 (Coverage expansion) — Clear process for creating formulas for unscored capabilities

## BEHAVIORS PREVENTED

- A1 (Stale formulas) — Evolution mechanisms ensure formulas change when data says they should
- A2 (Untraceable changes) — Versioning makes every modification visible and auditable
- A3 (Content leakage) — All formulas must use only the 7 topology primitives + universe graph observables; review enforces this

---

## PRINCIPLES

### Principle 1: Educated Guesses Are the Starting Point, Not the Destination

The 35 existing formulas are v1 — first approximations. They will be wrong in specific, identifiable ways. This is expected and healthy. The system's value comes not from perfect initial formulas but from the machinery that makes them better over time.

### Principle 2: The Registry Is the Architecture

The `@register` decorator pattern in `registry.py` is not just an implementation convenience — it is the architectural decision that makes formula evolution possible. Formulas are registered by capability_id, which means they can be replaced, A/B tested, and versioned independently. Any formula evolution design must preserve this pattern.

### Principle 3: Topology-Only Is Non-Negotiable

No formula evolution — no matter how much it would improve accuracy — may introduce content-reading signals. The 7 brain topology primitives and the universe graph observables in `PRIMITIVES_Universe_Graph.md` are the complete signal space. A formula that achieves 95% accuracy by reading brain content is worse than one that achieves 70% accuracy from topology alone. This is a hard constraint, not a tradeoff.

### Principle 4: Shadow Testing Before Deployment

No formula change goes live without running in shadow mode first: the new formula computes scores alongside the old one, both are recorded, but only the old one is used for interventions. After sufficient shadow data (minimum 2 weeks), compare outcomes. Only if the new formula performs equal or better does it replace the old one.

---

## DATA

| Source | Type | Purpose / Description |
|--------|------|-----------------------|
| `services/health_assessment/scoring_formulas/registry.py` | FILE | The @register decorator pattern, CapabilityScore dataclass, FormulaFn type |
| `services/health_assessment/scoring_formulas/*.py` | FILE | 14 formula files covering 35 capabilities across all aspects |
| `docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md` | FILE | The 7 topology primitives and universe graph observables |
| `docs/specs/personhood_ladder.json` | FILE | All 104 capabilities with verification criteria |
| `data/health_history/{citizen_id}/{date}.json` | DIR | Historical scores with capability breakdown — the calibration dataset |

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| `assessment/daily_citizen_health` | Provides the scoring pipeline and formula invocation mechanism |
| `analysis/process_improvement` | Supplies intervention outcome data that reveals formula inaccuracy |
| `research/longitudinal_health` | Provides trend data for signal-outcome correlation analysis |
| `scientific_rigor/calibration` | Defines the statistical methods for weight adjustment |
| `scientific_rigor/reproducibility` | Ensures versioned formulas produce deterministic results |

---

## INSPIRATIONS

- **Machine learning hyperparameter tuning** — Same concept: initial parameters are educated guesses, systematic search finds better ones. But we keep humans in the loop instead of automated optimization, because formula meaning matters.
- **Open source contribution model** — Anyone can propose a change, but it goes through review and testing before adoption. The registry pattern is GraphCare's equivalent of a well-defined API that external contributors can implement against.
- **Scientific instrument calibration** — A thermometer is calibrated against known temperatures. A scoring formula is calibrated against known outcomes. Both require reference standards and regular recalibration.

---

## SCOPE

### In Scope

- Formula versioning (version numbers, changelogs, deployment dates)
- Weight calibration process (adjusting weights based on outcome data)
- Signal discovery process (finding new predictive primitives)
- Community proposal workflow (submit, review, shadow test, adopt/reject)
- Coverage tracking (which capabilities have formulas, which need them)
- Shadow testing infrastructure (run new formula alongside old, compare)

### Out of Scope

- The formulas themselves → see: `services/health_assessment/scoring_formulas/`
- Intervention outcome measurement → see: `analysis/process_improvement`
- Statistical calibration methods → see: `scientific_rigor/calibration`
- A/B testing methodology → see: `research/technique_measurement`

---

## MARKERS

<!-- @mind:todo Add version field to @register decorator (capability_id, version) -->
<!-- @mind:todo Create formula changelog format and storage location -->
<!-- @mind:todo Build shadow testing harness: run two formulas, record both, use original for interventions -->
<!-- @mind:proposition Consider a "formula playground" where citizens can test proposed formulas against their own historical data -->
