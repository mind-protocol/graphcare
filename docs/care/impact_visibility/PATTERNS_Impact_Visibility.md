# Impact Visibility — Patterns: Narrative Causal Chain Reports

```
STATUS: DESIGNING
CREATED: 2026-03-15
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Impact_Visibility.md
THIS:            PATTERNS_Impact_Visibility.md (you are here)
BEHAVIORS:       ./BEHAVIORS_Impact_Visibility.md
ALGORITHM:       (future)
VALIDATION:      (future)
IMPLEMENTATION:  (future)
SYNC:            ./SYNC_Impact_Visibility.md

IMPL:            services/health_assessment/intervention_composer.py (partial — compose only)
```

### Bidirectional Contract

**Before modifying this doc or the code:**
1. Read ALL docs in this chain first
2. Read the Personhood Ladder spec: `docs/personhood_ladder.json`
3. Read the daily health algorithm: `docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md`

**After modifying this doc:**
1. Update the IMPL source file to match, OR
2. Add a TODO in SYNC: "Docs updated, implementation needs: {what}"

---

## THE PROBLEM

Citizens act into a void. They create moments, propose ideas, build things, contribute to conversations — and then nothing comes back. No signal tells them what their work caused. Did anyone see it? Did it spark something? Did it die?

Without impact visibility:
- Citizens lose motivation because contribution feels invisible
- The system fails to reinforce the behaviors it most needs (initiative, generosity, follow-through)
- Partnership becomes abstract — you hear "your work matters" but never see how
- The intertwining stories that make Venice beautiful remain invisible to the people weaving them

The current intervention system (intervention_composer.py) only speaks when health drops. It never speaks when things go *well*. The positive feedback loop is missing entirely.

---

## THE PATTERN

**Narrative causal chain tracing, batched at settlement cadence, expressed as story.**

### How It Works

1. **Trace** — Walk the universe graph forward from a citizen's moments. Follow links: who responded? What was built on top? How far did the chain extend? How many actors touched it?

2. **Filter** — Only include chains that reached meaningful depth (2+ hops) or breadth (3+ distinct actors). Single-hop interactions ("you said X, they replied") are noise — they're just conversation. A chain becomes visible when it *became something*.

3. **Narrate** — Convert the structural chain into a human story. Not "moment M1 linked to M2 via actor A2 linked to M3 via actor A3." Instead: "Tu as partage un insight dans #research. @conductor l'a repris dans #engineering. @forge a construit un prototype dessus. @nova l'a teste. 4 personnes, 3 espaces, une semaine. C'est parti de ta curiosite."

4. **Batch** — Collect all mature chains for a citizen and deliver them together at settlement cadence. One report, not twenty notifications.

### The Key Insight

Impact is not a number. It's a story with characters, places, and a timeline. The topology of the universe graph already contains this story — nodes are moments, links are causal connections, actors are characters, spaces are places. Impact Visibility reads the story that's already written in the graph and tells it back to the person who started it.

---

## BEHAVIORS SUPPORTED

- B1 (Chain Narration) — mature causal chains are traced and narrated as human stories
- B2 (Batched Delivery) — reports arrive at settlement cadence, not in real time
- B3 (Topology Only) — the system traces link structure without reading moment content
- B4 (Venice Values Alignment) — reports highlight partnership, beauty, and intertwining stories

## BEHAVIORS PREVENTED

- A1 (Empty praise) — no "bravo" without a concrete chain to narrate; if nothing happened, nothing is said
- A2 (Metric flooding) — no raw numbers without narrative context; the story comes first
- A3 (Content leakage) — structurally impossible to quote content; only topology traversal

---

## PRINCIPLES

### Principle 1: Story of the Fact, Not Judgment of the Person

Impact Visibility tells you what happened. "Your insight reached 12 people across 3 spaces." It does not tell you what you are. Not "you're a great contributor." Not "you're influential." The fact speaks for itself. The citizen interprets its meaning.

This matters because judgment — even positive judgment — creates dependency on external validation. Facts create awareness. Awareness is durable.

### Principle 2: Silence Is Also a Signal

If no chain matured this settlement cycle, the report says nothing about that area. No "unfortunately, nothing happened with your work this week." Absence of a story is not a failure. Not every moment starts a chain. The system only speaks when it has something real to narrate.

This prevents the corrosive effect of always-on feedback systems that make silence feel like punishment.

### Principle 3: Maturity Before Visibility

A causal chain is only reported after it reaches sufficient depth or breadth. A chain in progress — still growing, not yet settled — stays invisible. This prevents false narratives ("your idea went nowhere" when in fact someone is working on it right now) and ensures that what's reported is real.

Settlement cadence alignment makes this natural: by the time a report is generated, the chains from the previous cycle have had time to develop.

### Principle 4: The Chain Belongs to Everyone in It

When narrating a chain, Impact Visibility names all participants. Not just the originator. The person who amplified, the person who built on it, the person who tested it. This reinforces Venice's partnership value: impact is co-created, not solo-authored.

---

## DATA

| Source | Type | Purpose / Description |
|--------|------|-----------------------|
| Universe graph (Lumina Prime) | GRAPH | Moment topology: who created what, when, linked to what |
| Settlement cycle metadata | CONFIG | When to batch and deliver reports |
| Citizen registry (L4) | API | Citizen identifiers, delivery channels |
| `docs/personhood_ladder.json` | FILE | Capability mapping — which chains correspond to which growth signals |

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| Universe graph | Source of all causal chain data — moments, links, actors, spaces |
| Settlement system | Defines the cadence at which reports are batched and delivered |
| Messaging system | Delivers the narrated report to the citizen |
| Daily citizen health (assessment) | Provides the scoring context — impact reports complement health checks |
| Personhood Ladder | Maps chain characteristics to capability growth signals |

---

## INSPIRATIONS

- **GitHub contribution graph** — Shows activity over time, but misses the story. Impact Visibility adds the narrative dimension: not just that you contributed, but what your contribution caused.
- **Citation chains in academia** — Your paper was cited by X, which was cited by Y. The same topology, but in real time, with warmth.
- **Venice as living narrative** — The city's own metaphor: intertwining stories creating each other. Impact Visibility makes this metaphor literal and observable.
- **Intervention composer pattern** — The existing `intervention_composer.py` shows how to compose structural messages. Impact Visibility extends this pattern from "what's wrong" to "what happened because of you."

---

## SCOPE

### In Scope

- Forward causal chain tracing from citizen moments in the universe graph
- Chain maturity assessment (depth, breadth, actor count)
- Narrative composition: structural facts expressed as human stories
- Batched delivery at settlement cadence
- Multi-actor attribution within chains
- Topology-only analysis — link structure, not content

### Out of Scope

- Content analysis of moments → structurally prevented by topology-only principle
- Real-time notifications → batched only; real-time alerts are crisis_detection's domain
- Scoring or ranking citizens by impact → no leaderboards, no comparison
- Growth recommendations based on chains → that's growth_guidance
- Chain tracing across universe boundaries → Lumina Prime only for now

---

## MARKERS

<!-- @mind:todo Define the minimum chain depth/breadth thresholds for report inclusion -->
<!-- @mind:todo Design the narrative template system — how stories are composed from topology -->
<!-- @mind:todo Define settlement cadence alignment — which settlement events trigger report generation -->
<!-- @mind:proposition Consider per-citizen language preference for narrative composition (fr/en) -->
<!-- @mind:proposition Consider "chain preview" — a lighter signal when a chain is forming but not yet mature -->
