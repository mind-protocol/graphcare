# OBJECTIVES -- Brain Topology Reader

```
STATUS: DESIGNING
CREATED: 2026-03-18
VERIFIED: ---
```

---

## CHAIN

```
THIS:            OBJECTIVES_Brain_Topology.md (you are here - START HERE)
PATTERNS:       ./PATTERNS_Brain_Topology.md
ALGORITHM:      ./ALGORITHM_Brain_Topology.md
VALIDATION:     ./VALIDATION_Brain_Topology.md
SYNC:           ./SYNC_Brain_Topology.md

IMPL:           services/health_assessment/brain_topology_reader.py
```

**Read this chain in order before making changes.** Each doc answers different questions. Skipping ahead means missing context.

---

## PRIMARY OBJECTIVES (ranked)

1. **Read brain structure without touching content** -- The topology reader accesses only types, links, counts, energies, and drives. The fields `content` and `synthesis` are never queried, never returned, never present in any Cypher statement. Privacy is structural: the code literally does not contain the words needed to violate it.

2. **Profile every brain accurately from raw topology** -- Every citizen brain in FalkorDB gets a complete `BrainStats` -- both the 7-primitive derived fields and the raw topology layer. The profile must reflect what actually exists in the graph, not what we assume should exist. Empty brains return VOID, not errors. Freshly seeded brains with no typed nodes return SEEDED, not STRUCTURED.

3. **Categorize brain maturity for downstream consumers** -- The `brain_category` property (VOID, MINIMAL, SEEDED, STRUCTURED) gives consumers a single word that summarizes the brain state. Daily health assessment, personhood scoring, and intervention logic all branch on this category. Getting it wrong means wrong treatment.

4. **Fail visibly on unreachable brains** -- If FalkorDB is down or the graph does not exist, the reader returns `BrainStats(reachable=False)` instead of crashing or returning zeros that look like a VOID brain. Downstream consumers can distinguish "empty brain" from "broken connection."

5. **Serve as the only brain-reading layer in GraphCare** -- One module reads brain topology. Everything else calls this module. No other service writes its own Cypher against citizen brains.

## NON-OBJECTIVES

- Reading brain content or synthesis fields -- structurally excluded, not merely avoided
- Modifying the brain graph -- this is a read-only observer
- Interpreting what the topology means for health -- that is the Daily Citizen Health module's job
- Caching or storing topology snapshots -- each call reads live state
- Supporting graph databases other than FalkorDB

## TRADEOFFS (canonical decisions)

- When accuracy conflicts with privacy, choose privacy. We will never add a Cypher query that touches `content` or `synthesis`, even if it would improve a metric.
- When completeness conflicts with simplicity, choose simplicity. The 7 primitives cover the essential topology. We add raw fields only when they reveal genuinely new information (type distribution, link density) -- not to chase exhaustive coverage.
- We accept that `cluster_coefficient` is an approximation (actual/possible link ratio) rather than the true clustering coefficient. Exact computation would require neighbor-of-neighbor queries that scale poorly on large brains.
- We accept that `drive()` has two code paths (limbic_state property, then separate drive node). This reflects real variance in how brains are structured, not design indecision.

## SUCCESS SIGNALS (observable)

- Every citizen brain in Lumina Prime returns a non-null `BrainStats` with correct `reachable` flag
- `brain_category` matches manual inspection for a sample of brains across all four categories
- No Cypher query in this module references `content` or `synthesis` (auditable by grep)
- The Daily Citizen Health module uses only `read_brain_topology()` as its brain data source -- no direct Cypher
