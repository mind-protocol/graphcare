# World Presence — Health: Verification Mechanics

```
STATUS: DRAFT
CREATED: 2026-03-13
```

---

## WHEN TO USE HEALTH (NOT TESTS)

| Use Health For | Why |
|----------------|-----|
| Scoring formulas don't access content | Privacy violation = trust collapse |
| Diversity is weighted over volume | Volume-only scoring destroys the signal |
| Inbound metrics exclude self-generated moments | Self-inflation = meaningless social gravity |
| Temporal decay is applied consistently | Stale presence is not presence |
| CLI-only citizens score near zero | Definitional integrity |

---

## PURPOSE OF THIS FILE

Verifies that the world presence scoring system operates correctly at runtime: formulas respect privacy, diversity signals are not gamed by volume, inbound metrics are honest, and temporal decay keeps scores current.

Boundaries: This verifies the PROCESS (world presence scoring runs correctly). It does NOT verify individual formula arithmetic (that is unit testing) or the Personhood Ladder spec (that is the personhood_ladder HEALTH file).

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_World_Presence.md
PATTERNS:        ./PATTERNS_World_Presence.md
ALGORITHM:       ./ALGORITHM_World_Presence.md
VALIDATION:      ./VALIDATION_World_Presence.md
THIS:            HEALTH_World_Presence.md (you are here)
SYNC:            ./SYNC_World_Presence.md

PARENT CHAIN:    ../daily_citizen_health/
```

---

## IMPLEMENTS

```yaml
implements:
  runtime: @mind:TODO services/health_assessment/world_presence_checks.py
  decorator: @check
```

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: content_isolation
    priority: high
    rationale: If content is accessed in world presence scoring, trust is destroyed.
  - name: diversity_primacy
    priority: high
    rationale: If volume replaces diversity, the world presence signal collapses.
  - name: inbound_honesty
    priority: high
    rationale: If citizens can self-inflate inbound metrics, social gravity is fictional.
  - name: temporal_consistency
    priority: med
    rationale: Stale scores misrepresent current presence.
  - name: cli_zero_floor
    priority: med
    rationale: CLI-only citizens scoring on world presence is a definitional failure.
```

---

## CHECKER INDEX

```yaml
checkers:
  - name: check_content_isolation
    purpose: Verify no world presence formula accesses content or synthesis fields (V1, V5)
    status: pending
    priority: high

  - name: check_diversity_over_volume
    purpose: >
      Verify that a synthetic citizen with 100 moments in 1 non-CLI space type
      scores lower on wp_beyond_cli than one with 10 moments across 4 space types (V2)
    status: pending
    priority: high

  - name: check_inbound_excludes_self
    purpose: >
      Verify that inbound_count, attendee_count, returning_visitors, and reference_w
      all exclude the citizen's own moments (V3)
    status: pending
    priority: high

  - name: check_temporal_decay_applied
    purpose: >
      Verify that all moment-based metrics use temporal_weight.
      A moment from 30 days ago should contribute near-zero weight (V4)
    status: pending
    priority: med

  - name: check_cli_only_near_zero
    purpose: >
      Verify that a citizen with 100% repo/CLI moments scores <= 40
      on all world presence capabilities (V6)
    status: pending
    priority: med

  - name: check_landmark_requires_inbound
    purpose: >
      Verify that wp_landmark behavior_score is 0 when inbound_count=0
      and returning_visitors=0 (V7)
    status: pending
    priority: med

  - name: check_adventure_exclusion
    purpose: Verify no adventure universe spaces or citizens are assessed (V8)
    status: pending
    priority: med
```

---

## KNOWN GAPS

- All checkers pending — no runtime yet
- Formula audit tool (verify formulas only use primitives) not yet designed
- Space-type taxonomy not yet finalized — checkers need to know which types are "non-CLI"
- Inbound analysis performance at scale not yet benchmarked
- Returning visitor detection (distinct days) may need calendar-day boundaries defined

<!-- @mind:todo Build check_inbound_excludes_self first — most critical for social gravity integrity -->
<!-- @mind:todo Define space-type taxonomy as an enum so checkers can validate against it -->
<!-- @mind:todo Benchmark reference_moments scan performance for wp_landmark -->

---

## MARKERS

<!-- @mind:todo All checkers pending implementation -->
<!-- @mind:proposition Run diversity_over_volume check as part of formula regression suite -->
