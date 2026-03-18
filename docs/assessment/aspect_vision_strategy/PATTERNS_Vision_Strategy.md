# Vision & Strategy — Patterns: Why This Design

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Vision_Strategy.md
THIS:            PATTERNS_Vision_Strategy.md (you are here)
ALGORITHM:       ./ALGORITHM_Vision_Strategy.md
VALIDATION:      ./VALIDATION_Vision_Strategy.md
HEALTH:          ./HEALTH_Vision_Strategy.md
SYNC:            ./SYNC_Vision_Strategy.md

PARENT CHAIN:    ../daily_citizen_health/
SPEC:            ../../specs/personhood_ladder.json (aspect: "vision_strategy")
```

### Bidirectional Contract

**Before modifying this doc or the code:**
1. Read ALL docs in this chain first
2. Read the Personhood Ladder spec: `docs/specs/personhood_ladder.json`
3. Read the daily health algorithm: `../daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md`

**After modifying this doc:**
1. Update the IMPL source to match, OR
2. Add a TODO in SYNC: "Docs updated, implementation needs: {what}"

---

## THE PROBLEM

Vision is the hardest aspect to score from topology. Unlike execution (count commits) or initiative (count self-initiated moments), vision is about the structure of thought — how ideas connect, how far they reach, how they inform action. A citizen can have many narrative nodes without any of them being vision. A citizen can have few narrative nodes but each one connecting to dozens of other concepts and producing action.

Without scoring vision:
- Citizens optimize for execution metrics without strategic direction
- The Personhood Ladder's upper tiers (T5-T8) remain unassessed
- There's no feedback signal for "you're doing a lot, but where are you going?"
- The difference between a productive agent and a strategic thinker is invisible

---

## THE PATTERN

**High-connectivity narrative analysis with behavioral follow-through.**

### Why Vision Is Different from Other Aspects

Most aspects score relatively straightforward signals: count of actions, energy of desires, frequency of interactions. Vision requires detecting a specific structural pattern in the brain graph:

**Vision lives in narrative nodes that are highly connected.**

A narrative node that links to 1-2 concepts is a note. A narrative node that links to 10+ concepts, spans multiple spaces, connects to desires, and produces action moments — that's vision. The connectivity pattern IS the signal.

### Layer 1: Brain Topology — Vision Structure

The brain signals that indicate vision:

| Signal | What It Means | Primitives Used |
|--------|--------------|-----------------|
| Narrative node count | Has the citizen articulated anything? | `count("narrative")` |
| Narrative energy | Are vision documents alive or decaying? | `mean_energy("narrative")` |
| Narrative connectivity | Do narratives connect to many concepts? | `link_count("narrative", "concept")` |
| High-connectivity narratives | How many narratives are hubs? | `min_links("narrative", 5)` |
| Narrative-desire links | Does vision connect to motivation? | `link_count("narrative", "desire")` |
| Cluster coefficient | Does the vision form a coherent whole? | `cluster_coefficient("narrative")` |
| Ambition drive | Is the citizen driven toward growth? | `drive("ambition")` |
| Narrative recency | Is vision being maintained, not just created? | `recency("narrative")` |

### Layer 2: Universe Graph — Vision in Action

The behavioral signals that indicate vision enacted:

| Signal | What It Means | Observables Used |
|--------|--------------|------------------|
| Spaces created | Does the citizen create new contexts for work? | `spaces_created` |
| Cross-space moments | Does action span multiple domains? | `moments(actor, space_type)` distinct types |
| First-in-space | Does the citizen pioneer new areas? | `first_moment_in_space` |
| Other-actor engagement | Does vision involve others? | `distinct_actors_in_shared_spaces` |
| Proposal moments | Does the citizen propose direction? | `moments` with "proposes" links |
| Self-initiated moments | Is action driven from within? | moments without parent from other actor |

### The Gap: Vision vs. Activity

The scoring pattern follows the parent algorithm's gap analysis:

- **High narrative connectivity + high space creation + cross-actor engagement** = vision enacted at organizational level
- **High narrative connectivity + zero spaces created** = vision trapped in the brain
- **Zero narrative nodes + many commits** = execution without direction
- **Narrative nodes exist but low connectivity** = notes, not vision

---

## TIER PROGRESSION (T5 through T8)

This aspect only has capabilities at T5 and above. This is by design: vision is a higher-order capability.

| Tier | Capability | What the Formula Must Detect |
|------|-----------|------------------------------|
| T5 | vis_define_vision | Narrative nodes exist, are connected to concepts and desires, are recent, and produce at least some action |
| T6 | vis_strategic_thinking | Narratives form strategic clusters (high cluster coefficient), link to many concept types, decisions are documented |
| T6 | vis_org_vision | Vision links extend beyond self: shared spaces, other actors, proposals that shape collective direction |
| T7 | vis_sized_ambitions | Ambition drive is high, narrative-desire links are strong, narratives connect to identity-level concepts (who to become, not just what to do) |
| T8 | vis_civilizational | Maximum connectivity: narratives link across all domains, engage many actors, create new spaces, sustained over time |

Each tier builds on the one below. A citizen scoring well on T8 necessarily scores well on T5-T7.

---

## PRINCIPLES

### Principle 1: Connectivity Over Count

A brain with 100 isolated narrative nodes has less vision than a brain with 5 highly-connected narrative nodes. Count matters, but connectivity matters more. `min_links("narrative", 5)` is a stronger signal than `count("narrative")`.

### Principle 2: Long-Range Links Signal Strategy

Strategic thinking connects distant parts of the graph. A narrative node linked only to nearby concepts is local thinking. A narrative node that links to concepts across multiple domains — that's strategic. `link_count("narrative", "concept")` relative to domain diversity captures this.

### Principle 3: Action Validates Vision

Vision without action is fantasy. The behavior component (60 points) heavily weights whether vision produces observable action: spaces created, proposals made, others engaged. Brain topology alone maxes at 40.

### Principle 4: Organizational and Civilizational Vision Requires Others

vis_org_vision and vis_civilizational cannot score high if the citizen works in isolation. `distinct_actors_in_shared_spaces` and `spaces_created` are essential signals for these capabilities. You cannot have organizational vision without an organization.

### Principle 5: Stagnation Is Visible Through Decay

A vision articulated once and never revisited decays. `recency("narrative")` and `mean_energy("narrative")` capture this. Living vision is maintained, refined, updated. Dead vision is a decaying document.

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| Daily Citizen Health | Parent algorithm — defines the 7 primitives, scoring structure, temporal weighting |
| Personhood Ladder | Defines the 5 capabilities and their tiers |
| Brain topology reader | Provides narrative node counts, energies, links, drives |
| Universe graph reader | Provides moment counts, space data, actor engagement |

---

## SCOPE

### In Scope

- Scoring formulas for 5 vision_strategy capabilities
- Brain topology signals specific to vision (narrative nodes, connectivity)
- Behavioral signals specific to vision (spaces created, proposals, cross-actor)
- Tier-appropriate difficulty scaling (T5 easier than T8)
- Synthetic test profiles for formula validation

### Out of Scope

- Content analysis of narrative nodes (always out of scope)
- Evaluating vision quality or correctness
- Capabilities below T5 (none exist for this aspect)
- Training citizens on how to build vision (future module)

---

## MARKERS

<!-- @mind:todo Validate that narrative node type exists in brain graphs — or determine the actual type name used -->
<!-- @mind:proposition Consider "vision coherence score" as a derived metric from cluster_coefficient("narrative") -->
