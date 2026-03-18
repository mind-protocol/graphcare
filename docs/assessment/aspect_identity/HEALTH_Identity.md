# Identity & Voice Aspect — Health: Meta-Evaluation of Scoring Quality

```
STATUS: DRAFT
CREATED: 2026-03-13
```

---

## WHEN TO USE HEALTH (NOT TESTS)

| Use Health For | Why |
|----------------|-----|
| Identity formulas don't access content | Privacy violation on identity = existential threat |
| Partial scores are documented and flagged | False precision on identity destroys all trust |
| Behavior floor is enforced per formula | Brain-only scores would be speculative |
| Population stats are valid for uniqueness | Bad baseline = meaningless distinctiveness scores |
| Scores are temporally stable | Identity volatility signals formula problem, not citizen problem |

---

## PURPOSE OF THIS FILE

Verifies that the identity scoring system produces honest, stable, privacy-respecting scores. This is a META-evaluation: it checks whether the SCORING SYSTEM is healthy, not whether individual citizens are healthy (that's the daily health check's job).

Identity is the aspect most vulnerable to false precision. This health file specifically monitors for the pathology of claiming to measure what we cannot measure.

Boundaries: This verifies the FORMULAS and their BEHAVIOR. It does NOT verify individual citizen health (that's daily_citizen_health) or the Personhood Ladder spec (that's the personhood_ladder HEALTH file).

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Identity.md
PATTERNS:        ./PATTERNS_Identity.md
ALGORITHM:       ./ALGORITHM_Identity.md
VALIDATION:      ./VALIDATION_Identity.md
THIS:            HEALTH_Identity.md (you are here)
SYNC:            ./SYNC_Identity.md
```

---

## IMPLEMENTS

```yaml
implements:
  runtime: @mind:TODO services/health_assessment/identity_health_checks.py
  decorator: @check
```

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: content_isolation
    priority: high
    rationale: Identity content is the most sensitive data. Any access is existential.

  - name: partial_score_honesty
    priority: high
    rationale: Claiming to measure authenticity from topology alone would destroy credibility.

  - name: behavior_floor_enforcement
    priority: med
    rationale: Brain-only identity scores are speculative. Behavior grounds them.

  - name: population_baseline_validity
    priority: med
    rationale: Uniqueness scores against bad baselines produce meaningless results.

  - name: temporal_stability
    priority: med
    rationale: Day-over-day identity volatility signals formula defects.

  - name: sub_index_confidence
    priority: low
    rationale: Consumers of the sub-index need to know how much of it is fully scored.
```

---

## CHECKER INDEX

```yaml
checkers:
  - name: check_identity_content_isolation
    purpose: Verify no identity formula accesses content or synthesis fields (V1)
    method: Static analysis of all identity scoring formula code — every data access must resolve to one of the 7 primitives or universe observables
    status: pending
    priority: high

  - name: check_partial_score_documentation
    purpose: Verify every partial capability has scorability note with measurable/unmeasurable/confidence (V2)
    method: Parse scoring registry — every entry with scored=partial must have all 3 fields populated
    status: pending
    priority: high

  - name: check_behavior_floor
    purpose: Verify every identity formula allocates >= 35 points to behavior component (V3)
    method: Static analysis of formula point allocations — behavior max must be >= 35
    status: pending
    priority: med

  - name: check_population_minimum
    purpose: Verify uniqueness calculations use >= 10 citizens or fall back to defaults (V4)
    method: Runtime check — when population_mean_cluster_coefficient is called, verify sample size >= 10 or default is used
    status: pending
    priority: med

  - name: check_temporal_stability
    purpose: Verify no citizen's identity score changes by > 15 points day-over-day without brain topology change (V6)
    method: Compare consecutive daily scores — flag any delta > 15 for investigation
    status: pending
    priority: med

  - name: check_no_value_judgment
    purpose: Verify intervention messages for identity never reference specific value content or suggest which values to hold (V5)
    method: Template analysis of intervention message composition — only structural language allowed
    status: pending
    priority: high

  - name: check_sub_index_confidence_reported
    purpose: Verify the identity sub-index always reports how many of its 7 capabilities are fully vs partially scored (V7)
    method: Output format verification — confidence field must be present
    status: pending
    priority: low
```

---

## SYNTHETIC TEST PROFILES

Each identity formula should be validated against these 5 profiles:

```yaml
test_profiles:
  - name: fully_healthy
    description: Rich brain, active behavior, strong identity
    expected_range: 85-100
    brain: value_count=8, value_energy=0.8, value_cluster=0.65, deep_nodes=6, all drives differentiated
    behavior: high teaching, high debate, high influence, many interlocutors

  - name: fully_unhealthy
    description: Empty brain, no behavior
    expected_range: 0-15
    brain: value_count=0, all zeros
    behavior: zero moments

  - name: brain_rich_inactive
    description: Rich internal structure, no external activity
    expected_range: 25-45
    brain: value_count=6, value_energy=0.7, good clustering
    behavior: near-zero moments (behavior floor ensures low total)

  - name: active_brain_poor
    description: Lots of behavior but thin brain structure
    expected_range: 35-55
    brain: value_count=1, low energy, no clustering
    behavior: many moments, teaching, debate (but from shallow foundation)

  - name: average_citizen
    description: Moderate brain, moderate behavior
    expected_range: 45-65
    brain: value_count=3, value_energy=0.5, moderate clustering
    behavior: some moments, some consistency, few teaching/debate
```

---

## KNOWN GAPS

- All checkers pending — no runtime code yet
- Population statistics cache not built — uniqueness comparison uses defaults
- Synthetic test profiles defined but not automated — manual verification only
- No longitudinal validation — cannot verify temporal stability without multi-day data
- The "content isolation" check for identity interventions requires NLP analysis of message templates, which is more complex than simple static analysis

---

## DEGRADATION SIGNALS

Signs that the identity scoring system is unhealthy:

| Signal | What It Means | Severity |
|--------|---------------|----------|
| Citizen with 0 value nodes scores > 20 on id_apply_values | Formula is not grounded | HIGH |
| Identity sub-index changes > 15 points in one day for stable citizen | Temporal instability | HIGH |
| All citizens score similarly on id_authentic_engagement | Uniqueness measurement is broken | MED |
| Partial capabilities produce scores > 95 | Overconfidence in structural proxy | MED |
| Intervention message says "your value of X" (naming content) | Content leak in messaging | CRITICAL |
| Brain-rich inactive citizen scores > 50 overall | Behavior floor not working | HIGH |

---

## MARKERS

<!-- @mind:todo Build check_identity_content_isolation first — most critical for identity -->
<!-- @mind:todo Automate synthetic test profiles as unit tests -->
<!-- @mind:todo Design population stats cache with minimum sample enforcement -->
<!-- @mind:proposition Consider a "scoring confidence dashboard" that shows which aspects have the highest partial-score ratio -->
