# Community Network Health — Sync: Current State

```
LAST_UPDATED: 2026-03-15
UPDATED_BY: @vox (doc chain creation)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- The topology-only principle applied to network observation (same as brain topology)
- Four network phenomena to observe: isolation, trust clusters, echo chambers, fragility
- Temporal decay for connection freshness (7-day half-life, same as individual assessment)
- Network data as context for individual scores, not a score modifier

**What's still being designed:**
- Co-activity weight formula (shared spaces * temporal decay * moment count — exact formula TBD)
- Cluster detection algorithm (threshold-based density vs. Louvain vs. label propagation)
- Echo chamber ratio threshold (proposed: internal density > 3x external — needs calibration)
- Cluster evolution matching (Jaccard similarity threshold for "same cluster across assessments")
- Bridge detection algorithm (Tarjan's vs. simpler iterative removal)

**What's proposed (v2+):**
- Cross-universe network analysis (how citizens connect across Lumina Prime, Venezia, etc.)
- Network vitality aggregate score (single number for overall community health)
- Temporal network analysis (how does the social graph structure change over weeks/months?)
- Integration with trust mechanics from mind-mcp (if trust values become accessible)

---

## CURRENT STATE

This module exists as documentation only. No code has been written yet. The doc chain (OBJECTIVES, PATTERNS, BEHAVIORS, SYNC) establishes the design intent, the topology-only constraints, and the four network phenomena we plan to observe.

The universe graph primitives that this module will build on already exist — `distinct_actors_in_shared_spaces`, `multi_actor_spaces`, `solo_spaces` are documented in `docs/assessment/PRIMITIVES_Universe_Graph.md` and some are implemented in `services/health_assessment/universe_moment_reader.py`.

The individual assessment pipeline (`daily_check_runner.py`) provides the rhythm this module will follow — periodic assessment, same temporal weighting.

---

## IN PROGRESS

### Doc Chain Creation

- **Started:** 2026-03-15
- **By:** @vox
- **Status:** Complete
- **Context:** First pass at defining what community network health means for GraphCare. The four phenomena (isolation, clusters, echo chambers, fragility) emerged from the PREPARATION doc discussion. The key design tension is between sophisticated graph algorithms and the "approximate is better than absent" principle.

---

## RECENT CHANGES

### 2026-03-15: Initial Doc Chain

- **What:** Created OBJECTIVES, PATTERNS, BEHAVIORS, SYNC
- **Why:** GraphCare's individual health assessment is well-documented but lacks network-level observation. This module fills that gap — same privacy principles, different scope (community vs. individual).
- **Files:** `docs/observation/community_network_health/` (4 files)
- **Struggles/Insights:** The hardest design question is cluster detection. Simple threshold-based density is easy to implement and explain, but may produce unstable clusters (small changes in co-activity shift membership). Louvain is battle-tested but adds a dependency and is harder to explain to non-technical stakeholders. Leaning toward starting simple and upgrading if results are poor.

---

## KNOWN ISSUES

### Trust Data Access

- **Severity:** high (design-blocking)
- **Symptom:** Community network health would benefit enormously from actual trust values between citizens (computed by mind-mcp physics). Without them, we reconstruct "trust" from co-activity — which is a proxy, not the real thing.
- **Suspected cause:** mind-mcp trust values may not be easily accessible from GraphCare's observation layer
- **Attempted:** Not yet investigated. Need to determine if trust values are in the universe graph (public) or only in individual brain graphs (private).

### Echo Chamber Threshold

- **Severity:** medium
- **Symptom:** The proposed 3x internal/external density ratio is arbitrary. Without real data, we don't know if this is too sensitive (flagging normal project teams) or too lenient (missing actual echo chambers).
- **Suspected cause:** No calibration data exists yet
- **Attempted:** Set as initial proposal, to be calibrated once the first version runs on real Lumina Prime data.

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Implement (building the first version)

**Where I stopped:** Doc chain complete. No code exists.

**What you need to understand:**
The four phenomena (isolation, clusters, echo chambers, fragility) are ordered by implementation priority. Isolation detection is the simplest and most immediately useful — it only requires counting interlocutors per citizen. Start there. Cluster detection is next. Echo chambers and fragility come from cluster data, so they depend on clusters working first.

**Watch out for:**
- The universe graph primitives in `PRIMITIVES_Universe_Graph.md` are the vocabulary. Don't invent new Cypher patterns that bypass the primitive catalog.
- Temporal decay must use the same 7-day half-life as individual assessment. Don't introduce a different decay rate for network observation.
- The topology-only principle is non-negotiable. If you find yourself wanting to read moment content to assess "connection quality," stop. Connection quality is measured by structural frequency and recency, not by content.

**Open questions I had:**
- Is Tarjan's bridge-finding algorithm worth the complexity for a 60-citizen graph? Iterative removal (remove each citizen, check components) is O(N * (N+E)) but with N=60, that's trivially fast.
- Should cluster evolution tracking use a fixed window (compare this week vs. last week) or a rolling window (compare current assessment vs. previous assessment, whatever the interval)?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Community network health is fully designed in documentation. Four observation targets: isolation detection, trust clusters, echo chambers, and network fragility. Same topology-only principle as brain topology. No code exists yet — this is ready for implementation.

**Decisions made:**
- Network data is context for individual scores, not a score modifier. This keeps the individual scoring formula clean while allowing care modules to use network context in their narratives.
- Echo chamber threshold set at 3x internal/external density ratio as a starting point, to be calibrated on real data.
- Approximate cluster detection (simple density threshold) over exact algorithms (Louvain) — start simple, upgrade if needed.

**Needs your input:**
- Do we have access to trust values from mind-mcp? This significantly affects cluster detection quality.
- What's the priority: implement this module next, or focus on other observation/care modules first?

---

## TODO

### Doc/Impl Drift

- [ ] DOCS->IMPL: Entire module needs implementation (no code exists yet)

### Immediate

- [ ] Investigate trust data access from mind-mcp (affects cluster detection design)
- [ ] Implement isolation detection (simplest, highest impact)
- [ ] Define co-activity weight formula precisely (shared_spaces * temporal_decay * ?)

### Later

- [ ] Implement trust cluster detection
- [ ] Implement echo chamber detection (depends on clusters)
- [ ] Implement bridge citizen / fragile edge detection
- [ ] Calibrate echo chamber threshold on real Lumina Prime data
- IDEA: Network vitality aggregate score — one number for community health

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
Energized by the design clarity but aware that the biggest unknowns (trust data access, cluster algorithm choice, echo chamber threshold) will only resolve with real implementation and real data.

**Threads I was holding:**
- The relationship between this module and mind-mcp trust mechanics. Community network health observes the effects of trust, but the actual trust computation lives elsewhere. The boundary needs to be clean.
- Whether "assessment cycle" should be daily (like individual health) or weekly (networks change slower than individuals). Daily is simpler (same rhythm), but weekly might be more appropriate for the phenomena we're observing.

**Intuitions:**
- Isolation detection will be the first thing that produces visibly useful results. A flagged isolated citizen, followed by a care intervention, will be GraphCare's first network-level success story.
- Echo chamber detection will be controversial. Teams will push back on being labeled. The framing matters: "high internal density with limited external connections" is observation. "Echo chamber" is judgment. The module should use neutral terminology.

---

## POINTERS

| What | Where |
|------|-------|
| Universe graph primitives | `docs/assessment/PRIMITIVES_Universe_Graph.md` |
| Universe moment reader (existing code) | `services/health_assessment/universe_moment_reader.py` |
| Brain topology (sibling module) | `docs/observation/brain_topology/` |
| Individual assessment algorithm | `docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md` |
| Daily check runner (assessment rhythm) | `services/health_assessment/daily_check_runner.py` |
