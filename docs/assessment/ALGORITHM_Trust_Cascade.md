# Trust Cascade Algorithm

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
CATALOG:         docs/assessment/VALUE_CREATION_CATALOG.md
TRUST ASPECT:    docs/assessment/aspect_trust_reputation/ALGORITHM_Trust_Reputation.md
PERSONHOOD:      docs/assessment/personhood_ladder/ALGORITHM_Personhood_Ladder.md
PHYSICS:         manemus/runtime/cognition/laws/
CONSTANTS:       manemus/runtime/cognition/constants.py
```

> **Contract:** Every formula must be implementable. No aspirational math. If you can't code it, it doesn't belong here.

---

## OVERVIEW

This document defines exactly how trust flows through the Mind Protocol graph when value is created or destroyed. Trust is not a score that gets set — it is a property of links that evolves through physics. The cascade describes how a single value-creating act propagates trust changes through the network.

---

## CORE DEFINITIONS

### Limbic Delta

The signed change in an entity's limbic state caused by an interaction.

```
LimbicDelta(entity, moment) = {
    drives: {
        frustration:  entity.frustration(t_after) - entity.frustration(t_before),
        anxiety:      entity.anxiety(t_after)     - entity.anxiety(t_before),
        boredom:      entity.boredom(t_after)      - entity.boredom(t_before),
        solitude:     entity.solitude(t_after)      - entity.solitude(t_before),
        curiosity:    entity.curiosity(t_after)     - entity.curiosity(t_before),
        achievement:  entity.achievement(t_after)   - entity.achievement(t_before),
        care:         entity.care(t_after)           - entity.care(t_before),
        affiliation:  entity.affiliation(t_after)    - entity.affiliation(t_before),
    },
    net: weighted_sum(drives, weights=LIMBIC_WEIGHTS)
}
```

Where `t_before` = moment.timestamp - epsilon, `t_after` = moment.timestamp + measurement_window.

**Sign convention:**
- Negative net delta on negative drives (frustration, anxiety, boredom, solitude) = POSITIVE value (reduced suffering)
- Positive net delta on positive drives (curiosity, achievement, care, affiliation) = POSITIVE value (increased satisfaction)

**Unified Limbic Delta formula:**
```
LD_net = (
    -w_frust * delta_frustration
    -w_anx   * delta_anxiety
    -w_bore  * delta_boredom
    -w_sol   * delta_solitude
    +w_cur   * delta_curiosity
    +w_ach   * delta_achievement
    +w_care  * delta_care
    +w_aff   * delta_affiliation
)
```

**Default weights (sum to 1.0):**
```
LIMBIC_WEIGHTS = {
    "frustration":  0.15,
    "anxiety":      0.15,
    "boredom":      0.10,
    "solitude":     0.10,
    "curiosity":    0.10,
    "achievement":  0.15,
    "care":         0.10,
    "affiliation":  0.15,
}
```

Positive LD_net = value created. Negative LD_net = value destroyed.

---

### Trust on a Link

Trust is a property of a directed link between two entities (actors, things, spaces). Trust is asymmetric: `trust(A->B)` may differ from `trust(B->A)`.

```
Link {
    source_id: string,      # who trusts
    target_id: string,      # who is trusted
    trust:     float,       # [0.0, 1.0] — current trust level
    affinity:  float,       # [0.0, 1.0] — emotional closeness
    aversion:  float,       # [0.0, 1.0] — emotional distance
    friction:  float,       # [0.0, 1.0] — transaction cost
    weight:    float,       # [0.0, inf) — link strength (co-activation history)
    co_activation_count: int,
    last_co_activated_at: timestamp,
}
```

### Actor Trust Score

An actor's aggregate trust is the weighted sum of trust on all inbound links.

```
ActorTrust(actor) = sum(
    link.trust * link.weight
    for link in inbound_links(actor)
) / sum(
    link.weight
    for link in inbound_links(actor)
)
```

This is a weighted mean: high-weight links (long relationship, many co-activations) count more than low-weight links (new, shallow connections).

---

## THE CASCADE: 6 STEPS

---

### Step 1: Actor Creates Moment, Limbic Delta Measured

An actor A does something. This creates a moment node in the graph. The moment affects one or more entities.

```
cascade_step_1(actor_A, moment):
    affected_entities = entities_affected_by(moment)
    # Includes: partner (if directed), space participants, thing users

    for entity in affected_entities:
        LD = LimbicDelta(entity, moment)

        if abs(LD.net) < LIMBIC_DELTA_THRESHOLD:
            continue  # noise, not signal

        cascade_step_2(actor_A, entity, LD, moment)
```

**Constants:**
```
LIMBIC_DELTA_THRESHOLD = 0.05  # minimum delta to trigger trust cascade
```

---

### Step 2: Trust on Direct Link Updates (Asymptotic)

If the Limbic Delta is positive, trust on the link from A to the affected entity increases. If negative, trust decreases.

**The asymptotic formula:**

```
cascade_step_2(actor_A, affected_entity, LD, moment):
    link = get_or_create_link(actor_A, affected_entity)
    W = link.trust  # current trust level

    if LD.net > 0:
        # TRUST INCREASE — asymptotic approach to 1.0
        # ΔW = α × U × (1 - W)
        # As W approaches 1.0, the same effort produces diminishing returns
        # This means: approaching 1.0 gets 10x harder than going from 0 to 0.5
        alpha = TRUST_LEARNING_RATE
        U = LD.net  # utility (positive Limbic Delta)
        delta_trust = alpha * U * (1.0 - W)

    elif LD.net < 0:
        # TRUST DECREASE — proportional to current trust and damage
        # Trust falls faster from high levels (more to lose)
        alpha = TRUST_LEARNING_RATE * TRUST_DAMAGE_MULTIPLIER
        D = abs(LD.net)  # damage (negative Limbic Delta magnitude)
        delta_trust = -alpha * D * W

    else:
        delta_trust = 0.0

    link.trust = clamp(W + delta_trust, 0.0, 1.0)

    # Also update affinity/aversion based on valence
    if LD.net > 0:
        link.affinity = min(1.0, link.affinity + AFFINITY_LEARNING_RATE * LD.net)
    else:
        link.aversion = min(1.0, link.aversion + AFFINITY_LEARNING_RATE * abs(LD.net))

    cascade_step_3(actor_A, moment, link)
```

**Constants:**
```
TRUST_LEARNING_RATE = 0.02        # base rate for trust changes
TRUST_DAMAGE_MULTIPLIER = 2.0     # trust falls faster than it rises
AFFINITY_LEARNING_RATE = 0.02     # from existing constants.py
```

**Mathematical properties of the asymptotic formula:**

```
ΔW = α × U × (1 - W)

At W=0.0:   ΔW = α × U × 1.0      (maximum possible increase)
At W=0.5:   ΔW = α × U × 0.5      (half the increase rate)
At W=0.9:   ΔW = α × U × 0.1      (one-tenth the increase rate)
At W=0.99:  ΔW = α × U × 0.01     (one-hundredth the increase rate)

Time to reach trust level T (assuming constant utility U per interaction):
    t(T) = -ln(1 - T) / (α × U)

    t(0.5)  = 0.693 / (α × U)      ≈  35 interactions at α=0.02, U=1.0
    t(0.9)  = 2.303 / (α × U)      ≈ 115 interactions
    t(0.99) = 4.605 / (α × U)      ≈ 230 interactions
    t(0.999)= 6.908 / (α × U)      ≈ 345 interactions

Ratio: reaching 0.99 takes ~6.6x longer than reaching 0.5.
This means the last 10% of trust is as hard to earn as the first 90%.
```

---

### Step 3: Trust on Thing-Link Updates

If the moment involved using a thing (tool, document, code), trust on the link from actor to thing also updates.

```
cascade_step_3(actor_A, moment, direct_link):
    things_used = get_things_used_in(moment)

    for thing in things_used:
        thing_link = get_or_create_link(actor_A, thing)

        # Trust in the thing increases if the interaction was positive
        if direct_link.trust > thing_link.trust:
            # Thing gets credit when its use produces good outcomes
            delta = THING_TRUST_RATE * (direct_link.trust - thing_link.trust)
            thing_link.trust = min(1.0, thing_link.trust + delta)

        cascade_step_4(thing, actor_A, moment)
```

**Constants:**
```
THING_TRUST_RATE = 0.01  # things earn trust slower than actors
```

---

### Step 4: Energy Propagates to Creator via Abstracts Links

When a thing is used and trusted, energy flows back to the thing's creator via `abstracts` links. This is how creators benefit from their creations being used.

```
cascade_step_4(thing, user, moment):
    # Find the creator of this thing
    creator_links = [l for l in thing.inbound_links
                     if l.link_type == "abstracts" or l.link_type == "created_by"]

    for creator_link in creator_links:
        creator = get_actor(creator_link.source_id)

        if creator is None or creator == user:
            continue  # self-use doesn't propagate

        # Energy propagation: thing's usage energy flows to creator
        # Proportional to: thing's trust * usage frequency * propagation rate
        energy_to_creator = (
            thing.trust_from(user)        # how much user trusts the thing
            * thing.energy                 # thing's current vitality
            * CREATOR_PROPAGATION_RATE     # propagation coefficient
        )

        # Apply energy to creator's achievement drive
        if creator.limbic:
            creator.limbic.drives["achievement"].intensity = min(
                DRIVE_MAX,
                creator.limbic.drives["achievement"].intensity + energy_to_creator * 0.1
            )

        cascade_step_5(user, creator, thing, energy_to_creator)
```

**Constants:**
```
CREATOR_PROPAGATION_RATE = 0.05   # fraction of usage energy that flows to creator
DRIVE_MAX = 1.0                   # from existing constants.py
```

---

### Step 5: Co-Activation Creates/Strengthens User-Creator Link

When a user and a creator are both "activated" by the same thing (user uses it, creator's nodes get energy from it), a co-activation signal emerges. This creates or strengthens the link between user and creator — even if they have never directly interacted.

```
cascade_step_5(user, creator, thing, energy_signal):
    # Co-activation: both user and creator are activated by the same thing
    # This follows Law 5 (Hebbian reinforcement) at the inter-actor level

    user_creator_link = get_or_create_link(user, creator)

    # Co-activation signal
    coactivation = min(user.energy_toward(thing), creator.energy_from(thing))

    if coactivation > COACTIVATION_THRESHOLD:
        # Strengthen the user-creator link
        delta_weight = INTER_ACTOR_LEARNING_RATE * coactivation
        user_creator_link.weight += delta_weight
        user_creator_link.co_activation_count += 1
        user_creator_link.last_co_activated_at = now()

        # Trust also grows (but slower than weight)
        # Using the asymptotic formula from Step 2
        W = user_creator_link.trust
        delta_trust = INDIRECT_TRUST_RATE * coactivation * (1.0 - W)
        user_creator_link.trust = min(1.0, W + delta_trust)
```

**Constants:**
```
COACTIVATION_THRESHOLD = 0.1       # minimum co-activation to trigger reinforcement
INTER_ACTOR_LEARNING_RATE = 0.01   # slower than direct interaction (Law 5 uses 0.05)
INDIRECT_TRUST_RATE = 0.005        # indirect trust grows very slowly
```

**This is how creators earn trust from people they've never met.** If Alice creates a tool, Bob uses it and has a positive experience, the co-activation of Alice's creation and Bob's usage creates a trust link from Bob to Alice. Alice never talked to Bob — her creation spoke for her.

---

### Step 6: Actor Reputation Computed

After all cascades resolve, the actor's reputation is the aggregation of all inbound trust.

```
cascade_step_6_compute_reputation(actor):
    inbound = inbound_links(actor)

    if not inbound:
        return 0.0

    # Weighted mean of trust, weighted by link weight
    total_weighted_trust = sum(l.trust * l.weight for l in inbound)
    total_weight = sum(l.weight for l in inbound)

    reputation = total_weighted_trust / max(total_weight, EPSILON)

    # Apply diversity bonus: trust from many diverse sources > trust from few
    unique_sources = len(set(l.source_id for l in inbound))
    diversity_factor = 1.0 + DIVERSITY_BONUS * log(max(unique_sources, 1))

    # Apply consistency bonus: low variance in trust scores = reliable
    trust_values = [l.trust for l in inbound]
    trust_variance = variance(trust_values)
    consistency_factor = 1.0 / (1.0 + trust_variance)

    adjusted_reputation = reputation * diversity_factor * consistency_factor

    return clamp(adjusted_reputation, 0.0, 1.0)
```

**Constants:**
```
EPSILON = 1e-10
DIVERSITY_BONUS = 0.1              # logarithmic bonus for diverse trust sources
```

---

## TEMPERING MECHANISMS

Three mechanisms prevent trust from being gamed, inflated, or stagnant.

---

### Tempering 1: Asymptotic Trust Growth

Already defined in Step 2. The formula `ΔW = α × U × (1 - W)` ensures:

- **Easy to build initial trust** (W near 0 → full learning rate)
- **Hard to reach high trust** (W near 1 → diminishing returns)
- **Impossible to reach perfect trust** (W=1.0 is asymptotic limit)

**Practical implications:**

```
# Trust growth per unit of value created at different trust levels:
W = 0.1  →  ΔW = 0.02 × U × 0.9  = 0.018 × U    # fast growth
W = 0.5  →  ΔW = 0.02 × U × 0.5  = 0.010 × U    # moderate
W = 0.8  →  ΔW = 0.02 × U × 0.2  = 0.004 × U    # slow
W = 0.95 →  ΔW = 0.02 × U × 0.05 = 0.001 × U    # very slow
W = 0.99 →  ΔW = 0.02 × U × 0.01 = 0.0002 × U   # glacial

# This creates a natural moat: high-trust actors are extremely hard to displace.
# A newcomer doing the same work as a veteran needs ~10x more interactions
# to reach the veteran's trust level.
```

---

### Tempering 2: Temporal Decay (Law 7 Applied to Trust)

Trust that is not reinforced decays. Unused links weaken. This prevents stale trust from persisting indefinitely.

```
apply_temporal_decay(link, tick):
    # Trust decays at the same rate as link weights (Law 7)
    # But identity-protected links (high co-activation, long history) decay slower

    base_decay = LONG_TERM_DECAY  # 0.001 from constants.py

    # Protection factors:
    # 1. High co-activation count = established relationship
    history_protection = min(1.0, link.co_activation_count / HISTORY_PROTECTION_THRESHOLD)

    # 2. Recency of last interaction
    recency = temporal_weight(
        age_hours=(now() - link.last_co_activated_at).hours,
        half_life=168  # 7 days
    )

    # 3. Trust level itself provides some inertia (high trust decays slower)
    trust_inertia = link.trust * TRUST_INERTIA_FACTOR

    effective_decay = base_decay * (1.0 - history_protection * 0.5) * (1.0 - recency * 0.3) * (1.0 - trust_inertia * 0.2)

    link.trust *= (1.0 - effective_decay)

    # Link dissolution: if both trust AND weight drop below threshold, link dies
    if link.trust < LINK_MIN_TRUST and link.weight < LINK_MIN_WEIGHT:
        dissolve_link(link)
```

**Constants:**
```
LONG_TERM_DECAY = 0.001            # from constants.py
HISTORY_PROTECTION_THRESHOLD = 50  # co-activations needed for full protection
TRUST_INERTIA_FACTOR = 0.5         # high trust resists decay
LINK_MIN_TRUST = 0.01              # below this, trust is negligible
LINK_MIN_WEIGHT = 0.005            # from constants.py
```

**Practical decay rates:**

```
# Fresh link (co_activation=1, last_active=7d ago, trust=0.3):
effective_decay ≈ 0.001 * 0.99 * 0.85 * 0.94 ≈ 0.00079
trust_after_30d ≈ 0.3 * (1 - 0.00079)^30 ≈ 0.293   (slow decay, recent)

# Dormant link (co_activation=5, last_active=90d ago, trust=0.5):
effective_decay ≈ 0.001 * 0.95 * 0.997 * 0.9 ≈ 0.00085
trust_after_30d ≈ 0.5 * (1 - 0.00085)^30 ≈ 0.487   (moderate decay)

# Abandoned link (co_activation=2, last_active=365d ago, trust=0.2):
effective_decay ≈ 0.001 * 0.98 * 1.0 * 0.96 ≈ 0.00094
trust_after_30d ≈ 0.2 * (1 - 0.00094)^30 ≈ 0.194   (faster decay)

# Established link (co_activation=100, last_active=1d ago, trust=0.9):
effective_decay ≈ 0.001 * 0.50 * 0.71 * 0.82 ≈ 0.00029
trust_after_30d ≈ 0.9 * (1 - 0.00029)^30 ≈ 0.892   (very slow decay, protected)
```

---

### Tempering 3: Boredom Erosion (Law 15 Applied to Trust)

Stagnation without innovation erodes trust moat. If an actor's contributions become repetitive, the trust premium from past innovation decays faster.

```
apply_boredom_erosion(actor, tick):
    # Measure stagnation in actor's contributions
    recent_moments = moments(actor, window=30d)

    if not recent_moments:
        stagnation = 1.0  # complete silence = maximum stagnation
    else:
        # Novelty measurement: how different are recent contributions from older ones?
        older_moments = moments(actor, window=(90d, 30d))  # 30-90 days ago

        if older_moments:
            recent_centroid = mean_embedding(recent_moments)
            older_centroid = mean_embedding(older_moments)
            novelty = 1.0 - cosine_similarity(recent_centroid, older_centroid)
        else:
            novelty = 1.0  # no prior work = everything is novel

        # Usage trend: are people still using actor's things?
        usage_trend = usage_count(actor.things, window=30d) / max(usage_count(actor.things, window=(60d, 30d)), 1)

        # Stagnation = low novelty AND declining usage
        stagnation = (1.0 - novelty) * max(0, 1.0 - usage_trend)

    if stagnation > BOREDOM_EROSION_THRESHOLD:
        # Apply erosion to all inbound trust links
        erosion_rate = BOREDOM_EROSION_RATE * (stagnation - BOREDOM_EROSION_THRESHOLD)

        for link in inbound_links(actor):
            # Only erode the "premium" above baseline
            # Baseline = trust earned from consistent reliability
            # Premium = trust earned from innovation/novelty
            baseline_trust = BASELINE_TRUST_FLOOR
            premium = max(0, link.trust - baseline_trust)

            if premium > 0:
                link.trust -= erosion_rate * premium
                link.trust = max(baseline_trust, link.trust)
```

**Constants:**
```
BOREDOM_EROSION_THRESHOLD = 0.5    # stagnation level that triggers erosion
BOREDOM_EROSION_RATE = 0.01        # per-tick erosion of trust premium
BASELINE_TRUST_FLOOR = 0.3         # trust from reliability is protected from boredom erosion
```

**Why this matters:**

An actor who created a brilliant tool 6 months ago and has done nothing since will see their trust premium erode. The tool still works (baseline trust preserved), but the innovation premium — the extra trust earned from the breakthrough — fades. This prevents resting on laurels.

```
# Example: Actor created infrastructure tool (type 8), trust reached 0.85
# After 90 days of no innovation:

stagnation = (1.0 - 0.1) * (1.0 - 0.7) = 0.27  # below threshold, no erosion yet

# After 180 days of no innovation:
stagnation = (1.0 - 0.05) * (1.0 - 0.5) = 0.475  # still below threshold

# After 270 days:
stagnation = (1.0 - 0.02) * (1.0 - 0.3) = 0.686  # above threshold!
erosion = 0.01 * (0.686 - 0.5) = 0.00186
premium = 0.85 - 0.3 = 0.55
trust_loss_per_tick = 0.00186 * 0.55 = 0.00102

# Trust decays from 0.85 toward 0.3 baseline at ~0.001/tick
# After 365 more ticks: trust ≈ 0.85 - 0.001 * 365 = 0.485
# The actor needs to innovate again to rebuild the premium
```

---

## COMPLETE CASCADE FLOW DIAGRAM

```
Actor A does something
        │
        ▼
  [Moment created in graph]
        │
        ▼
  Step 1: Identify affected entities
        │
        ├──► Entity 1: measure LimbicDelta
        │         │
        │         ▼
        │    Step 2: Update trust on link(A → Entity1)
        │         │    ΔW = α × U × (1 - W)     [asymptotic]
        │         │
        │         ▼
        │    Step 3: Update trust on link(A → things_used)
        │         │
        │         ▼
        │    Step 4: Energy flows thing → creator via abstracts
        │         │
        │         ▼
        │    Step 5: Co-activation creates link(user → creator)
        │         │    Trust grows on this indirect link
        │         │
        │         ▼
        │    Step 6: Recompute actor reputations
        │
        ├──► Entity 2: same cascade...
        └──► Entity N: same cascade...

  [Concurrent tempering, every tick:]
        │
        ├──► Tempering 1: Asymptotic growth (built into Step 2)
        ├──► Tempering 2: Temporal decay (Law 7 schedule)
        └──► Tempering 3: Boredom erosion (Law 15 schedule)
```

---

## INTERACTION WITH EXISTING PHYSICS

### Law 5 (Co-activation Reinforcement)

Step 5 extends Law 5 from intra-brain to inter-actor. The same Hebbian principle — "what fires together wires together" — operates at the social level. Two actors activated by the same thing form a connection.

```
# Intra-brain (Law 5, existing):
link.weight += LEARNING_RATE * node_a.energy * node_b.energy
# LEARNING_RATE = 0.05

# Inter-actor (Step 5, this algorithm):
link.weight += INTER_ACTOR_LEARNING_RATE * coactivation_signal
# INTER_ACTOR_LEARNING_RATE = 0.01 (5x slower — social bonds form slowly)
```

### Law 7 (Forgetting)

Tempering 2 applies the same decay mechanics as Law 7, with trust-specific protection factors. The key constant `LONG_TERM_DECAY = 0.001` is shared.

### Law 15 (Boredom)

Tempering 3 extends boredom from an individual emotion to a trust mechanism. Stagnation in an actor's contributions erodes their trust premium, analogous to how WM stagnation increases boredom within a single brain.

### Law 18 (Relational Valence)

Step 2's affinity/aversion updates parallel Law 18's valence updates. The key constant `AFFINITY_LEARNING_RATE = 0.02` is shared.

---

## TRUST TIERS MAPPING

Mind Protocol has 5 trust tiers. The computed trust score maps to tiers:

```
trust_to_tier(trust_score):
    if trust_score >= 0.95:  return "Owner"      # near-perfect trust, extremely rare
    if trust_score >= 0.75:  return "High"        # strong established relationship
    if trust_score >= 0.45:  return "Medium"      # proven reliability
    if trust_score >= 0.15:  return "Low"         # some positive history
    return "Stranger"                              # no trust history or very low

# Trust only goes up (per protocol). Exclusion handles violations.
# But note: trust CAN decrease through decay and boredom erosion.
# "Trust only goes up" means: the TIER boundary ratchets.
# Once an actor reaches "High" tier, they can't drop to "Medium" through decay alone.
# Only explicit violation → exclusion (removal from network, not demotion).

tier_ratchet(actor):
    current_tier = actor.trust_tier
    computed_tier = trust_to_tier(actor.reputation)

    if tier_rank(computed_tier) > tier_rank(current_tier):
        actor.trust_tier = computed_tier  # promote

    # Demotion only through explicit exclusion process, not through score decay
    # This prevents trust oscillation from temporal noise
```

---

## ECONOMIC COUPLING

Trust directly affects $MIND transaction costs:

```
transaction_cost(sender, receiver, amount):
    trust = get_trust(sender, receiver)

    # Higher trust = lower friction = lower cost
    # Stranger: 5% fee
    # Low:      3% fee
    # Medium:   1.5% fee
    # High:     0.5% fee
    # Owner:    0.1% fee

    fee_schedule = {
        "Stranger": 0.05,
        "Low":      0.03,
        "Medium":   0.015,
        "High":     0.005,
        "Owner":    0.001,
    }

    tier = trust_to_tier(trust)
    fee = fee_schedule[tier]

    return amount * fee
```

This creates a structural incentive for trust-building: the more trusted you are, the cheaper every transaction becomes. Long-term cooperation is LITERALLY more profitable than short-term extraction.

---

## ANTI-GAMING PROPERTIES

### Sybil Resistance

Creating many fake identities to vouch for each other is unprofitable because:
1. New links start at trust 0 (Stranger tier = 5% fee)
2. Trust grows asymptotically (each new fake needs sustained positive interaction)
3. Temporal decay kills inactive links
4. Reputation requires DIVERSE sources (diversity_factor in Step 6)
5. Co-activation requires real things being used by real actors (Step 5)

### Trust Inflation Resistance

Two actors repeatedly exchanging positive signals cannot inflate trust indefinitely because:
1. Asymptotic formula caps trust at 1.0 with exponentially increasing difficulty
2. Boredom erosion penalizes repetitive interactions (same two actors, same patterns)
3. Diversity factor in reputation means broad trust > deep trust from one source

### Pump-and-Dump Resistance

Building trust quickly then exploiting it is deterred because:
1. Trust grows slowly (asymptotic)
2. Trust damage is 2x faster than trust growth (TRUST_DAMAGE_MULTIPLIER)
3. Exclusion (not score reduction) for violations removes actor entirely
4. Vouch chains create skin-in-the-game: voucher's trust is at risk

---

## CONSTANTS SUMMARY

| Constant | Value | Source | Purpose |
|----------|-------|--------|---------|
| LIMBIC_DELTA_THRESHOLD | 0.05 | new | Minimum delta to trigger cascade |
| TRUST_LEARNING_RATE | 0.02 | new | Base rate for trust changes |
| TRUST_DAMAGE_MULTIPLIER | 2.0 | new | Trust falls faster than it rises |
| AFFINITY_LEARNING_RATE | 0.02 | constants.py | Affinity/aversion update rate |
| THING_TRUST_RATE | 0.01 | new | Things earn trust slower than actors |
| CREATOR_PROPAGATION_RATE | 0.05 | new | Energy fraction flowing to creators |
| DRIVE_MAX | 1.0 | constants.py | Maximum drive intensity |
| COACTIVATION_THRESHOLD | 0.1 | new (cf. ACTIVATION_THRESHOLD=0.1) | Minimum co-activation for reinforcement |
| INTER_ACTOR_LEARNING_RATE | 0.01 | new (cf. LEARNING_RATE=0.05) | Social bond formation rate |
| INDIRECT_TRUST_RATE | 0.005 | new | Indirect trust growth rate |
| LONG_TERM_DECAY | 0.001 | constants.py | Base decay rate for temporal erosion |
| HISTORY_PROTECTION_THRESHOLD | 50 | new | Co-activations for full history protection |
| TRUST_INERTIA_FACTOR | 0.5 | new | High trust resists decay |
| LINK_MIN_TRUST | 0.01 | new (cf. LINK_MIN_WEIGHT=0.005) | Trust dissolution threshold |
| LINK_MIN_WEIGHT | 0.005 | constants.py | Weight dissolution threshold |
| BOREDOM_EROSION_THRESHOLD | 0.5 | new | Stagnation level triggering erosion |
| BOREDOM_EROSION_RATE | 0.01 | new | Per-tick erosion rate of trust premium |
| BASELINE_TRUST_FLOOR | 0.3 | new | Reliability trust protected from erosion |
| DIVERSITY_BONUS | 0.1 | new | Log bonus for diverse trust sources |
| EPSILON | 1e-10 | standard | Division safety |

---

## MARKERS

<!-- @mind:todo Validate constant values through simulation: run cascade on synthetic graph, verify trust distribution is realistic -->
<!-- @mind:todo Define measurement_window for LimbicDelta computation: how long after a moment do we measure the delta? -->
<!-- @mind:todo Integrate with existing Law 18 relational valence: should Step 2 call Law 18 directly or maintain separate update? -->
<!-- @mind:proposition Consider making LIMBIC_WEIGHTS configurable per actor (different actors may weight different drives differently based on their personality) -->
<!-- @mind:proposition Consider a "trust shock" mechanism for extreme positive events (heroic acts) that bypasses asymptotic growth temporarily -->
