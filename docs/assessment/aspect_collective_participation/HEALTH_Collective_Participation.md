# Collective Participation — Health: Verification Mechanics

```
STATUS: DESIGNING
CREATED: 2026-03-13
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Collective_Participation.md
PATTERNS:        ./PATTERNS_Collective_Participation.md
ALGORITHM:       ./ALGORITHM_Collective_Participation.md
VALIDATION:      ./VALIDATION_Collective_Participation.md
THIS:            HEALTH_Collective_Participation.md (you are here)
SYNC:            ./SYNC_Collective_Participation.md

PARENT:          ../daily_citizen_health/HEALTH_Daily_Citizen_Health.md
```

---

## WHEN TO USE HEALTH (NOT TESTS)

| Use Health For | Why |
|----------------|-----|
| Formulas use only primitives (no content access) | Privacy violation = trust collapse |
| Dialogue detection produces correct ratios | Bad dialogue_ratio = false participation signals |
| Space creation metrics align with actual pioneering | Inflated pioneered_w = false movement building |
| Isolation caps work correctly | A solo citizen scoring high on collective = logical contradiction |
| Temporal decay catches stale participation | Coasting on old activity = misleading health signal |

---

## PURPOSE OF THIS FILE

Verifies that the Collective Participation scoring formulas operate correctly at runtime: produce scores within expected ranges, respect invariants from VALIDATION, and distinguish genuine collective participants from passive or isolated citizens.

Boundaries: This verifies the FORMULAS (do they produce correct scores?). It does NOT verify the daily check runner (that's daily_citizen_health HEALTH) or the Personhood Ladder spec (that's personhood_ladder HEALTH).

---

## IMPLEMENTS

```yaml
implements:
  runtime: @mind:TODO services/health_assessment/aspect_checks/collective_participation.py
  decorator: @check
```

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: content_isolation
    priority: high
    rationale: Collective participation formulas must never access moment content or vote content.
  - name: score_range_validity
    priority: high
    rationale: Every capability score must be in [0, 100] with brain in [0, 40] and behavior in [0, 60].
  - name: isolation_cap_enforcement
    priority: high
    rationale: Citizens with zero or near-zero distinct_actors must score below defined thresholds.
  - name: creation_requirement_enforcement
    priority: high
    rationale: T7/T8 capabilities must score low without space creation activity.
  - name: dialogue_sensitivity
    priority: med
    rationale: Dialogue ratio must create measurable score difference between broadcaster and conversationalist.
  - name: temporal_decay_effectiveness
    priority: med
    rationale: Old participation must score meaningfully lower than recent participation.
  - name: tier_ceiling_progression
    priority: med
    rationale: T8 formulas must be harder to max than T5 formulas given the same inputs.
```

---

## CHECKER INDEX

```yaml
checkers:
  - name: check_content_isolation
    purpose: Verify no scoring formula accesses moment content, vote content, or discussion text (CP1)
    status: pending
    priority: high
    method: Static analysis of formula code — grep for content field access

  - name: check_score_bounds
    purpose: Verify brain_score in [0, 40] and behavior_score in [0, 60] for all 4 capabilities (CP2, CP3)
    status: pending
    priority: high
    method: Run all 5 synthetic profiles through all 4 formulas, assert bounds

  - name: check_isolation_caps
    purpose: Verify CP5 — citizens with distinct_actors=0 score below 45 total on all capabilities
    status: pending
    priority: high
    method: Run synthetic profile with distinct_actors=0 through all formulas, assert thresholds

  - name: check_zero_collective_moments
    purpose: Verify CP6 — citizens with collective_w=0 have behavior_score < 10 on T5 capabilities
    status: pending
    priority: high
    method: Run synthetic profile with collective_w=0, assert behavior thresholds

  - name: check_creation_requirement
    purpose: Verify CP7 — col_movement_builder and col_global_movement score low without pioneered spaces
    status: pending
    priority: high
    method: Run synthetic profile with pioneered_w=0, assert T7/T8 behavior thresholds

  - name: check_dialogue_sensitivity
    purpose: Verify CP8 — dialogue_ratio=0 vs dialogue_ratio=0.4 creates 15+ point difference (CP8)
    status: pending
    priority: med
    method: Compare two profiles differing only in dialogue_ratio on col_dao_participation

  - name: check_temporal_decay
    purpose: Verify CP9 — old moments score 25+ points less than recent moments (CP9)
    status: pending
    priority: med
    method: Compare two profiles differing only in moment ages (all 30+ days old vs. all < 7 days)

  - name: check_tier_ceiling_progression
    purpose: Verify CP4 — same inputs score higher on T5 than T7/T8 formulas
    status: pending
    priority: med
    method: Run Profile 5 (average) through all 4 formulas, verify T5 scores > T7 > T8
```

---

## KNOWN GAPS

- All checkers pending — no runtime yet
- Formula audit tool (verify formulas only use primitives) not yet designed
- No real citizen data to validate against — all validation uses synthetic profiles
- Dialogue detection depends on moment_has_parent correctly identifying cross-actor responses — this needs integration testing with actual universe graph data
- Space type taxonomy ("governance", "discussion", "forum") not yet confirmed in universe graph schema

---

## MARKERS

<!-- @mind:todo Build check_content_isolation first — most critical invariant -->
<!-- @mind:todo Build check_isolation_caps — logical contradiction if violated -->
<!-- @mind:todo Confirm space_type values exist in universe graph schema before implementing behavior stats -->
<!-- @mind:proposition Run all checkers as part of CI pipeline once scoring formulas are implemented -->
<!-- @mind:proposition Add a "collective participation trend" health check: is the sub-index improving or declining over 14 days? -->
