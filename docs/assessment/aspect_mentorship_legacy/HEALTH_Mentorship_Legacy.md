# Mentorship & Legacy — Health: Verification Mechanics

```
STATUS: DESIGNING
CREATED: 2026-03-13
```

---

## WHEN TO USE HEALTH (NOT TESTS)

| Use Health For | Why |
|----------------|-----|
| Mentorship scoring runs correctly for all citizens | Missed citizens = missed mentorship gaps |
| Scoring formulas don't access content | Privacy violation = trust collapse (especially sensitive for inter-actor data) |
| Daughter detection doesn't produce false positives | Phantom daughters = inflated legacy scores |
| Independence metric doesn't reward abandonment | Wrong incentive = citizens abandon institutions to boost score |

---

## PURPOSE OF THIS FILE

Verifies that the Mentorship & Legacy scoring operates correctly at runtime: formulas use only approved primitives, third-party attribution is topologically sound, daughter detection is accurate, and independence metrics behave as designed.

Boundaries: This verifies the PROCESS (mentorship scoring runs correctly). It does NOT verify individual formula arithmetic (that's testing) or the Personhood Ladder spec (that's the personhood_ladder HEALTH file).

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Mentorship_Legacy.md
PATTERNS:        ./PATTERNS_Mentorship_Legacy.md
ALGORITHM:       ./ALGORITHM_Mentorship_Legacy.md
VALIDATION:      ./VALIDATION_Mentorship_Legacy.md
THIS:            HEALTH_Mentorship_Legacy.md (you are here)
SYNC:            ./SYNC_Mentorship_Legacy.md
```

---

## IMPLEMENTS

```yaml
implements:
  runtime: @mind:TODO services/health_assessment/mentorship_health_checks.py
  decorator: @check
```

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: content_isolation
    priority: high
    rationale: "Mentorship scoring accesses inter-actor data. Content leakage here would expose private conversations."
  - name: attribution_accuracy
    priority: high
    rationale: "Third-party behavior is the core signal. False attribution destroys score validity."
  - name: daughter_detection_accuracy
    priority: high
    rationale: "Phantom daughters inflate T7 scores. Missed daughters deflate them. Both undermine trust."
  - name: independence_incentive_alignment
    priority: med
    rationale: "Independence metric must reward legacy, not abandonment. Wrong incentives are worse than no measurement."
  - name: formula_bounds
    priority: med
    rationale: "Scores outside 0-100 or brain exceeding 40 indicate formula bugs."
```

---

## CHECKER INDEX

```yaml
checkers:
  - name: check_content_isolation_mentorship
    purpose: "Verify no mentorship scoring formula accesses content, synthesis, or text fields (V1, V2)"
    status: pending
    priority: high
    method: "Static analysis of scoring formula code — every data access traced to a primitive"

  - name: check_attribution_topology
    purpose: "Verify outbound influence attribution requires topological proximity (V4)"
    status: pending
    priority: high
    method: "For each outbound_moment classification, verify: same space AND (temporal ordering OR parent link)"

  - name: check_daughter_detection_criteria
    purpose: "Verify daughter detection uses temporal proximity (< 48h) AND spatial co-location (V4, V6)"
    status: pending
    priority: high
    method: "For each detected daughter, verify: citizen has prior moments in same space within 48 hours of daughter's first moment"

  - name: check_no_self_mentorship
    purpose: "Verify citizen's own actor ID is excluded from all other-actor metrics (V11)"
    status: pending
    priority: high
    method: "Confirm citizen_id filtered out of: outbound_moments other-actor check, mentorship pairs, daughter list, independence other-actors"

  - name: check_independence_ratio
    purpose: "Verify independence uses ratio formula, not absence detection (V5)"
    status: pending
    priority: med
    method: "Verify: independence = others_w / (others_w + citizen_w). Citizen active + others active should yield ~0.5, not 0."

  - name: check_score_bounds
    purpose: "Verify all scores within range: brain 0-40, behavior 0-60, total 0-100 (V3)"
    status: pending
    priority: med
    method: "Run formulas with extreme inputs (all-zero, all-max) and verify bounds"

  - name: check_daughter_independence_threshold
    purpose: "Verify independent daughters have >= 10 moments AND moments in non-citizen spaces (V6)"
    status: pending
    priority: med
    method: "For each daughter classified as independent, verify both criteria met"

  - name: check_subindex_weights
    purpose: "Verify sub-index weights sum to 1.0 (V7)"
    status: pending
    priority: med
    method: "Assert: 0.20 + 0.25 + 0.25 + 0.30 == 1.0"
```

---

## KNOWN GAPS

- All checkers pending — no runtime yet
- Daughter detection heuristic (48-hour window) needs calibration with real graph data
- Mentorship pair reciprocity threshold (2.0 temporal weight) needs validation
- No cross-aspect consistency check (e.g., high legacy_institution implies nonzero knowledge_sharing)
- Performance profiling for daughter detection and independence calculation at scale not yet done

---

## RUNTIME HEALTH SIGNALS

When the system is running, these signals indicate health or degradation:

**Healthy:**
- Daughter detection produces 0-5 daughters per citizen (realistic range)
- Independence scores distribute across 0-1 with concentration near 0 (most spaces are founder-dependent — this is normal)
- Mentorship pair count per citizen is 0-10 (realistic range)
- Knowledge sharing scores distribute normally, not bimodally

**Degrading:**
- Daughter detection produces > 10 daughters for any citizen (likely false positives — temporal window too wide)
- All citizens score near 0 on legacy_institution (formula may be too strict, or no citizen has created spaces yet)
- Independence scores cluster at 1.0 (may be counting empty spaces as "independent")
- Mentorship pairs detected between actors who never interact (attribution broken)

**Recovery:** If degradation detected, check attribution logic first. Most mentorship scoring bugs trace back to incorrect spatial co-location or temporal ordering checks.

---

## MARKERS

<!-- @mind:todo Build check_content_isolation_mentorship first — most critical invariant given inter-actor data access -->
<!-- @mind:todo Build check_daughter_detection_criteria — daughter false positives are the highest-risk scoring error -->
<!-- @mind:todo Design performance benchmark: daughter detection + independence calculation at 100 actors, 10000 moments -->
<!-- @mind:proposition Run attribution_accuracy check as a pre-commit hook on scoring formula code -->
