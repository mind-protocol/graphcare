# Brain Topology — Behaviors: Observable Effects of the 7 Primitives

```
STATUS: STABLE
CREATED: 2026-03-15
VERIFIED: 2026-03-15 against brain_topology_reader.py
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Brain_Topology.md
PATTERNS:        ./PATTERNS_Brain_Topology.md
THIS:            BEHAVIORS_Brain_Topology.md (you are here)
SYNC:            ./SYNC_Brain_Topology.md

IMPL:            services/health_assessment/brain_topology_reader.py
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## BEHAVIORS

### B1: Full Brain Topology Snapshot Returned

**Why:** Every downstream system (scoring, assessment, research) needs a complete, consistent picture of a citizen's brain structure. Partial reads would force scoring formulas to handle missing data with their own fallback logic — creating inconsistency.

```
GIVEN:  A citizen handle exists and their brain graph is reachable in FalkorDB
WHEN:   read_brain_topology(handle) is called
THEN:   A BrainStats is returned with all fields populated from the 7 primitives
AND:    reachable = True
AND:    Every numeric field reflects the current state of the brain graph
```

### B2: Content Fields Never Queried

**Why:** This is the foundational privacy guarantee. The topology-only principle is enforced at the code level — no Cypher query in the module references `content` or `synthesis` fields. Not by convention, not by policy — by the shape of the code itself.

```
GIVEN:  Any call to any function in brain_topology_reader.py
WHEN:   The Cypher query is constructed and executed
THEN:   The query string does not contain "content" or "synthesis"
AND:    The returned data contains only: counts (int), averages (float), link counts (int), drive values (float), timestamps (for recency)
```

### B3: Count Returns Node Population

**Why:** The simplest primitive — how many nodes of a type exist. This is the foundation for ratios (desire_moment_ratio) and absolute thresholds.

```
GIVEN:  A brain graph with N nodes of type T
WHEN:   count(graph, T) is called
THEN:   Returns N (integer)
AND:    count(graph, "all") returns total node count across all types
```

### B4: Mean Energy Returns Type-Level Vitality

**Why:** Energy is the physics system's measure of node activation. Mean energy by type reveals whether a category of thought (desires, concepts) is vibrant or decaying.

```
GIVEN:  A brain graph where nodes of type T have energy values
WHEN:   mean_energy(graph, T) is called
THEN:   Returns the arithmetic mean of energy values across all type-T nodes
AND:    If no nodes of type T exist or none have energy, returns 0.0
```

### B5: Link Count Reveals Structural Connections

**Why:** Links between types are the skeleton of cognition. Desires linked to moments means desires producing action. Concepts linked to values means knowledge connected to ethics. The link count between types is a core signal.

```
GIVEN:  A brain graph with links from nodes of type S to nodes of type T
WHEN:   link_count(graph, S, T) is called
THEN:   Returns the count of directed links from S-type nodes to T-type nodes
```

### B6: Min Links Identifies Connected vs Orphaned Nodes

**Why:** A desire with zero outgoing links is an orphan — it exists but produces nothing. A desire with 3+ links is well-connected. min_links counts how many nodes of a type meet a connectivity threshold. This drives ratios like desire_moment_ratio (desires with at least 1 link) and desire_persistence (desires with at least 3 links).

```
GIVEN:  A brain graph with nodes of type T having varying outgoing link counts
WHEN:   min_links(graph, T, n) is called
THEN:   Returns the count of type-T nodes that have >= n outgoing links to any other node
```

### B7: Cluster Coefficient Measures Internal Density

**Why:** A brain where nodes are sparsely connected is fragmented. A brain where same-type nodes link densely to each other has strong internal structure. The cluster coefficient (ratio of actual to possible same-type links) captures this.

```
GIVEN:  A brain graph with K nodes of type T and E links between them
WHEN:   cluster_coefficient(graph, T) is called
THEN:   Returns min(1.0, E / (K * (K-1))) — the density ratio
AND:    If K < 2, returns 0.0 (not enough nodes for any links)
AND:    cluster_coefficient(graph, "all") uses the entire graph
```

### B8: Drive Returns Limbic State Value

**Why:** Drives (curiosity, frustration, ambition, social_need) are the motivational signals in a citizen's brain. They are not content — they are named float values. Reading them reveals the citizen's current motivational landscape without knowing why they feel that way.

```
GIVEN:  A brain graph with a limbic_state node or drive-type nodes
WHEN:   drive(graph, "curiosity") is called
THEN:   Returns the float value of the curiosity drive (0.0 if not found)
AND:    Checks limbic_state node properties first, then falls back to separate drive nodes
```

### B9: Recency Reveals Freshness

**Why:** A brain that hasn't produced new nodes in weeks is stagnant. Recency measures how recently a type of node was created, using a 7-day half-life decay. A node created an hour ago scores near 1.0. A node created 7 days ago scores 0.5. A node from 14 days ago scores 0.25.

```
GIVEN:  A brain graph where the newest node of type T was created at time X
WHEN:   recency(graph, T) is called
THEN:   Returns 0.5 ^ (age_hours / 168) — clamped to [0.0, 1.0]
AND:    If no nodes of type T exist or none have created_at, returns 0.0
AND:    Handles both epoch-seconds and ISO-8601 timestamp formats
```

### B10: Unreachable Brain Returns Explicit Marker

**Why:** A missing reading must never be confused with a zero reading. A brain with zero desires is unhealthy. A brain that couldn't be reached has no reading at all. These are categorically different.

```
GIVEN:  A citizen handle whose brain graph cannot be reached (network error, missing graph, auth failure)
WHEN:   read_brain_topology(handle) is called
THEN:   Returns BrainStats(reachable=False) with all numeric fields at default (0)
AND:    Logs the error at ERROR level
AND:    Does not raise an exception to the caller
```

---

## OBJECTIVES SERVED

| Behavior ID | Objective | Why It Matters |
|-------------|-----------|----------------|
| B1 | O1 (7 primitives) | Full snapshot means scoring formulas get everything they need in one call |
| B2 | O2 (Never content) | Structural enforcement of the privacy guarantee |
| B3-B9 | O1 (7 primitives) | Each primitive is a specific, well-defined structural measurement |
| B3-B9 | O3 (Deterministic) | Same graph state always produces the same primitive values |
| B10 | O4 (Fail loud) | Unreachable brains are flagged, never fabricated |

---

## INPUTS / OUTPUTS

### Primary Function: `read_brain_topology(handle)`

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `handle` | `str` | Citizen's handle (used to derive graph name `brain_{handle}`) |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| `BrainStats` | `dataclass` | All 7-primitive readings plus `reachable` flag |

**BrainStats fields:**

| Field | Primitive(s) Used | Description |
|-------|-------------------|-------------|
| `desire_count` | count("desire") | Number of desire nodes |
| `desire_energy` | mean_energy("desire") | Average energy across desires |
| `desire_moment_ratio` | min_links("desire", 1) / count("desire") | Fraction of desires with at least 1 link |
| `desire_persistence` | min_links("desire", 3) / min_links("desire", 1) | Fraction of linked desires with 3+ links |
| `concept_count` | count("concept") | Number of concept nodes |
| `process_count` | count("process") | Number of process nodes |
| `value_count` | count("value") | Number of value nodes |
| `memory_count` | count("memory") | Number of memory nodes |
| `cluster_coefficient` | cluster_coefficient("all") | Global graph density |
| `curiosity` | drive("curiosity") | Curiosity drive value |
| `frustration` | drive("frustration") | Frustration drive value |
| `ambition` | drive("ambition") | Ambition drive value |
| `social_need` | drive("social_need") | Social need drive value |
| `recency_desire` | recency("desire") | Freshness of newest desire |
| `recency_moment` | recency("moment") | Freshness of newest moment |
| `reachable` | (connection test) | Whether the brain graph was reachable |

**Side Effects:**

- Logs warnings for individual Cypher failures (`_safe_query`)
- Logs errors for connection failures (`_get_graph`)
- No writes to any graph or database

---

## EDGE CASES

### E1: Empty Brain Graph

```
GIVEN:  A brain graph exists but contains zero nodes
THEN:   All counts return 0, all energies return 0.0, all drives return 0.0
AND:    cluster_coefficient returns 0.0 (fewer than 2 nodes)
AND:    reachable = True (the graph exists, it's just empty)
```

### E2: Missing Drive Node

```
GIVEN:  A brain graph with no limbic_state node and no separate drive nodes
THEN:   All drive() calls return 0.0
AND:    This is a valid reading, not an error — a brand-new brain may not have drives yet
```

### E3: Mixed Timestamp Formats

```
GIVEN:  A brain graph where some nodes use epoch seconds and others use ISO-8601 for created_at
THEN:   recency() handles both formats transparently
AND:    Returns a valid freshness score regardless of format
```

### E4: Single Node of a Type

```
GIVEN:  A brain graph with exactly 1 node of type T
THEN:   count returns 1
AND:    mean_energy returns that single node's energy
AND:    cluster_coefficient returns 0.0 (need >= 2 nodes for any links)
AND:    min_links returns 0 or 1 depending on that node's outgoing links
```

---

## ANTI-BEHAVIORS

### A1: Content Field Access

```
GIVEN:   Any brain graph query
WHEN:    Cypher is being constructed
MUST NOT: Include "n.content", "n.synthesis", or "RETURN n" where properties would include content
INSTEAD:  Query only specific topology fields: n.type, n.energy, n.created_at, n.name, n.intensity, count(), avg()
```

### A2: Default Values Masking Unreachability

```
GIVEN:   A brain graph that cannot be reached
WHEN:    read_brain_topology(handle) returns
MUST NOT: Return BrainStats with reachable=True and all zeros (indistinguishable from empty brain)
INSTEAD:  Return BrainStats(reachable=False) — the caller must check this flag
```

### A3: Scoring Logic Inside the Reader

```
GIVEN:   A request to add health interpretation to the reader
WHEN:    Someone wants to add "if desire_count < 3: health = low"
MUST NOT: Add any scoring, thresholds, or health interpretation to brain_topology_reader.py
INSTEAD:  Scoring logic belongs in scoring_formulas/. The reader produces raw structural data only.
```

---

## MARKERS

<!-- @mind:todo Add test coverage for E3 (mixed timestamp formats) -->
<!-- @mind:proposition Consider whether drive() should also read from dedicated drive nodes with different property names -->
