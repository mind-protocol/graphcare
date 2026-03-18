# Trust & Reputation — Health: Verification Mechanics

```
STATUS: DESIGNING
CREATED: 2026-03-13
```

---

## WHEN TO USE HEALTH (NOT TESTS)

| Use Health For | Why |
|----------------|-----|
| Regularity metric correctly distinguishes consistency from volume | Conflation would reward burst behavior over reliability |
| Scoring formulas don't access content | Privacy violation = trust collapse |
| Inbound signals correctly exclude self-generated moments | Self-inflation = scoring integrity collapse |
| Trust tier doesn't dominate behavioral evidence | Assigned trust would override earned trust |
| Response chain completion handles zero-request edge case | New/low-interaction citizens would be unfairly penalized |

---

## PURPOSE OF THIS FILE

Verifies that the trust & reputation scoring operates correctly at runtime: regularity measures consistency, inbound signals are genuine, content is never accessed, brain/behavior split is respected, and edge cases are handled gracefully.

Boundaries: This verifies the PROCESS (trust scoring runs correctly). It does NOT verify individual formula arithmetic (that's testing) or the Personhood Ladder spec (that's the personhood_ladder HEALTH file).

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Trust_Reputation.md
PATTERNS:        ./PATTERNS_Trust_Reputation.md
ALGORITHM:       ./ALGORITHM_Trust_Reputation.md
VALIDATION:      ./VALIDATION_Trust_Reputation.md
THIS:            HEALTH_Trust_Reputation.md (you are here)
SYNC:            ./SYNC_Trust_Reputation.md
```

---

## IMPLEMENTS

```yaml
implements:
  runtime: @mind:TODO services/health_assessment/trust_reputation_checks.py
  decorator: @check
```

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: content_isolation
    priority: high
    rationale: Trust scoring must never access content fields. Violation destroys the entire system's credibility.

  - name: regularity_correctness
    priority: high
    rationale: If regularity conflates with volume, burst citizens get inflated reliability scores, undermining the foundational trust signal.

  - name: inbound_integrity
    priority: high
    rationale: If inbound signals can be self-generated, community and global trust scores are gameable.

  - name: trust_tier_proportion
    priority: med
    rationale: If drive("trust") dominates the score, assigned trust overrides earned trust.

  - name: edge_case_handling
    priority: med
    rationale: New citizens and low-interaction citizens must not receive unfairly low scores due to missing data.

  - name: score_bounds
    priority: med
    rationale: All scores must stay within [0, 100] with brain <= 40 and behavior <= 60.
```

---

## CHECKER INDEX

```yaml
checkers:
  - name: check_content_isolation
    purpose: Verify no trust scoring formula accesses content or synthesis fields (V1, V2)
    method: Static analysis of formula code — ensure only primitive calls exist
    status: pending
    priority: high

  - name: check_regularity_consistency_over_volume
    purpose: Verify regularity(low_variance) > regularity(high_variance) for equal total moments (V3)
    method: |
      Construct two moment sets with equal count:
        Set A: 5 moments/day for 30 days (150 total, low variance)
        Set B: 50 moments on days 1,2,3 + 0 for remaining 27 days (150 total, high variance)
      Assert: regularity(Set A) > regularity(Set B)
    status: pending
    priority: high

  - name: check_inbound_excludes_self
    purpose: Verify inbound_moments never includes the citizen's own moments (V4)
    method: |
      For each citizen assessed:
        inbound = inbound_moments(citizen_id)
        Assert: all(m.actor != citizen_id for m in inbound)
    status: pending
    priority: high

  - name: check_trust_tier_not_dominant
    purpose: Verify drive("trust")=1.0 + zero behavior scores below 40 total (V11)
    method: |
      Construct synthetic profile:
        brain: drive("trust")=1.0, all other brain signals at moderate levels
        behavior: all behavioral signals = 0
      Assert: total < 40 for all 5 capabilities
    status: pending
    priority: med

  - name: check_response_completion_zero_requests
    purpose: Verify response_completion returns 1.0 when zero inbound triggers exist (V6)
    method: |
      Construct synthetic profile with zero inbound triggers
      Assert: response_completion == 1.0
    status: pending
    priority: med

  - name: check_score_bounds
    purpose: Verify all scores within [0, 100], brain <= 40, behavior <= 60 (V5)
    method: |
      For each of the 25 test profiles (5 per capability):
        Assert: 0 <= brain_score <= 40
        Assert: 0 <= behavior_score <= 60
        Assert: 0 <= total <= 100
    status: pending
    priority: med

  - name: check_monotonicity_regularity
    purpose: Verify increasing regularity never decreases the reliability score (V8)
    method: |
      For regularity values [0.0, 0.1, 0.2, ..., 1.0]:
        Compute trust_basic_reliability score (holding all else constant)
        Assert: score[i+1] >= score[i]
    status: pending
    priority: med

  - name: check_monotonicity_inbound
    purpose: Verify increasing inbound_unique never decreases community trust score (V8)
    method: |
      For inbound_unique values [0, 1, 2, ..., 15]:
        Compute trust_community score (holding all else constant)
        Assert: score[i+1] >= score[i]
    status: pending
    priority: med

  - name: check_subindex_weights
    purpose: Verify sub-index weights sum to 1.0 (V7)
    method: Assert sum(weights) == 1.0
    status: pending
    priority: med

  - name: check_new_citizen_baseline
    purpose: Verify new citizen with 7 days regular activity scores >= 30 on basic reliability (V12)
    method: |
      Construct synthetic profile:
        brain: minimal (new citizen defaults)
        behavior: 7 days of 1 moment/day, 100% response completion
      Assert: trust_basic_reliability >= 30
    status: pending
    priority: low
```

---

## KNOWN GAPS

- All checkers pending — no runtime yet
- Formula audit tool (verify formulas only use primitives) not yet designed
- No long-term trust trajectory health check (does the system improve trust over months?)
- Sensitive space type list is hardcoded — no health check for whether the list is complete
- No cross-capability consistency check (high community trust should imply above-average basic reliability)

---

## MARKERS

<!-- @mind:todo Build check_content_isolation first — most critical invariant -->
<!-- @mind:todo Build check_regularity_consistency_over_volume — foundational trust signal integrity -->
<!-- @mind:todo Build check_inbound_excludes_self — community/global trust integrity -->
<!-- @mind:proposition Run content_isolation check as a pre-commit hook on trust scoring formula code -->
<!-- @mind:proposition Add cross-capability consistency checker: trust_community > 60 implies trust_basic_reliability > 40 -->
