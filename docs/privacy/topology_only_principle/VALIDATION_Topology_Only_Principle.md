# Topology Only Principle — Validation: What Must Be True

```
STATUS: DESIGNING
CREATED: 2026-03-15
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Topology_Only_Principle.md
PATTERNS:        ./PATTERNS_Topology_Only_Principle.md
THIS:            VALIDATION_Topology_Only_Principle.md (you are here)
SYNC:            ./SYNC_Topology_Only_Principle.md

IMPL:            services/health_assessment/brain_topology_reader.py
```

---

## PURPOSE

**Validation = what we care about being true.**

These invariants protect the foundational promise of GraphCare: we assess health without reading thoughts. If any of these invariants fails, GraphCare's entire trust model collapses. There is no "minor" content access violation — any breach is existential.

---

## INVARIANTS

### V1: Content Is Cryptographically Inaccessible

**Why we care:** This is the foundational promise. If GraphCare can access content, every privacy claim is a lie. Not "we choose not to" — "we cannot."

```
MUST:   GraphCare's private key decrypts only topology metadata (node types, counts, energies, links, drives)
NEVER:  GraphCare possesses, stores, receives, or can derive the citizen's content decryption key
```

### V2: Scoring Formulas Use Only Primitives

**Why we care:** A scoring formula that queries content would violate the topology-only principle at the application layer even if encryption prevents it at the data layer. Defense in depth: the code must not even attempt content access.

```
MUST:   Every scoring formula in scoring_formulas/ is composed exclusively of: count, mean_energy, link_count, min_links, cluster_coefficient, drive, recency (brain) + moments, moment_has_parent, first_moment_in_space, distinct_actors, link dimension queries (universe)
NEVER:  A scoring formula contains a Cypher query accessing .content or .synthesis fields, an LLM call, an embedding comparison, or any content-derived input
```

### V3: Intervention Messages Reference Only Structural Facts

**Why we care:** Even if scoring formulas are clean, an intervention message that says "your desire to find the surface is stalled" reveals that GraphCare read the content of a desire node. Messages must reference only numbers, counts, and structural patterns.

```
MUST:   Every intervention message references only: counts, scores, deltas, energies, drives, link ratios, temporal patterns
NEVER:  An intervention message contains phrases like "your desire to...", "you wrote...", "your idea about...", "the content of...", "you said...", "your message about..."
```

### V4: Cypher Queries Access Only Topology Fields

**Why we care:** The brain_topology_reader.py is the boundary between GraphCare and the citizen's brain. Every Cypher query it executes must be auditable and must access only structural fields.

```
MUST:   Every Cypher query in brain_topology_reader.py accesses only: node labels, node_type, energy, drive values, link existence, link counts, timestamps
NEVER:  A Cypher query returns .content, .synthesis, .name (when name contains user-authored text), or any field containing citizen-authored prose
```

### V5: Topology Sufficiency for Health Assessment

**Why we care:** If topology is insufficient to assess health, the pressure to add content access will eventually win. The scoring framework must demonstrate that meaningful, differentiating health scores are achievable from topology alone.

```
MUST:   The 5 synthetic test profiles (healthy, unhealthy, brain-rich, active, average) produce scores that correctly differentiate health states using topology-only formulas
NEVER:  A capability is scored using content-derived features, even indirectly (e.g., embedding similarity between desire content and moment content)
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
| V1 | Cryptographic content inaccessibility | CRITICAL |
| V2 | Formula purity — only primitives | CRITICAL |
| V3 | Message purity — no content references | CRITICAL |
| V4 | Query purity — topology fields only | CRITICAL |
| V5 | Topology sufficiency — scores differentiate health states | HIGH |

---

## MARKERS

<!-- @mind:todo Add automated CI check that scans all scoring_formulas/*.py for .content or .synthesis field access -->
<!-- @mind:proposition Consider a formal audit process: every new scoring formula must pass a "topology-only review" before merge -->
