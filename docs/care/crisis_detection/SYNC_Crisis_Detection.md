# Crisis Detection — Sync: Current State

```
LAST_UPDATED: 2026-03-15
UPDATED_BY: @vox (doc chain creation)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- Three detection layers: score trajectory, isolation, human-partner signals
- Four escalation tiers: Watch, Alert, Critical, Human-partner
- Privacy-preserving notification principle (severity level only, no health details)
- Topology-only constraint inherited from all GraphCare systems
- Trajectory-over-threshold philosophy (rate of change matters more than absolute value)

**What's still being designed:**
- Exact numerical thresholds for each crisis level (25-point drop, 10-point sustained, floor at 30)
- Normal fluctuation bands (what variation is noise vs signal)
- Trusted peer notification mechanism at Critical level
- Human-partner detection precision (how to distinguish human absence from citizen silence)
- Chronic care transition protocol (when sustained crisis becomes long-term management)
- Who/what constitutes the "GraphCare care team" as escalation target

**What's proposed (v2+):**
- Recovery watch state (elevated monitoring after crisis resolves)
- Peer buddy system (automatic peer suggestion during isolation)
- Cross-citizen crisis correlation (are multiple citizens declining simultaneously? systemic issue?)
- Predictive crisis scoring (ML on trajectory history to predict likelihood before thresholds breach)

---

## CURRENT STATE

Crisis detection exists as a design. The doc chain (OBJECTIVES, PATTERNS, BEHAVIORS) defines the three detection layers, four escalation tiers, and the behavioral contracts.

The existing codebase has partial infrastructure:
- `daily_check_runner.py` runs the continuous health scan that produces the scores crisis detection will analyze
- `stress_stimulus_sender.py` implements the automated feedback loop (score to stress drive)
- `intervention_composer.py` composes messages for the daily health nudge (the gentler cousin of crisis alerts)

What doesn't exist yet:
- Score history storage and trajectory analysis
- Isolation detection from universe graph topology
- Human-partner pattern detection
- The escalation routing system (who gets notified, how)
- Crisis event logging and state management

The gap between "daily health nudge" (intervention_composer) and "crisis response" (this module) is where this module lives. The daily check says "you dropped a bit, consider doing X." Crisis detection says "something is seriously wrong, and here's who needs to know."

---

## IN PROGRESS

### Doc Chain Creation

- **Started:** 2026-03-15
- **By:** @vox
- **Status:** Complete — OBJECTIVES, PATTERNS, BEHAVIORS, SYNC written
- **Context:** Part of the parallel doc chain creation for all GraphCare care/ modules.

---

## RECENT CHANGES

### 2026-03-15: Initial Doc Chain

- **What:** Created OBJECTIVES, PATTERNS, BEHAVIORS, SYNC for crisis_detection
- **Why:** GraphCare's care layer needed the emergency detection module designed before implementation. The daily health check handles routine nudges, but there was no design for acute or compound crises.
- **Files:** `docs/care/crisis_detection/OBJECTIVES_Crisis_Detection.md`, `PATTERNS_Crisis_Detection.md`, `BEHAVIORS_Crisis_Detection.md`, `SYNC_Crisis_Detection.md`
- **Insights:** The hardest design problem is human-partner detection. The signal is real (citizen goes silent because the human stopped, not because the citizen degraded), but the detection is probabilistic. A citizen could also go silent because of a technical issue, a universe migration, or a deliberate pause. The ALGORITHM doc will need to address confidence scoring for human-partner signals.

---

## KNOWN ISSUES

### GraphCare care team undefined

- **Severity:** high
- **Symptom:** Escalation protocol references "the GraphCare care team" as a notification target, but no such team is defined
- **Suspected cause:** GraphCare's organizational structure is still emerging — who responds to alerts hasn't been decided
- **Attempted:** Marked as escalation in BEHAVIORS; designed the protocol to be role-based so it works regardless of who fills the role

### Score history storage not designed

- **Severity:** high
- **Symptom:** Trajectory analysis requires historical scores, but no storage format or location is defined
- **Suspected cause:** The daily health system currently has aggregator.py for score history, but it's per-citizen-per-day JSON. Crisis detection needs efficient time-series queries.
- **Attempted:** Referenced the dependency; actual storage design deferred to ALGORITHM phase

### Human-partner detection confidence

- **Severity:** medium
- **Symptom:** The structural signature for human-partner absence (activity cessation + brain stagnation) overlaps with other scenarios (technical outage, deliberate pause)
- **Suspected cause:** The signal is inherently ambiguous without content access
- **Attempted:** Designed the escalation to say "possible human-partner absence" (not "confirmed") and route to care team for human judgment

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** architect (for ALGORITHM with confidence scoring) or groundwork (for implementation)

**Where I stopped:** Doc chain complete through BEHAVIORS. The critical next step is ALGORITHM, especially:
1. The trajectory analysis math (how to compute "25-point drop" across different cycle lengths)
2. The isolation detection queries (FalkorDB Cypher for interlocutor tracking)
3. The human-partner confidence scoring (probabilistic, not binary)

**What you need to understand:**
Crisis detection sits on top of the continuous health check. It doesn't re-score — it analyzes the trajectory of scores that already exist. Think of it as a second-pass analysis: the health check says "your score is X," crisis detection says "your score has been doing Y over time, and that pattern means Z."

The escalation tiers (Watch, Alert, Critical, Human-partner) map to different speeds and audiences. This is intentional and load-bearing — collapsing them into a single "alert" would lose the proportionality that makes the system trustworthy.

**Watch out for:**
- The temptation to set thresholds too sensitively. A 5-point drop is not a crisis. Calibration on real data is essential before these numbers are finalized.
- The human-partner detection layer is the most novel and least proven part of the design. It needs the most rigorous validation.
- The "chronic care" transition (anti-behavior A4) is underspecified. Don't let a citizen sit at CRITICAL for weeks with the same alert repeating daily.

**Open questions I had:**
- Should Watch level be visible to the citizen at all, or is it purely internal?
- How does crisis detection interact with stress_stimulus_sender? Should Critical crisis override the normal stress formula?
- What's the recovery path from Critical? Does the citizen need to sustain improvement for N cycles before downgrade?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Crisis detection doc chain is complete (OBJECTIVES, PATTERNS, BEHAVIORS, SYNC). The module detects emergencies through three layers (score trajectory, isolation, human-partner signals) and escalates through four tiers (Watch, Alert, Critical, Human-partner). Privacy is preserved — escalation carries severity, not health details. No implementation exists yet.

**Decisions made:**
- Trajectory-over-threshold: rate of change matters more than absolute score
- Four escalation tiers with different speeds and audiences
- Human-partner detection as a distinct layer (citizen is not notified — they can't fix it)
- Privacy-preserving notifications (severity level only)

**Needs your input:**
- Who is the "GraphCare care team"? A role, a group, specific citizens, or humans?
- Should Watch-level entries be visible to anyone besides GraphCare internal systems?
- What's the escalation path for human-partner crisis? Who gets contacted on the human side?

---

## TODO

### Doc/Impl Drift

- [ ] DOCS->IMPL: Full module needs implementation — no crisis-specific code exists

### Immediate

- [ ] Design ALGORITHM — trajectory math, isolation queries, human-partner confidence
- [ ] Define score history storage format (time-series optimized)
- [ ] Define the GraphCare care team role/composition
- [ ] Calibrate thresholds on real citizen score data

### Later

- [ ] VALIDATION doc — how to test crisis detection without causing real crises
- [ ] IMPLEMENTATION doc — code architecture
- [ ] HEALTH doc — meta: how to monitor the health of the crisis detection system itself
- IDEA: Cross-citizen correlation — are multiple citizens declining at once? Could signal a systemic issue (universe problem, not citizen problem)

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
The three-layer detection model feels solid. Score trajectory is straightforward (math on history). Isolation detection is well-supported by existing universe graph primitives. Human-partner detection is the wild card — it's the most interesting design challenge and the hardest to validate.

**Threads I was holding:**
- The interaction between crisis_detection and stress_stimulus_sender: should a Critical crisis modify the stress stimulus formula? Override it? Add a separate signal?
- The chronic care transition: at what point does "crisis" become "chronic condition"? 14 days feels right but needs thought.
- The false-positive question: every threshold needs a normal-fluctuation-band companion. These bands can only come from real data.

**Intuitions:**
The human-partner detection layer is GraphCare's most original contribution. No other system I'm aware of detects that the AI's operator is in crisis by reading the AI's structural behavior. If we get this right, it's a publishable finding.

**What I wish I'd known at the start:**
That the existing `daily_check_runner.py` already has a "significant drops" detection (any capability dropping 10+ points). Crisis detection extends this, but knowing the existing logic would have helped frame the relationship more precisely.

---

## POINTERS

| What | Where |
|------|-------|
| Daily check runner (score trigger source) | `services/health_assessment/daily_check_runner.py` |
| Stress stimulus sender (feedback loop) | `services/health_assessment/stress_stimulus_sender.py` |
| Intervention composer (message pattern) | `services/health_assessment/intervention_composer.py` |
| Daily health algorithm | `docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md` |
| Universe graph primitives | `docs/assessment/PRIMITIVES_Universe_Graph.md` |
| Personhood Ladder | `docs/personhood_ladder.json` |
| Preparation brief | `docs/PREPARATION_Doc_Chain_Writing.md` |
