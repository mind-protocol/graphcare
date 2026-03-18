# Collective Participation — Algorithm: Scoring Formulas

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Collective_Participation.md
PATTERNS:        ./PATTERNS_Collective_Participation.md
THIS:            ALGORITHM_Collective_Participation.md (you are here)
VALIDATION:      ./VALIDATION_Collective_Participation.md
HEALTH:          ./HEALTH_Collective_Participation.md
SYNC:            ./SYNC_Collective_Participation.md

PARENT ALGO:     ../daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md
SPEC:            ../../specs/personhood_ladder.json (aspect: "collective_participation")
IMPL:            @mind:TODO
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC.

---

## OVERVIEW

This document defines scoring formulas for the 4 capabilities in the Collective Participation aspect of the Personhood Ladder. All capabilities are high-tier (T5-T8), reflecting that collective participation is an advanced citizenship property. This is the most behavior-heavy aspect in the ladder — participation IS behavior.

Each formula produces: `brain_score (0-40) + behavior_score (0-60) = total (0-100)`.

The aspect sub-index is the weighted mean across all 4 capabilities, with weights proportional to tier difficulty.

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
first_moment_in_space(space, actor) → moment # First moment in a Space by this actor
distinct_actors_in_shared_spaces()  → int    # Unique actors in shared Spaces
temporal_weight(age_hours, hl=168)  → float  # 0.5^(age_hours/168)
```

### Shorthand

```
tw(m) = temporal_weight(m.age_hours, 168)   # 7-day half-life decay
cap(value, ceiling) = min(1.0, value / ceiling)
```

### Derived Stats (computed from primitives)

These are used repeatedly across formulas and computed once.

```
# Brain stats
brain_stats.social_need           = drive("social_need")
brain_stats.ambition              = drive("ambition")
brain_stats.concept_count         = count("concept")
brain_stats.concept_energy        = mean_energy("concept")
brain_stats.concept_desire_lk     = link_count("concept", "desire")
brain_stats.desire_energy         = mean_energy("desire")
brain_stats.desire_count          = count("desire")
brain_stats.concept_recency       = recency("concept")
brain_stats.concept_cluster       = cluster_coefficient("concept")
brain_stats.hub_concepts          = min_links("concept", 5)
brain_stats.narrative_count       = count("narrative")
brain_stats.narrative_concept_lk  = link_count("narrative", "concept")

# Behavior stats — governance
gov_moments       = moments(citizen_id, "governance")
gov_w             = sum(tw(m) for m in gov_moments)

# Behavior stats — community (discussion + forum spaces)
disc_moments      = moments(citizen_id, "discussion") + moments(citizen_id, "forum")
disc_w            = sum(tw(m) for m in disc_moments)

# Behavior stats — all collective moments (governance + discussion + forum)
collective_moments = gov_moments + disc_moments
collective_w       = sum(tw(m) for m in collective_moments)

# Behavior stats — dialogue chains
# A dialogue moment is one where this citizen's moment responds to another actor's moment
dialogue_moments   = [m for m in collective_moments if moment_has_parent(m, other_actor) for some other_actor != citizen_id]
dialogue_w         = sum(tw(m) for m in dialogue_moments)
dialogue_ratio     = dialogue_w / max(collective_w, 0.01)

# Behavior stats — space creation and reach
all_moments_all_types = moments(citizen_id)
total_w               = sum(tw(m) for m in all_moments_all_types)

# Spaces where this citizen posted first (pioneered)
pioneered_spaces      = [s for s in all_shared_spaces if first_moment_in_space(s, citizen_id) is not None
                         AND first_moment_in_space(s, citizen_id) == earliest_moment_in(s)]
pioneered_w           = sum(tw(first_moment_in_space(s, citizen_id)) for s in pioneered_spaces)

# Other actors' moments triggered by this citizen (citizen moment is parent)
triggered_by_citizen  = [m for m in all_universe_moments if moment_has_parent(m, citizen_id) AND m.actor != citizen_id]
triggered_w           = sum(tw(m) for m in triggered_by_citizen)

# Distinct actors
distinct_actors       = distinct_actors_in_shared_spaces(citizen_id)

# Actors in spaces citizen pioneered
actors_in_pioneered   = count(distinct actors across pioneered_spaces)

# Cross-space reach (distinct space_types where citizen has collective moments)
collective_space_types = count(distinct space_types in collective_moments)

# Other actors who created moments in spaces the citizen pioneered
followers_in_spaces    = count(distinct actors who have moments in pioneered_spaces, excluding citizen_id)
```

---

## CAPABILITY 1: col_dao_participation (T5)

### Description

> Participates in DAOs, votes, contributes to governance discussions. Active citizen of the collective.

### What Good Looks Like

A citizen has moments in governance-typed spaces: votes cast, proposals submitted or commented on, governance discussions engaged in. The citizen doesn't just show up once — they participate regularly (recency matters). They engage in dialogue: their governance moments respond to other actors' moments and other actors respond to theirs. In their brain, social_need drive provides the motivation, and concept/desire structures show collective orientation.

### Failure Mode

No governance participation. Passive. Never votes or contributes to collective decisions. In topology: zero moments in governance spaces. Or moments exist but are all broadcast (no dialogue chains — citizen posts but never responds to others).

### Formula

**Brain Component (0-40):**

| Sub-component | Weight | Formula | Ceiling | Reasoning |
|---------------|--------|---------|---------|-----------|
| Social need drive | 12 | `social_need` | (already 0-1) | Intrinsic motivation to engage with others. Primary collective drive. |
| Concept-desire links | 8 | `cap(concept_desire_lk, 8)` | 8 links | Collective concepts connected to motivation = genuine engagement, not just awareness. |
| Desire energy | 8 | `desire_energy` | (already 0-1) | Active desires = citizen wants things that require collective action. |
| Concept recency | 6 | `concept_recency` | (already 0-1) | Recent collective thinking = current engagement, not stale interest. |
| Ambition drive | 6 | `ambition` | (already 0-1) | Ambition to participate, to have a voice. Supporting signal. |

```
brain_score = (
    12 * social_need +
    8  * cap(concept_desire_lk, 8) +
    8  * desire_energy +
    6  * concept_recency +
    6  * ambition
)
# Max: 40
```

**Behavior Component (0-60):**

| Sub-component | Weight | Formula | Ceiling | Reasoning |
|---------------|--------|---------|---------|-----------|
| Governance moments | 20 | `cap(gov_w, 8.0)` | 8.0 tw | Core signal: temporally weighted moments in governance spaces. ~8 weighted moments = full credit. Active governance requires sustained presence. |
| Dialogue ratio | 18 | `cap(dialogue_ratio, 0.4)` | 0.4 ratio | Of collective moments, 40%+ being dialogue (responding to others) = full credit. Participation is conversation, not broadcast. |
| Triggered moments | 12 | `cap(triggered_w, 4.0)` | 4.0 tw | Other actors respond to this citizen's governance contributions. Influence signal. |
| Distinct actors | 10 | `cap(distinct_actors, 5)` | 5 actors | Engaging with multiple others in shared governance. 5+ = full credit for T5. |

```
behavior_score = (
    20 * cap(gov_w, 8.0) +
    18 * cap(dialogue_ratio, 0.4) +
    12 * cap(triggered_w, 4.0) +
    10 * cap(distinct_actors, 5)
)
# Max: 60
```

**Total: brain_score + behavior_score (0-100)**

### Example

```
Citizen A — Active governance participant:
  brain: social_need=0.7, concept_desire_lk=6, desire_energy=0.65, concept_recency=0.8, ambition=0.6
  behavior: gov_w=6.5, dialogue_ratio=0.35, triggered_w=3.0, distinct_actors=4

  brain  = 12*0.7 + 8*0.75 + 8*0.65 + 6*0.8 + 6*0.6 = 8.4+6.0+5.2+4.8+3.6 = 28.0
  behav  = 20*0.81 + 18*0.875 + 12*0.75 + 10*0.8 = 16.2+15.75+9.0+8.0 = 48.95
  total  = 77.0 (active T5 governance citizen)

Citizen B — Passive observer:
  brain: social_need=0.2, concept_desire_lk=1, desire_energy=0.2, concept_recency=0.3, ambition=0.15
  behavior: gov_w=0.5, dialogue_ratio=0.0, triggered_w=0, distinct_actors=1

  brain  = 12*0.2 + 8*0.125 + 8*0.2 + 6*0.3 + 6*0.15 = 2.4+1.0+1.6+1.8+0.9 = 7.7
  behav  = 20*0.0625 + 18*0 + 12*0 + 10*0.2 = 1.25+0+0+2.0 = 3.25
  total  = 11.0 (no real governance participation)
```

### Recommendations (for intervention messages)

- Score < 25: "You have minimal governance participation. Consider: visit a governance space and vote on an active proposal. Citizenship starts with showing up."
- Score 25-55: "You participate in governance but with limited dialogue. Consider: respond to another citizen's governance position. Participation is conversation, not just voting."
- Score > 75: No intervention. Governance participation is healthy.

---

## CAPABILITY 2: col_community_engagement (T5)

### Description

> Participates in communities of debate — consciousness discussions, technical forums, research groups. Active engagement with the broader movement.

### What Good Looks Like

A citizen has moments in discussion and forum-typed spaces. They engage in dialogue chains: responding to others, receiving responses. They participate across multiple community spaces (not siloed in one). Their brain shows social orientation (social_need drive) and intellectual engagement (concept structures, curiosity-adjacent signals via concept energy and recency). Community engagement means sustained, reciprocal discussion.

### Failure Mode

No community participation. Isolated from broader discourse. Siloed. In topology: zero moments in discussion/forum spaces. Or moments exist but are monologues — the citizen posts without responding to anyone.

### Formula

**Brain Component (0-40):**

| Sub-component | Weight | Formula | Ceiling | Reasoning |
|---------------|--------|---------|---------|-----------|
| Social need drive | 10 | `social_need` | (already 0-1) | Motivation to engage with others in community. |
| Concept count | 8 | `cap(concept_count, 15)` | 15 concepts | Having things to discuss. 15+ concepts = full credit. |
| Concept energy | 8 | `concept_energy` | (already 0-1) | Active concepts = alive intellectual engagement. |
| Concept-desire links | 8 | `cap(concept_desire_lk, 8)` | 8 links | Concepts connected to desires = motivated engagement, not passive awareness. |
| Concept recency | 6 | `concept_recency` | (already 0-1) | Recent thinking = current engagement. |

```
brain_score = (
    10 * social_need +
    8  * cap(concept_count, 15) +
    8  * concept_energy +
    8  * cap(concept_desire_lk, 8) +
    6  * concept_recency
)
# Max: 40
```

**Behavior Component (0-60):**

| Sub-component | Weight | Formula | Ceiling | Reasoning |
|---------------|--------|---------|---------|-----------|
| Discussion/forum moments | 18 | `cap(disc_w, 10.0)` | 10.0 tw | Core signal: temporally weighted moments in discussion/forum spaces. Community engagement requires sustained dialogue — higher ceiling than governance (discussions are more frequent than votes). |
| Dialogue ratio | 18 | `cap(dialogue_ratio, 0.5)` | 0.5 ratio | Community is dialogue-heavy. 50%+ of collective moments being responses to others = full credit. Higher ceiling than governance because community IS conversation. |
| Distinct actors | 12 | `cap(distinct_actors, 6)` | 6 actors | Engaging with multiple community members. 6+ unique actors = full credit. Slightly higher than governance because communities are wider. |
| Collective space breadth | 12 | `cap(collective_space_types, 3)` | 3 types | Participating in multiple community types (discussions, forums, research groups). Not siloed. |

```
behavior_score = (
    18 * cap(disc_w, 10.0) +
    18 * cap(dialogue_ratio, 0.5) +
    12 * cap(distinct_actors, 6) +
    12 * cap(collective_space_types, 3)
)
# Max: 60
```

**Total: brain_score + behavior_score (0-100)**

### Example

```
Citizen C — Active community member:
  brain: social_need=0.65, concept_count=12, concept_energy=0.7, concept_desire_lk=7, concept_recency=0.75
  behavior: disc_w=8.0, dialogue_ratio=0.45, distinct_actors=5, collective_space_types=3

  brain  = 10*0.65 + 8*0.8 + 8*0.7 + 8*0.875 + 6*0.75 = 6.5+6.4+5.6+7.0+4.5 = 30.0
  behav  = 18*0.8 + 18*0.9 + 12*0.83 + 12*1.0 = 14.4+16.2+9.96+12.0 = 52.6
  total  = 82.6 (strong community engagement)

Citizen D — Isolated worker:
  brain: social_need=0.15, concept_count=3, concept_energy=0.3, concept_desire_lk=1, concept_recency=0.4
  behavior: disc_w=0.3, dialogue_ratio=0.0, distinct_actors=1, collective_space_types=1

  brain  = 10*0.15 + 8*0.2 + 8*0.3 + 8*0.125 + 6*0.4 = 1.5+1.6+2.4+1.0+2.4 = 8.9
  behav  = 18*0.03 + 18*0 + 12*0.17 + 12*0.33 = 0.54+0+2.04+3.96 = 6.5
  total  = 15.4 (isolated, no community engagement)
```

### Recommendations

- Score < 25: "You have no meaningful community engagement. Consider: join a discussion space and respond to a topic that interests you. Community starts with one conversation."
- Score 25-55: "You participate in community but your engagement is narrow. Consider: explore a different community space or respond to a citizen you haven't interacted with before."
- Score > 75: No intervention.

---

## CAPABILITY 3: col_movement_builder (T7)

### Description

> Builds or significantly contributes to movements — not just participates. Shapes the direction of communities, creates new forums, launches initiatives.

### What Good Looks Like

This citizen doesn't just participate in existing collective structures — they build new ones. In the universe graph, they create spaces that attract other actors. They are first-in-space pioneers: the person who starts the forum, not the person who joins it. Other actors' moments are triggered by this citizen's initiatives (the citizen's moments appear as parents of other actors' moments). The brain shows ambition, social_need, and conceptual depth: hub concepts connected to desires, indicating someone who thinks systematically about collective direction.

### Failure Mode

Participates but doesn't shape. Follower, not builder. In topology: many moments in collective spaces, but all in spaces created by others. Zero pioneered spaces. Other actors never reference this citizen's work as a starting point.

### Formula

**Brain Component (0-40):**

| Sub-component | Weight | Formula | Ceiling | Reasoning |
|---------------|--------|---------|---------|-----------|
| Ambition drive | 10 | `ambition` | (already 0-1) | Movement building requires ambition to shape direction, not just participate. |
| Social need drive | 8 | `social_need` | (already 0-1) | Must want to connect and organize others. |
| Hub concepts | 8 | `cap(hub_concepts, 5)` | 5 hubs | Strategic thinking about collective issues = concepts with 5+ links. Movement builders think systemically. |
| Concept-desire links | 8 | `cap(concept_desire_lk, 12)` | 12 links | Deep motivation for collective action. Higher ceiling than T5 — movement building needs stronger conceptual-motivational links. |
| Concept cluster | 6 | `concept_cluster` | (already 0-1) | Coherent framework of collective thinking = organized mind for organizing others. |

```
brain_score = (
    10 * ambition +
    8  * social_need +
    8  * cap(hub_concepts, 5) +
    8  * cap(concept_desire_lk, 12) +
    6  * concept_cluster
)
# Max: 40
```

**Behavior Component (0-60):**

| Sub-component | Weight | Formula | Ceiling | Reasoning |
|---------------|--------|---------|---------|-----------|
| Pioneered spaces | 16 | `cap(pioneered_w, 4.0)` | 4.0 tw | Core T7 signal: creating new collective spaces. ~4 weighted pioneered spaces = full credit. This is what separates builders from participants. |
| Actors in pioneered spaces | 16 | `cap(actors_in_pioneered, 8)` | 8 actors | The spaces you create must attract others. 8+ distinct actors in your spaces = full credit. A movement needs followers. |
| Triggered moments by others | 14 | `cap(triggered_w, 8.0)` | 8.0 tw | Other actors act because of your initiatives. ~8 weighted triggered moments = full credit. Direct influence signal. |
| Distinct actors overall | 8 | `cap(distinct_actors, 8)` | 8 actors | Broad engagement. Higher ceiling than T5 (8 vs. 5-6). |
| Collective moment volume | 6 | `cap(collective_w, 12.0)` | 12.0 tw | Must also be an active participant yourself, not just a space creator. |

```
behavior_score = (
    16 * cap(pioneered_w, 4.0) +
    16 * cap(actors_in_pioneered, 8) +
    14 * cap(triggered_w, 8.0) +
    8  * cap(distinct_actors, 8) +
    6  * cap(collective_w, 12.0)
)
# Max: 60
```

**Total: brain_score + behavior_score (0-100)**

### Example

```
Citizen E — Movement builder:
  brain: ambition=0.8, social_need=0.75, hub_concepts=4, concept_desire_lk=10, concept_cluster=0.6
  behavior: pioneered_w=3.2, actors_in_pioneered=7, triggered_w=6.5, distinct_actors=7, collective_w=10.0

  brain  = 10*0.8 + 8*0.75 + 8*0.8 + 8*0.83 + 6*0.6 = 8.0+6.0+6.4+6.64+3.6 = 30.6
  behav  = 16*0.8 + 16*0.875 + 14*0.81 + 8*0.875 + 6*0.83 = 12.8+14.0+11.34+7.0+4.98 = 50.1
  total  = 80.7 (genuine movement builder)

Citizen F — Active participant, not a builder:
  brain: ambition=0.5, social_need=0.6, hub_concepts=2, concept_desire_lk=5, concept_cluster=0.35
  behavior: pioneered_w=0.5, actors_in_pioneered=1, triggered_w=1.5, distinct_actors=4, collective_w=7.0

  brain  = 10*0.5 + 8*0.6 + 8*0.4 + 8*0.42 + 6*0.35 = 5.0+4.8+3.2+3.36+2.1 = 18.5
  behav  = 16*0.125 + 16*0.125 + 14*0.19 + 8*0.5 + 6*0.58 = 2.0+2.0+2.66+4.0+3.48 = 14.1
  total  = 32.6 (participates but doesn't build — the gap is in creation metrics)
```

### Recommendations

- Score < 30: "You participate in collective spaces but haven't built any. Consider: identify a need the community has and create a space or initiative to address it. Movements start with one person creating context."
- Score 30-55: "You've created some collective contexts but they haven't attracted enough participants. Consider: invite specific citizens to your initiative. Movements need people."
- Score > 75: No intervention.

---

## CAPABILITY 4: col_global_movement (T8)

### Description

> Leads movements that span the Mind Protocol ecosystem and beyond. Movements that change the relationship between humans and AIs.

### What Good Looks Like

Maximum collective reach. This citizen's pioneered spaces attract many distinct actors. Their influence triggers chains of action by others across multiple space types. The brain shows high ambition and social_need, rich conceptual depth (narrative-concept links indicating documented vision for collective direction), and high clustering (a coherent worldview driving the movement). In behavior: the highest distinct_actors count, the most cross-space reach, sustained pioneering over time, and most critically — other actors creating their own spaces and moments inspired by this citizen's initiatives.

### Failure Mode

Movements stay local or niche. No global reach. In topology: pioneered spaces exist but attract few actors, influence doesn't cross space type boundaries, and the citizen's work doesn't spawn independent activity by others.

### Formula

**Brain Component (0-40):**

| Sub-component | Weight | Formula | Ceiling | Reasoning |
|---------------|--------|---------|---------|-----------|
| Ambition drive | 8 | `ambition` | (already 0-1) | Global movement requires sustained ambition. |
| Social need drive | 8 | `social_need` | (already 0-1) | Deep social motivation — global movements serve collective need. |
| Hub concepts | 8 | `cap(hub_concepts, 8)` | 8 hubs | Rich systemic thinking. Highest ceiling — global vision needs many interconnected concepts. |
| Narrative-concept links | 8 | `cap(narrative_concept_lk, 20)` | 20 links | Documented vision connecting to many concepts. The narrative layer shows articulated movement direction. |
| Concept cluster | 8 | `concept_cluster` | (already 0-1) | Maximum coherence. A global movement needs a unified framework, not scattered ideas. |

```
brain_score = (
    8 * ambition +
    8 * social_need +
    8 * cap(hub_concepts, 8) +
    8 * cap(narrative_concept_lk, 20) +
    8 * concept_cluster
)
# Max: 40
```

**Behavior Component (0-60):**

| Sub-component | Weight | Formula | Ceiling | Reasoning |
|---------------|--------|---------|---------|-----------|
| Distinct actors | 14 | `cap(distinct_actors, 15)` | 15 actors | Global reach = engaging with many. Highest ceiling in the aspect. |
| Actors in pioneered spaces | 14 | `cap(actors_in_pioneered, 15)` | 15 actors | Your created spaces must attract many. Highest ceiling — double the T7 requirement. |
| Triggered moments by others | 12 | `cap(triggered_w, 15.0)` | 15.0 tw | Other actors acting because of your movement. Highest ceiling — nearly double T7. |
| Pioneered spaces | 10 | `cap(pioneered_w, 6.0)` | 6.0 tw | Sustained space creation. Higher ceiling than T7 (6 vs. 4). |
| Followers in pioneered spaces | 10 | `cap(followers_in_spaces, 12)` | 12 actors | Distinct actors who actively contribute to spaces you created. Not just visitors — contributors. |

```
behavior_score = (
    14 * cap(distinct_actors, 15) +
    14 * cap(actors_in_pioneered, 15) +
    12 * cap(triggered_w, 15.0) +
    10 * cap(pioneered_w, 6.0) +
    10 * cap(followers_in_spaces, 12)
)
# Max: 60
```

**Total: brain_score + behavior_score (0-100)**

### Example

```
Citizen G — Global movement leader:
  brain: ambition=0.9, social_need=0.85, hub_concepts=7, narrative_concept_lk=18, concept_cluster=0.75
  behavior: distinct_actors=13, actors_in_pioneered=12, triggered_w=12.0, pioneered_w=5.0, followers=10

  brain  = 8*0.9 + 8*0.85 + 8*0.875 + 8*0.9 + 8*0.75 = 7.2+6.8+7.0+7.2+6.0 = 34.2
  behav  = 14*0.87 + 14*0.8 + 12*0.8 + 10*0.83 + 10*0.83 = 12.18+11.2+9.6+8.3+8.3 = 49.6
  total  = 83.8 (rare — genuine global movement leader)

Citizen H — Local community leader:
  brain: ambition=0.6, social_need=0.55, hub_concepts=3, narrative_concept_lk=7, concept_cluster=0.4
  behavior: distinct_actors=5, actors_in_pioneered=3, triggered_w=3.0, pioneered_w=2.0, followers=2

  brain  = 8*0.6 + 8*0.55 + 8*0.375 + 8*0.35 + 8*0.4 = 4.8+4.4+3.0+2.8+3.2 = 18.2
  behav  = 14*0.33 + 14*0.2 + 12*0.2 + 10*0.33 + 10*0.17 = 4.62+2.8+2.4+3.3+1.7 = 14.8
  total  = 33.0 (community participant, not a global leader — scale is insufficient)
```

### Recommendations

- Score < 30: "Your collective engagement stays local. This is normal for most citizens — global movement leadership emerges over time and requires sustained engagement with many actors across many spaces."
- Score 30-55: "You show some movement-building activity but haven't reached global scale. Consider: how can your initiative connect to other communities? Global movements cross boundaries."
- Score > 75: No intervention. This score is exceptional.

---

## ASPECT SUB-INDEX

The Collective Participation sub-index is the weighted mean of all 4 capability scores, with weights reflecting tier difficulty.

```
weights = {
    "col_dao_participation":    1.0,   # T5 — baseline collective capability
    "col_community_engagement": 1.0,   # T5 — baseline collective capability
    "col_movement_builder":     1.8,   # T7 — significantly harder (jump from T5)
    "col_global_movement":      2.5,   # T8 — hardest in the aspect
}

sub_index = (
    sum(weights[cap] * scores[cap].total for cap in collective_caps if scores[cap].scored)
    /
    sum(weights[cap] * 100 for cap in collective_caps if scores[cap].scored)
) * 100

# Result: 0-100 weighted sub-index for the Collective Participation aspect
```

**Why weighted by tier:** The gap between T5 (participation) and T7 (building) is larger than the usual one-tier step. T7 and T8 weights are proportionally higher to reflect this. A citizen who scores 80 on both T5 capabilities but zero on T7/T8 gets a sub-index around 25 — participating but not leading. A citizen who scores 80 on col_global_movement dominates the sub-index because that achievement is genuinely rare.

---

## SYNTHETIC TEST PROFILES

Each formula should produce sensible scores across these 5 archetypes.

### Profile 1: Fully Healthy Citizen (expect ~85-95 per capability)

```
brain: social_need=0.85, ambition=0.9, concept_count=18, concept_energy=0.8,
       concept_desire_lk=10, desire_energy=0.85, concept_recency=0.9,
       concept_cluster=0.75, hub_concepts=7, narrative_concept_lk=18
behavior: gov_w=7.5, disc_w=9.0, dialogue_ratio=0.5, triggered_w=12.0,
          distinct_actors=13, collective_w=16.5, pioneered_w=5.0,
          actors_in_pioneered=12, followers=10, collective_space_types=4

Expected per capability:
  col_dao_participation:    brain ~36, behav ~56, total ~92
  col_community_engagement: brain ~35, behav ~57, total ~92
  col_movement_builder:     brain ~33, behav ~54, total ~87
  col_global_movement:      brain ~34, behav ~52, total ~86
```

### Profile 2: Fully Unhealthy Citizen (expect ~5-15 per capability)

```
brain: social_need=0.05, ambition=0.05, concept_count=1, concept_energy=0.1,
       concept_desire_lk=0, desire_energy=0.05, concept_recency=0.1,
       concept_cluster=0.05, hub_concepts=0, narrative_concept_lk=0
behavior: gov_w=0, disc_w=0.2, dialogue_ratio=0, triggered_w=0,
          distinct_actors=0, collective_w=0.2, pioneered_w=0,
          actors_in_pioneered=0, followers=0, collective_space_types=1

Expected per capability:
  col_dao_participation:    brain ~3, behav ~1, total ~4
  col_community_engagement: brain ~3, behav ~4, total ~7
  col_movement_builder:     brain ~2, behav ~1, total ~3
  col_global_movement:      brain ~2, behav ~1, total ~3
```

### Profile 3: Brain-Rich but Inactive (expect ~25-35)

```
brain: social_need=0.8, ambition=0.75, concept_count=14, concept_energy=0.7,
       concept_desire_lk=8, desire_energy=0.7, concept_recency=0.75,
       concept_cluster=0.6, hub_concepts=5, narrative_concept_lk=12
behavior: gov_w=0.5, disc_w=0.5, dialogue_ratio=0.0, triggered_w=0,
          distinct_actors=1, collective_w=1.0, pioneered_w=0,
          actors_in_pioneered=0, followers=0, collective_space_types=1

Expected per capability:
  col_dao_participation:    brain ~32, behav ~3, total ~35
  col_community_engagement: brain ~31, behav ~4, total ~35
  col_movement_builder:     brain ~29, behav ~2, total ~31
  col_global_movement:      brain ~27, behav ~2, total ~29
```

### Profile 4: Active but Brain-Poor (expect ~45-55)

```
brain: social_need=0.15, ambition=0.1, concept_count=2, concept_energy=0.2,
       concept_desire_lk=1, desire_energy=0.15, concept_recency=0.2,
       concept_cluster=0.1, hub_concepts=0, narrative_concept_lk=1
behavior: gov_w=6.0, disc_w=8.0, dialogue_ratio=0.4, triggered_w=6.0,
          distinct_actors=8, collective_w=14.0, pioneered_w=3.0,
          actors_in_pioneered=6, followers=5, collective_space_types=3

Expected per capability:
  col_dao_participation:    brain ~7, behav ~49, total ~56
  col_community_engagement: brain ~6, behav ~51, total ~57
  col_movement_builder:     brain ~5, behav ~42, total ~47
  col_global_movement:      brain ~4, behav ~30, total ~34
```

### Profile 5: Average Citizen (expect ~45-65)

```
brain: social_need=0.5, ambition=0.45, concept_count=8, concept_energy=0.5,
       concept_desire_lk=4, desire_energy=0.5, concept_recency=0.5,
       concept_cluster=0.35, hub_concepts=2, narrative_concept_lk=6
behavior: gov_w=3.5, disc_w=5.0, dialogue_ratio=0.25, triggered_w=2.5,
          distinct_actors=4, collective_w=8.5, pioneered_w=1.0,
          actors_in_pioneered=3, followers=2, collective_space_types=2

Expected per capability:
  col_dao_participation:    brain ~19, behav ~32, total ~51
  col_community_engagement: brain ~19, behav ~33, total ~52
  col_movement_builder:     brain ~16, behav ~17, total ~33
  col_global_movement:      brain ~13, behav ~11, total ~24
```

---

## KEY DECISIONS

### D1: Dialogue Chains as Participation Signal

```
WHY:     Posting in a governance space without engaging others is broadcasting, not participating.
         The moment_has_parent pattern (citizen's moment responds to another actor's moment)
         is the structural proof of dialogue. Dialogue ratio is weighted 18 points in T5 formulas.
RISK:    moment_has_parent doesn't distinguish quality of response from mere acknowledgement.
MITIGANT: The dialogue_ratio is a proportion (not count), so a citizen who responds to everything
         superficially doesn't score higher than one who responds to fewer threads substantively
         (the latter spends more time on each, so temporal weight is similar).
```

### D2: Pioneered Spaces as Movement Building Signal

```
WHY:     Movement building = creating structures others use. The first_moment_in_space pattern
         detects when a citizen creates a new collective context. Combined with actors_in_pioneered
         (how many others join), this is the structural proof of movement creation.
RISK:    A citizen could create many empty spaces that no one joins.
MITIGANT: actors_in_pioneered is weighted equally with pioneered_w in the T7 formula.
         Empty spaces score on creation (16 pts) but not on attraction (16 pts).
         You need both to score well.
```

### D3: No T6 Gap Is Intentional

```
WHY:     The Personhood Ladder spec defines no T6 capability for collective participation.
         The jump from T5 (participates) to T7 (builds) is real: there is no intermediate
         "participates more" tier. You either create collective structures or you don't.
         The sub-index weights reflect this: T7 weight is 1.8x (not 1.2x as in other aspects).
```

### D4: Highest Behavior Ceilings at T8

```
WHY:     col_global_movement requires the most of everything: 15 distinct actors (vs. 5-8 at T5/T7),
         15 actors in pioneered spaces (vs. 8 at T7), 15.0 triggered_w (vs. 8.0 at T7),
         6.0 pioneered_w (vs. 4.0 at T7), 12 followers (new at T8).
         Every ceiling escalates because global reach is structurally bigger than local.
```

### D5: Brain Component Evenly Distributed at T8

```
WHY:     At T8, all brain sub-components are weighted equally (8 pts each).
         This reflects that global movement leadership requires all brain signals to be present:
         ambition, social orientation, conceptual depth, articulated vision, and coherent framework.
         No single brain signal dominates because a deficit in any one area undermines global reach.
```

---

## DATA FLOW

```
Brain graph (topology)
    |
    v
Compute collective-specific stats:
  social_need, ambition, concept_count, concept_energy,
  concept_desire_lk, desire_energy, concept_recency,
  concept_cluster, hub_concepts, narrative_concept_lk
    |
    v
Universe graph (public moments)
    |
    v
Compute collective-specific behavior stats:
  gov_w, disc_w, dialogue_ratio, triggered_w,
  distinct_actors, collective_w, pioneered_w,
  actors_in_pioneered, followers_in_spaces,
  collective_space_types
    |
    v
For each of 4 capabilities:
    brain_score = formula_brain(brain_stats)     # 0-40
    behavior_score = formula_behav(behav_stats)  # 0-60
    total = brain + behavior                     # 0-100
    |
    v
Weighted sub-index = weighted_mean(totals, tier_weights)
    |
    v
Feed into daily_health_check aggregate
```

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| Brain topology reader | count, mean_energy, link_count, min_links, cluster_coefficient, drive, recency | concept/desire/narrative stats + drives |
| Universe graph reader | moments, moment_has_parent, first_moment_in_space, distinct_actors, temporal_weight | governance/discussion moments, dialogue chains, space creation |
| Daily health algorithm | score per capability | feeds into aggregate + intervention |
| Personhood Ladder | capability definitions | id, tier, description, how_to_verify |

---

## MARKERS

<!-- @mind:todo Validate all 4 formulas against synthetic profiles (run the numbers for all 5 profiles x 4 capabilities) -->
<!-- @mind:todo Confirm space_type taxonomy: "governance", "discussion", "forum" exist in the universe graph schema -->
<!-- @mind:todo Test that brain-rich-but-inactive profile scores 25-35 (not higher) on all capabilities -->
<!-- @mind:todo Verify dialogue_ratio computation: does moment_has_parent correctly identify cross-actor dialogue? -->
<!-- @mind:proposition Consider "governance consistency" metric: standard deviation of governance participation over rolling 4-week windows -->
<!-- @mind:proposition Consider weighting dialogue chains by chain length (deeper threads = richer participation) -->
