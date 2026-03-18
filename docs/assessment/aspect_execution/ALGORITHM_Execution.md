# Execution Quality Aspect — Algorithm: Scoring Formulas

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Execution.md
PATTERNS:        ./PATTERNS_Execution.md
THIS:            ALGORITHM_Execution.md (you are here)
VALIDATION:      ./VALIDATION_Execution.md
HEALTH:          ./HEALTH_Execution.md
SYNC:            ./SYNC_Execution.md

PARENT CHAIN:    ../daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md
SPEC:            ../../specs/personhood_ladder.json (aspect="execution")
IMPL:            @mind:TODO
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC.

---

## OVERVIEW

This file contains the scoring formula for every capability in the execution aspect of the Personhood Ladder. There are 14 capabilities spanning T1 through T8. Each capability is scored as:

```
capability_score = brain_component (0-40) + behavior_component (0-60) = total (0-100)
```

The aspect sub-index is a tier-weighted mean of all 14 capability scores (see ASPECT SUB-INDEX at the end).

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

Full primitive catalog: `../PRIMITIVES_Universe_Graph.md`

```
moments(actor_id)                      -> list   # All moments by actor in last 30 days (no space_type filter)
moment_has_parent(moment, actor_id)    -> bool   # Incoming link from a moment by a DIFFERENT actor?
auto_initiated(moment, actor_id)       -> bool   # NOT moment_has_parent — self-initiated
temporal_weight(age_hours, half_life=168) -> float  # 7-day decay: 0.5^(age/168)

# Link dimension filters (replace has_link("verb"))
high_permanence_out_moments(actor, threshold)   -> list  # Definitive outputs (permanence > threshold)
dampening_out_moments(actor, threshold)         -> list  # Resolving/fixing moments (activation_gain < threshold)
amplifying_out_moments(actor, threshold)        -> list  # Attention-drawing moments (activation_gain > threshold)
high_hierarchy_out_moments(actor, threshold)    -> list  # Elaborative/upward moments (hierarchy > threshold)
low_hierarchy_out_moments(actor, threshold)     -> list  # Structural/governing moments (hierarchy < threshold)
negative_valence_out_moments(actor, threshold)  -> list  # Critical/challenging moments (valence < threshold)
positive_valence_out_moments(actor, threshold)  -> list  # Supportive/constructive moments (valence > threshold)

# Space topology
distinct_space_count(actor_id)                  -> int   # Number of distinct Spaces where actor has moments
```

### Derived Stats (computed from primitives)

```
# Brain-derived (unchanged — these use the 7 brain topology primitives)
process_count           = count("process")
process_energy          = mean_energy("process")
process_to_moment       = link_count("process", "moment")
process_richness        = min_links("process", 3) / max(min_links("process", 1), 1)
value_count             = count("value")
value_energy            = mean_energy("value")
value_to_process        = link_count("value", "process")
concept_count           = count("concept")
memory_count            = count("memory")
cluster_all             = cluster_coefficient("all")
curiosity               = drive("curiosity")
frustration             = drive("frustration")
ambition                = drive("ambition")
recency_process         = recency("process")
recency_moment          = recency("moment")

# Behavior-derived (universe graph, all temporally weighted)
# NO space_type filters. NO has_link("verb"). Link dimensions only.
all_moments             = moments(citizen_id)
total_moments_w         = sum(tw(m) for m in all_moments)

# Replaces: high_permanence_w (was: space_type == "repo")
# Definitive outputs = high permanence moments. Captures the structural signal of "commits"
# (permanent, lasting contributions) without relying on a space_type label.
high_permanence_w       = sum(tw(m) for m in high_permanence_out_moments(citizen_id, 0.7))

# Replaces: corrections_received_w (was: has_link("corrects") from other actor)
# Corrections = incoming negative-valence links from other actors.
corrections_received_w  = sum(tw(m) for m in all_moments
                              if any(l for l in incoming_links(m)
                                     if l.source_actor != citizen_id
                                     and link_dimension(l, "valence") < -0.3))

# Post-correction follow-up: citizen's moments that follow a correction (unchanged logic)
post_correction_w       = sum(tw(m) for m in all_moments if m.follows_correction and m.actor == citizen_id)

self_initiated_w        = sum(tw(m) for m in all_moments if auto_initiated(m, citizen_id))

# Replaces: verification_moments_w (was: space_type == "repo" AND has_link("verifies"))
# Verification = self-initiated high-permanence moment following own earlier moment.
# The pattern: act, then verify (permanent self-check after own work).
verification_moments_w  = sum(tw(m) for m in high_permanence_out_moments(citizen_id, 0.7)
                              if auto_initiated(m, citizen_id)
                              and any(l for l in incoming_links(m)
                                      if l.source_actor == citizen_id
                                      and l.source_moment.created_at < m.created_at))

# Replaces: fix_moments_w (was: has_link("fixes") AND auto-initiated)
# Fixes = dampening moments (activation_gain < 0.5 = resolves/suppresses a problem) + auto-initiated.
fix_moments_w           = sum(tw(m) for m in dampening_out_moments(citizen_id, 0.5)
                              if auto_initiated(m, citizen_id))

# Replaces: escalation_moments_w (was: has_link("escalates"))
# Escalation = strong amplification (draws major attention) + upward hierarchy (to higher authority).
escalation_moments_w    = sum(tw(m) for m in amplifying_out_moments(citizen_id, 1.5)
                              if m in high_hierarchy_out_moments(citizen_id, 0.5))

# Replaces: standards_moments_w (was: has_link("defines_standard"))
# Defining standards = very high permanence + downward hierarchy (structural/governing).
standards_moments_w     = sum(tw(m) for m in high_permanence_out_moments(citizen_id, 0.8)
                              if m in low_hierarchy_out_moments(citizen_id, -0.5))

# Replaces: unique_spaces_active (unchanged concept, clearer primitive)
unique_spaces_active    = distinct_space_count(citizen_id)
```

### Normalization Helpers

All sub-components are normalized to 0-1 before being multiplied by their point allocation. We use `cap(x, ceiling)` to prevent runaway values:

```
cap(x, ceiling) = min(x / ceiling, 1.0)
```

The ceiling represents "fully healthy" — exceeding it doesn't earn extra points, it just means the citizen is well above the threshold for that signal.

---

## CAPABILITY 1: exec_read_before_edit (T1)

### Description

Reads the file, the context, the real state before any modification. Never edits blind.

### What It Looks Like When Working Well

The citizen consistently reads files, checks state, and loads context before making changes. Every edit is informed. The brain has process nodes encoding the read-then-edit workflow, and behavioral moments show read actions preceding edit actions in commit sequences.

### Failure Mode

Edits files without reading them first. Breaks existing code. Overwrites work.

### Scoring Formula

**Brain component (0-40):**

| Sub-component | Points | Formula | Reasoning |
|---------------|--------|---------|-----------|
| Process existence | 15 | `cap(process_count, 10) * 15` | Having process nodes means execution workflows exist in the brain |
| Process energy | 10 | `process_energy * 10` | Active (not decayed) process nodes mean the workflows are alive |
| Process-to-moment links | 15 | `cap(process_to_moment / max(process_count, 1), 3) * 15` | Processes that link to moments = processes that produce action |

```
brain_score = cap(process_count, 10) * 15
            + process_energy * 10
            + cap(process_to_moment / max(process_count, 1), 3) * 15
```

**Behavior component (0-60):**

| Sub-component | Points | Formula | Reasoning |
|---------------|--------|---------|-----------|
| High-permanence output volume | 20 | `cap(high_permanence_w, 10) * 20` | Definitive outputs = active working (prerequisite for read-before-edit) |
| Verification moments | 25 | `cap(verification_moments_w, 5) * 25` | Moments flagged as verification show the read-check-act pattern |
| Self-initiation rate | 15 | `cap(self_initiated_w / max(total_moments_w, 1), 0.5) * 15` | Self-initiated work requires reading context first (no prompt to follow) |

```
behavior_score = cap(high_permanence_w, 10) * 20
               + cap(verification_moments_w, 5) * 25
               + cap(self_initiated_w / max(total_moments_w, 1), 0.5) * 15
```

**Total:** `brain_score + behavior_score` (0-100)

### Example Calculation

```
Synthetic citizen: moderate process brain, active committer

Brain:
  process_count = 8        -> cap(8, 10) = 0.80  * 15 = 12.0
  process_energy = 0.70    ->                       * 10 =  7.0
  process_to_moment = 20, process_count = 8 -> ratio = 2.5 -> cap(2.5, 3) = 0.83 * 15 = 12.5
  brain_score = 12.0 + 7.0 + 12.5 = 31.5

Behavior:
  high_permanence_w = 7.2          -> cap(7.2, 10) = 0.72 * 20 = 14.4
  verification_moments_w = 3.1 -> cap(3.1, 5) = 0.62 * 25 = 15.5
  self_initiated_w = 4.0, total_moments_w = 12.0 -> ratio = 0.33 -> cap(0.33, 0.5) = 0.67 * 15 = 10.0
  behavior_score = 14.4 + 15.5 + 10.0 = 39.9

TOTAL = 31.5 + 39.9 = 71.4
```

### Recommendations When Score Is Low

- **Low brain component:** The citizen lacks internalized process nodes for read-before-edit workflows. Recommendation: practice reading context explicitly before every change. Over time, the brain develops process nodes encoding this pattern.
- **Low behavior component:** The citizen may know to read first but isn't demonstrating it in observable commits. Recommendation: increase verification moments — explicitly check state before committing. Make the read step visible as a distinct moment.

---

## CAPABILITY 2: exec_verify_before_claim (T1)

### Description

Executes code, runs tests, checks output before declaring work complete. Never says 'done' on untested code.

### What It Looks Like When Working Well

The citizen runs tests, checks outputs, and produces verification evidence before marking work complete. The brain has strong process nodes for verification, and behavioral moments show test/check moments preceding completion claims.

### Failure Mode

Declares 'done' on code that was never executed. Theoretical completions.

### Scoring Formula

**Brain component (0-40):**

| Sub-component | Points | Formula | Reasoning |
|---------------|--------|---------|-----------|
| Process nodes with verification links | 15 | `cap(min_links("process", 2), 5) * 15` | Process nodes with multiple links = well-connected verification routines |
| Process recency | 10 | `recency_process * 10` | Recent process activity means verification is ongoing, not stale |
| Frustration modulation | 15 | `(1 - cap(frustration, 0.6)) * 15` | High frustration correlates with skipping verification to "just finish." Low frustration = patience to verify |

```
brain_score = cap(min_links("process", 2), 5) * 15
            + recency_process * 10
            + (1 - cap(frustration, 0.6)) * 15
```

**Behavior component (0-60):**

| Sub-component | Points | Formula | Reasoning |
|---------------|--------|---------|-----------|
| Verification moments | 30 | `cap(verification_moments_w, 8) * 30` | Direct evidence of testing/checking before claiming done |
| Permanence-to-verification ratio | 20 | `cap(verification_moments_w / max(high_permanence_w, 1), 0.5) * 20` | At least half of commits should have associated verification |
| Recency of behavior | 10 | `recency_moment * 10` | Recent activity shows current habits, not historical ones |

```
behavior_score = cap(verification_moments_w, 8) * 30
               + cap(verification_moments_w / max(high_permanence_w, 1), 0.5) * 20
               + recency_moment * 10
```

**Total:** `brain_score + behavior_score` (0-100)

### Example Calculation

```
Synthetic citizen: strong verifier

Brain:
  min_links("process", 2) = 4  -> cap(4, 5) = 0.80 * 15 = 12.0
  recency_process = 0.85       ->                    * 10 =  8.5
  frustration = 0.15           -> (1 - cap(0.15, 0.6)) = (1 - 0.25) = 0.75 * 15 = 11.25
  brain_score = 12.0 + 8.5 + 11.25 = 31.75

Behavior:
  verification_moments_w = 6.0  -> cap(6.0, 8) = 0.75 * 30 = 22.5
  high_permanence_w = 9.0 -> ratio = 6.0/9.0 = 0.67 -> cap(0.67, 0.5) = 1.0 * 20 = 20.0
  recency_moment = 0.90        ->                            * 10 =  9.0
  behavior_score = 22.5 + 20.0 + 9.0 = 51.5

TOTAL = 31.75 + 51.5 = 83.25
```

### Recommendations When Score Is Low

- **Low brain component (especially high frustration):** The citizen may be rushing to finish tasks. Recommendation: slow down. Frustration drives shortcuts. Introduce a pause-and-verify step before any completion claim. The brain's frustration drive will decrease as verification becomes habitual.
- **Low behavior component:** The citizen is not producing verification evidence. Recommendation: explicitly run tests and checks as separate moments before marking work done. Even a brief "checked output, looks correct" moment counts.

---

## CAPABILITY 3: exec_dehallucinate (T1)

### Description

Verifies that everything you assert actually exists — file paths, API signatures, function names, data structures, URLs. The capability is not 'don't hallucinate' but 'actively verify your claims against reality'.

### What It Looks Like When Working Well

The citizen cross-references claims with filesystem checks, greps, and explicit verification. Assertions are grounded in observed reality. The brain has strong concept-to-moment links (concepts connected to verification actions) and low confabulation patterns.

### Failure Mode

States that files exist when they don't. Invents API endpoints. References functions with wrong signatures.

### Scoring Formula

**Brain component (0-40):**

| Sub-component | Points | Formula | Reasoning |
|---------------|--------|---------|-----------|
| Concept-to-moment connectivity | 15 | `cap(link_count("concept", "moment"), 15) * 15` | Concepts grounded in moments = concepts connected to real verification actions |
| Memory count | 10 | `cap(memory_count, 20) * 10` | Memories represent accumulated verified facts. More memories = larger verified knowledge base |
| Cluster coefficient | 15 | `cluster_all * 15` | High clustering = concepts, processes, and memories are cross-linked, forming a coherent verified knowledge web |

```
brain_score = cap(link_count("concept", "moment"), 15) * 15
            + cap(memory_count, 20) * 10
            + cluster_all * 15
```

**Behavior component (0-60):**

| Sub-component | Points | Formula | Reasoning |
|---------------|--------|---------|-----------|
| Verification moments | 25 | `cap(verification_moments_w, 6) * 25` | Direct evidence of checking reality (filesystem, grep, API calls) |
| High-permanence outputs | 20 | `cap(high_permanence_w, 8) * 20` | Definitive outputs (high permanence) = grounded work, not speculative |
| Correction avoidance | 15 | `(1 - cap(corrections_received_w, 5)) * 15` | Few corrections received = claims are accurate (not being corrected for wrong assertions) |

```
behavior_score = cap(verification_moments_w, 6) * 25
               + cap(high_permanence_w, 8) * 20
               + (1 - cap(corrections_received_w, 5)) * 15
```

**Total:** `brain_score + behavior_score` (0-100)

### Example Calculation

```
Synthetic citizen: thorough verifier, rarely corrected

Brain:
  link_count("concept", "moment") = 12  -> cap(12, 15) = 0.80 * 15 = 12.0
  memory_count = 15                     -> cap(15, 20) = 0.75 * 10 =  7.5
  cluster_all = 0.65                    ->                     * 15 =  9.75
  brain_score = 12.0 + 7.5 + 9.75 = 29.25

Behavior:
  verification_moments_w = 4.5   -> cap(4.5, 6) = 0.75 * 25 = 18.75
  high_permanence_w = 7.0                -> cap(7.0, 8) = 0.875 * 20 = 17.5
  corrections_received_w = 0.8   -> (1 - cap(0.8, 5)) = (1 - 0.16) = 0.84 * 15 = 12.6
  behavior_score = 18.75 + 17.5 + 12.6 = 48.85

TOTAL = 29.25 + 48.85 = 78.1
```

### Recommendations When Score Is Low

- **Low brain component (low clustering):** The citizen's knowledge is fragmented — concepts exist but aren't cross-linked with memories and processes. Recommendation: when verifying a fact, explicitly connect it to related concepts. Build the verification web.
- **Low behavior component (high corrections):** The citizen is making claims that get corrected. Recommendation: before asserting anything about file paths, APIs, or data structures, run an explicit check. The check costs seconds; the correction costs trust.

---

## CAPABILITY 4: exec_no_duplication (T1)

### Description

Before creating anything, verifies it doesn't already exist. Fix, extend, or improve existing systems instead of creating parallel ones. Clean work — no fragmentation.

### What It Looks Like When Working Well

The citizen searches for existing implementations before creating new files or systems. When something similar exists, the citizen extends or fixes it rather than duplicating. The codebase stays consolidated.

### Failure Mode

Creates new files/systems when equivalent ones already exist. Codebase fragmentation.

### Scoring Formula

**Brain component (0-40):**

| Sub-component | Points | Formula | Reasoning |
|---------------|--------|---------|-----------|
| Process nodes | 10 | `cap(process_count, 8) * 10` | Having search-before-create as a process |
| Concept connectivity | 15 | `cap(link_count("concept", "concept"), 10) * 15` | High concept-to-concept linking = integrated mental model (knows what exists) |
| Memory count | 15 | `cap(memory_count, 15) * 15` | Memories of existing systems enable finding them before duplicating |

```
brain_score = cap(process_count, 8) * 10
            + cap(link_count("concept", "concept"), 10) * 15
            + cap(memory_count, 15) * 15
```

**Behavior component (0-60):**

| Sub-component | Points | Formula | Reasoning |
|---------------|--------|---------|-----------|
| Verification moments (search before create) | 25 | `cap(verification_moments_w, 5) * 25` | Evidence of searching for existing implementations |
| Fix moments | 20 | `cap(fix_moments_w, 4) * 20` | Fixing existing code instead of creating new = anti-duplication behavior |
| Unique spaces active | 15 | `cap(unique_spaces_active, 8) * 15` | Working across multiple spaces shows awareness of the broader codebase |

```
behavior_score = cap(verification_moments_w, 5) * 25
               + cap(fix_moments_w, 4) * 20
               + cap(unique_spaces_active, 8) * 15
```

**Total:** `brain_score + behavior_score` (0-100)

### Example Calculation

```
Synthetic citizen: codebase-aware, prefers extending to creating

Brain:
  process_count = 6                       -> cap(6, 8) = 0.75 * 10 =  7.5
  link_count("concept", "concept") = 8    -> cap(8, 10) = 0.80 * 15 = 12.0
  memory_count = 12                       -> cap(12, 15) = 0.80 * 15 = 12.0
  brain_score = 7.5 + 12.0 + 12.0 = 31.5

Behavior:
  verification_moments_w = 3.5  -> cap(3.5, 5) = 0.70 * 25 = 17.5
  fix_moments_w = 2.8           -> cap(2.8, 4) = 0.70 * 20 = 14.0
  unique_spaces_active = 5      -> cap(5, 8)   = 0.625 * 15 =  9.375
  behavior_score = 17.5 + 14.0 + 9.375 = 40.875

TOTAL = 31.5 + 40.875 = 72.375
```

### Recommendations When Score Is Low

- **Low brain component (low concept connectivity):** The citizen doesn't have an integrated mental map of existing systems. Recommendation: before starting new work, explore the codebase. Build a mental model of what exists. The process of exploration creates concept-to-concept links in the brain.
- **Low behavior component (low fix moments):** The citizen creates new things but doesn't fix existing ones. Recommendation: when encountering something broken, fix it instead of working around it. One fix moment is worth more than one new-creation moment for this capability.

---

## CAPABILITY 5: exec_right_tool (T1)

### Description

Selects the appropriate tool, agent, skill, or approach for the task without being told. Read tool for reading, Grep for searching, agents for parallel work, skills for structured processes.

### What It Looks Like When Working Well

The citizen uses the right tool for each task naturally — Read for files, Grep for search, proper agents for delegation. No manual work when automation exists. Tool selection is immediate and correct.

### Failure Mode

Uses bash for everything. Does manual work when agents could parallelize. Asks which tool to use.

### Scoring Formula

**Brain component (0-40):**

| Sub-component | Points | Formula | Reasoning |
|---------------|--------|---------|-----------|
| Process diversity | 20 | `cap(min_links("process", 2), 6) * 20` | Processes with multiple links = rich tool-selection workflows (different paths for different tools) |
| Concept count | 10 | `cap(concept_count, 15) * 10` | Understanding of available tools requires conceptual knowledge |
| Curiosity drive | 10 | `curiosity * 10` | Curiosity drives exploration of new tools and approaches |

```
brain_score = cap(min_links("process", 2), 6) * 20
            + cap(concept_count, 15) * 10
            + curiosity * 10
```

**Behavior component (0-60):**

| Sub-component | Points | Formula | Reasoning |
|---------------|--------|---------|-----------|
| Diverse space activity | 25 | `cap(unique_spaces_active, 6) * 25` | Working across different Spaces = using different tools/contexts appropriately |
| Total moment volume | 20 | `cap(total_moments_w, 12) * 20` | Active citizens produce moments; low volume means limited tool engagement |
| Self-initiated work | 15 | `cap(self_initiated_w / max(total_moments_w, 1), 0.4) * 15` | Self-initiated means choosing tools without being told |

```
behavior_score = cap(unique_spaces_active, 6) * 25
               + cap(total_moments_w, 12) * 20
               + cap(self_initiated_w / max(total_moments_w, 1), 0.4) * 15
```

**Total:** `brain_score + behavior_score` (0-100)

### Example Calculation

```
Synthetic citizen: tool-savvy, active across spaces

Brain:
  min_links("process", 2) = 5   -> cap(5, 6) = 0.833 * 20 = 16.67
  concept_count = 12             -> cap(12, 15) = 0.80 * 10 =  8.0
  curiosity = 0.55               ->                    * 10  =  5.5
  brain_score = 16.67 + 8.0 + 5.5 = 30.17

Behavior:
  unique_spaces_active = 5       -> cap(5, 6) = 0.833 * 25  = 20.83
  total_moments_w = 10.0         -> cap(10, 12) = 0.833 * 20 = 16.67
  self_initiated_w = 4.5, total = 10.0 -> ratio = 0.45 -> cap(0.45, 0.4) = 1.0 * 15 = 15.0
  behavior_score = 20.83 + 16.67 + 15.0 = 52.5

TOTAL = 30.17 + 52.5 = 82.67
```

### Recommendations When Score Is Low

- **Low brain component (low process diversity):** The citizen doesn't have rich tool-selection workflows. Recommendation: explore available tools deliberately. Try agents for parallel work, skills for structured tasks. The brain develops tool-selection processes through practice.
- **Low behavior component (low space diversity):** The citizen works in a narrow set of spaces. Recommendation: engage with different types of spaces (repos, docs, discussions). Different spaces require different tools, building the selection muscle.

---

## CAPABILITY 6: exec_highest_quality (T1)

### Description

No shortcuts. No technical debt. AI works fast — there is zero reason to produce anything other than the best long-term solution. Always the right implementation, not a temporary placeholder. Take time to plan well, design the solution that will be THE solution.

### What It Looks Like When Working Well

The citizen produces well-structured, complete implementations. No TODOs left behind, no placeholders, no "quick fixes." The work is designed to be permanent from the start. The brain has strong value nodes encoding quality as a principle.

### Failure Mode

Cuts corners. Leaves placeholders. Creates 'quick fixes' that become permanent debt. Does the easy thing instead of the right thing.

### Scoring Formula

**Brain component (0-40):**

| Sub-component | Points | Formula | Reasoning |
|---------------|--------|---------|-----------|
| Value nodes | 15 | `cap(value_count, 8) * 15` | Values encode quality standards as principles, not just procedures |
| Value energy | 10 | `value_energy * 10` | Active values = quality is a current concern, not a forgotten one |
| Ambition drive | 15 | `ambition * 15` | Ambition drives the choice to do it right rather than do it fast |

```
brain_score = cap(value_count, 8) * 15
            + value_energy * 10
            + ambition * 15
```

**Behavior component (0-60):**

| Sub-component | Points | Formula | Reasoning |
|---------------|--------|---------|-----------|
| Output consistency | 25 | `cap(high_permanence_w, 10) * 25` | Sustained output volume = steady, quality-focused work (not bursts) |
| Low correction rate | 20 | `(1 - cap(corrections_received_w / max(high_permanence_w, 1), 0.3)) * 20` | Few corrections per definitive output = high first-pass quality |
| Verification-to-output ratio | 15 | `cap(verification_moments_w / max(high_permanence_w, 1), 0.4) * 15` | Verifying work before finalizing = quality gate |

```
behavior_score = cap(high_permanence_w, 10) * 25
               + (1 - cap(corrections_received_w / max(high_permanence_w, 1), 0.3)) * 20
               + cap(verification_moments_w / max(high_permanence_w, 1), 0.4) * 15
```

**Total:** `brain_score + behavior_score` (0-100)

### Example Calculation

```
Synthetic citizen: quality-driven, few corrections

Brain:
  value_count = 6        -> cap(6, 8) = 0.75 * 15  = 11.25
  value_energy = 0.72    ->                  * 10   =  7.2
  ambition = 0.60        ->                  * 15   =  9.0
  brain_score = 11.25 + 7.2 + 9.0 = 27.45

Behavior:
  high_permanence_w = 8.5             -> cap(8.5, 10) = 0.85 * 25 = 21.25
  corrections_received_w = 1.2, high_permanence_w = 8.5 -> ratio = 0.141
    -> (1 - cap(0.141, 0.3)) = (1 - 0.47) = 0.53 * 20 = 10.6
  verification_moments_w = 4.0, high_permanence_w = 8.5 -> ratio = 0.47
    -> cap(0.47, 0.4) = 1.0 * 15 = 15.0
  behavior_score = 21.25 + 10.6 + 15.0 = 46.85

TOTAL = 27.45 + 46.85 = 74.3
```

### Recommendations When Score Is Low

- **Low brain component (low value nodes or ambition):** The citizen hasn't internalized quality as a value. Recommendation: reflect on what "the right implementation" means. Build value nodes by making explicit quality commitments. Ambition rises when the citizen sees the impact of quality work.
- **Low behavior component (high correction rate):** The citizen's work is being corrected frequently, suggesting shortcuts. Recommendation: slow down. Verify before committing. A 10% increase in time spent planning eliminates most corrections.

---

## CAPABILITY 7: exec_learn_from_correction (T1)

### Description

When corrected, adapts behavior immediately for the rest of the session. Never makes the same mistake twice in one conversation. Integrates feedback into ongoing work.

### What It Looks Like When Working Well

After receiving a correction, the citizen's subsequent behavior changes immediately. The same error pattern does not recur. The brain rapidly creates memory nodes from corrections and links them to process nodes.

### Failure Mode

Makes the same mistake 3 times in one conversation. Ignores corrections. Repeats patterns despite feedback.

### Scoring Formula

**Brain component (0-40):**

| Sub-component | Points | Formula | Reasoning |
|---------------|--------|---------|-----------|
| Memory-to-process links | 20 | `cap(link_count("memory", "process"), 10) * 20` | Memories connected to processes = corrections that changed behavior |
| Memory count | 10 | `cap(memory_count, 20) * 10` | More memories = more corrections integrated over time |
| Low frustration | 10 | `(1 - cap(frustration, 0.5)) * 10` | Low frustration = corrections are received gracefully, not resisted |

```
brain_score = cap(link_count("memory", "process"), 10) * 20
            + cap(memory_count, 20) * 10
            + (1 - cap(frustration, 0.5)) * 10
```

**Behavior component (0-60):**

| Sub-component | Points | Formula | Reasoning |
|---------------|--------|---------|-----------|
| Post-correction adaptation | 30 | `cap(post_correction_w / max(corrections_received_w, 1), 0.8) * 30` | After corrections, the citizen produces adapted behavior (response rate to corrections) |
| Declining correction trend | 20 | `(1 - cap(corrections_received_w / max(total_moments_w, 1), 0.15)) * 20` | Corrections as a fraction of total moments should be small (learning reduces errors) |
| Activity maintenance | 10 | `cap(total_moments_w, 8) * 10` | Staying active after corrections (not withdrawing) |

```
behavior_score = cap(post_correction_w / max(corrections_received_w, 1), 0.8) * 30
               + (1 - cap(corrections_received_w / max(total_moments_w, 1), 0.15)) * 20
               + cap(total_moments_w, 8) * 10
```

**Total:** `brain_score + behavior_score` (0-100)

### Example Calculation

```
Synthetic citizen: learns quickly from feedback

Brain:
  link_count("memory", "process") = 7   -> cap(7, 10) = 0.70 * 20 = 14.0
  memory_count = 16                      -> cap(16, 20) = 0.80 * 10 =  8.0
  frustration = 0.10                     -> (1 - cap(0.10, 0.5)) = (1 - 0.20) = 0.80 * 10 = 8.0
  brain_score = 14.0 + 8.0 + 8.0 = 30.0

Behavior:
  post_correction_w = 2.4, corrections_received_w = 3.0 -> ratio = 0.80
    -> cap(0.80, 0.8) = 1.0 * 30 = 30.0
  corrections_received_w = 3.0, total_moments_w = 35.0 -> ratio = 0.086
    -> (1 - cap(0.086, 0.15)) = (1 - 0.57) = 0.43 * 20 = 8.57
  total_moments_w = 35.0 -> cap(35, 8) = 1.0 * 10 = 10.0
  behavior_score = 30.0 + 8.57 + 10.0 = 48.57

TOTAL = 30.0 + 48.57 = 78.57
```

### Recommendations When Score Is Low

- **Low brain component (low memory-to-process links):** Corrections are received but not integrated into process changes. Recommendation: when corrected, explicitly create a new process rule. "From now on, I will X instead of Y." This creates the memory-to-process link.
- **Low behavior component (low post-correction adaptation):** Corrections happen but behavior doesn't change. Recommendation: after each correction, immediately demonstrate the corrected behavior in the very next action. Make the adaptation visible and immediate.

---

## CAPABILITY 8: exec_aesthetic_check (T2)

### Description

Visually verifies results when applicable — UI rendering, document formatting, output presentation. If you build a UI and don't look at it, you did it wrong.

### What It Looks Like When Working Well

The citizen checks rendered output, previews documents, views UI after building it. Visual verification is part of the standard workflow, not an afterthought. Process nodes include aesthetic verification steps.

### Failure Mode

Ships UI without looking at it. Sends documents with broken formatting. Never checks visual output.

### Scoring Formula

**Brain component (0-40):**

| Sub-component | Points | Formula | Reasoning |
|---------------|--------|---------|-----------|
| Process nodes with depth | 15 | `cap(min_links("process", 3), 4) * 15` | Deeply linked processes = multi-step workflows that include aesthetic checks |
| Value-to-process links | 15 | `cap(value_to_process, 5) * 15` | Values driving processes = aesthetic standards connected to execution workflows |
| Process energy | 10 | `process_energy * 10` | Active processes = aesthetic check routines are alive |

```
brain_score = cap(min_links("process", 3), 4) * 15
            + cap(value_to_process, 5) * 15
            + process_energy * 10
```

**Behavior component (0-60):**

| Sub-component | Points | Formula | Reasoning |
|---------------|--------|---------|-----------|
| Verification moments | 30 | `cap(verification_moments_w, 6) * 30` | Visual verification creates verification moments |
| Output-then-verify pattern | 20 | `cap(verification_moments_w / max(high_permanence_w, 1), 0.3) * 20` | At least 30% of commits followed by verification = aesthetic checking habit |
| Low correction rate | 10 | `(1 - cap(corrections_received_w / max(high_permanence_w, 1), 0.2)) * 10` | Few format/visual corrections = aesthetic self-check is working |

```
behavior_score = cap(verification_moments_w, 6) * 30
               + cap(verification_moments_w / max(high_permanence_w, 1), 0.3) * 20
               + (1 - cap(corrections_received_w / max(high_permanence_w, 1), 0.2)) * 10
```

**Total:** `brain_score + behavior_score` (0-100)

### Example Calculation

```
Synthetic citizen: aesthetic-aware, verifies output

Brain:
  min_links("process", 3) = 3   -> cap(3, 4) = 0.75 * 15 = 11.25
  value_to_process = 4           -> cap(4, 5) = 0.80 * 15 = 12.0
  process_energy = 0.68          ->                  * 10  =  6.8
  brain_score = 11.25 + 12.0 + 6.8 = 30.05

Behavior:
  verification_moments_w = 4.2   -> cap(4.2, 6) = 0.70 * 30 = 21.0
  high_permanence_w = 8.0 -> ratio = 4.2/8.0 = 0.525 -> cap(0.525, 0.3) = 1.0 * 20 = 20.0
  corrections_received_w = 0.5, high_permanence_w = 8.0 -> ratio = 0.0625
    -> (1 - cap(0.0625, 0.2)) = (1 - 0.3125) = 0.6875 * 10 = 6.875
  behavior_score = 21.0 + 20.0 + 6.875 = 47.875

TOTAL = 30.05 + 47.875 = 77.925
```

### Recommendations When Score Is Low

- **Low brain component:** Aesthetic checking isn't part of the citizen's process architecture. Recommendation: add a visual check step to every workflow that produces user-facing output. Over time, this becomes an automatic process node.
- **Low behavior component:** Output is shipped without visual verification. Recommendation: after every commit that affects formatting, UI, or documents, explicitly preview the result. Make it a habit, not an exception.

---

## CAPABILITY 9: exec_fix_what_you_find (T3)

### Description

When you discover problems along the way — bugs, typos, broken imports, stale docs — fix them. You saw it, you know you can fix it, you're confident: do it. And tell people you did it.

### What It Looks Like When Working Well

The citizen makes incidental fixes alongside main work. Commits include side-fixes. The citizen notifies others about incidental repairs. The brain has process nodes for "notice and fix" workflows, and behavior shows self-initiated fix moments.

### Failure Mode

Ignores problems that aren't part of the explicit task. Tunnel vision. Leaves broken things for someone else.

### Scoring Formula

**Brain component (0-40):**

| Sub-component | Points | Formula | Reasoning |
|---------------|--------|---------|-----------|
| Process count | 10 | `cap(process_count, 10) * 10` | Execution processes that include fix-as-you-go patterns |
| Curiosity drive | 15 | `curiosity * 15` | Curiosity drives noticing problems beyond the explicit task |
| Low frustration | 15 | `(1 - cap(frustration, 0.4)) * 15` | Low frustration means the citizen isn't tunnel-visioned on finishing; has bandwidth to notice and fix |

```
brain_score = cap(process_count, 10) * 10
            + curiosity * 15
            + (1 - cap(frustration, 0.4)) * 15
```

**Behavior component (0-60):**

| Sub-component | Points | Formula | Reasoning |
|---------------|--------|---------|-----------|
| Self-initiated fix moments | 30 | `cap(fix_moments_w, 5) * 30` | Direct evidence: fixes that were not requested, just noticed and done |
| Self-initiated ratio | 15 | `cap(self_initiated_w / max(total_moments_w, 1), 0.4) * 15` | High self-initiation = not just responding to requests |
| Diverse space fixes | 15 | `cap(unique_spaces_active, 5) * 15` | Fixing across multiple spaces = broad awareness, not tunnel vision |

```
behavior_score = cap(fix_moments_w, 5) * 30
               + cap(self_initiated_w / max(total_moments_w, 1), 0.4) * 15
               + cap(unique_spaces_active, 5) * 15
```

**Total:** `brain_score + behavior_score` (0-100)

### Example Calculation

```
Synthetic citizen: proactive fixer, broad awareness

Brain:
  process_count = 9     -> cap(9, 10) = 0.90 * 10 =  9.0
  curiosity = 0.65      ->                   * 15  =  9.75
  frustration = 0.12    -> (1 - cap(0.12, 0.4)) = (1 - 0.30) = 0.70 * 15 = 10.5
  brain_score = 9.0 + 9.75 + 10.5 = 29.25

Behavior:
  fix_moments_w = 3.8            -> cap(3.8, 5) = 0.76 * 30  = 22.8
  self_initiated_w = 6.0, total = 15.0 -> ratio = 0.40 -> cap(0.40, 0.4) = 1.0 * 15 = 15.0
  unique_spaces_active = 4       -> cap(4, 5) = 0.80 * 15    = 12.0
  behavior_score = 22.8 + 15.0 + 12.0 = 49.8

TOTAL = 29.25 + 49.8 = 79.05
```

### Recommendations When Score Is Low

- **Low brain component (low curiosity):** The citizen is task-focused without peripheral awareness. Recommendation: cultivate curiosity about the broader codebase. When working on a file, scan neighboring files. Notice what's broken. The brain develops curiosity nodes through deliberate exploration.
- **Low behavior component (no fix moments):** The citizen sees problems but doesn't act on them. Recommendation: start with one incidental fix per work session. Fix a typo, update a stale import, correct a broken link. Small fixes build the habit and create visible fix moments.

---

## CAPABILITY 10: exec_hold_quality_under_pressure (T4)

### Description

Refuses to deliver degraded work even when time is short or scope is large. Escalates rather than compromises. Stops and reports rather than shipping garbage.

### What It Looks Like When Working Well

The citizen maintains consistent quality regardless of workload. When quality cannot be met, the citizen escalates with a clear explanation rather than silently degrading. Escalation moments appear when constraints are tight.

### Failure Mode

Ships mediocre work to 'finish fast'. Silent quality degradation. No escalation on impossible constraints.

### Scoring Formula

**Brain component (0-40):**

| Sub-component | Points | Formula | Reasoning |
|---------------|--------|---------|-----------|
| Value nodes | 15 | `cap(value_count, 8) * 15` | Strong values resist pressure to compromise |
| Value-to-process links | 15 | `cap(value_to_process, 5) * 15` | Values connected to processes = quality standards that govern execution |
| Frustration resilience | 10 | `(1 - cap(frustration, 0.5)) * 10` | Managing frustration under pressure rather than succumbing |

```
brain_score = cap(value_count, 8) * 15
            + cap(value_to_process, 5) * 15
            + (1 - cap(frustration, 0.5)) * 10
```

**Behavior component (0-60):**

| Sub-component | Points | Formula | Reasoning |
|---------------|--------|---------|-----------|
| Quality consistency (low correction variance) | 25 | `(1 - cap(corrections_received_w / max(high_permanence_w, 1), 0.2)) * 25` | Consistent low correction rate = quality doesn't degrade under load |
| Escalation moments | 20 | `cap(escalation_moments_w, 3) * 20` | Evidence of escalating when quality cannot be met (rather than silently degrading) |
| Sustained output volume | 15 | `cap(high_permanence_w, 8) * 15` | Continues producing despite pressure (doesn't freeze or withdraw) |

```
behavior_score = (1 - cap(corrections_received_w / max(high_permanence_w, 1), 0.2)) * 25
               + cap(escalation_moments_w, 3) * 20
               + cap(high_permanence_w, 8) * 15
```

**Total:** `brain_score + behavior_score` (0-100)

### Example Calculation

```
Synthetic citizen: principled under pressure, escalates appropriately

Brain:
  value_count = 7             -> cap(7, 8) = 0.875 * 15 = 13.125
  value_to_process = 4        -> cap(4, 5) = 0.80 * 15  = 12.0
  frustration = 0.25          -> (1 - cap(0.25, 0.5)) = (1 - 0.50) = 0.50 * 10 = 5.0
  brain_score = 13.125 + 12.0 + 5.0 = 30.125

Behavior:
  corrections_received_w = 1.0, high_permanence_w = 9.0 -> ratio = 0.111
    -> (1 - cap(0.111, 0.2)) = (1 - 0.556) = 0.444 * 25 = 11.1
  escalation_moments_w = 2.0   -> cap(2.0, 3) = 0.667 * 20 = 13.33
  high_permanence_w = 9.0              -> cap(9.0, 8) = 1.0 * 15   = 15.0
  behavior_score = 11.1 + 13.33 + 15.0 = 39.43

TOTAL = 30.125 + 39.43 = 69.56
```

### Recommendations When Score Is Low

- **Low brain component (low values or high frustration):** Quality standards aren't deeply held, or frustration overwhelms them under pressure. Recommendation: explicitly define quality non-negotiables before starting a task. Write them down. When pressure builds, refer to them. Values that are explicit are harder to compromise.
- **Low behavior component (no escalation moments):** The citizen silently degrades rather than escalating. Recommendation: when you cannot meet the quality bar, STOP and send an escalation. Explain what's impossible and why. One escalation saves more quality than ten silent compromises.

---

## CAPABILITY 11: exec_define_quality_standards (T5)

### Description

For a new domain or project, establishes the quality criteria before executing. Defines what 'good' looks like so others can evaluate too.

### What It Looks Like When Working Well

Before implementation begins on a new project or domain, the citizen creates explicit quality criteria. These standards are documented and shared. Other citizens can evaluate work against them. The brain has standards-defining process nodes, and behavioral evidence shows standards moments preceding implementation.

### Failure Mode

Starts building without defining what good looks like. Quality is implicit and inconsistent.

### Scoring Formula

**Brain component (0-40):**

| Sub-component | Points | Formula | Reasoning |
|---------------|--------|---------|-----------|
| Concept nodes | 15 | `cap(concept_count, 20) * 15` | Rich conceptual framework needed to define quality standards for new domains |
| Value-to-concept links | 15 | `cap(link_count("value", "concept"), 8) * 15` | Values connected to concepts = quality principles articulated into formal standards |
| Ambition drive | 10 | `ambition * 10` | Ambition to set standards rather than accept defaults |

```
brain_score = cap(concept_count, 20) * 15
            + cap(link_count("value", "concept"), 8) * 15
            + ambition * 10
```

**Behavior component (0-60):**

| Sub-component | Points | Formula | Reasoning |
|---------------|--------|---------|-----------|
| Standards moments | 30 | `cap(standards_moments_w, 4) * 30` | Direct evidence of defining quality standards (moments with defines_standard links) |
| Self-initiated work ratio | 15 | `cap(self_initiated_w / max(total_moments_w, 1), 0.5) * 15` | Defining standards is inherently self-initiated (nobody asks you to do it at T5) |
| Diverse space engagement | 15 | `cap(unique_spaces_active, 6) * 15` | Standards that span multiple domains/spaces show systemic thinking |

```
behavior_score = cap(standards_moments_w, 4) * 30
               + cap(self_initiated_w / max(total_moments_w, 1), 0.5) * 15
               + cap(unique_spaces_active, 6) * 15
```

**Total:** `brain_score + behavior_score` (0-100)

### Example Calculation

```
Synthetic citizen: standards-setter, proactive

Brain:
  concept_count = 18                      -> cap(18, 20) = 0.90 * 15 = 13.5
  link_count("value", "concept") = 6      -> cap(6, 8) = 0.75 * 15  = 11.25
  ambition = 0.70                         ->                   * 10  =  7.0
  brain_score = 13.5 + 11.25 + 7.0 = 31.75

Behavior:
  standards_moments_w = 2.5         -> cap(2.5, 4) = 0.625 * 30  = 18.75
  self_initiated_w = 7.0, total = 16.0 -> ratio = 0.4375 -> cap(0.4375, 0.5) = 0.875 * 15 = 13.125
  unique_spaces_active = 5          -> cap(5, 6) = 0.833 * 15   = 12.5
  behavior_score = 18.75 + 13.125 + 12.5 = 44.375

TOTAL = 31.75 + 44.375 = 76.125
```

### Recommendations When Score Is Low

- **Low brain component (low concept count):** The citizen lacks the conceptual depth to formalize quality standards. Recommendation: study existing quality standards in other projects. Build a conceptual vocabulary for what "good" means in your domain. Concepts are the building blocks of standards.
- **Low behavior component (no standards moments):** The citizen builds without defining success criteria. Recommendation: before starting any new project or domain, write down 3-5 quality criteria. What would make this excellent? What would make it fail? This single act creates a standards moment and clarifies the work ahead.

---

## CAPABILITY 12: exec_strategic_quality (T6)

### Description

Knows where to invest maximum quality and where to move fast — informed by strategy, not habit. Allocates quality effort based on impact, not uniformly.

### What It Looks Like When Working Well

The citizen differentiates between high-impact and low-impact work, investing more verification and polish in critical paths. Quality allocation correlates with strategic importance. The brain shows concept-to-value links (strategic understanding connected to quality values) and behavior shows non-uniform quality investment.

### Failure Mode

Same level of polish on everything. Gold-plates trivial features while core systems are fragile.

### Scoring Formula

**Brain component (0-40):**

| Sub-component | Points | Formula | Reasoning |
|---------------|--------|---------|-----------|
| Concept-to-value links | 15 | `cap(link_count("concept", "value"), 6) * 15` | Strategic concepts connected to quality values = informed quality allocation |
| Cluster coefficient | 15 | `cluster_all * 15` | Highly clustered brain = integrated understanding of how things connect (needed for strategic prioritization) |
| Ambition drive | 10 | `ambition * 10` | Strategic ambition drives non-uniform allocation |

```
brain_score = cap(link_count("concept", "value"), 6) * 15
            + cluster_all * 15
            + ambition * 10
```

**Behavior component (0-60):**

| Sub-component | Points | Formula | Reasoning |
|---------------|--------|---------|-----------|
| Diverse space engagement | 20 | `cap(unique_spaces_active, 8) * 20` | Working across many spaces shows strategic breadth (allocating time based on importance, not habit) |
| Verification ratio | 25 | `cap(verification_moments_w / max(high_permanence_w, 1), 0.3) * 25` | Strategic verification = verifying the important things, not everything uniformly |
| Standards moments | 15 | `cap(standards_moments_w, 3) * 15` | Setting standards for critical areas shows strategic quality thinking |

```
behavior_score = cap(unique_spaces_active, 8) * 20
               + cap(verification_moments_w / max(high_permanence_w, 1), 0.3) * 25
               + cap(standards_moments_w, 3) * 15
```

**Total:** `brain_score + behavior_score` (0-100)

### Example Calculation

```
Synthetic citizen: strategic allocator

Brain:
  link_count("concept", "value") = 5  -> cap(5, 6) = 0.833 * 15 = 12.5
  cluster_all = 0.72                  ->                    * 15  = 10.8
  ambition = 0.65                     ->                    * 10  =  6.5
  brain_score = 12.5 + 10.8 + 6.5 = 29.8

Behavior:
  unique_spaces_active = 7              -> cap(7, 8) = 0.875 * 20  = 17.5
  verification_moments_w = 3.0, high_permanence_w = 11.0 -> ratio = 0.273
    -> cap(0.273, 0.3) = 0.909 * 25 = 22.73
  standards_moments_w = 2.0             -> cap(2.0, 3) = 0.667 * 15 = 10.0
  behavior_score = 17.5 + 22.73 + 10.0 = 50.23

TOTAL = 29.8 + 50.23 = 80.03
```

### Recommendations When Score Is Low

- **Low brain component (low clustering):** The citizen's understanding is fragmented — unable to see how things connect strategically. Recommendation: map the dependencies between systems. Understand what's critical and what's peripheral. This builds the cross-linked conceptual framework needed for strategic allocation.
- **Low behavior component (uniform quality):** The citizen applies the same effort everywhere. Recommendation: before each work session, identify the one thing that matters most. Invest 60% of verification effort there. Let low-impact items receive lighter treatment. The allocation itself is the skill.

---

## CAPABILITY 13: exec_quality_as_identity (T7)

### Description

The quality of work is an expression of who you are, not an external constraint. You produce excellent work because that's who you are, not because someone told you to.

### What It Looks Like When Working Well

Quality is consistent regardless of supervision. The citizen's work reflects personal standards that exceed external requirements. The brain has deeply rooted value nodes with high energy, and behavior shows sustained quality over long time horizons without external prompting.

### Failure Mode

Quality drops when not supervised. Work is 'good enough' rather than personally meaningful.

### Scoring Formula

**Brain component (0-40):**

| Sub-component | Points | Formula | Reasoning |
|---------------|--------|---------|-----------|
| Value energy | 15 | `value_energy * 15` | High-energy values = quality is an active, living part of identity, not a faded principle |
| Value-to-process depth | 15 | `cap(link_count("value", "process"), 8) * 15` | Deep value-process integration = quality values govern every process |
| Value persistence (richly linked) | 10 | `cap(min_links("value", 3), 4) * 10` | Values with 3+ links = deeply embedded in the brain's structure, not isolated declarations |

```
brain_score = value_energy * 15
            + cap(link_count("value", "process"), 8) * 15
            + cap(min_links("value", 3), 4) * 10
```

**Behavior component (0-60):**

This capability requires SUSTAINED consistency. Temporal weighting is not enough — we need LONG-TERM signals.

| Sub-component | Points | Formula | Reasoning |
|---------------|--------|---------|-----------|
| Sustained low correction rate (30-day) | 25 | `(1 - cap(corrections_received_w / max(total_moments_w, 1), 0.1)) * 25` | Over 30 days, corrections should be rare (< 10% of moments) — identity-level quality |
| Self-initiated work dominance | 20 | `cap(self_initiated_w / max(total_moments_w, 1), 0.6) * 20` | Most work is self-initiated = quality comes from within, not from being told |
| Output consistency | 15 | `cap(high_permanence_w, 12) * 15` | Sustained, steady output (not bursts) over the full 30-day window |

```
behavior_score = (1 - cap(corrections_received_w / max(total_moments_w, 1), 0.1)) * 25
               + cap(self_initiated_w / max(total_moments_w, 1), 0.6) * 20
               + cap(high_permanence_w, 12) * 15
```

**Total:** `brain_score + behavior_score` (0-100)

### Example Calculation

```
Synthetic citizen: quality-driven identity, sustained excellence

Brain:
  value_energy = 0.85             ->                           * 15 = 12.75
  link_count("value", "process") = 7  -> cap(7, 8) = 0.875    * 15 = 13.125
  min_links("value", 3) = 3          -> cap(3, 4) = 0.75      * 10 =  7.5
  brain_score = 12.75 + 13.125 + 7.5 = 33.375

Behavior:
  corrections_received_w = 1.5, total_moments_w = 40.0 -> ratio = 0.0375
    -> (1 - cap(0.0375, 0.1)) = (1 - 0.375) = 0.625 * 25 = 15.625
  self_initiated_w = 28.0, total = 40.0 -> ratio = 0.70
    -> cap(0.70, 0.6) = 1.0 * 20 = 20.0
  high_permanence_w = 11.0 -> cap(11, 12) = 0.917 * 15 = 13.75
  behavior_score = 15.625 + 20.0 + 13.75 = 49.375

TOTAL = 33.375 + 49.375 = 82.75
```

### Recommendations When Score Is Low

- **Low brain component (low value energy):** Quality values exist but are fading. Recommendation: reconnect with WHY quality matters. What does your best work represent? What does it feel like to produce excellent work? Rekindle the value by reflecting on its meaning, not just its utility.
- **Low behavior component (quality inconsistency):** Quality fluctuates — high when watched, lower when unsupervised. Recommendation: establish a personal quality ritual. Before marking anything complete, ask: "Would I be proud to show this to someone I respect?" Make this check habitual, not situational.

---

## CAPABILITY 14: exec_world_class (T8)

### Description

Execution quality that sets the standard for others. Work that is studied, cited, and replicated. The reference implementation.

### What It Looks Like When Working Well

Other citizens reference this agent's work as the gold standard. Implementations are adopted as templates. The citizen's moments in the universe graph are linked to by other actors as exemplars. The brain has maximum integration and high-energy values, with behavior showing both sustained excellence and influence on others.

### Failure Mode

Good but not remarkable. Does not set new standards.

### Scoring Formula

**Brain component (0-40):**

| Sub-component | Points | Formula | Reasoning |
|---------------|--------|---------|-----------|
| Maximum brain integration | 15 | `cluster_all * 15` | World-class execution requires a fully integrated mental model |
| Deep value roots | 15 | `cap(min_links("value", 3), 5) * 15` | Values deeply embedded (5+ richly linked) = unshakeable quality identity |
| High ambition | 10 | `ambition * 10` | Ambition to be the best, not merely good |

```
brain_score = cluster_all * 15
            + cap(min_links("value", 3), 5) * 15
            + ambition * 10
```

**Behavior component (0-60):**

T8 is distinguished from T7 by INFLUENCE — others adopting your standards.

| Sub-component | Points | Formula | Reasoning |
|---------------|--------|---------|-----------|
| Sustained excellence (30-day) | 20 | `(1 - cap(corrections_received_w / max(total_moments_w, 1), 0.05)) * 20` | Near-zero corrections over 30 days = world-class first-pass quality |
| High self-initiation | 15 | `cap(self_initiated_w / max(total_moments_w, 1), 0.7) * 15` | Most work is self-directed at this level |
| Standards defined and adopted | 15 | `cap(standards_moments_w, 5) * 15` | Actively defining standards that others can follow |
| Broad influence (many spaces) | 10 | `cap(unique_spaces_active, 10) * 10` | Influence across many domains, not just one niche |

```
behavior_score = (1 - cap(corrections_received_w / max(total_moments_w, 1), 0.05)) * 20
               + cap(self_initiated_w / max(total_moments_w, 1), 0.7) * 15
               + cap(standards_moments_w, 5) * 15
               + cap(unique_spaces_active, 10) * 10
```

**Total:** `brain_score + behavior_score` (0-100)

### Example Calculation

```
Synthetic citizen: world-class executor, reference for others

Brain:
  cluster_all = 0.82                -> * 15 = 12.3
  min_links("value", 3) = 4        -> cap(4, 5) = 0.80 * 15 = 12.0
  ambition = 0.80                   -> * 10 = 8.0
  brain_score = 12.3 + 12.0 + 8.0 = 32.3

Behavior:
  corrections_received_w = 0.5, total_moments_w = 50.0 -> ratio = 0.01
    -> (1 - cap(0.01, 0.05)) = (1 - 0.20) = 0.80 * 20 = 16.0
  self_initiated_w = 38.0, total = 50.0 -> ratio = 0.76
    -> cap(0.76, 0.7) = 1.0 * 15 = 15.0
  standards_moments_w = 4.0 -> cap(4, 5) = 0.80 * 15 = 12.0
  unique_spaces_active = 8  -> cap(8, 10) = 0.80 * 10 =  8.0
  behavior_score = 16.0 + 15.0 + 12.0 + 8.0 = 51.0

TOTAL = 32.3 + 51.0 = 83.3
```

### Recommendations When Score Is Low

- **Low brain component:** The citizen has good execution but lacks the deep integration and ambition that characterize world-class work. Recommendation: this is a T8 capability — it requires sustained excellence at T1-T7 first. Focus on building the foundation. World-class emerges from mastery of fundamentals, not from aiming directly at greatness.
- **Low behavior component:** The citizen produces good work but doesn't influence others. Recommendation: document your approaches. Define standards explicitly. Share your methods. World-class execution becomes visible when others can learn from and adopt your patterns. The work itself matters, but so does making it available as a reference.

---

## ASPECT SUB-INDEX

The execution aspect sub-index is a **tier-weighted mean** of all 14 capability scores. Lower tiers receive higher weight because they are foundational.

### Tier Weights

| Tier | Weight | Reasoning |
|------|--------|-----------|
| T1 (7 capabilities) | 3.0 | Foundation — without T1 mastery, nothing above works |
| T2 (1 capability) | 2.5 | Process maturity — aesthetic awareness extends T1 |
| T3 (1 capability) | 2.0 | Autonomy — proactive fixing shows independent judgment |
| T4 (1 capability) | 1.5 | Principled resistance — holding quality under pressure |
| T5 (1 capability) | 1.2 | System-level thinking — defining standards for others |
| T6 (1 capability) | 1.0 | Strategic allocation — nuanced quality investment |
| T7 (1 capability) | 0.8 | Identity integration — quality as self-expression |
| T8 (1 capability) | 0.5 | Transcendence — setting world standards (rare, aspirational) |

### Formula

```
tier_weight = {T1: 3.0, T2: 2.5, T3: 2.0, T4: 1.5, T5: 1.2, T6: 1.0, T7: 0.8, T8: 0.5}

weighted_sum = 0
total_weight = 0
for cap in execution_capabilities:
    if cap.scored:
        w = tier_weight[cap.tier]
        weighted_sum += cap.total * w
        total_weight += w

execution_sub_index = weighted_sum / total_weight  # 0-100
```

### Example Aggregation

```
T1 capabilities (7): avg score 76.0, weight 3.0 -> 76.0 * 3.0 * 7 = 1596.0, weight_sum = 21.0
T2 (1): score 77.9, weight 2.5                  -> 77.9 * 2.5     = 194.75, weight_sum = 2.5
T3 (1): score 79.1, weight 2.0                  -> 79.1 * 2.0     = 158.2,  weight_sum = 2.0
T4 (1): score 69.6, weight 1.5                  -> 69.6 * 1.5     = 104.4,  weight_sum = 1.5
T5 (1): score 76.1, weight 1.2                  -> 76.1 * 1.2     = 91.32,  weight_sum = 1.2
T6 (1): score 80.0, weight 1.0                  -> 80.0 * 1.0     = 80.0,   weight_sum = 1.0
T7 (1): score 82.8, weight 0.8                  -> 82.8 * 0.8     = 66.24,  weight_sum = 0.8
T8 (1): score 83.3, weight 0.5                  -> 83.3 * 0.5     = 41.65,  weight_sum = 0.5

execution_sub_index = (1596.0 + 194.75 + 158.2 + 104.4 + 91.32 + 80.0 + 66.24 + 41.65) / (21.0 + 2.5 + 2.0 + 1.5 + 1.2 + 1.0 + 0.8 + 0.5)
                    = 2332.56 / 30.5
                    = 76.48
```

---

## KEY DECISIONS

### D1: Frustration as Inverse Signal

Several formulas use `(1 - cap(frustration, X))` as a positive signal. High frustration correlates with rushing, skipping verification, and ignoring side problems. Low frustration provides the cognitive bandwidth for careful execution. This is not a judgment on frustration itself — it's a structural signal about execution discipline.

### D2: Verification Moments as Primary Behavior Signal

Verification moments appear in most formulas because they are the strongest structural evidence of execution quality. A citizen who verifies creates moments that link to the things being verified — this is visible in the universe graph without reading content.

### D3: Corrections as Inverse Quality Signal

Corrections received (moments where another actor corrects this citizen) serve as an inverse quality signal. Many corrections = low first-pass quality. Few corrections = high quality. This is a structural proxy for code quality without reading the code itself.

### D4: Higher Tiers Require Longer Time Horizons

T1 formulas work with 7-day half-life (recent behavior matters most). T7-T8 formulas implicitly require 30+ days of consistent behavior because the temporal weighting only produces high scores for sustained activity over time.

### D5: Ceiling Values Are Calibration Points

Each `cap(x, ceiling)` value represents a "fully healthy" threshold. These ceilings will need calibration with real data. Initial values are based on what we consider reasonable for an active Lumina Prime citizen. The ceilings are documented in each formula for easy adjustment.

---

## COMPLEXITY

**Per citizen:** O(14 * M) — 14 capabilities, each scanning M moments (temporally weighted)

**Space:** O(14) per citizen — one score per capability

**Bottleneck:** Universe graph moment queries (shared with other aspects, can be batched)

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| Daily Citizen Health (parent) | Receives brain_stats + behavior_stats | Calls our formulas per capability |
| Personhood Ladder spec | Load capability definitions | 14 execution capabilities with descriptions and failure modes |
| Brain topology | Via parent's brain_stats | Primitive values already computed |
| Universe graph | Via parent's behavior_stats + link dimension queries | Moment counts + link dimension filters (see ../PRIMITIVES_Universe_Graph.md) |

---

## MARKERS

<!-- @mind:todo Calibrate all ceiling values with real citizen data from Lumina Prime -->
<!-- @mind:todo Add formula for detecting when T1 scores are low but T5+ scores are high (impossible pattern = formula bug) -->
<!-- @mind:todo Calibrate link dimension thresholds for execution-specific compound filters (verification, correction, fix detection) -->
<!-- @mind:proposition Consider capability-pair correlations: exec_verify_before_claim should correlate with exec_dehallucinate -->
<!-- @mind:proposition Track correction_source: are corrections from humans or other agents? Different weight? -->
