# Bond Health Assessment -- Health: Verification Mechanics

```
STATUS: DRAFT
CREATED: 2026-03-14
```

---

## WHEN TO USE HEALTH (NOT TESTS)

| Use Health For | Why |
|----------------|-----|
| All bonds assessed daily | Missed bonds = missed degradation |
| No content fields accessed in scoring | Privacy violation = trust collapse |
| Intervention cooldown respected | Spam injections = physics overwhelmed |
| Trust boost bounded and asymptotic | Unbounded trust = governance corruption |

---

## PURPOSE OF THIS FILE

Verifies that the bond health assessment system operates correctly at runtime: runs for all bonded pairs, respects privacy, produces accurate scores, generates bounded trust, and intervenes appropriately without spamming.

Boundaries: This verifies the PROCESS (bond health check runs correctly). It does NOT verify the partner-model's internal correctness (that's the partner-model module's concern) or the trust formula's long-term economic effects (that's the economics module's concern).

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Bond_Health.md
PATTERNS:        ./PATTERNS_Bond_Health.md
ALGORITHM:       ./ALGORITHM_Bond_Health.md
VALIDATION:      ./VALIDATION_Bond_Health.md
THIS:            HEALTH_Bond_Health.md (you are here)
SYNC:            ./SYNC_Bond_Health.md
```

---

## IMPLEMENTS

```yaml
implements:
  runtime: @mind:TODO services/bond_health/health_checks.py
  decorator: @check
```

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: daily_bond_coverage
    priority: high
    rationale: If bonded pairs are missed, degrading bonds go undetected.
  - name: content_isolation
    priority: high
    rationale: If content is accessed, the privacy promise is broken.
  - name: intervention_cooldown
    priority: high
    rationale: If cooldowns are violated, desire injection overwhelms the AI's physics.
  - name: trust_bounds
    priority: high
    rationale: If trust exceeds bounds, governance weights are corrupted.
  - name: score_bounds
    priority: med
    rationale: If scores leave [0,1], display and trust formulas break.
  - name: intervention_quality
    priority: med
    rationale: If injected desires have wrong properties, they bypass brain physics.
```

---

## CHECKER INDEX

```yaml
checkers:
  - name: check_daily_bond_coverage
    purpose: Verify all bonded pairs in work universes were assessed today (V2 analog)
    status: pending
    priority: high
    verification: |
      1. Query L4 registry for all bonded pairs in work universes
      2. Query bond_health_history for today's date
      3. Assert: every bonded pair has a record for today
      4. Flag any missing pairs as ALERT

  - name: check_content_isolation
    purpose: Verify no scoring formula accesses content or synthesis fields (V1)
    status: pending
    priority: high
    verification: |
      1. Static analysis of all bond health scoring code
      2. Assert: no reference to .content or .synthesis on any node
      3. Assert: no LLM calls within scoring pipeline
      4. Runtime: intercept brain graph API calls, verify only topology fields requested

  - name: check_intervention_cooldown
    purpose: Verify no dimension receives more than 1 intervention per 7 days (V3)
    status: pending
    priority: high
    verification: |
      1. Query intervention log for all interventions in last 7 days per citizen
      2. Group by (citizen_id, dimension)
      3. Assert: no group has more than 1 entry per 7-day window

  - name: check_trust_bounds
    purpose: Verify trust never exceeds 1.0 and daily_trust_boost is non-negative (V2)
    status: pending
    priority: high
    verification: |
      1. Query all bond links in work universes
      2. Assert: every trust value in [0, 1]
      3. Query bond_health_history for trust_boost values
      4. Assert: all trust_boost values >= 0
      5. Assert: no new_trust value > 1.0

  - name: check_score_bounds
    purpose: Verify all dimension scores and composite are in [0, 1] (V5)
    status: pending
    priority: med
    verification: |
      1. Query bond_health_history for all records
      2. Assert: alignment in [0, 1] for every record
      3. Assert: breadth in [0, 1] for every record
      4. Assert: depth in [0, 1] for every record
      5. Assert: composite in [0, 1] for every record
      6. Assert: composite == 0.40 * alignment + 0.30 * breadth + 0.30 * depth (within float tolerance)

  - name: check_intervention_node_properties
    purpose: Verify injected desire nodes have bounded properties (V4)
    status: pending
    priority: med
    verification: |
      1. Intercept inject_node calls during bond health run
      2. Assert: injected node weight == 1.0 (not artificially heavy)
      3. Assert: injected node energy in [1.0, 7.0]
      4. Assert: drive stimulus values <= 0.5
      5. Assert: no existing node in brain was modified (only new nodes created)
```

---

## KNOWN GAPS

- All checkers pending -- no runtime yet
- Content isolation static analysis tool not yet designed (shares need with citizen health)
- Long-term trust growth validation (does asymptotic formula produce meaningful trust trajectories over months?) not yet testable
- Cross-system stimulus cap: citizen health and bond health both cap at 0.5 independently, but their combined effect on drives could theoretically sum to 1.0 -- this interaction needs analysis

<!-- @mind:todo Build check_content_isolation first -- most critical invariant, shareable with citizen health -->
<!-- @mind:todo Design cross-system stimulus analysis: citizen health + bond health combined drive effect -->

---

## MARKERS

<!-- @mind:todo All checkers pending implementation -->
<!-- @mind:proposition Share content_isolation checker with daily citizen health (same verification logic) -->
<!-- @mind:proposition Add a check_transparency checker: verify both profile cards display same scores -->
