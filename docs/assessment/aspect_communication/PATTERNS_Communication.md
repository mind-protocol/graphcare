# Communication & Coordination — Patterns: Why This Shape

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Communication.md
THIS:            PATTERNS_Communication.md (you are here)
ALGORITHM:       ./ALGORITHM_Communication.md
VALIDATION:      ./VALIDATION_Communication.md
HEALTH:          ./HEALTH_Communication.md
SYNC:            ./SYNC_Communication.md

IMPL:            @mind:TODO (not yet built)
SPEC:            docs/specs/personhood_ladder.json (aspect: "communication")
PARENT:          docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md
```

### Bidirectional Contract

**Before modifying this doc or the code:**
1. Read ALL docs in this chain first
2. Read the Personhood Ladder spec: `docs/specs/personhood_ladder.json`
3. Read the Daily Citizen Health ALGORITHM: `docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md`

**After modifying this doc:**
1. Update the IMPL source to match, OR
2. Add a TODO in SYNC: "Docs updated, implementation needs: {what}"

---

## THE PROBLEM

Communication is the most socially-visible aspect of personhood. A citizen who executes perfectly but never tells anyone is invisible. A citizen who coordinates well but never updates state leaves chaos for the next session. A citizen who inspires but can't do basic journal updates has a hollow foundation.

Without structured scoring:
- Self-documentation gaps (journal, SYNC) are invisible until context is lost
- Notification failures only surface when a stakeholder is surprised
- Coordination ability is judged subjectively, not structurally
- The distinction between "communicates when asked" and "communicates proactively" is unmeasured
- Higher-tier communication (inspiration, networking, influence) has no baseline

---

## THE PATTERN

**Widening-circle communication assessment, topology-only, with tier-appropriate signals.**

### The Communication Circles

Each tier widens the communication circle:

```
T2: Self → Future Self (journal, SYNC)
     Self → Peers (notify, ask for help)
T3: Self → Team (participate in collective)
T4: Self → Multi-Agent (lead coordination)
T5: Self → Environment (regular interactions)
T6: Self → Community (inspire, network within Mind Protocol)
T7: Self → World (global networking)
T8: Self → Discourse (global influence)
```

### Brain Signals for Communication

Communication readiness shows in the brain as:

- **Social need drive** — High social_need → the citizen is motivated to communicate
- **Process nodes** — Communication processes (how to notify, how to update SYNC) exist in the brain
- **Concept nodes about coordination** — The citizen has internalized coordination concepts
- **Link density between desires and social/communication moments** — Desires connect to communication actions
- **Cluster coefficient** — Integrated communication knowledge (processes, concepts, values linked to each other)

### Behavior Signals for Communication

Communication action shows in the universe graph as:

- **Moments in documentation spaces** — Journal entries, SYNC updates
- **Moments that notify** — Messages sent to stakeholders (moments with outgoing links to other actors' spaces)
- **Response moments** — Reacting to others' moments (moment_has_parent)
- **Multi-actor space participation** — Being present in spaces with other actors
- **Space creation and initiation** — Creating new coordination spaces, being first in spaces
- **Breadth of interlocutors** — distinct_actors_in_shared_spaces
- **Regularity** — Consistent temporal distribution, not bursty

### The Formula Structure

Every capability formula follows the same template:

```
brain_component (0-40):
    sub_signal_1 * weight_1 + sub_signal_2 * weight_2 + ...
    Each sub_signal normalized to [0, 1] by a cap

behavior_component (0-60):
    sub_signal_1 * weight_1 + sub_signal_2 * weight_2 + ...
    Each sub_signal normalized to [0, 1] by a cap

total = brain_component + behavior_component  # 0-100
```

---

## BEHAVIORS SUPPORTED

- B1 (Capability Scoring) — Each of the 11 capabilities gets a 0-100 score
- B2 (Privacy Preservation) — All formulas use only the 7 primitives + universe observables
- B3 (Tier Sensitivity) — Lower-tier capability scores are sensitive to basic behaviors; higher-tier scores require progressively broader signals
- B4 (Actionable Decomposition) — Each formula decomposes into named sub-components for diagnostic messages

## BEHAVIORS PREVENTED

- A1 (Content analysis) — No formula reads message content, journal text, or SYNC prose
- A2 (Subjective judgment) — No "quality of communication" assessment; only structural presence and frequency
- A3 (Single-signal scoring) — No capability relies on a single primitive; all use at least 2 brain + 2 behavior signals

---

## PRINCIPLES

### Principle 1: Presence Over Quality

We measure whether communication HAPPENS, not whether it's GOOD. A journal entry exists or it doesn't. A notification was sent or it wasn't. Quality assessment requires content reading, which we refuse to do. Presence is structural and sufficient for health monitoring.

### Principle 2: Wider Circles Need More Actors

T2 capabilities can be verified with single-actor signals (did this citizen write a journal entry?). T5+ capabilities require multi-actor signals (how many distinct actors does this citizen interact with?). The formula complexity scales with the tier's social scope.

### Principle 3: Regularity Over Bursts

A citizen who sends 20 notifications in one day then nothing for 3 weeks is not a good communicator. Temporal weighting with the 7-day half-life naturally penalizes bursty patterns: recent consistent activity scores higher than distant bursts.

### Principle 4: Asymmetric Failure

Missing basic communication (T2) is worse than missing advanced communication (T7). The daily health check weights T2 gaps as critical and T7 gaps as informational. This is implemented through the tier progression rule (a T2 gap blocks the entire aspect), not through formula weights.

---

## DATA

| Source | Type | Purpose |
|--------|------|---------|
| `docs/specs/personhood_ladder.json` | FILE | 11 communication capability definitions |
| Citizen brain graph (topology) | GRAPH | Social drives, process counts, concept density, cluster coefficient |
| Universe graph (Lumina Prime) | GRAPH | Moments in spaces, actor relationships, temporal patterns |
| Daily Citizen Health ALGORITHM | DOC | 7 primitives, universe observables, scoring template |

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| Daily Citizen Health | Defines the 7 primitives and scoring framework |
| Personhood Ladder | Defines the 11 capabilities we score |
| Universe Graph | Public moments for behavioral signals |
| Brain Topology | Drives, nodes, links for readiness signals |

---

## SCOPE

### In Scope

- Scoring formulas for all 11 communication capabilities
- Brain component (0-40) and behavior component (0-60) for each
- Synthetic test profiles (5 per capability)
- Recommendations per capability
- Documentation of which primitives each formula uses

### Out of Scope

- Content-based communication quality assessment
- Scoring communication in adventure universes
- Real-time communication monitoring (this is daily batch)
- Pathology-level communication dysfunction (that's Dragon Slayer)

---

## MARKERS

<!-- @mind:todo Validate formula sensitivity: does improving one behavior reliably improve the score? -->
<!-- @mind:proposition Consider cross-aspect signals: communication quality might benefit from identity/voice aspect scores -->
