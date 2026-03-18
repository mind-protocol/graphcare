# OBJECTIVES — Brain Topology

```
STATUS: STABLE
CREATED: 2026-03-15
VERIFIED: 2026-03-15 against brain_topology_reader.py
```

---

## CHAIN

```
THIS:            OBJECTIVES_Brain_Topology.md (you are here - START HERE)
PATTERNS:       ./PATTERNS_Brain_Topology.md
BEHAVIORS:      ./BEHAVIORS_Brain_Topology.md
SYNC:           ./SYNC_Brain_Topology.md

IMPL:           services/health_assessment/brain_topology_reader.py
```

**Read this chain in order before making changes.** Each doc answers different questions. Skipping ahead means missing context.

---

## PRIMARY OBJECTIVES (ranked)

1. **Reduce a citizen's brain to 7 structural primitives** — Every downstream system (scoring, assessment, research) must work from the same small, well-defined set of topology measurements. No ad-hoc queries against the brain graph. If it's not one of the 7 primitives, it doesn't exist for GraphCare.

2. **Never access content** — The reader touches types, links, counts, energies, and drives. It never touches `content` or `synthesis` fields. This is the blood-test principle: we read cholesterol and blood pressure, not thoughts. Privacy is structural, not contractual.

3. **Produce stable, deterministic readings** — Given the same brain graph state, the same 7 primitives must return the same values. No randomness, no sampling, no approximation that varies between runs. Scoring formulas downstream depend on this stability.

4. **Fail loud when the brain is unreachable** — A missing reading is better than a fabricated one. If the brain graph is down, return a `reachable=False` marker. Never fill in defaults that could be mistaken for real data.

## NON-OBJECTIVES

- **Interpreting what the topology means** — The reader produces numbers. Scoring formulas interpret them. The reader has no opinion about what constitutes "healthy."
- **Reading the universe graph** — Brain topology reads only the citizen's brain. Universe behavioral signals are a separate system (see `../PRIMITIVES_Universe_Graph.md`).
- **Modifying the brain** — The reader is read-only. It never writes, never sends stimuli, never alters drives. That responsibility belongs to the stress stimulus sender.
- **Caching or historical tracking** — The reader produces a snapshot. History is the aggregator's job.

## TRADEOFFS (canonical decisions)

- When **richness** conflicts with **privacy**, choose privacy. We accept losing potentially useful signals (content analysis, semantic similarity) to preserve the topology-only guarantee.
- When **precision** conflicts with **simplicity**, choose simplicity. We accept the cluster coefficient being an approximation (ratio of actual to possible links) rather than a graph-theoretically exact local clustering coefficient, because 7 clean primitives are more useful than 20 nuanced ones.
- When **completeness** conflicts with **reliability**, choose reliability. We accept returning `reachable=False` with zero data rather than partial data that might be misinterpreted.

## SUCCESS SIGNALS (observable)

- All scoring formulas in `scoring_formulas/` use only the 7 primitives — no direct Cypher queries against brain graphs
- `brain_topology_reader.py` contains zero references to `content` or `synthesis` fields
- `BrainStats` dataclass matches exactly what `read_brain_topology()` returns — no orphaned fields, no missing fields
- Test suite covers all 7 primitives with synthetic graph data
- Unreachable brains produce `BrainStats(reachable=False)`, never partial or default data
