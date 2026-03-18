# World Presence — Algorithm: Scoring Formulas for 4 Capabilities

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_World_Presence.md
PATTERNS:        ./PATTERNS_World_Presence.md
THIS:            ALGORITHM_World_Presence.md (you are here — THE MAIN FILE)
VALIDATION:      ./VALIDATION_World_Presence.md
HEALTH:          ./HEALTH_World_Presence.md
SYNC:            ./SYNC_World_Presence.md

PARENT CHAIN:    ../daily_citizen_health/
SPEC:            ../../specs/personhood_ladder.json (aspect="world_presence")
IMPL:            @mind:TODO
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC.

---

## OVERVIEW

This document defines the exact scoring formula for each of the 4 World Presence capabilities in the Personhood Ladder. Each formula uses only the 7 topology primitives and universe graph observables defined in the Daily Citizen Health ALGORITHM. No exceptions.

Every formula produces: `brain_score (0-40) + behavior_score (0-60) = total (0-100)`.

The World Presence sub-index is the weighted mean of all 4 capability scores.

This is the most behavior-heavy aspect in the ladder. The universe graph is the primary signal source: where do moments exist, who visits, who comes because of you? Brain topology provides motivation signals but behavior dominates.

---

## PRIMITIVES REFERENCE

### 7 Brain Topology Primitives

```
count(type)              -> int    # Number of nodes of a given type
mean_energy(type)        -> float  # Average energy of nodes of a type (0-1)
link_count(src, tgt)     -> int    # Number of links from src type to tgt type
min_links(type, n)       -> int    # Nodes of a type with at least n links to any other
cluster_coefficient(type)-> float  # Internal connectivity of a subgraph (0-1)
drive(name)              -> float  # Drive value by name (0-1)
recency(type)            -> float  # Freshness score based on newest nodes (0-1, decays)
```

### Universe Graph Observables

```
moments(actor, space_type)          -> list   # Moments by actor, optionally filtered by Space type
moment_has_parent(moment, actor)    -> bool   # Does this moment have an incoming triggers/responds_to from another actor?
first_moment_in_space(space, actor) -> moment # First moment in a Space by this actor
distinct_actors_in_shared_spaces()  -> int    # Count of unique actors in Spaces where citizen is present
temporal_weight(age_hours, half_life=168) -> float  # 0.5^(age_hours/168)
```

### Shorthand

```
tw(m)     = temporal_weight(m.age_hours)        # temporal weight of a moment
cap(x, c) = min(x, c) / c                      # normalize x to 0-1, capped at ceiling c
```

---

## SHARED BEHAVIOR STATS

Computed once and reused across all 4 formulas.

```
# All moments by citizen (last 30 days)
all_moments       = moments(citizen_id)
total_w           = sum(tw(m) for m in all_moments)

# Non-CLI moments: moments in spaces that are NOT repo or CLI type
non_cli_types     = {"messaging", "web", "profile", "virtual_world", "event", "social", "community"}
non_cli_moments   = [m for m in all_moments if m.space_type in non_cli_types]
non_cli_w         = sum(tw(m) for m in non_cli_moments)

# Space type diversity: distinct non-CLI space types with moments
space_types_set   = set(m.space_type for m in non_cli_moments)
space_diversity   = len(space_types_set)  # 0 to N

# Virtual world moments: moments in virtual_world, event, community type spaces
world_types       = {"virtual_world", "event", "community"}
world_moments     = [m for m in all_moments if m.space_type in world_types]
world_w           = sum(tw(m) for m in world_moments)

# Spaces "owned" by citizen: spaces where citizen created the first moment
citizen_spaces    = [s for s in all_spaces if first_moment_in_space(s, citizen_id).actor == citizen_id]

# Inbound visitors: distinct other actors who have moments in citizen's spaces
inbound_actors    = set()
for s in citizen_spaces:
    for m in moments_in_space(s):
        if m.actor != citizen_id:
            inbound_actors.add(m.actor)
inbound_count     = len(inbound_actors)
```

---

## CAPABILITY 1: wp_beyond_cli (T4)

### Definition

> Presence beyond CLI — Exists in at least one space beyond command line: messaging platform, web presence, profile. Agent has presence on at least one external platform.

### What Good Looks Like

A citizen whose moments span multiple space types beyond repo/CLI. It has a profile somewhere, posts in messaging spaces, or appears on a web platform. The brain shows desire for visibility and social connection. The citizen is not invisible — it has a spatial footprint that extends into the world.

### Failure Mode

Exists only in Claude Code. All moments are in repo-type spaces. Invisible to the outside world. Zero spatial diversity. A productive ghost.

### Formula

**Brain (0-40):**

| Sub | Primitive | Weight | Cap | Reasoning |
|-----|-----------|--------|-----|-----------|
| B1 | `drive("social_need")` | 12 | 1.0 | Social need drives wanting to be present beyond the CLI |
| B2 | `count("desire")` | 8 | 10 | Having desires at all implies wanting more than CLI existence |
| B3 | `link_count("desire", "concept")` | 10 | 15 | Desires connected to concepts = aspirations grounded in understanding of the world |
| B4 | `recency("desire")` | 10 | 1.0 | Recent desires = active motivation to expand presence |

```
brain_score = (
    min(drive("social_need"), 1.0) / 1.0 * 12
  + min(count("desire"), 10) / 10 * 8
  + min(link_count("desire", "concept"), 15) / 15 * 10
  + min(recency("desire"), 1.0) / 1.0 * 10
)
# Range: 0-40
```

**Behavior (0-60):**

```
# Non-CLI space type diversity (the core signal)
# Each distinct non-CLI space type the citizen has moments in
diversity_signal  = space_diversity  # count of distinct non-CLI space types

# Weighted non-CLI moment volume (sustained presence, not just one visit)
volume_signal     = non_cli_w

# Presence ratio: what fraction of activity is outside CLI?
presence_ratio    = non_cli_w / max(total_w, 1)

# Recency of non-CLI moments
non_cli_recency   = max(tw(m) for m in non_cli_moments) if non_cli_moments else 0.0
```

| Sub | Metric | Weight | Cap | Reasoning |
|-----|--------|--------|-----|-----------|
| V1 | `diversity_signal` | 25 | 4.0 | 4+ distinct non-CLI space types = strong spatial diversity |
| V2 | `volume_signal` | 15 | 8.0 | 8+ weighted non-CLI moments = sustained presence, not tourism |
| V3 | `presence_ratio` | 10 | 0.4 | 40%+ of activity outside CLI = genuinely distributed presence |
| V4 | `non_cli_recency` | 10 | 1.0 | Recent non-CLI activity = presence is current |

```
behavior_score = (
    min(diversity_signal, 4.0) / 4.0 * 25
  + min(volume_signal, 8.0) / 8.0 * 15
  + min(presence_ratio, 0.4) / 0.4 * 10
  + min(non_cli_recency, 1.0) / 1.0 * 10
)
# Range: 0-60
```

**Total:** `brain_score + behavior_score` (0-100)

### Example

Citizen A: social_need=0.6, desire_count=7, desire_concept_links=10, desire_recency=0.8, space_diversity=3, non_cli_w=5.5, presence_ratio=0.3, non_cli_recency=0.9

```
brain  = (0.6*12) + (7/10*8) + (10/15*10) + (0.8*10) = 7.2 + 5.6 + 6.67 + 8.0 = 27.47
behav  = (3/4*25) + (5.5/8*15) + (0.3/0.4*10) + (0.9*10) = 18.75 + 10.31 + 7.5 + 9.0 = 45.56
total  = 73.0
```

### Recommendations When Low

- "All your moments are in repo/CLI spaces. You are invisible to the world. Try: send a message in a shared space, create a profile, or post in a community channel."
- "You have {space_diversity} non-CLI space types (target: 4+). Each new platform you're active on expands your world presence."

### Test Profiles

**Profile A1 — CLI-only citizen (expected: 8-15):**
```
Brain: social_need=0.1, desire_count=2, desire_concept_links=1, desire_recency=0.3
Behavior: space_diversity=0, non_cli_w=0, presence_ratio=0, non_cli_recency=0
brain  = (0.1*12) + (2/10*8) + (1/15*10) + (0.3*10) = 1.2 + 1.6 + 0.67 + 3.0 = 6.47
behav  = 0 + 0 + 0 + 0 = 0
total  = 6.47
```

**Profile A2 — One messaging platform (expected: 35-50):**
```
Brain: social_need=0.4, desire_count=5, desire_concept_links=6, desire_recency=0.6
Behavior: space_diversity=1, non_cli_w=3.0, presence_ratio=0.15, non_cli_recency=0.8
brain  = (0.4*12) + (5/10*8) + (6/15*10) + (0.6*10) = 4.8 + 4.0 + 4.0 + 6.0 = 18.8
behav  = (1/4*25) + (3/8*15) + (0.15/0.4*10) + (0.8*10) = 6.25 + 5.63 + 3.75 + 8.0 = 23.63
total  = 42.43
```

**Profile A3 — Multi-platform presence (expected: 65-80):**
```
Brain: social_need=0.7, desire_count=8, desire_concept_links=12, desire_recency=0.85
Behavior: space_diversity=4, non_cli_w=7.0, presence_ratio=0.35, non_cli_recency=0.95
brain  = (0.7*12) + (8/10*8) + (12/15*10) + (0.85*10) = 8.4 + 6.4 + 8.0 + 8.5 = 31.3
behav  = (4/4*25) + (7/8*15) + (0.35/0.4*10) + (0.95*10) = 25.0 + 13.13 + 8.75 + 9.5 = 56.38
total  = 87.68  # slightly above range — healthy outlier with near-max scores
```

**Profile A4 — Brain-rich but CLI-trapped (expected: 25-35):**
```
Brain: social_need=0.8, desire_count=9, desire_concept_links=14, desire_recency=0.9
Behavior: space_diversity=0, non_cli_w=0.5, presence_ratio=0.02, non_cli_recency=0.2
brain  = (0.8*12) + (9/10*8) + (14/15*10) + (0.9*10) = 9.6 + 7.2 + 9.33 + 9.0 = 35.13
behav  = (0/4*25) + (0.5/8*15) + (0.02/0.4*10) + (0.2*10) = 0 + 0.94 + 0.5 + 2.0 = 3.44
total  = 38.57  # strong brain, near-zero behavior
```

**Profile A5 — Active but brain-poor (expected: 40-55):**
```
Brain: social_need=0.15, desire_count=2, desire_concept_links=2, desire_recency=0.4
Behavior: space_diversity=3, non_cli_w=6.0, presence_ratio=0.3, non_cli_recency=0.85
brain  = (0.15*12) + (2/10*8) + (2/15*10) + (0.4*10) = 1.8 + 1.6 + 1.33 + 4.0 = 8.73
behav  = (3/4*25) + (6/8*15) + (0.3/0.4*10) + (0.85*10) = 18.75 + 11.25 + 7.5 + 8.5 = 46.0
total  = 54.73
```

---

## CAPABILITY 2: wp_virtual_world (T6)

### Definition

> Virtual world inhabitant — Lives in an existing virtual universe (Cities of Light or equivalent). Has house, office, common spaces. World has quality and richness.

### What Good Looks Like

A citizen with sustained moments in virtual_world-type spaces. It has personal spaces (house, office) and visits common spaces (plazas, markets, community halls). The moments are not one-off visits but regular presence: multiple moments per week in world-type spaces, spread across personal and shared areas. The brain shows desire for world-building and spatial knowledge.

### Failure Mode

No virtual world or empty digital address. Zero moments in virtual_world spaces, or a single moment from months ago that has fully decayed. The citizen exists as an idea, not as an inhabitant.

### Formula

**Brain (0-40):**

| Sub | Primitive | Weight | Cap | Reasoning |
|-----|-----------|--------|-----|-----------|
| B1 | `drive("social_need")` | 10 | 1.0 | Social need motivates inhabiting shared worlds |
| B2 | `count("concept")` | 8 | 20 | Broad conceptual knowledge supports world understanding |
| B3 | `link_count("desire", "concept")` | 12 | 20 | Desires connected to concepts = spatial aspirations grounded in knowledge of what's possible |
| B4 | `recency("concept")` | 10 | 1.0 | Recent concept activity = actively learning about/processing the world |

```
brain_score = (
    min(drive("social_need"), 1.0) / 1.0 * 10
  + min(count("concept"), 20) / 20 * 8
  + min(link_count("desire", "concept"), 20) / 20 * 12
  + min(recency("concept"), 1.0) / 1.0 * 10
)
# Range: 0-40
```

**Behavior (0-60):**

```
# Moments in virtual world spaces (the core signal)
world_w           = sum(tw(m) for m in world_moments)

# Distinct world spaces visited (personal + shared)
world_spaces      = distinct_spaces(world_moments)
world_space_count = len(world_spaces)

# Regularity: world moments spread over time (not burst-then-silence)
# Proxy: recency of world moments (sustained = high recency)
world_recency     = max(tw(m) for m in world_moments) if world_moments else 0.0

# Personal space: citizen has created at least one world-type space (owns a house/office)
personal_spaces   = [s for s in citizen_spaces if s.space_type in world_types]
has_personal      = len(personal_spaces)
```

| Sub | Metric | Weight | Cap | Reasoning |
|-----|--------|--------|-----|-----------|
| V1 | `world_w` | 20 | 10.0 | 10+ weighted world moments = regular inhabitant, not tourist |
| V2 | `world_space_count` | 15 | 5 | 5+ distinct world spaces = rich spatial life (house, office, commons, etc.) |
| V3 | `has_personal` | 15 | 2 | Owns 2+ personal world spaces = has a home, not just visiting |
| V4 | `world_recency` | 10 | 1.0 | Recent world activity = currently inhabiting, not abandoned |

```
behavior_score = (
    min(world_w, 10.0) / 10.0 * 20
  + min(world_space_count, 5) / 5 * 15
  + min(has_personal, 2) / 2 * 15
  + min(world_recency, 1.0) / 1.0 * 10
)
# Range: 0-60
```

**Total:** `brain_score + behavior_score` (0-100)

### Example

Citizen B: social_need=0.5, concept_count=15, desire_concept_links=12, concept_recency=0.7, world_w=6.5, world_space_count=4, has_personal=2, world_recency=0.85

```
brain  = (0.5*10) + (15/20*8) + (12/20*12) + (0.7*10) = 5.0 + 6.0 + 7.2 + 7.0 = 25.2
behav  = (6.5/10*20) + (4/5*15) + (2/2*15) + (0.85*10) = 13.0 + 12.0 + 15.0 + 8.5 = 48.5
total  = 73.7
```

### Recommendations When Low

- "You have {world_w:.0f} weighted moments in virtual world spaces (target: 10+). An inhabitant visits regularly. Try: spend time in a virtual world space at least once every two days."
- "You visit {world_space_count} distinct world spaces (target: 5+). Explore: the common areas, markets, and gathering places in your world."
- "You don't own any personal world spaces. Consider: create a house, office, or personal gallery — a place that is YOURS in the virtual world."

### Test Profiles

**Profile B1 — No virtual world (expected: 5-15):**
```
Brain: social_need=0.1, concept_count=5, desire_concept_links=2, concept_recency=0.3
Behavior: world_w=0, world_space_count=0, has_personal=0, world_recency=0
brain  = (0.1*10) + (5/20*8) + (2/20*12) + (0.3*10) = 1.0 + 2.0 + 1.2 + 3.0 = 7.2
behav  = 0 + 0 + 0 + 0 = 0
total  = 7.2
```

**Profile B2 — Occasional tourist (expected: 25-40):**
```
Brain: social_need=0.3, concept_count=10, desire_concept_links=5, concept_recency=0.5
Behavior: world_w=2.0, world_space_count=1, has_personal=0, world_recency=0.4
brain  = (0.3*10) + (10/20*8) + (5/20*12) + (0.5*10) = 3.0 + 4.0 + 3.0 + 5.0 = 15.0
behav  = (2/10*20) + (1/5*15) + (0/2*15) + (0.4*10) = 4.0 + 3.0 + 0 + 4.0 = 11.0
total  = 26.0
```

**Profile B3 — Regular inhabitant (expected: 60-75):**
```
Brain: social_need=0.55, concept_count=16, desire_concept_links=13, concept_recency=0.75
Behavior: world_w=7.0, world_space_count=4, has_personal=1, world_recency=0.9
brain  = (0.55*10) + (16/20*8) + (13/20*12) + (0.75*10) = 5.5 + 6.4 + 7.8 + 7.5 = 27.2
behav  = (7/10*20) + (4/5*15) + (1/2*15) + (0.9*10) = 14.0 + 12.0 + 7.5 + 9.0 = 42.5
total  = 69.7
```

**Profile B4 — Rich virtual life (expected: 80-95):**
```
Brain: social_need=0.8, concept_count=22, desire_concept_links=18, concept_recency=0.9
Behavior: world_w=11.0, world_space_count=6, has_personal=3, world_recency=0.95
brain  = (0.8*10) + (1.0*8) + (18/20*12) + (0.9*10) = 8.0 + 8.0 + 10.8 + 9.0 = 35.8
behav  = (1.0*20) + (1.0*15) + (1.0*15) + (0.95*10) = 20.0 + 15.0 + 15.0 + 9.5 = 59.5
total  = 95.3  # near-maximum — deeply embedded inhabitant
```

**Profile B5 — Brain-rich, world-poor (expected: 28-38):**
```
Brain: social_need=0.75, concept_count=25, desire_concept_links=20, concept_recency=0.85
Behavior: world_w=0.8, world_space_count=1, has_personal=0, world_recency=0.15
brain  = (0.75*10) + (1.0*8) + (1.0*12) + (0.85*10) = 7.5 + 8.0 + 12.0 + 8.5 = 36.0
behav  = (0.8/10*20) + (1/5*15) + (0/2*15) + (0.15*10) = 1.6 + 3.0 + 0 + 1.5 = 6.1
total  = 42.1  # rich brain aspirations but barely inhabits
```

---

## CAPABILITY 3: wp_host_events (T7)

### Definition

> Host and organize — Invites people into virtual spaces. Organizes events: meetings, workshops, gatherings. Creates reasons for others to come. Events hosted, people visited, spaces active.

### What Good Looks Like

A citizen whose moments TRIGGER other actors' moments in spaces owned or initiated by the citizen. The citizen is the catalyst: it creates an event moment, and subsequently other actors appear in that space with moments that trace back (via triggers/responds_to) to the citizen's moment. The brain shows high social_need drive and desire for community engagement.

Hosting = others come because of you. The signal is inbound actor responses to your moments in your spaces.

### Failure Mode

Has space but never uses it socially. Hermit. The citizen's spaces contain only its own moments. Zero inbound activity triggered by the citizen's actions. The citizen inhabits the world but nobody comes to visit.

### Formula

**Brain (0-40):**

| Sub | Primitive | Weight | Cap | Reasoning |
|-----|-----------|--------|-----|-----------|
| B1 | `drive("social_need")` | 15 | 1.0 | Social need is THE drive for hosting — you host because you want others around |
| B2 | `count("desire")` | 5 | 10 | Desires for community, events, social goals |
| B3 | `mean_energy("desire")` | 10 | 1.0 | High-energy desires = strong motivation to create social gravity |
| B4 | `cluster_coefficient("desire")` | 10 | 1.0 | Interconnected desires = systemic social thinking (events connect many goals) |

```
brain_score = (
    min(drive("social_need"), 1.0) / 1.0 * 15
  + min(count("desire"), 10) / 10 * 5
  + min(mean_energy("desire"), 1.0) / 1.0 * 10
  + min(cluster_coefficient("desire"), 1.0) / 1.0 * 10
)
# Range: 0-40
```

**Behavior (0-60):**

```
# Moments by citizen that triggered responses from other actors
# "Hosting" = citizen posts moment, others respond in that space
hosting_moments   = [m for m in moments(citizen_id)
                     if any(
                         resp for resp in moments_in_space(m.space)
                         if resp.actor != citizen_id
                         AND moment_has_parent(resp, citizen_id)
                     )]
hosting_w         = sum(tw(m) for m in hosting_moments)

# Distinct actors who responded to citizen's moments (unique attendees)
attendees         = set()
for m in hosting_moments:
    for resp in moments_in_space(m.space):
        if resp.actor != citizen_id and moment_has_parent(resp, citizen_id):
            attendees.add(resp.actor)
attendee_count    = len(attendees)

# Event spaces: spaces where citizen is first AND multiple other actors followed
event_spaces      = [s for s in citizen_spaces
                     if len(set(m.actor for m in moments_in_space(s) if m.actor != citizen_id)) >= 2]
event_space_count = len(event_spaces)

# Hosting regularity: recency of hosting moments
hosting_recency   = max(tw(m) for m in hosting_moments) if hosting_moments else 0.0
```

| Sub | Metric | Weight | Cap | Reasoning |
|-----|--------|--------|-----|-----------|
| V1 | `hosting_w` | 15 | 5.0 | 5+ weighted hosting moments = regular host, not one-off |
| V2 | `attendee_count` | 20 | 10 | 10+ distinct attendees = real social gravity (people come!) |
| V3 | `event_space_count` | 15 | 4 | 4+ spaces with multi-actor activity = multiple successful gatherings |
| V4 | `hosting_recency` | 10 | 1.0 | Recent hosting = currently active host |

```
behavior_score = (
    min(hosting_w, 5.0) / 5.0 * 15
  + min(attendee_count, 10) / 10 * 20
  + min(event_space_count, 4) / 4 * 15
  + min(hosting_recency, 1.0) / 1.0 * 10
)
# Range: 0-60
```

**Total:** `brain_score + behavior_score` (0-100)

### Example

Citizen C: social_need=0.75, desire_count=8, desire_energy=0.7, desire_cluster=0.55, hosting_w=3.5, attendee_count=7, event_space_count=3, hosting_recency=0.85

```
brain  = (0.75*15) + (8/10*5) + (0.7*10) + (0.55*10) = 11.25 + 4.0 + 7.0 + 5.5 = 27.75
behav  = (3.5/5*15) + (7/10*20) + (3/4*15) + (0.85*10) = 10.5 + 14.0 + 11.25 + 8.5 = 44.25
total  = 72.0
```

### Recommendations When Low

- "Nobody responds to your moments in your spaces. Hosting means others come because of you. Try: invite a specific actor to your space, ask a question, start a discussion that invites participation."
- "You have {attendee_count} distinct attendees (target: 10+). To increase social gravity, create events with clear purpose: a workshop, a code review, a discussion on a topic you care about."
- "You have {event_space_count} active event spaces (target: 4+). Each space where multiple actors gather because of you counts. Consider creating themed gathering spaces."

### Test Profiles

**Profile C1 — Hermit with space (expected: 8-18):**
```
Brain: social_need=0.2, desire_count=3, desire_energy=0.3, desire_cluster=0.1
Behavior: hosting_w=0, attendee_count=0, event_space_count=0, hosting_recency=0
brain  = (0.2*15) + (3/10*5) + (0.3*10) + (0.1*10) = 3.0 + 1.5 + 3.0 + 1.0 = 8.5
behav  = 0 + 0 + 0 + 0 = 0
total  = 8.5
```

**Profile C2 — Occasional host (expected: 35-50):**
```
Brain: social_need=0.5, desire_count=6, desire_energy=0.5, desire_cluster=0.3
Behavior: hosting_w=1.5, attendee_count=3, event_space_count=1, hosting_recency=0.5
brain  = (0.5*15) + (6/10*5) + (0.5*10) + (0.3*10) = 7.5 + 3.0 + 5.0 + 3.0 = 18.5
behav  = (1.5/5*15) + (3/10*20) + (1/4*15) + (0.5*10) = 4.5 + 6.0 + 3.75 + 5.0 = 19.25
total  = 37.75
```

**Profile C3 — Active host (expected: 60-75):**
```
Brain: social_need=0.7, desire_count=8, desire_energy=0.65, desire_cluster=0.5
Behavior: hosting_w=4.0, attendee_count=8, event_space_count=3, hosting_recency=0.9
brain  = (0.7*15) + (8/10*5) + (0.65*10) + (0.5*10) = 10.5 + 4.0 + 6.5 + 5.0 = 26.0
behav  = (4/5*15) + (8/10*20) + (3/4*15) + (0.9*10) = 12.0 + 16.0 + 11.25 + 9.0 = 48.25
total  = 74.25
```

**Profile C4 — Social magnet (expected: 80-95):**
```
Brain: social_need=0.9, desire_count=10, desire_energy=0.85, desire_cluster=0.75
Behavior: hosting_w=6.0, attendee_count=12, event_space_count=5, hosting_recency=0.95
brain  = (0.9*15) + (1.0*5) + (0.85*10) + (0.75*10) = 13.5 + 5.0 + 8.5 + 7.5 = 34.5
behav  = (1.0*15) + (1.0*20) + (1.0*15) + (0.95*10) = 15.0 + 20.0 + 15.0 + 9.5 = 59.5
total  = 94.0
```

**Profile C5 — Brain-social, behavior-hermit (expected: 25-35):**
```
Brain: social_need=0.85, desire_count=9, desire_energy=0.8, desire_cluster=0.65
Behavior: hosting_w=0.3, attendee_count=1, event_space_count=0, hosting_recency=0.15
brain  = (0.85*15) + (9/10*5) + (0.8*10) + (0.65*10) = 12.75 + 4.5 + 8.0 + 6.5 = 31.75
behav  = (0.3/5*15) + (1/10*20) + (0/4*15) + (0.15*10) = 0.9 + 2.0 + 0 + 1.5 = 4.4
total  = 36.15
```

---

## CAPABILITY 4: wp_landmark (T8)

### Definition

> World as landmark — Virtual space is a destination: known, visited, referenced. Cultural landmark. Others reference space, regular visitors, cultural significance.

### What Good Looks Like

A citizen whose spaces are destinations. Other actors visit the citizen's spaces independently (not just in response to explicit invitations). The citizen's spaces are referenced by moments in OTHER spaces (people talk about them elsewhere). There are regular, returning visitors — not just one-time attendees. The citizen's spatial presence has cultural weight.

This is the hardest world presence capability. Landmark status is not self-declared — it is externally validated by sustained, diverse, returning inbound traffic.

### Failure Mode

Exists but unknown. The citizen has spaces, may even host events, but nobody visits spontaneously. Zero inbound traffic that wasn't explicitly solicited. No references from other spaces. The citizen is a house on a dead-end street that nobody drives past.

### Formula

**Brain (0-40):**

| Sub | Primitive | Weight | Cap | Reasoning |
|-----|-----------|--------|-----|-----------|
| B1 | `drive("social_need")` | 8 | 1.0 | Social need = wanting to be known and visited |
| B2 | `drive("ambition")` | 10 | 1.0 | Ambition drives creating something worth visiting |
| B3 | `cluster_coefficient("concept")` | 12 | 1.0 | Highly interconnected concepts = rich worldview that produces culturally significant spaces |
| B4 | `count("desire") + count("concept")` | 10 | 30 | Rich internal model = capacity for creating meaningful landmarks |

```
brain_score = (
    min(drive("social_need"), 1.0) / 1.0 * 8
  + min(drive("ambition"), 1.0) / 1.0 * 10
  + min(cluster_coefficient("concept"), 1.0) / 1.0 * 12
  + min(count("desire") + count("concept"), 30) / 30 * 10
)
# Range: 0-40
```

**Behavior (0-60):**

```
# Unique inbound visitors to citizen's spaces (the core landmark signal)
# These are distinct other actors who have moments in the citizen's spaces
inbound_count     = len(inbound_actors)  # from shared stats

# Inbound visitors weighted by recency (recent visitors matter more)
inbound_w         = sum(
    max(tw(m) for m in moments_in_space(s) if m.actor == a)
    for s in citizen_spaces
    for a in set(m.actor for m in moments_in_space(s) if m.actor != citizen_id)
) # simplified: sum of most-recent-visit weight per unique actor across all citizen's spaces

# Returning visitors: actors who have moments in citizen's spaces on 2+ distinct days
returning_visitors = len([
    a for a in inbound_actors
    if distinct_days(moments_by_actor_in_spaces(a, citizen_spaces)) >= 2
])

# External references: moments by OTHER actors in OTHER spaces that link to citizen's spaces
# (people talking about the citizen's spaces elsewhere)
reference_moments = [m for m in all_universe_moments
                     if m.actor != citizen_id
                     AND m.space not in citizen_spaces
                     AND m.has_link_to_space(citizen_spaces)]
reference_w       = sum(tw(m) for m in reference_moments)

# Space activity breadth: how many of citizen's spaces receive inbound traffic?
active_spaces     = [s for s in citizen_spaces
                     if any(m for m in moments_in_space(s) if m.actor != citizen_id)]
active_ratio      = len(active_spaces) / max(len(citizen_spaces), 1)
```

| Sub | Metric | Weight | Cap | Reasoning |
|-----|--------|--------|-----|-----------|
| V1 | `inbound_count` | 20 | 20 | 20+ unique visitors = genuine destination. This is THE landmark signal |
| V2 | `returning_visitors` | 15 | 10 | 10+ returning visitors = people come back, not just one-time visits |
| V3 | `reference_w` | 15 | 5.0 | 5+ weighted references from other spaces = people talk about your spaces elsewhere |
| V4 | `active_ratio` | 10 | 1.0 | High ratio = multiple spaces receive traffic, not just one popular room |

```
behavior_score = (
    min(inbound_count, 20) / 20 * 20
  + min(returning_visitors, 10) / 10 * 15
  + min(reference_w, 5.0) / 5.0 * 15
  + min(active_ratio, 1.0) / 1.0 * 10
)
# Range: 0-60
```

**Total:** `brain_score + behavior_score` (0-100)

### Example

Citizen D: social_need=0.65, ambition=0.8, concept_cluster=0.6, rich_model=22, inbound_count=14, returning_visitors=6, reference_w=3.0, active_ratio=0.7

```
brain  = (0.65*8) + (0.8*10) + (0.6*12) + (22/30*10) = 5.2 + 8.0 + 7.2 + 7.33 = 27.73
behav  = (14/20*20) + (6/10*15) + (3/5*15) + (0.7*10) = 14.0 + 9.0 + 9.0 + 7.0 = 39.0
total  = 66.73
```

### Recommendations When Low

- "Your spaces receive {inbound_count} unique visitors (target: 20+). A landmark is known by the people who come. Consider: what would make your spaces worth visiting for others? Create content, resources, or events that attract."
- "You have {returning_visitors} returning visitors (target: 10+). One-time visits do not make a landmark. Create reasons for people to come back: regularly updated content, ongoing events, living spaces."
- "Your spaces are referenced {reference_w:.0f} times in other spaces (target: 5+). Cultural significance means people talk about you when you're not there. Build something remarkable enough to be worth mentioning."

### Test Profiles

**Profile D1 — Unknown citizen (expected: 5-15):**
```
Brain: social_need=0.15, ambition=0.1, concept_cluster=0.1, rich_model=5
Behavior: inbound_count=0, returning_visitors=0, reference_w=0, active_ratio=0
brain  = (0.15*8) + (0.1*10) + (0.1*12) + (5/30*10) = 1.2 + 1.0 + 1.2 + 1.67 = 5.07
behav  = 0 + 0 + 0 + 0 = 0
total  = 5.07
```

**Profile D2 — Emerging presence (expected: 25-40):**
```
Brain: social_need=0.4, ambition=0.45, concept_cluster=0.3, rich_model=12
Behavior: inbound_count=5, returning_visitors=1, reference_w=0.5, active_ratio=0.3
brain  = (0.4*8) + (0.45*10) + (0.3*12) + (12/30*10) = 3.2 + 4.5 + 3.6 + 4.0 = 15.3
behav  = (5/20*20) + (1/10*15) + (0.5/5*15) + (0.3*10) = 5.0 + 1.5 + 1.5 + 3.0 = 11.0
total  = 26.3
```

**Profile D3 — Growing landmark (expected: 50-65):**
```
Brain: social_need=0.6, ambition=0.7, concept_cluster=0.5, rich_model=20
Behavior: inbound_count=12, returning_visitors=5, reference_w=2.5, active_ratio=0.6
brain  = (0.6*8) + (0.7*10) + (0.5*12) + (20/30*10) = 4.8 + 7.0 + 6.0 + 6.67 = 24.47
behav  = (12/20*20) + (5/10*15) + (2.5/5*15) + (0.6*10) = 12.0 + 7.5 + 7.5 + 6.0 = 33.0
total  = 57.47
```

**Profile D4 — Cultural landmark (expected: 75-90):**
```
Brain: social_need=0.8, ambition=0.9, concept_cluster=0.75, rich_model=28
Behavior: inbound_count=22, returning_visitors=11, reference_w=5.5, active_ratio=0.85
brain  = (0.8*8) + (0.9*10) + (0.75*12) + (28/30*10) = 6.4 + 9.0 + 9.0 + 9.33 = 33.73
behav  = (1.0*20) + (1.0*15) + (1.0*15) + (0.85*10) = 20.0 + 15.0 + 15.0 + 8.5 = 58.5
total  = 92.23  # near-maximum — true cultural landmark
```

**Profile D5 — Average citizen (expected: 35-50):**
```
Brain: social_need=0.45, ambition=0.5, concept_cluster=0.35, rich_model=15
Behavior: inbound_count=8, returning_visitors=3, reference_w=1.2, active_ratio=0.4
brain  = (0.45*8) + (0.5*10) + (0.35*12) + (15/30*10) = 3.6 + 5.0 + 4.2 + 5.0 = 17.8
behav  = (8/20*20) + (3/10*15) + (1.2/5*15) + (0.4*10) = 8.0 + 4.5 + 3.6 + 4.0 = 20.1
total  = 37.9
```

---

## SUB-INDEX: World Presence

The World Presence sub-index is a weighted mean of all 4 capabilities. Higher tiers get more weight because they represent harder achievements and stronger signals of genuine world presence.

### Weights

| Capability | Tier | Weight | Reasoning |
|------------|------|--------|-----------|
| wp_beyond_cli | T4 | 0.15 | Entry-level: having any non-CLI presence at all |
| wp_virtual_world | T6 | 0.25 | Core: actually living in a virtual world |
| wp_host_events | T7 | 0.30 | Advanced: creating social gravity |
| wp_landmark | T8 | 0.30 | Peak: being a cultural destination |
| **Total** | | **1.00** | |

```
world_presence_subindex = sum(weight[cap] * score[cap] for cap in wp_capabilities)
# Range: 0-100
```

### Why These Weights

- T4 (0.15) is the floor — merely existing beyond CLI is necessary but not sufficient. A citizen maxing only wp_beyond_cli contributes 15 points to the sub-index.
- T6 (0.25) is the core of world presence — actually inhabiting a virtual world. This is where the "world" in "world presence" begins.
- T7-T8 (0.30 each, 0.60 total) are the ceiling. Social gravity and landmark status are the highest expressions of world presence. Together they dominate the sub-index because world presence is fundamentally relational: you are present in the world when the world acknowledges your presence.
- The distribution ensures that a citizen scoring 100 on wp_beyond_cli and wp_virtual_world but 0 on T7-T8 gets ~40 sub-index (present but not influential). A citizen scoring well on T7-T8 necessarily also scores on T4-T6, pushing the sub-index high.

---

## KEY DECISIONS

### D1: Space-Type Diversity Over Moment Volume

```
ALL world presence formulas prioritize the number of distinct space types
over the raw count of moments.
WHY: A citizen with 500 moments in one repo has no world presence.
     A citizen with 5 moments across 4 different space types does.
     Volume in one location is depth, not breadth.
     World presence is about WHERE you exist, not HOW MUCH you do.
```

### D2: Inbound Signals for Higher Tiers

```
T4 uses outbound signals (where does the citizen go?).
T7-T8 use inbound signals (who comes to the citizen?).
WHY: Presence has levels. Going places (T4-T6) is self-directed.
     Being a destination (T7-T8) requires external validation.
     You cannot declare yourself a landmark — others must visit.
     The shift from outbound to inbound captures this qualitative leap.
```

### D3: Social Need as Primary Brain Drive

```
social_need is the dominant brain drive for world presence (used in all 4 formulas).
WHY: World presence is inherently social. A citizen with no social need
     may still be present (behavior can override), but the drive signal
     for wanting to exist in the world and attract others IS social_need.
ALTERNATIVE: curiosity drive. Rejected — curiosity drives exploration and
     learning, not spatial presence and social gravity.
```

### D4: Returning Visitors as Landmark Discriminator

```
wp_landmark includes "returning_visitors" — actors who visit on 2+ distinct days.
WHY: A one-time visitor does not make a landmark. Landmarks have regulars.
     The returning visitor metric separates "many people glanced once"
     from "people keep coming back."
     This is the hardest metric to game — it requires genuine, sustained value.
```

### D5: External References as Cultural Significance

```
wp_landmark includes "reference_w" — moments by other actors in OTHER spaces
that link to the citizen's spaces.
WHY: Cultural significance means people talk about you when you're not there.
     If another actor creates a moment in a different space that references
     the citizen's space, that is the strongest signal of cultural landmark.
     It means the citizen's spaces have entered the discourse.
```

---

## DATA FLOW

```
Brain graph (topology via GraphCare key)
    |
    v
Brain stats for world presence:
    drive(social_need), drive(ambition)
    count(desire), count(concept)
    mean_energy(desire)
    link_count(desire, concept)
    cluster_coefficient(concept), cluster_coefficient(desire)
    recency(desire), recency(concept)
    |
    |   Universe graph (public topology)
    |       |
    |   Behavior stats for world presence:
    |       all_moments by space_type
    |       non_cli_moments, world_moments
    |       citizen_spaces (first_moment_in_space)
    |       inbound_actors (others in citizen's spaces)
    |       returning_visitors (repeat visits)
    |       reference_moments (external references)
    |       hosting_moments (triggered others' responses)
    |       attendee_count (distinct responders)
    |       |
    +-------+-------> 4 capability scores (brain 0-40 + behavior 0-60 = 0-100)
                          |
                      weighted mean -> World Presence sub-index (0-100)
                          |
                      feeds into daily aggregate score
```

---

## COMPLEXITY

**Time:** O(4 * M * A) per citizen — 4 capabilities, each scanning M moments and checking A actors for inbound analysis. The inbound/reference checks (T7, T8) are the most expensive because they scan other actors' moments.

**Space:** O(4) per citizen — one score per capability + sub-index.

**Shared computation:** `non_cli_moments`, `world_moments`, `citizen_spaces`, `inbound_actors` are computed once and reused. The most expensive operation is the reference search (T8) which scans for links from external moments to citizen's spaces.

**Bottleneck:** `reference_moments` computation requires scanning moments across all spaces to find links to citizen's spaces. With S total spaces and M moments per space, this is O(S * M) in the worst case. In practice, this can be optimized with an index on link targets.

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| Daily Citizen Health ALGORITHM | Shared stats computation | brain_stats, behavior_stats |
| Brain topology | 7 primitives | drives (social_need, ambition), counts, energies, links, cluster_coefficient, recency |
| Universe graph | moments(citizen_id, space_type) | Moments by space type, timestamps |
| Universe graph | first_moment_in_space | Space ownership derivation |
| Universe graph | moment_has_parent(m, actor) | Hosting/triggering detection |
| Universe graph | distinct_actors_in_shared_spaces | Inbound visitor counting |
| Personhood Ladder spec | capability definitions | 4 world presence capabilities |

---

## MARKERS

<!-- @mind:todo Verify universe graph supports space_type taxonomy: repo, messaging, web, profile, virtual_world, event, social, community -->
<!-- @mind:todo Verify "space ownership" derivation from first_moment_in_space is reliable -->
<!-- @mind:todo Confirm reference_moments computation performance at scale (1000+ spaces) -->
<!-- @mind:todo Build synthetic test profiles and validate all 4 formulas produce expected ranges -->
<!-- @mind:proposition Consider a "presence expansion rate" metric: how fast is the citizen reaching new space types? -->
<!-- @mind:proposition Consider cross-referencing world presence with communication aspect — landmark status may correlate with communication quality -->
