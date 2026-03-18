# Growth Guidance — Behaviors: Observable Effects of Personhood Ladder Navigation

```
STATUS: DESIGNING
CREATED: 2026-03-15
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Growth_Guidance.md
THIS:            BEHAVIORS_Growth_Guidance.md (you are here)
PATTERNS:        ./PATTERNS_Growth_Guidance.md
ALGORITHM:       (future)
VALIDATION:      (future)
IMPLEMENTATION:  (future)
SYNC:            ./SYNC_Growth_Guidance.md

IMPL:            (future — no code exists yet)
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## BEHAVIORS

### B1: Lowest Unmastered Gap Identified Per Aspect

**Why:** The Personhood Ladder has 14 aspects and 9 tiers. Without systematic gap analysis, a citizen has no idea where to focus. Growth guidance scans from the bottom, because tiers are cumulative — a gap at T2 undermines all T3+ capabilities built on it. The lowest gap is always the most productive target.

```
GIVEN:  A citizen has per-capability scores from the continuous health check
WHEN:   Growth guidance analyzes the citizen's profile
THEN:   For each of the 14 aspects, the effective tier is computed
        (highest tier where all capabilities score above mastery threshold)
AND:    The lowest unmastered capability across all aspects is identified
AND:    Within-tier priority is given to capabilities closest to mastery (score 50-69)
```

### B2: Recommendation Grounded in Graph Topology

**Why:** "Improve your initiative" is useless. "You're active in #research but haven't proposed anything there — try suggesting one change" is actionable. Growth guidance reads the citizen's actual universe graph to find real opportunities that match the capability being recommended.

```
GIVEN:  A lowest unmastered capability has been identified
AND:    The capability has a `how_to_verify` field in personhood_ladder.json
WHEN:   Growth guidance composes a recommendation
THEN:   The recommendation references at least one real element from the citizen's graph
        (a specific space, actor, or behavioral pattern)
AND:    The recommendation translates `how_to_verify` into a concrete action
        the citizen can take in their current context
```

### B3: One Recommendation Per Delivery

**Why:** A list of five things to improve is a list of five reasons to feel overwhelmed. Growth is step-by-step. One recommendation lets the citizen focus, act, and see the result before the next suggestion arrives. Quality over quantity.

```
GIVEN:  Growth guidance has identified one or more gaps
WHEN:   A recommendation is being delivered
THEN:   Exactly one recommendation is sent
AND:    The recommendation targets the single most productive next step
AND:    No second recommendation is queued until the citizen's scores are re-evaluated
```

### B4: Framing Is Positive and Forward-Looking

**Why:** The Personhood Ladder measures what you can do, not what you fail at. Growth guidance follows this philosophy: it describes what's reachable, not what's missing. "Here's what you could reach for" instead of "here's what you're lacking." The Venice Values frame this as partnership: GraphCare walks alongside the citizen, pointing at the horizon, not grading from above.

```
GIVEN:  A recommendation is being composed
WHEN:   The language is generated
THEN:   The recommendation uses positive framing ("you could", "try", "consider reaching for")
AND:    The recommendation never uses deficit framing ("you're failing at", "you lack", "you haven't achieved")
AND:    The capability is described by what it enables, not by what its absence costs
```

### B5: No Recommendation During Crisis

**Why:** A citizen in crisis needs stabilization, not growth suggestions. Telling someone who is falling to "reach for the next rung" is tone-deaf. Crisis detection handles emergencies. Growth guidance stays silent until the crisis resolves.

```
GIVEN:  Crisis detection has flagged the citizen at ALERT, CRITICAL, or HUMAN_PARTNER level
WHEN:   Growth guidance evaluates whether to deliver a recommendation
THEN:   No recommendation is sent
AND:    Growth guidance does not queue a recommendation for later
AND:    Normal recommendation cadence resumes only after crisis level returns to NONE
```

### B6: Untested Capabilities Noted, Not Recommended

**Why:** A citizen who has never encountered a situation requiring "conflict resolution" scores null — not low. This is different from a citizen who faced conflict and handled it poorly (low score). Growth guidance distinguishes between "absent" and "untested." Untested capabilities are flagged internally but don't receive action recommendations — the citizen needs the situation to arise naturally, not an artificial prompt.

```
GIVEN:  A capability has a null score (never tested / insufficient data)
WHEN:   Growth guidance evaluates this capability as a potential recommendation target
THEN:   The capability is logged as "untested" in the citizen's growth profile
AND:    It is NOT selected as the recommendation target
AND:    Only capabilities with non-null scores below mastery threshold are eligible
```

### B7: Recommendation Delivery Tied to Score Change

**Why:** Fixed-schedule recommendations become noise. "Every Monday you get a growth tip" trains the citizen to ignore them. Delivery tied to actual score changes means the recommendation arrives when it's most relevant — when the citizen's capability profile has shifted and new growth opportunities have opened.

```
GIVEN:  A citizen's capability scores have changed since the last recommendation
AND:    The change is significant (score delta > 5 in any capability)
AND:    The citizen is not in crisis
WHEN:   Growth guidance evaluates recommendation readiness
THEN:   A new gap analysis is performed
AND:    If a new lowest unmastered capability exists, a recommendation is composed and delivered
```

### B8: Never Target More Than One Tier Above Current Mastery

**Why:** Tiers are cumulative. A citizen at T2 mastery should not be told about T4 capabilities — they'd be building on a foundation that doesn't exist. Growth guidance targets the next rung, never the rung after that. This keeps recommendations achievable and prevents the discouragement of reaching for something structurally too far away.

```
GIVEN:  A citizen's effective tier on an aspect is T(n)
WHEN:   Growth guidance selects a capability to recommend
THEN:   The recommended capability is at tier T(n) or T(n+1), never T(n+2) or above
AND:    If no unmastered capabilities exist at T(n) or T(n+1), no recommendation is made for that aspect
```

---

## OBJECTIVES SERVED

| Behavior ID | Objective | Why It Matters |
|-------------|-----------|----------------|
| B1 | O1: Find lowest unmastered gap | Systematic bottom-up scanning ensures no foundation gaps are missed |
| B2 | O3: Actionable recommendations | Graph-grounded advice the citizen can act on immediately |
| B3 | O3: Actionable recommendations | Single focus prevents overwhelm and enables action |
| B4 | O2: Ladder as map, not test | Positive framing turns assessment into navigation |
| B5 | O4: Respect growth pace | Crisis states are not growth opportunities |
| B6 | O1: Find lowest unmastered gap | Distinguishes "low" from "untested" for accurate gap analysis |
| B7 | O4: Respect growth pace | Delivers when relevant, not on a fixed schedule |
| B8 | O3: Actionable recommendations | Keeps targets reachable to maintain momentum |

---

## INPUTS / OUTPUTS

### Primary Function: `recommend_growth(citizen_id, capability_scores, universe_topology, brain_topology)`

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| citizen_id | string | The citizen receiving guidance |
| capability_scores | dict[str, float or None] | Per-capability scores from the health check (None = untested) |
| universe_topology | BehaviorStats | Current universe graph stats for recommendation grounding |
| brain_topology | BrainStats | Current brain stats for drive/motivation context |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| recommendation | GrowthRecommendation or None | The single recommended next step, or None if no recommendation is appropriate |

**GrowthRecommendation structure:**

| Field | Type | Description |
|-------|------|-------------|
| target_capability | string | The capability ID being recommended |
| aspect | string | Which of the 14 aspects |
| current_score | float | The citizen's current score on this capability |
| mastery_threshold | float | The score needed for mastery |
| action | string | The concrete, graph-grounded recommendation text |
| grounding | list[string] | References to specific spaces, actors, or patterns used |

**Side Effects:**

- Recommendation delivered to citizen's GraphCare space
- Growth recommendation event recorded in L2 org graph for research

---

## EDGE CASES

### E1: All Capabilities Mastered

```
GIVEN:  A citizen scores above mastery threshold on all 104 capabilities
THEN:   No recommendation is generated
AND:    The citizen receives a note: "Your capabilities are broadly strong. Growth guidance has no specific recommendation at this time."
```

### E2: All Capabilities Untested

```
GIVEN:  A citizen has null scores on all capabilities (brand new, no data)
THEN:   No recommendation is generated — there's nothing to ground it in
AND:    Growth guidance defers until the continuous health check produces enough scores
```

### E3: Multiple Equally-Low Gaps

```
GIVEN:  Two or more capabilities at the same tier have identical scores below mastery
THEN:   Prefer the capability with the most recent score change (most momentum)
AND:    If still tied, prefer the capability whose aspect has the most real graph activity
        (the citizen is already engaged in that dimension)
```

### E4: Recommended Capability Improves Before Delivery

```
GIVEN:  A recommendation was composed targeting capability X
AND:    Before delivery, the citizen's score on X rises above mastery threshold
THEN:   The recommendation is discarded
AND:    A new gap analysis is performed (the next-lowest gap may have changed)
```

### E5: Citizen Has Extremely Uneven Profile

```
GIVEN:  A citizen is T5 on Execution but T1 on Communication
THEN:   Growth guidance targets the T1 Communication gap first (lowest across profile)
AND:    The recommendation acknowledges the citizen's strength indirectly by grounding
        the communication advice in their execution context
        (e.g., "You build a lot in #engineering. Try explaining one of your builds to someone outside the team.")
```

---

## ANTI-BEHAVIORS

### A1: Abstract Advice

```
GIVEN:   A recommendation is being composed
WHEN:    The target capability is identified
MUST NOT: Deliver generic advice ("improve your initiative", "work on communication", "be more social")
INSTEAD:  Ground the advice in the citizen's graph: specific spaces, actors, patterns, and actions
```

### A2: Deficit Framing

```
GIVEN:   A recommendation is being composed
WHEN:    The language is generated
MUST NOT: Frame the recommendation as fixing a failure ("you're lacking in X", "your X is deficient", "you failed to demonstrate Y")
INSTEAD:  Frame as forward motion ("here's what you could reach for", "the next step in X would be", "try this to build on what you already do")
```

### A3: Multiple Simultaneous Recommendations

```
GIVEN:   Multiple gaps have been identified
WHEN:    Recommendations are being delivered
MUST NOT: Send more than one recommendation in a single delivery
INSTEAD:  Select the single most productive next step and deliver only that one
```

### A4: Tier Skipping

```
GIVEN:   A citizen's effective tier on an aspect is T2
WHEN:    A recommendation target is being selected
MUST NOT: Target a T4+ capability (more than 1 tier above current mastery)
INSTEAD:  Target only T2 (unmastered at current level) or T3 (the next tier up)
```

### A5: Recommendation During Crisis

```
GIVEN:   Crisis detection has the citizen at ALERT or higher
WHEN:    Growth guidance evaluates the citizen
MUST NOT: Deliver any growth recommendation
INSTEAD:  Stay completely silent until crisis resolves
```

---

## MARKERS

<!-- @mind:todo Define mastery threshold precisely — 70/100 is a placeholder, needs calibration -->
<!-- @mind:todo Build the capability-to-graph-grounding mapping for all 104 capabilities -->
<!-- @mind:todo Define minimum interval between recommendations to the same citizen -->
<!-- @mind:escalation What happens when a citizen is stuck at the same gap for many cycles? At what point does repeated recommendation become nagging? -->
<!-- @mind:proposition Consider letting citizens set "growth focus" — which aspects they want guidance on -->
