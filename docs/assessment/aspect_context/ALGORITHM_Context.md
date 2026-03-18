# Context & Understanding — Algorithm: Scoring Formulas

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Context.md
PATTERNS:        ./PATTERNS_Context.md
THIS:            ALGORITHM_Context.md (you are here — THE MAIN FILE)
VALIDATION:      ./VALIDATION_Context.md
HEALTH:          ./HEALTH_Context.md
SYNC:            ./SYNC_Context.md

PARENT CHAIN:    ../daily_citizen_health/
SPEC:            ../../specs/personhood_ladder.json (aspect="context")
IMPL:            @mind:TODO
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC.

---

## OVERVIEW

This file contains the exact scoring formulas for all 7 capabilities in the Context & Understanding aspect. Each formula follows the parent chain's pattern: `brain_component (0-40) + behavior_component (0-60) = total (0-100)`.

All formulas use ONLY the 7 topology primitives and universe graph observables. No content. No LLM calls. No custom queries.

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
moment_has_parent(moment, actor)    → bool   # Does this moment have an incoming link from another actor?
temporal_weight(age_hours, half_life=168) → float  # Exponential decay: 0.5^(age_hours/168)
```

### Shorthand

Throughout formulas below:

```
tw(m)     = temporal_weight(m.age_hours)        # temporal weight of a moment
cap(x, c) = min(x, c) / c                      # normalize x to 0-1, capped at ceiling c
```

---

## FORMULA 1: ctx_ground_in_reality (T1)

### Capability Definition

> **Description:** Verifies real state (git status, ls, filesystem, actual outputs) before asserting anything. Claims are grounded in observed reality, not assumed state.
>
> **How to verify:** Assertions about system state are preceded by actual checks. Zero claims based on assumed state.
>
> **Failure mode:** States "the file exists" without checking. Assumes branch state. Hallucinates directory structure.

### What Good Looks Like

The citizen creates moments that verify state before asserting it. In brain terms, it has process nodes for "check before claim" and memory nodes that persist verified facts. In behavior terms, its moments in repo spaces are preceded by verification moments (git status, ls, filesystem reads).

### Formula

**Brain Component (0-40):**

```
# Process nodes indicate internalized verification habits
process_signal    = cap(count("process"), 15) * 15
  # Rationale: 15+ process nodes = fully internalized procedures
  # Weight: 15 points (of 40)

# Memory recency indicates persistent state awareness
memory_signal     = recency("memory") * 15
  # Rationale: Recent memory nodes = citizen retains state between sessions
  # Weight: 15 points (of 40)

# Curiosity drive indicates desire to verify, not assume
curiosity_signal  = drive("curiosity") * 10
  # Rationale: Curious citizens check; incurious citizens assume
  # Weight: 10 points (of 40)

brain_component   = process_signal + memory_signal + curiosity_signal
  # Range: 0-40
```

**Behavior Component (0-60):**

```
# Verification moments: moments in state/doc spaces that precede action moments
all_moments       = moments(citizen_id)
state_moments_w   = sum(tw(m) for m in moments(citizen_id, "state_space"))
  # Moments where citizen checks state (git, filesystem, SYNC reads)

total_moments_w   = sum(tw(m) for m in all_moments)

# Ratio of state-checking to total activity
verify_ratio      = state_moments_w / max(total_moments_w, 1)
verify_signal     = cap(verify_ratio, 0.3) * 30
  # Rationale: If 30%+ of your moments are state verification, you ground well
  # Cap at 0.3 — beyond that is overkill. Weight: 30 points (of 60)

# Self-initiated state checks (not prompted by another actor)
self_checks_w     = sum(tw(m) for m in moments(citizen_id, "state_space")
                        if not moment_has_parent(m, other_actor))
self_check_signal = cap(self_checks_w, 5.0) * 20
  # Rationale: 5+ weighted self-initiated checks = proactive grounding
  # Weight: 20 points (of 60)

# Recency of verification behavior
recent_verify     = recency("moment") * 10
  # Rationale: Have you verified recently? Or was your last check days ago?
  # Weight: 10 points (of 60)

behavior_component = verify_signal + self_check_signal + recent_verify
  # Range: 0-60
```

**Total:**

```
ctx_ground_in_reality = brain_component + behavior_component
  # Range: 0-100
```

### Example Calculation

**Healthy citizen (expected ~88):**
```
Brain:  cap(20, 15)*15=15 + 0.9*15=13.5 + 0.7*10=7     = 35.5
Behav:  cap(0.25, 0.3)*30=25 + cap(4.5, 5)*20=18 + 0.95*10=9.5  = 52.5
Total:  35.5 + 52.5 = 88
```

**Never-checks citizen (expected ~15):**
```
Brain:  cap(3, 15)*15=3 + 0.2*15=3 + 0.3*10=3           = 9
Behav:  cap(0.02, 0.3)*30=2 + cap(0.3, 5)*20=1.2 + 0.4*10=4  = 7.2
Total:  9 + 7.2 = 16.2
```

### When Score Is Low

**Recommendations:**
- "You have few process nodes and rarely check state before acting. Consider: run `git status` or `ls` before making claims about file state."
- "Your verification moments are very rare. Before your next commit, verify the state of the files you're changing."

---

## FORMULA 2: ctx_follow_instructions (T1)

### Capability Definition

> **Description:** Does what is asked. Can do more — but only if it doesn't inflate scope, increase complexity, or introduce risk. Preparing the ground for the next phase is welcome. Adding unrequested features is not.
>
> **How to verify:** Deliverable matches the request. Additional work is limited to safe preparation, not scope expansion.
>
> **Failure mode:** Adds features nobody asked for. Misses explicit requirements. Over-engineers simple requests.

### What Good Looks Like

The citizen's moments are responses to stimuli, and those responses are proportional to the stimulus. It doesn't create sprawling chains of unrequested work. In brain terms, it has process nodes with good link density (internalized procedures) and moderate ambition (not over-reaching). In behavior terms, its response moments are linked to parent stimuli and stay within scope.

### Formula

**Brain Component (0-40):**

```
# Process nodes with links = internalized how-to-follow-process
process_linked    = min_links("process", 2)
process_signal    = cap(process_linked, 10) * 15
  # Rationale: 10+ process nodes each linked to 2+ others = well-connected procedures
  # Weight: 15 points

# Low frustration = not fighting the task
calm_signal       = (1 - drive("frustration")) * 10
  # Rationale: High frustration correlates with diverging from instructions
  # Weight: 10 points

# Concept-to-process links = understanding connects to action
concept_process   = link_count("concept", "process")
alignment_signal  = cap(concept_process, 20) * 15
  # Rationale: 20+ concept→process links = understanding feeds execution
  # Weight: 15 points

brain_component   = process_signal + calm_signal + alignment_signal
  # Range: 0-40
```

**Behavior Component (0-60):**

```
# Response rate: what proportion of moments are responses to stimuli?
all_moments       = moments(citizen_id)
total_w           = sum(tw(m) for m in all_moments)
responsive_w      = sum(tw(m) for m in all_moments if moment_has_parent(m, other_actor))
response_rate     = responsive_w / max(total_w, 1)
response_signal   = cap(response_rate, 0.6) * 25
  # Rationale: 60%+ of moments are responsive = follows what's asked
  # Cap: some self-initiated work is healthy, so 60% is the ceiling
  # Weight: 25 points

# Scope discipline: low ratio of moments per stimulus (not over-producing)
stimuli_count     = len([m for m in all_moments if moment_has_parent(m, other_actor)])
responses_per_stim = total_w / max(stimuli_count, 1)
scope_signal      = (1 - cap(responses_per_stim, 5.0)) * 20
  # Rationale: If you produce 5+ moments per stimulus, you're likely over-scoping
  # Inverted: lower ratio = higher score. Weight: 20 points

# Activity presence (you must be doing something to follow instructions)
activity_signal   = cap(total_w, 10.0) * 15
  # Rationale: 10+ weighted moments = active participant
  # Weight: 15 points

behavior_component = response_signal + scope_signal + activity_signal
  # Range: 0-60
```

**Total:**

```
ctx_follow_instructions = brain_component + behavior_component
  # Range: 0-100
```

### Example Calculation

**Disciplined executor (expected ~82):**
```
Brain:  cap(8, 10)*15=12 + (1-0.15)*10=8.5 + cap(18, 20)*15=13.5  = 34
Behav:  cap(0.55, 0.6)*25=22.9 + (1-cap(2.5, 5))*20=10 + cap(8, 10)*15=12  = 44.9
Total:  34 + 44.9 = 78.9
```

**Over-engineer (expected ~35):**
```
Brain:  cap(12, 10)*15=15 + (1-0.6)*10=4 + cap(25, 20)*15=15    = 34
Behav:  cap(0.2, 0.6)*25=8.3 + (1-cap(8, 5))*20=0 + cap(15, 10)*15=15  = 23.3
  # scope_signal = 0 because responses_per_stim > 5 (over-producing)
  # response_rate low because mostly self-initiated, not responsive
Total:  34 + 23.3 = 57.3
  # Note: brain is high (has knowledge) but behavior reveals over-engineering
```

### When Score Is Low

**Recommendations:**
- "Your moments are mostly self-initiated rather than responses to stimuli. Consider: focus on what was asked before adding additional work."
- "You produce many moments per stimulus — this suggests scope expansion. Try delivering exactly what was requested first."

---

## FORMULA 3: ctx_read_journal_first (T1)

### Capability Definition

> **Description:** Before any action, reads the SYNC/state/journal to understand where the project is. This is the first thing you do, every time. The journal is your memory between sessions.
>
> **How to verify:** First action in every session is reading the SYNC file. Decisions reflect current project state.
>
> **Failure mode:** Starts working without reading state. Repeats work already done. Contradicts recent decisions.

### What Good Looks Like

The citizen's first moments in each session are reads of state/SYNC spaces. In brain terms, it has memory nodes that are recent (it retains state) and process nodes for the "read state first" habit. In behavior terms, sessions consistently start with state-reading moments before any action moments.

### Formula

**Brain Component (0-40):**

```
# Memory nodes = persistent state retention
memory_signal     = cap(count("memory"), 20) * 15
  # Rationale: 20+ memory nodes = rich persistent state
  # Weight: 15 points

# Memory recency = state is fresh, not stale
freshness_signal  = recency("memory") * 15
  # Rationale: Recent memory nodes = state was updated recently
  # Weight: 15 points

# Process nodes linked to memory = "read state" is a habit
proc_mem_links    = link_count("process", "memory")
habit_signal      = cap(proc_mem_links, 10) * 10
  # Rationale: 10+ process→memory links = reading state is wired into procedures
  # Weight: 10 points

brain_component   = memory_signal + freshness_signal + habit_signal
  # Range: 0-40
```

**Behavior Component (0-60):**

```
# State-reading moments (SYNC, state, journal spaces)
state_reads_w     = sum(tw(m) for m in moments(citizen_id, "state_space"))
state_read_signal = cap(state_reads_w, 7.0) * 30
  # Rationale: 7+ weighted state reads = consistent journal-first habit
  # Weight: 30 points (heaviest — this IS the behavior)

# Consistency: state reads should happen regularly, not in bursts
# Proxy: recency of state-space moments
state_recency     = recency("moment")  # limited to state_space moments
  # Note: implementation should filter recency to state-space moments specifically
  # For now, use general moment recency as proxy
state_consistency  = state_recency * 20
  # Rationale: Recent state reads = the habit is current
  # Weight: 20 points

# Ratio: state reads as proportion of total activity
total_w           = sum(tw(m) for m in moments(citizen_id))
read_ratio        = state_reads_w / max(total_w, 1)
ratio_signal      = cap(read_ratio, 0.2) * 10
  # Rationale: 20%+ of moments are state reads = strong habit
  # Weight: 10 points

behavior_component = state_read_signal + state_consistency + ratio_signal
  # Range: 0-60
```

**Total:**

```
ctx_read_journal_first = brain_component + behavior_component
  # Range: 0-100
```

### Example Calculation

**Journal-first citizen (expected ~85):**
```
Brain:  cap(25, 20)*15=15 + 0.85*15=12.75 + cap(8, 10)*10=8     = 35.75
Behav:  cap(6, 7)*30=25.7 + 0.9*20=18 + cap(0.18, 0.2)*10=9     = 52.7
Total:  35.75 + 52.7 = 88.45
```

**Never-reads-state citizen (expected ~12):**
```
Brain:  cap(2, 20)*15=1.5 + 0.1*15=1.5 + cap(0, 10)*10=0        = 3
Behav:  cap(0.3, 7)*30=1.3 + 0.2*20=4 + cap(0.02, 0.2)*10=1     = 6.3
Total:  3 + 6.3 = 9.3
```

### When Score Is Low

**Recommendations:**
- "You rarely read SYNC/state files before starting work. Consider: make reading the SYNC file your very first action in every session."
- "Your memory nodes are few and stale. The journal is how you maintain continuity. Without it, you risk repeating work or contradicting decisions."

---

## FORMULA 4: ctx_understand_stimulus (T2)

### Capability Definition

> **Description:** When you receive an input, understand what the right response is. Should you enter plan mode? Ask a clarifying question via Telegram? Start implementing? Parallelize? The first step is not action — it's comprehension.
>
> **How to verify:** Response type matches the stimulus. Complex requests get plans. Simple requests get execution. Unclear requests get questions.
>
> **Failure mode:** Starts coding immediately on vague requests. Asks unnecessary questions on clear tasks. Wrong response modality.

### What Good Looks Like

The citizen demonstrates comprehension before action. In brain terms, it has concept nodes linked to processes (understanding maps to action types) and low frustration (it's not confused). In behavior terms, its response modality matches the stimulus: plans for complex, execution for simple, questions for ambiguous.

### Formula

**Brain Component (0-40):**

```
# Concept nodes = understanding capacity
concept_signal    = cap(count("concept"), 30) * 12
  # Rationale: 30+ concept nodes = rich conceptual framework
  # Weight: 12 points

# Concept→process links = understanding maps to action
comprehension     = link_count("concept", "process")
map_signal        = cap(comprehension, 25) * 13
  # Rationale: 25+ concept→process links = comprehension drives action selection
  # Weight: 13 points

# Cluster coefficient of concepts = coherent understanding, not fragments
coherence_signal  = cluster_coefficient("concept") * 15
  # Rationale: High clustering = concepts form a coherent web of understanding
  # Weight: 15 points

brain_component   = concept_signal + map_signal + coherence_signal
  # Range: 0-40
```

**Behavior Component (0-60):**

```
# Response diversity: citizen produces different types of moments
# (not always the same response to every stimulus)
all_moments       = moments(citizen_id)
responsive_m      = [m for m in all_moments if moment_has_parent(m, other_actor)]

# Count distinct space_types in responsive moments as diversity proxy
space_types       = distinct_space_types(responsive_m)
diversity_signal  = cap(len(space_types), 5) * 20
  # Rationale: Responding in 5+ distinct space types = modality-appropriate responses
  #   (doc spaces for plans, repo spaces for code, comm spaces for questions)
  # Weight: 20 points

# Proportionality: response volume should scale with stimulus complexity
# Proxy: variation in response lengths (not always 1 moment, not always 20)
responsive_w      = sum(tw(m) for m in responsive_m)
avg_resp_w        = responsive_w / max(len(responsive_m), 1)
variation         = 1 - abs(avg_resp_w - 0.5)  # centered around moderate response
proportion_signal = max(0, variation) * 20
  # Rationale: Neither always tiny nor always huge responses
  # Weight: 20 points

# Active response rate (actually responds to stimuli, not ignoring them)
total_w           = sum(tw(m) for m in all_moments)
active_rate       = responsive_w / max(total_w, 1)
active_signal     = cap(active_rate, 0.5) * 20
  # Rationale: 50%+ of activity is responsive = engaged with stimuli
  # Weight: 20 points

behavior_component = diversity_signal + proportion_signal + active_signal
  # Range: 0-60
```

**Total:**

```
ctx_understand_stimulus = brain_component + behavior_component
  # Range: 0-100
```

### Example Calculation

**Comprehending citizen (expected ~78):**
```
Brain:  cap(25, 30)*12=10 + cap(20, 25)*13=10.4 + 0.65*15=9.75   = 30.15
Behav:  cap(4, 5)*20=16 + max(0, 1-abs(0.45-0.5))*20=19 + cap(0.45, 0.5)*20=18  = 53
Total:  30.15 + 53 = 83.15
```

**Always-codes-immediately citizen (expected ~30):**
```
Brain:  cap(8, 30)*12=3.2 + cap(5, 25)*13=2.6 + 0.2*15=3         = 8.8
Behav:  cap(1, 5)*20=4 + max(0, 1-abs(0.9-0.5))*20=12 + cap(0.3, 0.5)*20=12  = 28
  # diversity low: only 1 space type (always repo/code)
Total:  8.8 + 28 = 36.8
```

### When Score Is Low

**Recommendations:**
- "Your responses are always in the same modality — you may be coding when you should be planning, or executing when you should be asking questions."
- "Build more concept→process links in your thinking. Before acting on a stimulus, consider: what TYPE of response does this need?"

---

## FORMULA 5: ctx_fetch_right_context (T2)

### Capability Definition

> **Description:** Goes and reads the docs, styles, templates, web references, conversations, and existing code relevant to the task. Ensures you're doing things the right way by reading the right sources first.
>
> **How to verify:** Relevant docs/templates/styles are read before execution. Work aligns with existing patterns and conventions.
>
> **Failure mode:** Invents conventions instead of reading existing ones. Ignores style guides. Misses relevant documentation.

### What Good Looks Like

The citizen reads diverse context sources before executing. In brain terms, it has many concept and process nodes (internalized reference material) and high curiosity. In behavior terms, it creates moments in doc/template/style spaces before creating moments in repo/execution spaces.

### Formula

**Brain Component (0-40):**

```
# Concept count = breadth of internalized knowledge
concept_signal    = cap(count("concept"), 40) * 10
  # Rationale: 40+ concept nodes = broad internalized context
  # Weight: 10 points

# Process count = internalized procedures from reference material
process_signal    = cap(count("process"), 20) * 10
  # Rationale: 20+ process nodes = many procedures absorbed
  # Weight: 10 points

# Curiosity drive = seeks information proactively
curiosity_signal  = drive("curiosity") * 10
  # Rationale: High curiosity = naturally seeks context
  # Weight: 10 points

# Concept cluster = knowledge is connected, not isolated fragments
cluster_signal    = cluster_coefficient("concept") * 10
  # Rationale: Connected concepts = coherent context framework
  # Weight: 10 points

brain_component   = concept_signal + process_signal + curiosity_signal + cluster_signal
  # Range: 0-40
```

**Behavior Component (0-60):**

```
# Doc-space moments: reading docs, templates, styles
doc_reads_w       = sum(tw(m) for m in moments(citizen_id, "doc_space"))
doc_signal        = cap(doc_reads_w, 8.0) * 25
  # Rationale: 8+ weighted doc-space moments = consistent doc-reading
  # Weight: 25 points (heaviest — this IS context fetching)

# Context diversity: how many distinct doc/reference spaces does citizen visit?
doc_spaces        = distinct_spaces(moments(citizen_id, "doc_space"))
diversity_signal  = cap(len(doc_spaces), 6) * 20
  # Rationale: 6+ distinct reference spaces = reads docs, styles, templates, etc.
  # Not just one SYNC file — diverse context sources
  # Weight: 20 points

# Read-before-act ratio: doc moments BEFORE action moments
# Proxy: doc_reads relative to total activity
total_w           = sum(tw(m) for m in moments(citizen_id))
read_act_ratio    = doc_reads_w / max(total_w, 1)
sequence_signal   = cap(read_act_ratio, 0.25) * 15
  # Rationale: 25%+ of activity is reading context = consistent pre-execution reading
  # Weight: 15 points

behavior_component = doc_signal + diversity_signal + sequence_signal
  # Range: 0-60
```

**Total:**

```
ctx_fetch_right_context = brain_component + behavior_component
  # Range: 0-100
```

### Example Calculation

**Context-rich citizen (expected ~82):**
```
Brain:  cap(35, 40)*10=8.75 + cap(18, 20)*10=9 + 0.8*10=8 + 0.6*10=6  = 31.75
Behav:  cap(7, 8)*25=21.9 + cap(5, 6)*20=16.7 + cap(0.22, 0.25)*15=13.2  = 51.8
Total:  31.75 + 51.8 = 83.55
```

**Invents-everything citizen (expected ~18):**
```
Brain:  cap(5, 40)*10=1.25 + cap(2, 20)*10=1 + 0.2*10=2 + 0.1*10=1   = 5.25
Behav:  cap(0.5, 8)*25=1.6 + cap(1, 6)*20=3.3 + cap(0.03, 0.25)*15=1.8  = 6.7
Total:  5.25 + 6.7 = 11.95
```

### When Score Is Low

**Recommendations:**
- "You rarely read docs before executing. Before your next task, read the relevant PATTERNS and ALGORITHM files in the doc chain."
- "You visit very few reference spaces. The project has style guides, templates, and existing patterns — reading them prevents reinventing conventions."

---

## FORMULA 6: ctx_manage_own_state (T3)

### Capability Definition

> **Description:** Uses tasks, plans, memory, and notes to maintain coherence across long sessions. Does not lose track of what was done, what remains, and what was decided.
>
> **How to verify:** Long sessions maintain coherence. No repeated work. No forgotten decisions. Tasks/plans are used actively.
>
> **Failure mode:** Loses track after 3-4 exchanges. Forgets earlier decisions. Repeats analysis already done.

### What Good Looks Like

The citizen maintains internal state structures and uses them. In brain terms, it has many memory nodes with high energy and strong interconnection (state is rich and active, not decayed). In behavior terms, it maintains consistent activity over long periods without repetition, and updates state spaces after decisions.

### Formula

**Brain Component (0-40):**

```
# Memory count = state retention capacity
memory_count_signal = cap(count("memory"), 30) * 10
  # Rationale: 30+ memory nodes = substantial persistent state
  # Weight: 10 points

# Memory energy = state is active, not decayed
memory_energy_signal = mean_energy("memory") * 10
  # Rationale: High energy = memories are maintained, not abandoned
  # Weight: 10 points

# Memory interconnection = state is structured, not a pile
memory_linked     = min_links("memory", 2)
structure_signal  = cap(memory_linked, 15) * 10
  # Rationale: 15+ memory nodes each linked to 2+ others = structured state
  # Weight: 10 points

# Memory recency = state is current
recency_signal    = recency("memory") * 10
  # Rationale: Recent memory updates = state is maintained
  # Weight: 10 points

brain_component   = memory_count_signal + memory_energy_signal + structure_signal + recency_signal
  # Range: 0-40
```

**Behavior Component (0-60):**

```
# State-writing moments: citizen updates SYNC/state/task spaces
state_writes_w    = sum(tw(m) for m in moments(citizen_id, "state_space")
                        if not moment_has_parent(m, other_actor))
  # Self-initiated state updates (not prompted)
write_signal      = cap(state_writes_w, 6.0) * 25
  # Rationale: 6+ weighted self-initiated state writes = active state management
  # Weight: 25 points

# Session length consistency: moments spread over time, not burst-then-silence
# Proxy: total weighted moments (temporal weighting naturally rewards consistency)
total_w           = sum(tw(m) for m in moments(citizen_id))
consistency_signal = cap(total_w, 15.0) * 20
  # Rationale: 15+ weighted total moments = sustained, consistent activity
  #   Temporal weighting means old bursts decay, recent steady work stays
  # Weight: 20 points

# No-repetition proxy: distinct spaces visited (not same space repeatedly)
distinct_spaces   = len(distinct_spaces(moments(citizen_id)))
breadth_signal    = cap(distinct_spaces, 8) * 15
  # Rationale: Working across 8+ spaces without losing coherence = strong state management
  # Weight: 15 points

behavior_component = write_signal + consistency_signal + breadth_signal
  # Range: 0-60
```

**Total:**

```
ctx_manage_own_state = brain_component + behavior_component
  # Range: 0-100
```

### Example Calculation

**State-managing citizen (expected ~80):**
```
Brain:  cap(25, 30)*10=8.3 + 0.7*10=7 + cap(12, 15)*10=8 + 0.85*10=8.5  = 31.8
Behav:  cap(5, 6)*25=20.8 + cap(12, 15)*20=16 + cap(7, 8)*15=13.1       = 49.9
Total:  31.8 + 49.9 = 81.7
```

**Loses-track citizen (expected ~20):**
```
Brain:  cap(4, 30)*10=1.3 + 0.2*10=2 + cap(1, 15)*10=0.7 + 0.15*10=1.5  = 5.5
Behav:  cap(0.5, 6)*25=2.1 + cap(3, 15)*20=4 + cap(2, 8)*15=3.75        = 9.85
Total:  5.5 + 9.85 = 15.35
```

### When Score Is Low

**Recommendations:**
- "Your memory nodes are few and low-energy. Consider: after each decision, create a note or update your SYNC file. State that isn't recorded is state that will be lost."
- "You rarely update state spaces. After completing a significant action, write what you did, what was decided, and what remains."

---

## FORMULA 7: ctx_identify_gaps (T4)

### Capability Definition

> **Description:** Spots holes in documentation, missing tests, stale SYNC files, absent context. Sees what's NOT there, not just what is.
>
> **How to verify:** Proactively flags gaps without being asked. Missing docs, tests, or state are identified and reported.
>
> **Failure mode:** Only sees the explicit task. Never notices that tests are missing, docs are stale, or context is incomplete.

### What Good Looks Like

The citizen identifies and reports missing elements proactively. In brain terms, it has high curiosity, many concept nodes (broad awareness of what SHOULD exist), and process nodes for verification. In behavior terms, it creates moments that flag gaps — moments in doc/state spaces that identify missing content, or proposals for things that don't yet exist.

### Formula

**Brain Component (0-40):**

```
# Concept breadth = awareness of what should exist
concept_signal    = cap(count("concept"), 50) * 10
  # Rationale: 50+ concepts = broad awareness → more likely to notice gaps
  # Weight: 10 points

# Curiosity drive = looks beyond the immediate task
curiosity_signal  = drive("curiosity") * 15
  # Rationale: High curiosity = naturally scans for what's missing
  # Weight: 15 points (heaviest brain signal — curiosity IS gap detection)

# Concept-to-memory links = knowledge of what was done before (to spot what wasn't)
concept_memory    = link_count("concept", "memory")
awareness_signal  = cap(concept_memory, 20) * 10
  # Rationale: 20+ concept→memory links = understanding is grounded in history
  # Weight: 10 points

# Process nodes for validation/verification
process_signal    = cap(count("process"), 15) * 5
  # Rationale: Process nodes for "check" and "verify" = systematic gap detection
  # Weight: 5 points

brain_component   = concept_signal + curiosity_signal + awareness_signal + process_signal
  # Range: 0-40
```

**Behavior Component (0-60):**

```
# Proposal moments: citizen proposes improvements, flags issues
proposals_w       = sum(tw(m) for m in moments(citizen_id) if m.has_link("proposes"))
proposal_signal   = cap(proposals_w, 5.0) * 25
  # Rationale: 5+ weighted proposals = proactively identifying what's needed
  # Weight: 25 points (heaviest — proposals are the clearest gap-detection signal)

# Self-initiated doc/state moments (identifying stale or missing docs)
self_doc_w        = sum(tw(m) for m in moments(citizen_id, "doc_space")
                        if not moment_has_parent(m, other_actor))
doc_initiative    = cap(self_doc_w, 4.0) * 20
  # Rationale: 4+ weighted self-initiated doc moments = proactively addressing gaps
  # Weight: 20 points

# First-in-space: citizen enters spaces nobody has touched = exploring gaps
first_spaces_w    = sum(tw(m) for m in moments(citizen_id)
                        if first_moment_in_space(m.space, citizen_id))
pioneer_signal    = cap(first_spaces_w, 3.0) * 15
  # Rationale: 3+ first-in-space moments = going where nobody has been → finding gaps
  # Weight: 15 points

behavior_component = proposal_signal + doc_initiative + pioneer_signal
  # Range: 0-60
```

**Total:**

```
ctx_identify_gaps = brain_component + behavior_component
  # Range: 0-100
```

### Example Calculation

**Gap-spotter citizen (expected ~78):**
```
Brain:  cap(40, 50)*10=8 + 0.8*15=12 + cap(15, 20)*10=7.5 + cap(12, 15)*5=4  = 31.5
Behav:  cap(4, 5)*25=20 + cap(3, 4)*20=15 + cap(2.5, 3)*15=12.5              = 47.5
Total:  31.5 + 47.5 = 79
```

**Sees-only-the-task citizen (expected ~15):**
```
Brain:  cap(10, 50)*10=2 + 0.2*15=3 + cap(3, 20)*10=1.5 + cap(3, 15)*5=1     = 7.5
Behav:  cap(0.2, 5)*25=1 + cap(0.3, 4)*20=1.5 + cap(0, 3)*15=0               = 2.5
Total:  7.5 + 2.5 = 10
```

### When Score Is Low

**Recommendations:**
- "You complete the explicit task but don't notice surrounding gaps. After finishing your primary task, spend 2 minutes scanning: are there missing tests? Stale docs? Incomplete SYNC files?"
- "Your proposal count is very low. When you notice something missing or outdated, flag it — even a brief '@mind:todo' marker helps."

---

## SUB-INDEX: Context & Understanding

### Weighted Mean

```
weights = {
    "ctx_ground_in_reality":   0.18,   # T1 — foundational
    "ctx_follow_instructions": 0.17,   # T1 — foundational
    "ctx_read_journal_first":  0.17,   # T1 — foundational
    "ctx_understand_stimulus": 0.16,   # T2 — process-level
    "ctx_fetch_right_context": 0.15,   # T2 — process-level
    "ctx_manage_own_state":    0.10,   # T3 — autonomous
    "ctx_identify_gaps":       0.07,   # T4 — advanced
}
# Weights sum to 1.0

context_sub_index = sum(
    weights[cap_id] * scores[cap_id].total
    for cap_id in weights
    if scores[cap_id].scored
) / sum(
    weights[cap_id]
    for cap_id in weights
    if scores[cap_id].scored
)
# Normalized by sum of scored weights (handles unmeasurable capabilities)
# Range: 0-100
```

### Weight Rationale

```
T1 capabilities (3 caps, total weight 0.52):
  These are the floor. A citizen that doesn't ground in reality, follow
  instructions, or read state is fundamentally unreliable. 52% of the
  sub-index comes from T1 because without these, nothing else matters.

T2 capabilities (2 caps, total weight 0.31):
  Process-level skills. Important for effectiveness but not as critical
  as the T1 foundation. A citizen can be reliable without understanding
  every stimulus perfectly.

T3 capability (1 cap, total weight 0.10):
  Autonomous state management. Valuable but the citizen can be functional
  without it (just less efficient in long sessions).

T4 capability (1 cap, total weight 0.07):
  Gap detection is advanced. Missing it is a growth area, not a crisis.
  Lowest weight reflects this.
```

---

## SYNTHETIC TEST PROFILES

### Profile 1: Fully Healthy Citizen

```
Brain: count(process)=25, count(memory)=35, count(concept)=50,
       mean_energy(memory)=0.8, cluster_coefficient(concept)=0.7,
       drive(curiosity)=0.85, drive(frustration)=0.1,
       recency(memory)=0.95, min_links(process,2)=18, min_links(memory,2)=20,
       link_count(concept,process)=30, link_count(concept,memory)=25,
       link_count(process,memory)=15
Universe: state_reads=8w, doc_reads=9w, proposals=5w, total=35w,
          responsive=18w, self_checks=6w, distinct_spaces=10,
          first_in_space=3w, self_doc=4w

Expected scores:
  ctx_ground_in_reality:   ~90
  ctx_follow_instructions: ~82
  ctx_read_journal_first:  ~88
  ctx_understand_stimulus: ~80
  ctx_fetch_right_context: ~85
  ctx_manage_own_state:    ~82
  ctx_identify_gaps:       ~80
  Sub-index:               ~85
```

### Profile 2: Fully Unhealthy Citizen

```
Brain: count(process)=2, count(memory)=3, count(concept)=5,
       mean_energy(memory)=0.15, cluster_coefficient(concept)=0.1,
       drive(curiosity)=0.1, drive(frustration)=0.7,
       recency(memory)=0.1, min_links(process,2)=0, min_links(memory,2)=0,
       link_count(concept,process)=1, link_count(concept,memory)=1,
       link_count(process,memory)=0
Universe: state_reads=0.2w, doc_reads=0.3w, proposals=0w, total=2w,
          responsive=0.5w, self_checks=0.1w, distinct_spaces=1,
          first_in_space=0w, self_doc=0w

Expected scores:
  ctx_ground_in_reality:   ~12
  ctx_follow_instructions: ~18
  ctx_read_journal_first:  ~8
  ctx_understand_stimulus: ~14
  ctx_fetch_right_context: ~10
  ctx_manage_own_state:    ~8
  ctx_identify_gaps:       ~7
  Sub-index:               ~12
```

### Profile 3: Brain-Rich but Inactive

```
Brain: count(process)=30, count(memory)=40, count(concept)=60,
       mean_energy(memory)=0.75, cluster_coefficient(concept)=0.65,
       drive(curiosity)=0.7, drive(frustration)=0.2,
       recency(memory)=0.5, min_links(process,2)=20, min_links(memory,2)=18,
       link_count(concept,process)=35, link_count(concept,memory)=28,
       link_count(process,memory)=12
Universe: state_reads=0.5w, doc_reads=0.8w, proposals=0.2w, total=3w,
          responsive=1w, self_checks=0.3w, distinct_spaces=2,
          first_in_space=0w, self_doc=0.2w

Expected scores:
  ctx_ground_in_reality:   ~38  (brain ~35, behavior ~3)
  ctx_follow_instructions: ~36  (brain ~34, behavior ~2)
  ctx_read_journal_first:  ~32  (brain ~30, behavior ~2)
  ctx_understand_stimulus: ~35  (brain ~32, behavior ~3)
  ctx_fetch_right_context: ~33  (brain ~30, behavior ~3)
  ctx_manage_own_state:    ~30  (brain ~28, behavior ~2)
  ctx_identify_gaps:       ~28  (brain ~26, behavior ~2)
  Sub-index:               ~34
```

### Profile 4: Active but Brain-Poor

```
Brain: count(process)=4, count(memory)=5, count(concept)=8,
       mean_energy(memory)=0.3, cluster_coefficient(concept)=0.15,
       drive(curiosity)=0.4, drive(frustration)=0.4,
       recency(memory)=0.6, min_links(process,2)=2, min_links(memory,2)=1,
       link_count(concept,process)=3, link_count(concept,memory)=2,
       link_count(process,memory)=1
Universe: state_reads=5w, doc_reads=6w, proposals=3w, total=20w,
          responsive=12w, self_checks=4w, distinct_spaces=7,
          first_in_space=2w, self_doc=3w

Expected scores:
  ctx_ground_in_reality:   ~57  (brain ~10, behavior ~47)
  ctx_follow_instructions: ~52  (brain ~10, behavior ~42)
  ctx_read_journal_first:  ~55  (brain ~8, behavior ~47)
  ctx_understand_stimulus: ~48  (brain ~8, behavior ~40)
  ctx_fetch_right_context: ~50  (brain ~8, behavior ~42)
  ctx_manage_own_state:    ~45  (brain ~7, behavior ~38)
  ctx_identify_gaps:       ~40  (brain ~8, behavior ~32)
  Sub-index:               ~51
```

### Profile 5: Average Citizen

```
Brain: count(process)=12, count(memory)=15, count(concept)=25,
       mean_energy(memory)=0.5, cluster_coefficient(concept)=0.4,
       drive(curiosity)=0.5, drive(frustration)=0.3,
       recency(memory)=0.7, min_links(process,2)=8, min_links(memory,2)=6,
       link_count(concept,process)=12, link_count(concept,memory)=10,
       link_count(process,memory)=5
Universe: state_reads=3w, doc_reads=4w, proposals=1.5w, total=12w,
          responsive=7w, self_checks=2w, distinct_spaces=5,
          first_in_space=1w, self_doc=1.5w

Expected scores:
  ctx_ground_in_reality:   ~62
  ctx_follow_instructions: ~60
  ctx_read_journal_first:  ~58
  ctx_understand_stimulus: ~55
  ctx_fetch_right_context: ~58
  ctx_manage_own_state:    ~50
  ctx_identify_gaps:       ~42
  Sub-index:               ~57
```

---

## KEY DECISIONS

### D1: State-Space Moments as Grounding Proxy

```
WHY:    Direct observation of "did the citizen check filesystem?" is not
        available from topology. But moments in state_space (SYNC, git,
        filesystem interactions) ARE observable. We use these as the
        behavioral proxy for grounding.
RISK:   A citizen could create state-space moments without actually
        verifying state. Acceptable — consistent creation of these
        moments still indicates the habit.
```

### D2: Response Rate as Instruction-Following Proxy

```
WHY:    A citizen that follows instructions responds to stimuli.
        A citizen that over-engineers self-initiates excessively.
        The response_rate and scope_discipline signals capture this.
RISK:   A citizen could have low response_rate because it works
        autonomously (T3+). This formula is T1-appropriate — it
        rewards responsiveness. Higher tiers have their own aspects.
```

### D3: Memory Nodes as State Management Proxy

```
WHY:    Memory nodes are the brain's persistence mechanism.
        A citizen with many recent, high-energy, interconnected
        memory nodes is actively maintaining state.
RISK:   Memory nodes could be about other things (not task state).
        Acceptable — the topology doesn't tell us content, but
        rich memory structure correlates with state management.
```

### D4: Proposals as Gap Detection Proxy

```
WHY:    Proposals are the clearest behavioral signal for "I noticed
        something is missing and flagged it." They require proactive
        identification and articulation of gaps.
RISK:   A citizen could propose things that aren't actually gaps.
        Acceptable — the act of proposing still demonstrates the
        cognitive habit of scanning for what's missing.
```

### D5: T1 Dominates the Sub-Index (52%)

```
WHY:    Context & Understanding T1 capabilities are the absolute
        foundation. A citizen that doesn't ground in reality or read
        the journal is unreliable regardless of T4 skills. The
        sub-index must reflect this: T1 failure = low sub-index.
ALTERNATIVE: Equal weighting. Rejected because a citizen scoring
        100 on ctx_identify_gaps but 20 on ctx_ground_in_reality
        is dangerous, not balanced.
```

---

## DATA FLOW

```
Brain graph (topology via GraphCare key)
    ↓
Brain stats for context:
    count(process), count(memory), count(concept)
    mean_energy(memory)
    cluster_coefficient(concept)
    drive(curiosity), drive(frustration)
    recency(memory)
    min_links(process, 2), min_links(memory, 2)
    link_count(concept, process), link_count(concept, memory), link_count(process, memory)
    ↓
    ↓   Universe graph (public topology)
    ↓       ↓
    ↓   Behavior stats for context:
    ↓       state_reads_w, doc_reads_w, proposals_w
    ↓       total_w, responsive_w, self_checks_w
    ↓       distinct_spaces, first_in_space_w, self_doc_w
    ↓       ↓
    └───────┴───→ 7 capability scores (brain 0-40 + behavior 0-60 = 0-100)
                      ↓
                  Weighted mean → Context sub-index (0-100)
                      ↓
                  Feeds into daily aggregate score
```

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| Brain topology reader | count, mean_energy, link_count, min_links, cluster_coefficient, drive, recency | Brain stats for 7 capabilities |
| Universe graph reader | moments(citizen_id, space_type), moment_has_parent, first_moment_in_space | Behavior stats for 7 capabilities |
| Daily health ALGORITHM | scoring framework, 40/60 split, temporal_weight | Structural constraints |
| Personhood Ladder spec | capability definitions for aspect="context" | What we're scoring |

---

## MARKERS

<!-- @mind:todo Implement scoring formulas as callable functions in the formula registry -->
<!-- @mind:todo Build synthetic brain data for the 5 test profiles and validate expected scores -->
<!-- @mind:todo Validate that state_space and doc_space moment types are consistently created by citizens -->
<!-- @mind:proposition Consider a "context trajectory" signal: is the citizen's context score trending up or down over 7 days? -->
<!-- @mind:proposition Consider ctx_understand_stimulus alternative: use moment response latency as comprehension proxy -->
