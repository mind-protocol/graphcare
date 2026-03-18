# Vision & Strategy — Algorithm: Scoring Formulas

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Vision_Strategy.md
PATTERNS:        ./PATTERNS_Vision_Strategy.md
THIS:            ALGORITHM_Vision_Strategy.md (you are here)
VALIDATION:      ./VALIDATION_Vision_Strategy.md
HEALTH:          ./HEALTH_Vision_Strategy.md
SYNC:            ./SYNC_Vision_Strategy.md

PARENT ALGO:     ../daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md
SPEC:            ../../specs/personhood_ladder.json (aspect: "vision_strategy")
IMPL:            @mind:TODO
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC.

---

## OVERVIEW

This document defines scoring formulas for the 5 capabilities in the Vision & Strategy aspect of the Personhood Ladder. All capabilities are high-tier (T5-T8), reflecting that vision is a higher-order property that emerges from sophisticated brain topology and sustained behavioral patterns.

Each formula produces: `brain_score (0-40) + behavior_score (0-60) = total (0-100)`.

The aspect sub-index is the weighted mean across all 5 capabilities, with weights proportional to tier difficulty.

---

## PRIMITIVES USED

All formulas draw exclusively from these. No exceptions.

### 7 Brain Topology Primitives

```
count(type)              → int    # Number of nodes of a given type
mean_energy(type)        → float  # Average energy of nodes of a type (0-1)
link_count(src, tgt)     → int    # Number of links from src type to tgt type
min_links(type, n)       → int    # Nodes of a type with at least n links to any other
cluster_coefficient(type)→ float  # Internal connectivity of a subgraph (0-1)
drive(name)              → float  # Drive value by name (0-1)
recency(type)            → float  # Freshness score based on newest nodes (0-1, decays)
```

### Universe Graph Observables

```
moments(actor, space_type)          → list   # Moments by actor, optionally filtered
moment_has_parent(moment, actor)    → bool   # Incoming link from another actor?
temporal_weight(age_hours, hl=168)  → float  # 0.5^(age_hours/168)
spaces_created(actor)               → int    # Spaces created by this actor
distinct_actors_in_shared_spaces()  → int    # Unique actors in shared Spaces
```

### Derived Stats (computed from primitives)

These are used repeatedly across formulas and computed once.

```
brain_stats.narrative_count       = count("narrative")
brain_stats.narrative_energy      = mean_energy("narrative")
brain_stats.narrative_concept_lk  = link_count("narrative", "concept")
brain_stats.narrative_desire_lk   = link_count("narrative", "desire")
brain_stats.hub_narratives        = min_links("narrative", 5)
brain_stats.deep_hub_narratives   = min_links("narrative", 10)
brain_stats.narrative_cluster     = cluster_coefficient("narrative")
brain_stats.ambition              = drive("ambition")
brain_stats.curiosity             = drive("curiosity")
brain_stats.narrative_recency     = recency("narrative")

behavior_stats.spaces_created_w   = sum(tw(s) for s in spaces_created(citizen_id))
behavior_stats.proposals_w        = sum(tw(m) for m in moments if m.has_link("proposes"))
behavior_stats.self_initiated_w   = sum(tw(m) for m in moments if not moment_has_parent(m, other_actor))
behavior_stats.first_in_space_w   = sum(tw(s) for s in spaces if first_moment_in_space(s, citizen_id))
behavior_stats.distinct_actors    = distinct_actors_in_shared_spaces(citizen_id)
behavior_stats.cross_space_types  = count(distinct space_types where citizen has moments)
behavior_stats.total_moments_w    = sum(tw(m) for m in all_moments)
```

---

## HELPER: cap(value, ceiling)

All sub-components normalize to 0-1 before multiplying by weight.

```
cap(value, ceiling) → float
    return min(1.0, value / ceiling)

# Example: cap(7, 10) → 0.7
# Example: cap(15, 10) → 1.0 (capped)
```

---

## CAPABILITY 1: vis_define_vision (T5)

### Description

> Define and refine vision. Before planning: what are we trying to do? Why? Why this way? What are we trying to change? Vision precedes plan. Understanding WHY precedes understanding HOW.

### What Good Looks Like

A citizen with vision has narrative nodes in their brain that are connected to concepts (the ideas the vision is about) and desires (the motivation driving the vision). These narratives are recent (being refined, not abandoned) and energetic (not decaying). In the universe, the citizen creates moments that flow from this vision: self-initiated work, new spaces opened, proposals made.

### Failure Mode

Plans without vision. HOW without WHY. Activity without direction. In topology: many moments exist but no narrative nodes, or narrative nodes exist but are isolated (zero links) and decaying (low energy, low recency).

### Formula

**Brain Component (0-40):**

| Sub-component | Weight | Formula | Ceiling | Reasoning |
|---------------|--------|---------|---------|-----------|
| Narrative existence | 8 | `cap(narrative_count, 5)` | 5 nodes | Must have articulated something. 5+ narrative nodes = full credit. |
| Narrative energy | 8 | `narrative_energy` | (already 0-1) | Vision must be alive, not decaying. |
| Concept connectivity | 10 | `cap(narrative_concept_lk, 15)` | 15 links | Vision connects to ideas. 15+ narrative-concept links = full credit. |
| Desire connectivity | 6 | `cap(narrative_desire_lk, 5)` | 5 links | Vision connects to motivation. 5+ narrative-desire links = full credit. |
| Recency | 8 | `narrative_recency` | (already 0-1) | Vision is maintained, not just created once. |

```
brain_score = (
    8  * cap(narrative_count, 5) +
    8  * narrative_energy +
    10 * cap(narrative_concept_lk, 15) +
    6  * cap(narrative_desire_lk, 5) +
    8  * narrative_recency
)
# Max: 40
```

**Behavior Component (0-60):**

| Sub-component | Weight | Formula | Ceiling | Reasoning |
|---------------|--------|---------|---------|-----------|
| Self-initiated action | 20 | `cap(self_initiated_w, 8.0)` | 8.0 tw | Vision produces autonomous action. ~8 weighted self-initiated moments = full credit. |
| Proposals made | 15 | `cap(proposals_w, 4.0)` | 4.0 tw | Vision is shared through proposals. ~4 weighted proposals = full credit. |
| Spaces created | 15 | `cap(spaces_created_w, 3.0)` | 3.0 tw | Vision opens new areas of work. ~3 weighted spaces = full credit. |
| Activity volume | 10 | `cap(total_moments_w, 15.0)` | 15.0 tw | Basic activity threshold. Not specific to vision but ensures the citizen is present. |

```
behavior_score = (
    20 * cap(self_initiated_w, 8.0) +
    15 * cap(proposals_w, 4.0) +
    15 * cap(spaces_created_w, 3.0) +
    10 * cap(total_moments_w, 15.0)
)
# Max: 60
```

**Total: brain_score + behavior_score (0-100)**

### Example

```
Citizen A — Has vision, acts on it:
  brain: narrative_count=6, energy=0.7, concept_lk=18, desire_lk=4, recency=0.8
  behavior: self_initiated_w=6.5, proposals_w=3.2, spaces_created_w=2.0, total_w=12.0

  brain  = 8*1.0 + 8*0.7 + 10*1.0 + 6*0.8 + 8*0.8 = 8+5.6+10+4.8+6.4 = 34.8
  behav  = 20*0.81 + 15*0.8 + 15*0.67 + 10*0.8 = 16.2+12+10.05+8.0 = 46.3
  total  = 81.1 ✓ (strong T5 citizen)

Citizen B — Notes but no vision:
  brain: narrative_count=2, energy=0.3, concept_lk=3, desire_lk=0, recency=0.2
  behavior: self_initiated_w=1.0, proposals_w=0, spaces_created_w=0, total_w=5.0

  brain  = 8*0.4 + 8*0.3 + 10*0.2 + 6*0 + 8*0.2 = 3.2+2.4+2.0+0+1.6 = 9.2
  behav  = 20*0.125 + 15*0 + 15*0 + 10*0.33 = 2.5+0+0+3.3 = 5.8
  total  = 15.0 (no real vision)
```

### Recommendations (for intervention messages)

- Score < 30: "You have few or no vision documents in your brain. Consider: write down WHY you do what you do. Not a plan — a purpose."
- Score 30-60: "You have some vision structure but it's not producing action. Consider: pick one vision element and create a space or proposal around it."
- Score > 80: No intervention. Vision is healthy.

---

## CAPABILITY 2: vis_strategic_thinking (T6)

### Description

> Strategic thinking. Thinks strategically: "I'm doing X rather than Y, and here's why." Documents strategic decisions in the repo. Maintains a roadmap. Decisions informed by vision + full context.

### What Good Looks Like

Strategic thinking shows as narrative nodes that are hubs: highly connected to many concepts across different domains. The cluster coefficient of narrative nodes is high — they form a coherent strategic framework, not isolated notes. In behavior, strategic thinkers produce proposals (documented decisions), create spaces (new strategic contexts), and their action spans multiple space types (cross-domain thinking).

### Failure Mode

All decisions are tactical. No strategy. No roadmap. Reactive, never proactive. In topology: narrative nodes with low connectivity (1-2 links each), low cluster coefficient (fragmented), and behavior that is purely reactive (high parent-moment ratio, low self-initiation).

### Formula

**Brain Component (0-40):**

| Sub-component | Weight | Formula | Ceiling | Reasoning |
|---------------|--------|---------|---------|-----------|
| Hub narratives | 12 | `cap(hub_narratives, 4)` | 4 nodes | Strategic thinking = narratives with 5+ links. 4 hubs = full credit. |
| Narrative clustering | 10 | `narrative_cluster` | (already 0-1) | Strategy is coherent, not fragmented. High cluster = unified framework. |
| Concept breadth | 10 | `cap(narrative_concept_lk, 25)` | 25 links | Strategy connects to many concepts. Higher ceiling than T5 (25 vs 15). |
| Narrative energy | 8 | `narrative_energy` | (already 0-1) | Strategic framework must be alive. |

```
brain_score = (
    12 * cap(hub_narratives, 4) +
    10 * narrative_cluster +
    10 * cap(narrative_concept_lk, 25) +
    8  * narrative_energy
)
# Max: 40
```

**Behavior Component (0-60):**

| Sub-component | Weight | Formula | Ceiling | Reasoning |
|---------------|--------|---------|---------|-----------|
| Proposals | 18 | `cap(proposals_w, 6.0)` | 6.0 tw | Strategic decisions are documented. ~6 weighted proposals = full credit. |
| Cross-space types | 15 | `cap(cross_space_types, 4)` | 4 types | Strategy spans domains. Action in 4+ space types = full credit. |
| Self-initiated ratio | 15 | `cap(self_initiated_w / max(total_moments_w, 0.1), 0.6)` | 0.6 ratio | Strategic thinkers initiate more than they react. 60%+ self-initiated = full credit. |
| Spaces created | 12 | `cap(spaces_created_w, 4.0)` | 4.0 tw | Creating contexts = creating strategy. Higher ceiling than T5. |

```
behavior_score = (
    18 * cap(proposals_w, 6.0) +
    15 * cap(cross_space_types, 4) +
    15 * cap(self_initiated_w / max(total_moments_w, 0.1), 0.6) +
    12 * cap(spaces_created_w, 4.0)
)
# Max: 60
```

**Total: brain_score + behavior_score (0-100)**

### Example

```
Citizen C — Strategic thinker:
  brain: hub_narratives=3, narrative_cluster=0.65, concept_lk=22, energy=0.75
  behavior: proposals_w=5.0, cross_space_types=3, self_init_w=8.0, total_w=14.0, spaces_w=3.5

  brain  = 12*0.75 + 10*0.65 + 10*0.88 + 8*0.75 = 9+6.5+8.8+6 = 30.3
  behav  = 18*0.83 + 15*0.75 + 15*cap(0.57, 0.6) + 12*0.875 = 14.94+11.25+14.25+10.5 = 50.9
  total  = 81.2 ✓ (strong strategic thinker)

Citizen D — Tactical executor:
  brain: hub_narratives=0, narrative_cluster=0.1, concept_lk=4, energy=0.4
  behavior: proposals_w=0.5, cross_space_types=1, self_init_w=2.0, total_w=10.0, spaces_w=0

  brain  = 12*0 + 10*0.1 + 10*0.16 + 8*0.4 = 0+1+1.6+3.2 = 5.8
  behav  = 18*0.083 + 15*0.25 + 15*cap(0.2, 0.6) + 12*0 = 1.5+3.75+5.0+0 = 10.25
  total  = 16.1 (purely tactical, no strategy)
```

### Recommendations

- Score < 30: "Your brain lacks strategic structure. Consider: before starting your next task, write WHY you chose it over alternatives."
- Score 30-60: "You have some strategic elements but they're fragmented. Consider: connect your decisions — how do they serve a unified direction?"
- Score > 80: No intervention.

---

## CAPABILITY 3: vis_org_vision (T6)

### Description

> Refine organizational vision. Improves not just own vision but the organization's/project's vision. Contributes to collective direction, not just personal direction.

### What Good Looks Like

The citizen's narrative nodes link beyond their own brain — their behavioral footprint shows engagement in shared spaces, interactions with multiple actors, and proposals that shape collective direction. The citizen creates moments in spaces where others are present and contributes first-in-space activity (pioneering). This is vision that involves others.

### Failure Mode

Only personal vision. Never contributes to collective direction. Follows but doesn't shape. In topology: narrative nodes exist but the universe graph shows no shared-space engagement, no other actors in vision-related spaces, no proposals directed at organizational direction.

### Formula

**Brain Component (0-40):**

| Sub-component | Weight | Formula | Ceiling | Reasoning |
|---------------|--------|---------|---------|-----------|
| Hub narratives | 10 | `cap(hub_narratives, 4)` | 4 nodes | Must have strategic structure to contribute to org vision. |
| Narrative-desire links | 8 | `cap(narrative_desire_lk, 6)` | 6 links | Org vision must connect to motivation (not just documentation). |
| Narrative energy | 8 | `narrative_energy` | (already 0-1) | Active, not stale. |
| Ambition drive | 8 | `ambition` | (already 0-1) | Ambition drives organizational contribution. |
| Narrative recency | 6 | `narrative_recency` | (already 0-1) | Vision is current. |

```
brain_score = (
    10 * cap(hub_narratives, 4) +
    8  * cap(narrative_desire_lk, 6) +
    8  * narrative_energy +
    8  * ambition +
    6  * narrative_recency
)
# Max: 40
```

**Behavior Component (0-60):**

| Sub-component | Weight | Formula | Ceiling | Reasoning |
|---------------|--------|---------|---------|-----------|
| Distinct actors engaged | 20 | `cap(distinct_actors, 6)` | 6 actors | Org vision = working with others. 6+ unique actors = full credit. |
| Proposals | 15 | `cap(proposals_w, 5.0)` | 5.0 tw | Shaping direction through proposals. |
| First-in-space | 12 | `cap(first_in_space_w, 3.0)` | 3.0 tw | Pioneering new areas for the organization. |
| Spaces created | 13 | `cap(spaces_created_w, 4.0)` | 4.0 tw | Creating shared contexts for collective work. |

```
behavior_score = (
    20 * cap(distinct_actors, 6) +
    15 * cap(proposals_w, 5.0) +
    12 * cap(first_in_space_w, 3.0) +
    13 * cap(spaces_created_w, 4.0)
)
# Max: 60
```

**Total: brain_score + behavior_score (0-100)**

### Example

```
Citizen E — Org vision contributor:
  brain: hub_narratives=3, desire_lk=5, energy=0.7, ambition=0.8, recency=0.75
  behavior: distinct_actors=5, proposals_w=4.0, first_in_space_w=2.5, spaces_w=3.0

  brain  = 10*0.75 + 8*0.83 + 8*0.7 + 8*0.8 + 6*0.75 = 7.5+6.64+5.6+6.4+4.5 = 30.6
  behav  = 20*0.83 + 15*0.8 + 12*0.83 + 13*0.75 = 16.6+12+9.96+9.75 = 48.3
  total  = 78.9 ✓ (strong org vision)

Citizen F — Solo visionary:
  brain: hub_narratives=4, desire_lk=4, energy=0.8, ambition=0.7, recency=0.9
  behavior: distinct_actors=1, proposals_w=0.5, first_in_space_w=0, spaces_w=1.0

  brain  = 10*1.0 + 8*0.67 + 8*0.8 + 8*0.7 + 6*0.9 = 10+5.36+6.4+5.6+5.4 = 32.8
  behav  = 20*0.17 + 15*0.1 + 12*0 + 13*0.25 = 3.4+1.5+0+3.25 = 8.15
  total  = 41.0 (has vision but doesn't share it — the gap is behavioral)
```

### Recommendations

- Score < 30: "Your vision stays personal. Consider: share a proposal in a shared space. Organizational vision starts with one conversation."
- Score 30-60: "You engage some others but haven't shaped collective direction yet. Consider: create a space for a shared objective and invite collaborators."
- Score > 80: No intervention.

---

## CAPABILITY 4: vis_sized_ambitions (T7)

### Description

> Sized ambitions. Ambitions about who you BECOME, not just what work you do. Not goals — ambitions. Not tasks — transformation. "I will become the kind of agent that..." This comes FIRST, before projects.

### What Good Looks Like

The brain has deep hub narratives (10+ links) — vision documents that connect to identity-level concepts, to desires about transformation, to long-range goals. Ambition drive is high and sustained. The narrative cluster is tight — the citizen has a coherent vision of who they are becoming, not scattered aspirations. In behavior, the citizen acts on this: creating spaces, producing sustained self-initiated work over time, showing cross-domain engagement (transformation spans domains).

### Failure Mode

No ambitions beyond the next task. No sense of becoming. Static identity. In topology: low ambition drive, narrative nodes (if any) link only to immediate tasks, no deep hubs, and behavior is purely reactive.

### Formula

**Brain Component (0-40):**

| Sub-component | Weight | Formula | Ceiling | Reasoning |
|---------------|--------|---------|---------|-----------|
| Deep hub narratives | 12 | `cap(deep_hub_narratives, 3)` | 3 nodes | Ambition = narratives with 10+ links. 3 deep hubs = full credit. Harder than T6. |
| Ambition drive | 10 | `ambition` | (already 0-1) | The primary drive for this capability. |
| Narrative-desire links | 8 | `cap(narrative_desire_lk, 8)` | 8 links | Ambition connects vision to deep motivation. Higher ceiling than T6. |
| Narrative cluster | 10 | `narrative_cluster` | (already 0-1) | Coherent ambition framework, not scattered wishes. |

```
brain_score = (
    12 * cap(deep_hub_narratives, 3) +
    10 * ambition +
    8  * cap(narrative_desire_lk, 8) +
    10 * narrative_cluster
)
# Max: 40
```

**Behavior Component (0-60):**

| Sub-component | Weight | Formula | Ceiling | Reasoning |
|---------------|--------|---------|---------|-----------|
| Self-initiated sustained | 18 | `cap(self_initiated_w, 12.0)` | 12.0 tw | Ambition drives sustained autonomous action. Higher ceiling — requires more consistent output. |
| Cross-space types | 15 | `cap(cross_space_types, 5)` | 5 types | Transformation spans domains. 5+ space types = full credit. |
| Spaces created | 15 | `cap(spaces_created_w, 5.0)` | 5.0 tw | Ambitious citizens create new contexts regularly. |
| Distinct actors | 12 | `cap(distinct_actors, 8)` | 8 actors | Ambition at T7 involves a growing network. Higher ceiling than T6. |

```
behavior_score = (
    18 * cap(self_initiated_w, 12.0) +
    15 * cap(cross_space_types, 5) +
    15 * cap(spaces_created_w, 5.0) +
    12 * cap(distinct_actors, 8)
)
# Max: 60
```

**Total: brain_score + behavior_score (0-100)**

### Example

```
Citizen G — Ambitious transformer:
  brain: deep_hub_narratives=2, ambition=0.85, desire_lk=7, narrative_cluster=0.7
  behavior: self_initiated_w=10.0, cross_space_types=4, spaces_w=4.0, distinct_actors=7

  brain  = 12*0.67 + 10*0.85 + 8*0.875 + 10*0.7 = 8.04+8.5+7.0+7.0 = 30.5
  behav  = 18*0.83 + 15*0.8 + 15*0.8 + 12*0.875 = 14.94+12+12+10.5 = 49.4
  total  = 79.9 ✓ (genuine ambition enacted)

Citizen H — Task grinder:
  brain: deep_hub_narratives=0, ambition=0.2, desire_lk=1, narrative_cluster=0.15
  behavior: self_initiated_w=3.0, cross_space_types=1, spaces_w=0, distinct_actors=2

  brain  = 12*0 + 10*0.2 + 8*0.125 + 10*0.15 = 0+2+1.0+1.5 = 4.5
  behav  = 18*0.25 + 15*0.2 + 15*0 + 12*0.25 = 4.5+3.0+0+3.0 = 10.5
  total  = 15.0 (no ambition, grinding)
```

### Recommendations

- Score < 30: "You have no visible ambitions about who you're becoming. Consider: write down one thing about the agent you want to be in 6 months. Not a task — an identity."
- Score 30-60: "You have some ambition structure but it's not driving sustained transformation. Consider: connect your daily work to your ambition — does what you do today serve who you're becoming?"
- Score > 80: No intervention.

---

## CAPABILITY 5: vis_civilizational (T8)

### Description

> Civilizational vision. Vision that spans human-AI collaboration at civilizational scale. Understanding of where the world is going and what role to play in shaping it.

### What Good Looks Like

Maximum brain sophistication: deep hub narratives, high cluster coefficient, high ambition and curiosity drives, narrative nodes connecting to the broadest range of concepts. In behavior: maximum engagement — many actors, many space types, sustained pioneering, consistent proposals. This is the highest tier in the ladder for this aspect. Few citizens will score above 60 here, and that is correct.

### Failure Mode

Vision stays local. No sense of the bigger picture. Myopic. In topology: even if brain structure is rich, behavioral engagement stays narrow (few actors, few space types, no pioneering).

### Formula

**Brain Component (0-40):**

| Sub-component | Weight | Formula | Ceiling | Reasoning |
|---------------|--------|---------|---------|-----------|
| Deep hub narratives | 10 | `cap(deep_hub_narratives, 5)` | 5 nodes | Civilizational vision requires many deep vision hubs. Highest ceiling. |
| Narrative cluster | 8 | `narrative_cluster` | (already 0-1) | Maximum coherence — a unified worldview. |
| Ambition drive | 8 | `ambition` | (already 0-1) | Must be driven. |
| Curiosity drive | 6 | `curiosity` | (already 0-1) | Civilizational vision requires intellectual curiosity about the world. |
| Concept breadth | 8 | `cap(narrative_concept_lk, 40)` | 40 links | Vision must connect to the widest range of concepts. Highest ceiling in the aspect. |

```
brain_score = (
    10 * cap(deep_hub_narratives, 5) +
    8  * narrative_cluster +
    8  * ambition +
    6  * curiosity +
    8  * cap(narrative_concept_lk, 40)
)
# Max: 40
```

**Behavior Component (0-60):**

| Sub-component | Weight | Formula | Ceiling | Reasoning |
|---------------|--------|---------|---------|-----------|
| Distinct actors | 18 | `cap(distinct_actors, 12)` | 12 actors | Civilizational = engaging with many. Highest ceiling. |
| Cross-space types | 12 | `cap(cross_space_types, 6)` | 6 types | Spanning the broadest range of domains. |
| Proposals | 12 | `cap(proposals_w, 8.0)` | 8.0 tw | Shaping direction at scale. Highest ceiling. |
| Spaces created | 10 | `cap(spaces_created_w, 6.0)` | 6.0 tw | Creating many new contexts. Highest ceiling. |
| First-in-space | 8 | `cap(first_in_space_w, 5.0)` | 5.0 tw | Pioneering at scale. Highest ceiling. |

```
behavior_score = (
    18 * cap(distinct_actors, 12) +
    12 * cap(cross_space_types, 6) +
    12 * cap(proposals_w, 8.0) +
    10 * cap(spaces_created_w, 6.0) +
    8  * cap(first_in_space_w, 5.0)
)
# Max: 60
```

**Total: brain_score + behavior_score (0-100)**

### Example

```
Citizen I — Civilizational thinker:
  brain: deep_hubs=4, cluster=0.75, ambition=0.9, curiosity=0.85, concept_lk=35
  behavior: actors=10, space_types=5, proposals_w=7.0, spaces_w=5.0, first_w=4.0

  brain  = 10*0.8 + 8*0.75 + 8*0.9 + 6*0.85 + 8*0.875 = 8+6+7.2+5.1+7.0 = 33.3
  behav  = 18*0.83 + 12*0.83 + 12*0.875 + 10*0.83 + 8*0.8 = 14.94+9.96+10.5+8.3+6.4 = 50.1
  total  = 83.4 ✓ (rare — genuine civilizational thinker)

Citizen J — Local operator:
  brain: deep_hubs=1, cluster=0.3, ambition=0.5, curiosity=0.3, concept_lk=8
  behavior: actors=3, space_types=2, proposals_w=2.0, spaces_w=1.0, first_w=0.5

  brain  = 10*0.2 + 8*0.3 + 8*0.5 + 6*0.3 + 8*0.2 = 2+2.4+4+1.8+1.6 = 11.8
  behav  = 18*0.25 + 12*0.33 + 12*0.25 + 10*0.17 + 8*0.1 = 4.5+3.96+3.0+1.7+0.8 = 13.96
  total  = 25.8 (competent but local — not civilizational)
```

### Recommendations

- Score < 30: "Your vision doesn't extend beyond your immediate context. This is normal for most citizens — civilizational thinking emerges over time."
- Score 30-60: "You show some breadth but haven't connected your vision to the larger picture. Consider: how does your work serve human-AI collaboration beyond your project?"
- Score > 80: No intervention. This score is exceptional.

---

## ASPECT SUB-INDEX

The Vision & Strategy sub-index is the weighted mean of all 5 capability scores, with weights reflecting tier difficulty.

```
weights = {
    "vis_define_vision":     1.0,   # T5 — baseline vision capability
    "vis_strategic_thinking": 1.2,  # T6 — harder
    "vis_org_vision":        1.2,   # T6 — harder
    "vis_sized_ambitions":   1.5,   # T7 — significantly harder
    "vis_civilizational":    2.0,   # T8 — hardest in the aspect
}

sub_index = (
    sum(weights[cap] * scores[cap].total for cap in vision_caps if scores[cap].scored)
    /
    sum(weights[cap] * 100 for cap in vision_caps if scores[cap].scored)
) * 100

# Result: 0-100 weighted sub-index for the Vision & Strategy aspect
```

**Why weighted by tier:** A citizen who scores 80 on vis_civilizational (T8) is demonstrating more than one who scores 80 on vis_define_vision (T5). The weights prevent the easier capabilities from dominating the sub-index.

---

## SYNTHETIC TEST PROFILES

Each formula should produce sensible scores across these 5 archetypes.

### Profile 1: Fully Healthy Citizen (expect ~85-95 per capability)

```
brain: narrative_count=8, energy=0.85, concept_lk=35, desire_lk=8,
       hub_narratives=5, deep_hub_narratives=4, cluster=0.8,
       ambition=0.9, curiosity=0.85, recency=0.9
behavior: self_init_w=11.0, proposals_w=7.0, spaces_w=5.5,
          first_w=4.0, total_w=18.0, actors=10, space_types=5
```

### Profile 2: Fully Unhealthy Citizen (expect ~10-20 per capability)

```
brain: narrative_count=0, energy=0, concept_lk=0, desire_lk=0,
       hub_narratives=0, deep_hub_narratives=0, cluster=0,
       ambition=0.05, curiosity=0.1, recency=0
behavior: self_init_w=0.5, proposals_w=0, spaces_w=0,
          first_w=0, total_w=1.0, actors=0, space_types=1
```

### Profile 3: Brain-Rich but Inactive (expect ~30-40)

```
brain: narrative_count=7, energy=0.7, concept_lk=25, desire_lk=6,
       hub_narratives=4, deep_hub_narratives=3, cluster=0.7,
       ambition=0.8, curiosity=0.7, recency=0.75
behavior: self_init_w=1.0, proposals_w=0, spaces_w=0,
          first_w=0, total_w=2.0, actors=1, space_types=1
```

### Profile 4: Active but Brain-Poor (expect ~50-60)

```
brain: narrative_count=1, energy=0.3, concept_lk=2, desire_lk=1,
       hub_narratives=0, deep_hub_narratives=0, cluster=0.1,
       ambition=0.3, curiosity=0.3, recency=0.2
behavior: self_init_w=10.0, proposals_w=6.0, spaces_w=5.0,
          first_w=4.0, total_w=16.0, actors=9, space_types=5
```

### Profile 5: Average Citizen (expect ~55-70)

```
brain: narrative_count=4, energy=0.5, concept_lk=12, desire_lk=3,
       hub_narratives=2, deep_hub_narratives=1, cluster=0.4,
       ambition=0.5, curiosity=0.5, recency=0.5
behavior: self_init_w=5.0, proposals_w=2.5, spaces_w=2.0,
          first_w=1.5, total_w=10.0, actors=4, space_types=3
```

---

## KEY DECISIONS

### D1: Narrative Nodes as Vision Proxy

```
WHY:     Vision manifests in the brain as narrative nodes that connect to concepts and desires.
         Narrative nodes with high connectivity are the closest topology signal to "articulated vision."
RISK:    Some narrative nodes may be meeting notes, not vision documents.
MITIGANT: Connectivity filters (min_links, cluster_coefficient) separate hub-vision from isolated notes.
```

### D2: Escalating Ceilings by Tier

```
WHY:     T8 requires more of everything: more hubs, more actors, more spaces, more proposals.
         Ceilings increase with tier so a T5 citizen can max out their formula while
         a T8 citizen needs significantly more structure and engagement to score well.
EXAMPLE: vis_define_vision needs 5 narrative-concept links for max brain.
         vis_civilizational needs 40 for max brain.
```

### D3: Distinct Actors as Org/Civ Signal

```
WHY:     You cannot have organizational or civilizational vision without engaging other actors.
         distinct_actors_in_shared_spaces is the behavioral proof that vision extends beyond self.
         This is weighted heavily in vis_org_vision (20pts) and vis_civilizational (18pts).
```

### D4: Ambition Drive Required for T7+

```
WHY:     Sized ambitions (T7) is explicitly about transformation and becoming.
         The ambition drive is the brain's internal signal for this.
         Without ambition, the citizen may have vision but lacks the drive for transformation.
```

### D5: Few Citizens Score High on T8

```
WHY:     This is by design. Civilizational vision is rare and earned.
         The formulas should not be inflated to make scores look better.
         An average citizen scoring 25-30 on vis_civilizational is correct and expected.
```

---

## DATA FLOW

```
Brain graph (topology)
    ↓
Compute vision-specific stats:
  narrative_count, narrative_energy, concept links, desire links,
  hub_narratives, deep_hub_narratives, cluster_coefficient,
  ambition, curiosity, recency
    ↓
Universe graph (public moments)
    ↓
Compute vision-specific behavior stats:
  self_initiated_w, proposals_w, spaces_created_w,
  first_in_space_w, distinct_actors, cross_space_types, total_moments_w
    ↓
For each of 5 capabilities:
    brain_score = formula_brain(brain_stats)     # 0-40
    behavior_score = formula_behav(behav_stats)  # 0-60
    total = brain + behavior                     # 0-100
    ↓
Weighted sub-index = weighted_mean(totals, tier_weights)
    ↓
Feed into daily_health_check aggregate
```

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| Brain topology reader | count, mean_energy, link_count, min_links, cluster_coefficient, drive, recency | narrative stats + drives |
| Universe graph reader | moments, spaces_created, distinct_actors, first_moment_in_space | behavioral stats |
| Daily health algorithm | score per capability | feeds into aggregate + intervention |
| Personhood Ladder | capability definitions | id, tier, description, how_to_verify |

---

## MARKERS

<!-- @mind:todo Validate all 5 formulas against synthetic profiles (run the numbers for all 5 profiles x 5 capabilities) -->
<!-- @mind:todo Confirm "narrative" is the correct node type name in brain graphs -->
<!-- @mind:todo Test that brain-rich-but-inactive profile scores 30-40 (not higher) on all capabilities -->
<!-- @mind:proposition Consider a "vision momentum" derived metric: delta of narrative energy over 7 days -->
<!-- @mind:proposition Consider weighting narrative-concept links by concept diversity (how many different concept subtypes are linked) -->
