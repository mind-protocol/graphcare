# Calibration — Validation: What Must Be True

```
STATUS: DESIGNING
CREATED: 2026-03-15
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Calibration.md
PATTERNS:        ./PATTERNS_Calibration.md
THIS:            VALIDATION_Calibration.md (you are here)
SYNC:            ./SYNC_Calibration.md

IMPL:            services/health_assessment/scoring_formulas/ (all formula files)
```

---

## PURPOSE

**Validation = what we care about being true.**

These invariants protect the integrity of the calibration process itself. Calibration is how GraphCare improves — but calibration done wrong is how GraphCare degrades. These invariants ensure that every adjustment makes things better, or at least does not make them worse.

---

## INVARIANTS

### V1: Synthetic Profiles Survive Calibration

**Why we care:** Synthetic profiles represent known-good behavior. If calibration causes a healthy citizen to score below 85 or an unhealthy citizen to score above 20, the adjustment has broken fundamental score semantics. The profiles are the floor — calibration builds upward from them, never through them.

```
MUST:   After every weight adjustment, all 5 synthetic profile tests pass with scores in their expected ranges
NEVER:  A calibration adjustment is deployed that causes any synthetic profile test to fail
```

### V2: Every Adjustment Is Documented

**Why we care:** Undocumented weight changes are invisible technical debt. Future maintainers will not know why a weight is 0.35 instead of 0.5. If calibration results are poor, undocumented changes cannot be traced or reverted. Documentation is not overhead — it is the mechanism that makes calibration reversible.

```
MUST:   Every weight change has a documented reason (the data that motivated it), the before/after values, and the expected impact
NEVER:  A weight is changed in a scoring formula without a corresponding entry in the calibration log or commit message
```

### V3: One Variable at a Time

**Why we care:** Changing multiple weights simultaneously makes it impossible to attribute improvements or regressions to specific changes. If three weights change and scores improve, which change helped? If scores degrade, which change hurt? Single-variable adjustment preserves causal clarity.

```
MUST:   Each calibration adjustment changes weights for exactly one identified issue (which may involve one or a few related weights within a single formula)
NEVER:  Multiple unrelated weight changes are bundled into a single calibration step
```

### V4: The 40/60 Split Is Sacred

**Why we care:** The brain (0-40) and behavior (0-60) component boundaries encode a design principle: action matters more than potential. Calibration adjusts weights within these boundaries. If calibration suggests the boundaries themselves are wrong, that is a design conversation, not a calibration adjustment.

```
MUST:   Calibration adjusts only the weights within brain_component and behavior_component formulas — the component ceilings (40 and 60) remain fixed
NEVER:  A calibration adjustment modifies the CapabilityScore clamping bounds or effectively circumvents them by rescaling weights to make one component dominate
```

### V5: Bias Is Tracked Over Time

**Why we care:** A single calibration cycle might fix one bias while introducing another. Only longitudinal tracking reveals whether biases are actually decreasing. If the same bias reappears after correction, the formula structure (not just the weights) may need redesign.

```
MUST:   Bias analysis results are recorded for each calibration cycle, allowing comparison across cycles to verify that biases are decreasing
NEVER:  A bias is "fixed" and then forgotten — it must be re-measured in subsequent cycles to confirm the fix held
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
| V1 | Non-regression — profiles survive calibration | CRITICAL |
| V2 | Traceability — every change documented | HIGH |
| V3 | Causal clarity — one variable at a time | HIGH |
| V4 | Design integrity — 40/60 split preserved | CRITICAL |
| V5 | Bias reduction — tracked longitudinally | MEDIUM |

---

## MARKERS

<!-- @mind:todo Create the calibration log format and storage location (probably docs/scientific_rigor/calibration/log/) -->
<!-- @mind:proposition Consider a "calibration review" process: weight changes require review by at least one other contributor before merge -->
