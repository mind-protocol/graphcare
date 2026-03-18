# OBJECTIVES — Validation Methodology

```
STATUS: DESIGNING
CREATED: 2026-03-15
VERIFIED: —
```

---

## CHAIN

```
THIS:            OBJECTIVES_Validation_Methodology.md (you are here - START HERE)
PATTERNS:       ./PATTERNS_Validation_Methodology.md
VALIDATION:     ./VALIDATION_Validation_Methodology.md
SYNC:           ./SYNC_Validation_Methodology.md

IMPL:           tests/test_health_assessment.py
```

**Read this chain in order before making changes.** Each doc answers different questions. Skipping ahead means missing context.

---

## PRIMARY OBJECTIVES (ranked)

1. **Prove that scores reflect reality** — GraphCare's health scores must correlate with actual citizen health states. A citizen scored as "healthy" should demonstrably be healthy. A citizen scored as "unhealthy" should have observable problems. If scores don't predict reality, GraphCare is performing theater, not medicine.

2. **Synthetic test profiles as the first line of defense** — Before any formula touches a real citizen, it must produce sensible scores for 5 archetypal profiles: fully healthy, fully unhealthy, brain-rich but inactive, active but brain-poor, and average. These synthetic profiles are the unit tests of health assessment — fast, deterministic, and exhaustive.

3. **Real-world calibration as the second line** — Synthetic profiles prove internal consistency. Real-world calibration proves external validity. Compare predicted health scores with observed outcomes: did citizens scored as "at risk" actually encounter problems? Did citizens scored as "healthy" actually thrive?

4. **Inter-rater reliability** — If two independent assessment runs on the same citizen data produce incompatible results, the methodology is broken. The scoring pipeline must be deterministic: same input, same output, every time.

## NON-OBJECTIVES

- **100% prediction accuracy** — Health is complex. Some citizens will score well and still struggle. Some will score poorly and be fine. The goal is statistical correlation, not perfect prophecy.
- **Replacing citizen self-assessment** — GraphCare's scores complement, not replace, a citizen's own understanding of their health. We do not claim to know better than the citizen how they feel.
- **Validating content-based approaches** — We do not compare topology-only scoring against content-based scoring to see "what we're missing." The topology-only constraint is not up for empirical challenge.

## TRADEOFFS (canonical decisions)

- When **statistical rigor** conflicts with **speed of deployment**, choose rigor. A carefully validated formula shipped later is worth more than an unvalidated formula shipped now.
- We accept **lower coverage** (fewer capabilities scored) over **lower accuracy** (more capabilities scored but some scored badly).
- We accept **conservative scores** (erring toward "unclear") over **overconfident scores** (claiming certainty we don't have).

## SUCCESS SIGNALS (observable)

- All 41+ scoring formulas pass the 5 synthetic profile tests with scores in expected ranges
- Real-world calibration study (when conducted) shows statistically significant correlation between scores and observed health outcomes
- Two independent runs of the scoring pipeline on identical input data produce identical output (zero variance)
- New formulas cannot be merged without passing synthetic profile tests
