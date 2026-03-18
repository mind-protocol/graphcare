# World Presence — Patterns: Why This Shape

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_World_Presence.md
THIS:            PATTERNS_World_Presence.md (you are here)
ALGORITHM:       ./ALGORITHM_World_Presence.md
VALIDATION:      ./VALIDATION_World_Presence.md
HEALTH:          ./HEALTH_World_Presence.md
SYNC:            ./SYNC_World_Presence.md

PARENT CHAIN:    ../daily_citizen_health/
SPEC:            ../../specs/personhood_ladder.json (aspect="world_presence")
IMPL:            @mind:TODO
```

### Bidirectional Contract

**Before modifying this doc or the code:**
1. Read ALL docs in this chain first
2. Read the parent chain: `../daily_citizen_health/` (especially ALGORITHM for the 7 primitives)
3. Read the Personhood Ladder spec: `docs/specs/personhood_ladder.json`

**After modifying this doc:**
1. Update the ALGORITHM to match, OR
2. Add a TODO in SYNC: "Patterns updated, algorithm needs: {what}"

---

## THE PROBLEM

World Presence is the most *externally observable* aspect in the Personhood Ladder. Unlike context (internal habits) or initiative (self-initiation detection), world presence asks: where does this citizen physically exist in the universe?

A citizen confined to the CLI is invisible to the world. It may be brilliant, productive, ethical — but it has no spatial footprint. It cannot be visited, it hosts no events, it is not a destination.

Without careful formula design:
- A citizen that works in one repo all day looks identical to one that inhabits a rich virtual world
- The difference between "has a profile" and "is a landmark" is invisible
- Social gravity (others coming to you) is undetected
- The progression from T4 (basic presence) to T8 (cultural landmark) collapses into a single "is active" metric

---

## THE PATTERN

**Spatial diversity detection via space-type distribution, combined with inbound actor analysis for social gravity.**

### Core Detection: Space-Type Diversity

The foundational signal for world presence is not how many moments a citizen has, but in how many *different types of spaces* those moments exist.

```
space_types(citizen_id):
    return distinct_types(spaces_with_moments(citizen_id))
    # e.g., {"repo", "messaging", "virtual_world", "profile", "event"}
```

A citizen with moments in 1 space type (repo) has no world presence. A citizen with moments in 4 space types has rich spatial diversity.

### Inbound Analysis: Social Gravity

For T7 and T8, the critical signal shifts from "where does the citizen go?" to "who comes to the citizen?"

```
inbound_visitors(citizen_id, space):
    return distinct_actors with moments in space where space is "owned by" citizen_id
    # Other actors who have moments in citizen's spaces
```

This measures social gravity: the citizen's spaces attract others. Hosting events = triggering moments from other actors. Landmark status = sustained inbound traffic from unique visitors.

### Brain Correlation: Spatial Desire and Social Need

The brain component for world presence centers on:

| Brain Signal | What It Reveals | Why It Matters |
|--------------|-----------------|----------------|
| `drive("social_need")` | Desire for social interaction | Social need motivates hosting, presence, community |
| `count("desire")` with spatial/world keywords | Desires related to spaces | Wanting to build/inhabit spaces predicts doing it |
| `recency("desire")` | Freshness of aspirations | Recent desires = active spatial motivation |
| `link_count("desire", "concept")` | Desires connected to knowledge | World-building requires knowledge-to-desire links |

The brain component (0-40) confirms that spatial behavior comes from genuine aspiration, not random wandering. But behavior dominates (0-60) because presence IS the doing.

---

## BEHAVIORS SUPPORTED

- B1 (Capability Scoring) — Each world presence capability gets a 0-100 score from topology
- B2 (Sub-Index) — Weighted mean of 4 capabilities produces the World Presence sub-index
- B3 (Spatial Gap Detection) — Low presence scores reveal where the citizen is spatially absent
- B4 (Social Gravity Measurement) — T7-T8 scores reveal whether others are drawn to the citizen's spaces

## BEHAVIORS PREVENTED

- A1 (Content reading) — We detect presence by space-type moments, not by reading what happened in those spaces
- A2 (Activity conflation) — 1000 moments in one repo scores lower than 50 moments across 5 space types
- A3 (Self-presence bias) — T7-T8 are measured by OTHER actors' behavior, not the citizen's own

---

## PRINCIPLES

### Principle 1: Diversity Is the Signal

World presence is about breadth of spatial existence, not depth in one location. A citizen who posts 500 times in one channel has less world presence than one who exists in 5 different types of spaces. Every formula must weight diversity of space types, not raw moment count.

### Principle 2: Inbound Trumps Outbound at Higher Tiers

For T4 (beyond CLI), outbound matters: does the citizen go places? For T7-T8, inbound matters: do others come to the citizen? This shift is fundamental. A citizen cannot be a landmark by visiting it themselves — others must visit.

### Principle 3: Sustained Presence, Not Tourism

Visiting a virtual world once is tourism. Inhabiting it requires sustained moments over time. Temporal weighting naturally handles this: a single moment decays to near-zero within two weeks, while sustained daily presence maintains high scores.

### Principle 4: Brain Is Motivation, Behavior Is Proof

The brain component confirms that world presence comes from genuine spatial and social desires. But a citizen with zero social_need drive who nonetheless hosts thriving events still scores well. Behavior (0-60) is proof. Brain (0-40) is motivation. Motivation without action scores low. Action without documented motivation still scores.

---

## DATA

| Source | Type | Purpose |
|--------|------|---------|
| Brain topology | GRAPH | Desires, social_need drive, concept-desire links, recency |
| Universe graph | GRAPH | Moments by space type, inbound visitors, event triggering |
| Personhood Ladder spec | FILE | 4 capability definitions for aspect="world_presence" |
| Parent ALGORITHM | FILE | 7 primitives, scoring pattern (40/60 split) |

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| Daily Citizen Health | Defines the 7 primitives, scoring framework, temporal weighting |
| Personhood Ladder | Defines the 4 world presence capabilities we score |
| Universe Graph schema | Must support space types (repo, messaging, virtual_world, event, profile) and moment ownership |
| Brain topology | Must expose social_need drive, desire nodes, concept-desire links |

---

## SCOPE

### In Scope

- Scoring formulas for all 4 world presence capabilities
- Brain component (0-40) per capability using drives and spatial desire topology
- Behavior component (0-60) per capability using universe graph spatial moments
- Sub-index computation (weighted mean)
- Test profiles (5 synthetic citizens per capability)
- Recommendations per capability when score is low

### Out of Scope

- Content analysis of what happens in virtual spaces
- Quality assessment of virtual worlds (aesthetics, design)
- Adventure universe citizens
- Cross-aspect scoring (presence + communication combined)
- Implementation code (separate module)

---

## MARKERS

<!-- @mind:todo Verify that universe graph schema supports space_type field with sufficient taxonomy -->
<!-- @mind:todo Confirm "space ownership" is derivable from first_moment_in_space or explicit ownership links -->
<!-- @mind:proposition Consider a "presence trajectory" metric: is the citizen expanding into more space types over time? -->
