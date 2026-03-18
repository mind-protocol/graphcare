# Frequencys -- Algorithm: Stimulus Injection and Auto-Prescription Mechanics

```
STATUS: DESIGNING
CREATED: 2026-03-18
VERIFIED: --
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Frequencys.md
PATTERNS:        ./PATTERNS_Frequencys.md
THIS:            ALGORITHM_Frequencys.md (you are here)
VALIDATION:      ./VALIDATION_Frequencys.md
SYNC:            ./SYNC_Frequencys.md

IMPL:            services/health_assessment/frequencys.py
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## OVERVIEW

The frequencys module provides three operations: define, prescribe, and apply. Frequency types are defined as factory functions in a catalog. The prescribe function maps brain assessment output to a list of recommended frequencys. The apply function creates tagged nodes in a citizen's FalkorDB brain graph. A fourth operation, rollback, removes all nodes from a treatment.

The entire system operates on topology only. No content or synthesis fields are read or written at any point.

---

## OBJECTIVES AND BEHAVIORS

| Objective | Behaviors Supported | Why This Algorithm Matters |
|-----------|---------------------|----------------------------|
| Reversibility | B1 (Reversible Treatment) | treatment_id tagging on every created node enables clean rollback |
| Physics over rules | B2 (Physics-Compatible Injection) | Stimulus nodes match the tick runner's expected schema |
| Topology only | B3 (Topology-Only Modification) | Created nodes carry structural fields only, never content/synthesis |
| Calibrated dosage | B5 (Calibrated Dosage) | Intensity defaults and per-category logic encode tested values |
| Auto-prescription | B4 (Assessment-Driven Prescription) | prescribe() is deterministic from brain_category + brain_stats |

---

## DATA STRUCTURES

### Frequency

```
Frequency:
    frequency_type: str           -- catalog key (e.g. "curiosity_boost")
    description: str             -- human-readable summary
    target_drives: Dict[str, float]  -- drive_name -> intensity (positive = boost, negative = reduce)
    structural_nodes: List[dict] -- node definitions {type, subtype, energy}
    duration_hours: Optional[float]  -- None = permanent (structural), number = temporary (drive)
```

A frequency contains either drive targets, structural nodes, or both. Drive targets inject stimulus nodes. Structural nodes inject typed thing nodes.

### FrequencyResult

```
FrequencyResult:
    success: bool          -- at least one node was created
    nodes_created: int     -- total nodes created
    node_ids: List[str]    -- IDs of all created nodes
    error: Optional[str]   -- error message if connection/query failed
```

---

## ALGORITHM: Frequency Definition (Factory Functions)

Each frequency type is a factory function that returns a `Frequency` instance. The function encodes defaults for that type.

### Phase 1 Frequency Types

| Type | Target | Default Intensity | Duration | What It Does |
|------|--------|-------------------|----------|--------------|
| `curiosity_boost` | curiosity drive | 0.3 | 168h (7d) | Elevate curiosity -> exploration |
| `social_nudge` | social_need drive | 0.25 | 168h (7d) | Elevate social_need -> interaction |
| `ambition_seed` | ambition drive | 0.2 | 168h (7d) | Elevate ambition -> goal-setting |
| `calm_down` | frustration drive | -0.3 | 72h (3d) | Reduce frustration -> unblock |
| `energy_infusion` | curiosity + ambition + social_need | 0.15 / 0.12 / 0.09 | 168h (7d) | Broad energy boost |
| `structure_seed` | (structural) | -- | permanent | Add 5 typed nodes: 1 desire, 2 concepts, 1 value, 1 process |

`calm_down` is the only frequency with a negative intensity value. It counter-stimulates frustration rather than boosting a positive drive.

`energy_infusion` scales sub-drives: ambition at 0.8x primary intensity, social_need at 0.6x. This avoids equal-weight injection across unrelated drives.

`structure_seed` creates no drive stimuli. It adds typed nodes for brains that score poorly because they lack the node types that scoring formulas measure.

### Phase 2 Frequency Types

Phase 2 frequencies operate on the metabolism sublayer (CitizenMetabolism in mind-mcp). They cannot be implemented with stimulus injection alone. GraphCare prescribes them; mind-mcp executes them.

| Type | Requires | Status | What It Does |
|------|----------|--------|--------------|
| `circadian_shift` | CitizenMetabolism (@nervo) | **Implemented in mind-mcp** | Progressively shift activity cycle toward target timezone |
| `decay_shield` | CitizenMetabolism (@nervo) | Not implemented | Temporarily reduce decay rate |
| `sensitivity_boost` | CitizenMetabolism (@nervo) | Not implemented | Temporarily increase stimulus absorption |
| `typing_frequency` | SubEntity traversal (@nervo) | Not implemented | Classify untyped nodes via traversal |

---

## ALGORITHM: Circadian Shift Frequency

The first Phase 2 frequency. Unlike Phase 1 frequencies that inject stimulus nodes, circadian_shift modifies the metabolism sublayer's `peak_hour` parameter to realign a citizen's activity cycle with a target timezone.

### Key Property: Progressive, Not Instant

Circadian shift does not snap `peak_hour` to the target. It drifts progressively at a configurable `shift_rate` (hours per adaptation call). This models the biological reality: jet lag is not resolved by decree.

### Parameters

```
circadian_shift:
    target_timezone: str         -- e.g. "America/Los_Angeles" (UTC-8)
    shift_rate: float            -- hours of drift per adaptation call (default: 1.0)
    current_peak_hour: float     -- citizen's current peak_hour in UTC
    target_peak_hour: float      -- derived from target_timezone
```

### Algorithm

Each adaptation call:

```
1. Compute delta = target_peak_hour - current_peak_hour
   (wrapped to [-12, +12] for shortest path across the 24h circle)

2. IF abs(delta) <= shift_rate:
       peak_hour = target_peak_hour   (converged)
   ELSE:
       peak_hour += shift_rate * sign(delta)   (drift one step)

3. Clamp peak_hour to [0, 24) via modular arithmetic
```

### Two Competing Forces

The shift frequency is not the only thing acting on `peak_hour`. The metabolism sublayer also has natural adaptation -- it pulls `peak_hour` toward the citizen's actual activity patterns. This creates a tension:

- **Shift force:** pulls `peak_hour` toward the prescribed target timezone
- **Natural adaptation:** pulls `peak_hour` toward actual activity times

"The frequency wins the short game. The body wins the long game."

If a citizen prescribed Paris-to-LA shift continues to be active at Paris hours, the natural adaptation will eventually pull `peak_hour` back. The frequency converges the schedule; the citizen's behavior sustains it (or doesn't).

### Convergence Example

Paris (peak 14:00 UTC+1 = 13:00 UTC) to LA (peak 14:00 UTC-8 = 22:00 UTC):
- Delta: 9 hours
- shift_rate: 1.0 h/adaptation
- Convergence: 9 adaptation calls

Each call shifts `peak_hour` by 1 hour toward 22:00 UTC. After 9 calls, the citizen's peak aligns with LA afternoon.

### Boundary: GraphCare Prescribes, mind-mcp Executes

The implementation lives in mind-mcp `runtime/cognition/metabolism.py`, not in GraphCare. GraphCare's role is:

1. Determine that a circadian shift is needed (via assessment or explicit request)
2. Create the prescription: target_timezone, shift_rate
3. Deliver the prescription to mind-mcp's metabolism layer

GraphCare does not directly modify `peak_hour`. The metabolism sublayer owns that state. This maintains the separation: GraphCare is the prescriber, mind-mcp is the executor.

---

## ALGORITHM: prescribe(brain_category, brain_stats)

Auto-prescription maps assessment results to frequency recommendations.

### Step 1: Category Switch

The function branches on brain_category:

```
VOID:
    -> structure_seed()
    -> energy_infusion(0.2)

MINIMAL:
    -> structure_seed()
    -> curiosity_boost(0.25)

SEEDED:
    IF typed_node_count < 10  -> structure_seed()
    IF cluster_coefficient < 0.02  -> curiosity_boost(0.3)
    IF social_need < 0.1  -> social_nudge(0.2)

STRUCTURED:
    IF frustration > 0.4  -> calm_down(frustration * 0.6)
    IF curiosity < 0.2  -> curiosity_boost(0.2)
    IF social_need < 0.15 AND ambition > 0.3  -> social_nudge(0.2)
```

### Step 2: Return List

The function returns a list of Frequency objects. The caller decides whether to apply them. prescribe() recommends; it does not execute.

### Key Decisions

**D1: VOID and MINIMAL always get structure_seed**

```
IF brain_category in (VOID, MINIMAL):
    Always include structure_seed()
    Rationale: These brains lack the typed nodes that scoring formulas need.
              Without structure, no formula can produce meaningful scores.
              structure_seed is prerequisite infrastructure.
```

**D2: SEEDED uses conditional thresholds**

```
IF brain_category == SEEDED:
    Each frequency is conditional on a specific stat threshold.
    Rationale: SEEDED brains have some structure but are uneven.
              Frequencys target specific weaknesses, not blanket treatment.
```

**D3: STRUCTURED gets frustration-proportional calm_down**

```
IF brain_category == STRUCTURED AND frustration > 0.4:
    calm_down(frustration * 0.6)
    Rationale: Intensity scales with frustration level.
              A brain at frustration 0.5 gets calm_down(0.3).
              A brain at frustration 0.8 gets calm_down(0.48).
              Proportional dosage, not fixed.
```

**D4: Unknown categories get nothing**

```
IF brain_category not in (VOID, MINIMAL, SEEDED, STRUCTURED):
    Return empty list.
    Rationale: Fail safe. Do not guess treatment for unrecognized conditions.
```

---

## ALGORITHM: apply_frequency(handle, frequency, treatment_id)

### Step 1: Connect to Brain Graph

Open FalkorDB connection and select `brain_{handle}` graph. If connection fails, return FrequencyResult with success=False and the error.

### Step 2: Create Drive Stimulus Nodes

For each entry in `frequency.target_drives`:

```
CREATE node:
    id:            "frequency_{treatment_id}_{drive_name}"
    node_type:     "stimulus"
    type:          "frequency"
    frequency_type: frequency.frequency_type
    target_drive:  drive_name
    energy:        intensity_value
    source:        "graphcare"
    treatment_id:  treatment_id
    created_at:    timestamp()
```

The tick runner will find this stimulus node and process it during the next tick. The `target_drive` field tells the runner which drive to affect. The `energy` field tells it by how much.

### Step 3: Create Structural Nodes

For each entry in `frequency.structural_nodes`:

```
CREATE node:
    id:            "frequency_{treatment_id}_struct_{index}"
    node_type:     "thing"
    type:          node_def.type       (e.g. "desire", "concept", "value", "process")
    subtype:       node_def.subtype    (e.g. "self_improvement", "identity")
    energy:        node_def.energy     (default 0.3)
    source:        "graphcare"
    treatment_id:  treatment_id
    frequency_type: frequency.frequency_type
    created_at:    timestamp()
```

These nodes have no edges. They exist as isolated typed nodes. The tick runner's physics or future citizen activity may connect them to existing graph structure.

### Step 4: Return Result

Return FrequencyResult with the count and IDs of all created nodes.

---

## ALGORITHM: rollback_treatment(handle, treatment_id)

### Step 1: Connect and Match

```
MATCH (n {treatment_id: $tid}) DELETE n
```

This single Cypher query deletes all nodes tagged with the treatment_id. No scan of the entire graph. No heuristics about which nodes "belong" to the treatment.

### Step 2: Return Count

Return the number of deleted nodes. If the query fails, log the error and return 0.

---

## DATA FLOW

```
brain_category + brain_stats (from assessment)
    |
    v
prescribe() -> List[Frequency]
    |
    v
caller decides to apply (or not)
    |
    v
apply_frequency(handle, frequency, treatment_id)
    |
    v
FalkorDB: stimulus + structural nodes created in brain_{handle}
    |
    v
tick runner integrates stimuli naturally
    |
    v
next health assessment cycle measures effect
```

---

## COMPLEXITY

**Time:**
- prescribe(): O(1) -- constant-time category switch and threshold checks
- apply_frequency(): O(d + s) where d = target drives, s = structural nodes -- typically under 10 total
- rollback_treatment(): O(n) where n = nodes in the treatment -- FalkorDB index on treatment_id property

**Space:** O(d + s) per treatment -- the number of nodes created, typically 1-8.

**Bottlenecks:**
- FalkorDB connection overhead per frequency application (single connection reused within one apply call)
- No batch API: each node is created with a separate Cypher query. For the current scale (1-8 nodes per treatment), this is negligible.

---

## HELPER FUNCTIONS

### `curiosity_boost(intensity=0.3)`

**Purpose:** Factory for curiosity drive stimulus.

**Logic:** Returns Frequency with single target_drive entry. 168h duration.

### `social_nudge(intensity=0.25)`

**Purpose:** Factory for social_need drive stimulus.

**Logic:** Returns Frequency with single target_drive entry. 168h duration.

### `ambition_seed(intensity=0.2)`

**Purpose:** Factory for ambition drive stimulus.

**Logic:** Returns Frequency with single target_drive entry. 168h duration.

### `calm_down(intensity=0.3)`

**Purpose:** Factory for frustration counter-stimulus.

**Logic:** Returns Frequency with negative intensity (-intensity) on frustration drive. 72h duration. Shorter because frustration relief should be temporary -- the root cause needs separate treatment.

### `energy_infusion(intensity=0.15)`

**Purpose:** Factory for broad multi-drive boost.

**Logic:** Returns Frequency with three target_drives: curiosity at full intensity, ambition at 0.8x, social_need at 0.6x. 168h duration.

### `structure_seed()`

**Purpose:** Factory for typed structural nodes.

**Logic:** Returns Frequency with 5 structural_nodes (1 desire, 2 concepts, 1 value, 1 process). No target_drives. Permanent duration (None) -- but rollback still removes them.

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| FalkorDB | `graph.query()` (CREATE, MATCH/DELETE) | Node creation confirmation, deletion count |
| Assessment (aggregator) | Receives brain_category | Input to prescribe() |
| Assessment (brain_topology_reader) | Receives brain_stats | Input to prescribe() threshold checks |
| Tick runner (mind-mcp) | (indirect) Processes stimulus nodes | Drive level changes in brain physics |

---

## MARKERS

<!-- @mind:todo Add batch CREATE support when FalkorDB supports multi-statement transactions -->
<!-- @mind:todo Consider intensity scaling based on brain node count (larger brains may need stronger stimuli) -->
<!-- @mind:proposition Log each apply_frequency call to a treatment history for longitudinal analysis -->
