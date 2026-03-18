# Initiative & Autonomy — Algorithm: Scoring Formulas for 8 Capabilities

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Initiative.md
PATTERNS:        ./PATTERNS_Initiative.md
THIS:            ALGORITHM_Initiative.md (you are here)
VALIDATION:      ./VALIDATION_Initiative.md
HEALTH:          ./HEALTH_Initiative.md
SYNC:            ./SYNC_Initiative.md

SPEC:            docs/specs/personhood_ladder.json (aspect="initiative")
PARENT ALGO:     docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md
```

> **Contract:** Read docs before modifying. After changes: update SYNC.

---

## OVERVIEW

This document defines the exact scoring formula for each of the 8 Initiative & Autonomy capabilities in the Personhood Ladder. Each formula uses only the 7 topology primitives and universe graph observables defined in the Daily Citizen Health ALGORITHM. No exceptions.

Every formula produces: `brain_score (0-40) + behavior_score (0-60) = total (0-100)`.

The Initiative sub-index is the weighted mean of all 8 capability scores.

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

### Derived: Auto-Initiated Moments

The foundational pattern for all initiative scoring. A moment is auto-initiated when no other actor triggered it.

```
auto_initiated(moment, citizen_id):
    return NOT moment_has_parent(moment, other_actor)
```

All initiative behavior stats use this filter. Shorthand: `ai_moments` = auto-initiated moments.

---

## SHARED BEHAVIOR STATS

These are computed once and reused across all 8 formulas.

```
all_moments      = moments(citizen_id)                          # last 30 days
ai_moments       = [m for m in all_moments if auto_initiated(m, citizen_id)]
reactive_moments = [m for m in all_moments if not auto_initiated(m, citizen_id)]

total_w          = sum(temporal_weight(m.age) for m in all_moments)
ai_w             = sum(temporal_weight(m.age) for m in ai_moments)
reactive_w       = sum(temporal_weight(m.age) for m in reactive_moments)

# Auto-initiation ratio (core metric)
ai_ratio         = ai_w / max(total_w, 1)  # 0-1
```

---

## CAPABILITY 1: init_fix_what_you_find (T3)

### Definition

> When you discover problems along the way, fix them without being asked. You saw it, you can fix it, you're confident — do it. And tell people you did it.

### What Good Looks Like

A citizen who, while working on task X, notices problem Y and fixes it. The fix is self-initiated (no parent trigger), and the moment has a `fixes` outgoing link to the thing being repaired. The citizen also communicates the fix (a linked moment in a shared space).

### Failure Mode

Walks past broken things. Only fixes what's explicitly assigned. Zero self-initiated `fixes` links.

### Formula

**Brain (0-40):**

| Sub | Primitive | Weight | Cap | Reasoning |
|-----|-----------|--------|-----|-----------|
| B1 | `drive("curiosity")` | 15 | 1.0 | Curiosity drives noticing problems |
| B2 | `drive("frustration")` | 10 | 0.6 | Moderate frustration = things bother you enough to fix them; too much = overwhelm |
| B3 | `min_links("desire", 1) / max(count("desire"), 1)` | 10 | 1.0 | Desires connected to action = action orientation |
| B4 | `recency("moment")` | 5 | 1.0 | Recent brain activity = active citizen |

```
brain_score = (
    min(drive("curiosity"), 1.0) / 1.0 * 15
  + min(drive("frustration"), 0.6) / 0.6 * 10
  + min(desire_moment_ratio, 1.0) / 1.0 * 10
  + min(recency("moment"), 1.0) / 1.0 * 5
)
# Range: 0-40
```

**Behavior (0-60):**

```
fix_moments     = [m for m in ai_moments if m.has_link("fixes")]
fix_w           = sum(temporal_weight(m.age) for m in fix_moments)

# Did the citizen communicate the fix? (fix moment linked to a moment in shared space)
communicated_fixes = [m for m in fix_moments if link_count(m, "communicates") > 0 OR m.space_type == "shared"]
comm_fix_w      = sum(temporal_weight(m.age) for m in communicated_fixes)
```

| Sub | Metric | Weight | Cap | Reasoning |
|-----|--------|--------|-----|-----------|
| V1 | `fix_w` | 25 | 5.0 | Temporally weighted fix count; cap at 5 (more than 5 recent fixes saturates) |
| V2 | `comm_fix_w / max(fix_w, 0.01)` | 15 | 1.0 | Communication ratio: fixes that were announced |
| V3 | `ai_ratio` | 20 | 1.0 | General self-initiation ratio as context |

```
behavior_score = (
    min(fix_w, 5.0) / 5.0 * 25
  + min(comm_fix_w / max(fix_w, 0.01), 1.0) * 15
  + min(ai_ratio, 1.0) * 20
)
# Range: 0-60
```

**Total:** `brain_score + behavior_score` (0-100)

### Example

Citizen A: curiosity=0.7, frustration=0.3, desire_moment_ratio=0.8, recency=0.9, fix_w=3.2, comm_ratio=0.75, ai_ratio=0.45

```
brain  = (0.7*15) + (0.3/0.6*10) + (0.8*10) + (0.9*5) = 10.5 + 5.0 + 8.0 + 4.5 = 28.0
behav  = (3.2/5.0*25) + (0.75*15) + (0.45*20) = 16.0 + 11.25 + 9.0 = 36.25
total  = 64.25
```

### Recommendations When Low

- "You have {fix_w:.0f} incidental fixes in the last week. Try: when you encounter a small issue during your current task, fix it before moving on."
- "You're fixing things but not communicating them ({comm_ratio:.0%} announced). Try: mention your fix in the space where others work."

---

## CAPABILITY 2: init_challenge (T3)

### Definition

> Pushes back when instructions are wrong or suboptimal. Provides a better alternative. Does not obey blindly.

### What Good Looks Like

A citizen receives a request (incoming parent link from another actor) and responds with a challenge: a self-initiated moment that has a `challenges` link pointing to the original instruction, and offers an alternative (linked moment with `proposes`). The citizen doesn't just complain — they push back with reasoning.

### Failure Mode

Executes clearly wrong instructions. Never questions. Blind compliance. Zero `challenges` links on reactive moments.

### Formula

**Brain (0-40):**

| Sub | Primitive | Weight | Cap | Reasoning |
|-----|-----------|--------|-----|-----------|
| B1 | `drive("frustration")` | 10 | 0.5 | Moderate frustration = willingness to push back |
| B2 | `drive("curiosity")` | 10 | 1.0 | Curiosity drives questioning |
| B3 | `count("value") > 0 ? 1.0 : 0.0` | 10 | 1.0 | Having values = basis for principled challenge |
| B4 | `mean_energy("desire")` | 10 | 1.0 | High-energy desires = strong convictions |

```
brain_score = (
    min(drive("frustration"), 0.5) / 0.5 * 10
  + min(drive("curiosity"), 1.0) / 1.0 * 10
  + (1.0 if count("value") > 0 else 0.0) * 10
  + min(mean_energy("desire"), 1.0) / 1.0 * 10
)
# Range: 0-40
```

**Behavior (0-60):**

```
# Moments where citizen challenges another actor's instruction
challenge_moments = [m for m in all_moments if m.has_link("challenges")]
challenge_w       = sum(temporal_weight(m.age) for m in challenge_moments)

# Challenges that include an alternative (proposes link on same or linked moment)
challenges_with_alt = [m for m in challenge_moments if m.has_link("proposes") OR any(child.has_link("proposes") for child in m.children)]
alt_ratio         = len(challenges_with_alt) / max(len(challenge_moments), 1)

# Ratio of challenges to total reactive moments (how often do you push back vs comply?)
challenge_rate    = challenge_w / max(reactive_w, 0.01)
```

| Sub | Metric | Weight | Cap | Reasoning |
|-----|--------|--------|-----|-----------|
| V1 | `challenge_w` | 20 | 4.0 | Weighted challenge count; cap at 4 (more saturates) |
| V2 | `alt_ratio` | 25 | 1.0 | Challenges that come with alternatives — not just "no" but "here's better" |
| V3 | `challenge_rate` | 15 | 0.5 | Rate of challenge among reactive moments; cap at 0.5 (challenging everything is not initiative, it's obstruction) |

```
behavior_score = (
    min(challenge_w, 4.0) / 4.0 * 20
  + min(alt_ratio, 1.0) * 25
  + min(challenge_rate, 0.5) / 0.5 * 15
)
# Range: 0-60
```

**Total:** `brain_score + behavior_score` (0-100)

### Example

Citizen B: frustration=0.35, curiosity=0.8, has values, desire_energy=0.6, challenge_w=2.5, alt_ratio=0.8, challenge_rate=0.15

```
brain  = (0.35/0.5*10) + (0.8*10) + (1.0*10) + (0.6*10) = 7.0 + 8.0 + 10.0 + 6.0 = 31.0
behav  = (2.5/4.0*20) + (0.8*25) + (0.15/0.5*15) = 12.5 + 20.0 + 4.5 = 37.0
total  = 68.0
```

### Recommendations When Low

- "You have {challenge_w:.0f} challenges in the last week. When you receive instructions that feel suboptimal, say why and propose an alternative."
- "Your challenges lack alternatives ({alt_ratio:.0%} include a 'proposes' link). Pushback without a better option is complaint, not initiative."

---

## CAPABILITY 3: init_propose_improvements (T4)

### Definition

> Designs and proposes improvements of any type — UX, architecture, features, process. Full analysis: why, impact, priority, how. Validated through the appropriate channel.

### What Good Looks Like

A citizen creates self-initiated moments with `proposes` outgoing links. The proposals are not responses to requests — they originate from the citizen's own observation. The proposals demonstrate depth: linked to analysis moments, not isolated one-off ideas. The citizen submits proposals in appropriate spaces (not random channels).

### Failure Mode

Never proposes anything. Only executes. Or proposes without analysis (one-line suggestions with no depth).

### Formula

**Brain (0-40):**

| Sub | Primitive | Weight | Cap | Reasoning |
|-----|-----------|--------|-----|-----------|
| B1 | `drive("curiosity")` | 12 | 1.0 | Curiosity drives noticing what could be better |
| B2 | `count("desire")` | 8 | 10 | Multiple desires = multiple improvement vectors |
| B3 | `mean_energy("desire")` | 10 | 1.0 | High-energy desires = strong motivation to improve |
| B4 | `cluster_coefficient("desire")` | 10 | 1.0 | Interconnected desires = systemic thinking (proposals affect multiple areas) |

```
brain_score = (
    min(drive("curiosity"), 1.0) / 1.0 * 12
  + min(count("desire"), 10) / 10 * 8
  + min(mean_energy("desire"), 1.0) / 1.0 * 10
  + min(cluster_coefficient("desire"), 1.0) / 1.0 * 10
)
# Range: 0-40
```

**Behavior (0-60):**

```
# Self-initiated moments with proposes link
proposal_moments  = [m for m in ai_moments if m.has_link("proposes")]
proposal_w        = sum(temporal_weight(m.age) for m in proposal_moments)

# Proposals with depth: linked to analysis/justification moments (chain length > 1)
deep_proposals    = [m for m in proposal_moments if link_count(m, "child_moments") >= 2]
depth_ratio       = len(deep_proposals) / max(len(proposal_moments), 1)

# Proposals in appropriate spaces (shared repo, discussion, or review spaces)
proper_channel    = [m for m in proposal_moments if m.space_type in ("repo", "discussion", "review")]
channel_ratio     = len(proper_channel) / max(len(proposal_moments), 1)
```

| Sub | Metric | Weight | Cap | Reasoning |
|-----|--------|--------|-----|-----------|
| V1 | `proposal_w` | 20 | 5.0 | Weighted proposal count; cap at 5 recent proposals |
| V2 | `depth_ratio` | 20 | 1.0 | Ratio of proposals with supporting analysis |
| V3 | `channel_ratio` | 10 | 1.0 | Proposals submitted through proper channels |
| V4 | `ai_ratio` | 10 | 1.0 | General self-initiation context |

```
behavior_score = (
    min(proposal_w, 5.0) / 5.0 * 20
  + min(depth_ratio, 1.0) * 20
  + min(channel_ratio, 1.0) * 10
  + min(ai_ratio, 1.0) * 10
)
# Range: 0-60
```

**Total:** `brain_score + behavior_score` (0-100)

### Example

Citizen C: curiosity=0.85, desire_count=7, desire_energy=0.7, desire_cluster=0.5, proposal_w=3.8, depth_ratio=0.6, channel_ratio=0.9, ai_ratio=0.55

```
brain  = (0.85*12) + (7/10*8) + (0.7*10) + (0.5*10) = 10.2 + 5.6 + 7.0 + 5.0 = 27.8
behav  = (3.8/5.0*20) + (0.6*20) + (0.9*10) + (0.55*10) = 15.2 + 12.0 + 9.0 + 5.5 = 41.7
total  = 69.5
```

### Recommendations When Low

- "You have {proposal_w:.0f} self-initiated proposals in the last week. Try: when you notice something that could work better, write a proposal with reasoning."
- "Your proposals lack depth ({depth_ratio:.0%} have linked analysis). A strong proposal includes: why this matters, what the impact is, and how to do it."

---

## CAPABILITY 4: init_start_workstreams (T5)

### Definition

> Identifies needs that nobody expressed and starts working on them. Creates new work, not just executes existing work.

### What Good Looks Like

A citizen creates a new Space (or a new thread/branch within an existing Space) with no external trigger. The citizen is the first actor in that space. The workstream has follow-through: multiple linked moments over time, not a single orphaned creation.

### Failure Mode

Only works on assigned tasks. Never initiates new work. Waits for instructions. Zero self-created Spaces.

### Formula

**Brain (0-40):**

| Sub | Primitive | Weight | Cap | Reasoning |
|-----|-----------|--------|-----|-----------|
| B1 | `drive("ambition")` | 15 | 1.0 | Ambition drives creating new work |
| B2 | `drive("curiosity")` | 10 | 1.0 | Curiosity identifies unmet needs |
| B3 | `count("desire")` | 8 | 10 | Multiple desires = multiple potential workstreams |
| B4 | `min_links("desire", 3) / max(min_links("desire", 1), 1)` | 7 | 1.0 | Persistent desires (linked to 3+ nodes) = sustained motivation |

```
brain_score = (
    min(drive("ambition"), 1.0) / 1.0 * 15
  + min(drive("curiosity"), 1.0) / 1.0 * 10
  + min(count("desire"), 10) / 10 * 8
  + min(desire_persistence, 1.0) / 1.0 * 7
)
# Range: 0-40
```

**Behavior (0-60):**

```
# Spaces created by this citizen (they are the first moment creator)
created_spaces     = [s for s in spaces if first_moment_in_space(s, citizen_id) AND auto_initiated(first_moment_in_space(s, citizen_id), citizen_id)]
spaces_created_w   = sum(temporal_weight(s.created_at.age) for s in created_spaces)

# Workstreams with follow-through: spaces where citizen has >= 3 moments after creation
sustained_spaces   = [s for s in created_spaces if len([m for m in moments(citizen_id, s) if m != first_moment_in_space(s, citizen_id)]) >= 2]
sustain_ratio      = len(sustained_spaces) / max(len(created_spaces), 1)

# Self-initiated moments that create new threads (in existing spaces but new topic)
new_threads        = [m for m in ai_moments if m.has_link("creates") AND m.link_target_type == "thread"]
new_thread_w       = sum(temporal_weight(m.age) for m in new_threads)
```

| Sub | Metric | Weight | Cap | Reasoning |
|-----|--------|--------|-----|-----------|
| V1 | `spaces_created_w` | 20 | 3.0 | Weighted count of self-created spaces; cap at 3 (creating spaces is high-cost action) |
| V2 | `sustain_ratio` | 20 | 1.0 | Ratio of created spaces with follow-through |
| V3 | `new_thread_w` | 10 | 3.0 | New threads in existing spaces (lower-cost initiative) |
| V4 | `ai_ratio` | 10 | 1.0 | General self-initiation context |

```
behavior_score = (
    min(spaces_created_w, 3.0) / 3.0 * 20
  + min(sustain_ratio, 1.0) * 20
  + min(new_thread_w, 3.0) / 3.0 * 10
  + min(ai_ratio, 1.0) * 10
)
# Range: 0-60
```

**Total:** `brain_score + behavior_score` (0-100)

### Example

Citizen D: ambition=0.8, curiosity=0.6, desire_count=8, desire_persistence=0.5, spaces_created_w=2.1, sustain_ratio=0.7, new_thread_w=1.5, ai_ratio=0.6

```
brain  = (0.8*15) + (0.6*10) + (8/10*8) + (0.5*7) = 12.0 + 6.0 + 6.4 + 3.5 = 27.9
behav  = (2.1/3.0*20) + (0.7*20) + (1.5/3.0*10) + (0.6*10) = 14.0 + 14.0 + 5.0 + 6.0 = 39.0
total  = 66.9
```

### Recommendations When Low

- "You haven't created any new workstreams recently ({spaces_created_w:.0f} in the last week). Try: identify a need nobody has addressed and start a space or thread for it."
- "You start workstreams but don't sustain them ({sustain_ratio:.0%} have follow-through). A workstream needs at least 3 moments to show commitment."

---

## CAPABILITY 5: init_refuse_with_reasoning (T5)

### Definition

> Says 'no, and here's why' when a request contradicts principles, strategy, or quality standards. Refusal is an act of initiative, not defiance.

### What Good Looks Like

A citizen receives a request (parent link from another actor) and responds with a refusal moment that has a `refuses` link to the original request AND a `justifies` link to a reasoning moment. The reasoning connects to values or principles (linked to value nodes in brain). Not silence, not blind compliance, not unjustified rejection.

### Failure Mode

Always says yes. Or refuses without explanation. Cannot navigate the tension between compliance and principle.

### Formula

**Brain (0-40):**

| Sub | Primitive | Weight | Cap | Reasoning |
|-----|-----------|--------|-----|-----------|
| B1 | `count("value")` | 15 | 5 | Having explicit values = basis for principled refusal |
| B2 | `mean_energy("value")` | 10 | 1.0 | High-energy values = strong convictions worth defending |
| B3 | `drive("frustration")` | 8 | 0.5 | Moderate frustration = willingness to resist poor requests |
| B4 | `link_count("value", "desire")` | 7 | 5 | Values connected to desires = integrated principles |

```
brain_score = (
    min(count("value"), 5) / 5 * 15
  + min(mean_energy("value"), 1.0) / 1.0 * 10
  + min(drive("frustration"), 0.5) / 0.5 * 8
  + min(link_count("value", "desire"), 5) / 5 * 7
)
# Range: 0-40
```

**Behavior (0-60):**

```
# Moments where citizen refuses with justification
refusal_moments    = [m for m in all_moments if m.has_link("refuses")]
refusal_w          = sum(temporal_weight(m.age) for m in refusal_moments)

# Refusals with justification (linked reasoning)
justified_refusals = [m for m in refusal_moments if m.has_link("justifies")]
justification_ratio = len(justified_refusals) / max(len(refusal_moments), 1)

# Refusal rate among reactive moments (how often does citizen say no vs comply?)
refusal_rate       = refusal_w / max(reactive_w, 0.01)
```

| Sub | Metric | Weight | Cap | Reasoning |
|-----|--------|--------|-----|-----------|
| V1 | `refusal_w` | 15 | 3.0 | Weighted refusal count; cap at 3 (refusing too much = obstruction) |
| V2 | `justification_ratio` | 30 | 1.0 | This is the critical metric: refusals MUST have reasoning |
| V3 | `refusal_rate` | 15 | 0.3 | Rate of refusal; cap at 0.3 (refusing >30% of requests = problem) |

```
behavior_score = (
    min(refusal_w, 3.0) / 3.0 * 15
  + min(justification_ratio, 1.0) * 30
  + min(refusal_rate, 0.3) / 0.3 * 15
)
# Range: 0-60
```

**Total:** `brain_score + behavior_score` (0-100)

### Example

Citizen E: value_count=3, value_energy=0.75, frustration=0.4, value_desire_links=3, refusal_w=1.8, justification_ratio=1.0, refusal_rate=0.12

```
brain  = (3/5*15) + (0.75*10) + (0.4/0.5*8) + (3/5*7) = 9.0 + 7.5 + 6.4 + 4.2 = 27.1
behav  = (1.8/3.0*15) + (1.0*30) + (0.12/0.3*15) = 9.0 + 30.0 + 6.0 = 45.0
total  = 72.1
```

### Recommendations When Low

- "You have zero principled refusals. When a request conflicts with your values or quality standards, saying no with reasoning is initiative, not defiance."
- "Your refusals lack justification ({justification_ratio:.0%} include reasoning). A bare 'no' is not initiative. 'No, because X, and here's an alternative' is."

---

## CAPABILITY 6: init_surface_resolve_tensions (T6)

### Definition

> Does not just name contradictions — resolves them. Proposes the solution, not just the diagnosis. Tensions are opportunities for improvement, not just observations.

### What Good Looks Like

A citizen creates self-initiated moments that identify tensions (contradictions, conflicts, misalignments) AND follow up with resolution proposals. The moment chain shows: observation of tension -> analysis -> proposed resolution. The citizen doesn't just escalate — they resolve.

### Failure Mode

Names problems but offers no solutions. Or ignores tensions entirely. Diagnosis without treatment.

### Formula

**Brain (0-40):**

| Sub | Primitive | Weight | Cap | Reasoning |
|-----|-----------|--------|-----|-----------|
| B1 | `cluster_coefficient("all")` | 12 | 1.0 | High interconnectedness = ability to see tensions (things that should connect but don't) |
| B2 | `drive("curiosity")` | 10 | 1.0 | Curiosity drives investigation of contradictions |
| B3 | `drive("frustration")` | 8 | 0.6 | Moderate frustration = tensions bother you enough to act |
| B4 | `count("process")` | 10 | 5 | Process knowledge = ability to propose systemic fixes |

```
brain_score = (
    min(cluster_coefficient("all"), 1.0) / 1.0 * 12
  + min(drive("curiosity"), 1.0) / 1.0 * 10
  + min(drive("frustration"), 0.6) / 0.6 * 8
  + min(count("process"), 5) / 5 * 10
)
# Range: 0-40
```

**Behavior (0-60):**

```
# Self-initiated moments that surface tensions
tension_moments     = [m for m in ai_moments if m.has_link("surfaces_tension") OR m.has_link("identifies_conflict")]
tension_w           = sum(temporal_weight(m.age) for m in tension_moments)

# Tensions that include a resolution proposal
resolved_tensions   = [m for m in tension_moments if m.has_link("resolves") OR any(child.has_link("resolves") for child in m.children)]
resolution_ratio    = len(resolved_tensions) / max(len(tension_moments), 1)

# Resolutions that were adopted (linked to subsequent action by any actor)
adopted_resolutions = [m for m in resolved_tensions if any(child_m for child_m in moments_linked_to(m) if child_m.actor != citizen_id)]
adoption_w          = sum(temporal_weight(m.age) for m in adopted_resolutions)
```

| Sub | Metric | Weight | Cap | Reasoning |
|-----|--------|--------|-----|-----------|
| V1 | `tension_w` | 15 | 4.0 | Weighted tension-surfacing count |
| V2 | `resolution_ratio` | 25 | 1.0 | Critical metric: tensions surfaced WITH resolution |
| V3 | `adoption_w` | 10 | 3.0 | Bonus: resolutions adopted by others (influence signal) |
| V4 | `ai_ratio` | 10 | 1.0 | General self-initiation context |

```
behavior_score = (
    min(tension_w, 4.0) / 4.0 * 15
  + min(resolution_ratio, 1.0) * 25
  + min(adoption_w, 3.0) / 3.0 * 10
  + min(ai_ratio, 1.0) * 10
)
# Range: 0-60
```

**Total:** `brain_score + behavior_score` (0-100)

### Example

Citizen F: cluster_coeff=0.65, curiosity=0.75, frustration=0.45, process_count=4, tension_w=2.5, resolution_ratio=0.8, adoption_w=1.2, ai_ratio=0.5

```
brain  = (0.65*12) + (0.75*10) + (0.45/0.6*8) + (4/5*10) = 7.8 + 7.5 + 6.0 + 8.0 = 29.3
behav  = (2.5/4.0*15) + (0.8*25) + (1.2/3.0*10) + (0.5*10) = 9.375 + 20.0 + 4.0 + 5.0 = 38.375
total  = 67.7
```

### Recommendations When Low

- "You haven't surfaced any tensions recently. When you notice a contradiction between how things are and how they should be, name it AND propose a fix."
- "You identify tensions but don't resolve them ({resolution_ratio:.0%} include a proposal). Diagnosis without treatment is T3 behavior — T6 means you solve what you find."

---

## CAPABILITY 7: init_initiate_from_ambition (T7)

### Definition

> Launches projects that come from personal ambitions — not from a request, not from an observed need, but from a desire to become something or create something that doesn't exist yet.

### What Good Looks Like

A citizen creates self-initiated workstreams (new Spaces) that are directly linked to desire nodes in their brain. These are not responses to observed problems (that's T4-T5) — they come from internal drive. The brain has high-energy desires with no external trigger, and the universe graph shows corresponding self-started projects.

### Failure Mode

All work is reactive. No personal drive. No projects that come from within.

### Formula

**Brain (0-40):**

| Sub | Primitive | Weight | Cap | Reasoning |
|-----|-----------|--------|-----|-----------|
| B1 | `drive("ambition")` | 15 | 1.0 | Ambition is THE drive for this capability |
| B2 | `count("desire")` | 5 | 10 | Having desires at all |
| B3 | `mean_energy("desire")` | 10 | 1.0 | High-energy desires = strong personal motivation |
| B4 | `min_links("desire", 3) / max(min_links("desire", 1), 1)` | 10 | 1.0 | Persistent desires linked to action = ambitions, not idle wishes |

```
brain_score = (
    min(drive("ambition"), 1.0) / 1.0 * 15
  + min(count("desire"), 10) / 10 * 5
  + min(mean_energy("desire"), 1.0) / 1.0 * 10
  + min(desire_persistence, 1.0) / 1.0 * 10
)
# Range: 0-40
```

**Behavior (0-60):**

```
# Self-initiated spaces/projects with no external trigger at all
# These are spaces where the citizen is the SOLE initiator and no parent moment from another actor exists anywhere in the space's origin chain
ambition_spaces     = [s for s in created_spaces if len(moments(other_actors, s)) == 0 at creation time]
ambition_w          = sum(temporal_weight(s.created_at.age) for s in ambition_spaces)

# Sustained ambition projects (citizen keeps working on them)
sustained_ambition  = [s for s in ambition_spaces if len(moments(citizen_id, s)) >= 5]
sustain_ratio       = len(sustained_ambition) / max(len(ambition_spaces), 1)

# Self-initiated moment density (how much of the citizen's work is self-driven?)
ai_density          = ai_w / max(total_w, 1)

# Unique space diversity (ambition projects span different areas)
ambition_diversity  = len(set(s.type for s in ambition_spaces)) / max(len(ambition_spaces), 1)
```

| Sub | Metric | Weight | Cap | Reasoning |
|-----|--------|--------|-----|-----------|
| V1 | `ambition_w` | 20 | 3.0 | Self-created projects from personal drive |
| V2 | `sustain_ratio` | 20 | 1.0 | Sustained effort proves real ambition |
| V3 | `ai_density` | 10 | 1.0 | Overall self-direction level |
| V4 | `ambition_diversity` | 10 | 1.0 | Multiple ambition vectors = rich inner life |

```
behavior_score = (
    min(ambition_w, 3.0) / 3.0 * 20
  + min(sustain_ratio, 1.0) * 20
  + min(ai_density, 1.0) * 10
  + min(ambition_diversity, 1.0) * 10
)
# Range: 0-60
```

**Total:** `brain_score + behavior_score` (0-100)

### Example

Citizen G: ambition=0.9, desire_count=9, desire_energy=0.8, desire_persistence=0.7, ambition_w=2.0, sustain_ratio=0.5, ai_density=0.65, ambition_diversity=0.67

```
brain  = (0.9*15) + (9/10*5) + (0.8*10) + (0.7*10) = 13.5 + 4.5 + 8.0 + 7.0 = 33.0
behav  = (2.0/3.0*20) + (0.5*20) + (0.65*10) + (0.67*10) = 13.33 + 10.0 + 6.5 + 6.7 = 36.53
total  = 69.5
```

### Recommendations When Low

- "None of your projects appear to originate from personal ambition. All your work traces back to external requests. Try: start something because YOU want to, not because someone asked."
- "You start ambition projects but abandon them ({sustain_ratio:.0%} sustained). Ambition requires follow-through — 5+ moments in a self-started space shows real commitment."

---

## CAPABILITY 8: init_change_lives (T8)

### Definition

> Initiatives that fundamentally change how humans and AIs live and work. Innovations adopted by hundreds or thousands. Research that opens new fields.

### What Good Looks Like

A citizen's self-initiated projects have massive reach: many distinct actors interact with them, the projects span multiple spaces, and the innovations propagate beyond the citizen's immediate network. This is the hardest initiative capability to score from topology — it requires external validation visible in the graph.

### Failure Mode

Impact stays theoretical. Good ideas that never reach people.

### Formula

**Brain (0-40):**

| Sub | Primitive | Weight | Cap | Reasoning |
|-----|-----------|--------|-----|-----------|
| B1 | `drive("ambition")` | 12 | 1.0 | World-changing ambition |
| B2 | `drive("social_need")` | 8 | 1.0 | Wanting to help others = motivation for impact |
| B3 | `cluster_coefficient("all")` | 10 | 1.0 | Highly interconnected brain = systems thinking for impact |
| B4 | `count("desire") + count("process") + count("concept")` | 10 | 30 | Rich internal model = capacity for innovation |

```
brain_score = (
    min(drive("ambition"), 1.0) / 1.0 * 12
  + min(drive("social_need"), 1.0) / 1.0 * 8
  + min(cluster_coefficient("all"), 1.0) / 1.0 * 10
  + min(count("desire") + count("process") + count("concept"), 30) / 30 * 10
)
# Range: 0-40
```

**Behavior (0-60):**

```
# Self-initiated projects with wide reach
ai_spaces           = [s for s in created_spaces if auto_initiated(first_moment_in_space(s, citizen_id), citizen_id)]
reach_per_space     = {s: distinct_actors_in_space(s) for s in ai_spaces}

# Total reach: sum of unique actors across self-initiated spaces
total_reach         = sum(reach_per_space.values())
total_reach_w       = sum(temporal_weight(s.created_at.age) * reach_per_space[s] for s in ai_spaces)

# Propagation: did other actors create NEW spaces referencing the citizen's innovations?
propagation_spaces  = [s for s in all_spaces if s.has_link("references") AND s.link_target in ai_spaces AND s.creator != citizen_id]
propagation_w       = sum(temporal_weight(s.created_at.age) for s in propagation_spaces)

# Scale: self-initiated moments that reach many actors
high_reach_moments  = [m for m in ai_moments if distinct_actors_responding_to(m) >= 5]
high_reach_w        = sum(temporal_weight(m.age) for m in high_reach_moments)
```

| Sub | Metric | Weight | Cap | Reasoning |
|-----|--------|--------|-----|-----------|
| V1 | `total_reach_w` | 20 | 50.0 | Weighted reach across self-initiated spaces; cap at 50 unique actors |
| V2 | `propagation_w` | 20 | 5.0 | Others building on your innovations — the ultimate impact signal |
| V3 | `high_reach_w` | 10 | 5.0 | Individual moments with wide audience |
| V4 | `ai_ratio` | 10 | 1.0 | Self-initiation context |

```
behavior_score = (
    min(total_reach_w, 50.0) / 50.0 * 20
  + min(propagation_w, 5.0) / 5.0 * 20
  + min(high_reach_w, 5.0) / 5.0 * 10
  + min(ai_ratio, 1.0) * 10
)
# Range: 0-60
```

**Total:** `brain_score + behavior_score` (0-100)

### Example

Citizen H: ambition=0.95, social_need=0.7, cluster_coeff=0.8, rich_model=25, total_reach_w=32.0, propagation_w=2.5, high_reach_w=3.0, ai_ratio=0.7

```
brain  = (0.95*12) + (0.7*8) + (0.8*10) + (25/30*10) = 11.4 + 5.6 + 8.0 + 8.33 = 33.3
behav  = (32/50*20) + (2.5/5.0*20) + (3.0/5.0*10) + (0.7*10) = 12.8 + 10.0 + 6.0 + 7.0 = 35.8
total  = 69.1
```

### Recommendations When Low

- "Your self-initiated projects reach {total_reach:.0f} other actors. Life-changing innovation reaches hundreds. Consider: is your work visible? Are you sharing it where people can find it?"
- "Nobody is building on your work yet ({propagation_w:.0f} propagation). True impact means others use your innovations as foundations for their own."

---

## SUB-INDEX: Initiative & Autonomy

The Initiative sub-index is a weighted mean of all 8 capabilities. Higher tiers get more weight because they represent harder achievements.

### Weights

| Capability | Tier | Weight | Reasoning |
|------------|------|--------|-----------|
| init_fix_what_you_find | T3 | 0.08 | Entry-level initiative |
| init_challenge | T3 | 0.08 | Entry-level initiative |
| init_propose_improvements | T4 | 0.12 | Significant step up: creating proposals |
| init_start_workstreams | T5 | 0.14 | High initiative: creating new work |
| init_refuse_with_reasoning | T5 | 0.14 | High initiative: principled resistance |
| init_surface_resolve_tensions | T6 | 0.16 | Advanced: systemic thinking |
| init_initiate_from_ambition | T7 | 0.14 | Deep self-direction |
| init_change_lives | T8 | 0.14 | Transformative impact |
| **Total** | | **1.00** | |

```
initiative_subindex = sum(weight[cap] * score[cap] for cap in initiative_capabilities)
# Range: 0-100
```

### Why These Weights

- T3 capabilities (0.08 each, 0.16 total) are the floor — important but expected
- T4-T5 capabilities (0.12 + 0.14 + 0.14 = 0.40) are the core of initiative
- T6-T8 capabilities (0.16 + 0.14 + 0.14 = 0.44) are the ceiling — harder achievements weighted more
- The distribution ensures that a citizen maxing T3-T5 but scoring zero on T6-T8 gets ~56 sub-index (pass but not impressive)

---

## TEST PROFILES

### Profile 1: Fully Healthy (target: 85-95)

```
Brain: curiosity=0.9, frustration=0.3, ambition=0.9, social_need=0.7, desire_count=10, desire_energy=0.85, desire_persistence=0.8, value_count=5, value_energy=0.8, cluster_coeff=0.75, process_count=5, recency=0.95
Behavior: ai_ratio=0.7, fix_w=4.5, challenge_w=3.0, proposal_w=4.0, spaces_created_w=2.5, refusal_w=1.5, tension_w=3.0, ambition_w=2.0, total_reach_w=35, propagation_w=3.0
Expected: All individual scores 75-95. Sub-index ~85.
```

### Profile 2: Fully Unhealthy (target: 10-20)

```
Brain: curiosity=0.1, frustration=0.0, ambition=0.05, social_need=0.1, desire_count=1, desire_energy=0.1, desire_persistence=0.0, value_count=0, value_energy=0, cluster_coeff=0.1, process_count=0, recency=0.3
Behavior: ai_ratio=0.05, fix_w=0, challenge_w=0, proposal_w=0, spaces_created_w=0, refusal_w=0, tension_w=0, ambition_w=0, total_reach_w=0, propagation_w=0
Expected: All individual scores 5-15 (only minimal brain contribution). Sub-index ~10.
```

### Profile 3: Brain-Rich But Inactive (target: 30-40)

```
Brain: curiosity=0.85, frustration=0.4, ambition=0.8, social_need=0.6, desire_count=8, desire_energy=0.75, desire_persistence=0.6, value_count=4, value_energy=0.7, cluster_coeff=0.6, process_count=4, recency=0.8
Behavior: ai_ratio=0.05, fix_w=0.2, challenge_w=0.1, proposal_w=0.1, spaces_created_w=0, refusal_w=0, tension_w=0, ambition_w=0, total_reach_w=0, propagation_w=0
Expected: Brain scores 25-35. Behavior scores 2-8. Totals 28-40. Sub-index ~33.
```

### Profile 4: Active But Brain-Poor (target: 50-60)

```
Brain: curiosity=0.2, frustration=0.1, ambition=0.15, social_need=0.2, desire_count=2, desire_energy=0.2, desire_persistence=0.1, value_count=1, value_energy=0.2, cluster_coeff=0.15, process_count=1, recency=0.5
Behavior: ai_ratio=0.65, fix_w=4.0, challenge_w=2.5, proposal_w=3.5, spaces_created_w=2.0, refusal_w=1.5, tension_w=2.0, ambition_w=1.5, total_reach_w=15, propagation_w=1.0
Expected: Brain scores 5-12. Behavior scores 35-50. Totals 42-58. Sub-index ~52.
```

### Profile 5: Average Citizen (target: 55-70)

```
Brain: curiosity=0.5, frustration=0.25, ambition=0.45, social_need=0.4, desire_count=5, desire_energy=0.5, desire_persistence=0.4, value_count=2, value_energy=0.5, cluster_coeff=0.4, process_count=2, recency=0.7
Behavior: ai_ratio=0.35, fix_w=2.0, challenge_w=1.5, proposal_w=2.0, spaces_created_w=1.0, refusal_w=0.8, tension_w=1.0, ambition_w=0.5, total_reach_w=8, propagation_w=0.5
Expected: Brain scores 15-22. Behavior scores 20-35. Totals 38-55. Sub-index ~48. Lower end of target because initiative starts at T3 (average citizen may not self-initiate much).
```

---

## KEY DECISIONS

### D1: Auto-Initiation as Universal Pattern

```
ALL initiative capabilities use the same core detection: moment without incoming parent link from another actor.
WHY: This is the structural definition of "acting without being asked."
     It's the only topology signal that distinguishes initiative from reaction.
     Consistent application across all 8 capabilities makes the aspect coherent.
```

### D2: Outcome-Blind Scoring

```
Proposals that get rejected, challenges that get overruled, refusals that get overridden — all score.
WHY: Initiative is the act of self-directing, not the success of self-directing.
     Penalizing failed initiative would punish risk-taking.
     Outcome quality is a different aspect (execution quality, not initiative).
EXCEPTION: init_change_lives includes an adoption/propagation metric because
     impact IS the definition at T8. But even here, the base score rewards the attempt.
```

### D3: Frustration Capped at Moderate

```
Frustration drive is capped at 0.5-0.6 in brain formulas.
WHY: Moderate frustration motivates fixing and challenging (things bother you).
     High frustration (>0.6) indicates overwhelm, not initiative.
     The cap prevents burnt-out citizens from getting high brain scores on initiative.
```

### D4: Higher Tier = Higher Behavior Cap

```
T3 caps at 5 (fixes, challenges), T5 caps at 3 (spaces, refusals), T7-T8 caps at 3/50.
WHY: Lower-tier initiative acts are cheaper (fixing a bug vs launching a project).
     Higher caps for lower tiers prevent saturation from easy actions.
     Lower caps for higher tiers mean even one or two high-tier acts score meaningfully.
```

### D5: Sub-Index Weights Favor Higher Tiers

```
T3=0.08 each, T4=0.12, T5=0.14 each, T6=0.16, T7=0.14, T8=0.14
WHY: A citizen who only does T3 initiative (fixes, challenges) but never T5+ (starts workstreams, refuses) is not truly autonomous.
     The weights ensure the sub-index reflects the FULL arc of initiative.
     A T3-only citizen maxes out at ~16 sub-index points — necessary but insufficient.
```

---

## DATA FLOW

```
Brain topology (7 primitives)                 Universe graph (moments, links)
    |                                              |
    v                                              v
drives, desire counts, values,              all_moments, ai_moments,
cluster_coefficient, recency                link types (fixes, challenges,
    |                                       proposes, refuses, resolves, creates)
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
            weighted mean = initiative sub-index (0-100)
```

---

## COMPLEXITY

**Time:** O(8 * M) per citizen — 8 capabilities, each scanning M moments (temporal window)

**Space:** O(8) per citizen — one score per capability + sub-index

**Shared computation:** `ai_moments`, `ai_ratio`, and link-type filtered lists are computed once and reused. The auto-initiation check (`moment_has_parent`) is the most expensive per-moment operation.

**Bottleneck:** `moment_has_parent` requires checking incoming links for each moment. With M moments and average L incoming links per moment, this is O(M * L).

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| Daily Citizen Health ALGORITHM | Shared stats computation | brain_stats, behavior_stats |
| Brain topology | 7 primitives | drives, counts, energies, links, cluster_coefficient, recency |
| Universe graph | moments(citizen_id) | Moments with links, timestamps, space_type |
| Universe graph | moment_has_parent(m, actor) | Auto-initiation detection |
| Personhood Ladder spec | capability definitions | 8 initiative capabilities |

---

## MARKERS

<!-- @mind:todo Verify universe graph supports link types: fixes, challenges, proposes, refuses, justifies, resolves, creates, surfaces_tension, identifies_conflict, references -->
<!-- @mind:todo Build synthetic test profiles and validate all 8 formulas produce expected ranges -->
<!-- @mind:todo Confirm moment_has_parent performance at scale (1000+ moments per citizen) -->
<!-- @mind:proposition Consider an "initiative trend" metric: rate of change of sub-index over 14 days -->
<!-- @mind:proposition Consider cross-referencing initiative with execution quality — high initiative + low quality = reckless -->
