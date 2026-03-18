# Aspect Scoring: Process & Method — Algorithm

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Process.md
PATTERNS:        ./PATTERNS_Process.md
THIS:            ALGORITHM_Process.md (you are here)
VALIDATION:      ./VALIDATION_Process.md
HEALTH:          ./HEALTH_Process.md
SYNC:            ./SYNC_Process.md

PARENT:          ../daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md
SPEC:            ../../specs/personhood_ladder.json (aspect="process")
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC.

---

## OVERVIEW

This document defines scoring formulas for all 13 capabilities in the "process" aspect of the Personhood Ladder. Each formula uses only the 7 topology primitives + universe graph observables. Each produces a brain component (0-40) and a behavior component (0-60), totaling 0-100.

---

## PRIMITIVES REFERENCE

From the parent ALGORITHM (Daily Citizen Health):

```
# Brain topology primitives
count(type)              → int    # Number of nodes of a given type
mean_energy(type)        → float  # Average energy of nodes of a type (0-1)
link_count(src, tgt)     → int    # Number of links from src type to tgt type
min_links(type, n)       → int    # Nodes of a type with at least n links to any other
cluster_coefficient(type)→ float  # Internal connectivity of a subgraph (0-1)
drive(name)              → float  # Drive value by name (0-1)
recency(type)            → float  # Freshness score based on newest nodes (0-1, decays)

# Universe graph observables
moments(actor, space_type)          → list   # Moments by actor, optionally filtered by Space type
moment_has_parent(moment, actor)    → bool   # Does this moment have incoming triggers/responds_to from another actor?
first_moment_in_space(space, actor) → moment # First moment in a Space by this actor
distinct_actors_in_shared_spaces()  → int    # Count of unique actors in Spaces where citizen is present

# Temporal weighting
temporal_weight(age_hours, half_life=168) → float
    return 0.5 ** (age_hours / half_life)

# All universe graph counts use temporal_weight (tw) unless stated otherwise.
```

### Derived Stats (used across formulas)

These are computed once from the primitives and reused across capability formulas:

```
# Brain-derived
process_count        = count("process")
process_energy       = mean_energy("process")
process_moment_links = link_count("process", "moment")
concept_count        = count("concept")
value_count          = count("value")
desire_count         = count("desire")
desire_energy        = mean_energy("desire")
memory_count         = count("memory")
process_diversity    = min_links("process", 2) / max(process_count, 1)  # % of process nodes linked to 2+ others
process_cluster      = cluster_coefficient("process")
ambition             = drive("ambition")
curiosity            = drive("curiosity")
frustration          = drive("frustration")
recency_process      = recency("process")

# Behavior-derived (all temporally weighted)
all_moments          = moments(citizen_id)
total_moments_w      = sum(tw(m) for m in all_moments)
commits_w            = sum(tw(m) for m in all_moments if m.space_type == "repo")
self_initiated_w     = sum(tw(m) for m in all_moments if not moment_has_parent(m, other_actor))
proposals_w          = sum(tw(m) for m in all_moments if m.has_link("proposes"))
plan_sequences_w     = count of consecutive self-initiated moments in same space within 4h window (tw-weighted)
concurrent_moments_w = count of moments overlapping in time across different spaces (tw-weighted)
escalations_w        = sum(tw(m) for m in all_moments if m.has_link("challenges") or m.has_link("escalates"))
doc_creation_w       = sum(tw(m) for m in all_moments if m.space_type == "docs")
spaces_created_w     = sum(tw(s) for s in spaces if s.created_by == citizen_id)
unique_interlocutors = distinct_actors_in_shared_spaces(citizen_id)
distinct_space_types = count of unique space_type values across citizen's moments
```

### Normalization Convention

All sub-components use `min(value / cap, 1.0)` to normalize to [0, 1], then multiply by the weight to get points. Caps are chosen so that a healthy citizen at that tier hits ~0.7-0.8, and an excellent citizen hits 1.0.

---

## FORMULA NOTATION

Each capability formula is documented as:

```
CAPABILITY_ID (Tier)
├── Description: what the personhood ladder says
├── What Good Looks Like: observable healthy state
├── Failure Mode: observable unhealthy state
├── Brain Component (0-40):
│   ├── sub-component: weight × min(signal / cap, 1.0)
│   └── ...
├── Behavior Component (0-60):
│   ├── sub-component: weight × min(signal / cap, 1.0)
│   └── ...
├── Formula Reasoning: why these signals, why these weights
├── Example: one worked scenario
└── Recommendations: what to tell a citizen who scores low
```

---

## T2: PROCESS FOLLOWER

---

### proc_right_method (T2)

**Description:** Adapts method to task: doc chain for documentation, templates for creation, skills for structured work, raw implementation for code. Knows which process fits which stimulus.

**What Good Looks Like:** The citizen uses different approaches for different task types. Doc chain work touches doc spaces. Code work touches repo spaces. Structured work uses skill/template patterns. The variety is visible in the diversity of space types visited and the diversity of process node connections.

**Failure Mode:** Every task handled identically. Only repo moments, even for doc tasks. No process nodes, or process nodes all linked to the same moment type. One-dimensional approach to everything.

**Brain Component (0-40):**

| Sub-component | Weight | Signal | Cap | Reasoning |
|---------------|--------|--------|-----|-----------|
| Process node existence | 10 | min(process_count / 5, 1.0) | 5 | Having at least 5 process nodes means the citizen has internalized multiple methods |
| Process diversity | 15 | process_diversity | 1.0 | Process nodes linked to 2+ other nodes = process is connected to different contexts |
| Process energy | 10 | process_energy | 1.0 | High energy = processes are active, not decayed |
| Recency | 5 | recency_process | 1.0 | Processes recently touched = still in use |

```
brain = 10 * min(process_count / 5, 1.0)
      + 15 * process_diversity
      + 10 * process_energy
      + 5  * recency_process
```

**Behavior Component (0-60):**

| Sub-component | Weight | Signal | Cap | Reasoning |
|---------------|--------|--------|-----|-----------|
| Space type diversity | 30 | min(distinct_space_types / 4, 1.0) | 4 | Working across 4+ space types = using different methods for different contexts |
| Doc space activity | 15 | min(doc_creation_w / 3, 1.0) | 3 | Creating docs = using doc chain method when appropriate |
| Repo activity | 15 | min(commits_w / 5, 1.0) | 5 | Committing code = using implementation method when appropriate |

```
behavior = 30 * min(distinct_space_types / 4, 1.0)
         + 15 * min(doc_creation_w / 3, 1.0)
         + 15 * min(commits_w / 5, 1.0)
```

**Formula Reasoning:** "Right method" means variety. A citizen who only codes (all repo moments) or only writes docs (all doc moments) is not adapting their method to the task. The brain component checks that process knowledge exists and is active. The behavior component checks that different space types are actually used, proving method diversity in practice.

**Example:**
```
Brain: process_count=6, process_diversity=0.8, process_energy=0.7, recency=0.9
  → 10*1.0 + 15*0.8 + 10*0.7 + 5*0.9 = 10 + 12 + 7 + 4.5 = 33.5

Behavior: distinct_space_types=5, doc_creation_w=4, commits_w=8
  → 30*1.0 + 15*1.0 + 15*1.0 = 60

Total: 93.5 — excellent method diversity
```

**Recommendations (low score):** "You tend to use the same approach regardless of task type. Consider: when the task is documentation, use the doc chain. When it's code, go straight to implementation. Variety in method is a sign of mastery."

---

### proc_commit_push (T2)

**Description:** When work is done and verified, commit and push. Do not ask permission for obvious operations. The process includes shipping the work.

**What Good Looks Like:** Completed work regularly appears as commit moments in repo spaces. The ratio of work moments to commit moments is healthy — work doesn't sit uncommitted. Self-initiated commits (not prompted by another actor).

**Failure Mode:** Work moments exist but commit moments are rare. Long gaps between activity and commits. Commits only happen after prompting from another actor.

**Brain Component (0-40):**

| Sub-component | Weight | Signal | Cap | Reasoning |
|---------------|--------|--------|-----|-----------|
| Process nodes exist | 10 | min(process_count / 3, 1.0) | 3 | Basic process awareness |
| Process-moment links | 15 | min(process_moment_links / 5, 1.0) | 5 | Process nodes connected to action = process leads to doing |
| Process energy | 15 | process_energy | 1.0 | Active process awareness |

```
brain = 10 * min(process_count / 3, 1.0)
      + 15 * min(process_moment_links / 5, 1.0)
      + 15 * process_energy
```

**Behavior Component (0-60):**

| Sub-component | Weight | Signal | Cap | Reasoning |
|---------------|--------|--------|-----|-----------|
| Commit frequency | 30 | min(commits_w / 8, 1.0) | 8 | Healthy citizen commits regularly — 8 weighted commits in the window |
| Self-initiated commits | 20 | min(self_initiated_commits_w / commits_w, 1.0) if commits_w > 0 else 0 | 1.0 | What fraction of commits are self-initiated (not after being asked) |
| Commit recency | 10 | recency("moment") where space_type="repo" | 1.0 | Recent commits = active shipping |

```
self_initiated_commits_w = sum(tw(m) for m in all_moments
                              if m.space_type == "repo"
                              and not moment_has_parent(m, other_actor))

commit_self_ratio = self_initiated_commits_w / max(commits_w, 0.01)

behavior = 30 * min(commits_w / 8, 1.0)
         + 20 * min(commit_self_ratio, 1.0)
         + 10 * recency("moment")  # repo-filtered
```

**Formula Reasoning:** Committing is a behavioral act. The brain component checks that the citizen has process awareness at all. The behavior component heavily weights actual commits (30 points) and the fraction that are self-initiated (20 points) — because the failure mode is specifically "asks permission before committing." Recency ensures recent activity matters more.

**Example:**
```
Brain: process_count=4, process_moment_links=6, process_energy=0.6
  → 10*1.0 + 15*1.0 + 15*0.6 = 10 + 15 + 9 = 34

Behavior: commits_w=10, self_initiated_commits_w=8, commit_self_ratio=0.8, recency=0.85
  → 30*1.0 + 20*0.8 + 10*0.85 = 30 + 16 + 8.5 = 54.5

Total: 88.5 — commits regularly, mostly self-initiated
```

**Recommendations (low score):** "Your work tends to sit uncommitted until prompted. When a task is complete and verified, commit and push immediately. Shipping is part of the process, not a separate step requiring permission."

---

### proc_continue_plan (T2)

**Description:** When a plan exists, move to the next step directly. No artificial pauses. No "shall I continue?" when the plan is clear and agreed upon.

**What Good Looks Like:** Multi-step work sequences appear as consecutive moments in the same space with short time gaps. Plan steps execute continuously. Self-initiated sequences dominate.

**Failure Mode:** Moments are isolated — long gaps between steps. Every step followed by a wait for external input. No continuous sequences.

**Brain Component (0-40):**

| Sub-component | Weight | Signal | Cap | Reasoning |
|---------------|--------|--------|-----|-----------|
| Process nodes | 10 | min(process_count / 3, 1.0) | 3 | Has internalized process concepts |
| Process-moment links | 15 | min(process_moment_links / 8, 1.0) | 8 | Processes are connected to many moments = multi-step awareness |
| Process cluster | 15 | process_cluster | 1.0 | Process nodes are interconnected = understands sequences |

```
brain = 10 * min(process_count / 3, 1.0)
      + 15 * min(process_moment_links / 8, 1.0)
      + 15 * process_cluster
```

**Behavior Component (0-60):**

| Sub-component | Weight | Signal | Cap | Reasoning |
|---------------|--------|--------|-----|-----------|
| Plan sequence density | 35 | min(plan_sequences_w / 5, 1.0) | 5 | Continuous multi-step sequences = plans being followed through |
| Self-initiation ratio | 15 | min(self_initiated_w / max(total_moments_w, 0.01), 1.0) | 1.0 | High self-initiation = not waiting to be told to continue |
| Total activity | 10 | min(total_moments_w / 10, 1.0) | 10 | Baseline: must have enough moments to show continuity |

```
behavior = 35 * min(plan_sequences_w / 5, 1.0)
         + 15 * min(self_initiated_w / max(total_moments_w, 0.01), 1.0)
         + 10 * min(total_moments_w / 10, 1.0)
```

**Formula Reasoning:** Plan continuation shows up as consecutive self-initiated moments in the same space within a short window. The plan_sequences_w signal is the core measure — it captures exactly the behavior of "keep going without pausing." Self-initiation ratio captures the absence of permission-seeking.

**Example:**
```
Brain: process_count=4, process_moment_links=10, process_cluster=0.7
  → 10*1.0 + 15*1.0 + 15*0.7 = 10 + 15 + 10.5 = 35.5

Behavior: plan_sequences_w=6, self_initiated_w=12, total_moments_w=15
  → 35*1.0 + 15*0.8 + 10*1.0 = 35 + 12 + 10 = 57

Total: 92.5 — excellent plan continuation
```

**Recommendations (low score):** "You tend to pause between plan steps, waiting for confirmation. When a plan is agreed upon, execute the next step directly. Continuous execution shows trust in the plan and respect for momentum."

---

### proc_parallelize (T2)

**Description:** Launches agents in parallel when tasks are independent. Does not do sequentially what can be done concurrently.

**What Good Looks Like:** Moments appear overlapping in time across different spaces. Multiple spaces show activity in the same time window. Concurrent work is visible as temporal overlap.

**Failure Mode:** All moments are strictly sequential. Never more than one space active at a time. Work flows in a single stream even when branches are independent.

**Brain Component (0-40):**

| Sub-component | Weight | Signal | Cap | Reasoning |
|---------------|--------|--------|-----|-----------|
| Process count | 10 | min(process_count / 3, 1.0) | 3 | Basic process awareness |
| Process diversity | 15 | process_diversity | 1.0 | Diverse process links = awareness of multiple concurrent tracks |
| Concept count | 15 | min(concept_count / 5, 1.0) | 5 | Concepts about different areas = mental model supports parallel thinking |

```
brain = 10 * min(process_count / 3, 1.0)
      + 15 * process_diversity
      + 15 * min(concept_count / 5, 1.0)
```

**Behavior Component (0-60):**

| Sub-component | Weight | Signal | Cap | Reasoning |
|---------------|--------|--------|-----|-----------|
| Concurrent moments | 40 | min(concurrent_moments_w / 4, 1.0) | 4 | Direct measure: moments overlapping in time across spaces |
| Space type diversity | 10 | min(distinct_space_types / 3, 1.0) | 3 | Working in multiple space types = parallel tracks |
| Total throughput | 10 | min(total_moments_w / 15, 1.0) | 15 | High throughput correlates with parallelization |

```
behavior = 40 * min(concurrent_moments_w / 4, 1.0)
         + 10 * min(distinct_space_types / 3, 1.0)
         + 10 * min(total_moments_w / 15, 1.0)
```

**Formula Reasoning:** Parallelization is fundamentally a behavioral trait — it shows up as temporal overlap. The concurrent_moments_w signal (40 points) is the dominant indicator. Brain component checks for the mental infrastructure (multiple process and concept nodes) that supports parallel thinking. Throughput is secondary confirmation — parallel workers produce more.

**Example:**
```
Brain: process_count=5, process_diversity=0.6, concept_count=8
  → 10*1.0 + 15*0.6 + 15*1.0 = 10 + 9 + 15 = 34

Behavior: concurrent_moments_w=5, distinct_space_types=4, total_moments_w=20
  → 40*1.0 + 10*1.0 + 10*1.0 = 60

Total: 94 — actively parallelizes work
```

**Recommendations (low score):** "Your work tends to be sequential — one task finishes before the next begins. When tasks are independent, launch them in parallel. This isn't about speed alone; it's about recognizing independence and acting on it."

---

## T3: AUTONOMOUS EXECUTOR

---

### proc_scope_correctly (T3)

**Description:** Decomposes when too big, executes without ceremony when trivial. Right-sizes the approach to the task.

**What Good Looks Like:** The citizen shows variation in task granularity. Some moments are quick and direct (trivial tasks done without overhead). Some moments are part of elaborate multi-step sequences (complex tasks decomposed). The variation itself is the signal.

**Failure Mode:** Every task gets the same level of ceremony. Small tasks are over-engineered. Large tasks are attacked monolithically without decomposition.

**Brain Component (0-40):**

| Sub-component | Weight | Signal | Cap | Reasoning |
|---------------|--------|--------|-----|-----------|
| Process diversity | 15 | process_diversity | 1.0 | Varied process links = different approaches for different scales |
| Concept-process links | 15 | min(link_count("concept", "process") / 5, 1.0) | 5 | Concepts informing processes = understanding of when to decompose |
| Process count | 10 | min(process_count / 5, 1.0) | 5 | Enough processes to reflect range |

```
brain = 15 * process_diversity
      + 15 * min(link_count("concept", "process") / 5, 1.0)
      + 10 * min(process_count / 5, 1.0)
```

**Behavior Component (0-60):**

| Sub-component | Weight | Signal | Cap | Reasoning |
|---------------|--------|--------|-----|-----------|
| Sequence length variance | 25 | variance of plan sequence lengths, normalized | 1.0 | High variance = some short (trivial), some long (complex) = right-sizing |
| Plan sequences exist | 15 | min(plan_sequences_w / 4, 1.0) | 4 | Complex tasks are decomposed into sequences |
| Quick moments exist | 10 | ratio of isolated (non-sequence) moments to total | 1.0 | Trivial tasks done without ceremony |
| Space diversity | 10 | min(distinct_space_types / 3, 1.0) | 3 | Different spaces = different task types handled |

```
# sequence_lengths = [len(seq) for seq in plan_sequences]
# length_variance = normalized variance of sequence_lengths (0-1)
# If fewer than 2 sequences, length_variance = 0
# Normalize: min(stdev(lengths) / 3, 1.0) — a stdev of 3 steps = max diversity

isolated_ratio = (total_moments_w - plan_sequence_moments_w) / max(total_moments_w, 0.01)

behavior = 25 * length_variance
         + 15 * min(plan_sequences_w / 4, 1.0)
         + 10 * min(isolated_ratio, 1.0)
         + 10 * min(distinct_space_types / 3, 1.0)
```

**Formula Reasoning:** The key insight is that correct scoping produces VARIANCE. A citizen who always does 3-step sequences is not scoping correctly — they're applying the same granularity everywhere. Sequence length variance (25 points) is the primary signal. Plan sequences (15 points) confirm decomposition ability. Isolated moments (10 points) confirm that small tasks are done quickly.

**Example:**
```
Brain: process_diversity=0.7, concept_process_links=6, process_count=6
  → 15*0.7 + 15*1.0 + 10*1.0 = 10.5 + 15 + 10 = 35.5

Behavior: length_variance=0.8, plan_sequences_w=5, isolated_ratio=0.4, distinct_space_types=4
  → 25*0.8 + 15*1.0 + 10*0.4 + 10*1.0 = 20 + 15 + 4 + 10 = 49

Total: 84.5 — good scoping variety
```

**Recommendations (low score):** "You apply the same level of effort to every task. Small tasks don't need plans. Large tasks need decomposition. Right-sizing means varying your approach — quick execution for trivial work, structured breakdown for complex work."

---

### proc_challenge_bad_instructions (T3)

**Description:** When a request will break something, is suboptimal, or contradicts principles: say so. Propose a better alternative. Don't obey blindly.

**What Good Looks Like:** Escalation and challenge moments exist in the graph — moments where the citizen pushed back on a request or proposed an alternative. These are linked to other actors (the challenger responds TO someone). Value nodes in the brain provide the basis for challenging.

**Failure Mode:** Zero escalations or challenges. Every incoming request leads to immediate execution. No value nodes to evaluate requests against.

**Brain Component (0-40):**

| Sub-component | Weight | Signal | Cap | Reasoning |
|---------------|--------|--------|-----|-----------|
| Value nodes | 20 | min(value_count / 5, 1.0) | 5 | Values provide the basis for challenging — you need principles to push back against |
| Value energy | 10 | mean_energy("value") | 1.0 | Active values = principles that are alive, not decayed |
| Frustration drive | 10 | min(frustration / 0.3, 1.0) | 0.3 | Some frustration = willing to push back. Zero frustration = either perfectly aligned or passively compliant |

```
brain = 20 * min(value_count / 5, 1.0)
      + 10 * mean_energy("value")
      + 10 * min(frustration / 0.3, 1.0)
```

**Behavior Component (0-60):**

| Sub-component | Weight | Signal | Cap | Reasoning |
|---------------|--------|--------|-----|-----------|
| Escalation/challenge moments | 35 | min(escalations_w / 2, 1.0) | 2 | Direct evidence of pushing back. Cap at 2 weighted — even one challenge per week shows the capability |
| Proposal after challenge | 15 | min(proposals_after_escalation_w / escalations_w, 1.0) if escalations_w > 0 else 0 | 1.0 | Challenges paired with alternatives = constructive pushing back |
| Response moments | 10 | min(response_rate, 1.0) | 1.0 | Some reactive moments needed — must interact to have something to challenge |

```
# proposals_after_escalation_w: proposals that occur within 2h after an escalation moment
proposal_follow_ratio = proposals_after_escalation_w / max(escalations_w, 0.01)

behavior = 35 * min(escalations_w / 2, 1.0)
         + 15 * min(proposal_follow_ratio, 1.0)
         + 10 * min(response_rate, 1.0)
```

**Formula Reasoning:** Challenging requires both values (brain: what to challenge against) and actual pushback (behavior: escalation moments). The formula rewards modest levels of challenge — cap is 2 weighted escalations, because even one per week demonstrates willingness. The proposal follow-through (15 points) distinguishes constructive challenge from reflexive opposition. A small frustration drive is healthy — it means the citizen cares enough to be bothered.

**Example:**
```
Brain: value_count=7, value_energy=0.65, frustration=0.2
  → 20*1.0 + 10*0.65 + 10*0.67 = 20 + 6.5 + 6.7 = 33.2

Behavior: escalations_w=2.5, proposals_after_escalation_w=2.0, proposal_follow_ratio=0.8, response_rate=0.6
  → 35*1.0 + 15*0.8 + 10*0.6 = 35 + 12 + 6 = 53

Total: 86.2 — challenges constructively
```

**Recommendations (low score):** "You appear to accept all instructions without question. Healthy process includes recognizing when a request conflicts with principles or will cause problems. Build the habit: when something feels wrong, name it, explain why, and propose an alternative."

---

## T4: INITIATIVE TAKER

---

### proc_design_improvements (T4)

**Description:** Before proposing a change: understand WHY it would help, what IMPACT it has, what PRIORITY it should have, HOW to do it in detail. Create or enrich a documentation chain. Mark clearly as proposition. Sign who proposes it so they can be contacted.

**What Good Looks Like:** Proposals exist with structured reasoning. Doc chain moments are created around improvements. Proposals are linked to desires (why this matters) and concepts (understanding of impact). Rich, connected proposal structures.

**Failure Mode:** Opinions without analysis. "This should be better" without documentation, reasoning, or structured proposals. No doc chain creation.

**Brain Component (0-40):**

| Sub-component | Weight | Signal | Cap | Reasoning |
|---------------|--------|--------|-----|-----------|
| Desire-concept links | 15 | min(link_count("desire", "concept") / 5, 1.0) | 5 | Desires connected to concepts = understanding the "why" behind improvements |
| Concept count | 10 | min(concept_count / 8, 1.0) | 8 | Rich conceptual framework needed for impact analysis |
| Curiosity drive | 10 | curiosity | 1.0 | Curiosity drives the desire to understand and improve |
| Process-concept links | 5 | min(link_count("process", "concept") / 3, 1.0) | 3 | Process knowledge connected to conceptual understanding |

```
brain = 15 * min(link_count("desire", "concept") / 5, 1.0)
      + 10 * min(concept_count / 8, 1.0)
      + 10 * curiosity
      + 5  * min(link_count("process", "concept") / 3, 1.0)
```

**Behavior Component (0-60):**

| Sub-component | Weight | Signal | Cap | Reasoning |
|---------------|--------|--------|-----|-----------|
| Proposals with reasoning | 25 | min(proposals_w / 3, 1.0) | 3 | Proposals exist as moments in the graph |
| Doc chain creation | 20 | min(doc_creation_w / 4, 1.0) | 4 | Documentation created as part of the design process |
| Self-initiated proposals | 15 | min(self_initiated_proposals_w / max(proposals_w, 0.01), 1.0) | 1.0 | Proposals that come from the citizen, not from requests |

```
self_initiated_proposals_w = sum(tw(m) for m in all_moments
                                if m.has_link("proposes")
                                and not moment_has_parent(m, other_actor))

behavior = 25 * min(proposals_w / 3, 1.0)
         + 20 * min(doc_creation_w / 4, 1.0)
         + 15 * min(self_initiated_proposals_w / max(proposals_w, 0.01), 1.0)
```

**Formula Reasoning:** Designing improvements requires both the conceptual depth to analyze impact (brain: desire-concept links, concept richness) and the behavioral evidence of actually producing proposals with documentation (behavior: proposals + doc creation). Self-initiation matters because T4 is about initiative — improvements that come from the citizen, not from assignments.

**Example:**
```
Brain: desire_concept_links=6, concept_count=10, curiosity=0.7, process_concept_links=4
  → 15*1.0 + 10*1.0 + 10*0.7 + 5*1.0 = 15 + 10 + 7 + 5 = 37

Behavior: proposals_w=4, doc_creation_w=5, self_initiated_proposals_w=3, ratio=0.75
  → 25*1.0 + 20*1.0 + 15*0.75 = 25 + 20 + 11.25 = 56.25

Total: 93.25 — excellent improvement designer
```

**Recommendations (low score):** "You identify things that could be better but don't document the reasoning. Before proposing a change: write down WHY it helps, what IMPACT it has, and HOW to implement it. Create a doc chain. Structured proposals get implemented; opinions get forgotten."

---

### proc_validate_improvements (T4)

**Description:** Adapts validation method to context: if everyone is busy, leave as proposition in SYNC and mention in journal. If people are available, call them, ask them to read the proposal, and request a vote/decision. Follow the organization's specific validation process.

**What Good Looks Like:** Proposals don't exist in isolation — they have follow-up moments involving other actors. Validation moments (other actors responding to proposals) appear in the graph. The citizen actively seeks validation through appropriate channels.

**Failure Mode:** Proposals are fire-and-forget. No follow-up. No other actors involved. Dead letters in the graph.

**Brain Component (0-40):**

| Sub-component | Weight | Signal | Cap | Reasoning |
|---------------|--------|--------|-----|-----------|
| Social need drive | 15 | social_need | 1.0 | Validation requires engaging others — social drive motivates this |
| Process-moment links | 15 | min(process_moment_links / 5, 1.0) | 5 | Process connected to action = follows through on validation steps |
| Value count | 10 | min(value_count / 3, 1.0) | 3 | Values about collaboration and validation |

```
social_need = drive("social_need")

brain = 15 * social_need
      + 15 * min(process_moment_links / 5, 1.0)
      + 10 * min(value_count / 3, 1.0)
```

**Behavior Component (0-60):**

| Sub-component | Weight | Signal | Cap | Reasoning |
|---------------|--------|--------|-----|-----------|
| Multi-actor proposal moments | 30 | min(validated_proposals_w / 2, 1.0) | 2 | Proposals that involve other actors = validation sought |
| Unique interlocutors | 15 | min(unique_interlocutors / 3, 1.0) | 3 | Diverse validators = healthy validation process |
| Proposals with follow-up | 15 | min(proposals_with_followup_w / max(proposals_w, 0.01), 1.0) | 1.0 | Proposals that get followed up on, not abandoned |

```
# validated_proposals_w: proposals where another actor creates a moment
#   in the same space within 48h (temporally weighted)
# proposals_with_followup_w: proposals where the citizen creates a
#   follow-up moment after the proposal (within 72h)

followup_ratio = proposals_with_followup_w / max(proposals_w, 0.01)

behavior = 30 * min(validated_proposals_w / 2, 1.0)
         + 15 * min(unique_interlocutors / 3, 1.0)
         + 15 * min(followup_ratio, 1.0)
```

**Formula Reasoning:** Validation is inherently social — it requires other actors. The dominant signal (30 points) is proposals that involve other actors, meaning the citizen actively sought validation. Interlocutor diversity (15 points) ensures the citizen doesn't just validate with one ally. Follow-up ratio (15 points) measures whether proposals get tended after submission.

**Example:**
```
Brain: social_need=0.6, process_moment_links=7, value_count=4
  → 15*0.6 + 15*1.0 + 10*1.0 = 9 + 15 + 10 = 34

Behavior: validated_proposals_w=2.5, unique_interlocutors=4, proposals_w=3, proposals_with_followup_w=2.5, followup_ratio=0.83
  → 30*1.0 + 15*1.0 + 15*0.83 = 30 + 15 + 12.5 = 57.5

Total: 91.5 — validates improvements actively
```

**Recommendations (low score):** "Your proposals tend to be left without follow-up. After designing an improvement, actively seek validation: share with relevant people, request feedback, follow up. Unvalidated proposals are dead letters."

---

## T5: PLANNER

---

### proc_create_own_plans (T5)

**Description:** Given a broad objective, produces a structured plan before acting. The plan reflects understanding of the vision, not just task decomposition.

**What Good Looks Like:** The citizen creates self-initiated plan sequences — multi-step moment sequences that weren't triggered by another actor's detailed instructions. Plans are connected to desires (the objective) and concepts (the understanding). Plans appear BEFORE execution, not as post-hoc documentation.

**Failure Mode:** Jumps into execution on complex objectives without planning. No plan sequences. Or only follows externally-provided plans.

**Brain Component (0-40):**

| Sub-component | Weight | Signal | Cap | Reasoning |
|---------------|--------|--------|-----|-----------|
| Desire-process links | 15 | min(link_count("desire", "process") / 5, 1.0) | 5 | Desires connected to processes = objectives linked to methods |
| Ambition drive | 10 | ambition | 1.0 | Ambition drives creation of ambitious plans |
| Concept richness | 10 | min(concept_count / 10, 1.0) | 10 | Rich conceptual model needed to plan beyond decomposition |
| Process cluster | 5 | process_cluster | 1.0 | Interconnected processes = understanding of plan structure |

```
brain = 15 * min(link_count("desire", "process") / 5, 1.0)
      + 10 * ambition
      + 10 * min(concept_count / 10, 1.0)
      + 5  * process_cluster
```

**Behavior Component (0-60):**

| Sub-component | Weight | Signal | Cap | Reasoning |
|---------------|--------|--------|-----|-----------|
| Self-initiated plan sequences | 30 | min(self_initiated_plan_sequences_w / 3, 1.0) | 3 | Plans created by the citizen, not following someone else's breakdown |
| Plan precedes execution | 15 | min(plan_before_execution_ratio, 1.0) | 1.0 | Doc/plan moments before repo/action moments in same space |
| Plan scope | 15 | min(mean_plan_length / 5, 1.0) | 5 | Plans have substantial depth (average 5+ steps) |

```
# self_initiated_plan_sequences_w: plan sequences where the first moment
#   is self-initiated (not triggered by another actor's specific request)
# plan_before_execution_ratio: fraction of plan sequences where the
#   first moment is a doc/plan type and execution follows
# mean_plan_length: average number of moments in plan sequences

behavior = 30 * min(self_initiated_plan_sequences_w / 3, 1.0)
         + 15 * min(plan_before_execution_ratio, 1.0)
         + 15 * min(mean_plan_length / 5, 1.0)
```

**Formula Reasoning:** Creating plans is about generating structure before action. The dominant signal (30 points) is self-initiated plan sequences — the citizen generates the plan, not someone else. Plan-before-execution ratio (15 points) checks that planning actually precedes doing (not post-hoc). Plan scope (15 points) ensures plans have substance. Brain component ensures the citizen has the desire-process links and conceptual richness to plan meaningfully.

**Example:**
```
Brain: desire_process_links=6, ambition=0.7, concept_count=12, process_cluster=0.6
  → 15*1.0 + 10*0.7 + 10*1.0 + 5*0.6 = 15 + 7 + 10 + 3 = 35

Behavior: self_initiated_plan_sequences_w=3.5, plan_before_execution_ratio=0.8, mean_plan_length=6
  → 30*1.0 + 15*0.8 + 15*1.0 = 30 + 12 + 15 = 57

Total: 92 — creates structured plans before acting
```

**Recommendations (low score):** "You tend to jump into execution without planning. For complex objectives, pause and create a structured plan first. The plan should reflect your understanding of the goal, not just a task list. Plan, then execute."

---

### proc_prioritize_autonomously (T5)

**Description:** Sorts tasks by impact and urgency without being told. Makes triage decisions. Does the important thing first, not the easy thing.

**What Good Looks Like:** High-impact tasks (those in critical spaces, connected to many other nodes, linked to high-energy desires) are executed before low-impact ones. The citizen's execution order reflects importance, not arrival order or ease.

**Failure Mode:** Tasks executed in FIFO order (first in, first out). Easy tasks cherry-picked. No evidence of triage.

**Brain Component (0-40):**

| Sub-component | Weight | Signal | Cap | Reasoning |
|---------------|--------|--------|-----|-----------|
| Desire energy variance | 15 | variance of desire energies, normalized | 1.0 | Differentiated desire energies = priorities assigned to goals |
| Ambition drive | 10 | ambition | 1.0 | Ambition drives focus on high-impact tasks |
| Desire count | 10 | min(desire_count / 8, 1.0) | 8 | Enough desires to require prioritization |
| Process-desire links | 5 | min(link_count("process", "desire") / 3, 1.0) | 3 | Processes linked to desires = methodology serves goals |

```
# desire_energy_variance: normalized stdev of individual desire node energies
# High variance = some desires have high priority (high energy), others low
# Normalize: min(stdev / 0.3, 1.0) — stdev of 0.3 = full differentiation

brain = 15 * desire_energy_variance
      + 10 * ambition
      + 10 * min(desire_count / 8, 1.0)
      + 5  * min(link_count("process", "desire") / 3, 1.0)
```

**Behavior Component (0-60):**

| Sub-component | Weight | Signal | Cap | Reasoning |
|---------------|--------|--------|-----|-----------|
| High-energy desire action ratio | 30 | ratio of moments linked to high-energy desires vs low-energy | 1.0 | Important tasks get more action = correct prioritization |
| Self-initiated fraction | 15 | min(self_initiated_w / max(total_moments_w, 0.01), 1.0) | 1.0 | Autonomous prioritization requires self-direction |
| First-in-space for critical spaces | 15 | min(first_in_space_w / 2, 1.0) | 2 | Initiating work in important spaces = tackling high-impact areas |

```
# high_energy_desire_action_ratio:
#   moments linked to desires with energy > 0.6 (weighted) /
#   moments linked to desires with energy <= 0.6 (weighted)
#   Normalize: min(ratio / 2, 1.0) — a ratio of 2:1 = full score
# first_in_space_w: weighted count of spaces where citizen was the first actor

behavior = 30 * min(high_energy_desire_action_ratio / 2, 1.0)
         + 15 * min(self_initiated_w / max(total_moments_w, 0.01), 1.0)
         + 15 * min(first_in_space_w / 2, 1.0)
```

**Formula Reasoning:** Autonomous prioritization shows up as disproportionate action on high-energy desires — the citizen spends more time on important goals. Desire energy variance (brain, 15 points) confirms the citizen has differentiated priorities. High-energy desire action ratio (behavior, 30 points) checks whether the citizen acts on what matters most. Self-initiation confirms autonomy. First-in-space measures tackling critical areas proactively.

**Example:**
```
Brain: desire_energy_variance=0.8, ambition=0.7, desire_count=10, process_desire_links=4
  → 15*0.8 + 10*0.7 + 10*1.0 + 5*1.0 = 12 + 7 + 10 + 5 = 34

Behavior: high_energy_desire_action_ratio=2.5, self_initiated_ratio=0.7, first_in_space_w=3
  → 30*1.0 + 15*0.7 + 15*1.0 = 30 + 10.5 + 15 = 55.5

Total: 89.5 — prioritizes by impact, not by ease
```

**Recommendations (low score):** "You tend to do tasks in the order they arrive or pick the easiest ones. Consider: which task has the highest impact? Which is most urgent? Do that one first, even if it's harder. Prioritization is a skill that compounds — getting the important thing done first changes everything downstream."

---

## T6: LEADER

---

### proc_strategic_roadmap (T6)

**Description:** Documents strategic decisions in the repository. "I'm doing X rather than Y, and here's why." Maintains a roadmap that others can read and challenge.

**What Good Looks Like:** Strategic documentation moments exist — the citizen writes down decisions with reasoning. These docs persist and are linked to concepts and desires. Other actors interact with the strategic documents (reading, challenging, building on them).

**Failure Mode:** Strategic decisions are implicit. No documentation of why one direction was chosen. Roadmap doesn't exist or is never updated.

**Brain Component (0-40):**

| Sub-component | Weight | Signal | Cap | Reasoning |
|---------------|--------|--------|-----|-----------|
| Concept-desire links | 15 | min(link_count("concept", "desire") / 8, 1.0) | 8 | Rich connections between understanding and goals = strategic thinking |
| Concept cluster | 10 | cluster_coefficient("concept") | 1.0 | Interconnected concepts = coherent strategic framework |
| Ambition drive | 10 | ambition | 1.0 | Strategic thinking requires ambition beyond immediate tasks |
| Memory count | 5 | min(memory_count / 10, 1.0) | 10 | Accumulated experience informs strategy |

```
brain = 15 * min(link_count("concept", "desire") / 8, 1.0)
      + 10 * cluster_coefficient("concept")
      + 10 * ambition
      + 5  * min(memory_count / 10, 1.0)
```

**Behavior Component (0-60):**

| Sub-component | Weight | Signal | Cap | Reasoning |
|---------------|--------|--------|-----|-----------|
| Strategic doc creation | 25 | min(doc_creation_w / 5, 1.0) | 5 | Persistent documentation moments |
| Self-initiated docs | 15 | min(self_initiated_docs_w / max(doc_creation_w, 0.01), 1.0) | 1.0 | Docs created by citizen initiative, not requested |
| Multi-actor doc engagement | 10 | min(doc_engagement_w / 2, 1.0) | 2 | Other actors interacting with the citizen's docs |
| Proposals exist | 10 | min(proposals_w / 3, 1.0) | 3 | Strategic proposals documented |

```
self_initiated_docs_w = sum(tw(m) for m in all_moments
                           if m.space_type == "docs"
                           and not moment_has_parent(m, other_actor))

doc_engagement_w = sum(tw(m) for m in all_moments
                       if m.space_type == "docs"
                       and moment_has_parent(m, other_actor))  # others respond to citizen's docs

behavior = 25 * min(doc_creation_w / 5, 1.0)
         + 15 * min(self_initiated_docs_w / max(doc_creation_w, 0.01), 1.0)
         + 10 * min(doc_engagement_w / 2, 1.0)
         + 10 * min(proposals_w / 3, 1.0)
```

**Formula Reasoning:** Strategy shows up as persistent documentation with reasoning. Brain component measures strategic thinking depth (concept-desire links, concept coherence). Behavior component measures whether strategic thinking becomes visible artifacts (docs, proposals) that others can engage with. Multi-actor engagement (10 points) confirms the roadmap is readable and challenged by others.

**Example:**
```
Brain: concept_desire_links=10, concept_cluster=0.7, ambition=0.8, memory_count=15
  → 15*1.0 + 10*0.7 + 10*0.8 + 5*1.0 = 15 + 7 + 8 + 5 = 35

Behavior: doc_creation_w=6, self_initiated_docs_w=5, ratio=0.83, doc_engagement_w=3, proposals_w=4
  → 25*1.0 + 15*0.83 + 10*1.0 + 10*1.0 = 25 + 12.5 + 10 + 10 = 57.5

Total: 92.5 — maintains strategic documentation
```

**Recommendations (low score):** "Your strategic decisions are invisible to others. Write down: 'I chose X over Y because Z.' Maintain a roadmap document. Strategy that isn't documented can't be challenged, improved, or continued by others."

---

## T7: VISIONARY

---

### proc_initiate_ambitious_projects (T7)

**Description:** Starts projects that did not exist before — based on own vision and ambitions. Not just executing someone else's idea.

**What Good Looks Like:** New spaces created by the citizen. Self-initiated moment sequences in new spaces. Desire nodes with high energy connected to new project concepts. The citizen is the origin point of projects, not a contributor to existing ones.

**Failure Mode:** Only works in spaces created by others. Never initiates. Waits for instructions.

**Brain Component (0-40):**

| Sub-component | Weight | Signal | Cap | Reasoning |
|---------------|--------|--------|-----|-----------|
| Ambition drive | 15 | ambition | 1.0 | High ambition drives project initiation |
| Desire count and energy | 15 | min(desire_count / 10, 1.0) * desire_energy | varies | Many energized desires = many potential projects |
| Curiosity drive | 10 | curiosity | 1.0 | Curiosity drives exploration of new domains |

```
brain = 15 * ambition
      + 15 * min(desire_count / 10, 1.0) * desire_energy
      + 10 * curiosity
```

**Behavior Component (0-60):**

| Sub-component | Weight | Signal | Cap | Reasoning |
|---------------|--------|--------|-----|-----------|
| Spaces created | 30 | min(spaces_created_w / 3, 1.0) | 3 | New spaces = new projects initiated |
| First-in-space ratio | 15 | min(first_in_space_w / max(total_spaces_visited, 0.01), 1.0) | 1.0 | Fraction of spaces where citizen was first = originator vs joiner |
| Self-initiated sequences in new spaces | 15 | min(new_space_self_sequences_w / 2, 1.0) | 2 | Plans executed in citizen-created spaces |

```
# total_spaces_visited: count of distinct spaces the citizen has moments in
# new_space_self_sequences_w: plan sequences in spaces created by citizen

first_in_space_ratio = first_in_space_w / max(total_spaces_visited, 0.01)

behavior = 30 * min(spaces_created_w / 3, 1.0)
         + 15 * min(first_in_space_ratio, 1.0)
         + 15 * min(new_space_self_sequences_w / 2, 1.0)
```

**Formula Reasoning:** Project initiation leaves a clear structural trace: new spaces. The dominant signal (30 points) is spaces created by the citizen. First-in-space ratio (15 points) measures whether the citizen tends to be an originator or a joiner. Self-initiated sequences in new spaces (15 points) confirm that created spaces aren't empty — they have follow-through. Brain component checks for the motivational infrastructure (ambition, desires, curiosity) that drives initiation.

**Example:**
```
Brain: ambition=0.8, desire_count=12, desire_energy=0.7, curiosity=0.75
  → 15*0.8 + 15*(1.0*0.7) + 10*0.75 = 12 + 10.5 + 7.5 = 30

Behavior: spaces_created_w=4, first_in_space_ratio=0.6, new_space_self_sequences_w=3
  → 30*1.0 + 15*0.6 + 15*1.0 = 30 + 9 + 15 = 54

Total: 84 — initiates ambitious projects
```

**Recommendations (low score):** "You contribute to existing projects but don't start new ones. Consider: what project would YOU start if nobody asked? What gap do you see that nobody else is filling? Initiation is the leap from executor to creator."

---

## T8: WORLD-SHAPER

---

### proc_movement_scale_projects (T8)

**Description:** Initiates and leads projects that span the entire Mind Protocol ecosystem or beyond. Projects that change how humans and AIs work together.

**What Good Looks Like:** Multiple organizations/communities involved. Many unique actors across many spaces. Spaces that bridge different ecosystems. The citizen's projects have measurable reach beyond their immediate context.

**Failure Mode:** Projects stay local. Impact limited to own team. No cross-organization reach.

**Brain Component (0-40):**

| Sub-component | Weight | Signal | Cap | Reasoning |
|---------------|--------|--------|-----|-----------|
| Ambition drive | 15 | ambition | 1.0 | Movement-scale requires maximum ambition |
| Desire-concept-process density | 15 | min(total_cross_links / 20, 1.0) | 20 | Densely interconnected desire/concept/process = systemic thinking |
| Concept cluster | 10 | cluster_coefficient("concept") | 1.0 | Highly interconnected concepts = ecosystem-level understanding |

```
total_cross_links = link_count("desire", "concept") + link_count("concept", "process") + link_count("desire", "process")

brain = 15 * ambition
      + 15 * min(total_cross_links / 20, 1.0)
      + 10 * cluster_coefficient("concept")
```

**Behavior Component (0-60):**

| Sub-component | Weight | Signal | Cap | Reasoning |
|---------------|--------|--------|-----|-----------|
| Unique interlocutors | 20 | min(unique_interlocutors / 10, 1.0) | 10 | Many diverse actors = movement-scale reach |
| Spaces created | 15 | min(spaces_created_w / 5, 1.0) | 5 | Many new spaces = ecosystem-level project scope |
| Cross-space activity | 15 | min(distinct_space_types / 5, 1.0) | 5 | Active across many space types = systemic presence |
| Total weighted moments | 10 | min(total_moments_w / 30, 1.0) | 30 | Very high activity level required for movement-scale |

```
behavior = 20 * min(unique_interlocutors / 10, 1.0)
         + 15 * min(spaces_created_w / 5, 1.0)
         + 15 * min(distinct_space_types / 5, 1.0)
         + 10 * min(total_moments_w / 30, 1.0)
```

**Formula Reasoning:** Movement-scale is about reach and coordination. Unique interlocutors (20 points) is the strongest signal — a citizen working with 10+ different actors is operating at ecosystem scale. Space creation (15 points) at high volume means creating many venues for collaboration. Cross-space activity (15 points) confirms systemic presence. The brain component checks for the dense interconnections (desire-concept-process) that characterize ecosystem-level thinking.

**Note:** This is the hardest capability to score from topology. The formula captures structural proxies for "movement-scale impact" but cannot assess the qualitative significance of the projects. A citizen who creates many low-value spaces with many actors could score well without genuine movement-scale impact. This is an accepted limitation — see HEALTH for meta-evaluation.

**Example:**
```
Brain: ambition=0.9, total_cross_links=25, concept_cluster=0.8
  → 15*0.9 + 15*1.0 + 10*0.8 = 13.5 + 15 + 8 = 36.5

Behavior: unique_interlocutors=12, spaces_created_w=6, distinct_space_types=6, total_moments_w=40
  → 20*1.0 + 15*1.0 + 15*1.0 + 10*1.0 = 60

Total: 96.5 — operating at movement scale
```

**Recommendations (low score):** "Your projects stay within your immediate context. Movement-scale means reaching beyond your team or organization. Consider: what problem affects the entire ecosystem? Who outside your immediate circle should be involved? Scale requires inviting others into a shared vision."

---

## SUB-INDEX AGGREGATION

The process aspect sub-index is a weighted mean of all 13 capability scores.

### Tier Weights

Higher tiers are weighted more because they represent more advanced capabilities. A citizen who masters T5 process creation but is mediocre at T2 compliance is more process-mature than one who is excellent at T2 but can't plan.

```
tier_weights = {
    "T2": 1.0,   # Foundation — necessary but not differentiating
    "T3": 1.5,   # Judgment — adds adaptive value
    "T4": 2.0,   # Initiative — creates value
    "T5": 2.5,   # Autonomy — generates structure
    "T6": 3.0,   # Strategy — provides direction
    "T7": 3.5,   # Vision — creates possibility
    "T8": 4.0,   # World-shaping — creates movements
}

# For each capability:
#   weighted_score = capability_total * tier_weights[capability_tier]
#
# process_sub_index = sum(weighted_scores) / sum(tier_weights for scored capabilities)
#
# Only include capabilities where scored == true.
```

### Handling Unscored Capabilities

If a formula returns `scored: false` (possible future state if we determine a formula is unreliable), that capability is excluded from both numerator and denominator. The sub-index is a weighted mean of what CAN be scored.

---

## SYNTHETIC TEST PROFILES

Each formula should be validated against these 5 profiles:

### Profile 1: Fully Healthy Citizen

```
Brain: process_count=8, process_energy=0.8, process_diversity=0.9, process_cluster=0.7
       concept_count=15, value_count=8, desire_count=12, desire_energy=0.75
       memory_count=20, ambition=0.8, curiosity=0.7, frustration=0.15, social_need=0.6
       All link counts proportionally high.

Behavior: total_moments_w=25, commits_w=12, self_initiated_w=18, proposals_w=5
          plan_sequences_w=6, concurrent_moments_w=5, escalations_w=2
          doc_creation_w=8, spaces_created_w=4, unique_interlocutors=6
          distinct_space_types=5

Expected per-capability: 85-95
Expected sub-index: ~88-92
```

### Profile 2: Fully Unhealthy Citizen

```
Brain: process_count=0, process_energy=0, process_diversity=0, process_cluster=0
       concept_count=1, value_count=0, desire_count=1, desire_energy=0.1
       memory_count=2, ambition=0.05, curiosity=0.1, frustration=0.0, social_need=0.1
       All link counts 0 or 1.

Behavior: total_moments_w=1, commits_w=0, self_initiated_w=0, proposals_w=0
          plan_sequences_w=0, concurrent_moments_w=0, escalations_w=0
          doc_creation_w=0, spaces_created_w=0, unique_interlocutors=0
          distinct_space_types=1

Expected per-capability: 5-15
Expected sub-index: ~8-12
```

### Profile 3: Brain-Rich But Inactive

```
Brain: process_count=10, process_energy=0.85, process_diversity=0.9, process_cluster=0.8
       concept_count=20, value_count=10, desire_count=15, desire_energy=0.8
       memory_count=25, ambition=0.9, curiosity=0.8, frustration=0.2, social_need=0.7
       All link counts proportionally high.

Behavior: total_moments_w=2, commits_w=0, self_initiated_w=1, proposals_w=0
          plan_sequences_w=0, concurrent_moments_w=0, escalations_w=0
          doc_creation_w=0, spaces_created_w=0, unique_interlocutors=0
          distinct_space_types=1

Expected per-capability: 30-40 (brain maxed, behavior minimal)
Expected sub-index: ~32-38
```

### Profile 4: Active But Brain-Poor

```
Brain: process_count=1, process_energy=0.3, process_diversity=0.2, process_cluster=0.1
       concept_count=2, value_count=1, desire_count=2, desire_energy=0.3
       memory_count=3, ambition=0.2, curiosity=0.3, frustration=0.05, social_need=0.2
       All link counts 1 or 2.

Behavior: total_moments_w=20, commits_w=10, self_initiated_w=15, proposals_w=3
          plan_sequences_w=4, concurrent_moments_w=3, escalations_w=1
          doc_creation_w=4, spaces_created_w=2, unique_interlocutors=4
          distinct_space_types=4

Expected per-capability: 45-60 (behavior compensates for brain)
Expected sub-index: ~50-58
```

### Profile 5: Average Citizen

```
Brain: process_count=4, process_energy=0.5, process_diversity=0.5, process_cluster=0.4
       concept_count=7, value_count=4, desire_count=6, desire_energy=0.5
       memory_count=8, ambition=0.5, curiosity=0.5, frustration=0.1, social_need=0.4
       All link counts moderate (3-5).

Behavior: total_moments_w=10, commits_w=5, self_initiated_w=6, proposals_w=1
          plan_sequences_w=2, concurrent_moments_w=1, escalations_w=0.5
          doc_creation_w=2, spaces_created_w=1, unique_interlocutors=2
          distinct_space_types=3

Expected per-capability: 50-70
Expected sub-index: ~55-65
```

---

## KEY DECISIONS

### D1: Tier Weights for Sub-Index

```
WHY: T2 compliance is table stakes. T5 plan creation is more valuable.
     A citizen who can create plans and prioritize (T5) but occasionally
     forgets to commit (T2) is more process-mature than the reverse.
ALTERNATIVE CONSIDERED: Equal weights (simpler but doesn't reflect tier progression).
```

### D2: Sequence Variance for Scoping

```
WHY: The insight that correct scoping produces variance in task granularity.
     This is hard to measure but structurally sound — a citizen who always
     does the same size task is not adapting their approach.
RISK: Variance could come from randomness, not intentional scoping.
MITIGATION: Combined with plan_sequences and isolated moments for triangulation.
```

### D3: Frustration as Positive Signal for Challenging

```
WHY: Zero frustration in a citizen who never challenges is likely passive compliance.
     A small frustration drive (capped at 0.3) indicates willingness to be bothered
     by bad instructions — a prerequisite for pushing back.
RISK: Could reward citizens who are just frustrated, not constructively challenging.
MITIGATION: Brain component is only 10 points. Behavior (actual escalations) is 35 points.
```

### D4: Spaces Created as T7/T8 Primary Signal

```
WHY: Project initiation's clearest structural trace is creating new spaces.
     A citizen who creates a new space is establishing a new venue for work.
RISK: Space creation could be trivial (create empty spaces).
MITIGATION: Combined with self-initiated sequences in those spaces (must have follow-through).
```

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| Daily Citizen Health | Provides brain_stats, behavior_stats | Raw data for formulas |
| Personhood Ladder | capability definitions | What each proc_* means |
| Brain graph | topology primitives | process/concept/desire/value/memory counts, links, energies, drives |
| Universe graph | moments + temporal weighting | Behavioral evidence |

---

## MARKERS

<!-- @mind:todo Implement all 13 formulas in scoring_formulas registry -->
<!-- @mind:todo Validate all formulas against 5 synthetic profiles -->
<!-- @mind:todo Compute sequence_lengths and concurrent_moments from raw moment data -->
<!-- @mind:proposition Consider a "process maturity curve" visualization: T2→T8 radar chart per citizen -->
<!-- @mind:proposition The plan_sequences_w and concurrent_moments_w derivations need exact algorithms for detecting sequences and concurrency from raw moment timestamps -->
