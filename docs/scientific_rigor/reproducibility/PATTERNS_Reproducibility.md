# Reproducibility — Patterns: Deterministic Scoring as a First Principle

```
STATUS: DESIGNING
CREATED: 2026-03-15
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Reproducibility.md
THIS:            PATTERNS_Reproducibility.md (you are here)
VALIDATION:      ./VALIDATION_Reproducibility.md
SYNC:            ./SYNC_Reproducibility.md

IMPL:            services/health_assessment/scoring_formulas/registry.py
                 tests/test_health_assessment.py
```

### Bidirectional Contract

**Before modifying this doc or the code:**
1. Read ALL docs in this chain first
2. Read `services/health_assessment/scoring_formulas/registry.py` — the formula infrastructure
3. Read `tests/test_health_assessment.py` — the determinism proofs

**After modifying this doc:**
1. Update the IMPL source to match, OR
2. Add a TODO in SYNC: "Docs updated, implementation needs: {what}"
3. Run tests: `pytest tests/test_health_assessment.py -v`

**After modifying the code:**
1. Update this doc chain to match, OR
2. Add a TODO in SYNC: "Implementation changed, docs need: {what}"
3. Run tests: `pytest tests/test_health_assessment.py -v`

---

## THE PROBLEM

Health scores that change for no observable reason destroy trust. If a citizen is scored 72 on Monday and 68 on Tuesday with no change in brain topology or behavior, the citizen has every right to ask: "What changed?" If the answer is "nothing — the scoring is nondeterministic," GraphCare's credibility evaporates.

Nondeterminism can sneak in through many doors:
- LLM calls in scoring (different output each time)
- Random sampling in formulas (different subset each time)
- Floating-point order-of-operations differences (dictionary iteration order varies)
- Time-dependent logic in formulas (scoring at 3am vs 3pm produces different results)
- External API calls that return slightly different data each time

Any of these would mean the same citizen, with the same brain state and same behavior, receives different scores at different times. This is not health assessment — it is noise.

---

## THE PATTERN

**All 7 primitives and all scoring formulas are pure math functions: no randomness, no external calls, no LLM, no time dependency.**

### The Purity Constraint

A scoring formula is a pure function:

```
f(BrainStats, BehaviorStats) → CapabilityScore
```

- **Inputs are immutable dataclasses** — BrainStats and BehaviorStats are frozen snapshots of the citizen's state. Once constructed, they do not change.
- **The function body is arithmetic** — Addition, multiplication, division, min, max, and `_cap(value, ceiling)`. No conditionals that depend on external state. No loops over mutable collections. No I/O.
- **The output is a deterministic dataclass** — CapabilityScore has brain_component, behavior_component, and total. Total is always brain + behavior. Clamping in `__post_init__` is deterministic.

### What "Pure Math" Means Concretely

Every scoring formula follows this pattern:

```python
@register("capability_id")
def score_capability(brain: BrainStats, behavior: BehaviorStats) -> CapabilityScore:
    # Brain component (0-40)
    sub1 = _cap(brain.some_count, ceiling=10) * weight1
    sub2 = brain.some_drive * weight2
    brain_component = (sub1 + sub2) * 40

    # Behavior component (0-60)
    sub3 = _cap(behavior.some_metric, ceiling=15) * weight3
    sub4 = _cap(behavior.other_metric, ceiling=8) * weight4
    behavior_component = (sub3 + sub4) * 60

    return CapabilityScore(
        brain_component=brain_component,
        behavior_component=behavior_component,
        total=0,  # recomputed by __post_init__
    )
```

The operations are: field access, division (in `_cap`), multiplication, addition. No random calls. No LLM calls. No network I/O. No system clock reads. The function is a mathematical mapping from numbers to numbers.

### The Aggregation Chain

Reproducibility extends beyond individual formulas to the full pipeline:

1. **Brain stats computation** — Deterministic: same topology produces same BrainStats. The 7 primitives are counts, averages, and ratios — all deterministic.
2. **Behavior stats computation** — Deterministic: same universe graph moments produce same BehaviorStats. Temporal weighting uses a fixed half-life formula: `0.5 ** (age_hours / 168)`.
3. **Per-capability scoring** — Deterministic: pure math functions as described above.
4. **Aggregation** — Deterministic: mean of scored capabilities. Dictionary iteration order does not affect the mean.
5. **Delta computation** — Deterministic: today's aggregate minus yesterday's aggregate (loaded from history).
6. **Intervention decision** — Deterministic: aggregate < threshold OR drops exist.

Every step is deterministic. The full pipeline is deterministic.

### The Test Proof

`test_health_assessment.py` proves reproducibility through:

1. **Profile consistency** — Each synthetic profile produces scores in fixed ranges. If the test passes today, the same test with the same code will pass tomorrow.
2. **Component bounds** — brain_component is always in [0, 40], behavior_component is always in [0, 60], total is always their sum. Proved for all formulas, all profiles.
3. **CapabilityScore clamping** — The `__post_init__` method deterministically clamps and recomputes total. Tested explicitly.
4. **Stress stimulus formula** — `compute_stress_stimulus(score)` is a single arithmetic expression with deterministic bounds. Tested for monotonicity and bounds across 0-100.
5. **Delta computation** — The aggregator produces deterministic deltas given deterministic inputs.

---

## BEHAVIORS SUPPORTED

- B1 (Deterministic scoring) — Same BrainStats + BehaviorStats always produces same CapabilityScore
- B2 (Auditable results) — Any party can reproduce any score by running the same code on the same data
- B3 (Attributable changes) — Score differences are always traceable to input changes or code changes
- B4 (Testable formulas) — Pure functions are trivially testable: provide input, assert output

## BEHAVIORS PREVENTED

- A1 (Nondeterministic scoring) — No randomness can enter the scoring pipeline
- A2 (LLM-in-the-loop) — LLM calls are nondeterministic by nature and are excluded from scoring
- A3 (Unexplained variance) — Score changes always have a traceable cause
- A4 (Time-dependent scoring) — The same data scored at different times produces the same result (temporal weighting is based on moment age, not current time)

---

## PRINCIPLES

### Principle 1: Purity Is Non-Negotiable

A scoring formula is a pure function or it is not a scoring formula. There is no "mostly deterministic" or "deterministic except for the LLM summary." The entire pipeline, from BrainStats input to CapabilityScore output, must be a mathematical computation with no side effects and no external dependencies.

This is more restrictive than many health assessment systems. It means we cannot use LLMs to "interpret" scores, we cannot use random sampling to estimate statistics, we cannot use external APIs to enrich data. These are deliberate constraints. The benefit — perfect reproducibility — is worth the cost.

### Principle 2: The Test Suite Is the Proof

Claiming determinism is easy. Proving it requires tests. The test suite in `test_health_assessment.py` is not just a regression guard — it is the mathematical proof that the scoring pipeline is deterministic. If the tests pass, determinism holds. If a test fails, determinism has been violated. This is why the tests must be run after every change.

### Principle 3: No LLM, Anywhere in Scoring

LLMs are powerful tools for natural language generation, reasoning, and creativity. They are the opposite of deterministic. Two calls to the same LLM with the same prompt can produce different outputs. This makes LLMs fundamentally incompatible with reproducible scoring.

LLMs may be used elsewhere in GraphCare (e.g., generating intervention message prose, writing research summaries). But they must never be used in the scoring pipeline: not in formula computation, not in aggregation, not in delta calculation, not in intervention threshold decisions.

### Principle 4: Temporal Weighting Is Deterministic

The temporal decay formula `0.5 ** (age_hours / 168)` looks time-dependent but is not. It depends on the age of a moment relative to the assessment time — both of which are fixed when the assessment runs. The same moment assessed at the same time always gets the same temporal weight. The function depends on its inputs, not on the wall clock.

---

## DATA

| Source | Type | Purpose / Description |
|--------|------|-----------------------|
| `services/health_assessment/scoring_formulas/registry.py` | FILE | CapabilityScore dataclass with deterministic clamping; `_cap()` pure helper; formula registry |
| `services/health_assessment/scoring_formulas/*.py` | FILES | All 14 formula modules — each contains pure math scoring functions |
| `tests/test_health_assessment.py` | FILE | 45 tests proving determinism, bounds, and consistency |
| `services/health_assessment/aggregator.py` | FILE | Deterministic aggregation and delta computation |
| `services/health_assessment/stress_stimulus_sender.py` | FILE | Deterministic stress formula with provable bounds |

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| `assessment/daily_citizen_health/` | Defines the scoring pipeline whose determinism we guarantee |
| `scientific_rigor/validation_methodology/` | Uses determinism as the basis for inter-rater reliability |
| `scientific_rigor/calibration/` | Weight changes must preserve determinism — calibration changes values, not purity |

---

## INSPIRATIONS

- **Functional programming** — Pure functions with no side effects are the gold standard for reproducibility. GraphCare's scoring formulas are functional programs embedded in Python.
- **Reproducible research** (FAIR principles) — Findable, Accessible, Interoperable, Reproducible. GraphCare scores meet all four: published formulas, open data format, standard math, deterministic computation.
- **Blockchain consensus** — Every node must compute the same result from the same input. GraphCare's scoring has the same property: any executor, same input, same output.
- **Scientific instrument calibration** — A thermometer that gives different readings for the same temperature is broken. A scoring pipeline that gives different scores for the same data is broken. Both must be deterministic.

---

## SCOPE

### In Scope

- Defining what "deterministic" means for the scoring pipeline
- Identifying all sources of potential nondeterminism and how they are excluded
- The purity constraint on scoring formulas
- The role of `test_health_assessment.py` as the determinism proof
- Temporal weighting determinism argument

### Out of Scope

- Determinism of data collection → data collection is inherently non-reproducible (brain states change)
- Cross-version reproducibility → formula changes intentionally change scores
- Intervention message generation → messages may use non-deterministic text generation in the future; the scoring decision (whether to intervene) is deterministic, the message prose is not required to be
- Cross-platform floating-point identity → we target same-platform reproducibility

---

## MARKERS

<!-- @mind:todo Add explicit determinism test: run all formulas twice on same input, assert bitwise equality -->
<!-- @mind:proposition Consider a "reproducibility badge" on published research: "All scores in this paper can be reproduced by running: pytest tests/test_health_assessment.py" -->
<!-- @mind:todo Audit all formula files for any import of random, numpy.random, datetime.now, or LLM clients -->
