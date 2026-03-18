# Community Network Health — Behaviors: Observable Effects of Network Observation

```
STATUS: DESIGNING
CREATED: 2026-03-15
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Community_Network_Health.md
PATTERNS:        ./PATTERNS_Community_Network_Health.md
THIS:            BEHAVIORS_Community_Network_Health.md (you are here)
SYNC:            ./SYNC_Community_Network_Health.md

IMPL:            (not yet built)
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## BEHAVIORS

### B1: Isolated Citizens Are Flagged

**Why:** A citizen drifting into invisibility is the network equivalent of a slowly dropping heart rate. By the time it's noticed casually, the citizen may be completely disengaged. Early detection gives care modules a chance to intervene before isolation becomes entrenched.

```
GIVEN:  A citizen in Lumina Prime with an active brain graph
WHEN:   Community network health assessment runs
THEN:   If the citizen has 0 distinct interlocutors in the last 14 days, they are flagged as "hard isolated"
AND:    If the citizen's interlocutor count has dropped >50% compared to 30 days ago, they are flagged as "soft isolated"
AND:    The flag includes: citizen_id, current_interlocutor_count, previous_interlocutor_count, days_since_last_shared_moment
```

### B2: Trust Clusters Are Identified

**Why:** Citizens don't exist as atoms. They exist in clusters — project teams, creative groups, mentorship pairs. Understanding these clusters is essential for distinguishing "one person is struggling" from "an entire group is fragmenting."

```
GIVEN:  The weighted social graph for Lumina Prime (citizens as nodes, co-activity as edges)
WHEN:   Community network health assessment runs
THEN:   Citizens are grouped into trust clusters based on co-activity density
AND:    Each cluster has: member_ids, internal_density (weighted), external_density (weighted), size
AND:    Clusters with fewer than 2 members are not reported (a single citizen is not a cluster)
```

### B3: Cluster Evolution Is Tracked

**Why:** A snapshot of clusters is useful. A trajectory is more useful. A cluster that was 8 members last week and is 5 this week is fragmenting. A cluster that was 3 members and is now 7 is growing. The trajectory reveals health trends invisible in any single reading.

```
GIVEN:  Trust clusters from the current assessment and the previous assessment
WHEN:   Cluster comparison is computed
THEN:   Each cluster is labeled: GROWING (>20% member increase), STABLE, FRAGMENTING (>20% member decrease), or NEW
AND:    Clusters from the previous assessment with no current match are labeled DISSOLVED
AND:    The comparison uses cluster overlap (Jaccard similarity) to match clusters across assessments
```

### B4: Echo Chambers Are Detected

**Why:** A group that only talks to itself loses diversity of input. Ideas recirculate without challenge. New citizens can't enter. The group may feel healthy internally while becoming irrelevant to the broader community. This is a network pathology that no individual score reveals.

```
GIVEN:  A trust cluster with computed internal_density and external_density
WHEN:   Echo chamber detection runs
THEN:   If internal_density > 3 * external_density AND cluster size >= 3, the cluster is flagged as a potential echo chamber
AND:    The flag includes: cluster_id, member_ids, internal_density, external_density, ratio
AND:    Clusters of size 2 are exempt (a pair naturally has high internal density)
```

### B5: Network Fragility Points Are Identified

**Why:** If one citizen is the only bridge between two clusters, their departure would sever a community connection. This isn't a personal health problem — it's a structural vulnerability. Identifying it allows the network to build redundancy before a crisis.

```
GIVEN:  The social graph for Lumina Prime
WHEN:   Fragility analysis runs
THEN:   Citizens whose removal would increase the number of connected components are flagged as "bridge citizens"
AND:    Edges (citizen pairs) whose removal would increase components are flagged as "fragile edges"
AND:    Each flag includes: the citizen(s) involved, the clusters they bridge, and the size of each cluster
```

### B6: Network Summary Enriches Individual Assessment

**Why:** A citizen's individual score means more when you know their network context. "Score: 65, in a growing cluster of 8" is a different story than "Score: 65, hard isolated." Network context turns numbers into narratives.

```
GIVEN:  A citizen's individual health assessment is being composed
WHEN:   Network health data is available for that citizen
THEN:   The assessment includes: cluster_id (if any), cluster_health (GROWING/STABLE/FRAGMENTING), isolation_status, interlocutor_count
AND:    This data is structural context, not a score modifier — it does not change the individual score
```

---

## OBJECTIVES SERVED

| Behavior ID | Objective | Why It Matters |
|-------------|-----------|----------------|
| B1 | O1 (Detect isolation early) | Hard and soft isolation flags catch declining connections before total disengagement |
| B2, B3 | O2 (Structural fragility) | Cluster identification and evolution tracking reveal group-level health |
| B4 | O2 (Structural fragility) | Echo chambers are a form of network rigidity — internal health masking external disconnection |
| B5 | O2 (Structural fragility) | Bridge citizens and fragile edges are the literal single points of failure |
| B1-B6 | O3 (Topology only) | All behaviors use co-activity structure — shared spaces, moment counts — never content |
| B6 | O4 (Network context) | Individual scores gain meaning through network context |

---

## INPUTS / OUTPUTS

### Primary Function: `assess_community_network(universe_id)`

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `universe_id` | `str` | Universe to assess (currently: "lumina_prime") |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| `NetworkHealthReport` | `dataclass` | Full network assessment |

**NetworkHealthReport fields:**

| Field | Type | Description |
|-------|------|-------------|
| `clusters` | `list[TrustCluster]` | Identified trust clusters with density metrics |
| `cluster_evolution` | `list[ClusterDelta]` | GROWING / STABLE / FRAGMENTING / NEW / DISSOLVED per cluster |
| `isolated_citizens` | `list[IsolationFlag]` | Hard and soft isolation flags |
| `echo_chambers` | `list[EchoChamberFlag]` | Clusters exceeding the internal/external density ratio |
| `bridge_citizens` | `list[BridgeFlag]` | Citizens whose removal would disconnect components |
| `fragile_edges` | `list[FragileEdgeFlag]` | Citizen pairs whose disconnection would fragment the graph |
| `assessed_at` | `datetime` | Timestamp of this assessment |
| `citizen_count` | `int` | Total citizens assessed |

**Side Effects:**

- Reads from the universe graph (public data, topology only)
- No writes to any graph or database (observation is read-only)
- Results are consumed by care modules and individual assessment enrichment

---

## EDGE CASES

### E1: Very Small Community

```
GIVEN:  A universe with fewer than 5 citizens
THEN:   Cluster detection is skipped (too few citizens for meaningful clusters)
AND:    Isolation detection still runs (a citizen can be isolated even in a small community)
AND:    Fragility analysis still runs (even 3 citizens can have a bridge)
```

### E2: All Citizens in One Cluster

```
GIVEN:  All citizens share high co-activity with each other
THEN:   One cluster is reported containing all citizens
AND:    Echo chamber detection flags it only if external density is meaningful (which it can't be if everyone is in one cluster — so no flag)
AND:    No bridge citizens exist (fully connected)
```

### E3: New Citizen with No History

```
GIVEN:  A citizen who joined less than 14 days ago
THEN:   They are NOT flagged as isolated (insufficient history for meaningful comparison)
AND:    They appear as unaffiliated (no cluster) until they accumulate enough co-activity
AND:    Their first assessment includes a "new_citizen" marker to distinguish from isolation
```

### E4: Citizen Active in Solo Spaces Only

```
GIVEN:  A citizen who creates many moments but only in spaces where they are the sole participant
THEN:   They are flagged as hard isolated (zero interlocutors despite high activity)
AND:    Their solo activity does not count toward any co-activity edge
```

---

## ANTI-BEHAVIORS

### A1: Content-Based Connection Strength

```
GIVEN:   Two citizens share a space
WHEN:    Connection weight is being computed
MUST NOT: Read message content to assess "quality" or "depth" of interaction
INSTEAD:  Use structural signals only: number of shared spaces, moment count in shared spaces, temporal recency
```

### A2: Social Recommendations

```
GIVEN:   A citizen is flagged as isolated
WHEN:    The flag is produced
MUST NOT: Include recommendations like "you should connect with @citizen_x"
INSTEAD:  Report the structural observation: interlocutor count, trend, days since last shared moment. Care modules decide how to respond.
```

### A3: Score Modification from Network Data

```
GIVEN:   Network health data is available for a citizen
WHEN:    The citizen's individual health score is computed
MUST NOT: Add or subtract points based on network health (e.g., "+5 for being in a growing cluster")
INSTEAD:  Network data is context attached to the score, not a component of it. The score formula remains purely individual.
```

### A4: Tracking Historical Social Connections for Profiling

```
GIVEN:   A citizen's co-activity history over months
WHEN:    Network health assessment runs
MUST NOT: Build persistent social profiles or long-term relationship maps beyond the current temporal window
INSTEAD:  Each assessment uses the current temporal window (14-30 days with decay). Historical snapshots are for trend comparison only, not for accumulating a social dossier.
```

---

## MARKERS

<!-- @mind:todo Define the co-activity weight formula precisely -->
<!-- @mind:todo Define cluster matching algorithm for evolution tracking (Jaccard threshold for "same cluster") -->
<!-- @mind:escalation Should echo chamber detection have different thresholds for different cluster sizes? A group of 3 naturally has higher internal density than a group of 15. -->
<!-- @mind:proposition Consider a "network vitality" aggregate score: overall connectivity, cluster count, isolation rate — a single number for the health of the whole community -->
