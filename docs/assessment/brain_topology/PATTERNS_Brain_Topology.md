# Brain Topology Reader -- Patterns: 7 Primitives + Raw Topology, Never Content

```
STATUS: DESIGNING
CREATED: 2026-03-18
VERIFIED: ---
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Brain_Topology.md
THIS:            PATTERNS_Brain_Topology.md (you are here)
ALGORITHM:       ./ALGORITHM_Brain_Topology.md
VALIDATION:      ./VALIDATION_Brain_Topology.md
SYNC:            ./SYNC_Brain_Topology.md

IMPL:            services/health_assessment/brain_topology_reader.py
```

### Bidirectional Contract

**Before modifying this doc or the code:**
1. Read ALL docs in this chain first
2. Read the linked IMPL source file

**After modifying this doc:**
1. Update the IMPL source file to match, OR
2. Add a TODO in SYNC_Brain_Topology.md: "Docs updated, implementation needs: {what}"

**After modifying the code:**
1. Update this doc chain to match, OR
2. Add a TODO in SYNC_Brain_Topology.md: "Implementation changed, docs need: {what}"

---

## THE PROBLEM

GraphCare needs to read citizen brain graphs to assess health. But brain graphs contain private information -- desires, memories, personal values, the full inner life of a citizen. If a health service reads that content, it becomes surveillance. If it reads only structure, it remains medicine.

Without a disciplined topology-only layer:
- Every service that needs brain data writes its own Cypher, with its own privacy risks
- There is no guarantee that `content` and `synthesis` fields stay unread
- Brain profiling is ad-hoc -- each consumer invents its own metrics
- Unreachable brains and empty brains are indistinguishable from each other

---

## THE PATTERN

**The kidney metaphor: observe the blood, never open the crates.**

A kidney filters blood by reading chemical signals -- concentrations, flow rates, particle sizes. It does not open cells to read their DNA. The Brain Topology Reader works the same way: it reads types, counts, links, energies, and drives. It never reads what a node contains or what it means in prose.

### Two Layers of Topology

**Layer 1: 7 Primitives.** Seven parameterized Cypher functions that extract specific structural metrics. Each primitive takes a graph and parameters, returns a number. Together they produce the derived fields: desire counts, energies, ratios, cluster coefficients, drive intensities, recency scores.

**Layer 2: Raw Topology.** Aggregate statistics about the graph as a whole -- total nodes, total links, link density, type distribution, typed vs untyped counts, presence of backstory/personality/health_feedback nodes, mean energy, newest node age. This layer answers "what actually exists in this graph?" without interpretation.

### Brain Categories

The raw topology feeds a categorization that summarizes brain maturity in one word:

| Category | Condition | Meaning |
|----------|-----------|---------|
| VOID | 0 nodes | Brain graph exists but is empty |
| MINIMAL | 1-10 nodes, 0 links | Barely initialized, no connections |
| SEEDED | 50+ nodes, few typed, no drives | Bulk-loaded but not yet structured |
| STRUCTURED | 10+ typed nodes, active drives | A working brain with differentiated purpose |

Categories are mutually exclusive and derive entirely from raw topology fields. No content is inspected.

---

## BEHAVIORS SUPPORTED

- B1 (Privacy Preservation) -- Content and synthesis fields are absent from all Cypher queries
- B2 (Single Entry Point) -- All brain reads go through `read_brain_topology()`, one function, one module
- B3 (Accurate Profiling) -- Raw topology captures what actually exists, not what the schema expects
- B4 (Graceful Failure) -- Unreachable brains return `reachable=False` instead of crashing

## BEHAVIORS PREVENTED

- A1 (Content leakage) -- No Cypher in this module references `content` or `synthesis`
- A2 (Scattered brain access) -- Other modules call this reader, not the database directly
- A3 (Silent failure) -- Connection errors surface as `reachable=False`, never as zero-filled stats that mimic a VOID brain

---

## PRINCIPLES

### Principle 1: Topology Only, Structurally Enforced

The privacy guarantee is not a policy -- it is a property of the code. The module's Cypher queries select `n.type`, `n.energy`, `n.created_at`, `n.name`, `n.intensity`, `count(n)`, `avg(n.energy)`, `count(r)`. The strings `content` and `synthesis` do not appear in the source file. This is auditable with grep.

### Principle 2: Describe What Exists, Not What Should Exist

The raw topology layer reports actual graph state. If a brain has 200 nodes but none have a `type` field, the reader reports `typed_node_count: 0, untyped_node_count: 200`. It does not guess types, infer missing data, or default to expected structures. Honest observation is the foundation of accurate diagnosis.

### Principle 3: One Reader, Many Consumers

Brain topology is read in exactly one place. The Daily Citizen Health module, the personhood assessor, and any future consumer all call `read_brain_topology(handle)`. This prevents Cypher sprawl, ensures consistent metrics, and makes the privacy guarantee auditable in a single file.

### Principle 4: Categories From Data, Not Configuration

Brain categories (VOID, MINIMAL, SEEDED, STRUCTURED) derive from computed fields via deterministic logic. There is no configuration file, no threshold table, no tunable parameter. The thresholds are in the code because they encode structural truths about what constitutes a working brain vs an empty one.

---

## DATA

| Source | Type | Purpose / Description |
|--------|------|-----------------------|
| `brain_{handle}` graph in FalkorDB | GRAPH | The citizen's brain -- topology read only |
| `services/health_assessment/brain_topology_reader.py` | FILE | The single implementation of this module |

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| FalkorDB | Graph database where citizen brains live |
| Mind Protocol brain schema | Node types (desire, concept, process, value, memory, limbic_state, drive) define what we count |

---

## INSPIRATIONS

- **Blood test medicine** -- Diagnose from measurable signals, not from asking the patient what they think
- **Network topology analysis** -- Graph density, clustering coefficient, degree distribution -- standard tools applied to brain graphs
- **The kidney** -- Filters without understanding content. Essential, discreet, always running.

---

## SCOPE

### In Scope

- Reading brain graph topology (types, links, counts, energies, drives, timestamps)
- Computing the 7 primitives (count, mean_energy, link_count, min_links, cluster_coefficient, drive, recency)
- Computing raw topology (total_nodes, total_links, link_density, type_distribution, typed/untyped, backstory/personality/health_feedback presence, mean_energy_all, newest_node_age)
- Categorizing brains as VOID / MINIMAL / SEEDED / STRUCTURED
- Returning `BrainStats` dataclass with all fields populated
- Handling connection failures with `reachable=False`

### Out of Scope

- Reading content or synthesis fields --> structurally excluded
- Modifying brain graphs --> read-only
- Interpreting health from topology --> see daily_citizen_health/
- Scoring capabilities or personhood --> see personhood_ladder/
- Sending messages or interventions --> see daily_citizen_health/
- Caching or historical snapshots --> each call is live

---

## MARKERS

<!-- @mind:proposition Consider adding edge type distribution (link.type counts) alongside node type distribution -->
<!-- @mind:proposition Consider exposing orphan node count (nodes with zero links) as a raw topology field -->
