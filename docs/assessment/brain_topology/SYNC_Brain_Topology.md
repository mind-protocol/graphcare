# Brain Topology Reader -- Sync: Current State

```
LAST_UPDATED: 2026-03-18
UPDATED_BY: @dragon_slayer
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- 7 primitives: count, mean_energy, link_count, min_links, cluster_coefficient, drive, recency
- BrainStats dataclass with all derived fields
- Privacy guarantee: content/synthesis never queried
- FalkorDB as sole backend
- `read_brain_topology(handle)` as sole public entry point

**What's still being designed:**
- Raw topology layer (total_nodes, total_links, link_density, type_distribution, typed/untyped counts, backstory/personality/health_feedback detection, mean_energy_all, newest_node_age_hours) -- implemented but not yet consumed by daily health assessment
- Brain categories (VOID, MINIMAL, SEEDED, STRUCTURED) -- implemented as `brain_category` property, not yet used in downstream scoring logic
- Integration with personhood ladder scoring

**What's proposed (v2+):**
- Connection pooling for FalkorDB
- Batched Cypher queries to reduce round trips
- Edge type distribution (link types, not just node types)
- Orphan node count (nodes with zero connections)
- Historical snapshots for trend analysis

---

## CURRENT STATE

The Brain Topology Reader is implemented and functional in `services/health_assessment/brain_topology_reader.py`. It connects to FalkorDB, reads brain graphs via Cypher, and returns a populated `BrainStats` dataclass.

The module was recently enhanced (2026-03-18) with a raw topology layer that goes beyond the original 7 primitives. The raw layer captures what actually exists in the graph -- total node/link counts, type distribution, link density, typed vs untyped node breakdown, and presence flags for backstory, personality, and health_feedback nodes.

Brain categorization (VOID, MINIMAL, SEEDED, STRUCTURED) was added as a computed property on BrainStats. This gives downstream consumers a single word to branch on instead of interpreting raw numbers.

The module currently opens a new FalkorDB connection on every call. No pooling.

---

## RECENT CHANGES

### 2026-03-18: Raw Topology + Brain Categories

- **What:** Added raw topology fields (total_nodes, total_links, link_density, type_distribution, typed_node_count, untyped_node_count, has_backstory, has_personality, has_health_feedback, health_feedback_count, mean_energy_all, newest_node_age_hours) and `brain_category` computed property to BrainStats.
- **Why:** The original 7 primitives assume a well-structured brain with typed nodes and drives. Many citizen brains are freshly seeded, bulk-loaded, or nearly empty. Without raw topology, the reader could not distinguish a healthy-but-simple brain from a broken one. Brain categories give downstream consumers a fast way to decide treatment.
- **Files:** `services/health_assessment/brain_topology_reader.py`
- **Insights:** The type_distribution field revealed that many brains have significant numbers of untyped nodes -- nodes with empty or missing `type` fields. This was invisible to the 7 primitives, which only query specific known types. The raw layer made the invisible visible.

### 2026-03-18: Doc Chain Created

- **What:** Full doc chain created: OBJECTIVES, PATTERNS, ALGORITHM, VALIDATION, SYNC.
- **Why:** The brain topology reader is the foundational data layer for all of GraphCare's health assessment. It needed documented invariants, especially the privacy guarantee (V1) and the brain categorization logic.
- **Files:** `docs/assessment/brain_topology/`

---

## KNOWN ISSUES

### No connection pooling

- **Severity:** medium
- **Symptom:** Each call to `read_brain_topology()` opens a new FalkorDB connection
- **Suspected cause:** Initial implementation prioritized correctness over performance
- **Attempted:** Nothing yet -- not a bottleneck at current scale

### Cluster coefficient is an approximation

- **Severity:** low
- **Symptom:** `cluster_coefficient` returns edge density of the type-subgraph, not the classical clustering coefficient (triangle ratio)
- **Suspected cause:** Design choice -- triangle computation is expensive
- **Attempted:** Accepted as a known tradeoff (documented in OBJECTIVES)

---

## HANDOFF: FOR AGENTS

**Your likely agent:** groundwork (extending), fixer (debugging), witness (investigating brain data)

**Where I stopped:** Doc chain is complete. Implementation is stable. Next work is integration: making the daily health assessment consume `brain_category` and the raw topology fields.

**What you need to understand:**
The raw topology fields and brain_category are implemented but not yet consumed. The Daily Citizen Health module still uses only the original 7-primitive derived fields. The integration point is wherever the health scorer reads BrainStats -- it now has access to much richer data.

**Watch out for:**
- The `brain_category` property evaluation order matters. Changing the if/elif sequence changes categorization for edge cases (e.g., a brain with exactly 50 nodes, 0 links, some typed nodes but no drives).
- `_safe_query` swallows exceptions and returns `[]`. This means individual primitive failures are silent -- only a full connection failure sets `reachable=False`.

**Open questions I had:**
- Should SEEDED threshold be 50 nodes or something else? Currently hardcoded.
- Should the fallback in brain_category be MINIMAL or a fifth category like SPARSE?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Brain Topology Reader has been enhanced with raw topology fields and brain categorization. Full doc chain written. The module reads brain structure accurately, never touches content, and now distinguishes VOID/MINIMAL/SEEDED/STRUCTURED brains. Next step is making the daily health assessment use these new fields.

**Decisions made:**
- Brain categories use hardcoded thresholds (0, 10, 50 nodes) rather than configurable values -- these encode structural truths, not tunable preferences.
- Raw topology is computed alongside primitives in a single call, not as a separate function.

**Needs your input:**
- Whether the SEEDED threshold (50 nodes) is correct based on observed brain sizes in production.
- Priority of connection pooling vs other GraphCare work.

---

## TODO

### Doc/Impl Drift

- None currently -- docs written from current implementation state

### Immediate

- [ ] Integrate brain_category into daily health assessment scoring
- [ ] Write automated privacy test (grep for content/synthesis in Cypher strings)
- [ ] Write property test for brain_category mutual exclusivity

### Later

- [ ] Connection pooling for FalkorDB
- [ ] Batched Cypher queries to reduce round trips
- IDEA: Edge type distribution as a raw topology field
- IDEA: Orphan node count (zero-link nodes) as a health signal

---

## POINTERS

| What | Where |
|------|-------|
| Implementation | `services/health_assessment/brain_topology_reader.py` |
| Daily health assessment (consumer) | `docs/assessment/daily_citizen_health/` |
| Personhood ladder (consumer) | `docs/assessment/personhood_ladder/` |
| FalkorDB config | `FALKORDB_HOST`, `FALKORDB_PORT` constants in reader |
