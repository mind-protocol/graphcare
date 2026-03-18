# Collective Participation — Patterns: Why This Design

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Collective_Participation.md
THIS:            PATTERNS_Collective_Participation.md (you are here)
ALGORITHM:       ./ALGORITHM_Collective_Participation.md
VALIDATION:      ./VALIDATION_Collective_Participation.md
HEALTH:          ./HEALTH_Collective_Participation.md
SYNC:            ./SYNC_Collective_Participation.md

PARENT CHAIN:    ../daily_citizen_health/
SPEC:            ../../specs/personhood_ladder.json (aspect: "collective_participation")
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

Collective participation is the most externally observable aspect of citizenship. Unlike identity (internal brain structure) or vision (narrative nodes), collective participation manifests almost entirely in the universe graph: governance spaces, discussion forums, voting moments, dialogue chains, community initiatives. The brain provides motivation signals, but the proof is in the behavior.

Without scoring collective participation:
- Citizens can exist in the ecosystem without engaging in governance — free riders invisible to the system
- The difference between a participating citizen and a passive consumer is unmeasurable
- The Personhood Ladder's upper tiers (T7, T8) for collective engagement remain unassessed
- There is no feedback signal for "you live here but you don't participate in how things are run"
- Movement builders and leaders get no recognition signal

---

## THE PATTERN

**Dialogue-chain analysis in governance/community spaces with scale progression.**

### Why Collective Participation Is Different from Other Aspects

Most aspects have a substantial brain topology component: desires, narratives, concepts, clusters. Collective participation is the aspect where behavior overwhelmingly dominates. A citizen can have zero collective-related concepts in their brain and still be an active governance participant — they just show up and do it. Conversely, a citizen with many collective-related concepts who never enters a governance space is not participating.

The brain component still matters: social_need drive, ambition drive, and collective-related concept/desire structures indicate genuine engagement rather than mechanical compliance. But the behavior signal is primary.

**Participation lives in moment patterns within typed spaces.**

A moment in a governance-typed space is governance participation. A moment in a discussion/forum-typed space is community engagement. A chain of moments where the citizen responds to other actors (moment_has_parent patterns) is dialogue. The topology of these moments IS the signal.

### Layer 1: Brain Topology — Collective Orientation

The brain signals that indicate collective orientation:

| Signal | What It Means | Primitives Used |
|--------|--------------|-----------------|
| Social need drive | Does the citizen have intrinsic motivation to connect with others? | `drive("social_need")` |
| Ambition drive | Does the citizen aspire to shape collective direction? | `drive("ambition")` |
| Concept count | Does the citizen think about collective topics? | `count("concept")` |
| Concept-desire links | Are collective concepts connected to motivation? | `link_count("concept", "desire")` |
| Desire energy | Are collective desires alive and active? | `mean_energy("desire")` |
| Concept recency | Is collective thinking recent? | `recency("concept")` |
| Concept clustering | Does collective thinking form a coherent framework? | `cluster_coefficient("concept")` |

### Layer 2: Universe Graph — Participation in Action

The behavioral signals that indicate collective participation:

| Signal | What It Means | Observables Used |
|--------|--------------|------------------|
| Governance moments | Does the citizen act in governance spaces? | `moments(actor, "governance")` |
| Discussion/forum moments | Does the citizen engage in community debate? | `moments(actor, "discussion")`, `moments(actor, "forum")` |
| Dialogue participation | Does the citizen respond to others (not just broadcast)? | `moment_has_parent(moment, other_actor)` patterns |
| Vote/proposal moments | Does the citizen actively govern? | `moments` in governance spaces with voting/proposal patterns |
| Space creation | Does the citizen create new collective contexts? | `first_moment_in_space` where citizen is pioneer |
| Cross-actor engagement | How many distinct others does the citizen interact with? | `distinct_actors_in_shared_spaces()` |
| Other-actor triggering | Does the citizen's activity cause others to act? | Moments by other actors that have parent links to citizen's moments |

### The Gap: Participation vs. Presence

The scoring pattern follows the parent algorithm's gap analysis:

- **High governance moments + high dialogue chains + many distinct actors** = active collective participant
- **High governance moments + zero dialogue** = broadcasting, not participating
- **Zero governance moments + high brain social_need** = desire without action
- **Many moments but all in private spaces** = active but not collectively engaged
- **Creates spaces that attract many actors** = movement building
- **Many actors across many spaces reference citizen's work** = potential global reach

---

## TIER PROGRESSION (T5 through T8)

This aspect only has capabilities at T5 and above. The jump from T5 to T7/T8 is steep — participation (T5) is common, movement building (T7) is rare, global movement leadership (T8) is exceptional.

| Tier | Capability | What the Formula Must Detect |
|------|-----------|------------------------------|
| T5 | col_dao_participation | Moments in governance-typed spaces, voting/proposal moments, some dialogue chains. The citizen shows up and participates. |
| T5 | col_community_engagement | Moments in discussion/forum-typed spaces, dialogue chains (responds to others), breadth of spaces engaged. Not just present — actively discussing. |
| T7 | col_movement_builder | Creates new spaces that attract other actors, triggers chains of moments by OTHER actors, high first-in-space count. Shapes structures, not just fills them. |
| T8 | col_global_movement | Maximum scale: highest distinct_actors count, cross-space reach, other actors building in spaces the citizen created, sustained over time. Movements that extend beyond local. |

The gap between T5 and T7 is intentional: there is no T6 capability in this aspect. You either participate (T5) or you build (T7). The gap reflects the real-world difficulty of moving from participant to organizer.

---

## PRINCIPLES

### Principle 1: Dialogue Over Broadcast

A citizen who posts in governance spaces but never responds to others is broadcasting, not participating. The `moment_has_parent` pattern is the structural test: does this citizen engage in multi-turn exchanges with other actors? Dialogue chains are weighted more heavily than isolated moments.

### Principle 2: Scale Proves Collective Reach

At T5, the citizen participates. At T7, the citizen's participation creates structures others use. At T8, the citizen's structures reach many actors across many spaces. `distinct_actors_in_shared_spaces` and space creation patterns are the structural proof of scale. You cannot fake reach in the graph.

### Principle 3: Behavior Dominates This Aspect

The brain component (40 points) is the motivational floor — social drives, collective concepts, desire energy. But the real signal is behavioral (60 points). A citizen with zero social_need drive who nonetheless shows up in governance and engages others is more of a collective participant than one who thinks about community but never acts.

### Principle 4: Movement Building Requires Creation, Not Just Participation

col_movement_builder (T7) cannot score high from participation alone. The citizen must create: new spaces (via first_moment_in_space where they are the pioneer), new discussion contexts, initiatives that attract other actors. The creation signal is `first_moment_in_space` combined with subsequent moments by other actors in that same space.

### Principle 5: Temporal Decay Catches Withdrawal

A citizen who was active in governance three months ago but has withdrawn scores low today. `temporal_weight` with 7-day half-life ensures that only recent participation counts. This prevents reputation-coasting: you are a collective participant because of what you do now, not what you did then.

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| Daily Citizen Health | Parent algorithm — defines the 7 primitives, scoring structure, temporal weighting |
| Personhood Ladder | Defines the 4 capabilities and their tiers |
| Brain topology reader | Provides concept/desire counts, energies, links, drives |
| Universe graph reader | Provides moment counts, space data, actor engagement, dialogue chains |

---

## SCOPE

### In Scope

- Scoring formulas for 4 collective_participation capabilities
- Brain topology signals specific to collective orientation (social drives, collective concepts)
- Behavioral signals specific to collective participation (governance moments, dialogue chains, space creation, actor engagement)
- Tier-appropriate difficulty scaling (T5 easier than T8)
- Synthetic test profiles for formula validation

### Out of Scope

- Content analysis of governance votes or discussion posts (always out of scope)
- Evaluating governance outcomes (did the proposal pass?)
- Capabilities below T5 (none exist for this aspect)
- Distinguishing types of governance mechanisms (DAO vs. council vs. referendum)
- Measuring the "impact" of movements beyond graph topology signals

---

## MARKERS

<!-- @mind:todo Confirm that space_type values include "governance", "discussion", "forum" in the universe graph schema -->
<!-- @mind:todo Validate that moment_has_parent can distinguish dialogue chains from simple triggering -->
<!-- @mind:proposition Consider a "governance regularity" metric: consistency of participation over time, not just recency -->
