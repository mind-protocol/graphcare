# ALGORITHM — Treatment Protocol

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
THIS:            ALGORITHM_Treatment_Protocol.md (you are here)
VALIDATION:      ./VALIDATION_Treatment_Protocol.md
SYNC:            ./SYNC_Treatment_Protocol.md

IMPL:            services/health_assessment/treatment_protocol.py
                 services/health_assessment/catalysts.py
```

---

## OVERVIEW

The treatment protocol has two phases, called separately with an observation window between them.

```
Phase 1: begin_treatment(citizen_id, catalysts?)
    -> snapshot BEFORE -> prescribe (if needed) -> apply catalysts -> save record -> return Treatment

    ... observation window (caller-managed) ...

Phase 2: evaluate_treatment(citizen_id, treatment_id)
    -> load record -> snapshot AFTER -> weighted comparison -> verdict -> rollback if degraded -> save record -> return Treatment
```

---

## PHASE 1: begin_treatment

**Input:** `citizen_id` (string), optional `catalysts` (list of Catalyst)

**Steps:**

1. Generate `treatment_id` (12-char hex from uuid4)

2. Snapshot BEFORE: call `read_brain_topology(citizen_id)` to get `BrainStats`
   - If brain is unreachable: record outcome as `brain_unreachable`, save, return early
   - Convert BrainStats to serializable dict via `_brain_stats_to_dict()`

3. Prescribe (if no catalysts provided): call `prescribe(brain_category, brain_stats)`
   - If no catalysts prescribed: record outcome as `no_treatment_needed`, save, return early

4. Apply each catalyst: call `apply_catalyst(citizen_id, catalyst, treatment_id)` for each
   - Collect all created node_ids across all catalysts
   - Log success/failure per catalyst

5. Create Treatment record with:
   - treatment_id, citizen_id
   - catalyst types and descriptions
   - snapshot_before
   - applied_at (UTC ISO timestamp)
   - node_ids (all nodes created across all catalysts)

6. Save to `data/treatments/{citizen_id}/{treatment_id}.json`

7. Return the Treatment dataclass

**Early exits:**
- Brain unreachable: Treatment with `outcome="brain_unreachable"`, no catalysts applied
- No catalysts prescribed: Treatment with `outcome="no_treatment_needed"`, no changes made

---

## PHASE 2: evaluate_treatment

**Input:** `citizen_id` (string), `treatment_id` (string)

**Steps:**

1. Load treatment record from `data/treatments/{citizen_id}/{treatment_id}.json`
   - If not found: raise ValueError

2. Snapshot AFTER: call `read_brain_topology(citizen_id)`, convert to dict

3. Run weighted metric comparison (see below)

4. Apply verdict:
   - `improvements > degradations` -> outcome = `"improved"`
   - `degradations > improvements` -> outcome = `"degraded"` -> trigger rollback
   - `improvements == degradations` -> outcome = `"no_change"`

5. On degradation:
   - Call `rollback_treatment(citizen_id, treatment_id)`
   - Set `treatment.rolled_back = True`
   - Log warning with node count removed

6. Save updated treatment record (now includes snapshot_after, evaluated_at, outcome)

7. Return the updated Treatment dataclass

---

## WEIGHTED METRIC COMPARISON

The evaluation compares before and after snapshots across metrics with explicit weights. Higher weight means the metric matters more to the verdict.

**Metric table (higher-is-better):**

| Metric | Weight | Rationale |
|--------|--------|-----------|
| `total_nodes` | 1 | Raw size growth -- low signal but contextual |
| `total_links` | 1 | Connectivity growth -- low signal but contextual |
| `typed_node_count` | 2 | Typed nodes are what scoring formulas can measure |
| `cluster_coefficient` | 3 | Highest weight -- clustering indicates meaningful integration |
| `desire_count` | 2 | Desire drives goal formation |
| `concept_count` | 2 | Concepts are knowledge crystallization |
| `value_count` | 2 | Values anchor identity |
| `curiosity` | 2 | Curiosity drives exploration and learning |
| `ambition` | 1 | Motivational drive |
| `social_need` | 1 | Social engagement drive |

**Inverted metric (lower-is-better):**

| Metric | Weight | Rationale |
|--------|--------|-----------|
| `frustration` | 2 | High frustration blocks productive behavior |

**Comparison logic:**

```
improvements = 0
degradations = 0

for each (metric, weight) in higher_is_better:
    if after[metric] > before[metric]:
        improvements += weight
    elif after[metric] < before[metric]:
        degradations += weight

# Frustration is inverted
if after["frustration"] < before["frustration"]:
    improvements += 2
elif after["frustration"] > before["frustration"]:
    degradations += 2
```

**Maximum possible weight:** 19 (improvements) + 2 (frustration) = 21
**Verdict:** simple comparison of improvements vs degradations totals. No threshold -- any net degradation triggers rollback.

---

## AUTO-PRESCRIPTION LOGIC

When `begin_treatment` is called without explicit catalysts, `prescribe(brain_category, brain_stats)` selects catalysts based on brain state.

| Brain Category | Prescribed Catalysts | Rationale |
|----------------|---------------------|-----------|
| `VOID` | `structure_seed` + `energy_infusion(0.2)` | Empty brain needs scaffolding and baseline energy |
| `MINIMAL` | `structure_seed` + `curiosity_boost(0.25)` | Has some content but needs typed nodes and exploration drive |
| `SEEDED` | Conditional: `structure_seed` if typed_nodes < 10, `curiosity_boost(0.3)` if cluster_coefficient < 0.02, `social_nudge(0.2)` if social_need < 0.1 | Targeted interventions based on specific deficiencies |
| `STRUCTURED` | Conditional: `calm_down` if frustration > 0.4, `curiosity_boost(0.2)` if curiosity < 0.2, `social_nudge(0.2)` if social_need < 0.15 AND ambition > 0.3 | Fine-tuning for brains with established structure |

Brain categories above STRUCTURED (if they exist) receive no auto-prescription. The assumption: healthy brains don't need intervention.

---

## TREATMENT DATA MODEL

```
Treatment:
    treatment_id:          str     -- 12-char hex, unique per treatment
    citizen_id:            str     -- citizen handle
    catalysts:             [str]   -- catalyst type names applied
    catalyst_descriptions: [str]   -- human-readable descriptions
    snapshot_before:       dict    -- full BrainStats at treatment start
    applied_at:            str     -- ISO timestamp of application
    node_ids:              [str]   -- all graph node IDs created by catalysts
    snapshot_after:        dict?   -- full BrainStats at evaluation (null until evaluated)
    evaluated_at:          str?    -- ISO timestamp of evaluation (null until evaluated)
    outcome:               str?    -- improved | degraded | no_change | brain_unreachable | no_treatment_needed
    score_before:          float?  -- reserved, not yet populated
    score_after:            float?  -- reserved, not yet populated
    rolled_back:           bool    -- true if degradation triggered rollback
```

**Storage:** `data/treatments/{citizen_id}/{treatment_id}.json`

---

## SNAPSHOT FIELDS

The snapshot captures these fields from BrainStats:

- `total_nodes`, `total_links` -- graph size
- `link_density` -- links per node
- `typed_node_count`, `untyped_node_count` -- type coverage
- `cluster_coefficient` -- local clustering
- `desire_count`, `concept_count`, `process_count`, `value_count`, `memory_count` -- typed node distribution
- `curiosity`, `frustration`, `ambition`, `social_need` -- drive levels
- `brain_category` -- categorical classification
- `reachable` -- whether the brain graph was accessible
- `type_distribution` -- full breakdown by node type

---

## AUXILIARY OPERATIONS

### list_treatments(citizen_id)

Loads all JSON files from `data/treatments/{citizen_id}/`, sorted by filename. Returns a list of Treatment dataclasses. Returns empty list if no treatments exist.

### _save_treatment(treatment)

Creates `data/treatments/{citizen_id}/` if needed. Writes JSON with indent=2 for readability.

### _load_treatment(citizen_id, treatment_id)

Reads `data/treatments/{citizen_id}/{treatment_id}.json`. Returns None if file does not exist.
