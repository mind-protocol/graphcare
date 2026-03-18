# Brain Topology Reader -- Algorithm: 7 Cypher Primitives + Raw Topology + Brain Categorization

```
STATUS: DESIGNING
CREATED: 2026-03-18
VERIFIED: ---
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Brain_Topology.md
PATTERNS:        ./PATTERNS_Brain_Topology.md
THIS:            ALGORITHM_Brain_Topology.md (you are here)
VALIDATION:      ./VALIDATION_Brain_Topology.md
SYNC:            ./SYNC_Brain_Topology.md

IMPL:            services/health_assessment/brain_topology_reader.py
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## OVERVIEW

The Brain Topology Reader connects to a citizen's FalkorDB brain graph, executes a set of Cypher queries that touch only structural fields (type, energy, created_at, name, intensity, link existence), and assembles the results into a `BrainStats` dataclass. The process has three phases: connect to graph, run primitives + raw topology queries, categorize the brain.

---

## DATA STRUCTURES

### BrainStats

```
@dataclass
BrainStats:
    # 7-primitive derived fields
    desire_count: int               # count("desire")
    desire_energy: float            # mean_energy("desire")
    desire_moment_ratio: float      # min_links("desire", 1) / desire_count
    desire_persistence: float       # min_links("desire", 3) / min_links("desire", 1)
    concept_count: int              # count("concept")
    process_count: int              # count("process")
    value_count: int                # count("value")
    memory_count: int               # count("memory")
    cluster_coefficient: float      # cluster_coefficient("all")
    curiosity: float                # drive("curiosity")
    frustration: float              # drive("frustration")
    ambition: float                 # drive("ambition")
    social_need: float              # drive("social_need")
    recency_desire: float           # recency("desire")
    recency_moment: float           # recency("moment")
    reachable: bool                 # False if graph connection failed

    # Raw topology fields
    total_nodes: int                # count("all")
    total_links: int                # MATCH ()-[r]->() RETURN count(r)
    link_density: float             # total_links / max(total_nodes, 1)
    type_distribution: dict         # {type_string: count} for all non-empty types
    typed_node_count: int           # nodes with non-empty type
    untyped_node_count: int         # nodes with type="" or no type
    has_backstory: bool             # "backstory" in type_distribution
    has_personality: bool           # "personality" in type_distribution
    has_health_feedback: bool       # "health_feedback" in type_distribution
    health_feedback_count: int      # type_distribution.get("health_feedback", 0)
    mean_energy_all: float          # mean_energy("all")
    newest_node_age_hours: float    # age of most recent node, -1 if unknown

    @property
    brain_category -> str           # VOID | MINIMAL | SEEDED | STRUCTURED
```

---

## ALGORITHM: read_brain_topology(handle)

### Step 1: Connect to Graph

Open a FalkorDB connection to `brain_{handle}`. If the connection fails, return `BrainStats(reachable=False)` immediately. No partial results, no retries.

```
graph = FalkorDB(host, port).select_graph(f"brain_{handle}")
IF connection fails:
    RETURN BrainStats(reachable=False)
```

### Step 2: Execute 7 Primitives

Run each primitive against the graph. Each primitive is a standalone function that executes one or two Cypher queries and returns a single number.

```
desire_ct        = count(graph, "desire")
desire_energy    = mean_energy(graph, "desire")
desire_w_links   = min_links(graph, "desire", 1)
desire_w_3links  = min_links(graph, "desire", 3)
concept_count    = count(graph, "concept")
process_count    = count(graph, "process")
value_count      = count(graph, "value")
memory_count     = count(graph, "memory")
cluster_coeff    = cluster_coefficient(graph, "all")
curiosity        = drive(graph, "curiosity")
frustration      = drive(graph, "frustration")
ambition         = drive(graph, "ambition")
social_need      = drive(graph, "social_need")
recency_desire   = recency(graph, "desire")
recency_moment   = recency(graph, "moment")
```

Derived ratios:
```
desire_moment_ratio  = desire_w_links / max(desire_ct, 1)
desire_persistence   = desire_w_3links / max(desire_w_links, 1)
```

### Step 3: Read Raw Topology

Execute aggregate queries for the full graph.

```
total_nodes     = count(graph, "all")
total_links     = MATCH ()-[r]->() RETURN count(r)
link_density    = total_links / max(total_nodes, 1)

type_rows       = MATCH (n) RETURN COALESCE(n.type, '') AS t, count(n) AS c ORDER BY c DESC
FOR each row:
    IF t is non-empty: add to type_distribution, increment typed_node_count
    ELSE: increment untyped_node_count

mean_energy_all     = mean_energy(graph, "all")
newest_node_age     = (now - max(n.created_at)) / 3600, or -1 if unknown

has_backstory       = "backstory" in type_distribution
has_personality     = "personality" in type_distribution
has_health_feedback = "health_feedback" in type_distribution
health_feedback_count = type_distribution.get("health_feedback", 0)
```

### Step 4: Assemble and Return

Combine all fields into a single `BrainStats` instance with `reachable=True`.

---

## KEY DECISIONS

### D1: Brain Category Assignment

```
IF total_nodes == 0:
    category = "VOID"
ELIF total_nodes <= 10 AND total_links == 0:
    category = "MINIMAL"
ELIF typed_node_count > 10 AND (curiosity + ambition + social_need) > 0:
    category = "STRUCTURED"
ELIF total_nodes > 50:
    category = "SEEDED"
ELSE:
    category = "MINIMAL"
```

Evaluation order matters. VOID is checked first (empty graph). STRUCTURED requires both typed nodes AND active drives -- a brain with structure but no drives is not yet structured in a meaningful sense. SEEDED captures large graphs that were bulk-loaded but lack type differentiation. Everything else falls to MINIMAL.

### D2: Drive Retrieval Strategy

```
IF limbic_state node exists:
    read drive as property on that node (e.g., limbic_state.curiosity)
ELSE:
    look for separate drive node: type="drive", name=drive_name, return intensity
```

Two code paths because brain schemas vary. Some citizens have a single limbic_state node with drive properties. Others have individual drive nodes. Both are valid. The reader handles both without requiring schema migration.

### D3: Recency Decay Function

```
age_hours = (now - newest_created_at) / 3600
half_life = 168 hours (7 days)
recency = 0.5 ^ (age_hours / half_life)
```

Returns 1.0 for nodes created just now, 0.5 after 7 days, 0.25 after 14 days. Clamped to [0.0, 1.0]. If no created_at timestamp exists, returns 0.0.

### D4: Cluster Coefficient Approximation

```
n_count = count of nodes of type
e_count = count of edges between nodes of that type
possible = n_count * (n_count - 1)
cluster_coefficient = min(1.0, e_count / possible)
```

This is the density of the type-subgraph, not the classical clustering coefficient (which measures triangle closure per node). The approximation is cheaper and sufficient for health assessment purposes.

---

## DATA FLOW

```
handle (string)
    |
    v
FalkorDB connection --> brain_{handle} graph
    |
    v
7 primitives (14+ Cypher queries) --> derived fields
    |
    v
Raw topology queries (4 Cypher queries) --> raw fields
    |
    v
BrainStats dataclass (all fields + brain_category property)
```

---

## COMPLEXITY

**Time:** O(P) where P is the number of Cypher queries (~18 per call). Each query is O(N) or O(E) where N = nodes, E = edges. Total is dominated by graph size.

**Space:** O(T) where T is the number of distinct types in the graph (for type_distribution dict). All other fields are scalar.

**Bottlenecks:**
- `cluster_coefficient` runs two queries (count nodes, count edges within type) -- on large brains with many edges this could be slow
- `_read_raw_topology` runs a full type aggregation -- one pass over all nodes
- Each call opens a new FalkorDB connection (no connection pooling)

---

## HELPER FUNCTIONS

### `_get_graph(handle)`

**Purpose:** Open FalkorDB connection and select the `brain_{handle}` graph.

**Logic:** Creates a new FalkorDB client, calls `select_graph`. Raises on connection failure (caught by caller).

### `_safe_query(graph, cypher, params)`

**Purpose:** Execute a Cypher query and return result rows, or empty list on error.

**Logic:** Wraps `graph.query()` in try/except. Logs warnings on failure. Never raises -- returns `[]` so callers can safely destructure.

### `_read_raw_topology(graph)`

**Purpose:** Compute all raw topology fields in a single coordinated pass.

**Logic:** Calls `count(graph, "all")` for total nodes, runs a direct link count query, aggregates type distribution from a full-scan query, computes mean energy and newest node age. Returns a dict that is unpacked into BrainStats via `**raw`.

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| FalkorDB | `FalkorDB(host, port).select_graph()` | Graph handle for Cypher execution |
| FalkorDB | `graph.query(cypher, params)` | Result set rows |

---

## MARKERS

<!-- @mind:proposition Consider connection pooling to avoid per-call FalkorDB connections -->
<!-- @mind:proposition Consider batching Cypher queries (UNION or multi-statement) to reduce round trips -->
