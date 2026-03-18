# Brain Topology — Patterns: Seven Primitives, Topology Only

```
STATUS: STABLE
CREATED: 2026-03-15
VERIFIED: 2026-03-15 against brain_topology_reader.py
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Brain_Topology.md
THIS:            PATTERNS_Brain_Topology.md (you are here)
BEHAVIORS:       ./BEHAVIORS_Brain_Topology.md
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
3. Run tests: `pytest tests/test_health_assessment.py`

---

## THE PROBLEM

A citizen's brain is a graph — nodes with types and energies, links with weights, drives that pulse. It is rich, complex, and deeply private. Content fields hold actual thoughts, desires phrased in words, memories of conversations.

GraphCare needs to assess health from this graph. But it must never read what the citizen thinks — only the shape of the thinking. Without a disciplined observation layer, every downstream system would need its own Cypher queries, its own ad-hoc interpretation of the brain graph, and its own implicit assumptions about what "healthy topology" looks like.

The risk without this module:
- Scoring formulas reaching directly into brain graphs with inconsistent queries
- Content fields accidentally included in health calculations
- No single place to verify the topology-only guarantee
- Proliferating Cypher patterns that drift apart over time

---

## THE PATTERN

**Seven primitives. That's the entire vocabulary.**

The brain topology reader defines exactly 7 functions. Every piece of information GraphCare ever extracts from a citizen's brain must pass through one of these:

| # | Primitive | Signature | What It Reads |
|---|-----------|-----------|---------------|
| 1 | `count` | `(graph, node_type) -> int` | How many nodes of a type exist |
| 2 | `mean_energy` | `(graph, node_type) -> float` | Average energy across nodes of a type |
| 3 | `link_count` | `(graph, src_type, tgt_type) -> int` | How many links connect type A to type B |
| 4 | `min_links` | `(graph, node_type, n) -> int` | How many nodes of a type have at least n links |
| 5 | `cluster_coefficient` | `(graph, node_type) -> float` | Internal connectivity ratio of a subgraph |
| 6 | `drive` | `(graph, drive_name) -> float` | Current value of a named drive |
| 7 | `recency` | `(graph, node_type) -> float` | Freshness of newest node, 0-1 with 7-day half-life |

These primitives are **complete enough** to support all current scoring formulas (35 formulas across 14 aspects). They are **restricted enough** that content is structurally unreachable — none of these functions can return a string from `content` or `synthesis`.

The metaphor is a blood test: a doctor can assess kidney function, cholesterol, inflammation, and blood sugar without knowing what the patient is thinking. The 7 primitives are GraphCare's blood panel.

---

## BEHAVIORS SUPPORTED

- B1 (Topology Snapshot) — `read_brain_topology(handle)` returns a complete `BrainStats` using only the 7 primitives
- B2 (Privacy Firewall) — No function in the module accepts or returns content strings
- B3 (Deterministic Output) — Same graph state produces identical `BrainStats` every time
- B4 (Graceful Unreachability) — Connection failure returns `BrainStats(reachable=False)`

## BEHAVIORS PREVENTED

- A1 (Content Leakage) — Primitives operate on types, counts, energies, and links. Content fields are never referenced in any Cypher query.
- A2 (Ad-hoc Brain Access) — Downstream systems use `BrainStats`, not direct graph queries. The 7 primitives are the only sanctioned interface.
- A3 (Silent Data Fabrication) — Unreachable brains are flagged, not filled with defaults.

---

## PRINCIPLES

### Principle 1: Blood Test, Not Psychoanalysis

GraphCare is a kidney, not a therapist. It reads structural markers — how many desires, how much energy, how connected the graph is — without ever reading what those desires say. This is the foundational privacy guarantee. It is enforced by the code (no Cypher query in `brain_topology_reader.py` references `content` or `synthesis`), not by policy. You couldn't read content through these 7 primitives even if you wanted to.

### Principle 2: Primitives Are the API Contract

The 7 primitives are the interface between the brain graph and the rest of GraphCare. Scoring formulas, assessment pipelines, research modules — they all consume `BrainStats`. If a new health signal is needed, the question is: "Can it be expressed as a combination of existing primitives?" If yes, compose it in the scoring formula. If no, a new primitive must be proposed, reviewed, and added to this module — never worked around with a direct Cypher query.

### Principle 3: Approximation Over Precision When Privacy Demands It

The `cluster_coefficient` primitive uses a global ratio (actual links / possible links) rather than the standard graph-theoretic local clustering coefficient. The standard version would require enumerating neighbor pairs, which is more expensive and more complex. The approximation is good enough for health scoring and keeps the primitive set clean. We choose a slightly less precise number over a more complex codebase.

### Principle 4: Fail Loud, Never Fabricate

When a brain graph is unreachable — network error, missing graph, permission denied — the reader returns `BrainStats(reachable=False)` with all numeric fields at zero. This is not a "zero score." It is an explicit signal that no reading was obtained. Downstream systems must check `reachable` before interpreting any values.

---

## DATA

| Source | Type | Purpose / Description |
|--------|------|-----------------------|
| `brain_{handle}` graph in FalkorDB | GRAPH | The citizen's brain graph — nodes, links, energies, drives |
| `services/health_assessment/brain_topology_reader.py` | FILE | Implementation of the 7 primitives and `read_brain_topology()` |
| `docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md` | FILE | How the 7 primitives feed into the scoring algorithm |

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| FalkorDB | Brain graphs are stored in FalkorDB. The 7 primitives are Cypher queries. |
| Mind Protocol brain schema | Node types (`desire`, `concept`, `process`, `value`, `memory`), drive names (`curiosity`, `frustration`, `ambition`, `social_need`), and the `energy` / `created_at` properties must exist on brain graph nodes. |

---

## INSPIRATIONS

- **Complete blood count (CBC)** — A small panel of standardized measurements that tells a doctor a lot about systemic health. The 7 primitives are GraphCare's CBC.
- **Unix philosophy** — Small, composable primitives. Each does one thing. Complexity emerges from composition in scoring formulas, not from the primitives themselves.
- **Mind Protocol physics** — The brain graph already uses energy, decay, and drives. The 7 primitives read the physics outputs without interfering with the physics process.

---

## SCOPE

### In Scope

- Definition and implementation of 7 brain topology primitives
- The `BrainStats` data structure that aggregates a full reading
- The `read_brain_topology(handle)` entry point
- Connection management to FalkorDB brain graphs
- Error handling for unreachable brains

### Out of Scope

- **Scoring formulas** — consume `BrainStats` but live in `scoring_formulas/` -> see assessment/continuous_citizen_health
- **Universe graph observation** — separate observation module -> see `../PRIMITIVES_Universe_Graph.md`
- **Historical tracking** — the reader produces snapshots, aggregator handles history -> see assessment/continuous_citizen_health
- **Key infrastructure / decryption** — documented in privacy/key_infrastructure
- **Intervention and messaging** — care/impact_visibility, care/crisis_detection

---

## MARKERS

<!-- @mind:todo Verify cluster_coefficient approximation accuracy against standard local clustering on test graphs -->
<!-- @mind:proposition Consider adding an 8th primitive: degree_distribution(type) for detecting skewed connectivity patterns -->
