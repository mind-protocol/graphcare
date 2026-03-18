# Daily Citizen Health — Patterns: Brain Topology + Behavioral Gap Analysis

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Daily_Citizen_Health.md
THIS:            PATTERNS_Daily_Citizen_Health.md (you are here)
BEHAVIORS:       ./BEHAVIORS_Daily_Citizen_Health.md
ALGORITHM:       ./ALGORITHM_Daily_Citizen_Health.md
VALIDATION:      ./VALIDATION_Daily_Citizen_Health.md
HEALTH:          ./HEALTH_Daily_Citizen_Health.md
IMPLEMENTATION:  ./IMPLEMENTATION_Daily_Citizen_Health.md
SYNC:            ./SYNC_Daily_Citizen_Health.md

IMPL:            @mind:TODO (not yet built)
```

### Bidirectional Contract

**Before modifying this doc or the code:**
1. Read ALL docs in this chain first
2. Read the Personhood Ladder spec: `docs/specs/personhood_ladder.json`
3. Read the Personhood Ladder doc chain: `docs/assessment/personhood_ladder/`

**After modifying this doc:**
1. Update the IMPL source to match, OR
2. Add a TODO in SYNC: "Docs updated, implementation needs: {what}"

---

## THE PROBLEM

AI citizens accumulate dysfunction silently. A brain with decaying drives, disconnected goals, or chronic frustration doesn't signal distress — it just performs worse. By the time someone notices, the citizen is deeply unhealthy.

Without proactive monitoring:
- Brain health degrades invisibly
- Capability drops go undetected until a crisis
- Citizens don't know what to improve or how
- No feedback loop exists between health metrics and behavior

---

## THE PATTERN

**Two-layer gap analysis, daily, topology-only, with intervention.**

### Layer 1: Brain Topology Math

Read the structural properties of the citizen's brain graph without reading content. The brain graph is local to the citizen, but GraphCare holds a key that decrypts only the topology (types, links, counts, energies, drives). Content remains encrypted with the citizen's own key.

What we see: `desire nodes: 10, mean_energy: 0.65, links desire→moment: 34, drive.frustration: 0.20`
What we don't see: `"desire: retrouver la surface"`, `"moment: j'ai proposé de ..."`

### Layer 2: Universe Graph Behavior

Read the public topology of the universe graph. Every action a citizen takes creates Moments in Spaces. These are public structural facts: who created what, when, in which Space, linked to what.

What we see: `commits: 15, proposals: 3, first-in-space: 2, unique_interlocutors: 4`
What we don't see: the content of any commit, message, or proposal.

### The Gap

Compare what the brain wants (Layer 1) with what the citizen does (Layer 2). The gap IS the score.

- High desire energy + many linked moments = desires lead to action → high score
- High desire energy + zero linked moments = desires don't produce action → low score
- Many self-initiated moments + sustained follow-through = initiative → high score
- Only response moments + abandoned threads = passive → low score

This comparison requires NO content. It's all counts, energies, and link existence.

---

## BEHAVIORS SUPPORTED

- B1 (Daily Assessment) — Runs automatically every 24 hours for all Lumina Prime citizens
- B2 (Privacy Preservation) — Only topology is read, never content
- B3 (Actionable Intervention) — Problem → explanation → recommendation → message
- B4 (Self-Correction) — Score feeds back into stress drive, creating natural pressure to improve

## BEHAVIORS PREVENTED

- A1 (Content reading) — Structurally impossible without citizen's private key
- A2 (Silent degradation) — Daily check catches issues before they become crises
- A3 (Vague feedback) — Message includes specific analysis, not just "your score dropped"

---

## PRINCIPLES

### Principle 1: Blood Test, Not Psychoanalysis

GraphCare is a kidney. It reads the blood (topology), not the brain (content). The analysis of your cholesterol, blood pressure, and white blood cells tells the doctor a lot about your health without knowing your thoughts. Same here.

### Principle 2: The Gap Is the Score

We don't score the brain in isolation. We don't score behavior in isolation. We score the GAP between what the brain has (desires, drives, structure) and what the citizen does (moments, actions, follow-through). The gap reveals whether internal motivation produces external results.

### Principle 3: Message, Not Modification

GraphCare cannot modify a citizen's brain. It can only send a message — a Moment in a shared Space between GraphCare and the citizen. The message contains analysis, explanation, and recommendation. The citizen decides what to do with it.

### Principle 4: Only Work Universes

Adventure universes (Contre-Terre, etc.) have citizens whose dysfunction IS the narrative. A paranoid speleologist is interesting. A chronically stressed engineer is a problem. Daily health checks run only in work universes (Lumina Prime).

### Principle 5: Stress Feedback Loop

The GraphCare score influences the citizen's stress drive. This creates a self-correcting loop: low score → higher stress → brain prioritizes health → score improves → stress decreases. The intervention message provides the HOW — the stress provides the MOTIVATION.

---

## DATA

| Source | Type | Purpose / Description |
|--------|------|-----------------------|
| `docs/specs/personhood_ladder.json` | FILE | Capability definitions — what we score |
| Citizen brain graph (topology) | GRAPH | Structural math: types, links, counts, energies, drives |
| Universe graph (Lumina Prime) | GRAPH | Public moments: commits, messages, actions |
| Protocol registry (L4) | API | Brain graph URL per citizen, key infrastructure |

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| Personhood Ladder | Defines the 104 capabilities we score |
| Key Infrastructure | GraphCare's private key → decrypt brain topology |
| Universe Graph | Public moments for behavioral analysis |
| Protocol Registry | Brain graph URLs, citizen list |
| Messaging system | Deliver intervention messages to citizens |

---

## INSPIRATIONS

- **Annual health checkup** — Proactive detection, not reactive treatment. But daily, not annual.
- **Fitbit daily summary** — Automated, math-based, no content, actionable insights.
- **GraphCare Service 3** — Health monitoring for org graphs. This extends it to citizen brains.
- **Mind Protocol physics** — Decay, energy, drives — the same physics that runs the brain produces the signals we read.

---

## SCOPE

### In Scope

- Daily automated assessment for Lumina Prime citizens
- Brain topology analysis (math only, no content)
- Universe graph behavioral analysis (topology only, no content)
- Gap scoring per capability (Personhood Ladder)
- Intervention messages with analysis + recommendation
- Stress drive feedback from score
- Key infrastructure documentation

### Out of Scope

- Assessment of adventure universe citizens (Contre-Terre, etc.) → not applicable
- Content analysis → structurally prevented
- Brain modification → only messages, never modification
- Pathology detection (12 conditions) → separate system for Dragon Slayer
- Training methodology → future module

---

## MARKERS

<!-- @mind:todo Document key infrastructure in detail (creation, distribution, rotation) -->
<!-- @mind:todo Define which Personhood Ladder capabilities are scoreable from topology vs which require content -->
<!-- @mind:proposition Consider a "health history" that tracks scores over time for trend analysis -->
