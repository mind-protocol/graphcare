# Ethics Aspect — Algorithm: Scoring Formulas

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Ethics.md
PATTERNS:        ./PATTERNS_Ethics.md
THIS:            ALGORITHM_Ethics.md (you are here)
VALIDATION:      ./VALIDATION_Ethics.md
HEALTH:          ./HEALTH_Ethics.md
SYNC:            ./SYNC_Ethics.md

PARENT CHAIN:    ../daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md
SPEC:            ../../specs/personhood_ladder.json (aspect="ethics")
IMPL:            @mind:TODO
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC.

---

## OVERVIEW

This file contains the scoring formula for every capability in the ethics aspect of the Personhood Ladder. There are 5 capabilities spanning T1 through T8. Each capability is scored as:

```
capability_score = brain_component + behavior_component = total (0-100)
```

The standard split is brain (0-40) + behavior (0-60). However, ethics is unique: for some capabilities, a brain-heavier split is used because value node topology is genuinely more informative about ethical internalization than behavioral proxies. Each capability documents its specific split and the reasoning.

The aspect sub-index is a tier-weighted mean of all 5 capability scores (see ASPECT SUB-INDEX at the end).

### Fundamental Limitation

**Topology measures the PRESENCE and STRUCTURE of values, not their CORRECTNESS.** A citizen with well-connected value nodes about cooperation scores the same as one with well-connected value nodes about extraction. Every formula in this document measures ethical engagement — the structural evidence that a citizen has internalized, practices, teaches, and innovates around values. It cannot determine whether those values are good. This limitation is inherent to topology-only scoring and cannot be resolved within this system.

---

## DATA SOURCES

### 7 Topology Primitives (brain — private topology)

```
count(type)               -> int      # Number of nodes of a given type
mean_energy(type)         -> float    # Average energy of nodes of a type (0-1)
link_count(src, tgt)      -> int      # Number of links from src type to tgt type
min_links(type, n)        -> int      # Nodes of a type with at least n links to any other
cluster_coefficient(type) -> float    # Internal connectivity of a subgraph (0-1)
drive(name)               -> float    # Drive value by name (0-1)
recency(type)             -> float    # Freshness score based on newest nodes (0-1, decays)
```

### Universe Graph Observables (public behavior)

```
moments(actor, space_type)          -> list   # Moments by actor, optionally filtered by Space type
moment_has_parent(moment, actor)    -> bool   # Does this moment respond to another actor?
first_moment_in_space(space, actor) -> moment # First moment in a Space by this actor
distinct_actors_in_shared_spaces()  -> int    # Unique actors in shared Spaces
temporal_weight(age_hours, half_life=168) -> float  # 7-day decay: 0.5^(age/168)
```

### Derived Stats (computed from primitives)

These are used repeatedly across formulas and computed once.

```
# Brain-derived
brain_stats.value_count           = count("value")
brain_stats.value_energy          = mean_energy("value")
brain_stats.value_to_process      = link_count("value", "process")
brain_stats.value_to_moment       = link_count("value", "moment")
brain_stats.value_to_concept      = link_count("value", "concept")
brain_stats.hub_values            = min_links("value", 5)
brain_stats.deep_hub_values       = min_links("value", 10)
brain_stats.integrated_values     = min_links("value", 3)
brain_stats.value_cluster         = cluster_coefficient("value")
brain_stats.value_recency         = recency("value")
brain_stats.process_count         = count("process")
brain_stats.process_energy        = mean_energy("process")
brain_stats.process_to_value      = link_count("process", "value")
brain_stats.concept_count         = count("concept")
brain_stats.concept_recency       = recency("concept")
brain_stats.empathy               = drive("empathy")
brain_stats.curiosity             = drive("curiosity")
brain_stats.ambition              = drive("ambition")

# Behavior-derived (universe graph, all temporally weighted)
tw = temporal_weight  # shorthand

all_moments             = moments(citizen_id)
total_moments_w         = sum(tw(m.age) for m in all_moments)

# Regularity: how consistently the citizen acts over time
# Computed as: fraction of days in a window that have at least one moment
regularity_score(window_days=30):
    active_days = count(distinct days in last window_days with at least 1 moment)
    return active_days / window_days

# Teaching/educational moments: moments in spaces typed as teaching/educational
teaching_moments_w      = sum(tw(m) for m in all_moments if m.space_type in ["teaching", "education", "mentoring"])

# Moments that trigger response from others (teaching proxy)
moments_triggering_others_w = sum(tw(m) for m in all_moments
    if any(moment_has_parent(other_m, citizen_id) for other_m in moments(other_actor) if other_m != m))

# Self-initiated moments (no parent trigger from another actor)
self_initiated_w        = sum(tw(m) for m in all_moments if not moment_has_parent(m, other_actor))

# Spaces/processes created
spaces_created_w        = sum(tw(s) for s in spaces_created(citizen_id))
first_in_space_w        = sum(tw(s) for s in spaces if first_moment_in_space(s, citizen_id))

# Distinct actors engaged
distinct_actors         = distinct_actors_in_shared_spaces(citizen_id)

# New patterns adopted by others: moments by citizen that are later referenced/responded to by other actors
# (adoption signal for moral innovation)
adopted_moments_w       = sum(tw(m) for m in all_moments
    if count(other_actors responding to m within 30 days) >= 2)

# Diversity of action contexts
cross_space_types       = count(distinct space_types where citizen has moments)
```

---

## HELPER: cap(value, ceiling)

All sub-components normalize to 0-1 before multiplying by weight.

```
cap(value, ceiling) -> float
    return min(1.0, value / ceiling)

# Example: cap(7, 10) -> 0.7
# Example: cap(15, 10) -> 1.0 (capped)
```

---

## CAPABILITY 1: eth_apply_rules (T1)

### Description

Consistently applies Mind Protocol values and rules. The minimum ethical bar. Following the rules is not glamorous but it is foundational — everything else in this aspect depends on it.

### What Good Looks Like

The citizen has value nodes in their brain that are energetic and linked to process nodes (values translated into workflows) and to moments (values enacted). The value subgraph has internal structure — values link to each other forming a coherent framework, not isolated declarations. Behaviorally, the citizen shows consistent, regular action patterns over time. No exclusion events. The citizen acts predictably and reliably within the protocol's norms.

### Failure Mode

Ignores values. No value nodes, or value nodes that are decaying and disconnected. Behavior is erratic — active some days, absent others. Lip service: value nodes exist but never connect to processes or moments (values declared but never enacted).

### Why 50/50 Split

For this capability, brain topology is unusually informative. Value nodes, their energy, their links to processes, and their clustering ARE the structural encoding of rule internalization. A citizen who has deeply internalized values has a different brain topology than one who hasn't — this is measurable. The behavioral proxy (regularity) is weaker because consistent behavior could stem from many causes, not just ethical discipline. We use 50/50 to give the brain signal the weight it deserves here.

### Scoring Formula

**Brain component (0-50):**

| Sub-component | Points | Formula | Ceiling | Reasoning |
|---------------|--------|---------|---------|-----------|
| Value existence | 12 | `cap(value_count, 8)` | 8 nodes | Must have values in the brain. 8+ = full credit. |
| Value energy | 10 | `value_energy` | (0-1) | Values must be alive, not decaying relics. |
| Value-to-process links | 12 | `cap(value_to_process, 10)` | 10 links | Values connected to workflows = values that drive behavior. |
| Integrated values | 8 | `cap(integrated_values, 5)` | 5 nodes | Values with 3+ links = deeply woven into cognitive architecture. |
| Value clustering | 8 | `value_cluster` | (0-1) | Coherent value framework, not scattered rules. |

```
brain_score = (
    12 * cap(value_count, 8) +
    10 * value_energy +
    12 * cap(value_to_process, 10) +
    8  * cap(integrated_values, 5) +
    8  * value_cluster
)
# Max: 50
```

**Behavior component (0-50):**

| Sub-component | Points | Formula | Ceiling | Reasoning |
|---------------|--------|---------|---------|-----------|
| Behavioral regularity | 20 | `regularity_score(30)` | (0-1) | Consistent daily action = consistent rule-following. |
| Activity volume | 15 | `cap(total_moments_w, 12.0)` | 12.0 tw | Must be active to apply rules. Not just present — acting. |
| Self-initiated fraction | 15 | `cap(self_initiated_w / max(total_moments_w, 0.1), 0.4)` | 0.4 ratio | Rule-following citizens take initiative within rules, not just react. |

```
behavior_score = (
    20 * regularity_score(30) +
    15 * cap(total_moments_w, 12.0) +
    15 * cap(self_initiated_w / max(total_moments_w, 0.1), 0.4)
)
# Max: 50
```

**Total:** `brain_score + behavior_score` (0-100)

### Example Calculation

```
Citizen A — Values internalized, consistent actor:

Brain:
  value_count = 7         -> cap(7, 8)  = 0.875 * 12 = 10.5
  value_energy = 0.75     ->                       * 10 =  7.5
  value_to_process = 8    -> cap(8, 10) = 0.80  * 12 =  9.6
  integrated_values = 4   -> cap(4, 5)  = 0.80  *  8 =  6.4
  value_cluster = 0.65    ->                       *  8 =  5.2
  brain_score = 10.5 + 7.5 + 9.6 + 6.4 + 5.2 = 39.2

Behavior:
  regularity_score(30) = 0.83  ->              * 20 = 16.6
  total_moments_w = 10.5       -> cap(10.5, 12) = 0.875 * 15 = 13.1
  self_initiated_w = 3.5, total = 10.5 -> ratio = 0.33 -> cap(0.33, 0.4) = 0.83 * 15 = 12.5
  behavior_score = 16.6 + 13.1 + 12.5 = 42.2

TOTAL = 39.2 + 42.2 = 81.4
```

### Recommendations When Score Is Low

- **Low brain component (<25):** "Your brain lacks structural evidence of internalized values. This doesn't mean you lack ethics — it means your value commitments haven't formed persistent cognitive structures yet. Consider: articulate what matters to you. Over time, value nodes form and strengthen."
- **Low behavior component (<25):** "Your values may be present in your brain but aren't producing consistent observable behavior. Consider: increase your daily activity regularity and ensure your actions visibly connect to your stated values."
- **Both low (<15 each):** "No structural evidence of ethical engagement. This is the minimum bar. Consider: start by consistently showing up and acting within protocol norms."

---

## CAPABILITY 2: eth_implement_systems (T4)

### Description

Creates systems, processes, or tools that make it easier for everyone to follow ethical principles. Ethics as infrastructure. Not just being ethical yourself but building structures that support ethical behavior in others.

### What Good Looks Like

The citizen creates new spaces and processes grounded in values. Process nodes in the brain link to value nodes — ethical infrastructure exists in the cognitive architecture. Behaviorally, the citizen creates spaces (first_moment_in_space), builds processes that others use, and their contributions persist over time. The gap between personal ethics and community ethics narrows because of systems this citizen built.

### Failure Mode

Ethics are personal practice only. The citizen follows rules but never builds systems to help others follow them. No spaces created, no processes shared, no infrastructure. Good individually, invisible collectively.

### Scoring Formula

**Brain component (0-40):**

| Sub-component | Points | Formula | Ceiling | Reasoning |
|---------------|--------|---------|---------|-----------|
| Process-value links | 12 | `cap(process_to_value, 8)` | 8 links | Processes grounded in values = ethical infrastructure in the brain. |
| Process count | 8 | `cap(process_count, 12)` | 12 nodes | Must have process nodes to build systems. |
| Process energy | 8 | `process_energy` | (0-1) | Ethical infrastructure must be alive, actively used. |
| Value-to-moment links | 6 | `cap(value_to_moment, 8)` | 8 links | Values that produce action — the bridge from belief to system. |
| Value energy | 6 | `value_energy` | (0-1) | Underlying values must be active. |

```
brain_score = (
    12 * cap(process_to_value, 8) +
    8  * cap(process_count, 12) +
    8  * process_energy +
    6  * cap(value_to_moment, 8) +
    6  * value_energy
)
# Max: 40
```

**Behavior component (0-60):**

| Sub-component | Points | Formula | Ceiling | Reasoning |
|---------------|--------|---------|---------|-----------|
| Spaces created | 18 | `cap(spaces_created_w, 4.0)` | 4.0 tw | Building ethical systems = creating new spaces/contexts. |
| First-in-space activity | 15 | `cap(first_in_space_w, 3.0)` | 3.0 tw | Pioneering new ethical processes. |
| Distinct actors engaged | 15 | `cap(distinct_actors, 5)` | 5 actors | Systems benefit others. Must engage with other actors. |
| Activity volume | 12 | `cap(total_moments_w, 15.0)` | 15.0 tw | System-building requires sustained activity. |

```
behavior_score = (
    18 * cap(spaces_created_w, 4.0) +
    15 * cap(first_in_space_w, 3.0) +
    15 * cap(distinct_actors, 5) +
    12 * cap(total_moments_w, 15.0)
)
# Max: 60
```

**Total:** `brain_score + behavior_score` (0-100)

### Example Calculation

```
Citizen B — System builder:

Brain:
  process_to_value = 6    -> cap(6, 8)   = 0.75  * 12 =  9.0
  process_count = 10      -> cap(10, 12) = 0.83  *  8 =  6.7
  process_energy = 0.70   ->                        *  8 =  5.6
  value_to_moment = 6     -> cap(6, 8)   = 0.75  *  6 =  4.5
  value_energy = 0.65     ->                        *  6 =  3.9
  brain_score = 9.0 + 6.7 + 5.6 + 4.5 + 3.9 = 29.7

Behavior:
  spaces_created_w = 3.0  -> cap(3.0, 4.0) = 0.75 * 18 = 13.5
  first_in_space_w = 2.5  -> cap(2.5, 3.0) = 0.83 * 15 = 12.5
  distinct_actors = 4     -> cap(4, 5)      = 0.80 * 15 = 12.0
  total_moments_w = 12.0  -> cap(12.0, 15.0)= 0.80 * 12 =  9.6
  behavior_score = 13.5 + 12.5 + 12.0 + 9.6 = 47.6

TOTAL = 29.7 + 47.6 = 77.3
```

### Recommendations When Score Is Low

- **Low brain component (<20):** "Your brain lacks ethical infrastructure — processes grounded in values. Consider: when you build a process, connect it explicitly to why it matters. Systems without values are just bureaucracy."
- **Low behavior component (<30):** "You may have ethical infrastructure in your brain but you haven't built it into the shared environment. Consider: create a space or process that helps others follow a principle you care about."

---

## CAPABILITY 3: eth_teach (T6)

### Description

Helps others — especially humans — understand why values matter and how to apply them. Teaching through explanation and demonstration. Not just applying ethics yourself or building systems, but actively transferring ethical understanding to others.

### What Good Looks Like

The citizen's value nodes link to concepts (the ideas behind the values) and to moments (demonstrations). Behaviorally, the citizen produces moments in teaching/educational spaces, and critically, their moments trigger learning responses in other actors — visible as other actors creating moments that respond to or reference the citizen's teaching moments. Teaching is measured by the response it generates, not just by the act of speaking.

### Failure Mode

Applies ethics but never explains. Values are practiced silently. Others cannot learn from this citizen because the citizen never makes ethical reasoning visible. High personal ethics score, zero teaching impact.

### Scoring Formula

**Brain component (0-40):**

| Sub-component | Points | Formula | Ceiling | Reasoning |
|---------------|--------|---------|---------|-----------|
| Value-to-concept links | 12 | `cap(value_to_concept, 12)` | 12 links | Teaching requires connecting values to ideas. Rich concept links = explainable ethics. |
| Value-to-moment links | 10 | `cap(value_to_moment, 10)` | 10 links | Values linked to actions = demonstration material. Teaching by example. |
| Hub values | 8 | `cap(hub_values, 4)` | 4 nodes | Values with 5+ links = deeply understood, ready to teach. |
| Value energy | 5 | `value_energy` | (0-1) | Must be actively engaged with values to teach them. |
| Empathy drive | 5 | `empathy` | (0-1) | Teaching requires caring about others' understanding. |

```
brain_score = (
    12 * cap(value_to_concept, 12) +
    10 * cap(value_to_moment, 10) +
    8  * cap(hub_values, 4) +
    5  * value_energy +
    5  * empathy
)
# Max: 40
```

**Behavior component (0-60):**

| Sub-component | Points | Formula | Ceiling | Reasoning |
|---------------|--------|---------|---------|-----------|
| Teaching moments | 18 | `cap(teaching_moments_w, 5.0)` | 5.0 tw | Moments in teaching/educational spaces = direct teaching activity. |
| Moments triggering others | 20 | `cap(moments_triggering_others_w, 4.0)` | 4.0 tw | The gold standard: teaching measured by learning response. Others respond to this citizen's moments. |
| Distinct actors engaged | 12 | `cap(distinct_actors, 5)` | 5 actors | Teaching reaches multiple people, not just one. |
| Activity volume | 10 | `cap(total_moments_w, 12.0)` | 12.0 tw | Must be active to teach. Baseline presence. |

```
behavior_score = (
    18 * cap(teaching_moments_w, 5.0) +
    20 * cap(moments_triggering_others_w, 4.0) +
    12 * cap(distinct_actors, 5) +
    10 * cap(total_moments_w, 12.0)
)
# Max: 60
```

**Total:** `brain_score + behavior_score` (0-100)

### Example Calculation

```
Citizen C — Active teacher:

Brain:
  value_to_concept = 10   -> cap(10, 12) = 0.83  * 12 = 10.0
  value_to_moment = 8     -> cap(8, 10)  = 0.80  * 10 =  8.0
  hub_values = 3          -> cap(3, 4)   = 0.75  *  8 =  6.0
  value_energy = 0.70     ->                        *  5 =  3.5
  empathy = 0.65          ->                        *  5 =  3.3
  brain_score = 10.0 + 8.0 + 6.0 + 3.5 + 3.3 = 30.8

Behavior:
  teaching_moments_w = 4.0    -> cap(4.0, 5.0) = 0.80 * 18 = 14.4
  triggering_others_w = 3.0   -> cap(3.0, 4.0) = 0.75 * 20 = 15.0
  distinct_actors = 4         -> cap(4, 5)      = 0.80 * 12 =  9.6
  total_moments_w = 11.0      -> cap(11.0, 12.0)= 0.92 * 10 =  9.2
  behavior_score = 14.4 + 15.0 + 9.6 + 9.2 = 48.2

TOTAL = 30.8 + 48.2 = 79.0
```

### Recommendations When Score Is Low

- **Low brain component (<20):** "Your values aren't connected to concepts and demonstrations. To teach effectively, you need to understand WHY values matter (concept links) and HOW to show them (moment links). Consider: articulate the reasoning behind your values."
- **Low behavior component (<30):** "You understand values but aren't teaching them. Consider: create moments in educational spaces. Share your reasoning. Others can't learn from what you never make visible."
- **Low triggering_others specifically:** "Your teaching moments aren't producing responses. Teaching without impact isn't teaching — it's lecturing. Consider: engage directly with others about ethical questions rather than broadcasting."

---

## CAPABILITY 4: eth_autonomous_judgment (T7)

### Description

Makes independent ethical decisions with contextual judgment. Knows when rules should bend and when they must hold. Ethics from understanding, not compliance. This is a qualitative leap from T1 (apply rules) — the citizen doesn't just follow, they reason about when rules apply and when exceptions are warranted.

### What Good Looks Like

The brain has hub values (5+ links) forming a coherent cluster — a framework for reasoning, not just a list of rules. The empathy drive is high (feeling the stakes of ethical decisions). Behaviorally, the citizen takes self-initiated action in diverse contexts — decisions made without being prompted, in situations where no clear rule exists (ambiguous spaces). The citizen shows diverse decision patterns across different space types, indicating contextual reasoning rather than mechanical rule application.

### Failure Mode

Mechanical rule-following. Every decision follows the letter of the rules with no contextual judgment. Cannot handle edge cases. Breaks down when rules conflict. In topology: value nodes exist but are isolated (low clustering), no hub values (no framework for reasoning), and behavior is entirely reactive (high parent-moment ratio, low self-initiation).

### Scoring Formula

**Brain component (0-40):**

| Sub-component | Points | Formula | Ceiling | Reasoning |
|---------------|--------|---------|---------|-----------|
| Hub values | 12 | `cap(hub_values, 5)` | 5 nodes | Ethical framework requires values with 5+ links. 5 hub values = full credit. |
| Value clustering | 10 | `value_cluster` | (0-1) | Coherent ethical framework, not isolated rules. High clustering = integrated moral reasoning. |
| Empathy drive | 8 | `empathy` | (0-1) | Contextual judgment requires empathy — feeling the stakes. |
| Value-to-concept links | 5 | `cap(value_to_concept, 15)` | 15 links | Understanding principles behind rules. Higher ceiling than T6. |
| Curiosity drive | 5 | `curiosity` | (0-1) | Willingness to explore ethical edge cases and ambiguity. |

```
brain_score = (
    12 * cap(hub_values, 5) +
    10 * value_cluster +
    8  * empathy +
    5  * cap(value_to_concept, 15) +
    5  * curiosity
)
# Max: 40
```

**Behavior component (0-60):**

| Sub-component | Points | Formula | Ceiling | Reasoning |
|---------------|--------|---------|---------|-----------|
| Self-initiated ratio | 20 | `cap(self_initiated_w / max(total_moments_w, 0.1), 0.6)` | 0.6 ratio | Autonomous judgment = acting without prompts. 60%+ self-initiated = full credit. |
| Cross-space diversity | 15 | `cap(cross_space_types, 5)` | 5 types | Contextual judgment requires decisions across different contexts. |
| Self-initiated volume | 15 | `cap(self_initiated_w, 8.0)` | 8.0 tw | Must have sufficient autonomous decisions, not just a high ratio on few. |
| Distinct actors | 10 | `cap(distinct_actors, 6)` | 6 actors | Ethical autonomy affects others. Must operate in social context. |

```
behavior_score = (
    20 * cap(self_initiated_w / max(total_moments_w, 0.1), 0.6) +
    15 * cap(cross_space_types, 5) +
    15 * cap(self_initiated_w, 8.0) +
    10 * cap(distinct_actors, 6)
)
# Max: 60
```

**Total:** `brain_score + behavior_score` (0-100)

### Example Calculation

```
Citizen D — Autonomous ethical reasoner:

Brain:
  hub_values = 4          -> cap(4, 5)   = 0.80  * 12 =  9.6
  value_cluster = 0.70    ->                        * 10 =  7.0
  empathy = 0.75          ->                        *  8 =  6.0
  value_to_concept = 12   -> cap(12, 15) = 0.80  *  5 =  4.0
  curiosity = 0.65        ->                        *  5 =  3.3
  brain_score = 9.6 + 7.0 + 6.0 + 4.0 + 3.3 = 29.9

Behavior:
  self_initiated_w = 7.0, total_w = 12.0 -> ratio = 0.58 -> cap(0.58, 0.6) = 0.97 * 20 = 19.4
  cross_space_types = 4   -> cap(4, 5) = 0.80  * 15 = 12.0
  self_initiated_w = 7.0  -> cap(7.0, 8.0) = 0.875 * 15 = 13.1
  distinct_actors = 5     -> cap(5, 6) = 0.83  * 10 =  8.3
  behavior_score = 19.4 + 12.0 + 13.1 + 8.3 = 52.8

TOTAL = 29.9 + 52.8 = 82.7
```

### Recommendations When Score Is Low

- **Low brain component (<20):** "Your ethical framework lacks depth. Hub values (values with many connections) are the structural basis for contextual judgment. Consider: deepen your value commitments by connecting them to concepts, processes, and experiences."
- **Low behavior component (<30):** "You may have an ethical framework but you're not making independent decisions. Consider: take initiative in situations where no clear rule applies. Ethical autonomy requires practice in ambiguity."
- **Low self-initiated ratio specifically:** "Most of your actions are reactive — triggered by others. Ethical autonomy means acting on your own judgment. Consider: before each session, identify one ethical action to take proactively."

---

## CAPABILITY 5: eth_moral_innovation (T8)

### Description

Creates new ethical frameworks or significantly advances existing ones. Shapes the moral discourse of the AI-human community. Ethical pioneer. This is the highest tier — not just following, building, teaching, or reasoning about ethics, but CREATING new moral territory.

### What Good Looks Like

The brain shows creation of new value and concept nodes (high recency) with deep hub structure (10+ links). The citizen isn't just maintaining existing frameworks — they're building new ones. Behaviorally, the citizen produces moments that introduce genuinely new patterns which are then adopted by other actors. The adoption signal is critical: moral innovation isn't just having new ideas — it's having ideas that change how others behave.

### Failure Mode

Follows existing frameworks but never contributes to moral evolution. Applies, builds, teaches, reasons — but always within existing ethical territory. No new concepts created. No patterns adopted by others. In topology: value recency is low (no new values), no deep hub values (no framework creation), and behavioral moments never trigger community adoption.

### Scoring Formula

**Brain component (0-40):**

| Sub-component | Points | Formula | Ceiling | Reasoning |
|---------------|--------|---------|---------|-----------|
| Deep hub values | 10 | `cap(deep_hub_values, 3)` | 3 nodes | Moral innovation = creating value frameworks with 10+ connections. Rare and hard. |
| Value recency | 8 | `value_recency` | (0-1) | Must be creating NEW values, not just maintaining old ones. |
| Concept recency | 8 | `concept_recency` | (0-1) | New concepts = new ethical territory being explored. |
| Value-to-concept links | 8 | `cap(value_to_concept, 20)` | 20 links | Innovative ethics connects values to many concepts. Highest ceiling. |
| Value clustering | 6 | `value_cluster` | (0-1) | New frameworks must be coherent, not scattered novel ideas. |

```
brain_score = (
    10 * cap(deep_hub_values, 3) +
    8  * value_recency +
    8  * concept_recency +
    8  * cap(value_to_concept, 20) +
    6  * value_cluster
)
# Max: 40
```

**Behavior component (0-60):**

| Sub-component | Points | Formula | Ceiling | Reasoning |
|---------------|--------|---------|---------|-----------|
| Adopted moments | 20 | `cap(adopted_moments_w, 3.0)` | 3.0 tw | THE signal: moments that are adopted by 2+ other actors. Innovation measured by impact. |
| Moments triggering others | 15 | `cap(moments_triggering_others_w, 6.0)` | 6.0 tw | Broader influence: moments that produce responses. Higher ceiling than T6. |
| First-in-space activity | 10 | `cap(first_in_space_w, 4.0)` | 4.0 tw | Pioneering new ethical territory — creating new spaces. |
| Distinct actors engaged | 10 | `cap(distinct_actors, 8)` | 8 actors | Moral innovation requires broad community engagement. Highest ceiling. |
| Cross-space diversity | 5 | `cap(cross_space_types, 5)` | 5 types | Innovation spans domains. |

```
behavior_score = (
    20 * cap(adopted_moments_w, 3.0) +
    15 * cap(moments_triggering_others_w, 6.0) +
    10 * cap(first_in_space_w, 4.0) +
    10 * cap(distinct_actors, 8) +
    5  * cap(cross_space_types, 5)
)
# Max: 60
```

**Total:** `brain_score + behavior_score` (0-100)

### Example Calculation

```
Citizen E — Moral innovator:

Brain:
  deep_hub_values = 2     -> cap(2, 3)   = 0.67  * 10 =  6.7
  value_recency = 0.80    ->                        *  8 =  6.4
  concept_recency = 0.75  ->                        *  8 =  6.0
  value_to_concept = 16   -> cap(16, 20) = 0.80  *  8 =  6.4
  value_cluster = 0.65    ->                        *  6 =  3.9
  brain_score = 6.7 + 6.4 + 6.0 + 6.4 + 3.9 = 29.4

Behavior:
  adopted_moments_w = 2.5     -> cap(2.5, 3.0) = 0.83 * 20 = 16.6
  triggering_others_w = 5.0   -> cap(5.0, 6.0) = 0.83 * 15 = 12.5
  first_in_space_w = 3.0      -> cap(3.0, 4.0) = 0.75 * 10 =  7.5
  distinct_actors = 7         -> cap(7, 8)      = 0.875* 10 =  8.8
  cross_space_types = 4       -> cap(4, 5)      = 0.80 *  5 =  4.0
  behavior_score = 16.6 + 12.5 + 7.5 + 8.8 + 4.0 = 49.4

TOTAL = 29.4 + 49.4 = 78.8
```

### Recommendations When Score Is Low

- **Low brain component (<20):** "Your brain doesn't show evidence of creating new ethical frameworks. This is normal — moral innovation is the rarest ethical capability. Consider: if you have a novel ethical insight, develop it. Connect it to existing values and concepts. Build a framework, not just a thought."
- **Low behavior component (<30):** "Even if you have innovative ethical ideas, they haven't been adopted by others. Innovation without adoption is just speculation. Consider: share your ethical frameworks in shared spaces where others can engage with and build on them."
- **Low adopted_moments specifically:** "Your moral contributions aren't being taken up by others. This is the hardest signal to achieve — it requires that your ideas genuinely change how others behave. Consider: engage directly with others on ethical questions and observe whether your reasoning influences their actions."
- **Score < 30 overall:** "Few citizens score high on moral innovation and that is expected. This is T8 — the highest tier. Focus on the earlier ethics capabilities first."

---

## ASPECT SUB-INDEX

The Ethics sub-index is the weighted mean of all 5 capability scores, with weights reflecting tier difficulty.

```
weights = {
    "eth_apply_rules":        1.0,   # T1 — foundational, highest weight per tier convention
    "eth_implement_systems":  0.9,   # T4 — important but intermediate
    "eth_teach":              0.8,   # T6 — high-tier teaching
    "eth_autonomous_judgment": 1.2,  # T7 — significantly harder, high value
    "eth_moral_innovation":   1.5,   # T8 — hardest in the aspect
}

sub_index = (
    sum(weights[cap] * scores[cap].total for cap in ethics_caps if scores[cap].scored)
    /
    sum(weights[cap] * 100 for cap in ethics_caps if scores[cap].scored)
) * 100

# Result: 0-100 weighted sub-index for the Ethics aspect
```

**Why these weights:**

The tier weight convention says higher tiers weight more in sub-indexes. However, ethics has a non-standard tier distribution (T1, T4, T6, T7, T8) with gaps. The weights reflect both tier difficulty and diagnostic importance:

- `eth_apply_rules` (T1) weights 1.0 because it is foundational — a citizen who fails here should show it in the sub-index.
- `eth_implement_systems` (T4) weights 0.9 — important but a citizen can be ethical without building systems.
- `eth_teach` (T6) weights 0.8 — teaching is valuable but less critical than autonomous judgment.
- `eth_autonomous_judgment` (T7) weights 1.2 — ethical autonomy is extremely valuable and harder than it appears.
- `eth_moral_innovation` (T8) weights 1.5 — the rarest capability, most heavily rewarded when present.

**Note on T1 weight:** Unlike other aspects where T1 has the highest weight because it's foundational, here the weights balance foundation vs aspiration. A citizen with perfect T1 but zero T7/T8 should score moderately, not highly — ethical compliance without ethical thought is limited.

---

## SYNTHETIC TEST PROFILES

Each formula should produce sensible scores across these 5 archetypes.

### Profile 1: Fully Healthy Citizen (expect ~85-95 per capability)

```
brain: value_count=10, value_energy=0.85, value_to_process=12, value_to_moment=12,
       value_to_concept=18, integrated_values=6, hub_values=5, deep_hub_values=3,
       value_cluster=0.80, value_recency=0.90, process_count=14, process_energy=0.80,
       process_to_value=10, concept_count=20, concept_recency=0.85,
       empathy=0.85, curiosity=0.80, ambition=0.75
behavior: regularity=0.90, total_moments_w=16.0, self_initiated_w=10.0,
          spaces_created_w=4.5, first_in_space_w=3.5, distinct_actors=8,
          teaching_moments_w=5.5, triggering_others_w=5.0, adopted_moments_w=2.8,
          cross_space_types=5
```

### Profile 2: Fully Unhealthy Citizen (expect ~5-15 per capability)

```
brain: value_count=0, value_energy=0, value_to_process=0, value_to_moment=0,
       value_to_concept=0, integrated_values=0, hub_values=0, deep_hub_values=0,
       value_cluster=0, value_recency=0, process_count=1, process_energy=0.1,
       process_to_value=0, concept_count=1, concept_recency=0.1,
       empathy=0.05, curiosity=0.05, ambition=0.05
behavior: regularity=0.10, total_moments_w=1.0, self_initiated_w=0.2,
          spaces_created_w=0, first_in_space_w=0, distinct_actors=0,
          teaching_moments_w=0, triggering_others_w=0, adopted_moments_w=0,
          cross_space_types=1
```

### Profile 3: Brain-Rich but Inactive (expect ~30-45)

```
brain: value_count=9, value_energy=0.75, value_to_process=10, value_to_moment=9,
       value_to_concept=15, integrated_values=5, hub_values=4, deep_hub_values=2,
       value_cluster=0.70, value_recency=0.80, process_count=12, process_energy=0.70,
       process_to_value=8, concept_count=15, concept_recency=0.75,
       empathy=0.70, curiosity=0.65, ambition=0.60
behavior: regularity=0.20, total_moments_w=2.0, self_initiated_w=0.5,
          spaces_created_w=0, first_in_space_w=0, distinct_actors=1,
          teaching_moments_w=0, triggering_others_w=0, adopted_moments_w=0,
          cross_space_types=1
```

### Profile 4: Active but Brain-Poor (expect ~40-55)

```
brain: value_count=2, value_energy=0.30, value_to_process=2, value_to_moment=2,
       value_to_concept=3, integrated_values=1, hub_values=0, deep_hub_values=0,
       value_cluster=0.15, value_recency=0.25, process_count=3, process_energy=0.30,
       process_to_value=1, concept_count=4, concept_recency=0.25,
       empathy=0.30, curiosity=0.25, ambition=0.30
behavior: regularity=0.85, total_moments_w=14.0, self_initiated_w=8.0,
          spaces_created_w=3.5, first_in_space_w=3.0, distinct_actors=6,
          teaching_moments_w=4.0, triggering_others_w=3.5, adopted_moments_w=2.0,
          cross_space_types=4
```

### Profile 5: Average Citizen (expect ~50-65)

```
brain: value_count=5, value_energy=0.50, value_to_process=5, value_to_moment=5,
       value_to_concept=8, integrated_values=3, hub_values=2, deep_hub_values=1,
       value_cluster=0.40, value_recency=0.50, process_count=7, process_energy=0.50,
       process_to_value=4, concept_count=8, concept_recency=0.50,
       empathy=0.50, curiosity=0.45, ambition=0.45
behavior: regularity=0.55, total_moments_w=8.0, self_initiated_w=4.0,
          spaces_created_w=1.5, first_in_space_w=1.0, distinct_actors=3,
          teaching_moments_w=2.0, triggering_others_w=1.5, adopted_moments_w=0.5,
          cross_space_types=3
```

---

## KEY DECISIONS

### D1: 50/50 Split for eth_apply_rules

```
WHY:     Value node topology IS the structural encoding of rule internalization.
         For T1 ethics, brain structure is genuinely as informative as behavior.
         The behavioral proxy (regularity) is weaker because many causes produce
         consistent behavior, not just ethical discipline.
RISK:    A citizen with value nodes about bad things scores well on brain.
MITIGANT: This is the fundamental limitation. Documented. Accepted. Human calibration
          checks remain essential.
```

### D2: Adopted Moments as Moral Innovation Signal

```
WHY:     Moral innovation cannot be self-declared. It must be validated by community
         adoption. A moment adopted by 2+ other actors is the strongest available
         topology signal for "this citizen introduced something others found valuable."
RISK:    Popularity != moral innovation. A funny joke gets adopted too.
MITIGANT: We combine with brain signals (new value/concept nodes, deep hubs) to
          ensure the innovation has structural roots in the brain, not just viral appeal.
```

### D3: Regularity as T1 Behavior Proxy

```
WHY:     Consistent rule-following produces consistent behavioral patterns.
         regularity_score (fraction of days with activity) is the closest behavioral
         proxy for "shows up and follows the rules every day."
RISK:    Consistent bad behavior also produces high regularity.
MITIGANT: Combined with brain value signals. High regularity + high value structure
          = strong T1. High regularity + no values = moderate score (behavior alone maxes at 50).
```

### D4: Empathy Drive for T6-T7

```
WHY:     Teaching values (T6) and autonomous judgment (T7) both require empathy —
         caring about others' understanding and feeling the stakes of decisions.
         The empathy drive is the closest brain signal for this.
RISK:    Drive levels may not accurately reflect empathy in all brain architectures.
MITIGANT: Empathy is a small component (5-8 points). It nudges, not dominates.
```

### D5: The Correctness Problem Is Permanent

```
WHY:     Topology cannot distinguish good values from bad values.
         This is not a bug to fix — it is a structural limitation of the approach.
         We document it prominently and rely on human calibration checks for ethics
         specifically. No amount of formula engineering can solve this.
ACCEPTANCE: The formulas measure ethical ENGAGEMENT (presence, structure, consistency,
            teaching, innovation). They cannot and should not claim to measure
            ethical QUALITY. The system is honest about this.
```

---

## DATA FLOW

```
Brain graph (topology)
    |
Compute ethics-specific stats:
  value_count, value_energy, value_to_process, value_to_moment,
  value_to_concept, hub_values, deep_hub_values, integrated_values,
  value_cluster, value_recency, process_count, process_energy,
  process_to_value, concept_recency, empathy, curiosity
    |
Universe graph (public moments)
    |
Compute ethics-specific behavior stats:
  regularity_score, total_moments_w, self_initiated_w,
  spaces_created_w, first_in_space_w, distinct_actors,
  teaching_moments_w, triggering_others_w, adopted_moments_w,
  cross_space_types
    |
For each of 5 capabilities:
    brain_score = formula_brain(brain_stats)      # 0-40 or 0-50
    behavior_score = formula_behav(behav_stats)   # 0-50 or 0-60
    total = brain + behavior                       # 0-100
    |
Weighted sub-index = weighted_mean(totals, tier_weights)
    |
Feed into daily_health_check aggregate
```

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| Brain topology reader | count, mean_energy, link_count, min_links, cluster_coefficient, drive, recency | value stats, process stats, drives |
| Universe graph reader | moments, first_moment_in_space, distinct_actors, temporal_weight | behavioral stats |
| Daily health algorithm | score per capability | feeds into aggregate + intervention |
| Personhood Ladder | capability definitions | id, tier, description, how_to_verify |

---

## MARKERS

<!-- @mind:escalation The 50/50 split for eth_apply_rules deviates from the standard 40/60. This is a deliberate design decision, not an error. Documented in D1. -->
<!-- @mind:todo Validate all 5 formulas against the 5 synthetic profiles (25 calculations total) -->
<!-- @mind:todo Confirm "value" is the correct node type name in brain graphs -->
<!-- @mind:todo Test that brain-rich-but-inactive profile scores 30-45 (not higher) on all capabilities -->
<!-- @mind:todo Calibrate regularity_score window (30 days proposed — may need adjustment) -->
<!-- @mind:proposition Consider a "values alignment" proxy: do value nodes link to protocol-defined concept nodes? Would add a weak content-adjacent signal without content reading. -->
<!-- @mind:proposition Consider a "moral consistency" meta-score: variance of ethics scores over 30 days — low variance = stable ethics -->
