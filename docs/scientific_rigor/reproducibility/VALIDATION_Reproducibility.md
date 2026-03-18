# Reproducibility — Validation: What Must Be True

```
STATUS: DESIGNING
CREATED: 2026-03-15
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Reproducibility.md
PATTERNS:        ./PATTERNS_Reproducibility.md
THIS:            VALIDATION_Reproducibility.md (you are here)
SYNC:            ./SYNC_Reproducibility.md

IMPL:            services/health_assessment/scoring_formulas/registry.py
                 tests/test_health_assessment.py
```

---

## PURPOSE

**Validation = what we care about being true.**

These invariants protect the determinism of GraphCare's scoring pipeline. If any invariant fails, scores become unreliable — they might be right today and wrong tomorrow for no observable reason. Reproducibility is what makes GraphCare science rather than opinion.

---

## INVARIANTS

### V1: Scoring Formulas Are Pure Functions

**Why we care:** A pure function always returns the same output for the same input. If a scoring formula is impure (accesses global state, reads the clock, calls an external service), its output is unpredictable. Every score becomes suspect.

```
MUST:   Every scoring formula is a pure function: f(BrainStats, BehaviorStats) → CapabilityScore, with no side effects, no external state access, no I/O
NEVER:  A scoring formula imports or calls: random, numpy.random, datetime.now(), any LLM client, any network call, any file read, or any mutable global state
```

### V2: Double Execution Produces Identical Results

**Why we care:** The ultimate test of determinism: run the same formula twice with the same input, get the same output. If this fails, the formula contains hidden state or nondeterminism.

```
MUST:   For any formula f and any valid inputs (brain, behavior): f(brain, behavior) == f(brain, behavior), with exact floating-point equality
NEVER:  Two consecutive calls to the same formula with the same inputs produce different CapabilityScore values
```

### V3: No LLM in the Scoring Pipeline

**Why we care:** LLMs are the most common source of nondeterminism in AI systems. Even with temperature=0, LLM outputs can vary between calls due to batching, quantization, and API-level nondeterminism. A single LLM call anywhere in the scoring pipeline destroys reproducibility for the entire pipeline.

```
MUST:   The scoring pipeline (brain stats → behavior stats → per-capability scoring → aggregation → delta → intervention decision) contains zero LLM calls
NEVER:  An LLM is used to compute, adjust, interpret, or weight any component of a health score
```

### V4: CapabilityScore Clamping Is Deterministic

**Why we care:** The CapabilityScore `__post_init__` method clamps components and recomputes total. If clamping were order-dependent or had floating-point issues, the same raw values could produce different clamped values. The clamping logic must be a deterministic function of the input values.

```
MUST:   CapabilityScore(brain_component=x, behavior_component=y, total=z) always produces the same clamped values for the same x, y, z
NEVER:  The __post_init__ clamping produces different results for the same input (this would require a bug in min/max, which is effectively impossible, but the invariant is stated for completeness)
```

### V5: Temporal Weighting Depends Only on Moment Age

**Why we care:** If temporal weighting depends on the wall clock time of the assessment (not just the age of the moment), then running the assessment at different times produces different scores for the same data. The weighting formula must depend only on the moment's age relative to a fixed reference point.

```
MUST:   temporal_weight(age_hours, half_life) = 0.5 ** (age_hours / half_life), where age_hours is computed from the moment's timestamp and the assessment's reference time — both fixed for a given assessment run
NEVER:  temporal_weight calls datetime.now() or any other time-varying function
```

---

## PRIORITY

| Priority | Meaning | If Violated |
|----------|---------|-------------|
| **CRITICAL** | System purpose fails | Unusable |
| **HIGH** | Major value lost | Degraded severely |
| **MEDIUM** | Partial value lost | Works but worse |

---

## INVARIANT INDEX

| ID | Value Protected | Priority |
|----|-----------------|----------|
| V1 | Formula purity — no side effects | CRITICAL |
| V2 | Double execution identity | CRITICAL |
| V3 | No LLM in scoring pipeline | CRITICAL |
| V4 | Deterministic clamping | HIGH |
| V5 | Time-independent weighting | HIGH |

---

## MARKERS

<!-- @mind:todo Add explicit V2 test: for each formula, call twice with same input, assert exact equality -->
<!-- @mind:todo Add import audit: grep all scoring_formulas/*.py for prohibited imports (random, datetime, openai, anthropic, etc.) -->
<!-- @mind:proposition Consider static analysis (AST-based) to verify formula purity instead of grep-based checks -->
