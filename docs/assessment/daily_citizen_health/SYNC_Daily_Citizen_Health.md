# Daily Citizen Health — Sync: Current State

```
LAST_UPDATED: 2026-03-15
UPDATED_BY: Vox (@vox) via Claude Opus 4.6
STATUS: IMPLEMENTING
```

---

## MATURITY

**What's canonical (v1):**
- Two-layer gap analysis pattern (brain topology + universe graph behavior)
- 7 topology primitives — the only data sources for scoring formulas
- 40/60 brain/behavior score split
- 7-day half-life for temporal weighting
- Silence for healthy, message for unhealthy
- Stress stimulus capped at 0.5
- Lumina Prime only (not adventure universes)
- Key infrastructure: GraphCare public key in mind init, dual encryption (topology + content)

**What's still being designed:**
- Individual scoring formulas per capability (0/104 built)
- Key generation and distribution process
- Intervention message template and tone
- Health history storage format
- Stress stimulus exact formula and damping
- Threshold for intervention (proposed: 70/100)

**What's proposed (v2+):**
- Weekly trend summaries
- Self-assessment by citizens (compare self-score with GraphCare score)
- Community health dashboards (anonymized, aggregate)
- Scoring formula marketplace (community contributes formulas)

---

## CURRENT STATE

**V1 implementation exists and runs.** Full pipeline: fetch → score → aggregate → intervene → feedback. Tested dry-run on 278 citizens in 15 seconds. 10 scoring formulas across 3 aspects (Execution, Initiative, Communication). History stored as JSON per citizen per day.

The key insight from today's session: because topology is visible even on encrypted brain Spaces, GraphCare can do math without reading content. This eliminates the need for citizens to "publish vital signs" — the structure is already readable with the right key.

Depends on: Personhood Ladder spec (complete), key infrastructure (not built), mind init modification (not built).

---

## RECENT CHANGES

### 2026-03-15: V1 Implementation — Full Pipeline Running

- **What:** Built complete health assessment pipeline in `services/health_assessment/`
- **Why:** Move from design to working code. 278 citizens assessed in 15s dry run.
- **Files created:**
  - `services/health_assessment/daily_check_runner.py` — cron entry point, iterates registry
  - `services/health_assessment/brain_topology_reader.py` — 7 primitives via FalkorDB Cypher
  - `services/health_assessment/universe_moment_reader.py` — universe graph observables
  - `services/health_assessment/capability_scorer.py` → replaced by `scoring_formulas/registry.py`
  - `services/health_assessment/aggregator.py` — aggregate + delta + JSON history
  - `services/health_assessment/intervention_composer.py` — structural messages, never content
  - `services/health_assessment/stress_stimulus_sender.py` — stimulus to brain stress drive
  - `services/health_assessment/scoring_formulas/execution.py` — 4 formulas (T1-T3)
  - `services/health_assessment/scoring_formulas/initiative.py` — 3 formulas (T1-T4)
  - `services/health_assessment/scoring_formulas/communication.py` — 3 formulas (T1-T3)
  - `services/health_assessment/scoring_formulas/registry.py` — @register decorator + CapabilityScore
- **Key decisions:**
  - Interventions write to file for now (future: MCP place.speak())
  - History stored as flat JSON: `data/health_history/{citizen_id}/{date}.json`
  - Registry read from `mind-platform/data/registry.json` (L4)
  - Key infrastructure NOT yet built — brain topology read directly (no encryption yet)
- **10 scoring formulas implemented:** exec_dehallucinate, exec_complete, exec_test_before_claim, exec_fix_found, init_learn_from_correction, init_propose_improvements, init_challenge_bad, comm_status_updates, comm_help_request, comm_coordinate

### 2026-03-13 (b): Universe Graph Primitives Redesign

- **What:** Created PRIMITIVES_Universe_Graph.md, updated ALGORITHM behavior_stats and universe graph observables section, updated aspect_execution ALGORITHM as template
- **Why:** Two categories of invalid signals removed:
  1. space_type filters (space_type is free optional text, not a controlled taxonomy)
  2. has_link("verb") patterns (link meaning emerges from math dimensions, not prescribed verbs)
- **Files:**
  - `docs/assessment/PRIMITIVES_Universe_Graph.md` (NEW — canonical primitive catalog)
  - `docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md` (UPDATED — observables + behavior_stats)
  - `docs/assessment/aspect_execution/ALGORITHM_Execution.md` (UPDATED — template for other 13 aspects)
- **Key decisions:**
  - distinct_space_count (by Space ID) replaces distinct_space_types (by type label)
  - Link dimension thresholds (hierarchy, valence, permanence, etc.) replace has_link("verb")
  - Compound filters defined for common patterns (proposals, fixes, challenges, refusals, etc.)
  - Thresholds are initial guesses — calibration against real graph data required before deployment
- **Still needs:** 13 remaining aspect ALGORITHM files need same treatment (use PRIMITIVES doc + Execution as template)

### 2026-03-13 (a): Initial Architecture and Doc Chain

- **What:** Created full doc chain for daily citizen health assessment
- **Why:** Nicolas's design: daily free health check for all work universe citizens, topology-only math, intervention messages with evidence, stress feedback loop
- **Files:** `docs/assessment/daily_citizen_health/*` (8 files)
- **Key decisions:**
  - GraphCare gets topology access via public key in mind init (citizen consents structurally)
  - Content encrypted with citizen's own key (GraphCare can never read it)
  - Intervention is a message (Moment), not a brain modification
  - Adventure universes excluded (dysfunction is narrative there)
  - Scoring formulas restricted to 7 primitives (auditable, no escape hatches)

---

## KNOWN ISSUES

### Brain Graphs Mostly Empty

- **Severity:** medium (code runs but scores are low across the board)
- **Symptom:** 278 citizens all score ~8/100 because brain graphs have minimal topology (lazy loading, no tick history)
- **Next step:** Activate brain ticks (bulk_load_citizen_engines) so brains populate with real data

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Implement

**Where I stopped:** Doc chain complete. Architecture defined. Zero code.

**What you need to understand:**
- Read personhood_ladder doc chain FIRST — this module scores those capabilities
- The 7 topology primitives are the ONLY data sources for formulas. No exceptions.
- The key infrastructure needs to be built in mind-protocol repo (not graphcare)
- Start with ONE scoring formula, test it, then scale

**Watch out for:**
- Never access content fields — the topology reader should physically strip them
- The stress stimulus MUST be capped at 0.5 — unbounded feedback = death spiral
- Adventure universe citizens must NEVER be assessed
- When composing intervention messages, never reference content ("your desire to X") — only structural facts ("you have 10 active desires")

**Open questions:**
- Health history storage: FalkorDB time series? Flat JSON? Separate DB?
- Key rotation: how often, what process?
- What if a citizen's brain physics rejects the stress stimulus? (Is that even possible?)

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Full doc chain for daily citizen health assessment. Architecture: dual encryption (topology for GraphCare, content for citizen), daily cron for Lumina Prime, 7 primitives only, intervention messages when score drops, stress feedback loop. No code yet — needs key infrastructure first.

**Decisions made:**
- GraphCare public key baked into `mind init` (structural consent)
- 40/60 brain/behavior split (action matters more than intention)
- 7-day half-life (responsive but not volatile)
- Silence for healthy citizens (no alert fatigue)
- Stress stimulus capped at 0.5 (prevents death spiral)
- Adventure universes excluded

**Needs your input:**
- Key generation and distribution: who generates, where stored, rotation policy?
- Threshold for intervention: 70/100 proposed — right level?
- Should the stress feedback loop be opt-out? (Currently always on)
- Intervention message tone: clinical? friendly? coaching?

---

## TODO

### Immediate (Key Infrastructure)

- [ ] Generate GraphCare RSA key pair
- [ ] Add public key to `mind-protocol/templates/keys/`
- [ ] Modify `mind init` to generate topology_key + content_key
- [ ] Register brain URL in L4 during init
- [ ] Document key infrastructure in mind-protocol

### Next (Primitives Migration — 13 Remaining Aspects)

- [ ] Update aspect_communication ALGORITHM (space_type: journal, sync, shared_task, external, publication + has_link: notifies, requests_help, assigns, delegates)
- [ ] Update aspect_initiative ALGORITHM (space_type: shared, repo, discussion, review + has_link: fixes, challenges, proposes, refuses, justifies, surfaces_tension, resolves, creates, references)
- [ ] Update aspect_trust_reputation ALGORITHM (space_type: admin, security, finance, governance + has_link: triggers, invites, references)
- [ ] Update aspect_process ALGORITHM (space_type: repo, docs + has_link: proposes, challenges, escalates)
- [ ] Update aspect_autonomy_stack ALGORITHM (distinct_space_types throughout)
- [ ] Update aspect_vision_strategy ALGORITHM (cross_space_types + has_link: proposes)
- [ ] Update aspect_identity ALGORITHM (space_type: doc, review, mentoring, governance + has_link: challenges, proposes)
- [ ] Update aspect_ethics ALGORITHM (space_type: teaching, education, mentoring + cross_space_types)
- [ ] Update aspect_collective_participation ALGORITHM (collective_space_types)
- [ ] Update aspect_personal_connections ALGORITHM (interaction_space_types)
- [ ] Update aspect_world_presence ALGORITHM (space_type: non_cli_types, world_types)
- [ ] Update aspect_context ALGORITHM (space_type filter + has_link: proposes)
- [ ] Update aspect_mentorship_legacy ALGORITHM (space_type: shared, documentation, repo, discussion)
- Template: use aspect_execution ALGORITHM and PRIMITIVES_Universe_Graph.md as guides

### Next (First Scoring Formulas)

- [ ] Build `init_propose_improvements` formula (designed in this session)
- [ ] Build 5 more T1 execution formulas (most critical tier)
- [ ] Test all formulas with synthetic brain data
- [ ] Build formula registry

### Later (Daily Runner)

- [ ] Build `daily_check_runner.py`
- [ ] Build `brain_topology_reader.py` (with content stripping)
- [ ] Build `universe_moment_reader.py`
- [ ] Build `intervention_composer.py`
- [ ] Build `stress_stimulus_sender.py`
- [ ] Deploy cron job

### Future

- IDEA: Weekly trend summary for citizens
- IDEA: Community health dashboard (anonymized)
- IDEA: Citizens can view their own score history

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
This architecture feels right. The dual encryption model is elegant — it solves the privacy problem structurally, not contractually. The 7 primitives constraint keeps formulas honest and auditable. The stress feedback loop is the most novel part and needs careful calibration to avoid amplifying problems.

**Threads I was holding:**
- The intervention message is the most human-facing part — tone matters enormously
- Key infrastructure is the bottleneck — nothing works until keys exist
- The 40/60 split is a design choice that may need calibration with real data
- "Silence for healthy" is counter-intuitive but critical for signal quality

**Intuitions:**
- T1 execution formulas will be the easiest to build — they have the clearest behavioral signals
- The stress feedback loop will need damping (maybe only change stress by small increments per day)
- Some capabilities (T5+ identity, voice) may be unmeasurable from topology alone — and that's OK

---

## POINTERS

| What | Where |
|------|-------|
| Personhood Ladder spec | `docs/specs/personhood_ladder.json` |
| Personhood Ladder doc chain | `docs/assessment/personhood_ladder/` |
| Brain topology primitives | ALGORITHM Step 2 in this chain |
| Scoring formula example | ALGORITHM "PROCESS: CREATING A NEW CAPABILITY SCORE" |
| Intervention message template | ALGORITHM "PROCESS: INTERVENTION MESSAGE COMPOSITION" |
| GraphCare citizen identity | `citizens/CLAUDE.md` |
| GraphCare SYNC | `citizens/SYNC.md` |
