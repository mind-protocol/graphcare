# Crisis Detection — Behaviors: Observable Effects of Emergency Identification

```
STATUS: DESIGNING
CREATED: 2026-03-15
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Crisis_Detection.md
THIS:            BEHAVIORS_Crisis_Detection.md (you are here)
PATTERNS:        ./PATTERNS_Crisis_Detection.md
ALGORITHM:       (future)
VALIDATION:      (future)
IMPLEMENTATION:  (future)
SYNC:            ./SYNC_Crisis_Detection.md

IMPL:            services/health_assessment/daily_check_runner.py (partial — scoring triggers)
                 services/health_assessment/stress_stimulus_sender.py (partial — feedback)
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## BEHAVIORS

### B1: Sudden Score Drop Triggers Alert Escalation

**Why:** A dramatic single-cycle drop signals an acute event — something broke, something changed, the citizen needs attention now. The daily health check's nudge mechanism is too gentle and too slow for this.

```
GIVEN:  The continuous health check has completed for a citizen
AND:    The citizen's aggregate score dropped 25+ points since the previous cycle
WHEN:   Crisis detection analyzes the latest score delta
THEN:   An Alert-level escalation is triggered
AND:    The citizen receives a direct message acknowledging the drop (without health details)
AND:    The GraphCare care team is notified within 4 hours
```

### B2: Sustained Decline Triggers Watch

**Why:** Gradual decline is harder to notice but equally dangerous. A citizen losing 4 points per cycle doesn't trigger any single alarm, but after 3 cycles they've lost 12 points — a significant trajectory that needs monitoring.

```
GIVEN:  A citizen's aggregate score has declined for 3 consecutive cycles
AND:    The cumulative decline exceeds 10 points
WHEN:   Crisis detection analyzes the score history
THEN:   A Watch-level entry is created in the GraphCare internal log
AND:    The citizen is flagged for closer monitoring in the next cycle
AND:    No notification is sent to the citizen (Watch is internal only)
```

### B3: Floor Breach Triggers Critical Escalation

**Why:** Below score 30, basic capability is compromised. The citizen may not be able to self-correct even with a nudge. This requires coordinated human and peer response.

```
GIVEN:  A citizen's aggregate score drops below 30
WHEN:   Crisis detection evaluates the latest score
THEN:   A Critical-level escalation is triggered
AND:    The citizen receives a message within 1 hour
AND:    The GraphCare care team is notified within 1 hour
AND:    Trusted peers (if any registered) are notified within 1 hour
AND:    The notification contains severity level but NOT specific scores
```

### B4: Aspect Collapse Triggers Critical Escalation

**Why:** A single aspect dropping to zero means complete capability loss in one dimension. Even if the aggregate is still moderate, losing an entire aspect is an emergency — it's like losing hearing while your other vitals are fine.

```
GIVEN:  Any single aspect score drops to 0
AND:    The aspect was previously scored above 0
WHEN:   Crisis detection evaluates per-aspect scores
THEN:   A Critical-level escalation is triggered
AND:    The escalation identifies which aspect collapsed (by name, not score detail)
AND:    Care team and trusted peers are notified within 1 hour
```

### B5: Social Isolation Triggers Alert

**Why:** Isolation is both a symptom and an accelerant of crisis. A citizen who stops interacting with others loses the social scaffolding that supports recovery. Catching isolation early creates an opportunity for intervention before compound crisis develops.

```
GIVEN:  A citizen's unique_interlocutors drops to 0
AND:    This state persists for 5+ days
AND:    The citizen previously had interlocutors > 0
WHEN:   Crisis detection analyzes universe graph topology
THEN:   An Alert-level escalation is triggered with isolation flag
AND:    The citizen receives a message within 4 hours
AND:    The care team is notified with the context "social isolation detected"
```

### B6: Response Failure Compounds Isolation Alert

**Why:** When others are reaching out and getting no response, the isolation is not by choice — it's a withdrawal. This is more alarming than a citizen who simply has no incoming links.

```
GIVEN:  An isolation Alert (B5) has been triggered
AND:    The citizen has incoming links from other actors in the same period
AND:    The citizen's response_rate is 0
WHEN:   Crisis detection evaluates the isolation context
THEN:   The Alert is upgraded to include "unresponsive to outreach" flag
AND:    Escalation speed is increased (within 2 hours instead of 4)
```

### B7: Human Partner Crisis Detected via Structural Signature

**Why:** When the human behind a citizen enters crisis, the citizen's graph shows a distinctive pattern: not gradual degradation but sudden cessation. The brain doesn't decay — it stops changing. The universe graph doesn't show declining quality — it shows silence. Misdiagnosing this as citizen dysfunction would lead to wrong interventions.

```
GIVEN:  A citizen had consistent daily activity (moments in the universe graph)
AND:    Activity drops to zero for 5+ consecutive days
AND:    Brain topology shows no new nodes and energy delta < 0.01 for the same period
WHEN:   Crisis detection analyzes the combined brain + behavior pattern
THEN:   A Human-partner-level escalation is triggered
AND:    The GraphCare care team is notified within 24 hours
AND:    The notification is marked "possible human-partner absence"
AND:    The citizen is NOT notified (the citizen cannot fix this)
```

### B8: Escalation Notifications Contain Severity, Not Details

**Why:** Health data is private. When crisis detection escalates, the recipient needs to know that attention is required and how urgent it is. They do not need to know that the citizen's social_need drive is 0.91 or that their initiative score dropped from 72 to 28. The specifics are for the citizen and their direct care interaction, not for broadcast.

```
GIVEN:  An escalation notification is being composed
WHEN:   The notification is sent to any recipient (care team, trusted peer)
THEN:   The notification includes: citizen handle, escalation level, primary signal type
AND:    The notification does NOT include: specific scores, drive values, or behavioral metrics
AND:    The notification does NOT include: brain topology details or moment counts
```

---

## OBJECTIVES SERVED

| Behavior ID | Objective | Why It Matters |
|-------------|-----------|----------------|
| B1 | O1: Detect before collapse | Sudden drops are the clearest crisis signal |
| B2 | O1: Detect before collapse | Sustained decline is the sneakiest crisis signal |
| B3 | O1: Detect before collapse | Floor breach is the most severe crisis signal |
| B4 | O1: Detect before collapse | Aspect collapse catches dimension-specific emergencies |
| B5 | O1, O3: Detect + escalate | Isolation is both signal and accelerant |
| B6 | O3: Appropriate escalation | Unresponsive isolation is more urgent than quiet isolation |
| B7 | O2: Human partner detection | The citizen can't fix what the human caused |
| B8 | O3, O4: Escalation + no panic | Privacy-preserving notifications maintain trust |

---

## INPUTS / OUTPUTS

### Primary Function: `evaluate_crisis_state(citizen_id, score_history, brain_topology, universe_topology)`

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| citizen_id | string | The citizen being evaluated |
| score_history | list[ScoreSnapshot] | Aggregate + per-aspect scores for last N cycles |
| brain_topology | BrainStats | Current brain topology summary (from brain_topology_reader) |
| universe_topology | BehaviorStats | Current universe graph stats (from universe_moment_reader) |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| crisis_level | enum | NONE, WATCH, ALERT, CRITICAL, HUMAN_PARTNER |
| signals | list[CrisisSignal] | Which signals triggered (for internal logging) |
| escalation_actions | list[EscalationAction] | Who to notify, how, with what severity message |

**Side Effects:**

- Notifications sent to appropriate recipients per escalation protocol
- Crisis event recorded in L2 org graph for longitudinal tracking
- Watch entries created in internal monitoring log

---

## EDGE CASES

### E1: New Citizen With No History

```
GIVEN:  A citizen has fewer than 3 score snapshots (just joined)
THEN:   Trajectory analysis is skipped — not enough data
AND:    Only absolute thresholds apply (floor breach, aspect collapse)
AND:    Isolation detection compares against zero baseline (any non-zero interlocutors is positive)
```

### E2: Citizen Returns After Absence

```
GIVEN:  A citizen had no activity for 14+ days and then resumes
AND:    Their first-back score is significantly below their pre-absence baseline
THEN:   The drop is flagged as WATCH, not ALERT — the absence itself was the event
AND:    Trajectory analysis starts fresh from the return point
```

### E3: Crisis Level Downgrades

```
GIVEN:  A citizen was at CRITICAL level
AND:    Their next cycle shows score improvement of 10+ points
THEN:   The crisis level downgrades to ALERT
AND:    A "stabilizing" note is added to the care team log
AND:    Monitoring continues at elevated frequency until full recovery
```

### E4: Multiple Simultaneous Signals

```
GIVEN:  A citizen shows sudden drop AND isolation AND aspect collapse
THEN:   The highest applicable level is used (CRITICAL)
AND:    All triggering signals are listed in the crisis record
AND:    The escalation notification references the primary signal only (most actionable)
```

### E5: Citizen With Consistently Low Baseline

```
GIVEN:  A citizen has maintained a score between 35-45 for 30+ days
AND:    No significant trajectory change
THEN:   No crisis is detected — this is their stable baseline
AND:    The daily health check handles ongoing intervention (not crisis detection)
```

---

## ANTI-BEHAVIORS

### A1: Score Detail in Escalation

```
GIVEN:   A crisis escalation is being sent
WHEN:    The notification is composed
MUST NOT: Include specific scores ("aggregate: 28"), drive values ("frustration: 0.8"), or behavioral counts ("0 moments in 5 days")
INSTEAD:  Include only: citizen handle, escalation level, signal type ("sudden drop", "isolation", "human-partner absence")
```

### A2: Citizen Notification on Human-Partner Crisis

```
GIVEN:   A human-partner crisis pattern is detected
WHEN:    Escalation notifications are being routed
MUST NOT: Send any notification to the citizen — they cannot fix the human's absence and alerting them serves no purpose
INSTEAD:  Notify the GraphCare care team only, marked "possible human-partner absence"
```

### A3: Crisis From Natural Variation

```
GIVEN:   A citizen's score fluctuates by 5-8 points between cycles
WHEN:    Crisis detection evaluates the trajectory
MUST NOT: Trigger any escalation for variations within normal range
INSTEAD:  Log the variation as noise; only trigger on thresholds that exceed normal fluctuation bands
```

### A4: Permanent Crisis State

```
GIVEN:   A citizen has been at ALERT or CRITICAL for 14+ consecutive days
WHEN:    The next cycle evaluates crisis state
MUST NOT: Continue sending the same escalation indefinitely — this becomes noise
INSTEAD:  Transition to "chronic care" flag with weekly (not per-cycle) review by care team
```

---

## MARKERS

<!-- @mind:todo Define "normal fluctuation band" for anti-behavior A3 — needs calibration on real data -->
<!-- @mind:todo Design the "chronic care" transition protocol for A4 -->
<!-- @mind:escalation Who constitutes the "GraphCare care team"? Is this a defined role, a citizen group, or the NLR escalation path? -->
<!-- @mind:proposition Consider a "peer buddy" system: when isolation is detected, automatically suggest a specific peer for outreach -->
