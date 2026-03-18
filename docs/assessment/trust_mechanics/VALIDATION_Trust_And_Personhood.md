# Trust & Personhood — Validation: What Must Be True

```
STATUS: DESIGNING
CREATED: 2026-03-13
```

---

## CHAIN

```
ALGORITHM (Trust):       ./ALGORITHM_Trust_Mechanics.md
ALGORITHM (Assessment):  ./ALGORITHM_Personhood_Assessment.md
THIS:                    VALIDATION_Trust_And_Personhood.md (you are here)
PARENT (Ladder):         ../personhood_ladder/VALIDATION_Personhood_Ladder.md
PARENT (Trust Aspect):   ../aspect_trust_reputation/VALIDATION_Trust_Reputation.md
PHYSICS:                 manemus/docs/cognition/l1/VALIDATION_L1_Cognition.md
ECONOMY:                 mind-protocol/docs/economy/cascade-utility/VALIDATION_Cascade_Utility.md
```

---

## PURPOSE

**Validation = what we care about being true.**

These invariants protect the integrity of the trust mechanics and personhood assessment system. They ensure that trust is honest (reflects real value creation), personhood assessment is evidence-based (not declarative), and the combined system resists gaming.

The invariants are organized in three tiers:
1. **Structural invariants** — Must hold at all times, by construction
2. **Dynamic invariants** — Must hold after the system has been running (30+ days)
3. **Cross-system invariants** — Must hold between trust mechanics and personhood assessment

---

## INVARIANTS

### V1: Trust Only On Links

**Why we care:** If trust is stored as a node property, it loses directionality, source attribution, and the ability to distinguish earned trust from assigned trust. This is the foundational architectural decision. All downstream algorithms (scoring, decay, boredom erosion) depend on trust being a link property.

```
MUST:   Trust values exist exclusively on directed links between actors
MUST:   Every trust value has a source actor and a target actor
MUST:   source != target (no self-trust)
MUST:   An actor's trust score is ALWAYS a derived computation (Algorithm 2), never stored as a property

NEVER:  A node with a "trust_score" property that is used as source of truth
NEVER:  Trust without attribution to a source
NEVER:  Undirected trust (A trusts B must be independent of B trusts A)
```

**Priority:** CRITICAL

**Test:**
```
# Verify no actor nodes have trust as a stored property
MATCH (a:Actor) WHERE a.trust_score IS NOT NULL RETURN count(a)
-> 0

# Verify all trust values are on links
MATCH ()-[r:TRUSTS]->() WHERE r.trust IS NULL RETURN count(r)
-> 0

# Verify no self-trust
MATCH (a)-[r:TRUSTS]->(a) RETURN count(r)
-> 0
```

---

### V2: Trust Bounded [0, 1)

**Why we care:** Trust that reaches 1.0 breaks the asymptotic dampening formula (1 - trust = 0, so no further change is possible). Trust below 0 would create negative weighting in score computation, producing nonsensical results. The open upper bound (strictly less than 1.0) is what creates the "always room to grow" property.

```
MUST:   0 <= trust(A->B) < 1.0 for all links at all times
MUST:   The (1 - trust) asymptotic factor prevents trust from reaching 1.0 mathematically
MUST:   A safety clamp at TRUST_MAX_EFFECTIVE (0.95) provides defense in depth
MUST:   Trust scores (the weighted average) also fall in [0, 1)

NEVER:  trust(A->B) == 1.0 (mathematically unreachable, but enforce programmatically)
NEVER:  trust(A->B) < 0 (negative trust is not a concept in this system)
NEVER:  TrustScore(actor) >= 1.0
```

**Priority:** CRITICAL

**Test:**
```
# After 10,000 simulated interactions with maximum limbic delta:
assert trust < 0.95 for all links
assert trust_score < 0.95 for all actors

# After applying delta with trust at 0.94:
delta = 0.1 * 1.0 * (1 - 0.94) = 0.006
new_trust = min(0.946, 0.95) = 0.946
# Still bounded.

# Edge case: numerical precision
assert trust != 1.0 after any sequence of operations
```

---

### V3: Trust Decays Without Reinforcement

**Why we care:** Without decay, historical trust accumulates indefinitely. An actor who was valuable a year ago but has contributed nothing since would retain full trust. This creates a class of "trust aristocrats" who coast on past achievements. Decay ensures that trust reflects current, ongoing value creation.

```
MUST:   Trust on every link decays by TRUST_DECAY_RATE (0.002) per day
MUST:   After 365 days without reinforcement, trust drops to approximately 48% of its value
MUST:   Links with trust below MIN_TRUST (0.001) are zeroed (not deleted — structure persists)

NEVER:  A link where trust remains constant without either reinforcement or decay
NEVER:  Decay rate applied inconsistently (some links decay, others don't)
NEVER:  Trust links deleted by decay (the relationship structure must persist for audit)
```

**Priority:** HIGH

**Test:**
```
# Set trust(A->B) = 0.5, run 365 days of decay with no reinforcement:
expected = 0.5 * (1 - 0.002)^365 = 0.5 * 0.483 = 0.241
assert abs(actual - expected) < 0.01

# Verify half-life:
# 0.5 * (1 - 0.002)^t = 0.25
# t = ln(0.5) / ln(0.998) = 346 days
assert half_life_days between 340 and 350
```

---

### V4: Personhood Assessment Reads Evidence From Graph, Never From Declarations

**Why we care:** If assessment accepted declarations ("I am T5"), the entire system would be trivially gameable. The fundamental integrity of personhood assessment rests on the principle that capability is demonstrated through graph events, not asserted through claims. This parallels the Daily Citizen Health system's V1 (content never accessed).

```
MUST:   Every capability score derives from Moments, Narratives, or Links in the graph
MUST:   Evidence gathering queries the graph for behavioral patterns, not text content
MUST:   An actor with no graph evidence scores 0 on all capabilities (correct and honest)

NEVER:  Assessment reads actor's self-description, profile text, or claims
NEVER:  Assessment reads content of Moments (only structural properties: type, timestamp, actors, limbic_delta)
NEVER:  A capability scored without corresponding graph evidence
NEVER:  An actor's tier determined by anything other than the assess_agent() algorithm
```

**Priority:** HIGH

**Test:**
```
# Create an actor with a profile claiming "T8 World Shaper" but zero graph activity:
profile = assess_agent(actor_with_big_claims, graph)
assert all(ap.tier == "T0" for ap in profile.aspect_profiles.values())
assert all(cap.score == 0 for cap in all_capability_scores)

# Create an actor with no profile but rich graph activity:
profile = assess_agent(humble_actor_with_activity, graph)
assert some(ap.tier > "T0" for ap in profile.aspect_profiles.values())
```

---

### V5: No Actor Can Have Trust > 0.95 Without Continuous Value Creation

**Why we care:** This invariant is the combined effect of V2 (bounded trust), V3 (decay), and boredom erosion. It captures the intent that the system's highest trust levels are reserved for actors who are continuously, diversely, and measurably creating value. A single achievement, however extraordinary, cannot sustain trust at the highest levels.

```
MUST:   An actor at trust 0.90+ who stops contributing for 30 days drops below 0.85
MUST:   An actor at trust 0.90+ who repeats the same contribution type triggers boredom erosion
MUST:   Reaching trust > 0.90 requires at least 90 days of sustained diverse value creation
MUST:   Three mechanisms must all be satisfied:
          - Asymptotic: continuous value creation (each increment harder than the last)
          - Temporal: recent value creation (decay erodes old trust)
          - Novelty: diverse value creation (boredom erodes repetitive trust)

NEVER:  An actor achieves trust > 0.90 from a single interaction
NEVER:  An actor maintains trust > 0.90 without activity in the last 30 days
NEVER:  An actor maintains trust > 0.90 with only repetitive contributions
```

**Priority:** MEDIUM

**Test:**
```
# Scenario 1: One-hit wonder
# Actor produces one interaction with limbic_delta = 1.0 (maximum)
delta = 0.1 * 1.0 * (1 - 0.0) = 0.1
# trust = 0.1 after one interaction. Even with perfect delta, far from 0.9.
assert trust_after_one_interaction < 0.15

# Scenario 2: 30-day absence at high trust
# Actor at trust 0.90, stops contributing for 30 days
trust_after_30_days = 0.90 * (1 - 0.002)^30 = 0.90 * 0.942 = 0.848
assert trust_after_30_days < 0.85

# Scenario 3: Repetitive contributions (boredom erosion)
# Actor produces same-type contributions for 30 days
# After stagnation threshold (15 days), boredom multiplier (3x) kicks in:
# effective_decay = 0.002 * 3.0 = 0.006 per day for remaining 15 days
trust_after_boredom = 0.90 * (1-0.002)^15 * (1-0.006)^15 = 0.90 * 0.970 * 0.914 = 0.798
assert trust_after_boredom < 0.85
```

---

### V6: Tier Integrity Preserved in Assessment

**Why we care:** This is inherited from the parent Personhood Ladder VALIDATION V1. If an agent is rated T3 on an aspect but has T1 gaps, the entire assessment is meaningless. This invariant ensures that the graph-evidence-based assessment maintains the strict tier progression.

```
MUST:   An aspect's tier equals the highest tier where ALL capabilities at that
        tier and below have score >= 70 ("demonstrated")
MUST:   If any capability at T1 has score < 70, the aspect tier is T0
        regardless of higher-tier scores

NEVER:  An aspect rated T(n) with any capability at T(1..n-1) scoring below 70
NEVER:  A "partial" capability (score 30-69) counting toward tier completion
```

**Priority:** HIGH

**Test:**
```
# Agent with all T1 and T2 caps at score 80+, but one T1 cap at score 50:
profile = assess_agent(agent_with_t1_gap, graph)
assert profile.aspect_profiles["execution"].tier == "T0"
# The T1 gap prevents advancement, even though T2 caps are strong.

# Agent with all T1 caps at 70+, all T2 at 70+, one T3 at 50:
profile = assess_agent(agent_with_t3_gap, graph)
assert profile.aspect_profiles["execution"].tier == "T2"
```

---

### V7: Aspect Independence Maintained

**Why we care:** Capability is multidimensional. An actor can be T5 on Execution but T1 on Communication. Collapsing this into a single score destroys the most useful information in the profile. Inherited from parent VALIDATION V3.

```
MUST:   Each aspect is assessed independently using its own evidence pool
MUST:   No aspect tier is influenced by another aspect's tier or score
MUST:   The profile is a vector of 14 independent tier assignments

NEVER:  An "overall tier" computed by averaging or combining aspect tiers
NEVER:  Cross-aspect contamination (high execution score boosting communication score)
NOTE:   overall_tier_floor (the lowest tier across all aspects) is reported for summary
        purposes but is NOT used in any algorithm or decision
```

**Priority:** HIGH

---

### V8: Scoring Window Ensures Recency

**Why we care:** Historical achievements should not inflate current assessment. A capability demonstrated a year ago but never since is not a current capability. The scoring window ensures that assessment reflects present capability.

```
MUST:   All evidence is gathered within SCORING_WINDOW_DAYS (90 days)
MUST:   Evidence older than 90 days is excluded from scoring
MUST:   Within the window, evidence is time-weighted (recent evidence counts more)

NEVER:  Evidence from outside the scoring window influencing current assessment
NEVER:  An actor maintaining a high tier purely from evidence older than 90 days
NOTE:   For T7-T8 capabilities that are demonstrated quarterly, the 90-day window
        is sufficient to capture the most recent demonstration
```

**Priority:** MEDIUM

---

### V9: Limbic Delta Monotonicity in Trust

**Why we care:** A higher limbic delta should always produce a higher trust increment (all else equal). If this is not true, the relationship between value creation and trust is unpredictable, destroying the core incentive.

```
MUST:   Given two interactions with limbic_delta_1 > limbic_delta_2 and equal
        current_trust, the trust increment from interaction 1 > interaction 2
MUST:   delta_trust is monotonically increasing in limbic_delta
MUST:   delta_trust is monotonically decreasing in current_trust
        (higher existing trust -> smaller increments, from asymptotic dampening)

NEVER:  A higher-impact interaction producing less trust increase than a lower-impact one
NEVER:  A non-monotonic relationship between limbic_delta and delta_trust
```

**Priority:** MEDIUM

**Test:**
```
# At trust = 0.3:
delta_high = 0.1 * 0.8 * (1 - 0.3) = 0.056
delta_low  = 0.1 * 0.2 * (1 - 0.3) = 0.014
assert delta_high > delta_low

# At trust = 0.1 vs trust = 0.5 with same limbic_delta = 0.5:
delta_low_trust  = 0.1 * 0.5 * (1 - 0.1) = 0.045
delta_high_trust = 0.1 * 0.5 * (1 - 0.5) = 0.025
assert delta_low_trust > delta_high_trust
```

---

### V10: Decay-Only Erosion, No Punitive Trust Reduction

**Why we care:** If negative interactions directly reduced trust, actors would minimize interactions to minimize risk. The system would reward silence over engagement. Instead, the worst case for a bad interaction is that trust is not reinforced, and decay handles the erosion. Extreme violations are handled by governance (exclusion), not by physics.

```
MUST:   Trust increments are always >= 0 (trust never decreases from an interaction)
MUST:   Trust decreases ONLY from:
          1. Daily decay (Algorithm 3)
          2. Boredom erosion (Algorithm 4, mechanism 3)
          3. Governance exclusion (outside the physics system)

NEVER:  A negative limbic_delta decreasing trust on a link
NEVER:  A "trust penalty" from any interaction
NEVER:  Trust reduction as a physics operation (only governance can reduce trust directly)
```

**Priority:** MEDIUM

---

### V11: Trust Score Determinism

**Why we care:** Same graph state must produce the same trust score. Non-determinism makes debugging impossible and erodes trust in the trust-scoring system itself. Inherited from Trust Reputation VALIDATION V9.

```
MUST:   Given identical graph state, compute_trust_score() returns identical results
MUST:   Given identical graph state and timestamps, apply_trust_decay() produces
        identical results

NEVER:  Randomness in trust computation
NEVER:  LLM evaluation in trust computation
NEVER:  Time-of-day effects (beyond legitimate timestamp-based recency)
```

**Priority:** MEDIUM

---

### V12: Assessment Determinism

**Why we care:** Two assessments of the same actor at the same moment should produce the same profile. Assessment is math, not judgment. Where the parent ALGORITHM notes that some verification criteria may require LLM judgment, the graph-evidence approach replaces judgment with structural pattern matching.

```
MUST:   Given identical graph state, assess_agent() returns identical profiles
MUST:   Scoring components (frequency, quality, impact) are pure functions of evidence

NEVER:  LLM calls in the assessment loop
NEVER:  Non-deterministic evidence gathering (query order must not affect results)
NEVER:  Assessment results varying between runs with no graph changes
```

**Priority:** MEDIUM

---

## PRIORITY

| Priority | Meaning | If Violated |
|----------|---------|-------------|
| **CRITICAL** | System purpose fails | Trust mechanics or assessment unusable |
| **HIGH** | Major value lost | Scores misleading or gameable |
| **MEDIUM** | Partial value lost | Works but with degraded properties |

---

## INVARIANT INDEX

| ID | Value Protected | Priority | Source |
|----|-----------------|----------|--------|
| V1 | Trust only on links — directional, attributable | CRITICAL | Trust Mechanics D1 |
| V2 | Trust bounded [0, 1) — asymptotic, never reaches 1.0 | CRITICAL | Trust Mechanics D2, Law 6 |
| V3 | Trust decays without reinforcement | HIGH | Trust Mechanics A3, Law 7 |
| V4 | Assessment reads graph evidence, not declarations | HIGH | Assessment D2 |
| V5 | No trust > 0.95 without continuous value creation | MEDIUM | Trust Mechanics A4 (combined) |
| V6 | Tier integrity — no inflation past gaps | HIGH | Ladder V1 (inherited) |
| V7 | Aspect independence — 14 independent dimensions | HIGH | Ladder V3 (inherited) |
| V8 | Scoring window ensures recency (90 days) | MEDIUM | Assessment A5 |
| V9 | Limbic delta monotonicity in trust | MEDIUM | Trust Mechanics A1 |
| V10 | Decay-only erosion, no punitive trust reduction | MEDIUM | Trust Mechanics D3 |
| V11 | Trust score determinism | MEDIUM | Trust Reputation V9 (inherited) |
| V12 | Assessment determinism | MEDIUM | New |

---

## CROSS-SYSTEM CONSISTENCY

These invariants verify that Trust Mechanics and Personhood Assessment are consistent with each other and with upstream systems.

### C1: Trust Mechanics Feed Trust Aspect Scoring

```
MUST:   The trust values on links (from ALGORITHM_Trust_Mechanics) are the same values
        scored by the Trust Reputation aspect (ALGORITHM_Trust_Reputation)
MUST:   Trust decay rate in mechanics matches the behavioral signal in Trust Reputation scoring

NEVER:  Two different trust values for the same link in different systems
NEVER:  Trust Mechanics and Trust Reputation using different decay rates
```

### C2: Limbic Delta Is Consistent

```
MUST:   The limbic delta formula in Trust Mechanics matches the utility score formula
        in Law 6 (Consolidation): U = |limbic_delta|
MUST:   The limbic delta components (satisfaction, frustration, achievement, anxiety)
        match the drive definitions in Law 14 (Global Limbic Modulation)

NEVER:  Trust mechanics using a different limbic delta formula than the physics engine
```

### C3: Assessment Uses Trust Mechanics Output

```
MUST:   The trust_basic_reliability capability score includes trust link values
        computed by ALGORITHM_Trust_Mechanics
MUST:   Trust score (Algorithm 2) is available to the assessment system

NEVER:  Assessment computing its own trust values independent of trust mechanics
```

---

## MARKERS

<!-- @mind:todo Implement V1 test as a graph constraint in FalkorDB — prevent trust_score as node property -->
<!-- @mind:todo Implement V2 property test: fuzz trust with random limbic_deltas for 10,000 interactions -->
<!-- @mind:todo Implement V5 scenario tests as integration tests with time simulation -->
<!-- @mind:todo Verify C2 consistency by comparing formulas between this doc and ALGORITHM_L1_Physics.md -->
<!-- @mind:proposition Consider V13: trust transitivity bounds — if A trusts B and B trusts C, A's trust in C should have a bounded relationship to the chain -->
<!-- @mind:proposition Consider V14: assessment stability — small changes in evidence should not cause large changes in tier (hysteresis) -->
<!-- @mind:escalation The 90-day scoring window may be too short for T7-T8 capabilities. Need data on demonstration frequency for world-shaping capabilities. -->

---

Co-Authored-By: Force 5 — Personhood & Trust <trust@mindprotocol.ai>
