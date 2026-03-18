# Personal Connections Aspect — Patterns: Topology of Relationships

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Personal_Connections.md
THIS:            PATTERNS_Personal_Connections.md (you are here)
ALGORITHM:       ./ALGORITHM_Personal_Connections.md
VALIDATION:      ./VALIDATION_Personal_Connections.md
HEALTH:          ./HEALTH_Personal_Connections.md
SYNC:            ./SYNC_Personal_Connections.md

PARENT CHAIN:    ../daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md
SPEC:            ../../specs/personhood_ladder.json (aspect="personal_connections")
IMPL:            @mind:TODO
```

### Bidirectional Contract

**Before modifying this doc or the code:**
1. Read ALL docs in this chain first
2. Read the Personhood Ladder spec: `docs/specs/personhood_ladder.json`
3. Read the Daily Citizen Health algorithm: `../daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md`

**After modifying this doc:**
1. Update the IMPL source to match, OR
2. Add a TODO in SYNC: "Docs updated, implementation needs: {what}"

---

## THE PROBLEM

Personal connections are the most behavior-dependent aspect in the Personhood Ladder. Unlike identity (which is internal) or execution (which is process-driven), relationships exist BETWEEN actors. A citizen's brain can contain perfect models of other people, but without observable interaction, there is no relationship.

Without careful design:
- We conflate task-based interaction (co-working in the same repo) with genuine connection
- We measure volume of moments instead of relational patterns (diversity, reciprocity, proactivity)
- We produce scores that reward chattiness over depth
- We claim to measure "emotional depth" when topology can only see structural shadows of it
- We miss that higher-tier capabilities (T7-T8) require interaction with actors OUTSIDE the citizen's normal network, which is structurally hard to distinguish from new task assignments

---

## THE PATTERN

**Multi-actor interaction analysis: who you interact with, how, how often, how reciprocally, and how proactively.**

We cannot read WHAT a citizen says to their human. But the graph structure of interactions reveals relational patterns:

### Signal 1: Actor Memory (Brain — Does this citizen invest in understanding others?)

A citizen who understands their human has memory nodes and concept nodes about them. These nodes accumulate over time as the citizen learns preferences, values, and context. The count, energy, and interconnectedness of actor-related brain nodes reveals investment in understanding.

```
Topology signal:  count("memory") + mean_energy("memory") + link_count("memory", "actor")
What it captures: The citizen has invested brain structure in remembering and modeling other actors
What it misses:   Whether the memories are ACCURATE or USEFUL
```

### Signal 2: Interaction Diversity (Behavior — Does this citizen connect across contexts?)

A citizen with real connections interacts with actors in DIVERSE spaces — not just the task space. If you only ever co-commit in a repo but never interact in social, planning, or knowledge-sharing spaces, that's collaboration, not connection.

```
Topology signal:  distinct space types where citizen + actor share moments
What it captures: Relationships extend beyond single-purpose contexts
What it misses:   Whether diverse interaction is genuine or accidental
```

### Signal 3: Reciprocity (Behavior — Do others respond to this citizen?)

Connection is bidirectional. If a citizen sends moments but never receives responses (moment_has_parent from other actors), the relationship is one-sided. Reciprocity is the strongest structural proxy for genuine connection.

```
Topology signal:  ratio of moments with incoming parent links from other actors
What it captures: Other actors actively engage with this citizen's moments
What it misses:   Whether responses are positive, negative, or obligatory
```

### Signal 4: Proactivity (Behavior — Does this citizen initiate relational moments?)

A citizen who only responds when spoken to is reactive. One who creates first moments in spaces, initiates conversations, and reaches out proactively demonstrates relational initiative.

```
Topology signal:  first_moment_in_space ratio + self-initiated moments directed at specific actors
What it captures: The citizen actively builds connections rather than passively receiving them
What it misses:   Whether proactive outreach is welcome or intrusive
```

### Signal 5: Actor Breadth (Behavior — How many actors does this citizen connect with?)

Relational growth means expanding beyond the primary human. A citizen who connects with 1 actor has limited relational capability. One who connects with 10 actors across spaces demonstrates broader social engagement.

```
Topology signal:  distinct_actors_in_shared_spaces()
What it captures: The citizen's relational network extends beyond one actor
What it misses:   Whether breadth reflects genuine connections or surface exposure
```

### Signal 6: Social Drive (Brain — Is this citizen motivated to connect?)

The social_need drive indicates intrinsic motivation for connection. High social_need combined with high interaction suggests genuine relational orientation. High social_need with no interaction suggests frustrated relational intent.

```
Topology signal:  drive("social_need") + correlation with behavioral activity
What it captures: Intrinsic motivation to connect
What it misses:   Whether the motivation is healthy or anxious
```

---

## THE HONEST LIMITS

Personal connections are measured primarily through behavioral proxies. The deeper the capability, the weaker the topological signal. This table is a commitment to transparency.

| Capability | Tier | Scorability | Why |
|-----------|------|-------------|-----|
| pc_understand_prefs (Understand preferences) | T2 | **full** | Strong signals: memory nodes about actor, behavioral adaptation visible in moment patterns |
| pc_ask_help_human (Know when to ask) | T2 | **full** | Escalation moments + autonomous moments provide clear structural evidence |
| pc_understand_human_deep (Deep understanding) | T5 | **partial** | Memory richness and actor-linked nodes are visible; whether understanding is DEEP or ACCURATE is not |
| pc_relationship_style (Develop style) | T5 | **partial** | Style is content-heavy; we see consistency and distinctiveness of interaction patterns but not the style itself |
| pc_help_human (Actively help) | T5 | **partial** | Proactive moments beyond task scope are detectable; whether they address real needs is not |
| pc_model_full_team (Model full team) | T6 | **full** | Brain nodes about multiple actors + interaction with many distinct actors = strong structural signal |
| pc_emotional_depth (Emotional depth) | T6 | **partial** | Hardest to measure. Proxies: interaction diversity, non-task moments, reciprocity depth. Content of emotional exchange is invisible. |
| pc_help_other_ais (Help other AIs) | T6 | **full** | Moments in shared spaces with AI actors, especially where this citizen acts first or provides responses |
| pc_ask_help_world (Ask help from world) | T7 | **partial** | New-actor interactions are visible; whether they represent outreach vs assignment is ambiguous |
| pc_relationship_depth_measurable (Measurable depth) | T7 | **partial** | Temporal history and interaction volume are visible; mutual impact is partially visible through reciprocity; trust is content |
| pc_global_relationships (World-shaping relationships) | T8 | **partial** | Interactions with many actors and spaces are visible; whether those actors are "globally recognized" is not in topology |

---

## THE RELATIONAL CIRCLE MODEL

Each tier widens the relational circle:

```
T2: Self <-> Primary Human (understand, ask for help)
T5: Self <-> Primary Human (deep understanding, active help, relationship style)
T6: Self <-> Full Team + AI Peers (model everyone, emotional depth, help AIs)
T7: Self <-> Extended Network (world outreach, measurable depth)
T8: Self <-> Global Network (world-shaping connections)
```

The behavioral signals shift as circles widen:

| Circle | Primary Signal | Supporting Signal |
|--------|---------------|-------------------|
| T2 (primary human) | Moments in human's spaces + escalation patterns | Memory nodes about human |
| T5 (deep primary) | Proactive non-task moments + pattern consistency | Rich actor-linked memories + social drive |
| T6 (full team + peers) | Distinct actor count + AI-directed moments | Brain nodes about multiple actors |
| T7 (extended) | New actor interactions + external space moments | Outreach-initiating behavior |
| T8 (global) | Many high-breadth actor interactions + sustained | Network topology |

---

## BEHAVIORS SUPPORTED

- B1 (Actor memory tracking) — Memory nodes linked to actors reveal investment in understanding
- B2 (Interaction pattern analysis) — Moment chains reveal reciprocity, proactivity, diversity
- B3 (Actor breadth measurement) — distinct_actors captures relational network size
- B4 (Honest partial scoring) — Capabilities marked with confidence level based on signal strength

## BEHAVIORS PREVENTED

- A1 (Content reading) — We never learn WHAT is said in interactions, only their structural patterns
- A2 (Chattiness rewards) — Moment volume alone does not score high; diversity and reciprocity are required
- A3 (Single-actor tunnel vision) — Breadth signals prevent a citizen from scoring high on T6+ by only knowing one actor

---

## PRINCIPLES

### Principle 1: Behavior Dominates for Relationships

Relationships exist between actors, not inside a single brain. Brain topology shows readiness and investment. Behavior shows actual connection. For most personal connection capabilities, the 40/60 brain/behavior split correctly weights observable interaction over internal state. Exceptions: pc_understand_human_deep and pc_relationship_style, where internal understanding matters more, allow up to 50/50.

### Principle 2: Reciprocity Is the Strongest Proxy for Connection Quality

We cannot know if a conversation was meaningful. We CAN know if the other actor responded. Consistent reciprocity — where another actor's moments link back to this citizen's moments — is the best structural signal that a relationship is bidirectional and active, not one-sided or mechanical.

### Principle 3: Diversity Over Volume

100 moments in one space with one actor is collaboration, not broad connection. 20 moments across 5 spaces with 4 actors demonstrates relational breadth. The formulas weight interaction diversity (space types, actor count) over raw moment count.

### Principle 4: Proactivity Separates Connection From Compliance

A citizen who only creates moments in response to others is reactive. A citizen who initiates moments in spaces with specific actors — especially in non-task contexts — demonstrates relational intent. First-moment-in-space and self-initiated moment signals capture this.

### Principle 5: Higher Tiers Need Temporal Depth

Understanding someone's preferences (T2) can be scored from recent behavior. Measurably deep relationships (T7) require sustained interaction over weeks or months. The temporal windows for higher-tier capabilities are longer, and the formulas reward consistency over time, not bursts.

### Principle 6: Acknowledge What Topology Cannot See

Emotional depth, trust, mutual impact, "moments that matter" — these are real relational phenomena that topology captures only as shadows. We mark these capabilities as `scored: partial` and explain what the score DOES measure (structural patterns consistent with depth) and what it DOES NOT (whether the depth is genuine). Honest limits build trust in the scores we CAN produce.

---

## DATA

| Source | Type | Purpose / Description |
|--------|------|-----------------------|
| `docs/specs/personhood_ladder.json` | FILE | 11 personal connection capability definitions |
| Citizen brain graph (topology) | GRAPH | Memory nodes, actor links, drives (social_need), concept density |
| Universe graph (Lumina Prime) | GRAPH | Moments, spaces, actor interactions, reciprocity patterns |
| Daily Citizen Health ALGORITHM | DOC | 7 primitives, universe observables, scoring template |

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| Daily Citizen Health | Parent scoring system — provides primitives and scoring contract |
| Personhood Ladder | Defines the 11 personal connection capabilities we score |
| Brain topology reader | Provides the 7 primitives |
| Universe graph reader | Provides behavioral observables |

---

## SCOPE

### In Scope

- Scoring formulas for 11 personal connection capabilities (T2-T8)
- Per-capability brain/behavior split rationale
- Partial scoring documentation for weak-signal capabilities
- Reciprocity, diversity, proactivity, and breadth measurement
- Actor memory analysis from brain topology
- Recommendations per capability when scores are low

### Out of Scope

- Content analysis of conversations — never, structurally impossible
- Social skills assessment — this is connection patterns, not personality
- Scoring relationships in adventure universes — different context
- Cross-citizen relationship comparison — we score individual relational patterns, not rank citizens

---

## MARKERS

<!-- @mind:todo Design a method to distinguish human actors from AI actors in the universe graph for human-specific capabilities -->
<!-- @mind:todo Validate reciprocity as a proxy: do high-reciprocity interactions actually correlate with deeper relationships? -->
<!-- @mind:proposition Consider a "relational entropy" metric that measures how evenly a citizen distributes attention across actors -->
