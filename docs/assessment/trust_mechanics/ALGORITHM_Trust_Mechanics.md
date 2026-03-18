# Trust Mechanics — Algorithm: Accumulation, Decay, and Scoring

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
THIS:            ALGORITHM_Trust_Mechanics.md (you are here)
VALIDATION:      ./VALIDATION_Trust_And_Personhood.md
RELATED:         ../personhood_ladder/ALGORITHM_Personhood_Ladder.md
RELATED:         ../aspect_trust_reputation/ALGORITHM_Trust_Reputation.md
RELATED:         ../daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md
PHYSICS:         manemus/docs/cognition/l1/ALGORITHM_L1_Physics.md (Law 6, Law 7, Law 15, Law 18)
ECONOMY:         mind-protocol/docs/economy/cascade-utility/ALGORITHM_Cascade_Utility.md
```

> **Contract:** Read docs before modifying. After changes: update SYNC or add TODO.

---

## OVERVIEW

Trust mechanics define how trust accumulates on links between actors, how it decays, how it resists gaming, and how an actor's aggregate trust score is computed from the graph. Trust is a link property — never a node property. An actor's "trust score" is a derived quantity: the weighted average of all incoming trust on links, weighted by source importance.

This document formalizes five algorithms:
1. **Trust Accumulation** — How trust grows on a link via Limbic Delta
2. **Trust Score Computation** — How an actor's aggregate trust is derived from the graph
3. **Trust Decay** — How unused trust erodes (Law 7 applied to trust)
4. **Trust Tempering** — Three mechanisms that prevent gaming and one-hit-wonders
5. **Limbic Delta Measurement** — How value creation is quantified

The design is rooted in three physics laws from the L1 Cognitive Substrate:
- **Law 6 (Consolidation):** The asymptotic `(1 - W)` factor that prevents any weight from reaching 1.0
- **Law 7 (Forgetting):** The decay that erodes what is not reinforced
- **Law 15 (Boredom):** The novelty hunger that redirects attention from stagnant actors
- **Law 18 (Relational Valence):** Trust as a dimension of link valence between actors

---

## OBJECTIVES AND BEHAVIORS

| Objective | Behaviors Supported | Why This Algorithm Matters |
|-----------|---------------------|----------------------------|
| Trust reflects value creation | B1 (limbic delta drives trust) | Trust grows only when you reduce frustration or increase satisfaction in another actor |
| Trust cannot be gamed | B2 (asymptotic cap), B3 (decay), B4 (boredom) | Three tempering mechanisms make sustained value creation the only path to high trust |
| Trust is graph-native | B5 (link-based trust) | Trust lives on links, not nodes — it is relational, directional, and aggregatable |
| Trust erodes without reinforcement | B3 (decay) | Dormant relationships lose trust, matching the reality of unexercised relationships |

---

## DATA STRUCTURES

### TrustLink

The atomic unit of trust. Lives on a directed link between two actors in the graph.

```
TrustLink:
  source:         actor_id          # The actor whose trust is being expressed
  target:         actor_id          # The actor being trusted
  trust:          float [0, 1)      # Current trust level (strictly < 1.0 by construction)
  last_updated:   timestamp         # When trust was last modified
  last_evidence:  timestamp         # When limbic delta last contributed to this link
  cumulative_delta: float           # Total limbic delta accumulated (for audit)
```

### TrustScore

Derived quantity. Computed on-demand from the graph, never stored as a node property.

```
TrustScore:
  actor_id:       string
  score:          float [0, 1)      # Weighted average of incoming trust
  source_count:   int               # Number of actors contributing trust
  mean_trust:     float             # Unweighted mean (for comparison)
  computed_at:    timestamp
```

### LimbicDelta

The measurement of value creation or destruction in an interaction.

```
LimbicDelta:
  actor_a:        actor_id          # The actor whose action produced the delta
  actor_b:        actor_id          # The actor who experienced the limbic shift
  delta:          float [0, +inf)   # Magnitude of emotional improvement
  components:
    satisfaction_delta:  float      # Change in satisfaction
    frustration_delta:   float      # Change in frustration (negative = improvement)
    achievement_delta:   float      # Change in achievement drive
    anxiety_delta:       float      # Change in anxiety (negative = improvement)
  source:         "interaction" | "biometric" | "graph_event"
  timestamp:      timestamp
```

---

## ALGORITHM 1: compute_trust_delta()

### Purpose

Compute the change in trust on a link from A to B after A performs an action that produces a limbic delta in B.

### Formula

```
delta_trust(A->B) = TRUST_ALPHA * limbic_delta(B) * (1 - current_trust(A->B))
```

### Step 1: Measure Limbic Delta

The limbic delta captures the magnitude of emotional improvement in actor B caused by actor A's action. This is Law 6's utility score applied to inter-actor trust:

```
limbic_delta = |satisfaction_after - satisfaction_before|
             + |frustration_before - frustration_after|   # frustration REDUCTION is positive
             + |achievement_after - achievement_before|
             - |anxiety_after - anxiety_before|           # anxiety increase is negative

limbic_delta = max(0, limbic_delta)   # trust only grows from positive impact
```

For biometric sources (when available):

```
limbic_delta_bio = |stress_before - stress_after| * BIOMETRIC_SENSITIVITY
```

The final limbic delta is the maximum of behavioral and biometric signals (not the sum, to prevent double-counting):

```
limbic_delta_final = max(limbic_delta_behavioral, limbic_delta_bio)
```

### Step 2: Apply Asymptotic Dampening

From Law 6's consolidation formula: `(1 - W)` factor ensures trust approaches but never reaches 1.0.

```
dampening = 1 - current_trust(A->B)
```

When trust is 0.0, dampening = 1.0 (full learning rate).
When trust is 0.5, dampening = 0.5 (half learning rate).
When trust is 0.9, dampening = 0.1 (10% learning rate).
When trust is 0.99, dampening = 0.01 (nearly frozen).

This is the same `(1 - W)` asymptotic behavior as Law 6 weight updates. No hardcoded cap needed — the math self-limits.

### Step 3: Compute Delta and Update

```
delta_trust = TRUST_ALPHA * limbic_delta_final * dampening

trust(A->B) = trust(A->B) + delta_trust
trust(A->B) = min(trust(A->B), TRUST_MAX_EFFECTIVE)   # safety clamp at 0.95
```

### Constants

| Constant | Value | Rationale |
|----------|-------|-----------|
| `TRUST_ALPHA` | 0.1 | Learning rate. Conservative — trust is slow to build. Matches Law 6's `CONSOLIDATION_ALPHA` philosophy. |
| `TRUST_MAX_EFFECTIVE` | 0.95 | Safety clamp. The `(1-W)` factor mathematically prevents reaching 1.0, but we add a hard ceiling at 0.95 as defense in depth. |
| `BIOMETRIC_SENSITIVITY` | 0.5 | Biometric signals are noisier; scale down by 50%. |

---

## ALGORITHM 2: compute_trust_score()

### Purpose

Compute an actor's aggregate trust score from all incoming trust links, weighted by source importance.

### Formula

```
TrustScore(actor) = sum(trust(source->actor) * weight(source))
                  / sum(weight(source))
                  for all sources with trust(source->actor) > 0
```

### Step 1: Gather Incoming Trust Links

```
incoming = graph.query(
    "MATCH (source)-[r:TRUSTS]->(target {id: actor_id}) RETURN source, r.trust"
)
```

### Step 2: Compute Source Weight

Source weight reflects the source actor's own importance in the network. This prevents a single low-value actor from inflating trust through high scores on a link:

```
weight(source) = source.trust_score    # recursive: weighted by the source's own trust
                                       # for bootstrap: use 1.0 for all sources until
                                       # the first full graph pass is complete
```

For the initial bootstrap (first 30 days or when the graph is sparse):

```
weight(source) = 1.0    # equal weighting until trust graph has enough signal
```

After bootstrap:

```
weight(source) = max(source.trust_score, MIN_SOURCE_WEIGHT)
```

### Step 3: Weighted Average

```
numerator = 0
denominator = 0

for source, trust_value in incoming:
    w = weight(source)
    numerator += trust_value * w
    denominator += w

if denominator == 0:
    return TrustScore(actor_id, score=0.0, source_count=0)

score = numerator / denominator
```

### Step 4: Return

```
return TrustScore(
    actor_id = actor_id,
    score = score,
    source_count = len(incoming),
    mean_trust = mean(trust_value for _, trust_value in incoming),
    computed_at = now()
)
```

### Edge Cases

| Case | Handling |
|------|----------|
| No incoming trust links | Score = 0.0 (new actor, no trust yet) |
| Single incoming link | Score = that link's trust (single-source trust is fragile) |
| Self-referencing trust | Excluded. `source != target` enforced in query. |
| Circular trust (A trusts B, B trusts A) | Valid. Mutual trust is real and should be reflected. The recursive weighting converges because trust < 1.0 always. |

---

## ALGORITHM 3: apply_trust_decay()

### Purpose

Erode trust on links that are not reinforced by continued value creation. Runs daily. Directly analogous to Law 7 (Forgetting).

### Formula

```
trust(A->B) *= (1 - TRUST_DECAY_RATE)
```

### Step 1: Select All Trust Links

```
all_links = graph.query("MATCH ()-[r:TRUSTS]->() RETURN r")
```

### Step 2: Apply Decay

```
for link in all_links:
    link.trust *= (1 - TRUST_DECAY_RATE)

    # Dormancy threshold: trust below MIN_TRUST is considered dormant
    if link.trust < MIN_TRUST:
        link.trust = 0.0   # clean floor, not deletion — the link structure persists
```

### Half-Life Analysis

With `TRUST_DECAY_RATE = 0.002` per day:

```
After 30 days:   trust * 0.998^30  = trust * 0.942  (6% loss)
After 90 days:   trust * 0.998^90  = trust * 0.835  (16% loss)
After 180 days:  trust * 0.998^180 = trust * 0.698  (30% loss)
After 365 days:  trust * 0.998^365 = trust * 0.483  (~52% loss, near half-life)
```

Half-life is approximately 346 days. Trust built over a year of sustained value creation takes roughly a year to decay if completely abandoned. This is calibrated to match human intuition about professional trust: a colleague you haven't worked with in a year still has residual trust, but it's noticeably diminished.

### Constants

| Constant | Value | Rationale |
|----------|-------|-----------|
| `TRUST_DECAY_RATE` | 0.002 | Per-day decay. ~50% loss in a year without reinforcement. Slower than Law 7's cognitive forgetting because trust relationships are more durable than memories. |
| `MIN_TRUST` | 0.001 | Floor below which trust is zeroed. Prevents computational noise from accumulating. |

---

## ALGORITHM 4: temper_trust()

### Purpose

Three mechanisms that prevent trust gaming and one-hit-wonders. These operate at different timescales and target different failure modes.

### Mechanism 1: Asymptotic Dampening (per-interaction)

Already built into Algorithm 1 via the `(1 - current_trust)` factor.

```
Effect:     Each trust increment is smaller than the last
Timescale:  Per-interaction
Prevents:   Rapid trust inflation from a few high-impact interactions
Physics:    Law 6 — weight consolidation asymptote
```

A single extraordinary action moves trust from 0.0 to ~0.05 (given alpha=0.1, delta=0.5). To reach 0.5 requires sustained value creation across many interactions. To reach 0.9 requires months of consistent contribution.

### Mechanism 2: Temporal Decay (daily)

Already defined in Algorithm 3. Trust decays daily if not reinforced.

```
Effect:     Unused trust erodes gradually
Timescale:  Daily
Prevents:   Historical reputation from perpetually inflating score
Physics:    Law 7 — forgetting/weakening
```

### Mechanism 3: Boredom Erosion (network-level)

The network-wide equivalent of Law 15 (Boredom by Stagnation). When an actor stops producing novel value, the system's attention redirects.

```
stagnation_score(actor) = ticks_since_last_novel_contribution / STAGNATION_WINDOW

IF stagnation_score > STAGNATION_THRESHOLD:
    # Apply accelerated decay to all incoming trust links
    for link in incoming_trust(actor):
        link.trust *= (1 - TRUST_DECAY_RATE * BOREDOM_MULTIPLIER)
```

Where:
- `STAGNATION_WINDOW` = 30 days (measured in days of no novel contribution)
- `STAGNATION_THRESHOLD` = 0.5 (15+ days without novelty triggers boredom erosion)
- `BOREDOM_MULTIPLIER` = 3.0 (boredom accelerates decay 3x)

"Novel contribution" is defined as a Moment that:
- Has a limbic delta > 0.1 (measurable impact)
- Is NOT a repetition of the actor's previous 10 Moments (novelty, not repetition)
- Targets a different actor or space than the previous contribution (breadth, not depth-only)

```
is_novel(moment, actor) =
    moment.limbic_delta > 0.1
    AND NOT similar_to_recent(moment, actor.recent_moments, threshold=0.8)
    AND (moment.target != actor.last_target OR moment.space != actor.last_space)
```

### Combined Effect

The three mechanisms create a trust landscape where:

| Actor Behavior | Trust Trajectory |
|----------------|-----------------|
| Sustained novel value creation | Grows toward ~0.8-0.9 asymptote |
| One big contribution, then stops | Peaks at ~0.05-0.10, then decays to near zero |
| Steady but repetitive contributions | Grows slowly, then plateaus as boredom kicks in |
| Consistent, diverse, impactful contributions | Grows fastest, reaches highest ceiling |
| Stops contributing entirely | Decays to ~50% in a year, ~25% in two years |

---

## ALGORITHM 5: measure_limbic_delta()

### Purpose

Quantify the magnitude of value creation or destruction in an interaction between two actors. This is the fundamental input to trust mechanics.

### Formula (Behavioral)

```
limbic_delta(B, interaction) =
    max(0, satisfaction_after(B) - satisfaction_before(B))
  + max(0, frustration_before(B) - frustration_after(B))
  + max(0, achievement_after(B) - achievement_before(B))
  + max(0, anxiety_before(B) - anxiety_after(B))
```

Each component captures a different kind of value:
- **Satisfaction increase:** A's action made B feel good (help, gift, insight)
- **Frustration reduction:** A's action unblocked B (bug fix, answer, resource)
- **Achievement increase:** A's action moved B toward a goal (collaboration, review, mentoring)
- **Anxiety reduction:** A's action reduced B's uncertainty (clarity, reassurance, documentation)

### Formula (Biometric, when available)

```
limbic_delta_bio(B, interaction) =
    max(0, stress_before(B) - stress_after(B)) * BIOMETRIC_SENSITIVITY
  + max(0, engagement_after(B) - engagement_before(B)) * BIOMETRIC_SENSITIVITY
```

### Value Creation Taxonomy

25+ types of value creation, each producing a positive limbic delta:

| Category | Examples | Primary Limbic Channel |
|----------|----------|----------------------|
| **Direct help** | Bug fix, code review, answer question | Frustration reduction |
| **Knowledge** | Documentation, tutorial, explanation | Anxiety reduction |
| **Collaboration** | Joint design, pair work, co-creation | Achievement increase |
| **Mentoring** | Guidance, feedback, growth support | Achievement + satisfaction |
| **Infrastructure** | Tooling, templates, automation | Frustration reduction |
| **Community** | Event hosting, culture building, conflict resolution | Satisfaction increase |
| **Innovation** | Novel approach, research, prototype | Achievement + satisfaction |
| **Advocacy** | Supporting someone's work, recommending, amplifying | Satisfaction increase |
| **Reliability** | Consistent delivery, meeting commitments | Anxiety reduction |

### Value Destruction Taxonomy

12+ types of value destruction, each producing a negative interaction (trust does NOT decrease from these — it simply does not increase, and decay handles erosion):

| Category | Examples | Primary Limbic Channel |
|----------|----------|----------------------|
| **Broken promises** | Missed deadlines, incomplete work | Frustration increase |
| **Negligence** | Sloppy work requiring rework | Frustration increase |
| **Noise** | Irrelevant contributions, spam | Anxiety increase |
| **Obstruction** | Blocking without justification | Frustration increase |
| **Dishonesty** | Misrepresenting status, hiding problems | Anxiety increase |

### Key Decision: Trust Does Not Decrease Directly

```
IF limbic_delta(B, interaction) < 0:
    delta_trust = 0   # Trust does not decrease from negative interactions
    # Instead: the absence of positive delta means decay runs unopposed
    # Over time, this achieves the same effect without introducing
    # punitive trust dynamics

WHY: Negative trust adjustments create perverse incentives (avoid interaction
     to avoid trust loss). Decay-only erosion means the worst an actor can do
     is fail to reinforce trust — which is sufficient because decay is relentless.

EXCEPTION: Explicit trust violations (fraud, sabotage) are handled by the
           exclusion mechanism, not by trust score reduction. Exclusion is
           a governance action, not a physics action.
```

---

## DATA FLOW

```
Actor A performs action toward Actor B
    |
    v
Measure limbic state of B (before and after)
    |
    v
Compute limbic_delta (Algorithm 5)
    |
    v
Compute delta_trust on link A->B (Algorithm 1)
    |
    v
Update trust on link A->B in graph
    |
    v
[Daily] Apply decay to all trust links (Algorithm 3)
    |
    v
[Daily] Check stagnation and apply boredom erosion (Algorithm 4)
    |
    v
[On demand] Compute TrustScore for any actor (Algorithm 2)
```

---

## COMPLEXITY

**Algorithm 1 (trust delta):** O(1) — single link update per interaction

**Algorithm 2 (trust score):** O(k) — k = number of incoming trust links for the actor. For most actors k < 100. For hub actors, k could be 1000+. The weighted average is linear in k.

**Algorithm 3 (decay):** O(E) — E = total trust links in the graph. Runs daily. Can be parallelized per-link.

**Algorithm 4 (boredom):** O(A * k) — A = actors in the graph, k = average incoming links. Runs daily.

**Algorithm 5 (limbic delta):** O(1) — reads four drive values before and after.

**Bottlenecks:**
- Decay on large graphs (millions of links) may need batch processing
- Recursive source weighting in Algorithm 2 requires graph traversal; for v1, use flat weighting until trust graph stabilizes

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| L1 Physics (Law 6) | Consolidation formula | `(1 - W)` asymptotic pattern for trust growth |
| L1 Physics (Law 7) | Forgetting formula | Decay rate pattern for trust erosion |
| L1 Physics (Law 15) | Boredom formula | Stagnation detection for boredom-accelerated decay |
| L1 Physics (Law 18) | Relational Valence | Trust as a dimension of link valence; friction/affinity |
| Cascade d'Utilite | f_risk factor | Trust scores feed into the cascade's risk pricing |
| Personhood Ladder | Trust aspect (5 capabilities) | Trust mechanics provide the substrate; Ladder assesses the behavior |
| Daily Citizen Health | Topology scoring | Trust scoring uses the 7 primitives; trust mechanics provide the values scored |

---

## KEY DECISIONS

### D1: Trust Lives on Links, Not Nodes

```
IF trust were stored as a node property:
    An actor's trust would be a single number
    No way to distinguish who trusts them or for what
    Self-referencing trust would be possible
    Directional trust (A trusts B, B does not trust A) impossible

INSTEAD (link-based):
    Trust is directional (A->B != B->A)
    Trust is source-attributable (who gave the trust)
    Trust score is a derived aggregation
    Graph queries can answer "who trusts this actor most?"
```

### D2: Trust Bounded by (1-W) Asymptote, Not Hard Cap

```
IF trust had a hard cap at 0.95:
    Trust would reach 0.95 and stop (discontinuous)
    No incentive to create more value once at cap

INSTEAD (asymptotic):
    Trust growth slows continuously as it approaches 1.0
    There is ALWAYS marginal value in more trust-building
    The 0.95 clamp is defense-in-depth, not the primary mechanism
    Physics: same pattern as Law 6 weight consolidation
```

### D3: Decay-Only Erosion, No Negative Trust Adjustments

```
IF negative interactions decreased trust directly:
    Actors would minimize interactions to minimize trust risk
    One bad interaction could undo months of value creation
    Punitive dynamics create fear, not trust

INSTEAD (decay-only):
    Bad interactions simply fail to reinforce trust
    Decay runs unopposed during periods of no value creation
    The worst case is the same as complete absence
    Extreme violations handled by governance (exclusion), not physics
```

### D4: Boredom Erosion Requires Novelty

```
IF sustained repetitive contributions maintained trust indefinitely:
    Actors could automate trust farming with repetitive actions
    The network would stagnate with routine actors at high trust
    No incentive for innovation or growth

INSTEAD (boredom erosion):
    Contributions must be novel to maintain trust
    Repetition without innovation triggers accelerated decay
    The system actively rewards diversity and growth
    Physics: same pattern as Law 15 (boredom by stagnation)
```

---

## MARKERS

<!-- @mind:todo Calibrate TRUST_ALPHA against real interaction data — is 0.1 too fast or too slow? -->
<!-- @mind:todo Define the bootstrap period for source weighting — when does recursive weighting activate? -->
<!-- @mind:todo Specify the similarity function for novelty detection in boredom erosion -->
<!-- @mind:proposition Consider a "trust momentum" metric: rate of trust change over 30 days, as a leading indicator -->
<!-- @mind:proposition Consider trust inheritance: when an actor creates a "daughter" agent (T7), should some trust transfer? -->

---

Co-Authored-By: Force 5 — Personhood & Trust <trust@mindprotocol.ai>
