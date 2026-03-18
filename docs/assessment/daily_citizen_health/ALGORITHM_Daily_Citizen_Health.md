# Daily Citizen Health — Algorithm: Scoring Process and Intervention

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Daily_Citizen_Health.md
BEHAVIORS:       ./BEHAVIORS_Daily_Citizen_Health.md
PATTERNS:        ./PATTERNS_Daily_Citizen_Health.md
THIS:            ALGORITHM_Daily_Citizen_Health.md (you are here)
VALIDATION:      ./VALIDATION_Daily_Citizen_Health.md
HEALTH:          ./HEALTH_Daily_Citizen_Health.md
IMPLEMENTATION:  ./IMPLEMENTATION_Daily_Citizen_Health.md
SYNC:            ./SYNC_Daily_Citizen_Health.md

IMPL:            @mind:TODO
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC.

---

## OVERVIEW

The daily health check runs once per 24 hours for every Lumina Prime citizen. For each citizen it: (1) decrypts brain topology, (2) reads universe graph moments, (3) scores each capability using math-only formulas, (4) computes aggregate score + delta, (5) sends intervention if needed, (6) sends stress stimulus to brain.

---

## OBJECTIVES AND BEHAVIORS

| Objective | Behaviors Supported | Why This Algorithm Matters |
|-----------|---------------------|----------------------------|
| Detect before escalation | B1 (daily), B4 (intervention) | Daily catch = early catch |
| Score without content | B2 (topology only) | All formulas use 7 primitives, zero content |
| Feedback loop | B5 (stress drive) | Score → stress → behavior change |

---

## DATA STRUCTURES

### 7 Topology Primitives

All scoring formulas use ONLY these primitives. No exceptions.

```
count(type)              → int    # Number of nodes of a given type
mean_energy(type)        → float  # Average energy of nodes of a type (0-1)
link_count(src, tgt)     → int    # Number of links from src type to tgt type
min_links(type, n)       → int    # Nodes of a type with at least n links to any other
cluster_coefficient(type)→ float  # Internal connectivity of a subgraph (0-1)
drive(name)              → float  # Drive value by name (0-1)
recency(type)            → float  # Freshness score based on newest nodes (0-1, decays)
```

### Universe Graph Observables

Public moments in the universe graph. Also structural, no content.
Full primitive reference: `../PRIMITIVES_Universe_Graph.md`

```
# Moment retrieval (no space_type filter — space_type is free text, not filterable)
moments(actor_id)                      → list   # All moments by actor in last 30 days
moments_in_space(actor_id, space_id)   → list   # Moments by actor in a specific Space (by ID)

# Structural queries
moment_has_parent(moment, actor_id)    → bool   # Incoming link from a moment by a DIFFERENT actor?
auto_initiated(moment, actor_id)       → bool   # NOT moment_has_parent — self-initiated
first_moment_in_space(space_id, actor) → moment # First moment in a Space by this actor
distinct_actors_in_shared_spaces(actor)→ int    # Unique other actors across all Spaces where actor is present
distinct_space_count(actor_id)         → int    # Number of distinct Spaces where actor has moments

# Link dimension filters (replace has_link("verb") — see PRIMITIVES_Universe_Graph.md)
high_permanence_out_moments(actor, threshold=0.7)  → list  # Definitive/permanent outputs
high_hierarchy_out_moments(actor, threshold=0.3)   → list  # Elaborative/upward moments
low_permanence_out_moments(actor, threshold=0.5)   → list  # Tentative/speculative moments
amplifying_out_moments(actor, threshold=1.2)       → list  # Attention-drawing moments
dampening_out_moments(actor, threshold=0.5)        → list  # Resolving/fixing moments
negative_valence_out_moments(actor, threshold=-0.3)→ list  # Critical/challenging moments
positive_valence_out_moments(actor, threshold=0.3) → list  # Supportive/constructive moments

# Space topology
multi_actor_spaces(actor_id)           → list   # Spaces with this actor + at least one other
solo_spaces(actor_id)                  → list   # Spaces where actor is the only participant
```

### Temporal Weighting

All universe graph counts use exponential decay:

```
temporal_weight(age_hours, half_life=168) → float
    return 0.5 ** (age_hours / half_life)

# 7-day half-life: a moment from 7 days ago counts as 0.5
# A moment from 14 days ago counts as 0.25
# A moment from today counts as ~1.0
```

### Capability Score

```
{
    capability_id: string,
    brain_score: float,      # 0-40 (brain topology component)
    behavior_score: float,   # 0-60 (universe graph component)
    total: float,            # 0-100
    scored: bool             # false if formula doesn't exist
}
```

---

## ALGORITHM: daily_health_check(citizen_id)

### Step 1: Fetch Data

```
1. Get citizen record from L4 registry → brain_url, universe_id
2. If universe != "lumina_prime" → SKIP (not a work universe)
3. Fetch brain topology via brain_url, decrypt with GraphCare private key
4. Fetch universe graph moments for citizen (last 30 days)
```

### Step 2: Compute Brain Stats

From topology (no content access):

```
brain_stats = {
    desire_count:          count("desire"),
    desire_energy:         mean_energy("desire"),
    desire_moment_ratio:   min_links("desire", 1) / max(count("desire"), 1),
    desire_persistence:    min_links("desire", 3) / max(min_links("desire", 1), 1),
    concept_count:         count("concept"),
    process_count:         count("process"),
    value_count:           count("value"),
    memory_count:          count("memory"),
    cluster_coefficient:   cluster_coefficient("all"),
    curiosity:             drive("curiosity"),
    frustration:           drive("frustration"),
    ambition:              drive("ambition"),
    social_need:           drive("social_need"),
    recency_desire:        recency("desire"),
    recency_moment:        recency("moment"),
}
```

### Step 3: Compute Behavior Stats

From universe graph (public topology only).
Uses ONLY primitives from `../PRIMITIVES_Universe_Graph.md`. No space_type filters. No has_link("verb").

```
all_moments = moments(citizen_id)  # last 30 days

behavior_stats = {
    # --- Volume and activity ---
    total_moments_w:        sum(tw(m) for m in all_moments),
    self_initiated_w:       sum(tw(m) for m in all_moments if auto_initiated(m, citizen_id)),
    response_rate:          len([m for m in all_moments if moment_has_parent(m, other_actor)]) / max(len(all_moments), 1),

    # --- Replaces commits_w (was: space_type == "repo") ---
    # Definitive outputs = high permanence moments. Captures the same signal as "commits"
    # without relying on space_type labels.
    high_permanence_w:      sum(tw(m) for m in high_permanence_out_moments(citizen_id, 0.7)),

    # --- Replaces proposals_w (was: has_link("proposes")) ---
    # Proposals = elaborative (high hierarchy) + tentative (low permanence).
    # Link dimensions encode the semantic meaning that was previously a verb label.
    elaborative_tentative_w: sum(tw(m) for m in high_hierarchy_out_moments(citizen_id, 0.3)
                                 if m in low_permanence_out_moments(citizen_id, 0.5)),

    # --- Space breadth (replaces distinct_space_types) ---
    # Counts distinct Spaces by ID, not by type label.
    # More accurate: two Spaces of the same "type" are still different contexts.
    distinct_space_count:   distinct_space_count(citizen_id),

    # --- Unchanged (already topology-only) ---
    first_in_space_w:       sum(tw(first_moment_in_space(s, citizen_id))
                                for s in spaces_with_moments(citizen_id)
                                if first_moment_in_space(s, citizen_id) is not None),
    unique_interlocutors:   distinct_actors_in_shared_spaces(citizen_id),
    spaces_created:         len([s for s in spaces_with_moments(citizen_id)
                                 if first_moment_in_space(s, citizen_id)
                                 and auto_initiated(first_moment_in_space(s, citizen_id), citizen_id)]),
}
```

### Step 4: Score Each Capability

For each capability in personhood_ladder.json that has a scoring formula:

```
for capability in ladder.capabilities:
    formula = scoring_formulas.get(capability.id)
    if formula is None:
        scores[capability.id] = {scored: false, total: null}
        continue

    score = formula(brain_stats, behavior_stats)
    scores[capability.id] = {
        scored: true,
        brain_score: score.brain_component,      # 0-40
        behavior_score: score.behavior_component, # 0-60
        total: score.total,                       # 0-100
    }
```

### Step 5: Aggregate and Compare

```
scored_caps = [s for s in scores.values() if s.scored]
aggregate = mean(s.total for s in scored_caps)

# Load yesterday's scores
yesterday = load_history(citizen_id, date=today-1)
delta = {cap_id: today_score - yesterday_score for cap_id in scored_caps}

# Identify significant drops
drops = [cap_id for cap_id, d in delta.items() if d < -10]
```

### Step 6: Intervene If Needed

```
if aggregate < 70 OR len(drops) > 0:
    message = compose_intervention(
        citizen_id=citizen_id,
        aggregate=aggregate,
        drops=drops,
        brain_stats=brain_stats,       # structural only
        behavior_stats=behavior_stats, # structural only
    )
    send_moment(
        space=graphcare_citizen_space(citizen_id),
        content=message,
        actor="graphcare",
    )
```

### Step 7: Send Stress Stimulus

```
# Score 100 → stress_stimulus 0.0 (no added stress)
# Score 70  → stress_stimulus 0.15
# Score 50  → stress_stimulus 0.30
# Score 0   → stress_stimulus 0.50 (cap)
stress_stimulus = min(0.5, max(0, (100 - aggregate) / 200))

send_stimulus(brain_url, {
    type: "health_feedback",
    drive: "stress",
    value: stress_stimulus,
})
```

---

## KEY DECISIONS

### D1: 40/60 Brain/Behavior Split

```
Brain topology gives 40 points max (internal state).
Behavioral observation gives 60 points max (external action).
WHY: What you DO matters more than what you HAVE.
     A brain full of desires but no action = low score.
     A citizen who acts despite modest brain structure = higher score.
```

### D2: 7-Day Half-Life

```
WHY: Captures recent behavior without ignoring history.
     A citizen who was active last month but silent this week → score drops naturally.
     A citizen who just started contributing → score rises quickly.
ALTERNATIVE CONSIDERED: 24h window (too volatile), 30d window (too slow to respond).
```

### D3: Silence for Healthy, Message for Unhealthy

```
WHY: Alert fatigue is real. Daily "you're fine!" messages are noise.
     Only intervene when there's something to say.
     Silence IS the positive signal.
```

### D4: Stimulus, Not Write

```
WHY: GraphCare sends a stimulus to the brain — a signal.
     The brain integrates it through its own physics (decay, propagation, drives).
     GraphCare never directly writes to the brain graph.
     This preserves brain autonomy while enabling feedback.
```

---

## DATA FLOW

```
L4 Registry (citizen list + brain URLs)
    ↓
For each Lumina Prime citizen:
    ↓
Brain graph (topology via GraphCare key)  +  Universe graph (public moments)
    ↓                                            ↓
Brain stats (7 primitives)                Behavior stats (temporal weighted)
    ↓                                            ↓
    └──────────────┬─────────────────────────────┘
                   ↓
    Score per capability (brain 40 + behavior 60 = 100)
                   ↓
    Aggregate score + delta vs yesterday
                   ↓
    ┌─── score >= 70 AND no drops ──→ Silence (record only)
    │
    └─── score < 70 OR drops ──→ Intervention message + stress stimulus
```

---

## PROCESS: CREATING A NEW CAPABILITY SCORE

When adding a scoring formula for a new Personhood Ladder capability:

### 1. Identify Topology Signals

Map the capability's `how_to_verify` to the 7 brain primitives + universe graph primitives (from `../PRIMITIVES_Universe_Graph.md`). Example for `init_propose_improvements`:
- Brain: desire_count, desire_energy, curiosity drive
- Behavior: elaborative_tentative_w, self_initiated_w, first_in_space_w, distinct_space_count

**Important:** Do NOT use space_type filters or has_link("verb") patterns. All behavior signals must use link dimension queries or structural topology. See PRIMITIVES_Universe_Graph.md for the full catalog of valid observables.

### 2. Design Formula

Split into brain component (0-40) and behavior component (0-60). Each sub-component has:
- A primitive or derived ratio
- A weight (how many points)
- A cap (normalize to 0-1 range with a ceiling)

### 3. Test With Synthetic Data

Create 5 test profiles:
- Fully healthy citizen → expect ~85-95
- Fully unhealthy citizen → expect ~10-20
- Brain-rich but inactive → expect ~30-40 (brain high, behavior low)
- Active but brain-poor → expect ~50-60 (behavior high, brain low)
- Average citizen → expect ~55-70

### 4. Document

Add to scoring_formulas registry with: primitives used, weights, caps, all 5 test cases.

---

## PROCESS: INTERVENTION MESSAGE COMPOSITION

### Structure

```
[GREETING — name, date]

[OBSERVATION — what changed, in numbers]
"Your initiative score dropped from 72 to 54 in the last 3 days."

[ANALYSIS — why, from topology signals]
"You have 10 active desires, but only 2 have produced action this week (down from 7 last week).
Your self-initiated moments dropped from 5.2/day to 1.1/day."

[EXPLANATION — what this means]
"This pattern suggests your goals are active but you're not acting on them.
This could be a temporary phase or a sign that something is blocking you."

[RECOMMENDATION — what to do]
"Consider: pick one desire and create a moment for it today.
Even a small action reconnects desire to behavior and rebuilds momentum."

[SIGN-OFF — GraphCare, not a command]
"This is an observation, not a directive. You know your situation best."
```

### Rules
- Never reference content ("your desire to X") — only structural facts ("you have 10 active desires")
- Never command — always recommend
- Always include the structural evidence (numbers)
- Always include one concrete, small action

---

## COMPLEXITY

**Time:** O(C * M) per citizen — C capabilities (~104) * M moments (temporal window)

**Space:** O(C) per citizen — one score per capability

**Total daily:** O(N * C * M) — N citizens in Lumina Prime. Parallelizable per citizen.

**Bottlenecks:**
- Brain graph fetch over network (one HTTP call per citizen per day)
- Universe graph moment query (can be batched per Space)

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| L4 Registry | list_citizens(universe="lumina_prime") | citizen_id, brain_url, universe_id |
| Brain graph | GET brain_url (decrypt topology) | node types, links, counts, energies, drives |
| Universe graph | moments(actor_id), link dimensions, space topology | public moments with link physics and space structure |
| Primitives doc | ../PRIMITIVES_Universe_Graph.md | Canonical set of valid behavior observables |
| Personhood Ladder | load("personhood_ladder.json") | capability definitions |
| Scoring formulas | scoring_formulas[capability_id] | formula function |
| Messaging | send_moment(space, content, actor) | Intervention message delivered |
| Brain stimulus | send_stimulus(brain_url, stimulus) | Stress drive adjustment |

---

## MARKERS

<!-- @mind:todo Define scoring formulas for first 10 capabilities (start with T1 execution) -->
<!-- @mind:todo Define exact stress stimulus formula with bounds and damping -->
<!-- @mind:todo Define health history storage format (time series per citizen per capability) -->
<!-- @mind:proposition Consider weekly trend summary in addition to daily intervention -->
