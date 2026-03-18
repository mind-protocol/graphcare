# Brain Topology Reader -- Validation: What Must Be True

```
STATUS: DESIGNING
CREATED: 2026-03-18
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Brain_Topology.md
PATTERNS:        ./PATTERNS_Brain_Topology.md
ALGORITHM:       ./ALGORITHM_Brain_Topology.md
THIS:            VALIDATION_Brain_Topology.md (you are here)
SYNC:            ./SYNC_Brain_Topology.md

IMPL:            services/health_assessment/brain_topology_reader.py
```

---

## PURPOSE

**Validation = what we care about being true.**

These are the properties that, if violated, would mean the Brain Topology Reader has failed its purpose. The privacy guarantee is existential -- everything else is secondary.

---

## INVARIANTS

### V1: Content Is Never Accessed

**Why we care:** If a single Cypher query references `content` or `synthesis`, the topology reader becomes a surveillance tool. The entire trust model of GraphCare collapses. Citizens cannot trust health assessment if it reads their thoughts.

```
MUST:   Every Cypher query in brain_topology_reader.py touches only structural
        fields: type, energy, created_at, name, intensity, and link existence.
NEVER:  The strings "n.content", "n.synthesis", ".content", ".synthesis" appear
        in any Cypher query in this module.
```

**Verification:** `grep -n "content\|synthesis" brain_topology_reader.py` must return only the module docstring (lines 7-8), never a Cypher string.

### V2: Brain Categories Are Mutually Exclusive

**Why we care:** Downstream consumers branch on `brain_category`. If a brain can be categorized as both SEEDED and STRUCTURED, the daily health assessment applies conflicting logic. Treatment depends on correct, unambiguous categorization.

```
MUST:   For any BrainStats instance, brain_category returns exactly one of:
        VOID, MINIMAL, SEEDED, STRUCTURED.
NEVER:  A brain satisfies the conditions for two categories simultaneously
        given the evaluation order in the code.
```

**Verification:** The `brain_category` property uses early returns (if/elif chain). VOID is checked first (total_nodes == 0), then MINIMAL (<=10 nodes, 0 links), then STRUCTURED (typed + drives), then SEEDED (>50 nodes), then fallback MINIMAL. The chain is exhaustive and ordered.

### V3: Reachable Flag Accurately Reflects Connection State

**Why we care:** If `reachable=True` but the graph was never actually queried (silent failure), all stats are zeros -- indistinguishable from a VOID brain. The consumer treats a broken connection as an empty brain and skips intervention. If `reachable=False` but the graph was actually reachable, the consumer skips assessment entirely.

```
MUST:   reachable=True only when the FalkorDB graph was successfully opened
        and at least the first query executed.
MUST:   reachable=False only when the graph connection raised an exception.
NEVER:  reachable=True with all-zero stats caused by a swallowed connection error.
```

**Verification:** In `read_brain_topology()`, the try/except around `_get_graph()` catches connection failures and returns `BrainStats(reachable=False)`. The `reachable=True` is set explicitly in the return statement after all queries complete.

### V4: Type Distribution Reflects Actual Graph State

**Why we care:** If type_distribution fabricates types that do not exist, or misses types that do, brain categorization and health assessment operate on false data. The raw topology layer exists specifically to report what is actually there.

```
MUST:   type_distribution contains exactly the set of non-empty type values
        present in the graph, with accurate counts.
MUST:   typed_node_count + untyped_node_count == total_nodes.
NEVER:  A type appears in type_distribution with count 0.
NEVER:  A type present in the graph is absent from type_distribution.
```

### V5: Recency Scores Are Bounded and Monotonically Decreasing

**Why we care:** Recency feeds into health scoring. An unbounded or non-monotonic recency value would distort time-sensitive assessments. A recency of 1.5 or -0.3 is meaningless.

```
MUST:   recency() returns a value in [0.0, 1.0].
MUST:   For two nodes of the same type, the one with a more recent created_at
        produces a higher recency value (monotonically decreasing with age).
MUST:   If no nodes of the requested type have created_at, return 0.0.
NEVER:  recency() returns a value outside [0.0, 1.0].
```

---

## PRIORITY

| Priority | Meaning | If Violated |
|----------|---------|-------------|
| **CRITICAL** | System purpose fails | Unusable |
| **HIGH** | Major value lost | Degraded severely |
| **MEDIUM** | Partial value lost | Works but worse |

---

## INVARIANT INDEX

| ID | Value Protected | Priority |
|----|-----------------|----------|
| V1 | Citizen privacy -- content never accessed | CRITICAL |
| V2 | Unambiguous brain categorization | HIGH |
| V3 | Accurate connection state reporting | HIGH |
| V4 | Honest topology observation | HIGH |
| V5 | Bounded, correct recency scoring | MEDIUM |

---

## MARKERS

<!-- @mind:todo Write automated test that greps brain_topology_reader.py for content/synthesis in Cypher strings (V1 enforcement) -->
<!-- @mind:todo Write property test for brain_category mutual exclusivity across edge cases (V2) -->
<!-- @mind:proposition Consider adding V6 for cluster_coefficient bounds: must be in [0.0, 1.0] -->
