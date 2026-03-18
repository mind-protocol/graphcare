# Personhood Ladder — Health: Verification Mechanics and Coverage

```
STATUS: DRAFT
CREATED: 2026-03-13
```

---

## WHEN TO USE HEALTH (NOT TESTS)

Health checks verify runtime behavior that tests cannot catch:

| Use Health For | Why |
|----------------|-----|
| Spec integrity over time | Capabilities may be added/removed; must stay consistent |
| Assessment accuracy drift | Agent behavior changes; assessments must track reality |
| Profile consistency | Tier integrity must hold across all assessments |
| Longitudinal tracking | Growth patterns emerge over weeks/months, not test fixtures |

**Tests gate completion. Health monitors runtime.**

---

## PURPOSE OF THIS FILE

This HEALTH file covers the Personhood Ladder assessment module — verifying that the spec is structurally valid, that assessments produce correct profiles, and that profiles maintain integrity over time.

It exists because the spec is a living document (capabilities evolve) and assessments run against changing behavioral data. Structural drift and assessment inconsistency are the primary risks.

Boundaries: This file verifies the ladder itself and its assessments. It does NOT verify individual agent behavior or brain health substrate — those are separate health domains.

---

## WHY THIS PATTERN

HEALTH is separate from tests because spec integrity and assessment accuracy are runtime concerns. A test can verify that the algorithm computes tiers correctly from fixture data. Only health checks can verify that the live spec is structurally sound and that live assessments satisfy invariants.

Docking-based checks are the right tradeoff because they verify at boundaries (spec load, profile output) without requiring changes to assessment logic.

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Personhood_Ladder.md
PATTERNS:        ./PATTERNS_Personhood_Ladder.md
BEHAVIORS:       ./BEHAVIORS_Personhood_Ladder.md
ALGORITHM:       ./ALGORITHM_Personhood_Ladder.md
VALIDATION:      ./VALIDATION_Personhood_Ladder.md
IMPLEMENTATION:  ./IMPLEMENTATION_Personhood_Ladder.md
THIS:            HEALTH_Personhood_Ladder.md (you are here)
SYNC:            ./SYNC_Personhood_Ladder.md
```

---

## IMPLEMENTS

This HEALTH file is a **spec**. The actual code lives in runtime:

```yaml
implements:
  runtime: @mind:TODO runtime/checks/personhood_ladder_checks.py
  decorator: @check
```

> **Separation:** HEALTH.md defines WHAT to check and WHEN to trigger. Runtime code defines HOW to check.

---

## HEALTH INDICATORS SELECTED

## OBJECTIVES COVERAGE

| Objective | Indicators | Why These Signals Matter |
|-----------|------------|--------------------------|
| Measurable AI growth | spec_structural_integrity, tier_integrity | If spec is broken or tiers inflate, measurements are meaningless |
| Unified assessment framework | spec_structural_integrity | All agents assessed against the same spec |
| Actionable next steps | recommendation_quality | If recommendations don't prioritize foundation, growth guidance fails |

```yaml
health_indicators:
  - name: spec_structural_integrity
    flow_id: agent_assessment
    priority: high
    rationale: Spec is source of truth. If structurally invalid (missing aspects, orphaned capabilities), all assessments fail.
  - name: tier_integrity
    flow_id: agent_assessment
    priority: high
    rationale: Tier inflation destroys trust. Every profile must satisfy V1 (no higher-tier without lower-tier mastery).
  - name: recommendation_quality
    flow_id: agent_assessment
    priority: med
    rationale: Recommendations must surface lowest-tier gaps first (V6). Wrong prioritization wastes development effort.
```

---

## CHECKER INDEX

```yaml
checkers:
  - name: check_spec_structure
    purpose: Verify personhood_ladder.json is structurally valid (V2, V4)
    status: pending
    priority: high
  - name: check_tier_integrity
    purpose: Verify all produced profiles satisfy tier integrity (V1)
    status: pending
    priority: high
  - name: check_aspect_independence
    purpose: Verify no profile computes an overall tier (V3)
    status: pending
    priority: med
  - name: check_recommendation_order
    purpose: Verify recommendations prioritize lowest-tier gaps (V6)
    status: pending
    priority: med
```

---

## INDICATOR: spec_structural_integrity

### VALUE TO CLIENTS & VALIDATION MAPPING

```yaml
value_and_validation:
  indicator: spec_structural_integrity
  client_value: All assessments depend on a valid spec. Structural errors invalidate every profile.
  validation:
    - validation_id: V2
      criteria: All capability IDs, tier assignments, and aspect memberships in tooling match JSON exactly
    - validation_id: V4
      criteria: Every capability has non-empty how_to_verify
```

### ALGORITHM / CHECK MECHANISM

```python
@check(
    id="spec_structural_integrity",
    triggers=[
        triggers.file.on_change("docs/specs/personhood_ladder.json"),
    ],
    on_problem="SPEC_INVALID",
    task="fix_personhood_ladder_spec",
)
def check_spec_structure(ctx) -> dict:
    """Verify personhood_ladder.json structural integrity."""
    spec = load_json("docs/specs/personhood_ladder.json")

    # Check all capabilities reference valid aspects and tiers
    for cap in spec["capabilities"]:
        assert cap["aspect"] in spec["aspects"]
        assert cap["tier"] in spec["tiers"]
        assert cap["how_to_verify"].strip() != ""
        assert cap["failure_mode"].strip() != ""

    # Check no duplicate capability IDs
    ids = [c["id"] for c in spec["capabilities"]]
    assert len(ids) == len(set(ids))

    return Signal.healthy()
```

### SIGNALS

```yaml
signals:
  healthy: Spec loads, all references valid, no duplicates, all capabilities have verification criteria
  degraded: Minor issues (e.g., empty description but how_to_verify present)
  critical: Structural errors (orphaned capabilities, duplicate IDs, missing how_to_verify)
```

---

## INDICATOR: tier_integrity

### VALUE TO CLIENTS & VALIDATION MAPPING

```yaml
value_and_validation:
  indicator: tier_integrity
  client_value: Profiles must be trustworthy. Tier inflation means assessments are lies.
  validation:
    - validation_id: V1
      criteria: Aspect tier equals highest tier where ALL capabilities at that tier and below are demonstrated
```

### ALGORITHM / CHECK MECHANISM

```python
@check(
    id="tier_integrity",
    triggers=[
        triggers.event.on("assessment.profile.created"),
    ],
    on_problem="TIER_INFLATION",
    task="fix_tier_assessment",
)
def check_tier_integrity(ctx) -> dict:
    """Verify a produced profile satisfies tier integrity."""
    profile = ctx.payload

    for aspect, claimed_tier in profile["aspect_tiers"].items():
        # Get all capabilities at claimed tier and below for this aspect
        for tier_level in range(1, tier_to_int(claimed_tier) + 1):
            caps = get_capabilities(aspect, int_to_tier(tier_level))
            for cap in caps:
                assessment = profile["capabilities"][cap["id"]]
                if assessment["status"] != "demonstrated":
                    return Signal.critical(
                        details=f"Tier inflation: {aspect} claimed {claimed_tier} "
                                f"but {cap['id']} at T{tier_level} is {assessment['status']}"
                    )

    return Signal.healthy()
```

---

## KNOWN GAPS

- All checkers are `pending` — no runtime implementation yet
- Longitudinal tracking health (profile consistency over time) not yet defined
- Evidence quality assessment not covered — how good is the evidence behind each capability status?

<!-- @mind:todo Implement check_spec_structure as first checker (can run now, spec exists) -->
<!-- @mind:todo Define evidence quality health indicator when behavioral log interface is defined -->

---

## MARKERS

<!-- @mind:todo Build runtime checks once assessment engine exists -->
<!-- @mind:proposition Run spec_structural_integrity immediately — JSON exists, checker can be built now -->
