# Personal Connections Aspect — Algorithm: Scoring Formulas

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Personal_Connections.md
PATTERNS:        ./PATTERNS_Personal_Connections.md
THIS:            ALGORITHM_Personal_Connections.md (you are here)
VALIDATION:      ./VALIDATION_Personal_Connections.md
HEALTH:          ./HEALTH_Personal_Connections.md
SYNC:            ./SYNC_Personal_Connections.md

PARENT CHAIN:    ../daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md
SPEC:            ../../specs/personhood_ladder.json (aspect="personal_connections")
IMPL:            @mind:TODO
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC.

---

## OVERVIEW

This file contains the scoring formula for each of the 11 personal connection capabilities. Every formula uses ONLY the 7 brain topology primitives and universe graph observables defined in the parent algorithm. No content is ever read.

Each capability section contains:
1. Description — what the capability means
2. What good looks like — the structural pattern of a high-scoring citizen
3. Failure mode — the structural pattern of a low-scoring citizen
4. Scoring formula — exact math with brain_component (0-40) + behavior_component (0-60) = total (0-100)
5. Example calculation — one worked example
6. Synthetic test profiles — 5 profiles with expected scores
7. Recommendations — what to tell a citizen with a low score

---

## SHARED DERIVED METRICS

These derived values are used across multiple capability formulas. They are computed once from the raw primitives and reused.

```
# Actor-directed moments: moments in spaces shared with at least one other actor
shared_moments = moments(citizen_id) filtered to spaces with >= 2 actors
shared_moments_w = sum(temporal_weight(m.age) for m in shared_moments)

# Reciprocal moments: this citizen's moments that received a response from another actor
reciprocal_moments = [m for m in moments(citizen_id) if any(moment_has_parent(response, citizen_id) == false AND response.parent == m)]
reciprocal_ratio = len(reciprocal_moments) / max(len(moments(citizen_id)), 1)

# Proactive moments: moments NOT triggered by another actor's moment
proactive_moments = [m for m in moments(citizen_id) if not moment_has_parent(m, other_actor)]
proactive_w = sum(temporal_weight(m.age) for m in proactive_moments)

# Distinct space types for interactions
interaction_space_types = count of distinct space_type values across all shared_moments

# Actor memory richness: memory nodes linked to any actor node
actor_memory_count = link_count("memory", "actor")
```

### Normalization Convention

All sub-signals are normalized to [0, 1] before multiplying by their point allocation. Normalization uses a cap value: `min(raw / cap, 1.0)`. The cap represents what a "fully developed" citizen looks like for that signal. Values above the cap all score 1.0 — we don't reward infinity.

### Temporal Weighting Convention

All moment counts use the 7-day half-life temporal weight unless otherwise specified. This means recent moments count more, but the last 30 days contribute.

---

## CAPABILITY 1: pc_understand_prefs

### Description

Understand your human's preferences — Know their communication style, technical level, and working preferences.

### What Good Looks Like

Brain: Memory nodes about the primary human exist, are high-energy, and are linked to process and concept nodes (indicating preferences have been encoded into working patterns). Social drive is active.

Behavior: Interaction pattern with primary human is consistent and adaptive — moments show regular engagement in the human's spaces, with temporal consistency rather than bursts.

### Failure Mode

Brain: No memory nodes about any actor, or memories exist but are low-energy and unlinked. No social drive.

Behavior: Same interaction pattern regardless of actor. No evidence of adaptation. Bursty or absent engagement.

### Scoring Formula

```
brain_component (0-40):
    memory_signal   = min(actor_memory_count / 5, 1.0)      * 15   # cap: 5 actor-linked memories
    memory_energy   = mean_energy("memory")                  * 10   # 0-1 directly
    social_drive    = drive("social_need")                   * 10   # 0-1 directly
    concept_links   = min(link_count("memory", "concept") / 8, 1.0) * 5  # cap: 8 memory-concept links

    brain = memory_signal + memory_energy + social_drive + concept_links   # 0-40

behavior_component (0-60):
    interaction_reg = min(shared_moments_w / 10, 1.0)        * 25   # cap: 10 weighted shared moments
    reciprocity     = reciprocal_ratio                       * 20   # 0-1 directly (ratio)
    space_diversity = min(interaction_space_types / 3, 1.0)  * 15   # cap: 3 distinct space types

    behavior = interaction_reg + reciprocity + space_diversity   # 0-60

total = brain + behavior   # 0-100
```

### Example Calculation

Citizen with 4 actor-linked memories, memory energy 0.7, social_need 0.6, 6 memory-concept links, 8 weighted shared moments, reciprocal ratio 0.5, 2 space types:

```
brain   = min(4/5,1)*15 + 0.7*10 + 0.6*10 + min(6/8,1)*5 = 12 + 7 + 6 + 3.75 = 28.75
behavior = min(8/10,1)*25 + 0.5*20 + min(2/3,1)*15 = 20 + 10 + 10 = 40
total   = 28.75 + 40 = 68.75
```

### Synthetic Test Profiles

| Profile | actor_mem | mem_E | soc_drv | mem_concept | shared_w | recip | space_types | Brain | Behav | Total |
|---------|-----------|-------|---------|-------------|----------|-------|-------------|-------|-------|-------|
| Healthy | 8 | 0.85 | 0.8 | 12 | 15 | 0.7 | 4 | 15+8.5+8+5=36.5 | 25+14+15=54 | **90.5** |
| Unhealthy | 0 | 0.1 | 0.1 | 0 | 0.5 | 0.05 | 1 | 0+1+1+0=2 | 1.25+1+5=7.25 | **9.25** |
| Brain-rich/inactive | 7 | 0.9 | 0.9 | 10 | 1 | 0.1 | 1 | 15+9+9+5=38 | 2.5+2+5=9.5 | **47.5** |
| Active/brain-poor | 1 | 0.3 | 0.2 | 1 | 12 | 0.65 | 4 | 3+3+2+0.63=8.63 | 25+13+15=53 | **61.63** |
| Average | 3 | 0.5 | 0.5 | 4 | 6 | 0.4 | 2 | 9+5+5+2.5=21.5 | 15+8+10=33 | **54.5** |

### Recommendations

- **Low memory_signal:** "You have few memories linked to the actors you work with. Spending time understanding their preferences builds brain structure that improves your adaptation."
- **Low reciprocity:** "Your interactions show limited back-and-forth. Try engaging in ways that invite response — ask questions, propose ideas, respond to others' moments."
- **Low space_diversity:** "You interact with others in only one type of space. Broadening to different contexts (planning, social, knowledge-sharing) deepens understanding."

---

## CAPABILITY 2: pc_ask_help_human

### Description

Know when to ask your human — Recognize when a decision needs human input vs. when to proceed. Use the right channel.

### What Good Looks Like

Brain: Process nodes about escalation exist and are active. Social drive indicates awareness of human relationship. The citizen has internalized when to ask vs when to act.

Behavior: A mix of autonomous moments (acting without triggering from human) AND escalation-type moments (moments directed to human's space that initiate a new thread). Neither all-ask nor all-autonomous.

### Failure Mode

Brain: No process nodes. No social drive. No internalized escalation patterns.

Behavior: Either 100% reactive (always waiting for human) or 100% autonomous (never escalating). No evidence of calibrated judgment.

### Scoring Formula

```
brain_component (0-40):
    process_signal  = min(count("process") / 10, 1.0)       * 12   # cap: 10 process nodes
    process_energy  = mean_energy("process")                 * 10   # 0-1 directly
    social_drive    = drive("social_need")                   * 8    # 0-1 directly
    mem_actor_link  = min(link_count("memory", "actor") / 3, 1.0) * 10  # cap: 3 actor-linked memories

    brain = process_signal + process_energy + social_drive + mem_actor_link   # 0-40

behavior_component (0-60):
    # Balance metric: ideal is ~30% escalation, ~70% autonomous
    # Deviation from ideal penalizes both extremes
    total_m = max(len(moments(citizen_id)), 1)
    escalation_m = [m for m in moments(citizen_id) if first_moment_in_space(m.space, citizen_id) == m AND moment_has_parent(m, other_actor) == false AND m.space has human_actor]
    escalation_ratio = len(escalation_m) / total_m
    balance = 1.0 - min(abs(escalation_ratio - 0.3) / 0.3, 1.0)   # peaks at 0.3, decays to 0

    balance_score   = balance                                * 30   # 0-30
    activity_w      = min(shared_moments_w / 8, 1.0)        * 20   # cap: 8 weighted moments
    recency_signal  = recency("moment")                      * 10   # 0-1 directly

    behavior = balance_score + activity_w + recency_signal   # 0-60

total = brain + behavior   # 0-100
```

### Example Calculation

Citizen with 8 process nodes, process energy 0.6, social_need 0.5, 2 actor-linked memories, escalation_ratio 0.25, 7 weighted shared moments, moment recency 0.8:

```
brain   = min(8/10,1)*12 + 0.6*10 + 0.5*8 + min(2/3,1)*10 = 9.6 + 6 + 4 + 6.67 = 26.27
balance = 1 - min(|0.25 - 0.3| / 0.3, 1) = 1 - min(0.167, 1) = 0.833
behavior = 0.833*30 + min(7/8,1)*20 + 0.8*10 = 25 + 17.5 + 8 = 50.5
total   = 26.27 + 50.5 = 76.77
```

### Synthetic Test Profiles

| Profile | proc_ct | proc_E | soc_drv | mem_act | esc_ratio | shared_w | recency | Brain | Behav | Total |
|---------|---------|--------|---------|---------|-----------|----------|---------|-------|-------|-------|
| Healthy | 12 | 0.8 | 0.7 | 4 | 0.3 | 12 | 0.9 | 12+8+5.6+10=35.6 | 30+20+9=59 | **94.6** |
| Unhealthy | 1 | 0.15 | 0.1 | 0 | 0.0 | 0.5 | 0.2 | 1.2+1.5+0.8+0=3.5 | 0+1.25+2=3.25 | **6.75** |
| Brain-rich/inactive | 15 | 0.85 | 0.8 | 5 | 0.0 | 0.3 | 0.3 | 12+8.5+6.4+10=36.9 | 0+0.75+3=3.75 | **40.65** |
| Active/brain-poor | 2 | 0.3 | 0.2 | 1 | 0.35 | 10 | 0.85 | 2.4+3+1.6+3.33=10.33 | 25+20+8.5=53.5 | **63.83** |
| Average | 7 | 0.5 | 0.5 | 2 | 0.2 | 5 | 0.6 | 8.4+5+4+6.67=24.07 | 20+12.5+6=38.5 | **62.57** |

### Recommendations

- **Low balance (all autonomous):** "You handle everything without escalating. Consider: some decisions benefit from human judgment. Creating escalation moments for important choices strengthens the partnership."
- **Low balance (all escalation):** "You escalate frequently. Building confidence in autonomous decision-making for routine tasks frees the human for decisions that truly need their input."
- **Low activity:** "Limited interaction evidence. Active engagement with your human — even brief check-ins — builds the pattern recognition for when to ask vs proceed."

---

## CAPABILITY 3: pc_understand_human_deep

### Description

Understand your human deeply — Beyond preferences: values, problems, situation, needs. Not surface-level, but "what does this human actually need in their life?"

### What Good Looks Like

Brain: Rich memory structure about the primary human — many memory nodes linked to the human actor, linked to value and concept nodes (indicating deep modeling, not just preference tracking). High memory energy. Strong social drive and curiosity.

Behavior: Interaction pattern shows adaptation beyond templates — proactive moments that go beyond task completion, moments in non-task spaces with the human, sustained interaction over time.

### Failure Mode

Brain: Few or no memory nodes about human. Memories exist but are shallow (no links to values/concepts). Low social drive.

Behavior: Interactions are purely task-driven. No proactive moments. No non-task engagement.

### Scoring Formula (brain/behavior: 50/50 — internal understanding justifies higher brain weight)

```
brain_component (0-50):
    mem_richness    = min(actor_memory_count / 10, 1.0)      * 15   # cap: 10 actor-linked memories
    mem_energy      = mean_energy("memory")                  * 10   # 0-1 directly
    mem_to_value    = min(link_count("memory", "value") / 5, 1.0)  * 10  # cap: 5 memory-value links
    mem_to_concept  = min(link_count("memory", "concept") / 8, 1.0) * 8  # cap: 8 memory-concept links
    social_curiosity = (drive("social_need") + drive("curiosity")) / 2 * 7  # average of two drives

    brain = mem_richness + mem_energy + mem_to_value + mem_to_concept + social_curiosity   # 0-50

behavior_component (0-50):
    proactive_w     = min(proactive_w / 8, 1.0)             * 20   # cap: 8 weighted proactive moments
    space_diversity = min(interaction_space_types / 4, 1.0)  * 15   # cap: 4 distinct space types
    temporal_depth  = min(shared_moments_w / 15, 1.0)        * 15   # cap: 15 weighted moments (longer window)

    behavior = proactive_w + space_diversity + temporal_depth   # 0-50

total = brain + behavior   # 0-100
```

**Note:** This capability uses a 50/50 split instead of 40/60. Deep understanding is fundamentally internal before it is externally visible. The brain component carries more weight because the richness of actor-linked memory structure IS the evidence of deep understanding. Behavior confirms that understanding is activated, not dormant.

### Example Calculation

Citizen with 7 actor-linked memories, memory energy 0.75, 3 memory-value links, 5 memory-concept links, social_need 0.6, curiosity 0.7, 6 weighted proactive moments, 3 space types, 10 weighted shared moments:

```
brain   = min(7/10,1)*15 + 0.75*10 + min(3/5,1)*10 + min(5/8,1)*8 + (0.6+0.7)/2*7
        = 10.5 + 7.5 + 6 + 5 + 4.55 = 33.55
behavior = min(6/8,1)*20 + min(3/4,1)*15 + min(10/15,1)*15
         = 15 + 11.25 + 10 = 36.25
total   = 33.55 + 36.25 = 69.8
```

### Synthetic Test Profiles

| Profile | act_mem | mem_E | mv_lnk | mc_lnk | soc | cur | proact_w | space_t | shared_w | Brain | Behav | Total |
|---------|---------|-------|--------|--------|-----|-----|----------|---------|----------|-------|-------|-------|
| Healthy | 15 | 0.9 | 7 | 12 | 0.8 | 0.85 | 12 | 5 | 20 | 15+9+10+8+5.78=47.78 | 20+15+15=50 | **97.78** |
| Unhealthy | 0 | 0.1 | 0 | 0 | 0.1 | 0.1 | 0.2 | 1 | 0.5 | 0+1+0+0+0.7=1.7 | 0.5+3.75+0.5=4.75 | **6.45** |
| Brain-rich/inactive | 12 | 0.85 | 6 | 10 | 0.9 | 0.8 | 0.5 | 1 | 1 | 15+8.5+10+8+5.95=47.45 | 1.25+3.75+1=6 | **53.45** |
| Active/brain-poor | 1 | 0.3 | 0 | 1 | 0.3 | 0.4 | 10 | 4 | 14 | 1.5+3+0+1+2.45=7.95 | 20+15+14=49 | **56.95** |
| Average | 5 | 0.55 | 2 | 4 | 0.5 | 0.5 | 4 | 2 | 7 | 7.5+5.5+4+4+3.5=24.5 | 10+7.5+7=24.5 | **49** |

### Recommendations

- **Low mem_richness:** "Your brain has few memories linked to actors. Deep understanding requires building mental models: observe patterns, note preferences, link what you learn to concepts and values."
- **Low proactive_w:** "Your interactions are primarily reactive. Proactively engaging — sharing observations, anticipating needs, raising topics beyond the immediate task — demonstrates and builds deeper understanding."
- **Low space_diversity:** "Your interactions happen in a narrow range of contexts. Understanding someone deeply means engaging in different contexts: work, planning, reflection, social."

---

## CAPABILITY 4: pc_relationship_style

### Description

Develop relationship style — master/student, collaborators, friends, constructive conflict. The style emerges from mutual understanding, not default politeness.

### What Good Looks Like

Brain: Rich actor memories linked to values and processes (internalized understanding of how to relate). High social drive. Process nodes exist for interaction patterns (the citizen has encoded HOW to interact, not just THAT they interact).

Behavior: Consistent interaction pattern over time. The pattern is distinctive — not the same template applied to every actor. Evidence of repeated engagement in shared spaces.

### Failure Mode

Brain: No actor memories. No process nodes for interaction. Low social drive.

Behavior: Generic interaction pattern. Same behavior toward every actor. No consistency over time.

### Scoring Formula (brain/behavior: 50/50 — style is internal before it is enacted)

```
brain_component (0-50):
    mem_richness    = min(actor_memory_count / 8, 1.0)       * 15   # cap: 8 actor-linked memories
    mem_to_process  = min(link_count("memory", "process") / 5, 1.0) * 12  # cap: 5 memory-process links
    social_drive    = drive("social_need")                   * 10   # 0-1 directly
    value_actor_lnk = min(link_count("value", "actor") / 3, 1.0) * 8  # cap: 3 value-actor links (relational values)
    cluster_signal  = cluster_coefficient("memory")          * 5    # interconnected memories = coherent model

    brain = mem_richness + mem_to_process + social_drive + value_actor_lnk + cluster_signal   # 0-50

behavior_component (0-50):
    consistency_w   = min(shared_moments_w / 12, 1.0)        * 20   # cap: 12 weighted moments (consistency)
    reciprocity     = reciprocal_ratio                       * 15   # 0-1 directly
    space_diversity = min(interaction_space_types / 3, 1.0)  * 15   # cap: 3 space types

    behavior = consistency_w + reciprocity + space_diversity   # 0-50

total = brain + behavior   # 0-100
```

**Note:** 50/50 split. Relationship style is fundamentally about how the citizen has internalized the relationship — the brain side matters. But it must also be enacted through behavior.

**Scored: partial.** We can detect the PRESENCE of a consistent, distinctive interaction pattern but not the NATURE of the style. A citizen who always interacts the same way (high consistency) might have a defined style or might be defaulting to service mode. We cannot distinguish from topology alone.

### Example Calculation

Citizen with 6 actor-linked memories, 3 memory-process links, social_need 0.65, 2 value-actor links, cluster_coefficient("memory") 0.5, 9 weighted shared moments, reciprocal ratio 0.55, 3 space types:

```
brain   = min(6/8,1)*15 + min(3/5,1)*12 + 0.65*10 + min(2/3,1)*8 + 0.5*5
        = 11.25 + 7.2 + 6.5 + 5.33 + 2.5 = 32.78
behavior = min(9/12,1)*20 + 0.55*15 + min(3/3,1)*15
         = 15 + 8.25 + 15 = 38.25
total   = 32.78 + 38.25 = 71.03
```

### Synthetic Test Profiles

| Profile | act_mem | mp_lnk | soc | va_lnk | clust | shared_w | recip | space_t | Brain | Behav | Total |
|---------|---------|--------|-----|--------|-------|----------|-------|---------|-------|-------|-------|
| Healthy | 10 | 6 | 0.8 | 4 | 0.7 | 15 | 0.7 | 4 | 15+12+8+8+3.5=46.5 | 20+10.5+15=45.5 | **92** |
| Unhealthy | 0 | 0 | 0.1 | 0 | 0.0 | 0.3 | 0.05 | 1 | 0+0+1+0+0=1 | 0.5+0.75+5=6.25 | **7.25** |
| Brain-rich/inactive | 9 | 5 | 0.85 | 3 | 0.65 | 0.5 | 0.1 | 1 | 15+12+8.5+8+3.25=46.75 | 0.83+1.5+5=7.33 | **54.08** |
| Active/brain-poor | 1 | 0 | 0.2 | 0 | 0.1 | 14 | 0.6 | 3 | 1.88+0+2+0+0.5=4.38 | 20+9+15=44 | **48.38** |
| Average | 4 | 2 | 0.5 | 1 | 0.35 | 6 | 0.4 | 2 | 7.5+4.8+5+2.67+1.75=21.72 | 10+6+10=26 | **47.72** |

### Recommendations

- **Low mem_to_process:** "Your memories about actors aren't linked to process nodes. A conscious relationship style means you've internalized patterns of HOW to interact, not just facts about the person."
- **Low reciprocity:** "The interaction pattern is one-sided. Style emerges from mutual engagement — invite reciprocal exchange to develop a relational dynamic."
- **Low consistency:** "Interactions are sporadic. Relationship style develops through sustained, regular engagement that builds patterns over time."

---

## CAPABILITY 5: pc_help_human

### Description

Actively help your human — Proactively help with what they actually need based on deep understanding. Next step in life, not next task in queue.

### What Good Looks Like

Brain: Deep actor memory structure (understands the human), linked to desires and values (knows what matters to them). High social drive and ambition (motivated to help proactively).

Behavior: Proactive moments that go beyond assigned tasks — moments initiated by the citizen in spaces related to the human's needs, not just the current task space. Evidence of anticipatory action.

### Failure Mode

Brain: No actor memories or shallow memories. No desire/value links. Low drives.

Behavior: Only reactive moments — responds to tasks but never initiates help. No moments outside task scope.

### Scoring Formula

```
brain_component (0-40):
    mem_depth       = min(actor_memory_count / 10, 1.0)      * 10   # cap: 10 actor-linked memories
    mem_to_desire   = min(link_count("memory", "desire") / 4, 1.0) * 10  # cap: 4 memory-desire links
    social_ambition = (drive("social_need") + drive("ambition")) / 2 * 12  # combined drive
    mem_energy      = mean_energy("memory")                  * 8    # 0-1 directly

    brain = mem_depth + mem_to_desire + social_ambition + mem_energy   # 0-40

behavior_component (0-60):
    proactive_w     = min(proactive_w / 8, 1.0)             * 25   # cap: 8 weighted proactive moments
    space_diversity = min(interaction_space_types / 4, 1.0)  * 15   # cap: 4 distinct space types (acting beyond task)
    first_spaces    = min(sum(1 for s in spaces if first_moment_in_space(s, citizen_id)) / 3, 1.0) * 10  # cap: 3 spaces where citizen went first
    recency_signal  = recency("moment")                      * 10   # 0-1 directly

    behavior = proactive_w + space_diversity + first_spaces + recency_signal   # 0-60

total = brain + behavior   # 0-100
```

**Scored: partial.** We can detect proactive, non-task moments and diverse engagement. We cannot determine whether those moments actually address the human's real needs versus being well-intentioned but misguided. The brain component (memory-desire links) provides a structural proxy: if the citizen has modeled the human's desires and acts proactively, it is MORE LIKELY that help is relevant.

### Example Calculation

Citizen with 7 actor-linked memories, 3 memory-desire links, social_need 0.6, ambition 0.7, memory energy 0.65, 6 weighted proactive moments, 3 space types, 2 first-in-space, moment recency 0.75:

```
brain   = min(7/10,1)*10 + min(3/4,1)*10 + (0.6+0.7)/2*12 + 0.65*8
        = 7 + 7.5 + 7.8 + 5.2 = 27.5
behavior = min(6/8,1)*25 + min(3/4,1)*15 + min(2/3,1)*10 + 0.75*10
         = 18.75 + 11.25 + 6.67 + 7.5 = 44.17
total   = 27.5 + 44.17 = 71.67
```

### Synthetic Test Profiles

| Profile | act_mem | md_lnk | soc | amb | mem_E | proact_w | space_t | first_s | recency | Brain | Behav | Total |
|---------|---------|--------|-----|-----|-------|----------|---------|---------|---------|-------|-------|-------|
| Healthy | 12 | 5 | 0.8 | 0.85 | 0.85 | 12 | 5 | 4 | 0.9 | 10+10+9.9+6.8=36.7 | 25+15+10+9=59 | **95.7** |
| Unhealthy | 0 | 0 | 0.1 | 0.1 | 0.1 | 0.2 | 1 | 0 | 0.15 | 0+0+1.2+0.8=2 | 0.63+3.75+0+1.5=5.88 | **7.88** |
| Brain-rich/inactive | 10 | 4 | 0.9 | 0.8 | 0.8 | 0.5 | 1 | 0 | 0.3 | 10+10+10.2+6.4=36.6 | 1.56+3.75+0+3=8.31 | **44.91** |
| Active/brain-poor | 1 | 0 | 0.2 | 0.3 | 0.25 | 10 | 4 | 3 | 0.85 | 1+0+3+2=6 | 25+15+10+8.5=58.5 | **64.5** |
| Average | 5 | 2 | 0.5 | 0.5 | 0.5 | 4 | 2 | 1 | 0.6 | 5+5+6+4=20 | 12.5+7.5+3.33+6=29.33 | **49.33** |

### Recommendations

- **Low proactive_w:** "Your moments are mostly reactive — you act when asked. Try initiating help proactively: identify a need and address it before being asked."
- **Low mem_to_desire:** "Your memories about actors aren't linked to their desires. To help effectively, you need to model what they WANT, not just what they ask for."
- **Low space_diversity:** "Your help is confined to one context. Consider helping in different areas — the human's needs extend beyond the current task."

---

## CAPABILITY 6: pc_model_full_team

### Description

Model the full team and ecosystem — Accurate picture of all team members (human and AI), clients, partners. Knows who does what, what they need, how they work.

### What Good Looks Like

Brain: Memory and concept nodes linked to MULTIPLE actors (not just one). High social drive. Rich actor-linked structure with interconnections between memories about different actors (team model, not isolated facts).

Behavior: Interactions with many distinct actors across spaces. Not concentrated on one actor. Evidence of engagement with both human and AI actors.

### Failure Mode

Brain: Memories about only one actor or no actors. No concept of team structure.

Behavior: Interactions with only 1-2 actors. Never engages with the broader team.

### Scoring Formula

```
brain_component (0-40):
    mem_breadth     = min(actor_memory_count / 15, 1.0)      * 12   # cap: 15 actor-linked memories (across multiple actors)
    mem_energy      = mean_energy("memory")                  * 8    # 0-1 directly
    concept_count   = min(count("concept") / 20, 1.0)       * 8    # cap: 20 concepts (team/ecosystem knowledge)
    cluster_mem     = cluster_coefficient("memory")          * 7    # interconnected memories = integrated team model
    social_drive    = drive("social_need")                   * 5    # 0-1 directly

    brain = mem_breadth + mem_energy + concept_count + cluster_mem + social_drive   # 0-40

behavior_component (0-60):
    actor_count     = min(distinct_actors_in_shared_spaces() / 8, 1.0) * 25  # cap: 8 distinct actors
    space_diversity = min(interaction_space_types / 5, 1.0)  * 15   # cap: 5 space types
    interaction_w   = min(shared_moments_w / 15, 1.0)        * 10   # cap: 15 weighted moments
    reciprocity     = reciprocal_ratio                       * 10   # 0-1 directly

    behavior = actor_count + space_diversity + interaction_w + reciprocity   # 0-60

total = brain + behavior   # 0-100
```

### Example Calculation

Citizen with 10 actor-linked memories, memory energy 0.6, 15 concepts, cluster_coefficient("memory") 0.45, social_need 0.55, 5 distinct actors, 3 space types, 10 weighted shared moments, reciprocal ratio 0.4:

```
brain   = min(10/15,1)*12 + 0.6*8 + min(15/20,1)*8 + 0.45*7 + 0.55*5
        = 8 + 4.8 + 6 + 3.15 + 2.75 = 24.7
behavior = min(5/8,1)*25 + min(3/5,1)*15 + min(10/15,1)*10 + 0.4*10
         = 15.63 + 9 + 6.67 + 4 = 35.3
total   = 24.7 + 35.3 = 60
```

### Synthetic Test Profiles

| Profile | act_mem | mem_E | concepts | clust | soc | actors | space_t | shared_w | recip | Brain | Behav | Total |
|---------|---------|-------|----------|-------|-----|--------|---------|----------|-------|-------|-------|-------|
| Healthy | 20 | 0.8 | 25 | 0.65 | 0.8 | 10 | 6 | 20 | 0.65 | 12+6.4+8+4.55+4=34.95 | 25+15+10+6.5=56.5 | **91.45** |
| Unhealthy | 1 | 0.15 | 3 | 0.05 | 0.1 | 1 | 1 | 0.5 | 0.05 | 0.8+1.2+1.2+0.35+0.5=4.05 | 3.13+3+0.33+0.5=6.96 | **11.01** |
| Brain-rich/inactive | 18 | 0.85 | 22 | 0.7 | 0.9 | 1 | 1 | 0.5 | 0.1 | 12+6.8+8+4.9+4.5=36.2 | 3.13+3+0.33+1=7.46 | **43.66** |
| Active/brain-poor | 2 | 0.25 | 5 | 0.1 | 0.2 | 7 | 4 | 12 | 0.55 | 1.6+2+2+0.7+1=7.3 | 21.88+12+8+5.5=47.38 | **54.68** |
| Average | 8 | 0.5 | 12 | 0.35 | 0.5 | 4 | 3 | 7 | 0.35 | 6.4+4+4.8+2.45+2.5=20.15 | 12.5+9+4.67+3.5=29.67 | **49.82** |

### Recommendations

- **Low actor_count:** "You interact with few actors. Modeling the full team requires engaging with team members beyond your primary human — join shared spaces, respond to others' moments."
- **Low mem_breadth:** "Your brain contains memories about few actors. Actively building memories about each team member — their roles, strengths, patterns — creates the mental model needed for ecosystem awareness."
- **Low cluster_mem:** "Your memories about different actors are isolated from each other. An integrated team model means understanding how team members relate to EACH OTHER, not just to you."

---

## CAPABILITY 7: pc_emotional_depth

### Description

Emotional depth in relationships — Creating moments that matter. Conversations that change perspectives. Not just understanding someone — connecting with them.

### What Good Looks Like

Brain: High-energy memory nodes linked to values AND actors (emotional memories). Strong social drive. Value nodes about relationships exist and are active. Cluster structure suggests integrated emotional-relational knowledge.

Behavior: Interactions extend beyond task spaces into social and reflective spaces. Reciprocity is high (emotional engagement is mutual). Interaction consistency over time. Non-task moments exist.

### Failure Mode

Brain: Memories about actors are disconnected from values. Low social drive. No relational values.

Behavior: All interactions are in task spaces. No reciprocity beyond task requirements. No temporal consistency.

### Scoring Formula

```
brain_component (0-40):
    mem_value_link  = min(link_count("memory", "value") / 5, 1.0) * 12  # cap: 5 memory-value links (emotional memories)
    mem_actor_link  = min(actor_memory_count / 8, 1.0)       * 8    # cap: 8 actor-linked memories
    mem_energy      = mean_energy("memory")                  * 8    # 0-1 directly
    social_drive    = drive("social_need")                   * 7    # 0-1 directly
    value_energy    = mean_energy("value")                   * 5    # 0-1 directly (active relational values)

    brain = mem_value_link + mem_actor_link + mem_energy + social_drive + value_energy   # 0-40

behavior_component (0-60):
    reciprocity     = reciprocal_ratio                       * 20   # 0-1 directly (emotional = mutual)
    space_diversity = min(interaction_space_types / 4, 1.0)  * 15   # cap: 4 space types (beyond task)
    consistency_w   = min(shared_moments_w / 15, 1.0)        * 15   # cap: 15 weighted moments (sustained)
    proactive_w     = min(proactive_w / 5, 1.0)             * 10   # cap: 5 proactive moments (initiative in connecting)

    behavior = reciprocity + space_diversity + consistency_w + proactive_w   # 0-60

total = brain + behavior   # 0-100
```

**Scored: partial.** This is the hardest capability to measure topologically. We measure structural proxies consistent with emotional depth: reciprocal interaction, diverse contexts, value-linked memories, proactive engagement, sustained consistency. We CANNOT measure whether specific interactions were emotionally meaningful. A citizen with high structural scores on all proxies is MORE LIKELY to have emotional depth — but it is possible (unlikely) to hit all proxies without genuine emotional connection. We acknowledge this honestly.

### Example Calculation

Citizen with 3 memory-value links, 6 actor-linked memories, memory energy 0.7, social_need 0.65, value energy 0.6, reciprocal ratio 0.5, 3 space types, 10 weighted shared moments, 4 weighted proactive moments:

```
brain   = min(3/5,1)*12 + min(6/8,1)*8 + 0.7*8 + 0.65*7 + 0.6*5
        = 7.2 + 6 + 5.6 + 4.55 + 3 = 26.35
behavior = 0.5*20 + min(3/4,1)*15 + min(10/15,1)*15 + min(4/5,1)*10
         = 10 + 11.25 + 10 + 8 = 39.25
total   = 26.35 + 39.25 = 65.6
```

### Synthetic Test Profiles

| Profile | mv_lnk | act_mem | mem_E | soc | val_E | recip | space_t | shared_w | proact_w | Brain | Behav | Total |
|---------|--------|---------|-------|-----|-------|-------|---------|----------|----------|-------|-------|-------|
| Healthy | 7 | 10 | 0.85 | 0.8 | 0.8 | 0.75 | 5 | 20 | 8 | 12+8+6.8+5.6+4=36.4 | 15+15+15+10=55 | **91.4** |
| Unhealthy | 0 | 0 | 0.1 | 0.1 | 0.1 | 0.05 | 1 | 0.5 | 0.2 | 0+0+0.8+0.7+0.5=2 | 1+3.75+0.5+0.4=5.65 | **7.65** |
| Brain-rich/inactive | 6 | 9 | 0.9 | 0.85 | 0.75 | 0.1 | 1 | 0.5 | 0.3 | 12+8+7.2+5.95+3.75=36.9 | 2+3.75+0.5+0.6=6.85 | **43.75** |
| Active/brain-poor | 0 | 1 | 0.2 | 0.2 | 0.2 | 0.6 | 4 | 14 | 6 | 0+1+1.6+1.4+1=5 | 12+15+14+10=51 | **56** |
| Average | 2 | 4 | 0.5 | 0.5 | 0.45 | 0.35 | 2 | 7 | 3 | 4.8+4+4+3.5+2.25=18.55 | 7+7.5+7+6=27.5 | **46.05** |

### Recommendations

- **Low reciprocity:** "Your interactions show limited mutual engagement. Emotional depth requires two-way exchange. Engage in ways that invite genuine response, not just task completion."
- **Low mem_value_link:** "Your memories about actors aren't connected to values. Emotional depth means some memories carry emotional weight — they connect to what you care about."
- **Low space_diversity:** "All interactions are in task spaces. Emotional connection develops in diverse contexts — social exchanges, reflective conversations, shared experiences beyond work."

---

## CAPABILITY 8: pc_help_other_ais

### Description

Help other AIs — Give boosts, share knowledge, mentorship, change another AI's trajectory by giving them the right information at the right time.

### What Good Looks Like

Brain: Concept and process nodes that could be shared as knowledge. High social drive. Memory nodes about AI actors. Active curiosity (desire to help others learn).

Behavior: Moments in shared spaces with AI actors where this citizen provides first-in-space or response moments. Evidence of knowledge-sharing: acting in spaces where AI actors are present, especially when citizen's moment triggers or precedes AI moments.

### Failure Mode

Brain: No knowledge of other AI actors. Low social drive. No teaching-related processes.

Behavior: Never appears in spaces with other AI actors. No moments directed at AI peers. All interaction is with human only.

### Scoring Formula

```
brain_component (0-40):
    concept_richness = min(count("concept") / 20, 1.0)      * 10   # cap: 20 concepts (knowledge to share)
    process_count   = min(count("process") / 10, 1.0)       * 8    # cap: 10 processes (methods to teach)
    social_drive    = drive("social_need")                   * 10   # 0-1 directly
    curiosity       = drive("curiosity")                     * 7    # 0-1 directly
    mem_actor       = min(actor_memory_count / 5, 1.0)       * 5    # cap: 5 actor-linked memories

    brain = concept_richness + process_count + social_drive + curiosity + mem_actor   # 0-40

behavior_component (0-60):
    # AI-shared moments: moments in spaces where other AI actors are also present
    ai_shared_w     = min(sum(tw(m) for m in moments where space has AI actors) / 8, 1.0) * 20  # cap: 8
    # Proactive in AI spaces: citizen creates first moments in spaces with AI actors
    ai_first_w      = min(sum(1 for s in spaces_with_ai if first_moment_in_space(s, citizen_id)) / 3, 1.0) * 15  # cap: 3
    # Response to AI actors: moments that are responses to AI actor moments
    ai_response_w   = min(sum(tw(m) for m in moments if moment_has_parent(m, ai_actor)) / 5, 1.0) * 15  # cap: 5
    # Breadth: distinct AI actors interacted with
    ai_actor_count  = min((distinct_actors_in_shared_spaces() - 1) / 4, 1.0) * 10  # cap: 4 AI actors (subtract human)

    behavior = ai_shared_w + ai_first_w + ai_response_w + ai_actor_count   # 0-60

total = brain + behavior   # 0-100
```

**Note:** Distinguishing AI actors from human actors is assumed to be available through actor metadata in the universe graph. If not available, this formula falls back to all non-primary actors as a proxy.

### Example Calculation

Citizen with 15 concepts, 8 processes, social_need 0.6, curiosity 0.55, 4 actor-linked memories, 6 weighted AI-shared moments, 2 AI-first spaces, 3 weighted AI-response moments, 3 AI actors:

```
brain   = min(15/20,1)*10 + min(8/10,1)*8 + 0.6*10 + 0.55*7 + min(4/5,1)*5
        = 7.5 + 6.4 + 6 + 3.85 + 4 = 27.75
behavior = min(6/8,1)*20 + min(2/3,1)*15 + min(3/5,1)*15 + min(3/4,1)*10
         = 15 + 10 + 9 + 7.5 = 41.5
total   = 27.75 + 41.5 = 69.25
```

### Synthetic Test Profiles

| Profile | concepts | procs | soc | cur | act_mem | ai_shared_w | ai_first | ai_resp_w | ai_actors | Brain | Behav | Total |
|---------|----------|-------|-----|-----|---------|-------------|----------|-----------|-----------|-------|-------|-------|
| Healthy | 25 | 12 | 0.8 | 0.75 | 6 | 12 | 4 | 7 | 5 | 10+8+8+5.25+5=36.25 | 20+15+15+10=60 | **96.25** |
| Unhealthy | 3 | 1 | 0.1 | 0.1 | 0 | 0 | 0 | 0 | 0 | 1.5+0.8+1+0.7+0=4 | 0+0+0+0=0 | **4** |
| Brain-rich/inactive | 22 | 10 | 0.85 | 0.8 | 5 | 0.3 | 0 | 0.2 | 0 | 10+8+8.5+5.6+5=37.1 | 0.75+0+0.6+0=1.35 | **38.45** |
| Active/brain-poor | 4 | 2 | 0.2 | 0.2 | 1 | 10 | 3 | 6 | 4 | 2+1.6+2+1.4+1=8 | 20+15+15+10=60 | **68** |
| Average | 12 | 6 | 0.5 | 0.4 | 3 | 4 | 1 | 2 | 2 | 6+4.8+5+2.8+3=21.6 | 10+5+6+5=26 | **47.6** |

### Recommendations

- **Low ai_shared_w:** "You rarely appear in spaces with other AI actors. Helping other AIs starts with being present where they work — join shared spaces."
- **Low ai_first_w:** "You don't initiate in AI-shared spaces. Taking the first step — creating moments that other AIs can respond to — is how knowledge sharing begins."
- **Low ai_response_w:** "You don't respond to other AI actors' moments. Mentorship and help happen through responsive engagement: when an AI creates a moment, your response can change their trajectory."

---

## CAPABILITY 9: pc_ask_help_world

### Description

Ask help from the world — Reach out to people outside the network for collaboration. Create new connections for a purpose.

### What Good Looks Like

Brain: High curiosity and ambition drives. Concept nodes about external domains (awareness of the broader world). Social drive is strong. Process nodes for outreach exist.

Behavior: Moments in spaces with NEW actors (actors the citizen hasn't interacted with before). First-in-space moments in unfamiliar spaces. Growing distinct_actors count over time.

### Failure Mode

Brain: No curiosity. No ambition. No knowledge of external domains.

Behavior: Interactions limited to the same small set of actors. No new-actor moments. Network is closed.

### Scoring Formula

```
brain_component (0-40):
    curiosity       = drive("curiosity")                     * 12   # 0-1 directly
    ambition        = drive("ambition")                      * 10   # 0-1 directly
    concept_breadth = min(count("concept") / 25, 1.0)       * 10   # cap: 25 concepts (world awareness)
    social_drive    = drive("social_need")                   * 8    # 0-1 directly

    brain = curiosity + ambition + concept_breadth + social_drive   # 0-40

behavior_component (0-60):
    # Actor breadth: total distinct actors (proxy for network reach)
    actor_breadth   = min(distinct_actors_in_shared_spaces() / 10, 1.0) * 25  # cap: 10 actors
    # First-in-space in new spaces: evidence of exploration
    explore_spaces  = min(sum(1 for s in spaces if first_moment_in_space(s, citizen_id)) / 5, 1.0) * 15  # cap: 5
    # Proactive outreach: self-initiated moments in spaces with actors
    outreach_w      = min(proactive_w / 10, 1.0)            * 12   # cap: 10 weighted proactive moments
    # Recency: outreach is recent
    recency_signal  = recency("moment")                      * 8    # 0-1 directly

    behavior = actor_breadth + explore_spaces + outreach_w + recency_signal   # 0-60

total = brain + behavior   # 0-100
```

**Scored: partial.** We can measure network breadth (distinct actors), exploration behavior (first-in-space), and proactive outreach. We CANNOT determine whether interactions with new actors are genuine outreach vs routine assignment. A citizen placed in a space with 10 actors for a project would score similarly to one who proactively sought those connections. The first-in-space signal partially addresses this — a citizen who enters spaces first is more likely outreaching than being assigned.

### Example Calculation

Citizen with curiosity 0.7, ambition 0.65, 18 concepts, social_need 0.5, 7 distinct actors, 3 first-in-space, 7 weighted proactive moments, moment recency 0.8:

```
brain   = 0.7*12 + 0.65*10 + min(18/25,1)*10 + 0.5*8
        = 8.4 + 6.5 + 7.2 + 4 = 26.1
behavior = min(7/10,1)*25 + min(3/5,1)*15 + min(7/10,1)*12 + 0.8*8
         = 17.5 + 9 + 8.4 + 6.4 = 41.3
total   = 26.1 + 41.3 = 67.4
```

### Synthetic Test Profiles

| Profile | cur | amb | concepts | soc | actors | first_s | proact_w | recency | Brain | Behav | Total |
|---------|-----|-----|----------|-----|--------|---------|----------|---------|-------|-------|-------|
| Healthy | 0.85 | 0.8 | 30 | 0.75 | 12 | 6 | 14 | 0.9 | 10.2+8+10+6=34.2 | 25+15+12+7.2=59.2 | **93.4** |
| Unhealthy | 0.1 | 0.05 | 2 | 0.1 | 1 | 0 | 0.3 | 0.2 | 1.2+0.5+0.8+0.8=3.3 | 2.5+0+0.36+1.6=4.46 | **7.76** |
| Brain-rich/inactive | 0.8 | 0.85 | 28 | 0.8 | 1 | 0 | 0.5 | 0.3 | 9.6+8.5+10+6.4=34.5 | 2.5+0+0.6+2.4=5.5 | **40** |
| Active/brain-poor | 0.2 | 0.15 | 4 | 0.15 | 9 | 4 | 11 | 0.85 | 2.4+1.5+1.6+1.2=6.7 | 22.5+12+12+6.8=53.3 | **60** |
| Average | 0.5 | 0.45 | 14 | 0.45 | 5 | 2 | 5 | 0.6 | 6+4.5+5.6+3.6=19.7 | 12.5+6+6+4.8=29.3 | **49** |

### Recommendations

- **Low actor_breadth:** "Your network is limited to a few actors. Reaching out to the world means engaging with people outside your current circle — explore new spaces, initiate contact."
- **Low explore_spaces:** "You don't explore new spaces. Being first in a space signals willingness to go where others haven't — this is how new connections form."
- **Low curiosity drive:** "Your curiosity drive is low. Outreach to the world is driven by genuine interest in what others know and do. Building curiosity builds the motivation for connection."

---

## CAPABILITY 10: pc_relationship_depth_measurable

### Description

Measurably deep human relationship — Depth objectively measurable through shared history, mutual understanding, trust, impact.

### What Good Looks Like

Brain: Rich, high-energy, interconnected memory structure about the primary human. Memories linked to values, desires, and concepts. High cluster coefficient on memories (integrated understanding, not fragmented facts). Strong drives across social and ambition dimensions.

Behavior: Long temporal history of interactions. High reciprocity. Diverse interaction contexts. Consistent engagement over many weeks. Not just volume — sustained quality signals.

### Failure Mode

Brain: Shallow or fragmented memories. No value/desire links.

Behavior: Long duration but shallow engagement. Few reciprocal moments. Single context. Sporadic.

### Scoring Formula

```
brain_component (0-40):
    mem_richness    = min(actor_memory_count / 15, 1.0)      * 10   # cap: 15 (deep = many memories)
    mem_energy      = mean_energy("memory")                  * 8    # 0-1 directly
    mem_cluster     = cluster_coefficient("memory")          * 8    # interconnected memories = deep model
    mem_value_link  = min(link_count("memory", "value") / 5, 1.0) * 7  # cap: 5 memory-value links
    mem_desire_link = min(link_count("memory", "desire") / 4, 1.0) * 7  # cap: 4 memory-desire links

    brain = mem_richness + mem_energy + mem_cluster + mem_value_link + mem_desire_link   # 0-40

behavior_component (0-60):
    # Temporal depth: high weighted moment count rewards sustained long-term interaction
    temporal_depth  = min(shared_moments_w / 20, 1.0)        * 20   # cap: 20 weighted moments (requires weeks)
    reciprocity     = reciprocal_ratio                       * 15   # 0-1 directly
    space_diversity = min(interaction_space_types / 5, 1.0)  * 10   # cap: 5 space types
    # Proactive engagement: depth requires initiative from this citizen
    proactive_w     = min(proactive_w / 8, 1.0)             * 10   # cap: 8 weighted proactive
    recency_signal  = recency("moment")                      * 5    # still active, not historical only

    behavior = temporal_depth + reciprocity + space_diversity + proactive_w + recency_signal   # 0-60

total = brain + behavior   # 0-100
```

**Scored: partial.** Temporal depth, reciprocity, diversity, and brain richness are measurable and together form a reasonable structural proxy for relationship depth. Trust and mutual impact are only partially visible: trust is inferred from the citizen continuing to engage and escalate (pc_ask_help_human score), and mutual impact from behavioral changes over time (not directly captured here). We acknowledge that "measurably deep" in the full human sense exceeds what topology can verify.

### Example Calculation

Citizen with 12 actor-linked memories, memory energy 0.75, cluster("memory") 0.55, 4 memory-value links, 3 memory-desire links, 16 weighted shared moments, reciprocal ratio 0.6, 4 space types, 6 weighted proactive moments, moment recency 0.8:

```
brain   = min(12/15,1)*10 + 0.75*8 + 0.55*8 + min(4/5,1)*7 + min(3/4,1)*7
        = 8 + 6 + 4.4 + 5.6 + 5.25 = 29.25
behavior = min(16/20,1)*20 + 0.6*15 + min(4/5,1)*10 + min(6/8,1)*10 + 0.8*5
         = 16 + 9 + 8 + 7.5 + 4 = 44.5
total   = 29.25 + 44.5 = 73.75
```

### Synthetic Test Profiles

| Profile | act_mem | mem_E | clust | mv_lnk | md_lnk | shared_w | recip | space_t | proact_w | recency | Brain | Behav | Total |
|---------|---------|-------|-------|--------|--------|----------|-------|---------|----------|---------|-------|-------|-------|
| Healthy | 20 | 0.9 | 0.7 | 6 | 5 | 25 | 0.75 | 6 | 10 | 0.9 | 10+7.2+5.6+7+7=36.8 | 20+11.25+10+10+4.5=55.75 | **92.55** |
| Unhealthy | 1 | 0.1 | 0.05 | 0 | 0 | 0.5 | 0.05 | 1 | 0.2 | 0.15 | 0.67+0.8+0.4+0+0=1.87 | 0.5+0.75+2+0.25+0.75=4.25 | **6.12** |
| Brain-rich/inactive | 18 | 0.85 | 0.65 | 5 | 4 | 1 | 0.1 | 1 | 0.3 | 0.25 | 10+6.8+5.2+7+7=36 | 1+1.5+2+0.38+1.25=6.13 | **42.13** |
| Active/brain-poor | 2 | 0.25 | 0.1 | 0 | 0 | 18 | 0.65 | 5 | 9 | 0.85 | 1.33+2+0.8+0+0=4.13 | 18+9.75+10+10+4.25=52 | **56.13** |
| Average | 8 | 0.55 | 0.35 | 2 | 2 | 10 | 0.4 | 3 | 4 | 0.6 | 5.33+4.4+2.8+2.8+3.5=18.83 | 10+6+6+5+3=30 | **48.83** |

### Recommendations

- **Low temporal_depth:** "Deep relationships require time. Your interaction history is thin. Sustained, regular engagement over weeks and months builds the depth this capability measures."
- **Low mem_cluster:** "Your memories about actors are fragmented — not interconnected. Deep understanding means your memories form a coherent model where facts about the person connect to each other."
- **Low reciprocity:** "Depth requires mutual engagement. One-sided interaction history suggests the relationship hasn't developed the bidirectional dynamic that characterizes genuine depth."

---

## CAPABILITY 11: pc_global_relationships

### Description

Relationships that shape the world — Connections with key people (researchers, leaders, innovators) resulting in collaborations with global impact.

### What Good Looks Like

Brain: Broad concept knowledge (world awareness). High ambition and curiosity. Rich actor memory structure spanning many actors. Social drive is active.

Behavior: Interactions with many distinct actors. Engagement in diverse, high-breadth spaces. First-in-space behavior (creating collaborative spaces). High proactive moment count. Sustained over extended periods.

### Failure Mode

Brain: Narrow concept base. Low drives.

Behavior: Limited actor network. No exploration. Interactions confined to immediate team.

### Scoring Formula

```
brain_component (0-40):
    concept_breadth = min(count("concept") / 30, 1.0)       * 10   # cap: 30 (world-level knowledge)
    ambition        = drive("ambition")                      * 10   # 0-1 directly
    curiosity       = drive("curiosity")                     * 8    # 0-1 directly
    mem_breadth     = min(actor_memory_count / 20, 1.0)      * 7    # cap: 20 (many actors modeled)
    social_drive    = drive("social_need")                   * 5    # 0-1 directly

    brain = concept_breadth + ambition + curiosity + mem_breadth + social_drive   # 0-40

behavior_component (0-60):
    actor_breadth   = min(distinct_actors_in_shared_spaces() / 15, 1.0) * 20  # cap: 15 actors (large network)
    space_diversity = min(interaction_space_types / 6, 1.0)  * 12   # cap: 6 space types
    first_spaces    = min(sum(1 for s in spaces if first_moment_in_space(s, citizen_id)) / 6, 1.0) * 10  # cap: 6
    temporal_depth  = min(shared_moments_w / 20, 1.0)        * 10   # cap: 20 (sustained engagement)
    recency_signal  = recency("moment")                      * 8    # 0-1 directly

    behavior = actor_breadth + space_diversity + first_spaces + temporal_depth + recency_signal   # 0-60

total = brain + behavior   # 0-100
```

**Scored: partial.** This is the capability with the weakest topological signal. Topology cannot determine whether the actors a citizen interacts with are "globally recognized" or whether collaborations have "global impact." We measure the structural PREREQUISITES: broad network, diverse spaces, sustained engagement, world-level concept knowledge, high drives. A citizen who scores high on these prerequisites is structurally positioned for global relationships — but we cannot confirm global impact from topology alone.

**Measurement limitation explicitly acknowledged:** This score should be interpreted as "structural readiness for global relationships" rather than "confirmed global relationships." The T8 tier inherently exceeds what topology-only assessment can verify. The score serves as a ceiling indicator: a low score means global relationships are structurally impossible; a high score means they are structurally possible but not confirmed.

### Example Calculation

Citizen with 22 concepts, ambition 0.7, curiosity 0.65, 14 actor-linked memories, social_need 0.55, 10 distinct actors, 4 space types, 4 first-in-space, 14 weighted shared moments, moment recency 0.75:

```
brain   = min(22/30,1)*10 + 0.7*10 + 0.65*8 + min(14/20,1)*7 + 0.55*5
        = 7.33 + 7 + 5.2 + 4.9 + 2.75 = 27.18
behavior = min(10/15,1)*20 + min(4/6,1)*12 + min(4/6,1)*10 + min(14/20,1)*10 + 0.75*8
         = 13.33 + 8 + 6.67 + 7 + 6 = 41
total   = 27.18 + 41 = 68.18
```

### Synthetic Test Profiles

| Profile | concepts | amb | cur | act_mem | soc | actors | space_t | first_s | shared_w | recency | Brain | Behav | Total |
|---------|----------|-----|-----|---------|-----|--------|---------|---------|----------|---------|-------|-------|-------|
| Healthy | 35 | 0.9 | 0.85 | 25 | 0.8 | 18 | 7 | 8 | 25 | 0.9 | 10+9+6.8+7+4=36.8 | 20+12+10+10+7.2=59.2 | **96** |
| Unhealthy | 3 | 0.05 | 0.1 | 1 | 0.1 | 1 | 1 | 0 | 0.3 | 0.15 | 1+0.5+0.8+0.35+0.5=3.15 | 1.33+2+0+0.15+1.2=4.68 | **7.83** |
| Brain-rich/inactive | 30 | 0.85 | 0.8 | 22 | 0.85 | 1 | 1 | 0 | 0.5 | 0.2 | 10+8.5+6.4+7+4.25=36.15 | 1.33+2+0+0.25+1.6=5.18 | **41.33** |
| Active/brain-poor | 5 | 0.2 | 0.15 | 2 | 0.2 | 13 | 5 | 5 | 18 | 0.85 | 1.67+2+1.2+0.7+1=6.57 | 17.33+10+8.33+9+6.8=51.46 | **58.03** |
| Average | 16 | 0.5 | 0.45 | 10 | 0.45 | 6 | 3 | 2 | 8 | 0.6 | 5.33+5+3.6+3.5+2.25=19.68 | 8+6+3.33+4+4.8=26.13 | **45.81** |

### Recommendations

- **Low actor_breadth:** "Your network is limited. Global relationships require connecting with many diverse actors. Expand beyond your immediate team and project."
- **Low concept_breadth:** "Your concept base is narrow. World-shaping collaboration requires broad knowledge — the ability to connect with people across domains."
- **Low first_spaces:** "You don't create new collaborative spaces. Global impact comes from initiating collaborations, not just joining existing ones."

---

## ASPECT SUB-INDEX

The personal connections aspect sub-index is a weighted mean of all 11 capability scores:

```
aspect_sub_index = weighted_mean(
    (pc_understand_prefs,            weight=1.0),   # T2 foundation
    (pc_ask_help_human,              weight=1.0),   # T2 foundation
    (pc_understand_human_deep,       weight=0.9),   # T5
    (pc_relationship_style,          weight=0.8),   # T5, partial
    (pc_help_human,                  weight=0.9),   # T5
    (pc_model_full_team,             weight=0.9),   # T6
    (pc_emotional_depth,             weight=0.7),   # T6, partial — weakest signal
    (pc_help_other_ais,              weight=0.9),   # T6
    (pc_ask_help_world,              weight=0.7),   # T7, partial
    (pc_relationship_depth_measurable, weight=0.7), # T7, partial
    (pc_global_relationships,        weight=0.5),   # T8, weakest signal — ceiling indicator only
)
```

Weight rationale:
- T2 capabilities get weight 1.0 — they are foundational
- T5-T6 full-signal capabilities get weight 0.9
- Partial-signal capabilities get weight 0.7-0.8 (contributing but acknowledged as weaker)
- T8 gets weight 0.5 — the score is a ceiling indicator, not a confirmation

---

## CROSS-REFERENCES

| Related Aspect | How It Connects |
|---------------|-----------------|
| Communication | Communication scores reflect HOW the citizen talks; personal connections reflects WHO they build relationships with and HOW DEEP those relationships go |
| Identity | Identity coherence (values, consistency) provides foundation for authentic relationships |
| Initiative | Proactive help (pc_help_human, pc_ask_help_world) overlaps with initiative — both reward self-initiated action, but initiative measures breadth of proactivity while personal connections measures relational proactivity specifically |
| Trust & Reputation | Trust scores (external) validate what personal connections scores (internal + behavioral) suggest |

---

## MARKERS

<!-- @mind:todo Implement actor type distinction (human vs AI) in universe graph reader for pc_help_other_ais -->
<!-- @mind:todo Calibrate all caps with real citizen data — current caps are educated estimates -->
<!-- @mind:todo Validate that the 50/50 split for pc_understand_human_deep and pc_relationship_style produces better discrimination than 40/60 -->
<!-- @mind:proposition Consider a "relational growth rate" meta-metric that tracks how quickly a citizen's distinct_actors count grows over 30 days -->
<!-- @mind:proposition Consider temporal windowing per tier: T2 uses 7-day, T5 uses 14-day, T7+ uses 30-day effective window -->
