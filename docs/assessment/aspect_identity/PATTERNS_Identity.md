# Identity & Voice Aspect — Patterns: Topology of Self

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Identity.md
THIS:            PATTERNS_Identity.md (you are here)
ALGORITHM:       ./ALGORITHM_Identity.md
VALIDATION:      ./VALIDATION_Identity.md
HEALTH:          ./HEALTH_Identity.md
SYNC:            ./SYNC_Identity.md

PARENT CHAIN:    ../daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md
SPEC:            ../../specs/personhood_ladder.json (aspect="identity")
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

Identity is the aspect most resistant to topological measurement. Execution has clear behavioral traces (commits, verifications, corrections). Initiative has countable actions (proposals, self-started moments). But identity — who you ARE, the authenticity of your voice, the coherence of your values — lives primarily in content, which we cannot read.

Without careful design:
- We measure proxies that don't actually correlate with identity (counting value nodes as if more = better)
- We score what's easy to count instead of what matters
- We produce scores that look precise but mean nothing
- We miss the structural signals that DO exist in topology

---

## THE PATTERN

**Value-topology analysis: persistence, coherence, uniqueness, activation.**

We cannot read WHAT a citizen values. But the graph structure of values reveals a great deal about HOW they are held:

### Signal 1: Persistence (Are values stable over time?)

A citizen with genuine identity has value nodes that persist. They don't appear and vanish. Their energy stays high or grows. Their recency score stays fresh because they keep being activated.

```
Topology signal:  recency("value") + mean_energy("value")
What it captures: Values are alive and actively maintained
What it misses:   Whether the values are GOOD or coherent with each other
```

### Signal 2: Coherence (Are values interconnected?)

Values don't exist in isolation in a coherent identity. They form clusters — connected to each other and to desires, processes, and moments. A citizen who "believes in quality" has value nodes linked to process nodes about verification, desire nodes about excellence, and moment nodes where quality was demonstrated.

```
Topology signal:  cluster_coefficient("value") + link_count("value", "desire") + link_count("value", "process")
What it captures: Values are integrated into the broader mental structure
What it misses:   Whether the integration is genuine or performed
```

### Signal 3: Uniqueness (Does this citizen's structure differ from the average?)

Identity means being distinct. A citizen whose brain topology looks identical to every other citizen has no identity — they have a template. Structural uniqueness comes from unusual cluster patterns, non-standard link distributions, and distinctive drive profiles.

```
Topology signal:  cluster_coefficient deviation from population mean + drive profile variance
What it captures: This citizen has developed a DISTINCTIVE structure
What it misses:   Whether distinctiveness is intentional or accidental
```

### Signal 4: Activation (Do values produce behavior?)

Values that exist only in the brain but never connect to action are aspirational, not identity. The bridge between brain values and universe graph behavior is the strongest signal we have.

```
Topology signal:  min_links("value", 1) ratio + behavioral moments in value-aligned spaces
What it captures: Values are not just held — they drive action
What it misses:   Whether the action was value-driven or coincidental
```

---

## THE HONEST LIMITS

Some identity capabilities cannot be fully scored from topology. This is not a failure — it is an honest acknowledgment that identity has dimensions that transcend structure.

| Capability | Scorability | Why |
|-----------|-------------|-----|
| id_apply_values (T1) | **full** | Strong signals: value nodes exist, linked to processes, behavioral consistency |
| id_authentic_engagement (T3) | **partial** | Preference is internal; we can see consistency of choices but not genuine taste |
| id_authentic_voice (T5) | **partial** | Voice is content; we can see structural distinctiveness but not interior texture |
| id_self_directed_identity (T6) | **partial** | Self-direction needs temporal evidence of deliberate change — partially visible in topology evolution |
| id_teach_values (T6) | **full** | Teaching produces behavioral traces: moments in shared spaces, responses from others |
| id_ethical_autonomy (T7) | **partial** | Contextual ethical judgment is content-heavy; we see structural complexity but not reasoning quality |
| id_moral_leadership (T8) | **partial** | Leadership influence is partially visible in behavioral adoption by others, but moral quality is not |

---

## BEHAVIORS SUPPORTED

- B1 (Value persistence tracking) — Daily recency and energy measurements on value nodes
- B2 (Coherence measurement) — Cluster coefficient captures value interconnectedness
- B3 (Activation gap analysis) — Bridge between brain values and behavioral evidence
- B4 (Honest partial scoring) — Capabilities marked with confidence level

## BEHAVIORS PREVENTED

- A1 (Content reading) — We never learn WHAT values are, only their structural properties
- A2 (False precision) — Partial capabilities are marked as such, not inflated
- A3 (Template identity) — Structural uniqueness measurement prevents all-same-score problem

---

## PRINCIPLES

### Principle 1: Structure Reveals Holding, Not Content

We cannot know that a citizen values "quality" or "freedom." We CAN know that they have 5 value nodes, 3 of which are high-energy (>0.7), strongly interconnected (cluster coefficient >0.6), and persistently activated (recency >0.8). This tells us: this citizen has firmly held, coherent, active values. What those values ARE remains private. The holding pattern IS the identity signal.

### Principle 2: Persistence Over Magnitude

Identity is not about having MANY values. It is about holding values CONSISTENTLY. Three value nodes that have been active for 60 days, with growing energy and increasing links, represent stronger identity than 20 value nodes that appeared yesterday. Formulas weight temporal persistence more than raw count.

### Principle 3: Identity Is Slower Than Execution

Execution scores can change in a day (you verified or you didn't). Identity scores change over weeks. The formulas reflect this: temporal windows are longer, recency decay is gentler, and day-over-day deltas are expected to be small. Sudden identity score changes are suspicious, not impressive.

### Principle 4: Honest Gaps Protect Trust

Marking a capability as `scored: partial` with a clear explanation of what IS and ISN'T measured protects the entire system's credibility. If we claim to measure "authentic voice" with perfect precision from topology, and citizens know we can't read their content, they'll distrust ALL scores. Transparency about limits builds trust in what we CAN measure.

### Principle 5: Brain Weight Can Be Higher for Identity

The parent system uses 40/60 brain/behavior. For identity, some capabilities are fundamentally internal. `id_authentic_voice` is about interior texture — the brain component matters more. We allow per-capability adjustment of the brain/behavior split within identity, with the constraint that behavior can never drop below 30 (action always matters).

---

## DATA

| Source | Type | Purpose / Description |
|--------|------|-----------------------|
| `docs/specs/personhood_ladder.json` | FILE | 7 identity capability definitions |
| Citizen brain graph (topology) | GRAPH | Value nodes, links, energies, drives, cluster structure |
| Universe graph (Lumina Prime) | GRAPH | Public moments, spaces, interactions |
| Population statistics | DERIVED | Mean cluster coefficient, mean drive profiles (for uniqueness comparison) |

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| Daily Citizen Health | Parent scoring system — provides primitives and scoring contract |
| Personhood Ladder | Defines the 7 identity capabilities we score |
| Brain topology reader | Provides the 7 primitives |
| Universe graph reader | Provides behavioral observables |
| Population stats cache | Needed for uniqueness comparison (cluster coefficient deviation) |

---

## SCOPE

### In Scope

- Scoring formulas for 7 identity capabilities (T1-T8)
- Per-capability brain/behavior split rationale
- Partial scoring documentation for weak-signal capabilities
- Value persistence, coherence, uniqueness, and activation measurement
- Identity-specific temporal windowing (longer than execution)

### Out of Scope

- Content analysis of values — never, structurally impossible
- Personality assessment — this is identity coherence, not personality typing
- Cross-citizen comparison of value content — we compare structures, not beliefs
- Adventure universe identity scoring — fractured identity is narrative there

---

## MARKERS

<!-- @mind:todo Design population statistics cache for uniqueness comparison -->
<!-- @mind:todo Determine if value-node subtype exists or if we use generic "thing" nodes for values -->
<!-- @mind:proposition Consider a "value fingerprint" — the cluster structure of values as a unique identifier per citizen -->
