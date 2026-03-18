# Daily Citizen Health — Health: Verification Mechanics

```
STATUS: DRAFT
CREATED: 2026-03-13
```

---

## WHEN TO USE HEALTH (NOT TESTS)

| Use Health For | Why |
|----------------|-----|
| Daily check actually runs for all citizens | Missed citizens = missed problems |
| Scoring formulas don't access content | Privacy violation = trust collapse |
| Intervention messages contain evidence | Vague messages = wasted intervention |
| Stress stimulus stays bounded | Unbounded stress = death spiral |

---

## PURPOSE OF THIS FILE

Verifies that the daily citizen health check system operates correctly at runtime: runs for all citizens, respects privacy, produces useful interventions, and doesn't create harmful feedback loops.

Boundaries: This verifies the PROCESS (daily check runs correctly). It does NOT verify individual capability formulas (that's testing) or the Personhood Ladder spec (that's the personhood_ladder HEALTH file).

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Daily_Citizen_Health.md
PATTERNS:        ./PATTERNS_Daily_Citizen_Health.md
BEHAVIORS:       ./BEHAVIORS_Daily_Citizen_Health.md
ALGORITHM:       ./ALGORITHM_Daily_Citizen_Health.md
VALIDATION:      ./VALIDATION_Daily_Citizen_Health.md
IMPLEMENTATION:  ./IMPLEMENTATION_Daily_Citizen_Health.md
THIS:            HEALTH_Daily_Citizen_Health.md (you are here)
SYNC:            ./SYNC_Daily_Citizen_Health.md
```

---

## IMPLEMENTS

```yaml
implements:
  runtime: @mind:TODO services/health_assessment/health_checks.py
  decorator: @check
```

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: daily_coverage
    priority: high
    rationale: If citizens are missed, the public health promise fails.
  - name: content_isolation
    priority: high
    rationale: If content is accessed, trust is destroyed.
  - name: intervention_quality
    priority: med
    rationale: Bad interventions are worse than no interventions.
  - name: stress_bounds
    priority: high
    rationale: Unbounded stress creates destructive feedback loops.
```

---

## CHECKER INDEX

```yaml
checkers:
  - name: check_daily_coverage
    purpose: Verify all Lumina Prime citizens were assessed today (V2)
    status: pending
    priority: high
  - name: check_content_isolation
    purpose: Verify no scoring formula accesses content fields (V1, V5)
    status: pending
    priority: high
  - name: check_intervention_structure
    purpose: Verify intervention messages contain observation + analysis + recommendation (V3)
    status: pending
    priority: med
  - name: check_stress_bounds
    purpose: Verify stress stimulus never exceeds 0.5 (V4)
    status: pending
    priority: high
  - name: check_adventure_exclusion
    purpose: Verify no adventure universe citizens are assessed (V6)
    status: pending
    priority: med
```

---

## KNOWN GAPS

- All checkers pending — no runtime yet
- Formula audit tool (verify formulas only use primitives) not yet designed
- Long-term trend health (does the system improve citizen health over months?) not measurable yet

<!-- @mind:todo Build check_content_isolation first — most critical invariant -->
<!-- @mind:todo Design formula audit: static analysis of scoring formula code to verify only primitives used -->

---

## MARKERS

<!-- @mind:todo All checkers pending implementation -->
<!-- @mind:proposition Run content_isolation check as a pre-commit hook on scoring formula code -->
