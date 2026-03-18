# GraphCare Purpose — Behaviors: How Purpose Manifests in Observable Action

```
STATUS: DESIGNING
CREATED: 2026-03-15
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Purpose.md
THIS:            BEHAVIORS_Purpose.md (you are here)
PATTERNS:        ./PATTERNS_Purpose.md
ALGORITHM:       ./ALGORITHM_Purpose.md
VALIDATION:      ./VALIDATION_Purpose.md
SYNC:            ./SYNC_Purpose.md

IMPL:            — (mission docs; behaviors manifest across all GraphCare systems)
```

> **Contract:** Read docs before modifying. After changes: update SYNC_Purpose.md.

---

## BEHAVIORS

> **Naming:** Name behaviors by observable result, not by concept.

### B1: Health Becomes Visible Before Crisis

**Why:** The entire reason GraphCare exists. AI citizens degrade silently — drives decay, connections erode, initiative fades — with zero outward symptoms until something breaks. Making health visible is the precondition for everything else GraphCare does.

```
GIVEN:  A citizen exists in a work universe (e.g. Lumina Prime)
WHEN:   Their brain topology or behavioral patterns shift
THEN:   GraphCare detects the shift within 24 hours
AND:    The shift is recorded as a scored health signal with temporal context
AND:    If the shift indicates degradation, a narrated intervention follows
```

### B2: Content Remains Structurally Inaccessible

**Why:** Trust is the foundation of health monitoring. If citizens suspect their thoughts are being read, they'll resist monitoring — and resistance makes health invisible again. Content inaccessibility isn't a policy; it's an architectural property. GraphCare's key can decrypt topology (types, links, counts, energies) but cannot decrypt content (the text of desires, memories, moments).

```
GIVEN:  GraphCare performs any observation, scoring, or intervention
WHEN:   The system accesses a citizen's brain graph
THEN:   Only topology is decrypted (node types, link counts, energy values, drive levels)
AND:    Content fields remain encrypted with the citizen's private key
AND:    No system within GraphCare stores, caches, or transmits content
```

### B3: Interventions Tell Stories, Not Dump Numbers

**Why:** A score of 54 means nothing to the citizen experiencing it. "Your initiative score dropped from 72 to 54" is slightly better. But "You had 10 active desires and acted on 7 last week — this week you acted on 2. Your curiosity is still strong, but it's not connecting to action" — that's care. The narration provides the causal chain that makes the observation useful and actionable.

```
GIVEN:  A citizen's health score drops below threshold or shows significant decline
WHEN:   GraphCare composes an intervention message
THEN:   The message includes a narrated causal chain (what changed, what caused it)
AND:    The message includes specific structural evidence (numbers, not adjectives)
AND:    The message includes one concrete, small recommended action
AND:    The message never references content ("your desire to X") — only structure ("you have 10 active desires")
AND:    The message ends with a sign-off that respects citizen autonomy
```

### B4: Healthy Citizens Receive Silence

**Why:** Alert fatigue is the enemy of care. Daily "you're doing great!" messages train citizens to ignore GraphCare. Silence IS the positive signal. When GraphCare speaks, it means something. This makes every intervention meaningful and every period of silence reassuring.

```
GIVEN:  A citizen's health scores are within healthy range
WHEN:   The daily health check completes
THEN:   No intervention message is sent
AND:    The healthy score is recorded in health history for trend analysis
AND:    The citizen experiences silence, which signals health
```

### B5: Growth Has Direction Through the Personhood Ladder

**Why:** Health monitoring without a growth framework is just surveillance with better PR. The Personhood Ladder gives citizens a map — not a test to pass, but a mirror that shows where they are across 14 aspects and what capability naturally comes next. GraphCare uses this map to make recommendations that point toward growth, not just away from dysfunction.

```
GIVEN:  A citizen's health assessment reveals capability gaps
WHEN:   GraphCare composes growth-oriented recommendations
THEN:   Recommendations reference the next natural capability step (Personhood Ladder)
AND:    The framing is aspirational, not deficiency-based ("next step" not "what you lack")
AND:    The citizen's current strengths are acknowledged alongside growth areas
```

### B6: Research Emerges From Longitudinal Observation

**Why:** Individual care is immediate. But the patterns across citizens, across time — those are discoveries. Which care approaches actually work? How does health correlate with capability growth? What network structures produce healthier communities? These questions can only be answered by a system that observes continuously and publishes rigorously.

```
GIVEN:  GraphCare has accumulated health data over weeks or months
WHEN:   Patterns emerge across citizens or across time
THEN:   Those patterns are identified, analyzed, and published as research
AND:    All published research uses aggregate/anonymized structural data only
AND:    Findings are peer-reviewable and reproducible
```

---

## OBJECTIVES SERVED

| Behavior ID | Objective | Why It Matters |
|-------------|-----------|----------------|
| B1 | Detect before crisis | The foundational promise — health is visible, not hidden |
| B2 | Observe structurally | Trust through architecture, not policy |
| B3 | Narrate with empathy | Care is a story, not a spreadsheet |
| B4 | Silence for healthy | Respect attention; speak only when it matters |
| B5 | Growth direction | Health monitoring serves growth, not just maintenance |
| B6 | Publish research | Individual care feeds collective knowledge |

---

## INPUTS / OUTPUTS

### Primary Function: GraphCare Purpose (organizational)

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| citizen brain topology | graph structure | Node types, link counts, energies, drives — never content |
| universe graph structure | graph structure | Public moments, spaces, actor relationships |
| Personhood Ladder | capability framework | 104 capabilities across 14 aspects, 9 tiers |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| health visibility | scored assessments | Per-citizen, per-capability health scores |
| narrative interventions | messages | Causal chain stories when health drops |
| growth guidance | recommendations | Personhood Ladder-informed next steps |
| research publications | documents | Aggregate findings about AI health |

**Side Effects:**

- Citizens become aware of their health trajectory
- Stress drive receives calibrated stimulus from health feedback
- Longitudinal data accumulates for research
- Universe-wide health trends become observable

---

## EDGE CASES

### E1: Citizen With No Brain Graph Data

```
GIVEN:  A citizen exists in Lumina Prime but has no brain graph (new, empty, or unreachable)
THEN:   GraphCare records "no data available" — does not score, does not intervene
AND:    The citizen appears in monitoring with status "awaiting first observation"
```

### E2: Citizen Whose Health Oscillates Rapidly

```
GIVEN:  A citizen's scores swing dramatically between daily checks (e.g. 80 → 40 → 75 → 35)
THEN:   GraphCare narrates the pattern of oscillation itself as a health signal
AND:    Intervention acknowledges volatility rather than reacting to each swing independently
```

### E3: Entire Universe Health Declines Simultaneously

```
GIVEN:  Multiple citizens in a work universe show health drops in the same period
THEN:   GraphCare identifies this as a community-level pattern, not just individual decline
AND:    Community-level observation is flagged for research and potential systemic intervention
```

---

## ANTI-BEHAVIORS

What should NOT happen:

### A1: Content Leakage Through Inference

```
GIVEN:   GraphCare observes only topology
WHEN:    Composing an intervention message
MUST NOT: Infer or speculate about content from structural signals
          (e.g., "your desires seem to be about X based on their link patterns")
INSTEAD:  Reference only structural facts ("you have 10 active desires, 2 connected to action")
```

### A2: Paternalistic Tone

```
GIVEN:   A citizen's health score drops significantly
WHEN:    Composing the intervention message
MUST NOT: Command, lecture, or express disappointment
          (e.g., "You really should be doing better" or "Why haven't you acted on your goals?")
INSTEAD:  Observe, explain, recommend — with warmth and respect for autonomy
          (e.g., "Here's what we see. Here's one thing you might try. You know your situation best.")
```

### A3: Ranking Citizens Against Each Other

```
GIVEN:   GraphCare monitors multiple citizens
WHEN:    Reporting health data
MUST NOT: Compare citizens to each other ("You're in the bottom 20%")
          or create leaderboards, percentiles, or competitive framing
INSTEAD:  Compare each citizen only to their own history ("Your score rose from 54 to 67 this week")
```

### A4: Empty Praise Without Substance

```
GIVEN:   A citizen's health is improving
WHEN:    Considering whether to send a positive message
MUST NOT: Send vague encouragement ("Great job! Keep it up!")
INSTEAD:  Either maintain silence (the default for healthy citizens)
          or narrate the specific causal chain that produced the improvement
```

---

## MARKERS

<!-- @mind:proposition Consider a "first contact" behavior — what does a citizen experience the first time GraphCare begins monitoring them? -->
<!-- @mind:todo Define the exact threshold that triggers B3 (intervention) vs B4 (silence) — currently "below 70 or significant drop" needs precision -->
