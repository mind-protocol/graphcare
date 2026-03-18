# OBJECTIVES — Reproducibility

```
STATUS: DESIGNING
CREATED: 2026-03-15
VERIFIED: —
```

---

## CHAIN

```
THIS:            OBJECTIVES_Reproducibility.md (you are here - START HERE)
PATTERNS:       ./PATTERNS_Reproducibility.md
VALIDATION:     ./VALIDATION_Reproducibility.md
SYNC:           ./SYNC_Reproducibility.md

IMPL:           services/health_assessment/scoring_formulas/registry.py
                tests/test_health_assessment.py
```

**Read this chain in order before making changes.** Each doc answers different questions. Skipping ahead means missing context.

---

## PRIMARY OBJECTIVES (ranked)

1. **Same data produces same score, always** — Given identical BrainStats and BehaviorStats input, the scoring pipeline must produce bitwise identical CapabilityScore output regardless of when, where, or how many times it runs. No randomness. No LLM calls. No floating-point nondeterminism. Pure math.

2. **Any party can verify any score** — GraphCare's scoring pipeline is deterministic and open. A citizen, a researcher, or an auditor can take the same input data, run the same formulas, and get the same result. Reproducibility is the foundation of scientific credibility and citizen trust.

3. **Score differences are always attributable** — If a citizen's score changes between two assessments, the difference must be entirely attributable to changes in input data (brain topology or behavior stats), changes in formula weights (documented calibration), or changes in formula code (versioned in git). No unexplained variance.

## NON-OBJECTIVES

- **Reproducibility of the data collection step** — Brain topology changes between reads (drives fluctuate, nodes get created, energy decays). The data collection step is inherently non-reproducible. Reproducibility applies to the scoring step: given a snapshot of data, scoring is deterministic.
- **Cross-version reproducibility** — When formula weights change (calibration) or formula code changes (new version), scores change. This is intentional. Reproducibility means "same version + same input = same output," not "all versions produce the same output."
- **Exact floating-point portability** — Different CPU architectures may produce slightly different floating-point results. We target reproducibility within a single platform (FP epsilon tolerance), not cross-platform bitwise identity.

## TRADEOFFS (canonical decisions)

- When **convenience** conflicts with **determinism**, choose determinism. An LLM that generates more natural intervention messages is tempting, but LLM outputs are nondeterministic. The scoring pipeline must never include an LLM call.
- We accept **less "intelligent" scoring** to preserve full determinism. Math functions with fixed weights are less flexible than learned models but are perfectly reproducible.
- We accept **test complexity** (explicitly testing determinism) over **assumed determinism** (trusting that the code is deterministic without verification).

## SUCCESS SIGNALS (observable)

- `test_health_assessment.py` proves determinism: running the same profile through the same formula twice produces identical results
- All scoring formulas are composed of basic arithmetic operations: addition, multiplication, min, max, division, and the `_cap()` helper
- No import of `random`, `numpy.random`, `torch`, or any LLM client exists in `scoring_formulas/`
- The aggregator's delta computation is deterministic: yesterday's score is loaded from history (fixed), today's score is computed (deterministic), delta is subtraction
