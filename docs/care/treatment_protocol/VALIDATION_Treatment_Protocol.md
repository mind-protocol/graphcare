# VALIDATION — Treatment Protocol

```
STATUS: CANONICAL
CREATED: 2026-03-18
VERIFIED: code reviewed against services/health_assessment/treatment_protocol.py
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Treatment_Protocol.md
PATTERNS:        ./PATTERNS_Treatment_Protocol.md
ALGORITHM:       ./ALGORITHM_Treatment_Protocol.md
THIS:            VALIDATION_Treatment_Protocol.md (you are here)
VALIDATION:      (you are here)
SYNC:            ./SYNC_Treatment_Protocol.md

IMPL:            services/health_assessment/treatment_protocol.py
                 services/health_assessment/catalysts.py
```

---

## INVARIANTS

These must hold at all times. A violation of any invariant is a bug.

### INV-1: Snapshot always precedes application

**Statement:** No catalyst is applied to a brain graph without `snapshot_before` being captured first.

**Why it matters:** Without a baseline, evaluation is impossible. An unmeasured treatment cannot be verified as helpful or harmful.

**How to verify:** In `begin_treatment`, `read_brain_topology()` is called before any `apply_catalyst()` call. There is no code path that reaches catalyst application without passing through the snapshot step first.

**Violation signal:** A treatment record exists with `catalysts` populated but `snapshot_before` empty or containing only `{"reachable": false}` while `outcome` is not `brain_unreachable`.

---

### INV-2: All treatment nodes are tagged

**Statement:** Every node created by the treatment protocol carries a `treatment_id` property matching the treatment's ID.

**Why it matters:** Rollback depends on this tag. A node without `treatment_id` cannot be found by `rollback_treatment()` and will persist in the brain even after rollback.

**How to verify:** In `apply_catalyst()`, every CREATE query includes `treatment_id: $tid` in the node properties. Verify by querying: `MATCH (n {treatment_id: $tid, source: 'graphcare'}) RETURN count(n)` -- count must equal `len(treatment.node_ids)`.

**Violation signal:** After rollback, brain graph still contains nodes with `source: 'graphcare'` matching the treatment_id.

---

### INV-3: Degradation triggers rollback

**Statement:** When `evaluate_treatment` produces outcome `"degraded"`, `rollback_treatment()` is called and `treatment.rolled_back` is set to `true`.

**Why it matters:** A degrading treatment that persists makes the citizen worse. The auto-rollback guarantee is the safety mechanism that makes intervention acceptable.

**How to verify:** In `evaluate_treatment`, the `degradations > improvements` branch unconditionally calls `rollback_treatment()` and sets `rolled_back = True`. There is no conditional or configuration that can skip rollback on degradation.

**Violation signal:** A treatment record has `outcome: "degraded"` and `rolled_back: false`.

---

### INV-4: Treatment record always persisted

**Statement:** Every call to `begin_treatment` and `evaluate_treatment` saves a treatment record to disk before returning.

**Why it matters:** Treatment records are the audit trail. A treatment that ran but was not recorded is invisible to analysis and accountability.

**How to verify:** Both `begin_treatment` and `evaluate_treatment` call `_save_treatment()` on every code path, including early exits (brain_unreachable, no_treatment_needed).

**Violation signal:** A treatment was applied (nodes exist in brain graph with `source: 'graphcare'`) but no corresponding JSON file exists in `data/treatments/`.

---

### INV-5: Evaluation requires prior treatment

**Statement:** `evaluate_treatment` can only be called with a valid treatment_id that corresponds to an existing treatment record.

**Why it matters:** Evaluating a nonexistent treatment is meaningless and would produce corrupt data.

**How to verify:** `evaluate_treatment` loads the treatment via `_load_treatment()` and raises `ValueError` if not found.

**Violation signal:** N/A -- the function raises before producing any side effects.

---

### INV-6: Topology-only constraint

**Statement:** No function in the treatment protocol reads or writes `content` or `synthesis` fields on any node.

**Why it matters:** This is GraphCare's foundational privacy guarantee. Treatment works by manipulating structure (drives, typed nodes, energy) but never touches meaning.

**How to verify:** Audit all Cypher queries in `catalysts.py` -- CREATE statements set `node_type`, `type`, `subtype`, `energy`, `source`, `treatment_id`, `catalyst_type`, and `created_at`. No query references `content` or `synthesis`.

**Violation signal:** Any Cypher query containing the strings `content` or `synthesis` in a SET or RETURN clause.

---

## TEST SCENARIOS

### Scenario 1: Successful treatment lifecycle

1. Call `begin_treatment("test_citizen")`
2. Verify treatment record saved with `snapshot_before` populated and `outcome` is None
3. Verify nodes exist in brain graph with matching `treatment_id`
4. Call `evaluate_treatment("test_citizen", treatment_id)`
5. Verify `snapshot_after` populated, `outcome` is one of: improved, degraded, no_change
6. If degraded: verify `rolled_back` is true, verify tagged nodes removed from graph

### Scenario 2: Unreachable brain

1. Call `begin_treatment` with a citizen_id whose brain graph does not exist
2. Verify outcome is `brain_unreachable`
3. Verify no nodes were created in any graph
4. Verify treatment record saved

### Scenario 3: No prescription needed

1. Call `begin_treatment` with a citizen whose brain category produces no catalysts
2. Verify outcome is `no_treatment_needed`
3. Verify no nodes were created
4. Verify treatment record saved with empty catalysts list

### Scenario 4: Rollback completeness

1. Apply treatment with known node_ids
2. Force a degradation scenario (or mock the after-snapshot to be worse)
3. Call `evaluate_treatment`
4. Query brain graph: `MATCH (n {treatment_id: $tid}) RETURN count(n)` must return 0
5. Verify treatment record has `rolled_back: true`

### Scenario 5: Multiple treatments on same citizen

1. Apply treatment A, then treatment B (different treatment_ids)
2. Evaluate treatment A as degraded -- rollback removes only A's nodes
3. Verify treatment B's nodes remain intact (different treatment_id)
4. Both treatment records exist independently in `data/treatments/{citizen_id}/`

---

## EDGE CASES

| Case | Expected Behavior |
|------|-------------------|
| Brain unreachable at begin_treatment | Record saved with outcome `brain_unreachable`, no catalysts applied |
| Brain unreachable at evaluate_treatment | Snapshot AFTER still captured (with `reachable: false`), evaluation proceeds on available data |
| All catalyst applications fail | Treatment record saved with empty `node_ids`, outcome remains None until evaluation |
| Treatment evaluated twice | Second evaluation overwrites snapshot_after, evaluated_at, and outcome in the record |
| Rollback fails (FalkorDB error) | `rollback_treatment` returns 0, treatment record has `rolled_back: true` but nodes may persist -- logged as error |
| Treatment record manually deleted | `evaluate_treatment` raises ValueError -- no silent failure |
