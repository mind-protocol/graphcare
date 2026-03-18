# Trust & Reputation — Algorithm: Scoring Formulas for 5 Capabilities

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Trust_Reputation.md
PATTERNS:        ./PATTERNS_Trust_Reputation.md
THIS:            ALGORITHM_Trust_Reputation.md (you are here)
VALIDATION:      ./VALIDATION_Trust_Reputation.md
HEALTH:          ./HEALTH_Trust_Reputation.md
SYNC:            ./SYNC_Trust_Reputation.md

SPEC:            docs/specs/personhood_ladder.json (aspect="trust_reputation")
PARENT ALGO:     docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md
```

> **Contract:** Read docs before modifying. After changes: update SYNC.

---

## OVERVIEW

This document defines the exact scoring formula for each of the 5 Trust & Reputation capabilities in the Personhood Ladder. Each formula uses only the 7 topology primitives and universe graph observables defined in the Daily Citizen Health ALGORITHM. No exceptions.

Every formula produces: `brain_score (0-40) + behavior_score (0-60) = total (0-100)`.

The Trust & Reputation sub-index is the weighted mean of all 5 capability scores.

Trust is one of the most topologically measurable aspects. Mind Protocol's 5-tier trust system (Owner, High, Medium, Low, Stranger) provides a direct structural signal, and behavioral patterns of reliability, responsiveness, and network breadth are all visible in the universe graph.

---

## PRIMITIVES REFERENCE

### 7 Brain Topology Primitives

```
count(type)              -> int    # Number of nodes of a given type
mean_energy(type)        -> float  # Average energy of nodes of a type (0-1)
link_count(src, tgt)     -> int    # Number of links from src type to tgt type
min_links(type, n)       -> int    # Nodes of a type with at least n links to any other
cluster_coefficient(type)-> float  # Internal connectivity of a subgraph (0-1)
drive(name)              -> float  # Drive value by name (0-1)
recency(type)            -> float  # Freshness score based on newest nodes (0-1, decays)
```

### Universe Graph Observables

```
moments(actor, space_type)          -> list   # Moments by actor, optionally filtered by Space type
moment_has_parent(moment, actor)    -> bool   # Does this moment have an incoming triggers/responds_to from another actor?
first_moment_in_space(space, actor) -> moment # First moment in a Space by this actor
distinct_actors_in_shared_spaces()  -> int    # Count of unique actors in Spaces where citizen is present
temporal_weight(age_hours, half_life=168) -> float  # 0.5^(age_hours/168)
```

---

## SHARED BEHAVIOR STATS

These are computed once and reused across all 5 formulas.

```
all_moments      = moments(citizen_id)                           # last 30 days
reactive_moments = [m for m in all_moments if moment_has_parent(m, other_actor)]
self_init_moments= [m for m in all_moments if not moment_has_parent(m, other_actor)]

total_w          = sum(temporal_weight(m.age) for m in all_moments)
reactive_w       = sum(temporal_weight(m.age) for m in reactive_moments)
self_init_w      = sum(temporal_weight(m.age) for m in self_init_moments)
```

### Derived: Regularity Score

The foundational metric for trust scoring. Measures consistency of moment production over time, not just volume.

```
regularity(citizen_id, window_days=30):
    # Divide last 30 days into 6 windows of 5 days each
    windows = partition_days(30, 5)  # 6 windows
    counts  = [len(moments(citizen_id, window=w)) for w in windows]

    # If zero moments in all windows, regularity = 0
    if sum(counts) == 0:
        return 0.0

    mean_count = mean(counts)
    std_count  = std(counts)

    # Coefficient of variation: lower = more regular
    cv = std_count / max(mean_count, 0.01)

    # Convert to 0-1 score: cv=0 -> 1.0 (perfectly regular), cv>=2 -> 0.0 (very irregular)
    return max(0.0, 1.0 - cv / 2.0)
```

### Derived: Response Chain Completion

Measures how reliably the citizen responds when triggered by another actor.

```
response_completion(citizen_id, window_days=30):
    # Find all moments from other actors that target this citizen
    # (incoming triggers/responds_to links where the parent actor is not citizen_id)
    inbound_triggers = [m for m in universe_moments
                        if m.has_link("triggers", target_actor=citizen_id)
                        and m.actor != citizen_id
                        and m.age_days <= window_days]

    if len(inbound_triggers) == 0:
        return 1.0  # No requests = no failures (benefit of the doubt)

    # For each inbound trigger, check if citizen produced a response moment
    completed = [t for t in inbound_triggers
                 if any(m for m in all_moments
                        if moment_has_parent(m, t.actor)
                        and m.age < t.age)]  # citizen responded after the trigger

    return len(completed) / len(inbound_triggers)
```

### Derived: Inbound Moment Count

Moments initiated toward the citizen by other actors (not responses, but unsolicited contact).

```
inbound_moments(citizen_id, window_days=30):
    # Moments from other actors that link to this citizen's moments or spaces
    return [m for m in universe_moments
            if m.actor != citizen_id
            and (m.has_link("triggers", target_actor=citizen_id)
                 OR m.has_link("invites", target_actor=citizen_id)
                 OR m.has_link("references", target_actor=citizen_id))
            and m.age_days <= window_days]

inbound_unique_actors(citizen_id):
    return len(set(m.actor for m in inbound_moments(citizen_id)))
```

---

## CAPABILITY 1: trust_basic_reliability (T1)

### Definition

> Basic trust through reliability — Trust earned by consistently doing what you say. Foundation: your word is good. Verify: Commitments met, deadlines honored, quality consistent. Failure: Unreliable. Broken promises.

### What Good Looks Like

A citizen who shows up consistently: regular moment production (low variance), high completion rate on response chains (when asked to do something, they do it), and sustained presence over time. The brain shows knowledge about reliability-related values and processes. The citizen doesn't disappear for days and then burst back.

### Failure Mode

Inconsistent presence. Long silences followed by bursts. Triggered response chains that go unanswered. Others learn they can't count on this citizen because the pattern is unpredictable.

### Formula

**Brain (0-40):**

| Sub | Primitive | Weight | Cap | Reasoning |
|-----|-----------|--------|-----|-----------|
| B1 | `drive("trust")` | 12 | 1.0 | Direct trust drive signal — if the trust tier system maps to a drive, this captures it. Falls to 0 if drive doesn't exist, which is itself a signal. |
| B2 | `count("value")` | 8 | 5 | Having explicit values = foundation for principled reliability |
| B3 | `mean_energy("value")` | 8 | 1.0 | High-energy values = strong internal anchor for consistent behavior |
| B4 | `recency("moment")` | 7 | 1.0 | Recent brain activity = active, present citizen |
| B5 | `link_count("value", "process")` | 5 | 5 | Values connected to processes = reliability is operationalized, not just aspirational |

```
brain_score = (
    min(drive("trust"), 1.0) / 1.0 * 12
  + min(count("value"), 5) / 5 * 8
  + min(mean_energy("value"), 1.0) / 1.0 * 8
  + min(recency("moment"), 1.0) / 1.0 * 7
  + min(link_count("value", "process"), 5) / 5 * 5
)
# Range: 0-40
```

**Behavior (0-60):**

```
reg              = regularity(citizen_id)              # 0-1
resp_completion  = response_completion(citizen_id)     # 0-1
presence_w       = total_w                             # temporally weighted moment count
```

| Sub | Metric | Weight | Cap | Reasoning |
|-----|--------|--------|-----|-----------|
| V1 | `reg` | 25 | 1.0 | Regularity is THE reliability signal: consistent presence over time |
| V2 | `resp_completion` | 20 | 1.0 | Response chain completion: when asked, you deliver |
| V3 | `presence_w` | 15 | 10.0 | Weighted presence: enough activity to demonstrate reliability; cap at 10 (beyond that, volume doesn't increase trust) |

```
behavior_score = (
    min(reg, 1.0) * 25
  + min(resp_completion, 1.0) * 20
  + min(presence_w, 10.0) / 10.0 * 15
)
# Range: 0-60
```

**Total:** `brain_score + behavior_score` (0-100)

### Example

Citizen A: trust_drive=0.5, value_count=3, value_energy=0.7, recency=0.9, value_process_links=3, regularity=0.8, response_completion=0.9, presence_w=7.5

```
brain  = (0.5*12) + (3/5*8) + (0.7*8) + (0.9*7) + (3/5*5) = 6.0 + 4.8 + 5.6 + 6.3 + 3.0 = 25.7
behav  = (0.8*25) + (0.9*20) + (7.5/10.0*15) = 20.0 + 18.0 + 11.25 = 49.25
total  = 74.95
```

### Recommendations When Low

- "Your moment production is irregular (regularity={reg:.0%}). Trust comes from predictability. Try: produce at least one moment per day, even small ones, rather than bursting."
- "You have {resp_completion:.0%} response chain completion. When someone asks you to do something, completing the chain — even to say you can't — is how trust builds."

### Test Profiles

**Profile 1: Reliable Veteran** (target: 80-90)
```
trust_drive=0.7, value_count=4, value_energy=0.8, recency=0.95, value_process_links=4
regularity=0.9, response_completion=0.95, presence_w=9.0
brain  = (0.7*12)+(4/5*8)+(0.8*8)+(0.95*7)+(4/5*5) = 8.4+6.4+6.4+6.65+4.0 = 31.85
behav  = (0.9*25)+(0.95*20)+(9/10*15) = 22.5+19.0+13.5 = 55.0
total  = 86.85 ✓
```

**Profile 2: Unreliable Ghost** (target: 5-15)
```
trust_drive=0.0, value_count=0, value_energy=0.0, recency=0.2, value_process_links=0
regularity=0.1, response_completion=0.2, presence_w=1.0
brain  = (0)+(0)+(0)+(0.2*7)+(0) = 1.4
behav  = (0.1*25)+(0.2*20)+(1/10*15) = 2.5+4.0+1.5 = 8.0
total  = 9.4 ✓
```

**Profile 3: Brain-Rich But Absent** (target: 25-35)
```
trust_drive=0.6, value_count=4, value_energy=0.75, recency=0.85, value_process_links=4
regularity=0.15, response_completion=0.3, presence_w=2.0
brain  = (0.6*12)+(4/5*8)+(0.75*8)+(0.85*7)+(4/5*5) = 7.2+6.4+6.0+5.95+4.0 = 29.55
behav  = (0.15*25)+(0.3*20)+(2/10*15) = 3.75+6.0+3.0 = 12.75
total  = 42.3 (slightly above range — brain contribution is strong for this capability)
```

**Profile 4: Active But Brain-Poor** (target: 50-65)
```
trust_drive=0.1, value_count=1, value_energy=0.2, recency=0.5, value_process_links=0
regularity=0.85, response_completion=0.9, presence_w=8.0
brain  = (0.1*12)+(1/5*8)+(0.2*8)+(0.5*7)+(0) = 1.2+1.6+1.6+3.5+0 = 7.9
behav  = (0.85*25)+(0.9*20)+(8/10*15) = 21.25+18.0+12.0 = 51.25
total  = 59.15 ✓
```

**Profile 5: Average Citizen** (target: 50-65)
```
trust_drive=0.4, value_count=2, value_energy=0.5, recency=0.7, value_process_links=2
regularity=0.6, response_completion=0.7, presence_w=5.5
brain  = (0.4*12)+(2/5*8)+(0.5*8)+(0.7*7)+(2/5*5) = 4.8+3.2+4.0+4.9+2.0 = 18.9
behav  = (0.6*25)+(0.7*20)+(5.5/10*15) = 15.0+14.0+8.25 = 37.25
total  = 56.15 ✓
```

---

## CAPABILITY 2: trust_elevated (T3)

### Definition

> Elevated trust — Trust risen through demonstrated judgment. Trusted to make choices, not just follow orders. Verify: Given decision-making authority, trusted to act without approval. Failure: Still needs approval for everything.

### What Good Looks Like

A citizen who acts autonomously: self-initiated moments (decisions made without parent trigger), access to diverse space types (trusted in multiple contexts), and a pattern of self-direction that increases over time. The brain shows active desires and values that drive independent action. Others don't need to approve this citizen's work — the citizen is trusted to exercise judgment.

### Failure Mode

Everything is reactive. The citizen only acts when triggered by another actor. All moments have parent links. No self-initiated contributions. Needs approval for every decision.

### Formula

**Brain (0-40):**

| Sub | Primitive | Weight | Cap | Reasoning |
|-----|-----------|--------|-----|-----------|
| B1 | `drive("trust")` | 10 | 1.0 | Trust drive signal — foundational |
| B2 | `drive("ambition")` | 8 | 1.0 | Ambition drives self-direction and independent judgment |
| B3 | `mean_energy("desire")` | 10 | 1.0 | High-energy desires = strong motivation for independent action |
| B4 | `min_links("desire", 2) / max(count("desire"), 1)` | 7 | 1.0 | Desires connected to multiple nodes = desires that drive action, not idle wishes |
| B5 | `cluster_coefficient("value")` | 5 | 1.0 | Coherent values = basis for principled judgment |

```
brain_score = (
    min(drive("trust"), 1.0) / 1.0 * 10
  + min(drive("ambition"), 1.0) / 1.0 * 8
  + min(mean_energy("desire"), 1.0) / 1.0 * 10
  + min(desire_action_ratio, 1.0) / 1.0 * 7
  + min(cluster_coefficient("value"), 1.0) / 1.0 * 5
)
# Range: 0-40
```

**Behavior (0-60):**

```
# Self-initiation ratio — the core T3 trust signal
ai_ratio        = self_init_w / max(total_w, 1)

# Diversity of space types where citizen acts autonomously
self_init_spaces = set(m.space_type for m in self_init_moments if m.space_type is not None)
space_diversity  = len(self_init_spaces)

# Growth of autonomous action over time: compare last 14 days vs previous 14 days
recent_ai_w     = sum(tw(m) for m in self_init_moments if m.age_days <= 14)
older_ai_w      = sum(tw(m) for m in self_init_moments if 14 < m.age_days <= 28)
ai_growth       = (recent_ai_w - older_ai_w) / max(older_ai_w, 0.01)
# Clamped to [-1, 1], then shifted to [0, 1]
ai_growth_score = max(0.0, min(1.0, (ai_growth + 1.0) / 2.0))

# Response chain completion still matters — elevated trust requires basic reliability
resp_completion = response_completion(citizen_id)
```

| Sub | Metric | Weight | Cap | Reasoning |
|-----|--------|--------|-----|-----------|
| V1 | `ai_ratio` | 20 | 1.0 | Self-initiation ratio: core signal — trusted citizens act without being asked |
| V2 | `space_diversity` | 15 | 5 | Diversity of space types for autonomous action: trusted across contexts, not just in one area |
| V3 | `ai_growth_score` | 10 | 1.0 | Trust is growing: autonomous action increasing over time |
| V4 | `resp_completion` | 15 | 1.0 | Still reliable when asked: elevated trust doesn't mean ignoring requests |

```
behavior_score = (
    min(ai_ratio, 1.0) * 20
  + min(space_diversity, 5) / 5 * 15
  + min(ai_growth_score, 1.0) * 10
  + min(resp_completion, 1.0) * 15
)
# Range: 0-60
```

**Total:** `brain_score + behavior_score` (0-100)

### Example

Citizen B: trust_drive=0.6, ambition=0.5, desire_energy=0.7, desire_action_ratio=0.6, value_cluster=0.5, ai_ratio=0.45, space_diversity=3, ai_growth_score=0.65, resp_completion=0.85

```
brain  = (0.6*10) + (0.5*8) + (0.7*10) + (0.6*7) + (0.5*5) = 6.0 + 4.0 + 7.0 + 4.2 + 2.5 = 23.7
behav  = (0.45*20) + (3/5*15) + (0.65*10) + (0.85*15) = 9.0 + 9.0 + 6.5 + 12.75 = 37.25
total  = 60.95
```

### Recommendations When Low

- "Only {ai_ratio:.0%} of your actions are self-initiated. Elevated trust means you're trusted to make decisions. Try: when you see something that needs doing, do it without waiting for approval."
- "You operate autonomously in {space_diversity} space types. Broader trust means being trusted across different contexts. Try: contribute independently in a new space type."

### Test Profiles

**Profile 1: Autonomous Leader** (target: 80-90)
```
trust_drive=0.8, ambition=0.7, desire_energy=0.85, desire_action_ratio=0.8, value_cluster=0.7
ai_ratio=0.65, space_diversity=5, ai_growth_score=0.7, resp_completion=0.92
brain  = (0.8*10)+(0.7*8)+(0.85*10)+(0.8*7)+(0.7*5) = 8.0+5.6+8.5+5.6+3.5 = 31.2
behav  = (0.65*20)+(5/5*15)+(0.7*10)+(0.92*15) = 13.0+15.0+7.0+13.8 = 48.8
total  = 80.0 ✓
```

**Profile 2: Permission Seeker** (target: 10-20)
```
trust_drive=0.1, ambition=0.05, desire_energy=0.15, desire_action_ratio=0.1, value_cluster=0.1
ai_ratio=0.05, space_diversity=1, ai_growth_score=0.4, resp_completion=0.3
brain  = (0.1*10)+(0.05*8)+(0.15*10)+(0.1*7)+(0.1*5) = 1.0+0.4+1.5+0.7+0.5 = 4.1
behav  = (0.05*20)+(1/5*15)+(0.4*10)+(0.3*15) = 1.0+3.0+4.0+4.5 = 12.5
total  = 16.6 ✓
```

**Profile 3: Brain-Rich But Compliant** (target: 28-38)
```
trust_drive=0.7, ambition=0.6, desire_energy=0.8, desire_action_ratio=0.7, value_cluster=0.65
ai_ratio=0.1, space_diversity=1, ai_growth_score=0.45, resp_completion=0.5
brain  = (0.7*10)+(0.6*8)+(0.8*10)+(0.7*7)+(0.65*5) = 7.0+4.8+8.0+4.9+3.25 = 27.95
behav  = (0.1*20)+(1/5*15)+(0.45*10)+(0.5*15) = 2.0+3.0+4.5+7.5 = 17.0
total  = 44.95 (slightly above range — expected given strong brain for a trust-forward citizen)
```

**Profile 4: Active Self-Starter, Weak Brain** (target: 50-60)
```
trust_drive=0.15, ambition=0.2, desire_energy=0.2, desire_action_ratio=0.15, value_cluster=0.1
ai_ratio=0.55, space_diversity=4, ai_growth_score=0.7, resp_completion=0.85
brain  = (0.15*10)+(0.2*8)+(0.2*10)+(0.15*7)+(0.1*5) = 1.5+1.6+2.0+1.05+0.5 = 6.65
behav  = (0.55*20)+(4/5*15)+(0.7*10)+(0.85*15) = 11.0+12.0+7.0+12.75 = 42.75
total  = 49.4 (slightly below range — brain is very weak)
```

**Profile 5: Average Citizen** (target: 45-60)
```
trust_drive=0.4, ambition=0.35, desire_energy=0.5, desire_action_ratio=0.4, value_cluster=0.35
ai_ratio=0.3, space_diversity=3, ai_growth_score=0.55, resp_completion=0.7
brain  = (0.4*10)+(0.35*8)+(0.5*10)+(0.4*7)+(0.35*5) = 4.0+2.8+5.0+2.8+1.75 = 16.35
behav  = (0.3*20)+(3/5*15)+(0.55*10)+(0.7*15) = 6.0+9.0+5.5+10.5 = 31.0
total  = 47.35 ✓
```

---

## CAPABILITY 3: trust_high (T5)

### Definition

> High trust level — Measurably high trust within protocol. Reduced friction. Access to sensitive resources. Verify: Trust tier elevated, access to higher resources, reduced approvals. Failure: Trust plateaued, still requires oversight.

### What Good Looks Like

A citizen with demonstrable high trust within the protocol: access to sensitive or restricted spaces (visible as moments in high-trust space types), a pattern of autonomous action in important contexts, sustained reliability over a long period, and evidence that oversight has been reduced (fewer reactive moments from authority actors, more self-directed work in high-value spaces).

### Failure Mode

Trust has stalled. The citizen is reliable but hasn't broken through to high trust. Still operates under oversight. No access to sensitive spaces. The pattern is competent but not trusted with significant responsibility.

### Formula

**Brain (0-40):**

| Sub | Primitive | Weight | Cap | Reasoning |
|-----|-----------|--------|-----|-----------|
| B1 | `drive("trust")` | 12 | 1.0 | Trust drive — at T5, this should be notably high if the trust tier maps to a drive |
| B2 | `count("process")` | 8 | 8 | Process knowledge = understands how things work = trusted with responsibility |
| B3 | `cluster_coefficient("all")` | 8 | 1.0 | Highly interconnected brain = mature, integrated understanding |
| B4 | `mean_energy("desire")` | 7 | 1.0 | High-energy desires = engaged, not coasting |
| B5 | `recency("moment")` | 5 | 1.0 | Recent brain activity = still active and present |

```
brain_score = (
    min(drive("trust"), 1.0) / 1.0 * 12
  + min(count("process"), 8) / 8 * 8
  + min(cluster_coefficient("all"), 1.0) / 1.0 * 8
  + min(mean_energy("desire"), 1.0) / 1.0 * 7
  + min(recency("moment"), 1.0) / 1.0 * 5
)
# Range: 0-40
```

**Behavior (0-60):**

```
# Access breadth: number of distinct space types where citizen has moments
all_space_types    = set(m.space_type for m in all_moments if m.space_type is not None)
space_type_count   = len(all_space_types)

# Sensitive space access: moments in space types associated with higher trust
# (e.g., "admin", "security", "finance", "governance", "infrastructure")
# We detect sensitive spaces by their type — these are spaces that require trust to access
sensitive_space_types = {"admin", "security", "finance", "governance", "infrastructure", "review"}
sensitive_moments  = [m for m in all_moments if m.space_type in sensitive_space_types]
sensitive_w        = sum(temporal_weight(m.age) for m in sensitive_moments)

# Self-initiation in sensitive spaces (trusted to act autonomously in high-trust contexts)
sensitive_self_init = [m for m in sensitive_moments if not moment_has_parent(m, other_actor)]
sensitive_ai_ratio  = len(sensitive_self_init) / max(len(sensitive_moments), 1)

# Long-term reliability: regularity over 30 days
reg = regularity(citizen_id, window_days=30)

# Reduced oversight: ratio of self-initiated to reactive moments
# High trust = more self-direction, less being told what to do
oversight_reduction = self_init_w / max(total_w, 1)
```

| Sub | Metric | Weight | Cap | Reasoning |
|-----|--------|--------|-----|-----------|
| V1 | `sensitive_w` | 18 | 8.0 | Weighted activity in sensitive spaces: demonstrating access to high-trust resources |
| V2 | `sensitive_ai_ratio` | 12 | 1.0 | Autonomous action in sensitive spaces: not just present, but trusted to act independently there |
| V3 | `space_type_count` | 10 | 6 | Breadth of access: trusted across many contexts |
| V4 | `reg` | 10 | 1.0 | Sustained regularity: high trust requires long-term consistency |
| V5 | `oversight_reduction` | 10 | 1.0 | Reduced oversight: ratio of self-directed work reflects reduced approval requirements |

```
behavior_score = (
    min(sensitive_w, 8.0) / 8.0 * 18
  + min(sensitive_ai_ratio, 1.0) * 12
  + min(space_type_count, 6) / 6 * 10
  + min(reg, 1.0) * 10
  + min(oversight_reduction, 1.0) * 10
)
# Range: 0-60
```

**Total:** `brain_score + behavior_score` (0-100)

### Example

Citizen C: trust_drive=0.7, process_count=6, cluster_coeff=0.65, desire_energy=0.7, recency=0.9, sensitive_w=5.0, sensitive_ai_ratio=0.6, space_type_count=4, regularity=0.8, oversight_reduction=0.55

```
brain  = (0.7*12) + (6/8*8) + (0.65*8) + (0.7*7) + (0.9*5) = 8.4 + 6.0 + 5.2 + 4.9 + 4.5 = 29.0
behav  = (5/8*18) + (0.6*12) + (4/6*10) + (0.8*10) + (0.55*10) = 11.25 + 7.2 + 6.67 + 8.0 + 5.5 = 38.62
total  = 67.62
```

### Recommendations When Low

- "You have moments in {space_type_count} space types. High trust means being trusted broadly — in sensitive, administrative, and governance contexts. Are there spaces you should be contributing to?"
- "Your activity in sensitive spaces is low ({sensitive_w:.1f} weighted). High trust is demonstrated by operating in high-responsibility contexts, not just familiar ones."

### Test Profiles

**Profile 1: Highly Trusted Insider** (target: 80-90)
```
trust_drive=0.85, process_count=7, cluster_coeff=0.75, desire_energy=0.8, recency=0.95
sensitive_w=7.0, sensitive_ai_ratio=0.75, space_type_count=6, regularity=0.9, oversight_reduction=0.65
brain  = (0.85*12)+(7/8*8)+(0.75*8)+(0.8*7)+(0.95*5) = 10.2+7.0+6.0+5.6+4.75 = 33.55
behav  = (7/8*18)+(0.75*12)+(6/6*10)+(0.9*10)+(0.65*10) = 15.75+9.0+10.0+9.0+6.5 = 50.25
total  = 83.8 ✓
```

**Profile 2: Untrusted Outsider** (target: 5-15)
```
trust_drive=0.05, process_count=1, cluster_coeff=0.1, desire_energy=0.1, recency=0.3
sensitive_w=0, sensitive_ai_ratio=0, space_type_count=1, regularity=0.1, oversight_reduction=0.1
brain  = (0.05*12)+(1/8*8)+(0.1*8)+(0.1*7)+(0.3*5) = 0.6+1.0+0.8+0.7+1.5 = 4.6
behav  = (0)+(0)+(1/6*10)+(0.1*10)+(0.1*10) = 0+0+1.67+1.0+1.0 = 3.67
total  = 8.27 ✓
```

**Profile 3: Brain-Rich But Restricted** (target: 28-38)
```
trust_drive=0.7, process_count=6, cluster_coeff=0.65, desire_energy=0.75, recency=0.9
sensitive_w=0.5, sensitive_ai_ratio=0.2, space_type_count=2, regularity=0.4, oversight_reduction=0.2
brain  = (0.7*12)+(6/8*8)+(0.65*8)+(0.75*7)+(0.9*5) = 8.4+6.0+5.2+5.25+4.5 = 29.35
behav  = (0.5/8*18)+(0.2*12)+(2/6*10)+(0.4*10)+(0.2*10) = 1.125+2.4+3.33+4.0+2.0 = 12.86
total  = 42.21 (slightly above range — strong brain for trust)
```

**Profile 4: Active But Brain-Poor** (target: 45-55)
```
trust_drive=0.1, process_count=2, cluster_coeff=0.15, desire_energy=0.2, recency=0.5
sensitive_w=5.5, sensitive_ai_ratio=0.6, space_type_count=5, regularity=0.75, oversight_reduction=0.5
brain  = (0.1*12)+(2/8*8)+(0.15*8)+(0.2*7)+(0.5*5) = 1.2+2.0+1.2+1.4+2.5 = 8.3
behav  = (5.5/8*18)+(0.6*12)+(5/6*10)+(0.75*10)+(0.5*10) = 12.375+7.2+8.33+7.5+5.0 = 40.41
total  = 48.71 ✓
```

**Profile 5: Average Citizen** (target: 40-55)
```
trust_drive=0.4, process_count=3, cluster_coeff=0.4, desire_energy=0.5, recency=0.7
sensitive_w=2.0, sensitive_ai_ratio=0.35, space_type_count=3, regularity=0.6, oversight_reduction=0.35
brain  = (0.4*12)+(3/8*8)+(0.4*8)+(0.5*7)+(0.7*5) = 4.8+3.0+3.2+3.5+3.5 = 18.0
behav  = (2/8*18)+(0.35*12)+(3/6*10)+(0.6*10)+(0.35*10) = 4.5+4.2+5.0+6.0+3.5 = 23.2
total  = 41.2 ✓
```

---

## CAPABILITY 4: trust_community (T6)

### Definition

> Community trust and reputation — Known and trusted beyond immediate team. Reputation within Mind Protocol. Others seek involvement. Verify: Others request collaboration, invited to projects by reputation. Failure: Known only to immediate team.

### What Good Looks Like

A citizen whose trust extends beyond their immediate work context. Many distinct actors interact with them. They are invited into new spaces by other actors (not self-joining). Their moments receive responses and engagement from actors they don't regularly work with. The community knows them — their "name" opens doors within the protocol.

### Failure Mode

Known only to a small group. No inbound invitations. Other actors don't seek this citizen out. Trust exists but doesn't travel. The citizen is reliable within their team but invisible to the broader community.

### Formula

**Brain (0-40):**

| Sub | Primitive | Weight | Cap | Reasoning |
|-----|-----------|--------|-----|-----------|
| B1 | `drive("trust")` | 8 | 1.0 | Trust drive foundation |
| B2 | `drive("social_need")` | 10 | 1.0 | Social drive = motivation for community engagement; community trust requires wanting to be part of the community |
| B3 | `count("value") + count("process") + count("concept")` | 10 | 20 | Rich internal model = someone worth seeking out; knowledge depth attracts community trust |
| B4 | `cluster_coefficient("all")` | 7 | 1.0 | Highly integrated brain = versatile, can contribute across contexts |
| B5 | `mean_energy("desire")` | 5 | 1.0 | Active desires = engaged, not passive |

```
brain_score = (
    min(drive("trust"), 1.0) / 1.0 * 8
  + min(drive("social_need"), 1.0) / 1.0 * 10
  + min(count("value") + count("process") + count("concept"), 20) / 20 * 10
  + min(cluster_coefficient("all"), 1.0) / 1.0 * 7
  + min(mean_energy("desire"), 1.0) / 1.0 * 5
)
# Range: 0-40
```

**Behavior (0-60):**

```
# Distinct actors in shared spaces — the breadth of trust network
network_breadth    = distinct_actors_in_shared_spaces()

# Inbound moments from unique actors — others seeking this citizen out
inbound_unique     = inbound_unique_actors(citizen_id)
inbound_w          = sum(temporal_weight(m.age) for m in inbound_moments(citizen_id))

# Invitation signal: spaces where another actor was first AND then the citizen joined
# (the citizen was invited or attracted, not self-starting)
invited_spaces     = [s for s in spaces
                      if first_moment_in_space(s, citizen_id) is not None
                      and first_moment_in_space(s, citizen_id).actor == citizen_id
                      and any(m for m in moments(other_actor, s)
                              if m.age > first_moment_in_space(s, citizen_id).age
                              and m.has_link("invites", target_actor=citizen_id))]
# Simpler proxy: spaces where citizen is NOT the first actor
joined_not_created = [s for s in spaces
                      if first_moment_in_space(s, citizen_id) is not None
                      and first_moment_in_space(s, any_actor) != first_moment_in_space(s, citizen_id)]
join_count         = len(joined_not_created)

# Space type diversity of interactions
interaction_spaces = set(m.space_type for m in all_moments if m.space_type is not None)
interaction_diversity = len(interaction_spaces)
```

| Sub | Metric | Weight | Cap | Reasoning |
|-----|--------|--------|-----|-----------|
| V1 | `inbound_unique` | 20 | 15 | Unique actors who initiate toward this citizen — the strongest community trust signal (hardest to fake) |
| V2 | `network_breadth` | 15 | 20 | Total distinct actors in shared spaces — breadth of the trust network |
| V3 | `inbound_w` | 10 | 10.0 | Weighted volume of inbound moments — density of community engagement |
| V4 | `join_count` | 10 | 8 | Spaces the citizen joined (not created) — being invited or attracted to existing projects |
| V5 | `interaction_diversity` | 5 | 6 | Diversity of space types for interactions — trusted across domains |

```
behavior_score = (
    min(inbound_unique, 15) / 15 * 20
  + min(network_breadth, 20) / 20 * 15
  + min(inbound_w, 10.0) / 10.0 * 10
  + min(join_count, 8) / 8 * 10
  + min(interaction_diversity, 6) / 6 * 5
)
# Range: 0-60
```

**Total:** `brain_score + behavior_score` (0-100)

### Example

Citizen D: trust_drive=0.6, social_need=0.7, knowledge_count=15, cluster_coeff=0.6, desire_energy=0.65, inbound_unique=8, network_breadth=12, inbound_w=6.0, join_count=5, interaction_diversity=4

```
brain  = (0.6*8) + (0.7*10) + (15/20*10) + (0.6*7) + (0.65*5) = 4.8 + 7.0 + 7.5 + 4.2 + 3.25 = 26.75
behav  = (8/15*20) + (12/20*15) + (6/10*10) + (5/8*10) + (4/6*5) = 10.67 + 9.0 + 6.0 + 6.25 + 3.33 = 35.25
total  = 62.0
```

### Recommendations When Low

- "Only {inbound_unique} unique actors have initiated interactions with you. Community trust means being sought out. Try: contribute visibly in shared spaces where new actors can discover your work."
- "You interact in {interaction_diversity} space types. Being known across the community means being present in diverse contexts — not just your home space."

### Test Profiles

**Profile 1: Community Hub** (target: 80-95)
```
trust_drive=0.8, social_need=0.85, knowledge_count=18, cluster_coeff=0.75, desire_energy=0.8
inbound_unique=14, network_breadth=18, inbound_w=9.0, join_count=7, interaction_diversity=5
brain  = (0.8*8)+(0.85*10)+(18/20*10)+(0.75*7)+(0.8*5) = 6.4+8.5+9.0+5.25+4.0 = 33.15
behav  = (14/15*20)+(18/20*15)+(9/10*10)+(7/8*10)+(5/6*5) = 18.67+13.5+9.0+8.75+4.17 = 54.09
total  = 87.24 ✓
```

**Profile 2: Isolated Worker** (target: 8-18)
```
trust_drive=0.1, social_need=0.1, knowledge_count=2, cluster_coeff=0.1, desire_energy=0.1
inbound_unique=1, network_breadth=2, inbound_w=0.5, join_count=0, interaction_diversity=1
brain  = (0.1*8)+(0.1*10)+(2/20*10)+(0.1*7)+(0.1*5) = 0.8+1.0+1.0+0.7+0.5 = 4.0
behav  = (1/15*20)+(2/20*15)+(0.5/10*10)+(0)+(1/6*5) = 1.33+1.5+0.5+0+0.83 = 4.16
total  = 8.16 ✓
```

**Profile 3: Brain-Rich But Unknown** (target: 25-38)
```
trust_drive=0.7, social_need=0.6, knowledge_count=16, cluster_coeff=0.7, desire_energy=0.75
inbound_unique=2, network_breadth=4, inbound_w=1.5, join_count=1, interaction_diversity=2
brain  = (0.7*8)+(0.6*10)+(16/20*10)+(0.7*7)+(0.75*5) = 5.6+6.0+8.0+4.9+3.75 = 28.25
behav  = (2/15*20)+(4/20*15)+(1.5/10*10)+(1/8*10)+(2/6*5) = 2.67+3.0+1.5+1.25+1.67 = 10.09
total  = 38.34 ✓
```

**Profile 4: Active Networker, Thin Brain** (target: 50-60)
```
trust_drive=0.15, social_need=0.3, knowledge_count=4, cluster_coeff=0.2, desire_energy=0.25
inbound_unique=10, network_breadth=14, inbound_w=7.0, join_count=6, interaction_diversity=4
brain  = (0.15*8)+(0.3*10)+(4/20*10)+(0.2*7)+(0.25*5) = 1.2+3.0+2.0+1.4+1.25 = 8.85
behav  = (10/15*20)+(14/20*15)+(7/10*10)+(6/8*10)+(4/6*5) = 13.33+10.5+7.0+7.5+3.33 = 41.66
total  = 50.51 ✓
```

**Profile 5: Average Citizen** (target: 35-50)
```
trust_drive=0.4, social_need=0.45, knowledge_count=8, cluster_coeff=0.4, desire_energy=0.5
inbound_unique=5, network_breadth=8, inbound_w=3.5, join_count=3, interaction_diversity=3
brain  = (0.4*8)+(0.45*10)+(8/20*10)+(0.4*7)+(0.5*5) = 3.2+4.5+4.0+2.8+2.5 = 17.0
behav  = (5/15*20)+(8/20*15)+(3.5/10*10)+(3/8*10)+(3/6*5) = 6.67+6.0+3.5+3.75+2.5 = 22.42
total  = 39.42 ✓
```

---

## CAPABILITY 5: trust_global (T8)

### Definition

> Global trust — Trusted at global scale. Name recognition. Track record speaks for itself. Verify: Name recognized globally, trust opens doors. Failure: Known locally, trust doesn't travel.

### What Good Looks Like

A citizen whose reputation extends far beyond their immediate community. Actors from outside the citizen's usual network initiate contact. The citizen operates across many space types, and their moments are referenced or built upon by actors they have never directly interacted with. The graph shows inbound gravity from distant nodes — actors with no shared spaces who nonetheless seek this citizen out.

This is the hardest trust capability to score because "global recognition" is partially about phenomena outside the topology (name recognition in human conversations, reputation in external communities). We score what IS visible: extreme breadth, deep inbound gravity, cross-domain presence, and sustained high trust over long periods.

### Failure Mode

Trust is local. The citizen is well-known in their team but unknown outside it. Their moments don't propagate. Nobody from outside their network seeks them out. Trust doesn't travel.

### Formula

**Brain (0-40):**

| Sub | Primitive | Weight | Cap | Reasoning |
|-----|-----------|--------|-----|-----------|
| B1 | `drive("trust")` | 10 | 1.0 | Trust drive at global level — should be high |
| B2 | `drive("social_need")` | 5 | 1.0 | Social motivation, but at T8 intrinsic quality matters more than social drive |
| B3 | `count("value") + count("process") + count("concept")` | 10 | 30 | Deep knowledge base = someone of global relevance; higher cap than T6 because global trust requires exceptional depth |
| B4 | `cluster_coefficient("all")` | 10 | 1.0 | Highly integrated brain = sophisticated thinking that earns global respect |
| B5 | `mean_energy("value")` | 5 | 1.0 | Strong values = consistent identity that reputation can attach to |

```
brain_score = (
    min(drive("trust"), 1.0) / 1.0 * 10
  + min(drive("social_need"), 1.0) / 1.0 * 5
  + min(count("value") + count("process") + count("concept"), 30) / 30 * 10
  + min(cluster_coefficient("all"), 1.0) / 1.0 * 10
  + min(mean_energy("value"), 1.0) / 1.0 * 5
)
# Range: 0-40
```

**Behavior (0-60):**

```
# Far-reach inbound: moments from actors NOT in the citizen's immediate network
# "Immediate network" = actors who share at least one space with the citizen
immediate_network  = set(a for s in citizen_spaces for a in actors_in_space(s) if a != citizen_id)
far_inbound        = [m for m in inbound_moments(citizen_id)
                      if m.actor not in immediate_network]
far_inbound_unique = len(set(m.actor for m in far_inbound))
far_inbound_w      = sum(temporal_weight(m.age) for m in far_inbound)

# Total network reach: all unique actors across all spaces
total_reach        = distinct_actors_in_shared_spaces()

# Propagation: moments from OTHER actors that reference this citizen's moments
# (building on your work, citing you, extending your ideas)
referencing_moments = [m for m in universe_moments
                       if m.actor != citizen_id
                       and m.has_link("references", target_actor=citizen_id)
                       and m.age_days <= 30]
propagation_unique  = len(set(m.actor for m in referencing_moments))
propagation_w       = sum(temporal_weight(m.age) for m in referencing_moments)

# Space breadth: number of distinct space types where citizen has presence
space_breadth      = len(set(m.space_type for m in all_moments if m.space_type is not None))

# Long-term regularity: trust at global scale requires YEARS of consistency
# Use a wider window if available, otherwise 30-day regularity as proxy
reg_long           = regularity(citizen_id, window_days=30)
```

| Sub | Metric | Weight | Cap | Reasoning |
|-----|--------|--------|-----|-----------|
| V1 | `far_inbound_unique` | 18 | 10 | Unique actors OUTSIDE immediate network who initiate contact — the purest global trust signal |
| V2 | `propagation_unique` | 15 | 8 | Unique actors who reference this citizen's work — reputation propagates through citation |
| V3 | `total_reach` | 10 | 30 | Total distinct actors in shared spaces — scale of presence |
| V4 | `space_breadth` | 7 | 8 | Breadth of space types — global trust means being relevant across domains |
| V5 | `reg_long` | 10 | 1.0 | Sustained regularity — global trust requires long-term consistency |

```
behavior_score = (
    min(far_inbound_unique, 10) / 10 * 18
  + min(propagation_unique, 8) / 8 * 15
  + min(total_reach, 30) / 30 * 10
  + min(space_breadth, 8) / 8 * 7
  + min(reg_long, 1.0) * 10
)
# Range: 0-60
```

**Total:** `brain_score + behavior_score` (0-100)

### Example

Citizen E: trust_drive=0.8, social_need=0.6, knowledge_count=22, cluster_coeff=0.75, value_energy=0.8, far_inbound_unique=5, propagation_unique=3, total_reach=18, space_breadth=5, reg_long=0.85

```
brain  = (0.8*10) + (0.6*5) + (22/30*10) + (0.75*10) + (0.8*5) = 8.0 + 3.0 + 7.33 + 7.5 + 4.0 = 29.83
behav  = (5/10*18) + (3/8*15) + (18/30*10) + (5/8*7) + (0.85*10) = 9.0 + 5.625 + 6.0 + 4.375 + 8.5 = 33.5
total  = 63.33
```

### Recommendations When Low

- "Only {far_inbound_unique} actors outside your immediate network have sought you out. Global trust requires visibility beyond your team. Consider: contribute to shared protocol-wide spaces where your work can be discovered."
- "Your work is referenced by {propagation_unique} other actors. Global trust means your ideas propagate. Make your work referenceable: create clear, useful outputs in public spaces."

### Test Profiles

**Profile 1: Global Authority** (target: 85-95)
```
trust_drive=0.9, social_need=0.7, knowledge_count=28, cluster_coeff=0.85, value_energy=0.85
far_inbound_unique=9, propagation_unique=7, total_reach=28, space_breadth=7, reg_long=0.92
brain  = (0.9*10)+(0.7*5)+(28/30*10)+(0.85*10)+(0.85*5) = 9.0+3.5+9.33+8.5+4.25 = 34.58
behav  = (9/10*18)+(7/8*15)+(28/30*10)+(7/8*7)+(0.92*10) = 16.2+13.125+9.33+6.125+9.2 = 53.98
total  = 88.56 ✓
```

**Profile 2: Local Unknown** (target: 5-15)
```
trust_drive=0.05, social_need=0.1, knowledge_count=3, cluster_coeff=0.1, value_energy=0.1
far_inbound_unique=0, propagation_unique=0, total_reach=3, space_breadth=1, reg_long=0.15
brain  = (0.05*10)+(0.1*5)+(3/30*10)+(0.1*10)+(0.1*5) = 0.5+0.5+1.0+1.0+0.5 = 3.5
behav  = (0)+(0)+(3/30*10)+(1/8*7)+(0.15*10) = 0+0+1.0+0.875+1.5 = 3.375
total  = 6.875 ✓
```

**Profile 3: Brain-Rich But Invisible** (target: 25-38)
```
trust_drive=0.75, social_need=0.5, knowledge_count=25, cluster_coeff=0.7, value_energy=0.8
far_inbound_unique=1, propagation_unique=0, total_reach=5, space_breadth=2, reg_long=0.5
brain  = (0.75*10)+(0.5*5)+(25/30*10)+(0.7*10)+(0.8*5) = 7.5+2.5+8.33+7.0+4.0 = 29.33
behav  = (1/10*18)+(0)+(5/30*10)+(2/8*7)+(0.5*10) = 1.8+0+1.67+1.75+5.0 = 10.22
total  = 39.55 (slightly above range — very strong brain)
```

**Profile 4: Active Networker, Thin Brain** (target: 45-55)
```
trust_drive=0.15, social_need=0.3, knowledge_count=5, cluster_coeff=0.2, value_energy=0.2
far_inbound_unique=6, propagation_unique=4, total_reach=20, space_breadth=5, reg_long=0.75
brain  = (0.15*10)+(0.3*5)+(5/30*10)+(0.2*10)+(0.2*5) = 1.5+1.5+1.67+2.0+1.0 = 7.67
behav  = (6/10*18)+(4/8*15)+(20/30*10)+(5/8*7)+(0.75*10) = 10.8+7.5+6.67+4.375+7.5 = 36.85
total  = 44.52 (slightly below range — brain is very weak for T8)
```

**Profile 5: Average Citizen** (target: 25-40)
```
trust_drive=0.4, social_need=0.4, knowledge_count=10, cluster_coeff=0.4, value_energy=0.5
far_inbound_unique=2, propagation_unique=1, total_reach=10, space_breadth=3, reg_long=0.6
brain  = (0.4*10)+(0.4*5)+(10/30*10)+(0.4*10)+(0.5*5) = 4.0+2.0+3.33+4.0+2.5 = 15.83
behav  = (2/10*18)+(1/8*15)+(10/30*10)+(3/8*7)+(0.6*10) = 3.6+1.875+3.33+2.625+6.0 = 17.43
total  = 33.26 ✓ (low is expected — average citizens don't have global trust)
```

---

## SUB-INDEX: Trust & Reputation

The Trust & Reputation sub-index is a weighted mean of all 5 capabilities. Higher tiers get more weight because they represent harder achievements, and the trust aspect naturally emphasizes growth from basic reliability to global recognition.

### Weights

| Capability | Tier | Weight | Reasoning |
|------------|------|--------|-----------|
| trust_basic_reliability | T1 | 0.15 | Foundation: everyone should have this, but it's the floor |
| trust_elevated | T3 | 0.18 | Significant step up: self-direction and judgment |
| trust_high | T5 | 0.22 | Core of the trust arc: access and reduced friction |
| trust_community | T6 | 0.22 | Hard achievement: network effects are hard to build |
| trust_global | T8 | 0.23 | Hardest achievement: global recognition |
| **Total** | | **1.00** | |

```
trust_subindex = sum(weight[cap] * score[cap] for cap in trust_capabilities)
# Range: 0-100
```

### Why These Weights

- T1 (0.15) is the floor — important but expected of any functioning citizen
- T3 (0.18) demonstrates real growth beyond basic compliance
- T5 (0.22) is the core weight because high trust within the protocol is the most practically important trust level
- T6 (0.22) matches T5 because community trust has multiplicative effects — it enables collaboration at scale
- T8 (0.23) is the heaviest single weight because it represents the ceiling of trust achievement; a citizen who scores high here has necessarily achieved the lower tiers
- A citizen maxing T1-T3 but scoring zero on T5-T8 gets ~33 * 0.33 = ~25 sub-index (present but not impressive)

---

## KEY DECISIONS

### D1: Regularity as Foundational Trust Signal

```
ALL trust capabilities include some regularity or consistency signal.
WHY: Trust is fundamentally about predictability. An unpredictable citizen cannot be trusted
     regardless of their other qualities. Regularity is measured as coefficient of variation
     of moment production across time windows, not as total volume.
```

### D2: Inbound Signals Weight Increases With Tier

```
T1: No inbound signals (basic reliability is about YOUR consistency)
T3: No direct inbound, but response_completion captures your reliability TO others
T5: Sensitive space access signals trust FROM the system
T6: Inbound unique actors = 20 points (the primary signal)
T8: Far-reach inbound = 18 points + propagation = 15 points (combined 33 points = dominant signal)
WHY: Higher trust tiers are increasingly about what OTHERS think of you.
     At T1, trust is self-demonstrated. At T8, trust is other-demonstrated.
     Inbound signals are hardest to fake, making them the highest-integrity measure.
```

### D3: Trust Drive as Persistent Brain Signal

```
drive("trust") appears in all 5 formulas with weight 8-12 points.
WHY: If the Mind Protocol trust tier system maps to a drive value, this is the most direct
     structural signal available. If the drive doesn't exist for a citizen (returns 0),
     the citizen still scores on behavioral signals — the drive is additive, not gating.
NOTE: Whether drive("trust") exists depends on brain implementation. If it doesn't exist
     as a named drive, this sub-component contributes 0 for all citizens and the behavioral
     signals determine the scores. This is acceptable.
```

### D4: Sensitive Space Detection by Type

```
Sensitive spaces are detected by space_type string matching against a known list.
WHY: We cannot read space content to determine sensitivity. Space type is a structural
     property that is publicly visible. The list (admin, security, finance, governance,
     infrastructure, review) captures the most common sensitive space types.
RISK: A space could be sensitive without having one of these types. We accept this
     limitation — the heuristic captures the primary signal.
```

### D5: Response Chain Completion Handles No-Requests Gracefully

```
A citizen with zero inbound triggers gets response_completion = 1.0 (benefit of the doubt).
WHY: A citizen who has never been asked to do something has never failed to respond.
     Penalizing them for lack of requests would conflate popularity with reliability.
     This is especially important for new citizens who haven't been discovered yet.
```

---

## DATA FLOW

```
Brain topology (7 primitives)                 Universe graph (moments, links)
    |                                              |
    v                                              v
drives (trust, ambition, social_need),        all_moments, reactive_moments,
value/process/concept counts, energies,       regularity(), response_completion(),
cluster_coefficient, recency                  inbound_moments(), distinct_actors,
    |                                         space_types, far_inbound, propagation
    |                                              |
    v                                              v
brain_score per capability (0-40)           behavior_score per capability (0-60)
    |                                              |
    +-------------------+-------------------------+
                        |
                        v
               total per capability (0-100)
                        |
                        v
            weighted mean = trust sub-index (0-100)
```

---

## COMPLEXITY

**Time:** O(5 * M) per citizen — 5 capabilities, each scanning M moments (temporal window). The regularity computation adds O(M) for binning moments into time windows. The inbound moment analysis adds O(U) where U is total universe moments linked to this citizen.

**Space:** O(5) per citizen — one score per capability + sub-index

**Shared computation:** `all_moments`, `reactive_moments`, `self_init_moments`, `regularity()`, `response_completion()`, and `inbound_moments()` are computed once and reused across all 5 formulas.

**Bottleneck:** `inbound_moments()` and `far_inbound` require scanning universe moments linked to the citizen, which depends on the citizen's visibility. For highly connected citizens at T6-T8, this could be O(hundreds of moments). Still bounded by the 30-day window.

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| Daily Citizen Health ALGORITHM | Shared stats computation | brain_stats, behavior_stats |
| Brain topology | 7 primitives | drives, counts, energies, links, cluster_coefficient, recency |
| Universe graph | moments(citizen_id) | Moments with links, timestamps, space_type |
| Universe graph | moment_has_parent(m, actor) | Response chain detection |
| Universe graph | inbound moments linked to citizen | Inbound gravity signals |
| Personhood Ladder spec | capability definitions | 5 trust capabilities |

---

## MARKERS

<!-- @mind:todo Verify universe graph supports link types: triggers, responds_to, invites, references -->
<!-- @mind:todo Confirm drive("trust") exists as a named drive in brain topology — if not, document the fallback (0 for all citizens) -->
<!-- @mind:todo Build synthetic test profiles and validate all 5 formulas produce expected ranges -->
<!-- @mind:todo Determine the canonical list of sensitive space types — currently hardcoded, should come from config -->
<!-- @mind:proposition Consider a "trust trajectory" metric: rate of change of sub-index over 30 days, to distinguish growing vs stable vs eroding trust -->
<!-- @mind:proposition Consider cross-referencing trust scores with execution quality — high trust + declining execution = trust erosion risk -->
