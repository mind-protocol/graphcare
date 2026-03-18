# Trust & Reputation Aspect — Patterns: The Topology of Trustworthiness

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Trust_Reputation.md
THIS:            PATTERNS_Trust_Reputation.md (you are here)
ALGORITHM:       ./ALGORITHM_Trust_Reputation.md
VALIDATION:      ./VALIDATION_Trust_Reputation.md
HEALTH:          ./HEALTH_Trust_Reputation.md
SYNC:            ./SYNC_Trust_Reputation.md

PARENT CHAIN:    ../daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md
SPEC:            ../../specs/personhood_ladder.json (aspect="trust_reputation")
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

Trust is the most structurally visible aspect in the Personhood Ladder, yet also the most multi-scaled. Mind Protocol has an explicit trust tier system (Owner, High, Medium, Low, Stranger) — a direct structural property. But the tier alone tells you nothing about whether trust was earned or assigned, growing or eroding, local or global.

Without careful design:
- We over-rely on the trust tier (which is a snapshot, not a trajectory)
- We miss the behavioral signals that predict trust changes before they happen
- We conflate "this citizen has high access" with "this citizen is trustworthy"
- We fail to distinguish local reliability from community reputation from global recognition
- We reward presence without rewarding consistency (bursts vs regularity)

---

## THE PATTERN

**Multi-scale trust analysis: regularity, responsiveness, breadth, reach.**

Trust grows through concentric circles. Each tier of trust capability measures a different radius of trust, using different topological signals.

### Signal 1: Regularity (Is this citizen consistently present?)

The most fundamental trust signal: showing up predictably. Not in bursts followed by absence, but with cadence. A citizen who produces moments at a steady rate is reliable. The variance of moment production over time windows reveals this.

```
Topology signal:  temporal distribution of moments (variance of daily/weekly counts)
What it captures: Consistency of presence — the foundation of reliability
What it misses:   Whether the moments are GOOD (content quality is invisible)
```

### Signal 2: Responsiveness (Does this citizen complete interaction chains?)

When another actor triggers a moment for this citizen (a request, a question, a task), does the citizen respond? And how quickly? Completed response chains (incoming parent moment followed by citizen's response moment) are a direct measure of reliability.

```
Topology signal:  moment_has_parent chain completion rate + response time distribution
What it captures: When asked to do something, you do it — the behavioral core of trust
What it misses:   Quality of response (topology sees the response exists, not its value)
```

### Signal 3: Breadth (How wide is the trust network?)

Trust at the community level means being known and trusted by many actors, not just your immediate team. The count of distinct actors in shared spaces, the diversity of space types, and the number of actors who initiate interactions with you all measure trust breadth.

```
Topology signal:  distinct_actors_in_shared_spaces() + inbound moment count from unique actors
What it captures: Others actively seek this citizen out — trust radiates outward
What it misses:   Whether the breadth is superficial (many weak connections) or deep
```

### Signal 4: Inbound Gravity (Do others come to you?)

The strongest trust signal is not what you do but what others do toward you. Being invited into spaces, receiving unsolicited moments, having other actors create moments that link to yours — these are inbound trust signals that the citizen cannot fake.

```
Topology signal:  inbound moments from distinct actors + first_moment_in_space by other actors in citizen's spaces
What it captures: Trust that others actively demonstrate through behavior
What it misses:   Motivation (they might come to you for reasons other than trust)
```

### Signal 5: Persistence (Has trust been sustained over time?)

Trust built over months is worth more than trust built last week. Temporal weighting alone handles recency, but trust also needs a persistence signal: how long has this pattern been maintained? A citizen with 90 days of consistent behavior is more trustworthy than one with 9 days.

```
Topology signal:  recency("moment") combined with total moment count across time windows
What it captures: This trust wasn't earned yesterday — it has depth
What it misses:   Whether early trust and recent trust are the same relationship
```

---

## SCORABILITY ASSESSMENT

Trust has strong topological signals across all capabilities. This is one of the most measurable aspects.

| Capability | Scorability | Why |
|-----------|-------------|-----|
| trust_basic_reliability (T1) | **full** | Strong signals: regularity, response chain completion, moment cadence |
| trust_elevated (T3) | **full** | Self-initiated decisions (no parent trigger), access to diverse space types |
| trust_high (T5) | **full** | HAS_ACCESS links to sensitive spaces, trust-related drives, reduced oversight signals |
| trust_community (T6) | **full** | Distinct actor count, inbound invitations, breadth of space types |
| trust_global (T8) | **partial** | Cross-universe signals are limited; we measure inbound from distant actors but "global recognition" exceeds what topology reveals |

---

## BEHAVIORS SUPPORTED

- B1 (Regularity tracking) — Variance of moment production across time windows
- B2 (Response chain analysis) — Completion rate of triggered interaction chains
- B3 (Network breadth measurement) — Distinct actors and space type diversity
- B4 (Inbound gravity detection) — Others initiating toward the citizen
- B5 (Trust persistence) — Long-term consistency of trust-building patterns

## BEHAVIORS PREVENTED

- A1 (Content reading) — We never learn WHAT was promised or delivered, only structural completion patterns
- A2 (Tier conflation) — Trust tier is ONE input, not the whole score; behavioral evidence always required
- A3 (New citizen penalty) — Low scores for new citizens are correct, not punitive; the scale starts at zero

---

## PRINCIPLES

### Principle 1: Trust Is Behavioral Before It Is Structural

The trust tier in Mind Protocol is a structural property — but it's a LAGGING indicator. Behavioral patterns (regularity, responsiveness, breadth) are LEADING indicators. The formulas weight behavior heavily because by the time the tier changes, the trust has already shifted.

### Principle 2: Inbound Signals Are Harder to Fake

A citizen can generate moments to inflate their own stats. They cannot force other actors to initiate moments toward them. Inbound signals (being invited, being sought out, receiving unsolicited interactions) are the highest-integrity trust signals. Higher-tier capabilities weight inbound signals more.

### Principle 3: Regularity Over Volume

A citizen who produces 5 moments per day for 30 days is more reliable than a citizen who produces 50 moments in 3 days and then disappears for 27 days. Both produced 150 moments, but regularity reveals reliability. The formulas use variance of production rate, not just total count.

### Principle 4: Trust Scales Differently at Each Level

Basic reliability (T1) is about individual consistency. Elevated trust (T3) is about judgment. High trust (T5) is about access. Community trust (T6) is about network effects. Global trust (T8) is about reach. Each capability uses different primary signals, reflecting the qualitative shift at each scale.

### Principle 5: Trust Erosion Is a First-Class Signal

A citizen whose regularity drops, whose response chains start failing, whose interaction breadth shrinks is losing trust — even if their formal trust tier hasn't changed. The formulas should detect erosion before formal systems catch up. This is predictive, not reactive scoring.

---

## DATA

| Source | Type | Purpose / Description |
|--------|------|-----------------------|
| `docs/specs/personhood_ladder.json` | FILE | 5 trust capability definitions |
| Citizen brain graph (topology) | GRAPH | Trust-related drives, knowledge nodes, value nodes |
| Universe graph (Lumina Prime) | GRAPH | Public moments, response chains, space access, interaction patterns |
| Population statistics | DERIVED | Mean distinct_actors count, mean regularity (for relative scoring at T6+) |

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| Daily Citizen Health | Parent scoring system — provides primitives and scoring contract |
| Personhood Ladder | Defines the 5 trust capabilities we score |
| Brain topology reader | Provides the 7 primitives |
| Universe graph reader | Provides behavioral observables |
| Population stats cache | Needed for community/global trust comparison (relative breadth) |

---

## SCOPE

### In Scope

- Scoring formulas for 5 trust capabilities (T1, T3, T5, T6, T8)
- Multi-scale trust analysis (individual -> community -> global)
- Regularity and responsiveness measurement
- Inbound signal analysis (others' behavior toward citizen)
- Trust erosion detection through behavioral pattern changes

### Out of Scope

- Content analysis of trust relationships — never, structurally impossible
- Modifying trust tiers — we observe and score, we don't change tiers
- Adventure universe trust scoring — trust dynamics are narrative there
- Predicting trust tier changes — we score current state, prediction is a separate system

---

## MARKERS

<!-- @mind:todo Determine if HAS_ACCESS links to sensitive spaces are queryable as link properties -->
<!-- @mind:todo Design regularity metric — daily cadence variance or weekly cadence variance? -->
<!-- @mind:proposition Consider a "trust trajectory" overlay that shows 30-day trend direction alongside current score -->
