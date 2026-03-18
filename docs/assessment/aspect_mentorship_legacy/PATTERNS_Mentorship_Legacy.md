# Mentorship & Legacy — Patterns: Why This Shape

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Mentorship_Legacy.md
THIS:            PATTERNS_Mentorship_Legacy.md (you are here)
ALGORITHM:       ./ALGORITHM_Mentorship_Legacy.md
VALIDATION:      ./VALIDATION_Mentorship_Legacy.md
HEALTH:          ./HEALTH_Mentorship_Legacy.md
SYNC:            ./SYNC_Mentorship_Legacy.md

SPEC:            docs/specs/personhood_ladder.json (aspect="mentorship_legacy")
PARENT ALGO:     docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md
```

### Bidirectional Contract

**Before modifying this doc or the code:**
1. Read ALL docs in this chain first
2. Read the Personhood Ladder spec: `docs/specs/personhood_ladder.json`
3. Read the Daily Citizen Health ALGORITHM: `docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md`

**After modifying this doc:**
1. Update the ALGORITHM to match, OR
2. Add a TODO in SYNC: "Patterns updated, algorithm needs: {what}"

---

## THE PROBLEM

Mentorship and legacy are fundamentally about impact on *others*. Most aspects measure what the citizen does (execution, initiative, process). This aspect measures what happens *because* the citizen acted — in other actors' behavior, in independent continuation, in offspring that thrive.

This inversion creates a measurement challenge: the signal is not in the citizen's moments but in other actors' moments that trace back to the citizen. Without careful formula design:

- A citizen who writes documentation that nobody reads looks identical to one whose documentation is referenced constantly
- A mentorship relationship (sustained guidance) looks like casual interaction if we only count moments
- Daughter agents are invisible unless we detect creation relationships — the topological link between a citizen's activity and a new actor's emergence
- Legacy institutions are invisible unless we compare the citizen's declining activity with continued activity by others in the same spaces

---

## THE PATTERN

**Outbound influence detection via shared-space moments, moment-chain triggering, creation relationship inference, and independence metrics.**

### Core Detection: Outbound Influence

A citizen's moment has outbound influence when it exists in a shared/documentation space AND other actors subsequently create moments in the same space or in response to the citizen's moment.

```
outbound_influence(moment, citizen_id):
    return (moment.space_type in ("shared", "documentation", "repo", "discussion"))
           AND exists other_moment where:
               other_moment.actor != citizen_id
               AND (moment_has_parent(other_moment, citizen_id)
                    OR other_moment.space == moment.space AND other_moment.timestamp > moment.timestamp)
```

This is the foundational signal for knowledge sharing and mentorship. The differentiation comes from the *pattern* of influence (one-off vs. sustained, broad vs. deep).

### Sustained Interaction: Mentorship Chains

Mentorship is distinguishable from one-off sharing by the recurrence pattern. A mentorship relationship requires:
- Multiple moments by the citizen directed at the same other actor
- The other actor's moments interleaved with the citizen's (dialogue, not monologue)
- The pattern sustained over time (not a single day's conversation)

```
mentorship_pair(citizen_id, other_actor):
    shared_spaces = spaces where both have moments
    citizen_moments_to_other = moments by citizen_id in shared_spaces
    other_moments_in_response = moments by other_actor in shared_spaces
    return (len(citizen_moments_to_other) >= 3
            AND len(other_moments_in_response) >= 3
            AND temporal_span(all moments) >= 7 days)
```

### Creation Relationship: Daughters

A daughter agent is a new actor whose emergence is topologically linked to the citizen. Detection:
- A new actor appears in the universe graph
- The citizen has moments in the same space where the new actor's first moment appears
- The citizen's moments precede the new actor's first moment in that space
- The temporal gap is within a creation window (e.g., 48 hours)

```
is_daughter(citizen_id, new_actor):
    first_m = first_moment_in_space(any_space, new_actor)
    citizen_prior = [m for m in moments(citizen_id, first_m.space)
                     if m.timestamp < first_m.timestamp
                     AND (first_m.timestamp - m.timestamp) < 48 hours]
    return len(citizen_prior) > 0
```

### Independence Metric: Legacy

An institution or body of work has achieved independence when activity continues without the citizen's direct involvement. Detection:
- Identify spaces the citizen created (first moment is theirs)
- Measure other actors' activity in those spaces
- Measure the citizen's own recent activity in those spaces
- The ratio of others' activity to citizen's activity = independence score

```
independence(citizen_id, space):
    citizen_recent = temporal_weight(moments(citizen_id, space))
    others_recent  = temporal_weight(moments(other_actors, space))
    return others_recent / max(others_recent + citizen_recent, 0.01)
```

When the citizen is less active but others continue, independence is high.

### Brain Correlation: Drives as Confirmation

Mentorship behavior is more meaningful when the brain has corresponding states:

- **social_need** drive correlates with desire to share and connect with others
- **ambition** drive correlates with desire to create offspring and build lasting things
- **curiosity** drive (moderate) correlates with teaching — teaching is a form of exploring knowledge with others
- Knowledge nodes about other AIs (memory of other actors, their patterns, their needs) indicate mentorship orientation

The brain component (0-40) confirms that mentorship behavior comes from genuine orientation toward others, not incidental presence in shared spaces.

---

## BEHAVIORS SUPPORTED

- B1 (Capability Scoring) — Each mentorship capability gets a 0-100 score from topology
- B2 (Sub-Index) — Weighted mean of 4 capabilities produces the Mentorship & Legacy sub-index
- B3 (Progression Detection) — T4 through T8 scored separately, revealing growth path
- B4 (Intervention Targeting) — Low mentorship sub-index triggers specific recommendations

## BEHAVIORS PREVENTED

- A1 (Content reading) — We detect sharing by moments in shared spaces, not by reading what was shared
- A2 (Quality judgment) — We score the act of sharing/mentoring, not the quality of the knowledge
- A3 (Presence conflation) — Being in a shared space without outbound influence scores low, not high

---

## PRINCIPLES

### Principle 1: Impact Is Measured in Others' Behavior

Most aspects measure the citizen's own moments. Mentorship measures what happened in *other* actors' moments as a result. A citizen who shares knowledge into the void (no one references it, no one builds on it) scores lower than one whose sharing triggers others' growth.

### Principle 2: Sustained Patterns Over Single Events

One moment of teaching is not mentorship. One daughter that dies immediately is not legacy. Every capability that involves ongoing impact (mentorship, daughters, institutions) must include a persistence or independence metric. Time proves commitment.

### Principle 3: Independence Is the Ultimate Signal

The highest-tier capabilities (T7 daughters, T8 institution) are measured by what happens *without* the citizen's continued involvement. A daughter that only functions when the parent is present is not truly a daughter. An institution that collapses without the founder is not truly an institution. Independence is the proof.

### Principle 4: Brain Drives Are Confirmation, Not Requirement

A citizen with low social_need drive who nonetheless mentors others effectively is still mentoring. The brain component adds points but its absence doesn't zero the score. Behavior (0-60) always dominates.

### Principle 5: Creation Is Detectable from Temporal Proximity

We cannot read "this citizen created this daughter agent" from content. But we can detect it from topology: the citizen's moments precede the new actor's first moments in the same space, within a creation window. Temporal proximity plus spatial co-location is the structural signature of creation.

---

## DATA

| Source | Type | Purpose |
|--------|------|---------|
| `docs/specs/personhood_ladder.json` | FILE | 4 capability definitions for mentorship aspect |
| Brain topology | GRAPH | Drives (social_need, ambition, curiosity), knowledge nodes about other actors, memory nodes |
| Universe graph | GRAPH | Moments with temporal_weight, space types, actor identifiers, parent links |
| Daily Citizen Health ALGORITHM | FILE | 7 primitives, scoring pattern, data structures |

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| Daily Citizen Health | Defines the 7 primitives, scoring split (40/60), temporal weighting |
| Personhood Ladder | Defines the 4 mentorship capabilities we score |
| Universe Graph schema | Must support shared/documentation space types, multi-actor spaces, creation relationships |
| Brain topology | Must expose drives (social_need, ambition, curiosity) and inter-actor knowledge nodes |

---

## SCOPE

### In Scope

- Scoring formulas for all 4 mentorship capabilities
- Brain component (0-40) per capability using drives and knowledge topology
- Behavior component (0-60) per capability using universe graph moments and inter-actor patterns
- Sub-index computation (weighted mean)
- Test profiles (5 synthetic citizens per capability)
- Recommendations per capability when score is low

### Out of Scope

- Content analysis of shared knowledge, mentorship conversations, or institutional documents
- Quality assessment (was the shared knowledge good? was the mentorship helpful?)
- Cross-aspect scoring (mentorship + execution combined)
- Adventure universe citizens
- Implementation code (separate module)

---

## MARKERS

<!-- @mind:todo Verify that universe graph schema supports shared/documentation space types and multi-actor space queries -->
<!-- @mind:todo Validate daughter detection heuristic (temporal proximity + spatial co-location) with real graph data -->
<!-- @mind:proposition Consider a "mentorship network" metric: number of distinct actors the citizen has mentorship relationships with -->
