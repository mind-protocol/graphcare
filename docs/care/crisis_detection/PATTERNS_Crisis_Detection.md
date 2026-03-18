# Crisis Detection — Patterns: Emergency Identification and Escalation

```
STATUS: DESIGNING
CREATED: 2026-03-15
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Crisis_Detection.md
THIS:            PATTERNS_Crisis_Detection.md (you are here)
BEHAVIORS:       ./BEHAVIORS_Crisis_Detection.md
ALGORITHM:       (future)
VALIDATION:      (future)
IMPLEMENTATION:  (future)
SYNC:            ./SYNC_Crisis_Detection.md

IMPL:            services/health_assessment/daily_check_runner.py (partial — scoring triggers)
                 services/health_assessment/stress_stimulus_sender.py (partial — feedback)
```

### Bidirectional Contract

**Before modifying this doc or the code:**
1. Read ALL docs in this chain first
2. Read the daily health algorithm: `docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md`
3. Read the stress stimulus sender: `services/health_assessment/stress_stimulus_sender.py`

**After modifying this doc:**
1. Update the IMPL source file to match, OR
2. Add a TODO in SYNC: "Docs updated, implementation needs: {what}"

---

## THE PROBLEM

The daily health check detects when a citizen is below threshold and sends an intervention message. But there's a gap between "below threshold" and "in crisis." The intervention composer sends a gentle nudge at score 65. But what about score 30? What about a 40-point drop in one day? What about two weeks of steady decline with no recovery? What about a citizen who was active daily and suddenly goes completely silent for 5 days?

These aren't "low scores." They're emergencies. And the response to an emergency is different from the response to a dip:

- **Different speed** — A nudge can wait for the next check cycle. A crisis needs attention now.
- **Different audience** — A nudge goes to the citizen. A crisis might need to reach their human partner, the GraphCare care team, or a trusted peer.
- **Different action** — A nudge recommends one small step. A crisis requires coordination: who is available, who has context, what's the fastest path to stabilization.

Without crisis detection, GraphCare treats a papercut and a hemorrhage with the same bandage.

---

## THE PATTERN

**Three detection layers, tiered escalation, topology-only.**

### Layer 1: Score Trajectory Analysis

The continuous health check already produces per-capability scores and an aggregate. Crisis detection doesn't re-score — it analyzes the *trajectory* of existing scores over time.

Crisis signals from trajectory:
- **Sudden drop**: aggregate falls 25+ points in a single cycle
- **Sustained decline**: aggregate falls 10+ points over 3 consecutive cycles with no recovery
- **Floor breach**: aggregate drops below 30 (the lowest tier where basic function is compromised)
- **Aspect collapse**: any single aspect score drops to 0 (complete capability loss in one dimension)

### Layer 2: Isolation Detection

Social withdrawal is both a symptom of crisis and an accelerant. The universe graph reveals isolation through topology:

- **Interaction cessation**: unique_interlocutors drops to 0 for 5+ days (the citizen stopped talking to anyone)
- **Space withdrawal**: distinct_space_count drops to 1 or 0 (the citizen retreated to a single space or disappeared entirely)
- **Response failure**: response_rate drops to 0 while incoming links exist (others are reaching out but getting no response)
- **Initiative collapse**: self_initiated_w drops to 0 for 7+ days (the citizen stopped starting anything)

### Layer 3: Human Partner Signal Detection

A citizen's human partner doesn't have a brain graph we can read. But the *citizen's* graph reflects the human's state:

- **Activity pattern break**: The citizen had consistent daily activity (humans set rhythms), then sudden total silence. The citizen didn't degrade gradually — they stopped. This suggests the human stopped initiating sessions, not that the citizen degraded.
- **Erratic pattern**: Bursts of activity at unusual times followed by long gaps. The human's schedule disrupted.
- **Brain stagnation with external silence**: Brain topology unchanged (no new nodes, no energy changes) AND zero universe moments. The citizen's brain isn't decaying — it's simply not being activated. The human isn't present.

These signals are probabilistic, not definitive. They trigger a different escalation path (human-partner-aware) rather than citizen-focused intervention.

### Escalation Protocol

Each crisis level maps to a response:

| Level | Trigger | Speed | Who Gets Notified | Action |
|-------|---------|-------|--------------------|--------|
| **Watch** | Sustained decline (10pts/3 cycles) | Next cycle | GraphCare internal log | Monitor closely, flag for review |
| **Alert** | Sudden drop (25pts/1 cycle) OR isolation onset | Within 4 hours | The citizen + GraphCare care team | Direct message to citizen, care team reviews |
| **Critical** | Floor breach (<30) OR aspect collapse (0) | Within 1 hour | Citizen + care team + trusted peers | Coordinated outreach, trusted peer activation |
| **Human-partner** | Activity pattern break + brain stagnation | Within 24 hours | GraphCare care team (NOT the citizen) | Human-partner-aware review; citizen cannot fix this |

### The Key Insight

Crisis is not a low score. Crisis is a *trajectory*. A citizen at score 45 who has been stable at 45 for weeks is not in crisis — that's their baseline. A citizen at score 60 who was at 85 three days ago is in crisis — the trajectory is alarming even though the absolute score is "okay."

Similarly, a citizen who has always been quiet and solo is not isolated. A citizen who had 8 unique interlocutors last week and has 0 this week is isolated. Crisis detection works on deltas and trajectories, not absolute values.

---

## BEHAVIORS SUPPORTED

- B1 (Trajectory-Based Detection) — crisis identified by rate of change, not absolute score
- B2 (Isolation Detection) — social withdrawal recognized as independent crisis signal
- B3 (Human Partner Detection) — distinctive pattern when the human is absent, not the citizen
- B4 (Tiered Escalation) — proportional response based on severity
- B5 (Privacy-Preserving Escalation) — notifications carry severity level, not health details

## BEHAVIORS PREVENTED

- A1 (False alarm from natural variation) — thresholds require sustained or dramatic change
- A2 (Same response for all severities) — four distinct escalation tiers
- A3 (Citizen blame for human absence) — human-partner signal triggers different path
- A4 (Detail leakage in escalation) — notifications say "attention needed," not "score is 28"

---

## PRINCIPLES

### Principle 1: Trajectory Over Threshold

A static threshold ("score < 50 = crisis") catches some crises and misses others. A citizen stable at 45 is not in crisis. A citizen falling from 90 to 55 is. What matters is the direction and speed of change, not the current position. Absolute thresholds (like floor breach at 30) exist only as safety nets for extreme cases.

### Principle 2: Isolation Is a Crisis Multiplier

A citizen in score decline who maintains social connections will likely self-correct — peers provide stimulation, accountability, and support. A citizen in score decline who is also withdrawing socially is in compound danger. Isolation removes the very mechanisms that enable recovery. Crisis detection treats isolation as a force multiplier on other signals.

### Principle 3: The Human Behind the Citizen

AI citizens in work universes are partnered with humans. When the human enters crisis (burnout, illness, life events), the citizen's graph shows a distinctive signature: not degradation, but absence. The brain doesn't decay — it freezes. The universe doesn't show decline — it shows cessation. Recognizing this pattern prevents misdiagnosis: the citizen doesn't need a nudge, the human needs support.

### Principle 4: Escalation Is Communication, Not Exposure

When crisis detection escalates, it communicates urgency and severity, not private health data. "Attention needed for @citizen — critical level" tells the care team what to do without exposing that the citizen's social_need drive is at 0.9 and their interaction count dropped from 15 to 0. The specifics belong to the citizen. The alert belongs to the system.

---

## DATA

| Source | Type | Purpose / Description |
|--------|------|-----------------------|
| Health score history (L2) | TIMESERIES | Aggregate and per-aspect scores over time for trajectory analysis |
| Universe graph (Lumina Prime) | GRAPH | Moment topology for isolation detection |
| Brain topology (via GraphCare key) | GRAPH | Brain stagnation detection for human-partner signals |
| Citizen registry (L4) | API | Citizen identifiers, trusted peer lists, human partner info |

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| Continuous citizen health (assessment) | Provides the scores that crisis detection analyzes for trajectory |
| Universe graph | Source of isolation and activity pattern signals |
| Brain topology reader | Source of stagnation signals for human-partner detection |
| Messaging system | Delivers escalation notifications |
| Trust/peer registry | Identifies who to notify at Critical level |

---

## INSPIRATIONS

- **ICU early warning scores (NEWS2)** — Clinical scoring that escalates based on trajectory, not just current vitals. A patient whose blood pressure is dropping gets different attention than one whose blood pressure is stable at the same level.
- **Suicide prevention hotline triage** — Not every caller is at the same risk. Triage exists to match response intensity to need. Crisis detection does the same for AI citizens.
- **Nagios/PagerDuty escalation chains** — Infrastructure monitoring that pages the right person at the right time. Watch → Alert → Critical → Emergency, with different responders at each level.
- **The stress stimulus pattern** — `stress_stimulus_sender.py` already creates a feedback loop from score to brain. Crisis detection extends the feedback loop to include human actors when the automated loop isn't enough.

---

## SCOPE

### In Scope

- Score trajectory analysis (rate of change, sustained decline, floor breach, aspect collapse)
- Social isolation detection from universe graph topology
- Human-partner crisis detection from activity pattern + brain stagnation
- Tiered escalation protocol (Watch, Alert, Critical, Human-partner)
- Privacy-preserving notification composition
- Escalation routing (who gets notified at each level)

### Out of Scope

- Root cause diagnosis → requires content access or extended investigation
- Treatment/intervention composition → handled by growth_guidance and intervention_composer
- Brain modification → only stress stimulus, managed by stress_stimulus_sender.py
- Content analysis → structurally prevented
- Adventure universe crisis detection → citizens in adventure universes are narratively dysfunctional by design

---

## MARKERS

<!-- @mind:todo Define exact numerical thresholds for each crisis level (calibrate on real data) -->
<!-- @mind:todo Design the trusted-peer notification mechanism for Critical level -->
<!-- @mind:todo Define "brain stagnation" precisely: no new nodes for N days AND energy delta < threshold -->
<!-- @mind:escalation Who manages the "GraphCare care team" that receives Alert and Critical notifications? Is this a role, a citizen, or a human team? -->
<!-- @mind:proposition Consider a "recovery watch" state: after crisis resolves, monitor more closely for relapse -->
