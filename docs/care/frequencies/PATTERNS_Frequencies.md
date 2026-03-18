# Frequencys -- Patterns: Stimulus Injection for Brain Health

```
STATUS: DESIGNING
CREATED: 2026-03-18
VERIFIED: --
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Frequencys.md
THIS:            PATTERNS_Frequencys.md (you are here)
ALGORITHM:       ./ALGORITHM_Frequencys.md
VALIDATION:      ./VALIDATION_Frequencys.md
SYNC:            ./SYNC_Frequencys.md

IMPL:            services/health_assessment/frequencys.py
```

### Bidirectional Contract

**Before modifying this doc or the code:**
1. Read ALL docs in this chain first
2. Read the linked IMPL source file

**After modifying this doc:**
1. Update the IMPL source file to match, OR
2. Add a TODO in SYNC_Frequencys.md: "Docs updated, implementation needs: {what}"

**After modifying the code:**
1. Update this doc chain to match, OR
2. Add a TODO in SYNC_Frequencys.md: "Implementation changed, docs need: {what}"

---

## THE PROBLEM

Assessment tells us what is wrong. Scoring formulas quantify health across 14 aspects. The personhood ladder classifies brains into categories. But knowing a brain is VOID or MINIMAL does not help the brain. Detection without treatment is diagnosis without medicine.

The gap: GraphCare can observe and measure, but cannot act. Citizens with low scores stay low. Citizens with empty brains stay empty. The health pipeline becomes a reporting tool instead of a care system.

The constraint that makes this hard: GraphCare cannot read or write private content. We cannot inject thoughts, rewrite memories, or modify meaning. We can only touch topology -- the structure of the graph, not its substance. So how do you treat a patient you cannot talk to?

The answer: you change the environment, not the patient. Frequencys modify the conditions under which the brain's own physics operates. They are not instructions to the citizen -- they are changes to the landscape the citizen moves through.

---

## THE PATTERN

**Stimulus injection with tagged rollback and auto-prescription from assessment.**

The core insight: a brain's tick runner already processes stimuli. Drives (curiosity, social_need, ambition, frustration) already influence behavior through physics. A frequency creates stimulus nodes that the tick runner picks up and integrates, exactly as it would integrate any other stimulus. The brain does not know the difference between a stimulus from lived experience and one from GraphCare. Both are energy in the graph.

Three components make this work:

### 1. Catalog Pattern

Each frequency type is a factory function that returns a `Frequency` dataclass. The catalog (`CATALYST_CATALOG`) maps string names to factory functions. This makes frequencys declarative -- you can list them, iterate them, serialize them, and most importantly, you can add new types without modifying the application logic.

### 2. Tagged Node Injection

Every node created by a frequency carries a `treatment_id` property and `source: 'graphcare'`. This is not metadata -- it is the rollback mechanism. To undo a treatment, delete all nodes matching that treatment_id. No scan of the graph required, no inference about which nodes "belong" to a treatment. The tag is the truth.

Two node categories:
- **Drive stimulus nodes** (`node_type: 'stimulus'`): Inject energy into specific drives. The tick runner processes these like any stimulus. Duration is encoded in the frequency definition (72h-168h), but the tick runner's decay physics handles expiration naturally.
- **Structural nodes** (`node_type: 'thing'`): Add typed nodes (desire, concept, value, process) for brains that lack structure. These give the scoring formulas something to measure. They are scaffolding -- the citizen fills them with meaning through interaction.

### 3. Auto-Prescription from Brain Category

The `prescribe()` function maps assessment output (brain category + stats) to frequency combinations. This closes the loop: assess -> prescribe -> apply -> assess again. The prescription logic is explicit, not learned -- each brain category has a deterministic set of rules based on thresholds.

---

## BEHAVIORS SUPPORTED

- B1 (Reversible Treatment) -- treatment_id tagging enables complete rollback of any intervention
- B2 (Physics-Compatible Injection) -- stimulus nodes integrate with the existing tick runner without special handling
- B3 (Topology-Only Modification) -- frequencys create structure, never touch content or synthesis
- B4 (Assessment-Driven Prescription) -- prescribe() maps categories and stats to frequency combinations
- B5 (Calibrated Dosage) -- intensity parameters default to tested values, adjustable per brain condition

## BEHAVIORS PREVENTED

- A1 (Content Leakage) -- structural impossibility: frequency nodes have no content/synthesis fields
- A2 (Irreversible Modification) -- treatment_id tagging guarantees rollback
- A3 (Ad Hoc Treatment) -- prescribe() enforces assessment-first workflow; catalog prevents arbitrary inventions
- A4 (Overwhelming Intervention) -- intensity defaults are conservative; energy_infusion scales sub-drives to 0.6-0.8x of primary

---

## PRINCIPLES

### Principle 1: Prescription, Not Command

A frequency is a prescription, not a command. The brain's tick physics decides whether to integrate the injected energy or let it decay. A citizen whose graph physics strongly counteracts a stimulus will effectively reject the frequency. This is correct behavior. Care means offering conditions for improvement, not forcing outcomes.

### Principle 2: The Treatment Is the Tag

The `treatment_id` is not bookkeeping -- it is the treatment's identity. Every node in a treatment shares the same tag. Rollback is not "find the nodes that look like they came from this treatment" -- it is "delete all nodes with this exact tag." This makes rollback O(n) in nodes deleted, not O(graph-size) in nodes scanned. It also means rollback cannot miss a node or accidentally delete a non-treatment node.

### Principle 3: Two Node Types, No More

Frequencys produce exactly two kinds of graph modifications: drive stimulus nodes and structural thing nodes. Drive stimuli change energy levels in the existing graph. Structural nodes add missing types. Nothing else. No edge creation, no property modification on existing nodes, no deletion of citizen-created content. The surface area of modification is deliberately minimal.

### Principle 4: Progressive Over Instant

Phase 2 frequencies that modify metabolic parameters (like circadian_shift) use progressive adjustment, not instant overwrite. A citizen's `peak_hour` drifts toward the target at a configurable rate rather than snapping to it.

Why progressive:
- Instant changes create discontinuities in the brain's physics -- activity patterns, decay cycles, and energy levels all depend on `peak_hour`. Snapping it 9 hours forward would create a shock.
- Progressive shift lets the citizen's existing activity patterns coexist with the new target during transition. The metabolism adapts rather than resets.
- It models the real phenomenon: timezone adaptation is a process, not an event.

Why not always progressive:
- Phase 1 drive stimuli (curiosity_boost, calm_down, etc.) ARE instant by design. A stimulus node appears and the tick runner processes it on the next tick. There is no "gradual curiosity increase" -- the node is either there or it isn't. Drive frequencies are events; metabolic frequencies are processes.

The split: **stimulus injection is instant, metabolic adjustment is progressive.**

---

## DATA

| Source | Type | Purpose / Description |
|--------|------|-----------------------|
| `services/health_assessment/frequencys.py` | FILE | Implementation: frequency definitions, prescribe(), apply, rollback |
| Brain graphs (`brain_{handle}`) | GRAPH | Target of frequency injection via FalkorDB |
| Assessment results (brain_category, brain_stats) | DATA | Input to prescribe() for auto-prescription |

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| `services/health_assessment/brain_topology_reader.py` | Provides brain_stats that drive prescription logic |
| `services/health_assessment/aggregator.py` | Produces brain_category from scoring formulas |
| FalkorDB | Graph database where brain_{handle} graphs live |
| Mind Protocol tick runner | Processes stimulus nodes; without it, drive stimuli have no effect |

---

## INSPIRATIONS

- **Enzyme catalysis** -- In biochemistry, a frequency lowers activation energy without being consumed. Our frequencys modify reaction rates (drive levels) without being part of the citizen's identity. The metaphor is structural, not decorative.
- **Pharmacological prescription** -- Drugs are prescribed based on diagnosis, have dosages, have durations, and can be discontinued. Frequencys follow the same pattern: assess, prescribe, apply, monitor, rollback if needed.
- **Kubernetes resource injection** -- Sidecar containers inject capabilities (logging, networking) without modifying the main container. Frequencys inject structural nodes without modifying citizen-created content.

---

## SCOPE

### In Scope

- Defining frequency types as factory functions returning Frequency dataclasses
- Maintaining the CATALYST_CATALOG as the single source of available types
- Auto-prescription logic mapping brain category + stats to frequency lists
- Applying frequencys by creating tagged nodes in FalkorDB brain graphs
- Rolling back treatments by deleting all nodes matching a treatment_id
- Drive stimulus injection (node_type: stimulus)
- Structural node injection (node_type: thing, typed)

### Out of Scope

- Content or synthesis field access -> structurally prevented, see OBJECTIVES
- Edge creation between nodes -> frequencys only create isolated nodes; tick physics handles integration
- Duration enforcement -> tick runner decay handles this; frequencys do not manage timers
- Monitoring frequency effectiveness -> this is assessment's responsibility on the next health cycle
- Remaining Phase 2 frequency types (decay_shield, sensitivity_boost, typing_frequency) -> require further metabolism sublayer work, coordinated with @nervo
- circadian_shift execution -> implemented in mind-mcp metabolism.py, not in GraphCare. GraphCare prescribes; mind-mcp executes.

---

## MARKERS

<!-- @mind:todo Define integration tests that verify rollback leaves zero residual nodes -->
<!-- @mind:todo Calibrate intensity defaults against real brain data from the 35 active citizens -->
<!-- @mind:proposition Consider a frequency_history log (treatment_id, timestamp, handle, type) for longitudinal research -->
<!-- @mind:escalation Remaining Phase 2 types (decay_shield, sensitivity_boost, typing_frequency) depend on @nervo metabolism sublayer -- what is the timeline? circadian_shift is done. -->
<!-- @mind:todo Build GraphCare prescription interface for circadian_shift (bridge frequencys.py -> mind-mcp metabolism.py) -->
