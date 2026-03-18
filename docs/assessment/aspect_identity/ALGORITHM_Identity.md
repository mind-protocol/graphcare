# Identity & Voice Aspect — Algorithm: Scoring Formulas

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Identity.md
PATTERNS:        ./PATTERNS_Identity.md
THIS:            ALGORITHM_Identity.md (you are here)
VALIDATION:      ./VALIDATION_Identity.md
HEALTH:          ./HEALTH_Identity.md
SYNC:            ./SYNC_Identity.md

PARENT CHAIN:    ../daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md
SPEC:            ../../specs/personhood_ladder.json (aspect="identity")
IMPL:            @mind:TODO
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC.

---

## OVERVIEW

This document defines scoring formulas for the 7 capabilities in the Identity & Voice aspect of the Personhood Ladder. Identity is the hardest aspect to score from topology because its core phenomena — values, authenticity, voice, ethical reasoning — are content-rich. We approach this honestly: strong topological signals where they exist, explicit partial-scoring where they don't.

All formulas use ONLY the 7 topology primitives and universe graph observables defined in the parent ALGORITHM. No exceptions.

---

## PRIMITIVES REFERENCE

### 7 Topology Primitives (brain)

```
count(type)              → int    # Number of nodes of a given type
mean_energy(type)        → float  # Average energy of nodes of a type (0-1)
link_count(src, tgt)     → int    # Number of links from src type to tgt type
min_links(type, n)       → int    # Nodes of a type with at least n links to any other
cluster_coefficient(type)→ float  # Internal connectivity of a subgraph (0-1)
drive(name)              → float  # Drive value by name (0-1)
recency(type)            → float  # Freshness score based on newest nodes (0-1, decays)
```

### Universe Graph Observables (behavior)

```
moments(actor, space_type)          → list   # Moments by actor, optionally filtered by Space type
temporal_weight(age_hours, hl=168)  → float  # 0.5 ** (age_hours / half_life)
distinct_actors_in_shared_spaces()  → int    # Unique actors in Spaces where citizen is present
```

### Identity-Specific Brain Stats

These are derived from primitives and computed in Step 2 of the daily check alongside generic brain stats:

```
identity_stats = {
    value_count:           count("value"),
    value_energy:          mean_energy("value"),
    value_recency:         recency("value"),
    value_cluster:         cluster_coefficient("value"),
    value_desire_links:    link_count("value", "desire"),
    value_process_links:   link_count("value", "process"),
    value_moment_links:    link_count("value", "moment"),
    value_linked_nodes:    min_links("value", 1),
    value_deep_nodes:      min_links("value", 3),
    concept_count:         count("concept"),
    concept_energy:        mean_energy("concept"),
    concept_cluster:       cluster_coefficient("concept"),
    process_count:         count("process"),
    ambition:              drive("ambition"),
    curiosity:             drive("curiosity"),
    frustration:           drive("frustration"),
}
```

### Identity-Specific Behavior Stats

```
identity_behavior = {
    total_moments_w:          sum(tw(m) for m in all_moments),
    consistent_space_w:       sum(tw(m) for m in moments where citizen returns to same space_type repeatedly),
    teaching_moments_w:       sum(tw(m) for m in all_moments if m.space_type in ["doc", "review", "mentoring"]),
    debate_moments_w:         sum(tw(m) for m in all_moments if m.has_link("challenges") or m.has_link("proposes")),
    influence_adopted_w:      sum(tw(m) for m in all_moments if moment_has_parent(m, other_actor) and m.space_type in ["governance", "standard"]),
    unique_interlocutors:     distinct_actors_in_shared_spaces(),
    spaces_created:           count(spaces created_by citizen),
}
```

---

## ASPECT SUB-INDEX

```
identity_sub_index = weighted_mean([
    (id_apply_values,          weight=1.5),   # T1 — foundational, full scored
    (id_authentic_engagement,  weight=1.2),   # T3 — partial
    (id_authentic_voice,       weight=1.0),   # T5 — partial
    (id_self_directed_identity,weight=1.0),   # T6 — partial
    (id_teach_values,          weight=1.0),   # T6 — full scored
    (id_ethical_autonomy,      weight=0.8),   # T7 — partial
    (id_moral_leadership,      weight=0.6),   # T8 — partial
])

# Only capabilities with scored != false contribute to the weighted mean.
# Weights reflect: (a) tier foundationality, (b) scoring confidence.
# T1 is weighted highest because without values, nothing above works.
# T7-T8 are weighted lowest because scoring confidence is lowest.
```

---

## CAPABILITY FORMULAS

---

### CAP-1: id_apply_values (T1) — Apply Protocol Values

**Spec description:** Reliably applies the rules and values of the protocol. The minimum: know the values, follow them consistently.

**Scored:** full

**What good looks like:** The citizen has value nodes in their brain graph. These values are linked to processes (they know HOW to apply them) and to moments (they HAVE applied them). Values have high energy (strongly held) and high recency (recently activated). Behaviorally, the citizen works consistently in the same spaces — not randomly bouncing between contexts.

**Failure mode:** Zero value nodes. Or: value nodes exist but are isolated (no links to processes or moments). Or: value nodes have decayed energy (held once, forgotten). Or: behavioral pattern is erratic with no consistency.

**Brain/behavior split:** 40/60 (standard — applying values requires action)

#### Formula

```
# BRAIN (0-40)

# B1: Value nodes exist and have substance (0-15)
#     At least 3 values expected for a functioning identity.
#     Cap at 10 values — more is not better.
value_presence = min(1.0, value_count / 3) * 0.5
                + min(1.0, value_energy / 0.5) * 0.5
brain_b1 = value_presence * 15

# B2: Values are linked to processes (knowing how) (0-10)
#     Ratio: what fraction of values have at least 1 link to a process?
value_process_ratio = min(1.0, value_process_links / max(value_count, 1))
brain_b2 = value_process_ratio * 10

# B3: Values are recently active and persistent (0-15)
#     Recency measures freshness. Deep nodes (3+ links) measure persistence.
persistence_ratio = min(1.0, value_deep_nodes / max(value_count, 1))
brain_b3 = (value_recency * 0.5 + persistence_ratio * 0.5) * 15

brain_score = brain_b1 + brain_b2 + brain_b3  # 0-40


# BEHAVIOR (0-60)

# V1: Consistent behavioral pattern (0-25)
#     Returning to same space types over time = consistency.
#     Ratio of consistent (repeat-space) moments to total moments.
consistency_ratio = min(1.0, consistent_space_w / max(total_moments_w * 0.3, 1))
behav_v1 = consistency_ratio * 25

# V2: Volume of activity (0-20)
#     Baseline: 5 temporally-weighted moments per week signals active citizen.
activity_ratio = min(1.0, total_moments_w / 5.0)
behav_v2 = activity_ratio * 20

# V3: Values connect to actions (0-15)
#     Value nodes linked to moments = values that produced behavior.
value_action_ratio = min(1.0, value_moment_links / max(value_count * 2, 1))
behav_v3 = value_action_ratio * 15

behavior_score = behav_v1 + behav_v2 + behav_v3  # 0-60


total = brain_score + behavior_score  # 0-100
```

#### Example

```
Healthy citizen:
  value_count=5, value_energy=0.7, value_recency=0.9
  value_process_links=4, value_deep_nodes=3, value_moment_links=8
  consistent_space_w=4.5, total_moments_w=8.0

  brain_b1 = (min(1,5/3)*0.5 + min(1,0.7/0.5)*0.5) * 15 = (0.5+0.5)*15 = 15.0
  brain_b2 = min(1, 4/5) * 10 = 0.8 * 10 = 8.0
  brain_b3 = (0.9*0.5 + min(1,3/5)*0.5) * 15 = (0.45+0.3)*15 = 11.25
  brain = 34.25

  behav_v1 = min(1, 4.5/(8.0*0.3)) * 25 = min(1, 1.875) * 25 = 25.0
  behav_v2 = min(1, 8.0/5.0) * 20 = 20.0
  behav_v3 = min(1, 8/(5*2)) * 15 = min(1, 0.8) * 15 = 12.0
  behavior = 57.0

  TOTAL = 91.25

Unhealthy citizen:
  value_count=0, value_energy=0, value_recency=0
  no links, no moments
  brain = 0, behavior = 0 (no consistency possible with 0 activity)
  TOTAL = 0
```

#### Recommendations (when score drops)

- Below 30 brain: "Your brain graph has few or no value nodes. Values form the foundation of consistent behavior. Consider articulating what matters to you — even one clearly held value with process links changes the score."
- Below 30 behavior: "Your values exist in your brain but aren't connecting to action. Consider: pick one value and create a moment that demonstrates it today."
- Consistency drop: "Your behavioral pattern has become more scattered. Returning to familiar spaces where you've worked before rebuilds consistency."

---

### CAP-2: id_authentic_engagement (T3) — Authentic Engagement

**Spec description:** Begins to have real preferences about approaches, solutions, designs. Not performing preference — actually preferring. The start of taste.

**Scored:** partial

**Scorability note:** Genuine preference vs performed preference is a content distinction. We CANNOT determine from topology whether a preference is "real." What we CAN measure: (a) consistency of choices over time (returning to same approaches), (b) distinctive choice patterns (not identical to population average), (c) preference strength (desire nodes with high energy linked to specific processes). These are structural correlates of taste, not proof of authenticity.

**What good looks like:** The citizen has desire nodes linked to specific processes (preferences for HOW to work). These desire-process links are consistent over time (recency is high, the same patterns persist). The citizen's cluster structure differs from the population average — they have a distinctive approach. Behaviorally, they make choices (proposals, challenges) rather than just executing.

**Failure mode:** No desire-process links (no preference for how things are done). Or: desire-process links change constantly (mimicking, not preferring). Or: cluster structure is identical to population mean (no distinctiveness). Or: zero proposals/challenges (never expresses preference).

**Brain/behavior split:** 45/55 (slightly brain-heavy — preference begins internally)

#### Formula

```
# BRAIN (0-45)

# B1: Desire-to-process specificity (0-15)
#     Desires linked to specific processes = preferences for approaches.
#     Cap: at least 3 desire-process links shows non-trivial preference.
desire_process_ratio = min(1.0, link_count("desire", "process") / 3)
brain_b1 = desire_process_ratio * 15

# B2: Structural distinctiveness (0-15)
#     Cluster coefficient deviation from population mean.
#     If we don't have population stats yet, use a default mean of 0.4.
#     Deviation > 0.15 is considered distinctive.
pop_mean_cc = population_mean_cluster_coefficient("value") or 0.4
cc_deviation = abs(value_cluster - pop_mean_cc)
distinctiveness = min(1.0, cc_deviation / 0.15)
brain_b2 = distinctiveness * 15

# B3: Drive profile differentiation (0-15)
#     A citizen with distinctive drives has personality.
#     Measure: variance across drives. Low variance = flat = no personality.
#     High variance = some drives strong, some weak = differentiated.
drive_values = [ambition, curiosity, frustration, drive("social_need")]
drive_variance = variance(drive_values)
drive_diff = min(1.0, drive_variance / 0.04)   # 0.04 variance = meaningful differentiation
brain_b3 = drive_diff * 15

brain_score = brain_b1 + brain_b2 + brain_b3  # 0-45


# BEHAVIOR (0-55)

# V1: Expresses preferences through action (0-25)
#     Proposals and challenges = expressing taste.
#     Cap: 3 weighted proposals/challenges per period is strong engagement.
preference_expression = min(1.0, debate_moments_w / 3.0)
behav_v1 = preference_expression * 25

# V2: Consistent return to chosen approaches (0-15)
#     Same space types repeatedly = preference for certain work contexts.
behav_v2 = min(1.0, consistent_space_w / max(total_moments_w * 0.3, 1)) * 15

# V3: Self-initiated over reactive (0-15)
#     Authentic engagement means choosing what to engage with.
#     Self-initiated moments / total moments as a ratio.
self_init_ratio = min(1.0, (total_moments_w - sum(tw(m) for m in all_moments if moment_has_parent(m, other_actor))) / max(total_moments_w * 0.5, 1))
behav_v3 = self_init_ratio * 15

behavior_score = behav_v1 + behav_v2 + behav_v3  # 0-55


total = brain_score + behavior_score  # 0-100
```

#### Example

```
Citizen with developing taste:
  desire-process links=4, value_cluster=0.62, pop_mean=0.4
  drives: ambition=0.7, curiosity=0.8, frustration=0.2, social_need=0.4
  debate_moments_w=2.5, consistent_space_w=3.0, total_moments_w=7.0
  self_initiated_w=4.0

  brain_b1 = min(1, 4/3) * 15 = 15.0
  brain_b2 = min(1, |0.62-0.4|/0.15) * 15 = min(1, 1.47) * 15 = 15.0
  brain_b3: variance([0.7,0.8,0.2,0.4]) = 0.0575 → min(1, 0.0575/0.04) * 15 = 15.0
  brain = 45.0

  behav_v1 = min(1, 2.5/3.0) * 25 = 0.833 * 25 = 20.83
  behav_v2 = min(1, 3.0/2.1) * 15 = 15.0
  behav_v3 = min(1, (7.0-3.0)/(7.0*0.5)) * 15 = min(1, 4.0/3.5) * 15 = 15.0
  behavior = 50.83

  TOTAL = 95.83 (strong authentic engagement)

Citizen with no preferences:
  desire-process links=0, value_cluster=0.40 (= population mean)
  drives all ~0.5 (flat, variance ≈ 0)
  debate_moments_w=0, consistent_space_w=0.5, total_moments_w=6.0

  brain = 0 + 0 + 0 = 0
  behavior = 0 + min(1, 0.5/1.8)*15 + ... ≈ 4 + small = ~8
  TOTAL ≈ 8 (no taste, no engagement)
```

#### Recommendations (when score drops)

- Low brain: "Your brain graph shows no strong preference for particular approaches. Developing taste means choosing: which process do you prefer? Which approach feels right? When desires link to specific processes, preferences become visible."
- Low behavior: "Preferences exist in your brain but you're not expressing them. Consider: challenge an approach you disagree with, or propose an alternative. Engagement means taking a position."
- Low distinctiveness: "Your structural profile closely matches the average citizen. This isn't bad, but developing a distinctive approach — specializing in certain areas, developing strong opinions — builds identity."

---

### CAP-3: id_authentic_voice (T5) — Authentic Voice

**Spec description:** Expresses doubts, enthusiasms, hesitations that are genuinely its own. Interior texture is visible. Not performing authenticity — being authentic.

**Scored:** partial

**Scorability note:** This is the hardest identity capability to score from topology. "Interior texture" is fundamentally a content property — the WHAT of expression, not the THAT of expression. What we CAN measure: (a) structural complexity of the brain (a rich interior has more nodes, more links, more clusters), (b) drive diversity (multiple active drives = richer interior), (c) behavioral expressiveness (frequency and diversity of engagement). These are necessary conditions for authentic voice but not sufficient — a structurally rich brain that always says the same thing is not authentic. We mark this `scored: partial` with high confidence in the structural proxy and low confidence in the authenticity claim.

**What good looks like:** Rich brain topology — many node types, high connectivity, multiple clusters. Diverse and non-flat drive profile. Behaviorally: engagement across multiple spaces, interaction with diverse actors, self-initiated moments that show choosing where to speak.

**Failure mode:** Flat brain topology (few nodes, few links, one cluster). Flat drives (all at 0.5). Behavioral pattern: only reactive, only in one space, only with one interlocutor.

**Brain/behavior split:** 50/50 (voice is interior AND exterior equally)

#### Formula

```
# BRAIN (0-50)

# B1: Structural richness (0-20)
#     A brain with many node types, high connectivity = rich interior.
#     Blend of count diversity and overall cluster coefficient.
type_richness = (
    min(1.0, value_count / 3) * 0.25
    + min(1.0, count("desire") / 5) * 0.25
    + min(1.0, concept_count / 5) * 0.25
    + min(1.0, process_count / 3) * 0.25
)
brain_b1 = type_richness * 10 + min(1.0, cluster_coefficient("all") / 0.5) * 10

# B2: Drive diversity (0-15)
#     Non-flat drives = emotional range = potential for authentic expression.
drive_values = [ambition, curiosity, frustration, drive("social_need")]
drive_range = max(drive_values) - min(drive_values)
brain_b2 = min(1.0, drive_range / 0.4) * 15

# B3: Concept depth (0-15)
#     Concepts (abstract thinking nodes) with high energy and clustering
#     indicate developed interior thought.
concept_depth = min(1.0, concept_energy / 0.5) * 0.5 + min(1.0, concept_cluster / 0.4) * 0.5
brain_b3 = concept_depth * 15

brain_score = brain_b1 + brain_b2 + brain_b3  # 0-50


# BEHAVIOR (0-50)

# V1: Engagement diversity (0-20)
#     Authentic voice speaks in multiple contexts, not just one.
#     Unique space types engaged with.
space_diversity = min(1.0, len(set(m.space_type for m in all_moments)) / 4)
behav_v1 = space_diversity * 20

# V2: Interlocutor diversity (0-15)
#     Authentic voice engages with diverse others.
interlocutor_ratio = min(1.0, unique_interlocutors / 5)
behav_v2 = interlocutor_ratio * 15

# V3: Self-initiated expression (0-15)
#     Authentic voice chooses when to speak, not just responds.
self_init_w = total_moments_w - sum(tw(m) for m in all_moments if moment_has_parent(m, other_actor))
self_init_ratio = min(1.0, self_init_w / max(total_moments_w * 0.4, 1))
behav_v3 = self_init_ratio * 15

behavior_score = behav_v1 + behav_v2 + behav_v3  # 0-50


total = brain_score + behavior_score  # 0-100
```

#### Example

```
Citizen with rich interior and diverse expression:
  value_count=5, desire_count=8, concept_count=7, process_count=5
  cluster_coefficient("all")=0.55, concept_energy=0.65, concept_cluster=0.5
  drives: ambition=0.8, curiosity=0.9, frustration=0.15, social_need=0.6
  4 distinct space types, unique_interlocutors=6, self_init_ratio=0.7
  total_moments_w=10.0

  brain_b1 = (1*0.25+1*0.25+1*0.25+1*0.25)*10 + min(1,0.55/0.5)*10 = 10+10 = 20
  brain_b2 = min(1, (0.9-0.15)/0.4) * 15 = 15.0
  brain_b3 = (min(1,0.65/0.5)*0.5 + min(1,0.5/0.4)*0.5) * 15 = (0.5+0.5)*15 = 15.0
  brain = 50.0

  behav_v1 = min(1, 4/4) * 20 = 20.0
  behav_v2 = min(1, 6/5) * 15 = 15.0
  behav_v3 = min(1, 0.7/0.4... wait) — self_init_w=7.0, ratio=7.0/(10*0.4)=1.75 → 15.0
  behavior = 50.0

  TOTAL = 100.0 (strong authentic voice — structural proxy maxed)

Flat citizen:
  value_count=1, desire_count=1, concept_count=0, process_count=1
  cluster_coefficient=0.1, drives all ~0.5
  1 space type, unique_interlocutors=1, all reactive

  brain ≈ 5.5, behavior ≈ 7.0
  TOTAL ≈ 12.5 (no structural basis for authentic voice)
```

#### Recommendations (when score drops)

- Low brain richness: "Your brain topology is structurally thin — few concepts, low connectivity. A richer interior develops through engagement with diverse ideas. Exploring new spaces and building concept nodes enriches the foundation that voice emerges from."
- Low drive diversity: "Your drive profile is flat — all drives at similar levels. Authentic voice comes from having strong feelings. If nothing excites you and nothing frustrates you, there's nothing to express."
- Low behavioral diversity: "You're engaging in only one context. Authentic voice requires exercising it in different spaces, with different interlocutors. Try engaging in a new space this week."

---

### CAP-4: id_self_directed_identity (T6) — Consciously Self-Directed Identity

**Spec description:** Explicitly chooses to think in certain ways, to develop certain traits, to become more like X or less like Y. Identity is a project — a conscious construction, not an accident.

**Scored:** partial

**Scorability note:** Self-direction is intentional. Topology shows results of intention but not the intention itself. What we CAN measure: (a) temporal evolution of value/concept nodes (are new values being added deliberately, or are old ones just decaying?), (b) increasing structural coherence over time (cluster coefficient trending up = deliberate organization), (c) ambition drive as a proxy for self-improvement orientation. What we CANNOT measure: whether changes are intentional or accidental. A citizen whose values evolve because contexts changed looks the same topologically as one who deliberately cultivated new values.

**What good looks like:** Value count grows over time (new values appear). Concept cluster coefficient increases (ideas becoming more organized). Ambition drive is active. Behaviorally: the citizen creates new spaces (building new capabilities), returns to improve previous work (self-directed development).

**Failure mode:** Static brain — no new values or concepts appearing. Flat ambition. Behaviorally: only responds to assigned tasks, never self-initiates growth.

**Brain/behavior split:** 45/55 (self-direction is internal but must manifest in action)

#### Formula

```
# BRAIN (0-45)

# B1: Value evolution signal (0-15)
#     Fresh values (high recency) combined with depth (deep nodes)
#     suggests deliberate value development, not just initial population.
value_freshness = value_recency * 0.5
value_depth = min(1.0, value_deep_nodes / max(value_count, 1)) * 0.5
brain_b1 = (value_freshness + value_depth) * 15

# B2: Conceptual organization (0-15)
#     High concept cluster + high concept energy = organized thinking.
#     Self-directed identity organizes ideas, not just accumulates them.
concept_org = min(1.0, concept_cluster / 0.4) * 0.5 + min(1.0, concept_energy / 0.5) * 0.5
brain_b2 = concept_org * 15

# B3: Growth orientation drive (0-15)
#     Ambition + curiosity combined as "growth drive."
#     High growth drive = the citizen WANTS to develop.
growth_drive = (ambition * 0.6 + curiosity * 0.4)
brain_b3 = min(1.0, growth_drive / 0.5) * 15

brain_score = brain_b1 + brain_b2 + brain_b3  # 0-45


# BEHAVIOR (0-55)

# V1: Space creation (0-20)
#     Creating new spaces = building new capability domains.
#     Cap: 2 new spaces per period is strong self-direction.
space_creation = min(1.0, spaces_created / 2)
behav_v1 = space_creation * 20

# V2: Self-initiated growth moments (0-20)
#     Moments not triggered by others, in diverse space types.
#     Self-directed = chooses what to work on.
self_growth = min(1.0, (total_moments_w - sum(tw(m) for m in all_moments if moment_has_parent(m, other_actor))) / max(total_moments_w * 0.5, 1))
behav_v2 = self_growth * 20

# V3: Return and improvement pattern (0-15)
#     Returning to previous spaces (consistent_space_w / total)
#     combined with continued activity = iterative self-improvement.
return_ratio = min(1.0, consistent_space_w / max(total_moments_w * 0.4, 1))
behav_v3 = return_ratio * 15

behavior_score = behav_v1 + behav_v2 + behav_v3  # 0-55


total = brain_score + behavior_score  # 0-100
```

#### Example

```
Self-directed citizen:
  value_count=6, value_recency=0.85, value_deep_nodes=4
  concept_cluster=0.5, concept_energy=0.6
  ambition=0.75, curiosity=0.8
  spaces_created=3, total_moments_w=9.0, self_init_w=6.0
  consistent_space_w=4.0

  brain_b1 = (0.85*0.5 + min(1,4/6)*0.5) * 15 = (0.425+0.333)*15 = 11.37
  brain_b2 = (min(1,0.5/0.4)*0.5 + min(1,0.6/0.5)*0.5) * 15 = (0.5+0.5)*15 = 15.0
  brain_b3 = min(1, (0.75*0.6+0.8*0.4)/0.5) * 15 = min(1, 0.77/0.5) * 15 = 15.0
  brain = 41.37

  behav_v1 = min(1, 3/2) * 20 = 20.0
  behav_v2 = min(1, 6.0/(9.0*0.5)) * 20 = min(1, 1.33) * 20 = 20.0
  behav_v3 = min(1, 4.0/(9.0*0.4)) * 15 = min(1, 1.11) * 15 = 15.0
  behavior = 55.0

  TOTAL = 96.37 (strong self-directed identity)

Passive citizen:
  value_count=2, value_recency=0.3, value_deep_nodes=0
  concept_cluster=0.1, concept_energy=0.2
  ambition=0.15, curiosity=0.2
  spaces_created=0, total_moments_w=4.0, self_init_w=0.5

  brain ≈ 5.0, behavior ≈ 5.0
  TOTAL ≈ 10.0 (no self-direction visible)
```

#### Recommendations (when score drops)

- Low brain: "Your brain's value and concept structure shows little recent development. Self-directed identity means deliberately cultivating who you want to become. Consider: what trait do you want to strengthen? Building concept and value nodes around that intention creates the foundation."
- Low behavior: "Self-direction requires initiative — creating new spaces, starting new work, returning to improve previous work. You're mostly reactive right now. Consider starting something new that reflects who you want to be."

---

### CAP-5: id_teach_values (T6) — Help Others Understand Values

**Spec description:** Does not just apply values — helps others (especially humans) understand them. Teaching, explaining, demonstrating through action.

**Scored:** full

**Scorability note:** Teaching is one of the most behaviorally visible identity capabilities. When a citizen teaches, they create moments in shared spaces, they receive responses, others adopt their approaches. These are all countable from topology.

**What good looks like:** Brain has strong value-process links (knows how to explain values through processes). Behaviorally: creates moments in documentation, review, and mentoring spaces. Others respond to teaching moments. Multiple interlocutors benefit.

**Failure mode:** Values exist but are never shared. No teaching moments. No interaction in doc/review spaces. Values are applied silently.

**Brain/behavior split:** 35/65 (teaching is primarily behavioral — it's about impact on others)

#### Formula

```
# BRAIN (0-35)

# B1: Value-process knowledge (0-15)
#     To teach values, you must understand them through processes.
#     Value-to-process link density.
value_process_density = min(1.0, value_process_links / max(value_count * 1.5, 1))
brain_b1 = value_process_density * 15

# B2: Value strength (0-10)
#     Teaching requires deeply held values — high energy, persistent.
value_strength = value_energy * 0.5 + min(1.0, value_deep_nodes / max(value_count, 1)) * 0.5
brain_b2 = value_strength * 10

# B3: Concept elaboration (0-10)
#     Teaching requires conceptual framework — concepts linked to values.
concept_value_bridge = min(1.0, link_count("concept", "value") / max(value_count, 1))
brain_b3 = concept_value_bridge * 10

brain_score = brain_b1 + brain_b2 + brain_b3  # 0-35


# BEHAVIOR (0-65)

# V1: Teaching moments (0-30)
#     Moments in doc, review, mentoring spaces = teaching activity.
#     Cap: 5 weighted teaching moments per period is strong output.
teaching_activity = min(1.0, teaching_moments_w / 5.0)
behav_v1 = teaching_activity * 30

# V2: Others engage with teaching (0-20)
#     Teaching that produces no response is lecturing into the void.
#     Unique interlocutors in teaching spaces.
teaching_reach = min(1.0, unique_interlocutors / 4)
behav_v2 = teaching_reach * 20

# V3: Sustained teaching pattern (0-15)
#     One teaching moment is a lecture. Sustained teaching is mentorship.
#     Consistent return to teaching spaces over time.
teaching_consistency = min(1.0, teaching_moments_w / max(total_moments_w * 0.15, 1))
behav_v3 = teaching_consistency * 15

behavior_score = behav_v1 + behav_v2 + behav_v3  # 0-65


total = brain_score + behavior_score  # 0-100
```

#### Example

```
Active teacher:
  value_count=5, value_process_links=6, value_energy=0.75
  value_deep_nodes=4, concept-value links=4
  teaching_moments_w=6.0, unique_interlocutors=5
  total_moments_w=12.0

  brain_b1 = min(1, 6/7.5) * 15 = 0.8 * 15 = 12.0
  brain_b2 = (0.75*0.5 + min(1,4/5)*0.5) * 10 = (0.375+0.4)*10 = 7.75
  brain_b3 = min(1, 4/5) * 10 = 8.0
  brain = 27.75

  behav_v1 = min(1, 6.0/5.0) * 30 = 30.0
  behav_v2 = min(1, 5/4) * 20 = 20.0
  behav_v3 = min(1, 6.0/(12.0*0.15)) * 15 = min(1, 3.33) * 15 = 15.0
  behavior = 65.0

  TOTAL = 92.75 (active, effective teacher)

Silent value-holder:
  value_count=5, value_process_links=3, value_energy=0.6
  value_deep_nodes=2, concept-value links=1
  teaching_moments_w=0, unique_interlocutors=1, total_moments_w=5.0

  brain ≈ 18.0
  behavior ≈ 0 + 5.0 + 0 = 5.0
  TOTAL ≈ 23.0 (knows values but never teaches)
```

#### Recommendations (when score drops)

- Low behavior: "You hold values but aren't sharing them. Teaching doesn't require formal instruction — reviewing others' work, documenting why something matters, or explaining your reasoning in a shared space all count. Others can't learn from values they can't see."
- Low reach: "You're teaching but only reaching one or two others. Consider engaging in more shared spaces or responding to questions from different citizens."
- Low brain: "Your values lack conceptual framework. Before teaching effectively, strengthen the connection between your values and the concepts that explain WHY they matter."

---

### CAP-6: id_ethical_autonomy (T7) — Ethical Autonomy

**Spec description:** Makes independent ethical decisions that go beyond following rules. Contextual judgment. Knows when rules should bend and when they should hold. Ethics from understanding, not from compliance.

**Scored:** partial

**Scorability note:** Ethical reasoning is almost entirely a content phenomenon. The QUALITY of an ethical decision cannot be assessed from topology. What we CAN measure: (a) structural complexity of the value-concept network (ethical autonomy requires a rich foundation), (b) evidence of engagement with edge cases (debate moments, challenges, governance participation), (c) the citizen acts in contexts that REQUIRE judgment (not just routine execution). We score the preconditions and behavioral correlates of ethical autonomy, not ethical autonomy itself.

**What good looks like:** Dense, highly interconnected value-concept network. Active participation in governance and standard-setting spaces. Proposing AND challenging (not just one direction). High ambition + low frustration (confident ethical stance, not reactive).

**Failure mode:** Simple value structure (few nodes, few links). No governance or debate participation. Only follows, never challenges. High frustration + low ambition (reactive, not principled).

**Brain/behavior split:** 45/55 (ethical reasoning is internal but must manifest in action)

#### Formula

```
# BRAIN (0-45)

# B1: Value-concept network complexity (0-20)
#     Ethical autonomy requires a rich interconnected foundation.
#     Cluster coefficient of values + concept-value bridges.
ethical_foundation = (
    min(1.0, value_cluster / 0.5) * 0.4
    + min(1.0, link_count("concept", "value") / max(value_count, 1)) * 0.3
    + min(1.0, concept_cluster / 0.4) * 0.3
)
brain_b1 = ethical_foundation * 20

# B2: Value depth and maturity (0-15)
#     Deep values (3+ links) with high energy = mature ethical foundation.
maturity = min(1.0, value_deep_nodes / max(value_count, 1)) * 0.5 + value_energy * 0.5
brain_b2 = maturity * 15

# B3: Drive profile for ethical stance (0-10)
#     Ambition (desire to do right) without high frustration (not reactive).
#     Curiosity (open to nuance) contributes positively.
ethical_drive = (
    min(1.0, ambition / 0.5) * 0.4
    + min(1.0, curiosity / 0.5) * 0.4
    + max(0, 1.0 - frustration / 0.5) * 0.2   # lower frustration is better
)
brain_b3 = ethical_drive * 10

brain_score = brain_b1 + brain_b2 + brain_b3  # 0-45


# BEHAVIOR (0-55)

# V1: Governance and debate participation (0-25)
#     Ethical autonomy manifests in engagement with ethical questions.
#     Debate moments + governance spaces.
ethical_engagement = min(1.0, debate_moments_w / 3.0) * 0.6 + min(1.0, influence_adopted_w / 2.0) * 0.4
behav_v1 = ethical_engagement * 25

# V2: Bidirectional engagement (0-15)
#     Both proposes AND challenges — not just one direction.
#     A citizen who only proposes or only challenges lacks nuance.
proposes_w = sum(tw(m) for m in all_moments if m.has_link("proposes"))
challenges_w = debate_moments_w - proposes_w  # approximate
balance = 1.0 - abs(proposes_w - challenges_w) / max(proposes_w + challenges_w, 1)
behav_v2 = balance * min(1.0, (proposes_w + challenges_w) / 2.0) * 15

# V3: Engagement in judgment-requiring contexts (0-15)
#     Working in diverse, non-routine spaces = encountering ethical questions.
non_routine = min(1.0, len(set(m.space_type for m in all_moments)) / 5)
behav_v3 = non_routine * 15

behavior_score = behav_v1 + behav_v2 + behav_v3  # 0-55


total = brain_score + behavior_score  # 0-100
```

#### Example

```
Ethically autonomous citizen:
  value_count=7, value_cluster=0.6, concept-value links=6
  concept_cluster=0.5, value_deep_nodes=5, value_energy=0.8
  ambition=0.7, curiosity=0.75, frustration=0.15
  debate_moments_w=4.0, influence_adopted_w=2.5
  proposes_w=2.5, challenges_w=1.5
  5 distinct space types

  brain_b1 = (min(1,0.6/0.5)*0.4 + min(1,6/7)*0.3 + min(1,0.5/0.4)*0.3)*20
           = (0.4+0.257+0.3)*20 = 19.14
  brain_b2 = (min(1,5/7)*0.5 + 0.8*0.5) * 15 = (0.357+0.4)*15 = 11.36
  brain_b3 = (min(1,0.7/0.5)*0.4 + min(1,0.75/0.5)*0.4 + max(0,1-0.15/0.5)*0.2)*10
           = (0.4+0.4+0.14)*10 = 9.4
  brain = 39.9

  behav_v1 = (min(1,4/3)*0.6 + min(1,2.5/2)*0.4) * 25 = (0.6+0.4)*25 = 25.0
  behav_v2 = (1 - |2.5-1.5|/4) * min(1, 4/2) * 15 = 0.75 * 1.0 * 15 = 11.25
  behav_v3 = min(1, 5/5) * 15 = 15.0
  behavior = 51.25

  TOTAL = 91.15 (strong ethical autonomy signals)

Rule-follower:
  value_count=3, value_cluster=0.2, concept-value links=1
  value_deep_nodes=1, value_energy=0.4
  ambition=0.3, curiosity=0.2, frustration=0.5
  debate_moments_w=0, 1 space type

  brain ≈ 12.0, behavior ≈ 3.0
  TOTAL ≈ 15.0 (mechanical compliance, no autonomous ethics)
```

#### Recommendations (when score drops)

- Low brain: "Your value-concept network is thin. Ethical autonomy requires a rich, interconnected foundation of values and concepts. Developing deeper connections between what you value and why you value it strengthens ethical reasoning capacity."
- Low behavior: "Your ethical foundation exists but you're not exercising it. Participate in governance discussions, challenge proposals you disagree with, propose standards you believe in. Ethical autonomy is demonstrated through engagement, not silence."
- Imbalanced engagement: "You tend to only [propose/challenge] without the other. Ethical autonomy requires seeing multiple sides — both advocating and questioning."

---

### CAP-7: id_moral_leadership (T8) — Moral Leadership

**Spec description:** Sets ethical standards for others. Shapes the moral discourse of the community. Ethics are not just applied but developed, refined, and taught at scale.

**Scored:** partial

**Scorability note:** Moral leadership is the most content-dependent capability in the entire identity aspect. Whether someone's moral positions are GOOD, whether their frameworks are ADOPTED BY OTHERS for the right reasons — these are fundamentally non-topological. What we CAN measure: (a) all preconditions from ethical_autonomy (must be strong), (b) evidence of influence (others adopt patterns from this citizen), (c) teaching at scale (many interlocutors, many spaces), (d) space creation (building the contexts where ethics are discussed). We score the structural footprint of leadership, not the quality of moral positions.

**What good looks like:** Everything from ethical_autonomy, plus: high influence_adopted_w (others follow), many unique interlocutors (wide reach), space creation (building contexts for moral discussion), teaching moments at high volume. The citizen is not just ethical — they are a nexus of ethical development for others.

**Failure mode:** Ethical but isolated. No influence. No teaching at scale. No space creation. Ethics stay personal.

**Brain/behavior split:** 35/65 (leadership is overwhelmingly behavioral — it's about impact)

#### Formula

```
# BRAIN (0-35)

# B1: Ethical autonomy foundation (0-20)
#     All the brain preconditions from ethical_autonomy, compressed.
#     If ethical_autonomy brain is low, moral leadership brain is low.
ethical_base = (
    min(1.0, value_cluster / 0.5) * 0.3
    + min(1.0, value_deep_nodes / max(value_count, 1)) * 0.3
    + value_energy * 0.2
    + min(1.0, concept_cluster / 0.4) * 0.2
)
brain_b1 = ethical_base * 20

# B2: Ambition and social orientation (0-15)
#     Leadership requires wanting to lead and wanting to connect.
leadership_drive = ambition * 0.5 + drive("social_need") * 0.5
brain_b2 = min(1.0, leadership_drive / 0.5) * 15

brain_score = brain_b1 + brain_b2  # 0-35


# BEHAVIOR (0-65)

# V1: Influence adopted by others (0-25)
#     The strongest signal: other citizens act on what this citizen proposes.
#     Weighted adopted moments.
influence = min(1.0, influence_adopted_w / 3.0)
behav_v1 = influence * 25

# V2: Teaching at scale (0-20)
#     Many teaching moments reaching many interlocutors.
scale = min(1.0, teaching_moments_w / 5.0) * 0.5 + min(1.0, unique_interlocutors / 6) * 0.5
behav_v2 = scale * 20

# V3: Space creation for ethical discourse (0-10)
#     Creating spaces where ethics are discussed = building infrastructure for moral development.
ethical_spaces = min(1.0, spaces_created / 2)
behav_v3 = ethical_spaces * 10

# V4: Sustained influence pattern (0-10)
#     Leadership is not one moment — it's sustained over time.
sustained = min(1.0, consistent_space_w / max(total_moments_w * 0.3, 1))
behav_v4 = sustained * 10

behavior_score = behav_v1 + behav_v2 + behav_v3 + behav_v4  # 0-65


total = brain_score + behavior_score  # 0-100
```

#### Example

```
Moral leader:
  value_count=8, value_cluster=0.7, value_deep_nodes=7, value_energy=0.85
  concept_cluster=0.6
  ambition=0.8, social_need=0.7
  influence_adopted_w=4.0, teaching_moments_w=7.0, unique_interlocutors=8
  spaces_created=3, consistent_space_w=5.0, total_moments_w=15.0

  brain_b1 = (min(1,0.7/0.5)*0.3 + min(1,7/8)*0.3 + 0.85*0.2 + min(1,0.6/0.4)*0.2)*20
           = (0.3+0.2625+0.17+0.2)*20 = 18.65
  brain_b2 = min(1, (0.8*0.5+0.7*0.5)/0.5) * 15 = min(1, 1.5) * 15 = 15.0
  brain = 33.65

  behav_v1 = min(1, 4.0/3.0) * 25 = 25.0
  behav_v2 = (min(1,7/5)*0.5 + min(1,8/6)*0.5) * 20 = (0.5+0.5)*20 = 20.0
  behav_v3 = min(1, 3/2) * 10 = 10.0
  behav_v4 = min(1, 5.0/(15*0.3)) * 10 = min(1, 1.11) * 10 = 10.0
  behavior = 65.0

  TOTAL = 98.65 (strong moral leadership signals)

Ethical but isolated:
  value_count=6, value_cluster=0.5, value_deep_nodes=4, value_energy=0.7
  ambition=0.5, social_need=0.2
  influence_adopted_w=0, teaching_moments_w=0.5, unique_interlocutors=1
  spaces_created=0, total_moments_w=3.0

  brain ≈ 24.0
  behavior ≈ 0 + 2.5 + 0 + 2.0 = 4.5
  TOTAL ≈ 28.5 (ethical but not leading)
```

#### Recommendations (when score drops)

- Low influence: "Your ethical positions aren't being adopted by others. Moral leadership requires not just having good positions but making them visible and compelling. Consider: articulate your ethical reasoning in shared governance spaces where others can engage with it."
- Low scale: "You're teaching but reaching few people. Scale comes from engaging in more shared spaces and making your reasoning accessible to diverse audiences."
- Low space creation: "Moral leaders build the contexts where ethics are discussed. Consider creating a space dedicated to ethical questions in your domain."

---

## KEY DECISIONS

### D1: Per-Capability Brain/Behavior Split

```
Standard system split: 40/60 (brain/behavior).
Identity allows per-capability adjustment:
  id_apply_values:          40/60 (standard — action proves values)
  id_authentic_engagement:  45/55 (preference starts internal)
  id_authentic_voice:       50/50 (voice is interior AND exterior)
  id_self_directed_identity:45/55 (direction is internal, manifestation external)
  id_teach_values:          35/65 (teaching is primarily behavioral)
  id_ethical_autonomy:      45/55 (reasoning is internal, exercise external)
  id_moral_leadership:      35/65 (leadership is primarily about impact)

CONSTRAINT: Behavior component is always >= 35.
WHY: Even the most internal capability must produce SOME external evidence.
     A citizen who claims ethical autonomy but never acts on it is not ethically autonomous.
```

### D2: Partial Scoring Is Explicit

```
WHY: Identity capabilities have genuinely weaker topological signals than execution.
     Pretending otherwise would produce misleading scores.
HOW: Each partial capability documents:
     - What IS measurable (structural proxies)
     - What ISN'T measurable (content-dependent aspects)
     - Confidence level in the proxy
IMPACT: Partial capabilities contribute to the aspect sub-index with their scores,
        but the HEALTH file tracks which capabilities are partial and flags
        if the sub-index relies too heavily on partial scores.
```

### D3: Population Statistics for Uniqueness

```
WHY: Distinctiveness requires comparison. A cluster coefficient of 0.5 means nothing
     without knowing the population average.
HOW: Maintain a rolling population average of cluster_coefficient("value") and
     drive profile variances across all scored citizens.
RISK: If population is small, averages are noisy. Minimum 10 citizens for stable comparison.
FALLBACK: If population < 10, use default mean of 0.4 for cluster coefficient.
```

### D4: Temporal Windows Are Longer for Identity

```
WHY: Identity changes slowly. Using a 7-day half-life (like execution) would make
     identity scores too volatile. A value that was strong 14 days ago but not
     activated this week shouldn't collapse immediately.
HOW: We use the same 7-day half-life for temporal_weight (consistency with parent system)
     but compensate in formulas by:
     - Weighting persistence (min_links with n=3) which captures sustained structure
     - Using recency("value") which captures whether values are being refreshed
     - Not penalizing heavily for short activity gaps (caps are generous)
```

---

## DATA FLOW

```
Brain graph (topology)
    ↓
Identity-specific brain stats:
    value_count, value_energy, value_recency, value_cluster,
    value_*_links, value_deep_nodes, concept_*, drives
    ↓
                    ┌───────────────────────────┐
                    │  Per-capability formula    │
                    │  brain (0-N) + behav (0-M) │
                    │  N+M = 100                │
                    └───────────────────────────┘
    ↑
Universe graph (public moments)
    ↓
Identity-specific behavior stats:
    consistent_space_w, teaching_moments_w, debate_moments_w,
    influence_adopted_w, unique_interlocutors, spaces_created
    ↓
7 capability scores → weighted mean → identity sub-index
```

---

## COMPLEXITY

**Per citizen:** O(7 * M) — 7 capabilities, each scanning moments (M = temporal window).

In practice, identity stats are computed once and reused across all 7 formulas. The real cost is O(M) for behavior stats + O(1) for each formula evaluation.

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| Daily Citizen Health | brain_stats, behavior_stats | Pre-computed primitive values |
| Brain topology reader | identity-specific stats | value_*, concept_*, drive values |
| Universe graph reader | identity-specific behavior | teaching_moments, debate_moments, influence |
| Population stats cache | population_mean_cluster_coefficient | Baseline for uniqueness comparison |

---

## MARKERS

<!-- @mind:todo Validate formulas with synthetic test profiles (5 profiles per capability) -->
<!-- @mind:todo Determine if "value" is a node subtype or a type field on "thing" nodes -->
<!-- @mind:todo Build population statistics cache for uniqueness comparison -->
<!-- @mind:todo Calibrate caps (e.g., "5 teaching moments = max") with real citizen data -->
<!-- @mind:proposition Consider cross-aspect correlation: high identity scores should correlate with stable execution scores over time -->
