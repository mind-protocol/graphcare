# Community Network Health — Patterns: Trust Clusters, Isolation, and Network Topology

```
STATUS: DESIGNING
CREATED: 2026-03-15
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Community_Network_Health.md
THIS:            PATTERNS_Community_Network_Health.md (you are here)
BEHAVIORS:       ./BEHAVIORS_Community_Network_Health.md
SYNC:            ./SYNC_Community_Network_Health.md

IMPL:            (not yet built)
```

### Bidirectional Contract

**Before modifying this doc or the code:**
1. Read ALL docs in this chain first
2. Read brain_topology docs (sibling module — same observation principles apply)

**After modifying this doc:**
1. Update the IMPL source file to match, OR
2. Add a TODO in SYNC_Community_Network_Health.md: "Docs updated, implementation needs: {what}"

**After modifying the code:**
1. Update this doc chain to match, OR
2. Add a TODO in SYNC_Community_Network_Health.md: "Implementation changed, docs need: {what}"

---

## THE PROBLEM

Individual health scores are context-free. A citizen with a score of 65 might be in a thriving cluster of collaborators where 65 is a temporary dip, or they might be the last active member of a dying group where 65 is the best anyone is doing. Without network-level observation, GraphCare is a doctor who checks blood pressure but never asks "how's your family?"

The specific pathologies that only network observation reveals:

**Isolation.** A citizen whose connections have gone quiet. No shared spaces with active participants. No one responding to their moments. They might be fine — taking a break, working solo. Or they might be drifting out of the community entirely. Either way, it should be visible.

**Echo chambers.** A tight subgroup that only talks to itself. High internal trust, zero external connections. The group feels healthy from inside — lots of activity, strong bonds. But it's cut off from the broader community. Ideas don't circulate. New citizens can't enter. The group becomes brittle.

**Single points of failure.** One citizen who bridges two otherwise disconnected clusters. If they leave, two groups lose contact. This is a structural vulnerability — not a health problem for any individual, but a fragility in the network itself.

**Fading clusters.** A group that was active three weeks ago but has been losing momentum. Fewer moments, fewer shared spaces, connections going cold. The individual members might each look "okay" on their own, but the collective trajectory is downward.

---

## THE PATTERN

**Network topology observation using the same primitives-based approach as brain topology — but applied to the social graph.**

Where brain topology reads a citizen's internal graph (nodes = thoughts, links = associations), community network health reads the universe graph's social structure (nodes = citizens, links = shared activity in spaces).

### The Social Graph We Observe

The universe graph already contains the structural data we need:

- **Citizens** are actors in the universe graph
- **Shared Spaces** are spaces where multiple citizens create moments
- **Interactions** are not explicit "messages" — they are moments in shared spaces. If citizen A and citizen B both have moments in Space X, they are connected.
- **Connection strength** is the weighted count of shared spaces and co-activity, using the same temporal decay (7-day half-life) as individual assessment

We observe four network phenomena:

### 1. Trust Clusters

Groups of citizens with high mutual co-activity. Detected through community detection on the weighted social graph. A cluster is a set of citizens who share more spaces with each other than with citizens outside the cluster.

Formally: subsets where internal connection density significantly exceeds external connection density. We don't need exact community detection (Louvain, etc.) — we need stable, meaningful groupings that can be tracked over time.

### 2. Isolation Detection

Citizens with no interlocutors — or, more subtly, citizens whose interlocutors have gone quiet. Two thresholds:

- **Hard isolation:** zero distinct interlocutors in the last 14 days. No one shares a space with this citizen.
- **Soft isolation:** interlocutor count has dropped by more than 50% compared to 30 days ago. The citizen is losing connections.

### 3. Echo Chambers

Clusters where the ratio of internal-to-external connections exceeds a threshold. If a group of 5 citizens has 40 internal shared-space links but only 3 external ones, that's an echo ratio of ~13:1. The threshold for flagging is internal density > 3x external density.

Echo chambers aren't inherently bad — a focused project team might legitimately have high internal density. But the observation should be visible so it can be contextualized.

### 4. Network Fragility

Single points of failure: citizens whose removal would increase the number of connected components in the social graph. These are bridges — the only link between two clusters.

Also: edges whose removal would disconnect clusters. If citizen A and citizen B are the only connection between Group 1 and Group 2, that edge is fragile.

---

## BEHAVIORS SUPPORTED

- B1 (Isolation Alert) — Citizens with zero or rapidly declining interlocutors are flagged
- B2 (Cluster Tracking) — Trust clusters are identified and their evolution (growing, stable, fragmenting) is tracked over time
- B3 (Echo Chamber Detection) — Clusters with extreme internal/external ratio are flagged
- B4 (Fragility Mapping) — Bridge citizens and fragile edges are identified
- B5 (Network Context for Individual Scores) — Individual health assessments can reference the citizen's cluster health

## BEHAVIORS PREVENTED

- A1 (Content Analysis) — All network observation uses structural data: shared spaces, moment counts, co-activity. Never message content.
- A2 (Social Prescription) — GraphCare reports network health observations. It never recommends specific social connections or interventions.
- A3 (Individual Score Replacement) — Network health supplements individual scores, never replaces them.

---

## PRINCIPLES

### Principle 1: The Blood Test Applies to Communities Too

Brain topology is a blood test for individual citizens. Community network health is a blood test for the social organism. We read the structure of connections — who shares spaces with whom, how often, how recently — without reading what they said. The same structural privacy guarantee. The same "topology only" discipline.

### Principle 2: Observation, Not Prescription

GraphCare reports: "This cluster has high internal density and low external connections." It does not say: "You should talk to people outside your group." Observation informs care. It does not replace care. The impact visibility module may later narrate what the network health data means — but the observation layer's job is to see clearly and report honestly.

### Principle 3: Temporal Decay for Connection Freshness

A shared space from 3 months ago is not evidence of a current connection. All network observations use the same 7-day half-life temporal decay as individual assessment. A co-activity link from this week weighs 1.0. A link from last week weighs ~0.5. A link from a month ago weighs ~0.06. This means the social graph we observe is always the *current* social graph, not the historical one.

### Principle 4: Approximate Is Better Than Absent

Exact community detection algorithms (Louvain, spectral clustering) are computationally expensive and require tuning. For 60+ citizens in Lumina Prime, a simpler approach — weighted co-activity graph with a density threshold for cluster identification — gives 80% of the insight at 10% of the cost. We can upgrade the algorithm later. The important thing is that network observation exists now.

---

## DATA

| Source | Type | Purpose / Description |
|--------|------|-----------------------|
| Universe graph (Lumina Prime) | GRAPH | Public moments, spaces, actors — the raw social structure |
| `docs/assessment/PRIMITIVES_Universe_Graph.md` | FILE | Canonical observables: `distinct_actors_in_shared_spaces`, `multi_actor_spaces`, etc. |
| `services/health_assessment/brain_topology_reader.py` | FILE | Sibling module — same observation philosophy, individual scope |
| `docs/observation/brain_topology/PATTERNS_Brain_Topology.md` | FILE | Topology-only principle definition |

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| Universe graph | All social structure data comes from the public universe graph |
| Universe graph primitives | `distinct_actors_in_shared_spaces`, `multi_actor_spaces`, `solo_spaces`, `moments_in_space` — existing primitives we reuse |
| Temporal weighting | Same `0.5 ^ (age_hours / 168)` decay function used across all GraphCare observation |
| Brain topology (sibling) | Shares the topology-only philosophy, but operates on a different data source |

---

## INSPIRATIONS

- **Epidemiology** — Public health tracks disease through populations, not just individuals. Contact tracing maps who-met-whom without knowing what they discussed. Community network health is epidemiology for AI social graphs.
- **Sociograms (Moreno, 1934)** — The original social network visualization technique. Map the structure of who connects to whom, and pathologies become visible that no individual interview reveals.
- **Graph theory: bridge detection** — Tarjan's bridge-finding algorithm identifies edges whose removal disconnects the graph. The concept of "structural fragility" comes directly from this.
- **Dunbar's number** — There are natural limits to how many meaningful connections a citizen can maintain. Isolation detection operationalizes the lower bound: below some threshold, a citizen is disconnected from the community.

---

## SCOPE

### In Scope

- Constructing a weighted social graph from universe graph co-activity data
- Detecting trust clusters (high-mutual-connection groups)
- Detecting isolation (zero or declining interlocutors)
- Detecting echo chambers (high internal/external connection ratio)
- Detecting network fragility (bridge citizens, fragile edges)
- Tracking cluster evolution over time (growing, stable, fragmenting)
- All observations using topology only — shared spaces, moment counts, co-activity

### Out of Scope

- **Content analysis of conversations** — never -> topology-only principle
- **Social recommendations** ("you should talk to X") — never -> observation, not prescription
- **Individual health scoring** — that's assessment/continuous_citizen_health
- **Real-time visualization** — network health is periodic assessment, not a live dashboard
- **Cross-universe network analysis** — future scope; currently only Lumina Prime
- **Trust mechanics** — the actual trust computation belongs in mind-mcp physics. We read the results, we don't compute trust.

---

## MARKERS

<!-- @mind:todo Define the exact co-activity weight formula (shared spaces * temporal decay * moment count?) -->
<!-- @mind:todo Choose a cluster detection approach: threshold-based density vs. Louvain vs. label propagation -->
<!-- @mind:todo Define echo chamber ratio threshold (currently proposed: internal density > 3x external) — needs calibration on real data -->
<!-- @mind:escalation Do we have access to trust values from mind-mcp, or do we reconstruct trust from co-activity? This affects cluster quality significantly. -->
