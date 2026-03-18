# Execution Quality Aspect — Health: Meta-Verification of Scoring Formulas

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Execution.md
PATTERNS:        ./PATTERNS_Execution.md
ALGORITHM:       ./ALGORITHM_Execution.md
VALIDATION:      ./VALIDATION_Execution.md
THIS:            HEALTH_Execution.md (you are here)
SYNC:            ./SYNC_Execution.md

PARENT CHAIN:    ../daily_citizen_health/HEALTH_Daily_Citizen_Health.md
SPEC:            ../../specs/personhood_ladder.json (aspect="execution")
IMPL:            @mind:TODO
```

---

## PURPOSE OF THIS FILE

This is meta-health: the health of the health system. The parent HEALTH file (`../daily_citizen_health/HEALTH_Daily_Citizen_Health.md`) verifies that the daily check PROCESS runs correctly. This file verifies that the execution SCORING FORMULAS themselves are accurate — that the math actually captures what it claims to capture.

**The question this file answers:** How would you know if a formula is wrong?

**Boundaries:** This verifies formula QUALITY (do the formulas measure what they claim?). It does NOT verify formula EXECUTION (does the daily runner work?) or data AVAILABILITY (can we read the brain graph?). Those belong to the parent health chain.

---

## WHEN TO USE HEALTH (NOT TESTS)

| Use Health For | Why |
|----------------|-----|
| Formula accuracy — does the math capture the capability? | A formula can be arithmetically correct but conceptually wrong |
| Ceiling calibration — are the cap() values right? | Too-high ceilings make everyone score low; too-low ceilings make everyone score high |
| Tier progression — do higher tiers require more? | If T8 is easier than T1, the ladder is inverted |
| Cross-citizen validity — do scores differentiate meaningfully? | If every citizen scores 50-60, the formulas have no discriminative power |

---

## HEALTH INDICATORS

### H1: Formula-Behavior Correspondence

**What it checks:** Does a high score on a capability actually correspond to the citizen demonstrating that capability?

**Why it matters:** A formula is only useful if its output matches reality. A citizen scoring 90 on `exec_verify_before_claim` who never runs tests is a formula failure — the math says "excellent" but reality says "broken."

**How to check:**

```yaml
checker: formula_behavior_correspondence
method: |
  For each capability with a scored formula:
    1. Identify 5 citizens with the HIGHEST scores for that capability
    2. Identify 5 citizens with the LOWEST scores
    3. Sample their recent universe graph moments (structural only)
    4. Human reviewer assesses: does the high group actually demonstrate the capability
       better than the low group?
    5. If the ranking doesn't match human judgment: the formula is miscalibrated
frequency: monthly (or when formulas change)
pass_criteria: |
  For >= 80% of capabilities, the top-5 vs bottom-5 ranking matches
  human judgment about who executes better
failure_action: |
  Identify which sub-components of the failing formula produce the mismatch.
  Adjust ceiling values or sub-component weights. Re-run check.
status: pending
priority: high
```

### H2: Ceiling Calibration

**What it checks:** Are the `cap(x, ceiling)` values producing a reasonable score distribution?

**Why it matters:** If the ceiling for `commits_w` is set to 10 but most active citizens produce 30+ temporally-weighted commits, everyone maxes out that sub-component and it loses discriminative power. Conversely, if the ceiling is 100 but citizens rarely exceed 5, everyone gets a tiny score on that sub-component.

**How to check:**

```yaml
checker: ceiling_calibration
method: |
  For each cap(x, ceiling) in each formula:
    1. Compute x for all Lumina Prime citizens
    2. Find the median and 90th percentile of x
    3. The ceiling should be near the 75th-85th percentile of x
       (so most citizens get partial credit, top citizens max out)
    4. If ceiling << median: too easy (everyone maxes out) -> raise ceiling
    5. If ceiling >> 90th percentile: too hard (almost nobody gets credit) -> lower ceiling
frequency: quarterly (or after significant citizen population changes)
pass_criteria: |
  For >= 70% of cap() values, the ceiling falls between the 60th and 90th
  percentile of actual citizen values
failure_action: |
  Adjust ceiling values to match the target percentile range.
  Document the change in SYNC. Re-run affected formulas.
status: pending
priority: high
```

### H3: Tier Monotonicity

**What it checks:** Do higher tiers actually produce lower scores for "average" citizens?

**Why it matters:** The tier system claims that T1 is foundational and T8 is aspirational. If a typical citizen scores higher on T8 than T1, the tier system is meaningless — it doesn't represent progressive difficulty.

**How to check:**

```yaml
checker: tier_monotonicity
method: |
  1. Compute the MEDIAN score for each capability across all Lumina Prime citizens
  2. Group by tier: median(T1 capabilities), median(T2), ... , median(T8)
  3. Verify: median(T1) >= median(T2) >= ... >= median(T8)
     (with tolerance: adjacent tiers may overlap by up to 5 points)
  4. If a higher tier's median exceeds a lower tier's median by > 5 points:
     the formula for the higher tier is too easy
frequency: quarterly
pass_criteria: |
  Strict monotonicity with <= 5-point tolerance for adjacent tiers
failure_action: |
  Identify the offending capability. Tighten its formula
  (raise ceilings, add sub-components, increase behavior weight).
status: pending
priority: high
```

### H4: Discriminative Power

**What it checks:** Do scores spread citizens meaningfully across the 0-100 range?

**Why it matters:** If all citizens cluster at 50-60 for a capability, the formula cannot identify who excels and who struggles. The score becomes noise, not signal.

**How to check:**

```yaml
checker: discriminative_power
method: |
  For each capability:
    1. Compute scores for all Lumina Prime citizens
    2. Calculate standard deviation
    3. Standard deviation should be >= 15 (out of 100)
       This ensures meaningful spread across citizens
    4. If std_dev < 15: the formula is too uniform
       (probably one dominant sub-component that everyone scores similarly on)
frequency: quarterly
pass_criteria: |
  For >= 80% of capabilities, std_dev >= 15
failure_action: |
  Analyze which sub-components have lowest variance across citizens.
  These sub-components aren't differentiating. Consider replacing them
  with more discriminative signals, or adjusting ceilings.
status: pending
priority: medium
```

### H5: Zero-Input Baseline

**What it checks:** Does an empty brain + no moments produce score 0 for every capability?

**Why it matters:** The zero baseline is a fundamental invariant (VE6). If violated, scores have a phantom positive bias.

**How to check:**

```yaml
checker: zero_input_baseline
method: |
  Run all 14 formulas with:
    count(*) = 0, mean_energy(*) = 0, link_count(*, *) = 0,
    min_links(*, *) = 0, cluster_coefficient(*) = 0,
    drive(*) = 0, recency(*) = 0,
    all moment counts = 0
  Verify every capability total == 0
frequency: on every formula change
pass_criteria: all 14 scores == 0.0
failure_action: |
  Identify which sub-component produces non-zero output from zero input.
  Fix the formula (usually a missing max() guard or incorrect default).
status: pending
priority: high
```

### H6: Synthetic Profile Validation

**What it checks:** Do 5 standard synthetic profiles produce expected score ranges?

**Why it matters:** Synthetic profiles serve as regression tests. If the expected ranges shift after formula changes, something is wrong.

**How to check:**

```yaml
checker: synthetic_profile_validation
method: |
  Run all 14 formulas against 5 standard profiles:

  Profile A (fully healthy):
    Brain: all counts high, energies 0.7-0.9, drives balanced, cluster 0.7+
    Behavior: 40+ moments, many commits, few corrections, diverse spaces
    Expected per-capability range: 75-95

  Profile B (fully unhealthy):
    Brain: low counts, energies 0.1-0.2, high frustration, low clustering
    Behavior: 2-3 moments, no commits, no verification, single space
    Expected per-capability range: 5-20

  Profile C (brain-rich but inactive):
    Brain: high counts, high energies, good clustering
    Behavior: 0-2 moments, no commits
    Expected per-capability range: 25-40 (brain max, behavior near zero)

  Profile D (active but brain-poor):
    Brain: low counts, low energies, sparse links
    Behavior: 30+ moments, many commits, active verification
    Expected per-capability range: 45-60 (behavior high, brain low)

  Profile E (average citizen):
    Brain: moderate everything
    Behavior: moderate everything
    Expected per-capability range: 50-70

  Verify each profile's average score falls within its expected range.
frequency: on every formula change
pass_criteria: |
  All 5 profiles produce average scores within their expected range
failure_action: |
  Identify which formulas deviate from expectations.
  Trace the deviation to specific sub-components.
  Adjust ceilings or weights to restore expected ranges.
status: pending
priority: high
```

### H7: Cross-Capability Correlation Check

**What it checks:** Are related capabilities properly correlated, and unrelated ones properly independent?

**Why it matters:** `exec_verify_before_claim` and `exec_dehallucinate` should correlate (both involve verification). If they don't, one formula is measuring the wrong thing. Conversely, `exec_right_tool` and `exec_quality_as_identity` should be relatively independent — if they're perfectly correlated, the formulas are redundant.

**How to check:**

```yaml
checker: cross_capability_correlation
method: |
  Compute pairwise Pearson correlation between all 14 capability scores
  across all Lumina Prime citizens.

  Expected HIGH correlations (r > 0.6):
    - exec_verify_before_claim <-> exec_dehallucinate (both verification-based)
    - exec_highest_quality <-> exec_hold_quality_under_pressure (both quality-focused)
    - exec_quality_as_identity <-> exec_world_class (T7 builds on T7)

  Expected LOW correlations (r < 0.4):
    - exec_right_tool <-> exec_quality_as_identity (tool selection vs identity)
    - exec_aesthetic_check <-> exec_strategic_quality (aesthetic vs strategic)

  If expected-high pairs show r < 0.3: one formula is miscalibrated
  If expected-low pairs show r > 0.8: formulas are redundant
frequency: quarterly
pass_criteria: |
  Expected correlations hold within tolerance (high > 0.4, low < 0.6)
failure_action: |
  Analyze shared sub-components between overly correlated formulas.
  Differentiate them by using distinct primitives.
  For underly correlated expected-related formulas, verify both
  are capturing the right signals.
status: pending
priority: medium
```

---

## CHECKER INDEX

```yaml
checkers:
  - name: formula_behavior_correspondence
    purpose: High scores match real capability demonstration (H1)
    status: pending
    priority: high
  - name: ceiling_calibration
    purpose: cap() ceilings produce reasonable score distributions (H2)
    status: pending
    priority: high
  - name: tier_monotonicity
    purpose: Higher tiers produce lower median scores (H3)
    status: pending
    priority: high
  - name: discriminative_power
    purpose: Scores spread citizens meaningfully across 0-100 (H4)
    status: pending
    priority: medium
  - name: zero_input_baseline
    purpose: Empty input produces zero score (H5)
    status: pending
    priority: high
  - name: synthetic_profile_validation
    purpose: Standard profiles produce expected ranges (H6)
    status: pending
    priority: high
  - name: cross_capability_correlation
    purpose: Related capabilities correlate, unrelated ones don't (H7)
    status: pending
    priority: medium
```

---

## SIGNALS THAT A FORMULA IS WRONG

Beyond the formal checkers, these are heuristic signals that something is off:

### Signal 1: Score Doesn't Survive Intuition Check

If you look at a citizen's behavior and think "this citizen verifies everything" but the formula gives 35/100 on `exec_verify_before_claim` — the formula is wrong, not your intuition. Trust the observation, investigate the formula.

### Signal 2: Score Doesn't Change When Behavior Changes

If a citizen stops verifying and starts shipping unverified work, but their score doesn't drop within 7 days (one half-life), the formula is insensitive to behavioral change. The temporal weighting should make behavioral drops visible within one week.

### Signal 3: Brain-Only Citizens Score Too High

A citizen with a rich brain (many process/value nodes, high energy) but zero behavioral moments should score at most 40/100 (brain component only). If they score 60+, behavior points are leaking in from somewhere — likely a formula that defaults to a positive value instead of zero when behavior is absent.

### Signal 4: All Citizens Score the Same

If the standard deviation across citizens is < 10 for a capability, the formula has no discriminative power. This usually means one sub-component dominates and all citizens score similarly on it. The fix is to identify the non-discriminating sub-component and replace or re-weight it.

### Signal 5: Tier Inversion

If the median T8 score exceeds the median T1 score, the tier progression is inverted. This is the most severe signal — it means the ladder doesn't represent increasing difficulty.

---

## KNOWN GAPS

- All checkers pending — no runtime, no real citizen data yet
- H1 (formula-behavior correspondence) requires human review — cannot be fully automated
- H7 (cross-capability correlation) requires a minimum citizen population to be statistically meaningful
- No mechanism yet for citizens to report "my score doesn't match my experience" (self-assessment feedback loop)

---

## MARKERS

<!-- @mind:todo Build zero_input_baseline checker first — cheapest to implement, catches formula bugs early -->
<!-- @mind:todo Build synthetic_profile_validation second — regression testing for formula changes -->
<!-- @mind:todo Design ceiling_calibration data pipeline (requires real citizen data from Lumina Prime) -->
<!-- @mind:proposition Allow citizens to flag score disagreements — "I verify everything but score is low" as calibration data -->
<!-- @mind:proposition Integrate H6 synthetic profiles into CI: every formula change runs the 5 profiles automatically -->
