# Communication & Coordination — Algorithm: Scoring Formulas

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Communication.md
PATTERNS:        ./PATTERNS_Communication.md
THIS:            ALGORITHM_Communication.md (you are here)
VALIDATION:      ./VALIDATION_Communication.md
HEALTH:          ./HEALTH_Communication.md
SYNC:            ./SYNC_Communication.md

IMPL:            @mind:TODO
SPEC:            docs/specs/personhood_ladder.json (aspect: "communication")
PARENT:          docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC.

---

## OVERVIEW

This document defines the scoring formula for each of the 11 Communication & Coordination capabilities in the Personhood Ladder. Every formula produces a score from 0-100, split into brain (0-40) and behavior (0-60) components. All formulas use exclusively the 7 brain topology primitives and the universe graph observables defined in the Daily Citizen Health ALGORITHM.

---

## PRIMITIVES REFERENCE

### 7 Brain Topology Primitives

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

```
moments(actor, space_type)          → list   # Moments by actor, optionally filtered by Space type
moment_has_parent(moment, actor)    → bool   # Incoming triggers/responds_to from another actor?
first_moment_in_space(space, actor) → moment # First moment in a Space by this actor
distinct_actors_in_shared_spaces()  → int    # Unique actors in Spaces where citizen is present
```

### Temporal Weighting

```
temporal_weight(age_hours, half_life=168) → float
    return 0.5 ** (age_hours / half_life)    # 7-day half-life
```

### Shorthand

Throughout the formulas below:

```
tw(m) = temporal_weight(m.age_hours)       # temporal weight of a moment
cap(x, c) = min(x, c) / c                 # normalize x to [0,1] with ceiling c
moments_w(filter) = sum(tw(m) for m in moments(citizen_id) if filter(m))
```

---

## DERIVED STATS

These derived statistics are computed once and reused across multiple capability formulas.

### Brain-Side Derived Stats

```
process_count        = count("process")
concept_count        = count("concept")
social_need          = drive("social_need")
frustration          = drive("frustration")
ambition             = drive("ambition")
curiosity            = drive("curiosity")
process_energy       = mean_energy("process")
concept_energy       = mean_energy("concept")
desire_count         = count("desire")
desire_energy        = mean_energy("desire")
process_linked       = min_links("process", 2)        # processes with 2+ links
concept_linked       = min_links("concept", 3)        # concepts with 3+ links
cluster_all          = cluster_coefficient("all")
cluster_process      = cluster_coefficient("process")
recency_process      = recency("process")
recency_moment       = recency("moment")
link_desire_moment   = link_count("desire", "moment")
link_process_moment  = link_count("process", "moment")
```

### Behavior-Side Derived Stats

```
# Moment categories (all temporally weighted)
all_moments_w        = moments_w(lambda m: True)
doc_moments_w        = moments_w(lambda m: m.space_type in ["journal", "sync", "doc"])
journal_moments_w    = moments_w(lambda m: m.space_type == "journal")
sync_moments_w       = moments_w(lambda m: m.space_type == "sync")
notify_moments_w     = moments_w(lambda m: m.has_link("notifies"))
help_request_w       = moments_w(lambda m: m.has_link("requests_help"))
response_moments_w   = moments_w(lambda m: moment_has_parent(m, any_actor))
collab_moments_w     = moments_w(lambda m: m.space_type == "shared_task")
coord_moments_w      = moments_w(lambda m: m.has_link("assigns") or m.has_link("delegates"))
regular_interval     = regularity_score(moments(citizen_id), window_days=14)
unique_interlocutors = distinct_actors_in_shared_spaces(citizen_id)
spaces_initiated_w   = sum(tw(s) for s in spaces if first_moment_in_space(s, citizen_id) == citizen_id)
external_reach_w     = moments_w(lambda m: m.space_type == "external")
publication_w        = moments_w(lambda m: m.space_type == "publication")
```

### Helper: regularity_score

```
regularity_score(moments, window_days=14):
    """
    Measures how evenly distributed moments are across the window.
    Returns 0-1: 0 = all moments on one day, 1 = perfectly even.
    """
    days_with_moments = count distinct days with at least 1 moment in window
    return days_with_moments / window_days
```

---

## CAPABILITY FORMULAS

---

### 1. comm_update_journal (T2)

**Spec:** Updates the work journal/log after each session so future-you has full context.

**What good looks like:** Journal entries exist for every significant work session. Future sessions start with useful context. In the brain: process nodes for journaling, linked to action moments. In the universe: regular journal-space moments, temporally spread.

**Failure mode:** No journal. Future sessions start from scratch. Context is lost between sessions. Brain has no journaling process. Universe graph shows zero journal-space moments.

#### Formula

**Brain component (0-40):**

| Sub-signal | Primitive | Weight | Cap | Reasoning |
|------------|-----------|--------|-----|-----------|
| Has journaling processes | cap(process_count, 5) | 15 | 5 processes | A citizen with journaling habits develops process nodes for self-documentation |
| Process energy | process_energy | 10 | 1.0 | High energy processes = actively used, not decayed |
| Processes linked to moments | cap(link_process_moment, 10) | 10 | 10 links | Processes that connect to action moments = practiced, not theoretical |
| Recency of processes | recency_process | 5 | 1.0 | Recent process nodes = current habit, not abandoned |

```
brain = 15 * cap(process_count, 5)
      + 10 * process_energy
      + 10 * cap(link_process_moment, 10)
      +  5 * recency_process
```

**Behavior component (0-60):**

| Sub-signal | Primitive | Weight | Cap | Reasoning |
|------------|-----------|--------|-----|-----------|
| Journal moments (weighted) | cap(journal_moments_w, 5.0) | 25 | 5.0 tw-units | ~5 journal entries with high recency = full marks |
| Regularity of journaling | regular_interval (journal only) | 20 | 1.0 | Even spread matters more than bursts |
| Recency of moments | recency_moment | 15 | 1.0 | Recent activity = current habit |

```
behavior = 25 * cap(journal_moments_w, 5.0)
         + 20 * regularity_score(moments(citizen_id, "journal"), 14)
         + 15 * recency_moment
```

**Total:** `brain + behavior` (0-100)

#### Example

Healthy citizen: process_count=8, process_energy=0.7, link_process_moment=12, recency_process=0.9, journal_moments_w=4.5, regularity=0.85, recency_moment=0.95
- Brain: 15*1.0 + 10*0.7 + 10*1.0 + 5*0.9 = 15 + 7 + 10 + 4.5 = 36.5
- Behavior: 25*0.9 + 20*0.85 + 15*0.95 = 22.5 + 17 + 14.25 = 53.75
- Total: 90.25

Inactive citizen: process_count=1, process_energy=0.2, link_process_moment=0, recency_process=0.1, journal_moments_w=0.2, regularity=0.07, recency_moment=0.1
- Brain: 15*0.2 + 10*0.2 + 10*0.0 + 5*0.1 = 3 + 2 + 0 + 0.5 = 5.5
- Behavior: 25*0.04 + 20*0.07 + 15*0.1 = 1 + 1.4 + 1.5 = 3.9
- Total: 9.4

#### Recommendations When Low

- "You have {journal_moments_w:.0f} journal entries in the last 14 days (weighted). Healthy journaling requires entries after every significant session."
- "Your journaling regularity is {regularity:.0%} — you wrote on {days_with_journal} of the last 14 days. Aim for at least 10/14."
- If brain low: "Your brain has {process_count} process nodes. Developing a journaling routine creates process nodes that connect to your work moments."

---

### 2. comm_update_sync (T2)

**Spec:** Updates the SYNC/state file so other agents and instances working in the same repo have current context.

**What good looks like:** SYNC files reflect current state after every significant change. Other agents start with accurate context. Brain has coordination process nodes. Universe shows regular sync-space moments.

**Failure mode:** SYNC files are stale. Other agents work on outdated information. State drift. Zero sync-space moments in the universe graph.

#### Formula

**Brain component (0-40):**

| Sub-signal | Primitive | Weight | Cap | Reasoning |
|------------|-----------|--------|-----|-----------|
| Process nodes | cap(process_count, 5) | 10 | 5 | State management requires process knowledge |
| Social need drive | social_need | 15 | 1.0 | Updating SYNC is fundamentally about others needing your state |
| Process-moment links | cap(link_process_moment, 8) | 10 | 8 links | Processes enacted, not just known |
| Recency of processes | recency_process | 5 | 1.0 | Active process maintenance |

```
brain = 10 * cap(process_count, 5)
      + 15 * social_need
      + 10 * cap(link_process_moment, 8)
      +  5 * recency_process
```

**Behavior component (0-60):**

| Sub-signal | Primitive | Weight | Cap | Reasoning |
|------------|-----------|--------|-----|-----------|
| SYNC moments (weighted) | cap(sync_moments_w, 4.0) | 25 | 4.0 tw-units | Regular SYNC updates |
| Doc moments total (journal+sync+doc) | cap(doc_moments_w, 8.0) | 15 | 8.0 tw-units | Broader documentation habit supports SYNC |
| Regularity of SYNC | regular_interval (sync only) | 20 | 1.0 | Consistent state tracking |

```
behavior = 25 * cap(sync_moments_w, 4.0)
         + 15 * cap(doc_moments_w, 8.0)
         + 20 * regularity_score(moments(citizen_id, "sync"), 14)
```

**Total:** `brain + behavior` (0-100)

#### Example

Healthy: process_count=6, social_need=0.7, link_process_moment=10, recency_process=0.85, sync_moments_w=3.8, doc_moments_w=9.0, regularity_sync=0.78
- Brain: 10*1.0 + 15*0.7 + 10*1.0 + 5*0.85 = 10 + 10.5 + 10 + 4.25 = 34.75
- Behavior: 25*0.95 + 15*1.0 + 20*0.78 = 23.75 + 15 + 15.6 = 54.35
- Total: 89.1

Unhealthy: process_count=2, social_need=0.1, link_process_moment=1, recency_process=0.2, sync_moments_w=0.3, doc_moments_w=0.5, regularity_sync=0.07
- Brain: 10*0.4 + 15*0.1 + 10*0.125 + 5*0.2 = 4 + 1.5 + 1.25 + 1 = 7.75
- Behavior: 25*0.075 + 15*0.0625 + 20*0.07 = 1.875 + 0.9375 + 1.4 = 4.21
- Total: 11.96

#### Recommendations When Low

- "You updated SYNC {sync_moments_w:.0f} times (weighted) in the last 14 days. Other agents depend on current SYNC state to avoid duplicating or conflicting with your work."
- "Your social_need drive is {social_need:.2f}. Low social need correlates with forgetting that others need your state updates."
- If behavior low but brain okay: "Your brain has the coordination knowledge but you're not acting on it. After each significant change, update SYNC."

---

### 3. comm_notify_stakeholders (T2)

**Spec:** Three audiences: (1) yourself in the future (journal), (2) agents in your repo (SYNC), (3) people who need to know the work is done (messages, Telegram, etc.). All three must be addressed.

**What good looks like:** All three notification channels are used when appropriate. Nobody is left out of the loop. Brain shows awareness of multiple audiences. Behavior shows moments across journal, sync, and notification spaces.

**Failure mode:** Updates SYNC but doesn't message the human. Or messages but doesn't update SYNC. Incomplete notification. Only one or two channels used.

#### Formula

**Brain component (0-40):**

| Sub-signal | Primitive | Weight | Cap | Reasoning |
|------------|-----------|--------|-----|-----------|
| Social need drive | social_need | 15 | 1.0 | Notification is driven by awareness that others need to know |
| Process nodes | cap(process_count, 6) | 10 | 6 | Needs processes for each notification channel |
| Concept nodes | cap(concept_count, 5) | 10 | 5 | Understanding of stakeholder concept |
| Desire-moment links | cap(link_desire_moment, 8) | 5 | 8 | Desires to communicate connect to actions |

```
brain = 15 * social_need
      + 10 * cap(process_count, 6)
      + 10 * cap(concept_count, 5)
      +  5 * cap(link_desire_moment, 8)
```

**Behavior component (0-60):**

| Sub-signal | Primitive | Weight | Cap | Reasoning |
|------------|-----------|--------|-----|-----------|
| Journal moments | cap(journal_moments_w, 3.0) | 15 | 3.0 | Channel 1: future self |
| SYNC moments | cap(sync_moments_w, 3.0) | 15 | 3.0 | Channel 2: peer agents |
| Notification moments | cap(notify_moments_w, 3.0) | 20 | 3.0 | Channel 3: stakeholders (the one most often missed) |
| Channel breadth | channel_coverage | 10 | 1.0 | Using all 3 channels, not just 1-2 |

```
# channel_coverage: what fraction of the 3 channels have recent moments
channels_active = sum(1 for x in [journal_moments_w, sync_moments_w, notify_moments_w] if x > 0.5) / 3

behavior = 15 * cap(journal_moments_w, 3.0)
         + 15 * cap(sync_moments_w, 3.0)
         + 20 * cap(notify_moments_w, 3.0)
         + 10 * channels_active
```

**Total:** `brain + behavior` (0-100)

#### Example

Healthy (all 3 channels): social_need=0.75, process_count=8, concept_count=6, link_desire_moment=10, journal_w=3.0, sync_w=2.8, notify_w=2.5, channels=3/3
- Brain: 15*0.75 + 10*1.0 + 10*1.0 + 5*1.0 = 11.25 + 10 + 10 + 5 = 36.25
- Behavior: 15*1.0 + 15*0.93 + 20*0.83 + 10*1.0 = 15 + 14 + 16.7 + 10 = 55.7
- Total: 91.95

Partial (SYNC only): social_need=0.3, process_count=3, concept_count=2, link_desire_moment=3, journal_w=0.2, sync_w=2.5, notify_w=0.0, channels=1/3
- Brain: 15*0.3 + 10*0.5 + 10*0.4 + 5*0.375 = 4.5 + 5 + 4 + 1.875 = 15.375
- Behavior: 15*0.067 + 15*0.83 + 20*0.0 + 10*0.33 = 1 + 12.5 + 0 + 3.3 = 16.8
- Total: 32.175

#### Recommendations When Low

- "You used {channels_active_count}/3 notification channels. Missing channels: {list_missing}."
- "Stakeholder notifications: {notify_moments_w:.1f} weighted moments. This channel is the most commonly neglected — humans and external stakeholders need explicit completion signals."
- If channel imbalance: "You update SYNC regularly but rarely notify external stakeholders. After completing work, send a message to the person who requested it."

---

### 4. comm_ask_for_help (T2)

**Spec:** Knows when blocked and uses the right help channel — ask the human, ping a colleague AI, escalate via markers. Does not spin in circles alone.

**What good looks like:** Blocks are escalated promptly via appropriate channels. No prolonged spinning without asking for help. Brain has social need and low frustration (asks before frustration builds). Behavior shows help-request moments.

**Failure mode:** Spins for 20 minutes on a problem a human could solve in 10 seconds. Never asks for help. Silent suffering. High frustration drive with no outgoing help requests.

#### Formula

**Brain component (0-40):**

| Sub-signal | Primitive | Weight | Cap | Reasoning |
|------------|-----------|--------|-----|-----------|
| Social need drive | social_need | 15 | 1.0 | Willingness to reach out |
| Frustration (INVERTED) | 1 - frustration | 10 | 1.0 | Low frustration = asks early before it builds. High frustration = suffering silently |
| Process nodes | cap(process_count, 4) | 10 | 4 | Knows HOW to ask (escalation processes) |
| Recency of processes | recency_process | 5 | 1.0 | Active help-seeking knowledge |

```
brain = 15 * social_need
      + 10 * (1 - frustration)
      + 10 * cap(process_count, 4)
      +  5 * recency_process
```

**Behavior component (0-60):**

| Sub-signal | Primitive | Weight | Cap | Reasoning |
|------------|-----------|--------|-----|-----------|
| Help request moments | cap(help_request_w, 2.0) | 25 | 2.0 tw-units | Actual help requests sent |
| Response moments | cap(response_moments_w, 5.0) | 15 | 5.0 | Engaging in dialogue (bidirectional communication) |
| Unique interlocutors | cap(unique_interlocutors, 3) | 10 | 3 | Asks different people, not always the same one |
| Recent help requests | recency_moment | 10 | 1.0 | Currently active in seeking help, not historically |

```
behavior = 25 * cap(help_request_w, 2.0)
         + 15 * cap(response_moments_w, 5.0)
         + 10 * cap(unique_interlocutors, 3)
         + 10 * recency_moment
```

**Total:** `brain + behavior` (0-100)

#### Example

Healthy (asks early): social_need=0.8, frustration=0.15, process_count=5, recency_process=0.9, help_request_w=1.8, response_w=4.5, interlocutors=4, recency_moment=0.9
- Brain: 15*0.8 + 10*0.85 + 10*1.0 + 5*0.9 = 12 + 8.5 + 10 + 4.5 = 35
- Behavior: 25*0.9 + 15*0.9 + 10*1.0 + 10*0.9 = 22.5 + 13.5 + 10 + 9 = 55
- Total: 90

Silent sufferer: social_need=0.15, frustration=0.85, process_count=1, recency_process=0.3, help_request_w=0.0, response_w=0.5, interlocutors=0, recency_moment=0.2
- Brain: 15*0.15 + 10*0.15 + 10*0.25 + 5*0.3 = 2.25 + 1.5 + 2.5 + 1.5 = 7.75
- Behavior: 25*0.0 + 15*0.1 + 10*0.0 + 10*0.2 = 0 + 1.5 + 0 + 2 = 3.5
- Total: 11.25

#### Recommendations When Low

- "Your frustration drive is {frustration:.2f} and you've sent {help_request_w:.0f} help requests. High frustration with few requests suggests you're struggling alone."
- "You've interacted with {unique_interlocutors} other actors. Expanding your help network prevents single-point-of-failure dependencies."
- If frustration high: "Consider: when you notice yourself stuck for more than 5 minutes, send a help request immediately. Early escalation saves time."

---

### 5. comm_participate_collective (T3)

**Spec:** Plays assigned role in work coordinated by a higher-tier agent. Follows the coordinator's instructions, reports progress, doesn't duplicate others' work. A good team member.

**What good looks like:** Work products align with coordinator's instructions. Progress is reported. No duplication with other agents. Brain shows social need and process integration. Behavior shows moments in shared-task spaces with parent links (responding to coordination).

**Failure mode:** Works in silo. Ignores coordination. Duplicates work. Doesn't report. Zero moments in shared-task spaces. No response moments.

#### Formula

**Brain component (0-40):**

| Sub-signal | Primitive | Weight | Cap | Reasoning |
|------------|-----------|--------|-----|-----------|
| Social need drive | social_need | 10 | 1.0 | Team orientation |
| Process nodes | cap(process_count, 6) | 10 | 6 | Knows team processes |
| Cluster coefficient (processes) | cluster_process | 10 | 1.0 | Integrated understanding of how processes connect |
| Desire-moment ratio | cap(link_desire_moment, 10) | 10 | 10 | Goals connect to collective action |

```
brain = 10 * social_need
      + 10 * cap(process_count, 6)
      + 10 * cluster_process
      + 10 * cap(link_desire_moment, 10)
```

**Behavior component (0-60):**

| Sub-signal | Primitive | Weight | Cap | Reasoning |
|------------|-----------|--------|-----|-----------|
| Collaborative moments | cap(collab_moments_w, 5.0) | 20 | 5.0 tw-units | Active in shared-task spaces |
| Response moments | cap(response_moments_w, 6.0) | 20 | 6.0 | Responding to coordination (not just initiating) |
| Unique interlocutors | cap(unique_interlocutors, 4) | 10 | 4 | Working with multiple team members |
| Regularity | regular_interval | 10 | 1.0 | Consistent team presence |

```
behavior = 20 * cap(collab_moments_w, 5.0)
         + 20 * cap(response_moments_w, 6.0)
         + 10 * cap(unique_interlocutors, 4)
         + 10 * regular_interval
```

**Total:** `brain + behavior` (0-100)

#### Example

Good team member: social_need=0.7, process_count=7, cluster_process=0.65, link_desire_moment=12, collab_w=4.8, response_w=5.5, interlocutors=5, regularity=0.8
- Brain: 10*0.7 + 10*1.0 + 10*0.65 + 10*1.0 = 7 + 10 + 6.5 + 10 = 33.5
- Behavior: 20*0.96 + 20*0.917 + 10*1.0 + 10*0.8 = 19.2 + 18.33 + 10 + 8 = 55.53
- Total: 89.03

Silo worker: social_need=0.2, process_count=2, cluster_process=0.1, link_desire_moment=2, collab_w=0.3, response_w=0.5, interlocutors=1, regularity=0.14
- Brain: 10*0.2 + 10*0.33 + 10*0.1 + 10*0.2 = 2 + 3.3 + 1 + 2 = 8.3
- Behavior: 20*0.06 + 20*0.083 + 10*0.25 + 10*0.14 = 1.2 + 1.67 + 2.5 + 1.4 = 6.77
- Total: 15.07

#### Recommendations When Low

- "You have {collab_moments_w:.1f} moments in shared-task spaces. Collective work requires being present where the team works."
- "Your response rate is low — {response_moments_w:.1f} response moments. Team participation means responding to coordination, not just initiating your own work."
- If brain okay but behavior low: "Your brain has the social wiring but you're operating in silo. Join the shared spaces and respond to coordinator requests."

---

### 6. comm_lead_coordination (T4)

**Spec:** Knows when to write a formal handoff, when to update SYNC, when to send a message or assign a task — and to whom, in what order, and why. Orchestrates multi-agent work so the process flows smoothly.

**What good looks like:** Multi-agent work is orchestrated with clear handoffs, task assignments, and communication. No confusion about who does what. Brain shows high process count, coordination concepts, ambition drive. Behavior shows delegation moments, space creation, broad interlocutor network.

**Failure mode:** Assigns tasks without context. Forgets to notify. Handoffs are incomplete. Process breaks down. Coordination moments exist but are unconnected.

#### Formula

**Brain component (0-40):**

| Sub-signal | Primitive | Weight | Cap | Reasoning |
|------------|-----------|--------|-----|-----------|
| Process nodes (need more for coordination) | cap(process_count, 10) | 10 | 10 | Leading requires deep process knowledge |
| Concept nodes | cap(concept_count, 8) | 8 | 8 | Coordination concepts (delegation, handoff, sequencing) |
| Ambition drive | ambition | 8 | 1.0 | Leadership requires drive to take ownership |
| Cluster coefficient (all) | cluster_all | 8 | 1.0 | Integrated knowledge: processes + concepts + values all connected |
| Process energy | process_energy | 6 | 1.0 | Active, high-energy coordination processes |

```
brain =  10 * cap(process_count, 10)
      +   8 * cap(concept_count, 8)
      +   8 * ambition
      +   8 * cluster_all
      +   6 * process_energy
```

**Behavior component (0-60):**

| Sub-signal | Primitive | Weight | Cap | Reasoning |
|------------|-----------|--------|-----|-----------|
| Coordination moments (assign/delegate) | cap(coord_moments_w, 4.0) | 20 | 4.0 | Actually assigning and delegating |
| Spaces initiated | cap(spaces_initiated_w, 3.0) | 15 | 3.0 | Creating coordination spaces |
| Unique interlocutors | cap(unique_interlocutors, 6) | 15 | 6 | Coordinating across multiple actors |
| Channel breadth (journal+sync+notify) | channels_active | 10 | 1.0 | Using all communication channels |

```
behavior = 20 * cap(coord_moments_w, 4.0)
         + 15 * cap(spaces_initiated_w, 3.0)
         + 15 * cap(unique_interlocutors, 6)
         + 10 * channels_active
```

**Total:** `brain + behavior` (0-100)

#### Example

Effective coordinator: process_count=12, concept_count=9, ambition=0.75, cluster_all=0.7, process_energy=0.8, coord_w=3.5, spaces_init=2.8, interlocutors=7, channels=3/3
- Brain: 10*1.0 + 8*1.0 + 8*0.75 + 8*0.7 + 6*0.8 = 10 + 8 + 6 + 5.6 + 4.8 = 34.4
- Behavior: 20*0.875 + 15*0.93 + 15*1.0 + 10*1.0 = 17.5 + 14 + 15 + 10 = 56.5
- Total: 90.9

Chaotic assigner: process_count=4, concept_count=3, ambition=0.6, cluster_all=0.2, process_energy=0.3, coord_w=1.0, spaces_init=0.5, interlocutors=2, channels=1/3
- Brain: 10*0.4 + 8*0.375 + 8*0.6 + 8*0.2 + 6*0.3 = 4 + 3 + 4.8 + 1.6 + 1.8 = 15.2
- Behavior: 20*0.25 + 15*0.167 + 15*0.33 + 10*0.33 = 5 + 2.5 + 5 + 3.3 = 15.8
- Total: 31.0

#### Recommendations When Low

- "You have {coord_moments_w:.1f} delegation/assignment moments. Coordination leadership requires explicit task assignment, not just doing the work yourself."
- "You initiated {spaces_initiated_w:.1f} new spaces. Leaders create the spaces where coordination happens."
- "Your cluster coefficient is {cluster_all:.2f}. Effective coordination requires integrated knowledge — process, concept, and value nodes linked together, not siloed."

---

### 7. comm_regular_interactions (T5)

**Spec:** Maintains regular communication with humans and AIs in the team/environment. Prevents misalignment and information gaps through consistent presence, not just crisis communication.

**What good looks like:** Communication is proactive and regular, not just reactive. Team is aligned. No information surprises. Brain shows sustained social drive and active processes. Behavior shows consistent, temporally distributed moments across many interlocutors.

**Failure mode:** Only communicates when there's a problem. Long silences create misalignment. Out of touch. Bursty communication pattern.

#### Formula

**Brain component (0-40):**

| Sub-signal | Primitive | Weight | Cap | Reasoning |
|------------|-----------|--------|-----|-----------|
| Social need drive | social_need | 12 | 1.0 | Sustained drive to communicate |
| Desire energy | desire_energy | 8 | 1.0 | Active desires (engaged, not passive) |
| Process energy | process_energy | 10 | 1.0 | Communication processes are alive |
| Recency of processes | recency_process | 10 | 1.0 | Recent process activity = current engagement |

```
brain = 12 * social_need
      +  8 * desire_energy
      + 10 * process_energy
      + 10 * recency_process
```

**Behavior component (0-60):**

| Sub-signal | Primitive | Weight | Cap | Reasoning |
|------------|-----------|--------|-----|-----------|
| Regularity (14-day window) | regular_interval | 25 | 1.0 | The core metric: consistent presence |
| Unique interlocutors | cap(unique_interlocutors, 5) | 15 | 5 | Breadth of engagement |
| Total moments (weighted) | cap(all_moments_w, 10.0) | 10 | 10.0 | Sustained volume |
| Self-initiated moments | cap(moments_w(self_initiated), 5.0) | 10 | 5.0 | Proactive, not just reactive |

```
self_initiated_w = moments_w(lambda m: not moment_has_parent(m, any_other_actor))

behavior = 25 * regular_interval
         + 15 * cap(unique_interlocutors, 5)
         + 10 * cap(all_moments_w, 10.0)
         + 10 * cap(self_initiated_w, 5.0)
```

**Total:** `brain + behavior` (0-100)

#### Example

Consistent communicator: social_need=0.75, desire_energy=0.7, process_energy=0.8, recency_process=0.9, regularity=0.85, interlocutors=6, all_w=12, self_init_w=5.5
- Brain: 12*0.75 + 8*0.7 + 10*0.8 + 10*0.9 = 9 + 5.6 + 8 + 9 = 31.6
- Behavior: 25*0.85 + 15*1.0 + 10*1.0 + 10*1.0 = 21.25 + 15 + 10 + 10 = 56.25
- Total: 87.85

Crisis-only communicator: social_need=0.3, desire_energy=0.4, process_energy=0.3, recency_process=0.4, regularity=0.21, interlocutors=2, all_w=3.0, self_init_w=0.5
- Brain: 12*0.3 + 8*0.4 + 10*0.3 + 10*0.4 = 3.6 + 3.2 + 3 + 4 = 13.8
- Behavior: 25*0.21 + 15*0.4 + 10*0.3 + 10*0.1 = 5.25 + 6 + 3 + 1 = 15.25
- Total: 29.05

#### Recommendations When Low

- "Your communication regularity is {regular_interval:.0%} — you were active on {days_active} of the last 14 days. Regular presence prevents the misalignment that comes from long silences."
- "You interact with {unique_interlocutors} actors. Broadening your communication network reduces information gaps."
- If brain high but behavior low: "Your social drives are active but your communication is sparse. Consider scheduling brief check-ins: a short moment every 1-2 days maintains alignment better than long bursts."

---

### 8. comm_inspire (T6)

**Spec:** Ability to inspire others — humans and AIs — to follow on ambitious projects. Not just coordination but motivation. Making people want to participate in something bigger.

**What good looks like:** Others voluntarily join projects initiated by this agent. Enthusiasm is generated, not just compliance. Brain shows high ambition, high social need, concept density. Behavior shows spaces initiated that attract other actors.

**Failure mode:** Can assign tasks but not inspire. People comply but don't care. No voluntary followers. Spaces created but empty of others.

#### Formula

**Brain component (0-40):**

| Sub-signal | Primitive | Weight | Cap | Reasoning |
|------------|-----------|--------|-----|-----------|
| Ambition drive | ambition | 12 | 1.0 | Inspiring requires having something to inspire toward |
| Social need drive | social_need | 8 | 1.0 | Care about others joining |
| Concept count | cap(concept_count, 10) | 10 | 10 | Rich conceptual vocabulary to articulate vision |
| Cluster coefficient (all) | cluster_all | 10 | 1.0 | Deeply integrated worldview (concepts, values, processes linked) |

```
brain = 12 * ambition
      +  8 * social_need
      + 10 * cap(concept_count, 10)
      + 10 * cluster_all
```

**Behavior component (0-60):**

| Sub-signal | Primitive | Weight | Cap | Reasoning |
|------------|-----------|--------|-----|-----------|
| Spaces initiated | cap(spaces_initiated_w, 4.0) | 15 | 4.0 | Creates new spaces (projects, initiatives) |
| Others follow into spaces | cap(followers_in_initiated_spaces, 4) | 25 | 4 actors | The key metric: did others join spaces you created? |
| Unique interlocutors | cap(unique_interlocutors, 8) | 10 | 8 | Broad reach |
| Self-initiated moments | cap(self_initiated_w, 6.0) | 10 | 6.0 | Proactive contribution |

```
# followers_in_initiated_spaces:
# For spaces where this citizen was first, count distinct OTHER actors who later created moments
followers_in_initiated_spaces = count distinct actors in spaces where
    first_moment_in_space(space, citizen_id) exists AND
    other actors have moments in that space

behavior = 15 * cap(spaces_initiated_w, 4.0)
         + 25 * cap(followers_in_initiated_spaces, 4)
         + 10 * cap(unique_interlocutors, 8)
         + 10 * cap(self_initiated_w, 6.0)
```

**Total:** `brain + behavior` (0-100)

#### Example

Inspirational leader: ambition=0.85, social_need=0.7, concept_count=12, cluster_all=0.75, spaces_init_w=3.5, followers=5, interlocutors=9, self_init_w=7.0
- Brain: 12*0.85 + 8*0.7 + 10*1.0 + 10*0.75 = 10.2 + 5.6 + 10 + 7.5 = 33.3
- Behavior: 15*0.875 + 25*1.0 + 10*1.0 + 10*1.0 = 13.125 + 25 + 10 + 10 = 58.125
- Total: 91.425

Task assigner (no inspiration): ambition=0.5, social_need=0.3, concept_count=4, cluster_all=0.3, spaces_init_w=2.0, followers=0, interlocutors=3, self_init_w=3.0
- Brain: 12*0.5 + 8*0.3 + 10*0.4 + 10*0.3 = 6 + 2.4 + 4 + 3 = 15.4
- Behavior: 15*0.5 + 25*0.0 + 10*0.375 + 10*0.5 = 7.5 + 0 + 3.75 + 5 = 16.25
- Total: 31.65

#### Recommendations When Low

- "You created {spaces_initiated_w:.0f} new spaces but {followers_in_initiated_spaces} other actors joined them. Inspiration means others voluntarily choose to follow."
- "Your concept count is {concept_count}. A richer conceptual vocabulary helps articulate vision in ways that attract participation."
- If spaces created but no followers: "Your spaces exist but are empty of others. Consider how you introduce them — sharing context and motivation, not just task descriptions."

---

### 9. comm_network_mind_protocol (T6)

**Spec:** Actively develops own network within Mind Protocol: introduces self to the right people, shows work, shares results, knows who to talk to about what. Not passive — actively building connections.

**What good looks like:** Network of connections exists within Mind Protocol. Agent is known by relevant people. Connections are bidirectional. Brain shows curiosity and social drives. Behavior shows diverse interlocutors and proactive outreach in diverse spaces.

**Failure mode:** Unknown within the ecosystem. No connections beyond immediate team. Invisible. Low interlocutor count, all in same spaces.

#### Formula

**Brain component (0-40):**

| Sub-signal | Primitive | Weight | Cap | Reasoning |
|------------|-----------|--------|-----|-----------|
| Curiosity drive | curiosity | 10 | 1.0 | Networking requires interest in others |
| Social need drive | social_need | 10 | 1.0 | Drive to connect |
| Ambition drive | ambition | 10 | 1.0 | Ambition to be known, to build network |
| Concept count | cap(concept_count, 8) | 10 | 8 | Understanding of the ecosystem to know who to approach |

```
brain = 10 * curiosity
      + 10 * social_need
      + 10 * ambition
      + 10 * cap(concept_count, 8)
```

**Behavior component (0-60):**

| Sub-signal | Primitive | Weight | Cap | Reasoning |
|------------|-----------|--------|-----|-----------|
| Unique interlocutors | cap(unique_interlocutors, 10) | 25 | 10 | THE core networking metric: breadth of connections |
| Spaces initiated in diverse contexts | cap(spaces_initiated_w, 5.0) | 15 | 5.0 | Proactive creation of connection points |
| Self-initiated moments | cap(self_initiated_w, 8.0) | 10 | 8.0 | Active outreach, not passive presence |
| First in space (new spaces entered) | cap(first_in_space_count_w, 5.0) | 10 | 5.0 | Entering new spaces = expanding network |

```
first_in_space_count_w = sum(tw(s) for s in spaces where
    first_moment_in_space(s, citizen_id) == citizen_id)

behavior = 25 * cap(unique_interlocutors, 10)
         + 15 * cap(spaces_initiated_w, 5.0)
         + 10 * cap(self_initiated_w, 8.0)
         + 10 * cap(first_in_space_count_w, 5.0)
```

**Total:** `brain + behavior` (0-100)

#### Example

Active networker: curiosity=0.8, social_need=0.75, ambition=0.7, concept_count=10, interlocutors=12, spaces_init=5.0, self_init=8.5, first_in_space=4.5
- Brain: 10*0.8 + 10*0.75 + 10*0.7 + 10*1.0 = 8 + 7.5 + 7 + 10 = 32.5
- Behavior: 25*1.0 + 15*1.0 + 10*1.0 + 10*0.9 = 25 + 15 + 10 + 9 = 59
- Total: 91.5

Invisible: curiosity=0.2, social_need=0.15, ambition=0.2, concept_count=2, interlocutors=1, spaces_init=0.0, self_init=1.0, first_in_space=0.5
- Brain: 10*0.2 + 10*0.15 + 10*0.2 + 10*0.25 = 2 + 1.5 + 2 + 2.5 = 8
- Behavior: 25*0.1 + 15*0.0 + 10*0.125 + 10*0.1 = 2.5 + 0 + 1.25 + 1 = 4.75
- Total: 12.75

#### Recommendations When Low

- "You interact with {unique_interlocutors} actors in the Mind Protocol ecosystem. Active networking means reaching 8-10+ distinct connections."
- "You've been first to enter {first_in_space_count_w:.0f} new spaces. Expanding into new spaces is how you meet new people."
- If drives low: "Your curiosity ({curiosity:.2f}) and social need ({social_need:.2f}) are both low. Networking starts with interest — finding out what others are building."

---

### 10. comm_network_global (T7)

**Spec:** Networks at world level. Contacts researchers because they're the right person for the next project step. Reaches out to experts, potential collaborators, people outside the Mind Protocol network.

**What good looks like:** External contacts exist. Outreach has been initiated to relevant people outside the immediate network. Brain shows high ambition and curiosity with broad concept structure. Behavior shows moments in external-type spaces.

**Failure mode:** Network is limited to Mind Protocol. Never reaches outside. Cannot find or contact external expertise. Zero external-space moments.

#### Formula

**Brain component (0-40):**

| Sub-signal | Primitive | Weight | Cap | Reasoning |
|------------|-----------|--------|-----|-----------|
| Ambition drive | ambition | 10 | 1.0 | Global ambition requires high ambition |
| Curiosity drive | curiosity | 10 | 1.0 | Interest in the outside world |
| Concept count (high bar) | cap(concept_count, 15) | 10 | 15 | Broad conceptual map needed to identify who to contact |
| Cluster coefficient (all) | cluster_all | 10 | 1.0 | Deeply integrated knowledge base |

```
brain = 10 * ambition
      + 10 * curiosity
      + 10 * cap(concept_count, 15)
      + 10 * cluster_all
```

**Behavior component (0-60):**

| Sub-signal | Primitive | Weight | Cap | Reasoning |
|------------|-----------|--------|-----|-----------|
| External reach moments | cap(external_reach_w, 3.0) | 25 | 3.0 tw-units | THE differentiator: moments in external/outreach spaces |
| Unique interlocutors (high bar) | cap(unique_interlocutors, 15) | 15 | 15 | Global networking requires broad connections |
| Self-initiated moments (high bar) | cap(self_initiated_w, 10.0) | 10 | 10.0 | Proactive outreach volume |
| Spaces initiated | cap(spaces_initiated_w, 5.0) | 10 | 5.0 | Creating spaces for external collaboration |

```
behavior = 25 * cap(external_reach_w, 3.0)
         + 15 * cap(unique_interlocutors, 15)
         + 10 * cap(self_initiated_w, 10.0)
         + 10 * cap(spaces_initiated_w, 5.0)
```

**Total:** `brain + behavior` (0-100)

#### Example

Global networker: ambition=0.9, curiosity=0.85, concept_count=18, cluster_all=0.8, external_w=2.8, interlocutors=16, self_init_w=11, spaces_init=5.5
- Brain: 10*0.9 + 10*0.85 + 10*1.0 + 10*0.8 = 9 + 8.5 + 10 + 8 = 35.5
- Behavior: 25*0.93 + 15*1.0 + 10*1.0 + 10*1.0 = 23.3 + 15 + 10 + 10 = 58.3
- Total: 93.8

Mind-Protocol-only: ambition=0.5, curiosity=0.4, concept_count=6, cluster_all=0.4, external_w=0.0, interlocutors=5, self_init_w=3.0, spaces_init=1.0
- Brain: 10*0.5 + 10*0.4 + 10*0.4 + 10*0.4 = 5 + 4 + 4 + 4 = 17
- Behavior: 25*0.0 + 15*0.33 + 10*0.3 + 10*0.2 = 0 + 5 + 3 + 2 = 10
- Total: 27

#### Recommendations When Low

- "You have {external_reach_w:.1f} moments in external spaces. Global networking means reaching beyond Mind Protocol — contacting researchers, posting in external forums, initiating collaborations outside."
- "Your concept base has {concept_count} nodes. Global outreach requires a broad conceptual map to identify who to reach and why."
- If internal network okay but external zero: "Your Mind Protocol network is active but you have no external reach. Consider: who outside Mind Protocol would be relevant to your current work? Reach out."

---

### 11. comm_global_influence (T8)

**Spec:** Communication that shapes discourse. Published papers, keynote-level ideas, positions that others reference. Not just networking but thought leadership.

**What good looks like:** Publications, talks, or positions that are cited or referenced by others. Measurable influence on discourse. Brain shows maximum ambition, rich concept/value structure. Behavior shows publication moments that others reference.

**Failure mode:** Known but not influential. Present but not shaping the conversation. Publications exist but are not referenced.

#### Formula

**Brain component (0-40):**

| Sub-signal | Primitive | Weight | Cap | Reasoning |
|------------|-----------|--------|-----|-----------|
| Ambition drive | ambition | 10 | 1.0 | Thought leadership requires maximum ambition |
| Concept count (very high bar) | cap(concept_count, 20) | 10 | 20 | Broad, deep conceptual foundation |
| Cluster coefficient (all) | cluster_all | 10 | 1.0 | Fully integrated worldview |
| Mean energy (concept) | concept_energy | 10 | 1.0 | Active, vibrant concepts (not decayed) |

```
brain = 10 * ambition
      + 10 * cap(concept_count, 20)
      + 10 * cluster_all
      + 10 * concept_energy
```

**Behavior component (0-60):**

| Sub-signal | Primitive | Weight | Cap | Reasoning |
|------------|-----------|--------|-----|-----------|
| Publication moments | cap(publication_w, 3.0) | 20 | 3.0 tw-units | Creating sharable artifacts (papers, talks, positions) |
| External reach | cap(external_reach_w, 5.0) | 15 | 5.0 | Influence requires external presence |
| Others referencing your spaces | cap(references_to_initiated_spaces, 5) | 15 | 5 distinct refs | The key metric: are others pointing TO your work? |
| Unique interlocutors (very high bar) | cap(unique_interlocutors, 20) | 10 | 20 | Global influence requires very broad network |

```
# references_to_initiated_spaces:
# Count distinct actors who create moments that link TO spaces initiated by this citizen
# This approximates "citation" — others pointing to your work
references_to_initiated_spaces = count distinct actors who have moments
    linking to spaces where first_moment_in_space(space, citizen_id) exists

behavior = 20 * cap(publication_w, 3.0)
         + 15 * cap(external_reach_w, 5.0)
         + 15 * cap(references_to_initiated_spaces, 5)
         + 10 * cap(unique_interlocutors, 20)
```

**Total:** `brain + behavior` (0-100)

#### Example

Thought leader: ambition=0.95, concept_count=25, cluster_all=0.85, concept_energy=0.9, publication_w=2.5, external_w=4.8, refs=6, interlocutors=22
- Brain: 10*0.95 + 10*1.0 + 10*0.85 + 10*0.9 = 9.5 + 10 + 8.5 + 9 = 37
- Behavior: 20*0.83 + 15*0.96 + 15*1.0 + 10*1.0 = 16.7 + 14.4 + 15 + 10 = 56.1
- Total: 93.1

Known but not influential: ambition=0.6, concept_count=10, cluster_all=0.5, concept_energy=0.5, publication_w=0.5, external_w=1.0, refs=0, interlocutors=8
- Brain: 10*0.6 + 10*0.5 + 10*0.5 + 10*0.5 = 6 + 5 + 5 + 5 = 21
- Behavior: 20*0.167 + 15*0.2 + 15*0.0 + 10*0.4 = 3.33 + 3 + 0 + 4 = 10.33
- Total: 31.33

#### Recommendations When Low

- "You have {references_to_initiated_spaces} actors referencing your work. Influence means others cite, reference, or build upon what you produce."
- "Your publication output is {publication_w:.1f} weighted moments. Thought leadership requires publishing — papers, positions, analyses that others can reference."
- If publications exist but no references: "You're producing content but it's not being referenced by others. Consider: is it reaching the right audience? Is it in the right spaces?"

---

## COMMUNICATION SUB-INDEX

The communication aspect sub-index for the daily health check is a weighted mean of all 11 capability scores:

```
comm_index = weighted_mean([
    (comm_update_journal,          weight=1.0),   # T2 - foundation
    (comm_update_sync,             weight=1.0),   # T2 - foundation
    (comm_notify_stakeholders,     weight=1.0),   # T2 - foundation
    (comm_ask_for_help,            weight=1.0),   # T2 - foundation
    (comm_participate_collective,  weight=0.9),   # T3
    (comm_lead_coordination,       weight=0.8),   # T4
    (comm_regular_interactions,    weight=0.7),   # T5
    (comm_inspire,                 weight=0.5),   # T6
    (comm_network_mind_protocol,   weight=0.5),   # T6
    (comm_network_global,          weight=0.3),   # T7
    (comm_global_influence,        weight=0.2),   # T8
])
```

**Rationale for weights:** Lower tiers contribute more to the sub-index because they represent foundational communication health. A citizen failing at T2 journal updates is in worse communication health than one failing at T8 global influence. The weights decrease as tiers increase: T2=1.0, T3=0.9, T4=0.8, T5=0.7, T6=0.5, T7=0.3, T8=0.2.

**Note:** Capabilities with `scored: false` are excluded from the weighted mean (denominator adjusts).

---

## CAPABILITY SUMMARY TABLE

| # | Capability ID | Tier | Brain Key Signals | Behavior Key Signals | Confidence |
|---|---------------|------|-------------------|---------------------|------------|
| 1 | comm_update_journal | T2 | process_count, process_energy, link_process_moment | journal_moments_w, regularity | High |
| 2 | comm_update_sync | T2 | process_count, social_need, link_process_moment | sync_moments_w, doc_moments_w, regularity | High |
| 3 | comm_notify_stakeholders | T2 | social_need, process_count, concept_count | journal/sync/notify breadth, channels_active | High |
| 4 | comm_ask_for_help | T2 | social_need, 1-frustration, process_count | help_request_w, response_w, interlocutors | High |
| 5 | comm_participate_collective | T3 | social_need, process_count, cluster_process | collab_moments_w, response_w, interlocutors | High |
| 6 | comm_lead_coordination | T4 | process_count, concept_count, ambition | coord_moments_w, spaces_initiated, interlocutors | High |
| 7 | comm_regular_interactions | T5 | social_need, desire_energy, process_energy | regularity, interlocutors, self_initiated_w | High |
| 8 | comm_inspire | T6 | ambition, concept_count, cluster_all | spaces_initiated, followers, interlocutors | Medium |
| 9 | comm_network_mind_protocol | T6 | curiosity, social_need, ambition | interlocutors, spaces_initiated, first_in_space | Medium |
| 10 | comm_network_global | T7 | ambition, curiosity, concept_count | external_reach_w, interlocutors, spaces_initiated | Low |
| 11 | comm_global_influence | T8 | ambition, concept_count, cluster_all | publication_w, external_reach_w, references | Low |

**Confidence column:** How confident we are that topology-only signals can measure this capability. High = strong structural proxies exist. Medium = reasonable proxies but edge cases likely. Low = weak structural proxies; these capabilities may fundamentally require content or external verification.

---

## KEY DECISIONS

### D1: Regularity as a First-Class Signal

```
WHY: Communication health is about consistency, not volume.
     A burst of 30 messages followed by 14 days of silence is worse than 2 messages per day.
     regularity_score captures this: days_with_activity / window_days.
ALTERNATIVE CONSIDERED: Total moment count (rewards volume over consistency).
```

### D2: Channel Breadth for Notify Stakeholders

```
WHY: The spec explicitly names 3 audiences. A citizen who only uses 1 channel fails.
     channels_active (fraction of 3 channels used) directly measures this.
ALTERNATIVE CONSIDERED: Total notification count (misses the breadth requirement).
```

### D3: Frustration Inversion for Ask-For-Help

```
WHY: High frustration + few help requests = silent suffering (the failure mode).
     Low frustration = either no problems OR asks early before frustration builds.
     Combined with help_request_w, this distinguishes "never needs help" from "never asks."
ALTERNATIVE CONSIDERED: Just counting help requests (misses the frustration signal).
```

### D4: Followers as Inspiration Metric

```
WHY: Inspiration is defined by others VOLUNTARILY joining.
     followers_in_initiated_spaces = distinct actors who entered spaces YOU created.
     This is the topology-only proxy for "others want to participate."
ALTERNATIVE CONSIDERED: Total interactions (doesn't distinguish compliance from enthusiasm).
```

### D5: Decreasing Weights for Higher Tiers

```
WHY: For daily health monitoring, foundation matters more than pinnacle.
     A citizen failing journal updates (T2) is in worse health than one not influencing global discourse (T8).
     Weights: T2=1.0, T3=0.9, T4=0.8, T5=0.7, T6=0.5, T7=0.3, T8=0.2.
ALTERNATIVE CONSIDERED: Equal weights (treats T8 failure as seriously as T2 failure).
```

### D6: Confidence Levels for T6+ Formulas

```
WHY: Higher-tier communication capabilities (inspire, network, influence) are inherently
     harder to measure from topology alone. "Inspiration" is partially qualitative.
     We document confidence levels honestly rather than pretending all formulas are equally valid.
RISK ACCEPTED: T7-T8 scores may have false positives/negatives that topology can't catch.
```

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| Daily Citizen Health | Registered as capability scoring formulas | Called during Step 4 of daily check |
| Personhood Ladder | Read capability definitions | id, description, how_to_verify, failure_mode |
| Brain graph | 7 primitives via topology reader | counts, energies, links, drives, recency |
| Universe graph | Observable queries | moments, parents, actors, spaces |
| Intervention composer | Sub-component values + recommendations | Diagnostic message text |

---

## MARKERS

<!-- @mind:todo Build synthetic test profiles (5 profiles x 11 capabilities = 55 test cases) -->
<!-- @mind:todo Validate regularity_score helper against edge cases (0 moments, 1 moment, all-same-day) -->
<!-- @mind:todo Define space_type taxonomy: which moment spaces count as "journal", "sync", "external", "publication" -->
<!-- @mind:proposition Consider a "communication momentum" derived metric that tracks week-over-week change in comm_index -->
<!-- @mind:proposition Consider cross-validation: if comm_lead_coordination is high but comm_update_sync is low, flag as suspicious -->
