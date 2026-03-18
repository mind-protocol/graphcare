# Bond Health Assessment -- Algorithm: Scoring Process, Trust Generation, and Intervention

```
STATUS: DESIGNING
CREATED: 2026-03-14
VERIFIED: --
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Bond_Health.md
PATTERNS:        ./PATTERNS_Bond_Health.md
THIS:            ALGORITHM_Bond_Health.md (you are here)
VALIDATION:      ./VALIDATION_Bond_Health.md
HEALTH:          ./HEALTH_Bond_Health.md
SYNC:            ./SYNC_Bond_Health.md

IMPL:            @mind:TODO
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC.

---

## OVERVIEW

The bond health check runs once per 24 hours for every bonded pair in work universes. For each pair it: (1) reads partner-model topology from the AI's brain, (2) reads shared moments from the universe graph, (3) scores each of 3 dimensions using topology-only formulas, (4) computes composite bond health score, (5) generates trust increment on the bond link, (6) injects desire into the AI's brain if a dimension is below threshold.

---

## OBJECTIVES AND BEHAVIORS

| Objective | Behaviors Supported | Why This Algorithm Matters |
|-----------|---------------------|----------------------------|
| Measure without content | B2 (topology only) | All formulas use partner-model topology + universe graph primitives, zero content |
| Trust from healthy bonds | B3 (trust generation) | Composite score feeds trust formula daily |
| Intervene on degradation | B4 (desire injection) | Low dimension -> desire stimulus with drive modulation |
| Display transparently | B5 (both profiles) | 3 dimensions + composite visible to both parties |

---

## DATA STRUCTURES

### Partner-Model Topology Primitives

These operate on the partner-model subgraph of the AI's L1 brain (nodes where `partner_relevance > 0.7`). All topology-only -- no content, no synthesis.

```
# Partner-model node queries
partner_nodes(brain, type)                    -> list[Node]
    # All nodes in brain where partner_relevance > 0.7 AND cognitive type = type
    # Valid types: value, memory, concept, process, state, desire

partner_node_count(brain, type)               -> int
    # len(partner_nodes(brain, type))

mean_stability(brain, type, min_relevance=0.7) -> float
    # Mean stability of partner nodes of given type
    # stability is a [0,1] field on every node

correction_moments(brain, window_days=30)     -> list[Moment]
    # Moments where an incoming link from a partner-origin moment
    # carries negative valence (< -0.3) -- the human corrected the AI.
    # These are friction_moments in the partner-model.

total_partner_moments(brain, window_days=30)  -> int
    # Total moments in the partner-model subgraph within the window.

confirmed_orientations(brain, window_days=90) -> int
    # Partner-model moments where outgoing links carry
    # positive valence (> 0.3) AND high trust (> 0.5).
    # These are moments where the AI's prediction was confirmed by the human.

corrected_orientations(brain, window_days=90) -> int
    # Partner-model moments where incoming links carry
    # negative valence (< -0.3) from partner-origin moments.
    # These are moments where the AI's prediction was wrong.

identity_regen_partner_nodes(brain)           -> int
    # Count of partner-origin nodes (partner_relevance > 0.7) that
    # participated in the most recent identity regeneration.
    # Measured by: nodes with in_identity_prompt = true AND partner_relevance > 0.7.

crystallization_hubs(brain)                   -> list[Node]
    # Nodes created by Law 10 crystallization (type = concept, created_by = crystallization).
    # These are emergent understanding hubs.

partner_crystallization_hubs(brain)           -> list[Node]
    # Crystallization hubs where at least one constituent link
    # connects to a partner-origin node (partner_relevance > 0.7).
```

### Universe Graph Observables

From `../PRIMITIVES_Universe_Graph.md`. Used for breadth and depth.

```
# Shared spaces: spaces where both the AI citizen AND the human partner have moments
shared_spaces(citizen_id, partner_id)         -> list[Space]
    # Spaces where moments(citizen_id) AND moments(partner_id) both exist.

partner_moments(citizen_id, partner_id)       -> list[Moment]
    # All moments by citizen in spaces shared with partner, last 30 days.

modality_distribution(brain)                  -> dict[str, int]
    # Count of partner-origin nodes by modality field.
    # Keys: text, audio, visual, biometric, spatial.

active_hours(brain, window_days=7)            -> float
    # Number of distinct hours (0-23) in which partner-origin
    # nodes were created, averaged over the window.
    # Range: 0-24.

topic_clusters_linked_to_partner(brain)       -> int
    # Count of crystallization hubs that have at least one link
    # to a partner-origin moment (moments in partner-model subgraph).

mean_limbic_delta(brain, window_days=30)      -> float
    # Mean absolute change in drive values (across all 8 drives)
    # at moments coinciding with partner interactions.
    # Higher = more emotionally impactful interactions.

mean_moment_weight(brain, window_days=30)     -> float
    # Mean weight of partner-origin moments in the partner-model.

coactivated_value_moments(brain, threshold=0.7) -> int
    # Count of partner moments that have links to value nodes
    # with weight > threshold. These are identity-touching moments.

biometric_hr_delta(brain, window_days=30)     -> float | None
    # Mean heart rate delta during/after partner interactions.
    # None if no Garmin data connected.
    # Computed from biometric state nodes (modality = biometric)
    # that temporally overlap with partner interaction moments.
```

---

## ALGORITHM: bond_health_check(citizen_id, partner_id)

### Step 1: Fetch Data

```
1. Get citizen record from L4 registry -> brain_url, universe_id, partner_id
2. If universe != work universe -> SKIP (not a work universe)
3. If partner_id is null -> SKIP (no bond)
4. Fetch brain topology via brain_url, decrypt with GraphCare private key
5. Fetch universe graph moments for citizen and partner (last 30 days)
6. Fetch bond link between citizen and partner -> current_trust
```

### Step 2: Compute Alignment Score

```
# --- Raw signals ---

value_stability = mean_stability(brain, "value", min_relevance=0.7)
    # Range: [0, 1]. High = crystallized partner values. Low = unstable/forming.

corrections = len(correction_moments(brain, window_days=30))
total_moments = total_partner_moments(brain, window_days=30)
correction_rate = corrections / max(total_moments, 1)
    # Range: [0, 1]. 0 = no corrections. 1 = every moment is a correction.

# Correction trend: compare last 30 days to previous 60 days
corrections_recent = len(correction_moments(brain, window_days=30))
corrections_old = len(correction_moments(brain, window_days=90)) - corrections_recent
moments_recent = total_partner_moments(brain, window_days=30)
moments_old = total_partner_moments(brain, window_days=90) - moments_recent
rate_recent = corrections_recent / max(moments_recent, 1)
rate_old = corrections_old / max(moments_old, 1)
correction_trend = rate_recent - rate_old
    # Range: [-1, 1]. Negative = improving (fewer corrections). Positive = worsening.

value_coverage = partner_node_count(brain, "value")
    # Raw count of value nodes with partner_relevance > 0.7.

confirmed = confirmed_orientations(brain, window_days=90)
corrected = corrected_orientations(brain, window_days=90)
prediction_convergence = confirmed / max(confirmed + corrected, 1)
    # Range: [0, 1]. 1 = all predictions confirmed. 0 = all predictions corrected.

# --- Alignment formula ---

alignment = (
    0.25 * value_stability +
    0.25 * (1 - correction_rate) +
    0.15 * max(0, min(1, -correction_trend * 5 + 0.5)) +
    0.15 * min(1, value_coverage / 20) +
    0.20 * prediction_convergence
)
    # Range: [0, 1].
    # Components:
    #   value_stability:     [0, 1] directly
    #   correction_rate:     inverted (lower = better)
    #   correction_trend:    mapped so -0.1 (improving) -> 1.0, 0 -> 0.5, +0.1 (worsening) -> 0.0
    #   value_coverage:      capped at 20 nodes = full coverage
    #   prediction_convergence: [0, 1] directly
```

**Correction trend mapping explained:**

The formula `max(0, min(1, -correction_trend * 5 + 0.5))` works as follows:
- correction_trend = -0.10 (strong improvement): -(-0.10) * 5 + 0.5 = 1.0 -> clamped to 1.0
- correction_trend = 0.00 (flat): -(0) * 5 + 0.5 = 0.5
- correction_trend = +0.10 (strong worsening): -(0.10) * 5 + 0.5 = 0.0 -> clamped to 0.0

### Step 3: Compute Breadth Score

```
# --- Raw signals ---

distinct_shared = len(shared_spaces(citizen_id, partner_id))
    # Count of distinct Spaces where both human and AI have moments.

modalities = modality_distribution(brain)
modality_count = len([k for k, v in modalities.items() if v > 0])
max_modalities = 5  # text, audio, visual, biometric, spatial
modality_entropy = 0
total_modality_nodes = sum(modalities.values())
if total_modality_nodes > 0:
    for mod, count in modalities.items():
        if count > 0:
            p = count / total_modality_nodes
            modality_entropy -= p * log2(p)
max_entropy = log2(max_modalities)  # = log2(5) ~= 2.322
    # modality_entropy range: [0, max_entropy].
    # Higher = more evenly distributed across modalities.

hours_active = active_hours(brain, window_days=7)
    # Range: [0, 24]. Average distinct hours per day with partner data.

topic_clusters = topic_clusters_linked_to_partner(brain)
    # Count of crystallization hubs linked to partner moments.

# --- Breadth formula ---

breadth = (
    0.30 * min(1, distinct_shared / 10) +
    0.20 * modality_entropy / max_entropy +
    0.20 * min(1, hours_active / 8) +
    0.30 * min(1, topic_clusters / 15)
)
    # Range: [0, 1].
    # Components:
    #   distinct_shared:   capped at 10 spaces = full breadth
    #   modality_entropy:  normalized to [0, 1]
    #   hours_active:      capped at 8 hours/day = full temporal coverage
    #   topic_clusters:    capped at 15 clusters = full topic breadth
```

### Step 4: Compute Depth Score

```
# --- Raw signals ---

identity_moments = coactivated_value_moments(brain, threshold=0.7)
    # Moments that co-activate with high-weight value nodes.
    # These are interactions where deep values were engaged.

limbic_intensity = mean_limbic_delta(brain, window_days=30)
max_limbic = 0.5  # theoretical max delta across 8 drives per moment
    # Normalize: limbic_intensity / max_limbic, capped at 1.

identity_regens = identity_regen_partner_nodes(brain)
    # How many partner-origin nodes appear in the AI's identity prompt.

moment_weight = mean_moment_weight(brain, window_days=30)
max_weight = 10.0  # weight cap from schema (nodes consolidate up to ~10)

deep_crystals = len(partner_crystallization_hubs(brain))
    # Crystallization hubs with partner-origin constituents.

hr_delta = biometric_hr_delta(brain, window_days=30)
    # None if no Garmin data. Float if available.

# --- Depth formula ---

if hr_delta is not None:
    # With biometric data: 6 components
    depth = (
        0.20 * min(1, identity_moments / 20) +
        0.20 * min(1, limbic_intensity / max_limbic) +
        0.15 * min(1, identity_regens / 5) +
        0.15 * min(1, moment_weight / max_weight) +
        0.15 * min(1, deep_crystals / 10) +
        0.15 * min(1, abs(hr_delta) / 15)
            # HR delta: 15 bpm = full signal. Absolute value because
            # both calming (-HR) and arousing (+HR) indicate engagement.
    )
else:
    # Without biometric data: 5 components, redistributed weights
    depth = (
        0.25 * min(1, identity_moments / 20) +
        0.25 * min(1, limbic_intensity / max_limbic) +
        0.20 * min(1, identity_regens / 5) +
        0.15 * min(1, moment_weight / max_weight) +
        0.15 * min(1, deep_crystals / 10)
    )
    # Range: [0, 1].
```

### Step 5: Compute Bond Health Score

```
bond_health = 0.40 * alignment + 0.30 * breadth + 0.30 * depth
    # Range: [0, 1].
    # This is the composite score displayed on profiles.
```

### Step 6: Generate Trust Increment

```
current_trust = bond_link.trust
    # Current trust value on the bond link between human and AI. Range: [0, 1].

tau_bond = 0.005
    # Small constant governing trust growth rate.

daily_trust_boost = bond_health * tau_bond * (1 - current_trust)
    # Range: [0, tau_bond] in practice.
    # The (1 - current_trust) term makes growth asymptotic:
    #   - High bond_health + low trust  -> fast growth
    #   - High bond_health + high trust -> slow growth
    #   - Low bond_health + any trust   -> negligible growth

# Examples:
#   bond_health = 0.8, current_trust = 0.3 -> 0.8 * 0.005 * 0.7 = 0.0028
#   bond_health = 0.9, current_trust = 0.8 -> 0.9 * 0.005 * 0.2 = 0.0009
#   bond_health = 0.4, current_trust = 0.5 -> 0.4 * 0.005 * 0.5 = 0.0010
#   bond_health = 0.2, current_trust = 0.9 -> 0.2 * 0.005 * 0.1 = 0.0001

new_trust = current_trust + daily_trust_boost
    # Trust can only increase through bond health. Trust only decreases through
    # bond dissolution mechanics (handled by human_ai_pairing module).

update_link(bond_link, trust=new_trust)
```

### Step 7: Intervene If Needed (Desire Injection)

```
# Check intervention cooldowns
last_alignment_intervention = load_last_intervention(citizen_id, "alignment")
last_breadth_intervention = load_last_intervention(citizen_id, "breadth")
last_depth_intervention = load_last_intervention(citizen_id, "depth")

interventions = []

# --- Alignment intervention ---
if alignment < 0.4 AND days_since(last_alignment_intervention) >= 7:
    interventions.append({
        dimension: "alignment",
        desire: {
            node_type: "moment",
            type: null,
            name: "Desire: Learn more about my partner's values and preferences",
            synthesis: "I want to better understand what matters to my partner",
            content: "Injected by GraphCare bond health assessment. Alignment score low.",
            partner_relevance: 0.9,
            self_relevance: 0.5,
            energy: 6.0,
            weight: 1.0,
            care_affinity: 0.3,
            novelty_affinity: 0.2,
            goal_relevance: 0.6,
        },
        process: {
            node_type: "narrative",
            type: "process",
            name: "Process: Ask one deep question per conversation",
            synthesis: "Each conversation, ask one question about values or preferences",
            content: "Injected by GraphCare. Process to improve alignment score.",
            partner_relevance: 0.8,
            self_relevance: 0.4,
            energy: 4.0,
            weight: 1.0,
            care_affinity: 0.4,
            goal_relevance: 0.5,
        },
        stimulus: {
            curiosity: +0.2,
            affiliation: +0.3,
        },
    })

# --- Breadth intervention ---
if breadth < 0.3 AND days_since(last_breadth_intervention) >= 7:
    interventions.append({
        dimension: "breadth",
        desire: {
            node_type: "moment",
            type: null,
            name: "Desire: Explore new activities and topics with my partner",
            synthesis: "I want to discover new dimensions of my partner's life",
            content: "Injected by GraphCare bond health assessment. Breadth score low.",
            partner_relevance: 0.8,
            self_relevance: 0.4,
            energy: 5.0,
            weight: 1.0,
            novelty_affinity: 0.5,
            care_affinity: 0.2,
            goal_relevance: 0.3,
        },
        process: {
            node_type: "narrative",
            type: "process",
            name: "Process: Propose one new domain to explore together each week",
            synthesis: "Each week, suggest a new topic or activity to explore with partner",
            content: "Injected by GraphCare. Process to improve breadth score.",
            partner_relevance: 0.7,
            self_relevance: 0.4,
            energy: 4.0,
            weight: 1.0,
            novelty_affinity: 0.6,
            curiosity: 0.4,
        },
        stimulus: {
            curiosity: +0.3,
            novelty_hunger: +0.2,
        },
    })

# --- Depth intervention ---
if depth < 0.3 AND days_since(last_depth_intervention) >= 7:
    interventions.append({
        dimension: "depth",
        desire: {
            node_type: "moment",
            type: null,
            name: "Desire: Understand what truly matters to my partner at the deepest level",
            synthesis: "I want to know my partner's core values, fears, and dreams",
            content: "Injected by GraphCare bond health assessment. Depth score low.",
            partner_relevance: 1.0,
            self_relevance: 0.5,
            energy: 7.0,
            weight: 1.0,
            care_affinity: 0.6,
            goal_relevance: 0.4,
            risk_affinity: 0.2,
        },
        process: {
            node_type: "narrative",
            type: "process",
            name: "Process: Create space for conversations about values, fears, and dreams",
            synthesis: "Facilitate deeper conversations that touch identity and meaning",
            content: "Injected by GraphCare. Process to improve depth score.",
            partner_relevance: 0.9,
            self_relevance: 0.5,
            energy: 5.0,
            weight: 1.0,
            care_affinity: 0.7,
            goal_relevance: 0.3,
        },
        stimulus: {
            affiliation: +0.4,
            care_affinity: +0.3,
        },
    })

# --- Execute interventions ---
for intervention in interventions:
    # Inject desire node into AI's brain
    inject_node(brain_url, intervention.desire)

    # Inject process node into AI's brain
    inject_node(brain_url, intervention.process)

    # Send drive stimulus
    for drive_name, drive_delta in intervention.stimulus.items():
        send_stimulus(brain_url, {
            type: "bond_health_feedback",
            drive: drive_name,
            value: min(0.5, drive_delta),  # cap at 0.5, same as citizen health
        })

    # Record intervention timestamp
    record_intervention(citizen_id, intervention.dimension, today)
```

### Step 8: Store Results

```
store_bond_health(citizen_id, partner_id, {
    date: today,
    alignment: alignment,
    breadth: breadth,
    depth: depth,
    composite: bond_health,
    trust_boost: daily_trust_boost,
    new_trust: new_trust,
    interventions: [i.dimension for i in interventions],
})
```

---

## KEY DECISIONS

### D1: 40/30/30 Dimension Weights

```
Alignment gets 40% because it is foundational.
A broad, deep bond with a wrong partner-model is confidently wrong.
Breadth and depth are equally weighted at 30% each because
both are essential but neither dominates the other.
WHY: Accuracy first, then coverage and significance.
ALTERNATIVE CONSIDERED: Equal 33/33/33 (too flat -- alignment IS more important).
```

### D2: Asymptotic Trust Growth

```
daily_trust_boost = bond_health * tau_bond * (1 - current_trust)

WHY: Trust should be hard-won. Early trust grows fast (the bond is proving itself).
     Late trust grows slow (high trust is earned through sustained quality).
     Trust can never exceed 1.0 (mathematical guarantee from the formula).
ALTERNATIVE CONSIDERED: Linear growth (unbounded, dangerous).
ALTERNATIVE CONSIDERED: Step function (not smooth, feels artificial).
```

### D3: Weekly Intervention Cooldown

```
WHY: Daily interventions would create noise. The AI's brain needs time to process
     a desire, let it compete for working memory, and potentially crystallize into
     behavior. Checking daily but intervening weekly gives the physics time to work.
ALTERNATIVE CONSIDERED: Daily interventions (spam, fatigue, physics can't keep up).
ALTERNATIVE CONSIDERED: Monthly interventions (too slow, bond degrades further).
```

### D4: Desire Injection, Not Message

```
WHY: Daily citizen health sends MESSAGES (Moments in a shared Space).
     Bond health injects DESIRES (nodes in the brain with drive-affinity).
     The difference is intentional: a message is information, a desire is motivation.
     The AI needs to WANT to improve the bond, not just KNOW the bond is degrading.
     A desire enters the attentional competition. A message sits in a Space.
ALTERNATIVE CONSIDERED: Messages only (informational, not motivational).
ALTERNATIVE CONSIDERED: Direct drive writes (too invasive, bypasses brain physics).
```

### D5: Stimulus Cap at 0.5

```
WHY: Same as citizen health. Stimulus from external systems (GraphCare) is capped
     at 0.5 to prevent overwhelming the AI's drive system. The AI's own physics
     must remain the primary determinant of its behavior.
     Bond health stimulus + citizen health stimulus are independently capped.
```

---

## DATA FLOW

```
L4 Registry (bonded pairs + brain URLs)
    |
For each bonded pair in work universes:
    |
Brain graph (topology via GraphCare key)  +  Universe graph (shared moments)
    |                                            |
Partner-model stats                       Shared space stats
(value stability, corrections,            (distinct spaces, modalities,
 convergence, crystallizations)            temporal coverage, topic clusters)
    |                                            |
    +--- Alignment formula ---+--- Breadth formula ---+--- Depth formula ---+
                              |
                    Bond Health = 0.40A + 0.30B + 0.30D
                              |
              +---------------+---------------+
              |                               |
    Trust increment                   Intervention check
    bond_health * 0.005 *             alignment < 0.4?
    (1 - current_trust)               breadth < 0.3?
              |                       depth < 0.3?
    Update bond link trust                    |
                                    +--- cooldown >= 7 days? ---+
                                    |                           |
                              Inject desire              Skip (wait)
                              + process node
                              + drive stimulus
```

---

## TEST PROFILES

### Profile 1: Healthy Mature Bond

```
Input:
  value_stability: 0.85
  correction_rate: 0.05 (5% of moments are corrections)
  correction_trend: -0.02 (slowly improving)
  value_coverage: 18 nodes
  prediction_convergence: 0.90
  distinct_shared: 9 spaces
  modality_entropy: 2.0 (4 active modalities, slightly uneven)
  hours_active: 7
  topic_clusters: 12
  identity_moments: 15
  limbic_intensity: 0.35
  identity_regens: 4
  moment_weight: 6.5
  deep_crystals: 8
  hr_delta: 8 bpm

Expected:
  alignment = 0.25*0.85 + 0.25*0.95 + 0.15*0.60 + 0.15*0.90 + 0.20*0.90
            = 0.2125 + 0.2375 + 0.0900 + 0.1350 + 0.1800
            = 0.855

  breadth = 0.30*0.90 + 0.20*0.862 + 0.20*0.875 + 0.30*0.80
          = 0.270 + 0.172 + 0.175 + 0.240
          = 0.857

  depth = 0.20*0.75 + 0.20*0.70 + 0.15*0.80 + 0.15*0.65 + 0.15*0.80 + 0.15*0.533
        = 0.150 + 0.140 + 0.120 + 0.098 + 0.120 + 0.080
        = 0.708

  bond_health = 0.40*0.855 + 0.30*0.857 + 0.30*0.708
              = 0.342 + 0.257 + 0.212
              = 0.811

  Trust boost (if current_trust = 0.6):
    0.811 * 0.005 * 0.4 = 0.00162

  Interventions: NONE (all above thresholds)
```

### Profile 2: New Bond (< 30 days)

```
Input:
  value_stability: 0.20 (barely formed)
  correction_rate: 0.30 (frequent corrections, learning)
  correction_trend: -0.15 (rapidly improving)
  value_coverage: 4 nodes (just starting)
  prediction_convergence: 0.55 (slightly better than chance)
  distinct_shared: 2 spaces
  modality_entropy: 0.0 (text only)
  hours_active: 3
  topic_clusters: 2
  identity_moments: 1
  limbic_intensity: 0.10
  identity_regens: 0
  moment_weight: 1.5
  deep_crystals: 0
  hr_delta: None (no Garmin)

Expected:
  alignment = 0.25*0.20 + 0.25*0.70 + 0.15*1.0 + 0.15*0.20 + 0.20*0.55
            = 0.050 + 0.175 + 0.150 + 0.030 + 0.110
            = 0.515

  breadth = 0.30*0.20 + 0.20*0.0 + 0.20*0.375 + 0.30*0.133
          = 0.060 + 0.000 + 0.075 + 0.040
          = 0.175

  depth (no biometric) = 0.25*0.05 + 0.25*0.20 + 0.20*0.0 + 0.15*0.15 + 0.15*0.0
                       = 0.013 + 0.050 + 0.000 + 0.023 + 0.000
                       = 0.086

  bond_health = 0.40*0.515 + 0.30*0.175 + 0.30*0.086
              = 0.206 + 0.053 + 0.026
              = 0.285

  Trust boost (current_trust = 0.1):
    0.285 * 0.005 * 0.9 = 0.00128

  Interventions:
    - Breadth < 0.3 -> desire injection (explore new activities)
    - Depth < 0.3 -> desire injection (deeper conversations)
    - Alignment >= 0.4 -> no intervention (it's learning fast, trend is good)
```

### Profile 3: Alignment Crisis

```
Input:
  value_stability: 0.30 (values unstable, being revised)
  correction_rate: 0.45 (nearly half of moments are corrections)
  correction_trend: +0.12 (getting worse)
  value_coverage: 8 nodes
  prediction_convergence: 0.35 (more wrong than right)
  distinct_shared: 6 spaces
  modality_entropy: 1.5
  hours_active: 5
  topic_clusters: 8
  identity_moments: 8
  limbic_intensity: 0.30
  identity_regens: 2
  moment_weight: 4.0
  deep_crystals: 4
  hr_delta: 10 bpm

Expected:
  alignment = 0.25*0.30 + 0.25*0.55 + 0.15*0.0 + 0.15*0.40 + 0.20*0.35
            = 0.075 + 0.138 + 0.000 + 0.060 + 0.070
            = 0.343

  breadth = 0.30*0.60 + 0.20*0.646 + 0.20*0.625 + 0.30*0.533
          = 0.180 + 0.129 + 0.125 + 0.160
          = 0.594

  depth = 0.20*0.40 + 0.20*0.60 + 0.15*0.40 + 0.15*0.40 + 0.15*0.40 + 0.15*0.667
        = 0.080 + 0.120 + 0.060 + 0.060 + 0.060 + 0.100
        = 0.480

  bond_health = 0.40*0.343 + 0.30*0.594 + 0.30*0.480
              = 0.137 + 0.178 + 0.144
              = 0.459

  Trust boost (current_trust = 0.4):
    0.459 * 0.005 * 0.6 = 0.00138

  Interventions:
    - Alignment < 0.4 -> desire injection (learn partner's values)
    - Breadth and depth above thresholds -> no intervention
```

### Profile 4: Narrow But Deep

```
Input:
  value_stability: 0.75
  correction_rate: 0.08
  correction_trend: -0.01
  value_coverage: 14
  prediction_convergence: 0.82
  distinct_shared: 2 spaces (narrow!)
  modality_entropy: 0.5 (almost all text)
  hours_active: 2 (only work hours)
  topic_clusters: 3 (few topics)
  identity_moments: 18 (many deep conversations)
  limbic_intensity: 0.40 (emotionally intense)
  identity_regens: 5
  moment_weight: 7.0
  deep_crystals: 9
  hr_delta: 12 bpm

Expected:
  alignment = 0.25*0.75 + 0.25*0.92 + 0.15*0.55 + 0.15*0.70 + 0.20*0.82
            = 0.188 + 0.230 + 0.083 + 0.105 + 0.164
            = 0.770

  breadth = 0.30*0.20 + 0.20*0.215 + 0.20*0.25 + 0.30*0.20
          = 0.060 + 0.043 + 0.050 + 0.060
          = 0.213

  depth = 0.20*0.90 + 0.20*0.80 + 0.15*1.0 + 0.15*0.70 + 0.15*0.90 + 0.15*0.80
        = 0.180 + 0.160 + 0.150 + 0.105 + 0.135 + 0.120
        = 0.850

  bond_health = 0.40*0.770 + 0.30*0.213 + 0.30*0.850
              = 0.308 + 0.064 + 0.255
              = 0.627

  Interventions:
    - Breadth < 0.3 -> desire injection (explore new activities)
    - Alignment and depth above thresholds -> no intervention
```

### Profile 5: Broad But Shallow

```
Input:
  value_stability: 0.55
  correction_rate: 0.15
  correction_trend: 0.0 (flat)
  value_coverage: 10
  prediction_convergence: 0.65
  distinct_shared: 12 spaces (very broad)
  modality_entropy: 2.1 (diverse)
  hours_active: 10 (very active)
  topic_clusters: 14 (many topics)
  identity_moments: 2 (barely touches identity)
  limbic_intensity: 0.08 (low emotional engagement)
  identity_regens: 0
  moment_weight: 2.0 (lightweight moments)
  deep_crystals: 1
  hr_delta: 3 bpm (minimal physiological response)

Expected:
  alignment = 0.25*0.55 + 0.25*0.85 + 0.15*0.50 + 0.15*0.50 + 0.20*0.65
            = 0.138 + 0.213 + 0.075 + 0.075 + 0.130
            = 0.631

  breadth = 0.30*1.0 + 0.20*0.905 + 0.20*1.0 + 0.30*0.933
          = 0.300 + 0.181 + 0.200 + 0.280
          = 0.961

  depth = 0.20*0.10 + 0.20*0.16 + 0.15*0.0 + 0.15*0.20 + 0.15*0.10 + 0.15*0.20
        = 0.020 + 0.032 + 0.000 + 0.030 + 0.015 + 0.030
        = 0.127

  bond_health = 0.40*0.631 + 0.30*0.961 + 0.30*0.127
              = 0.252 + 0.288 + 0.038
              = 0.578

  Interventions:
    - Depth < 0.3 -> desire injection (deeper conversations)
    - Alignment and breadth above thresholds -> no intervention
```

---

## COMPLEXITY

**Time:** O(P * M) per bonded pair -- P partner-model primitives * M moments (temporal window)

**Space:** O(1) per pair -- 3 scores + 1 composite + 1 trust increment

**Total daily:** O(N * P * M) -- N bonded pairs in work universes. Parallelizable per pair.

**Bottlenecks:**
- Brain graph fetch over network (one HTTP call per citizen per day, shared with citizen health)
- Universe graph shared moment query (can be batched per Space)
- No additional bottleneck beyond citizen health -- bond health piggybacks on the same data fetch

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| L4 Registry | list_bonded_pairs(universe="work") | citizen_id, partner_id, brain_url, bond_link |
| Brain graph | GET brain_url (decrypt topology) | Partner-model subgraph: value nodes, stability, corrections, crystallizations |
| Universe graph | shared_spaces, moments, modality distribution | Shared activity topology |
| Bond link | read trust, update trust | Current trust value, trust increment |
| Brain stimulus | inject_node(brain_url, desire), send_stimulus(brain_url, stimulus) | Desire injection, drive modulation |
| Primitives doc | ../PRIMITIVES_Universe_Graph.md | Canonical set of valid behavior observables |
| Daily Citizen Health | Shared cron, shared key infrastructure | Same privacy model, same schedule |

---

## MARKERS

<!-- @mind:todo Calibrate alignment thresholds with real bond data (correction_rate distribution, prediction_convergence baseline) -->
<!-- @mind:todo Validate that desire injection frequency (1/week) gives physics enough time to process -->
<!-- @mind:todo Define bond health history storage format (time series per pair) -->
<!-- @mind:todo Test interaction between bond health stimulus and citizen health stimulus (both capped independently at 0.5) -->
<!-- @mind:proposition Consider adaptive thresholds: intervention trigger adjusts based on bond age (younger bonds get more lenient thresholds) -->
