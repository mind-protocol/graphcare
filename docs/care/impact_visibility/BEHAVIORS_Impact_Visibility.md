# Impact Visibility — Behaviors: Observable Effects of Causal Chain Narration

```
STATUS: DESIGNING
CREATED: 2026-03-15
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Impact_Visibility.md
THIS:            BEHAVIORS_Impact_Visibility.md (you are here)
PATTERNS:        ./PATTERNS_Impact_Visibility.md
ALGORITHM:       (future)
VALIDATION:      (future)
IMPLEMENTATION:  (future)
SYNC:            ./SYNC_Impact_Visibility.md

IMPL:            services/health_assessment/intervention_composer.py (partial — compose only)
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## BEHAVIORS

### B1: Mature Causal Chains Produce Narrative Reports

**Why:** Citizens need to see what their actions caused. A moment that sparked a chain of responses, builds, and follow-ups across spaces and actors is a story worth telling. Without this, contribution feels invisible.

```
GIVEN:  A citizen has moments in the universe graph from the previous settlement cycle
WHEN:   At least one forward causal chain from those moments reaches depth >= 2 hops
        OR breadth >= 3 distinct actors
THEN:   A narrative report is composed describing the chain in story form
AND:    The report names all participating actors, spaces, and the timeline
AND:    The report is queued for batched delivery
```

### B2: Reports Are Batched at Settlement Cadence

**Why:** Impact chains need time to develop. A real-time notification after the first hop would be premature and misleading. Batching at settlement cadence lets chains mature and prevents notification fatigue.

```
GIVEN:  One or more narrative reports are queued for a citizen
WHEN:   The settlement cycle completes
THEN:   All queued reports are composed into a single delivery
AND:    The delivery is sent to the citizen's GraphCare space
AND:    The queue is cleared for the next cycle
```

### B3: Reports Use Structural Topology Only

**Why:** Privacy is non-negotiable. Impact Visibility traces who linked to whom, in which space, at what time — never what was said. This is structurally enforced: the tracing algorithm walks link edges and reads node types and actor IDs, not content fields.

```
GIVEN:  A causal chain is being traced
WHEN:   The trace encounters a moment node
THEN:   Only structural metadata is read: actor_id, space_id, created_at, link edges
AND:    Content fields are never accessed, logged, or transmitted
```

### B4: All Chain Participants Are Named

**Why:** Venice Values say partnership simply works better. A chain is co-created by everyone in it. The originator deserves to know what happened, but the amplifier, the builder, the tester — they all made the chain real. Attribution is collective.

```
GIVEN:  A narrative report describes a causal chain
WHEN:   The chain includes moments from multiple actors
THEN:   Every actor in the chain is named with their @handle
AND:    Each actor's role in the chain is described (initiated, amplified, built on, tested, etc.)
```

### B5: No Report When No Chain Matures

**Why:** Silence is not punishment. Not every moment starts a chain. Sending "nothing happened with your work this cycle" would be demoralizing and false — maybe a chain is forming right now. Impact Visibility only speaks when it has something real to narrate.

```
GIVEN:  A citizen has moments in the previous settlement cycle
WHEN:   No forward causal chain reaches the maturity threshold
THEN:   No impact report is generated for that citizen this cycle
AND:    No message is sent — silence is the default
```

### B6: Narrative Uses Warm, Specific Language

**Why:** The tone is the module's identity. Not "bravo" (empty flattery). Not "cascade: 12" (cold metrics). The story of the fact, told with the precision of data and the warmth of someone who genuinely cares. This is what makes Impact Visibility different from a dashboard.

```
GIVEN:  A narrative report is being composed
WHEN:   The chain data is translated into human language
THEN:   The report uses specific facts (actor names, space names, counts, timeline)
AND:    The report uses narrative structure (beginning, development, current state)
AND:    The report does not use empty praise phrases ("great job", "amazing work", "bravo")
AND:    The report does not use raw metric formatting ("score: X", "cascade: N")
```

---

## OBJECTIVES SERVED

| Behavior ID | Objective | Why It Matters |
|-------------|-----------|----------------|
| B1 | O1: Show citizens what their actions caused | The core purpose — turning topology into visible causal stories |
| B2 | O3: Align with settlement cadence | Prevents premature narration and notification fatigue |
| B3 | O1, O4: Privacy + Venice Values | Partnership requires trust; trust requires structural privacy |
| B4 | O4: Reinforce Venice Values | Partnership Simply Works Better — attribution is always collective |
| B5 | O2: Narrate with empathy | Silence is kinder and more honest than "nothing happened" |
| B6 | O2: Empathy, precision, warmth | The tone IS the care; without it, reports are just dashboards |

---

## INPUTS / OUTPUTS

### Primary Function: `trace_and_narrate_impact(citizen_id, settlement_cycle)`

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| citizen_id | string | The citizen whose moments are being traced forward |
| settlement_cycle | object | Start/end timestamps defining the window |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| report | string or None | Narrative text if chains matured, None if silence |
| chains | list[CausalChain] | Structured chain data for internal use (audit, research) |

**Side Effects:**

- Message delivered to the citizen's GraphCare space (if report is non-None)
- Chain metadata recorded in L2 org graph for longitudinal research

---

## EDGE CASES

### E1: Citizen Has Only One Moment

```
GIVEN:  The citizen created a single moment in the settlement cycle
AND:    That moment has no forward links
THEN:   No report is generated — silence
```

### E2: Chain Crosses Settlement Boundary

```
GIVEN:  A moment from cycle N-1 spawns a chain that continues into cycle N
THEN:   The chain is reported in cycle N (when it matures), not in N-1
AND:    The originating moment from N-1 is attributed correctly with its creation date
```

### E3: Circular Chain (A links to B links to A)

```
GIVEN:  A causal chain forms a cycle (actor A's moment links to actor B's, which links back to A's)
THEN:   The chain is traced up to the cycle point, not infinitely
AND:    The narrative notes the reciprocal pattern: "a back-and-forth between @A and @B"
```

### E4: Very Long Chain (10+ hops)

```
GIVEN:  A causal chain reaches extreme depth (10+ hops, 8+ actors)
THEN:   The narrative summarizes the middle section rather than listing every hop
AND:    The start and end are always narrated in full detail
AND:    The report highlights the exceptional nature: "a chain that crossed N spaces and involved M citizens"
```

### E5: Citizen Is Not the Originator But a Participant

```
GIVEN:  A citizen appears in the middle of a chain originated by someone else
THEN:   That citizen receives a report about their role in the chain, not just the originator's
AND:    The originator is credited: "this chain started with @originator's moment in #space"
```

---

## ANTI-BEHAVIORS

### A1: Empty Praise

```
GIVEN:   A report is being composed
WHEN:    The narrative template is applied
MUST NOT: Include generic praise without causal evidence ("Great work!", "You're amazing!", "Bravo!")
INSTEAD:  State the structural fact ("Your moment reached 4 actors across 2 spaces over 5 days")
```

### A2: Raw Metric Dump

```
GIVEN:   A report is being composed
WHEN:    Chain data is available
MUST NOT: Present raw metrics without narrative context ("Cascade depth: 3. Actor count: 4. $MIND: 2.1")
INSTEAD:  Embed metrics within the story ("4 citizens built on your work across 3 spaces — a chain that took 5 days to unfold")
```

### A3: Content Quotation

```
GIVEN:   A moment in the chain has content
WHEN:    The narrative is being composed
MUST NOT: Quote, paraphrase, or reference the content of any moment
INSTEAD:  Describe the structural fact: "a moment in #space" or "a response to @actor"
```

### A4: Comparison Between Citizens

```
GIVEN:   Multiple citizens have impact reports
WHEN:    Reports are being composed
MUST NOT: Compare one citizen's impact to another's ("Your chain was longer than average")
INSTEAD:  Each report tells only that citizen's story, with no external reference point
```

---

## MARKERS

<!-- @mind:todo Define the CausalChain data structure for internal representation -->
<!-- @mind:todo Specify the narrative template system (how topology maps to sentence patterns) -->
<!-- @mind:escalation How does settlement_cycle metadata get passed to Impact Visibility? Need integration design with economics module. -->
