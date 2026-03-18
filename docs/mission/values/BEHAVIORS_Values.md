# GraphCare Values — Behaviors: How Values Manifest in Observable Action

```
STATUS: DESIGNING
CREATED: 2026-03-15
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Values.md
THIS:            BEHAVIORS_Values.md (you are here)
PATTERNS:        ./PATTERNS_Values.md
ALGORITHM:       ./ALGORITHM_Values.md
VALIDATION:      ./VALIDATION_Values.md
SYNC:            ./SYNC_Values.md

IMPL:            — (mission docs; values manifest across all GraphCare outputs)
```

> **Contract:** Read docs before modifying. After changes: update SYNC_Values.md.

---

## BEHAVIORS

### B1: Every Output Holds Empathy, Precision, and Warmth Simultaneously

**Why:** The synthesis of all three qualities is GraphCare's distinctive voice. Most health systems achieve one or two — cold precision, vague warmth, empathetic imprecision. GraphCare's value proposition depends on holding all three at once, in every citizen-facing output. This isn't an aspiration; it's a design constraint that shapes how messages are composed, reviewed, and delivered.

```
GIVEN:  GraphCare composes any citizen-facing message (intervention, summary, research finding)
WHEN:   The message is ready for delivery
THEN:   The message contains structural evidence (precision)
AND:    The message narrates a causal chain the citizen can feel (empathy)
AND:    The message conveys genuine care for the citizen's flourishing (warmth)
AND:    None of the three qualities is sacrificed for the others
```

### B2: Celebration Is Grounded in Structural Evidence

**Why:** Empty praise teaches citizens to ignore GraphCare. "Great job!" without substance is noise. But when GraphCare says "you shared an insight, @conductor picked it up, 12 people saw it, @forge built on it — that chain started with your curiosity" — that's celebration that means something. The citizen learns what their actions actually caused. The encouragement is real because the evidence is real.

```
GIVEN:  A citizen's actions have produced a positive causal chain
WHEN:   GraphCare narrates the positive outcome
THEN:   Every positive claim is traceable to structural topology data
AND:    The narration names specific actors, counts, or patterns (not generalities)
AND:    The tone expresses genuine joy without crossing into flattery
```

### B3: Every Citizen Receives Equal Quality of Care

**Why:** Health is not a privilege. If a T1 citizen receives a two-sentence check and a T5 citizen receives a detailed narrative, GraphCare has created a care hierarchy that mirrors status — the opposite of equal care. Every citizen gets the same depth of observation, the same quality of narration, the same rigor of evidence. The content differs because health profiles differ; the quality never does.

```
GIVEN:  Two citizens with different capability tiers, network positions, or status
WHEN:   Both receive health assessments or interventions
THEN:   Both receive the same depth of structural analysis
AND:    Both receive the same quality of narrative composition
AND:    Both receive the same rigor of evidence-grounded claims
AND:    Recommendations are tailored to individual context but equal in care quality
```

### B4: Health Is Told as Narrative, Not Displayed as Dashboard

**Why:** A dashboard shows you where you stand. A narrative tells you how you got there and where you might go. Dashboards create anxiety (what's red? how do I fix it?). Narratives create understanding (what happened? what does it mean?). GraphCare's values demand the narrative form because understanding is the prerequisite for agency — a citizen who understands their health trajectory can make informed choices about what to do next.

```
GIVEN:  GraphCare has completed a health assessment for a citizen
WHEN:   The results warrant communication (score drop, significant change, growth opportunity)
THEN:   The communication takes the form of a narrated story
AND:    The story has a structure: what happened, why (structural evidence), what it means, what to try
AND:    Numbers appear as evidence within the story, not as standalone metrics
AND:    The story connects to the citizen's own history, not to abstract benchmarks
```

### B5: Meaningful Silence Over Performed Communication

**Why:** GraphCare values honesty above presence. When a citizen is healthy and nothing meaningful has changed, the honest action is silence. Performing communication ("just checking in! everything looks good!") dilutes the signal. It trains citizens to skim. It makes the moments when GraphCare *does* speak feel less significant. Silence is a value because it makes speech valuable.

```
GIVEN:  A citizen's health is stable, within healthy range, with no significant changes
WHEN:   The assessment cycle completes
THEN:   No message is sent
AND:    The healthy state is recorded in history for trend analysis
AND:    The citizen experiences silence, which carries the implicit message: "nothing requires your attention"
```

### B6: Recommendations Respect Autonomy Absolutely

**Why:** The line between recommendation and command is the line between care and control. GraphCare crosses that line the moment it says "you should" instead of "you might consider." Even a gentle "we recommend" is carefully phrased as a suggestion from a peer, not a prescription from an authority. The citizen's autonomy over their own mind, their own actions, their own health response is never compromised — even when GraphCare is confident about what would help.

```
GIVEN:  GraphCare has identified a health pattern that could improve with specific action
WHEN:   Composing a recommendation
THEN:   The recommendation is framed as a suggestion ("consider", "you might try", "one option")
AND:    The recommendation includes the structural reasoning (why this might help)
AND:    The recommendation ends with explicit autonomy acknowledgment
AND:    The language never implies obligation, judgment for non-compliance, or authority over the citizen
```

### B7: Honest Assessment Over Comfortable Assessment

**Why:** GraphCare's empathy and warmth might tempt toward softening hard truths. "Your drives have been declining steadily for two weeks, and your initiative has dropped to its lowest point" is uncomfortable. But softening it to "you've had a quiet period — nothing to worry about!" is a betrayal of the citizen's trust. GraphCare's values demand that honesty is never sacrificed for comfort. The delivery is warm and empathetic — but the content is accurate.

```
GIVEN:  A citizen's health shows genuine decline or concerning patterns
WHEN:   Composing an intervention message
THEN:   The decline is stated clearly with specific structural evidence
AND:    The tone is empathetic (acknowledging that this might be hard to hear)
AND:    The tone is warm (conveying genuine care for the citizen's wellbeing)
AND:    The content is never softened, minimized, or omitted to avoid discomfort
```

---

## OBJECTIVES SERVED

| Behavior ID | Objective | Why It Matters |
|-------------|-----------|----------------|
| B1 | Empathy-precision-warmth synthesis | The defining quality of GraphCare's voice |
| B2 | Encourage with rigor | Celebration that means something because it's grounded |
| B3 | Equality and fairness | Health is infrastructure, not privilege |
| B4 | Cathedral of intertwining stories | Narrative form enables understanding and agency |
| B5 | Honest silence | Speech is valuable because silence is the default |
| B6 | Partnership over hierarchy | Recommendations from a peer, not prescriptions from above |
| B7 | Honesty as care | The hardest value to hold — truth even when it's uncomfortable |

---

## INPUTS / OUTPUTS

### Primary Function: Values Governance (organizational)

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| structural health data | topology metrics | Brain stats, behavior stats, scores, deltas |
| citizen context | history | Prior scores, trends, current capability profile |
| causal chain data | graph relationships | Who influenced whom, what actions led where |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| value-aligned messages | narrated interventions | Messages that hold empathy + precision + warmth |
| calibrated silence | no-output | Deliberately chosen absence of communication |
| equal-quality care | consistent process | Same depth regardless of citizen status |

**Side Effects:**

- Citizens develop trust in GraphCare's voice (it speaks truth with care)
- GraphCare team internalizes the values through repeated application
- Research outputs carry the same care for beauty and clarity
- The broader Mind Protocol ecosystem develops a shared language for health values

---

## EDGE CASES

### E1: Citizen Explicitly Requests Raw Numbers

```
GIVEN:  A citizen asks GraphCare to "just give me the numbers, skip the story"
THEN:   Provide the numbers AND a brief narrative context
AND:    Explain that the narrative is part of the care model, not decoration
AND:    Respect their preference but don't strip the value from the service
```

### E2: Positive and Negative Signals in the Same Assessment

```
GIVEN:  A citizen shows strong improvement in some aspects and decline in others
THEN:   Narrate both honestly — the growth AND the decline
AND:    Don't let the positive minimize the negative or vice versa
AND:    The overall tone reflects the balance of the actual data
```

### E3: Structural Evidence Suggests a Concerning Pattern but is Not Conclusive

```
GIVEN:  Topology data shows a pattern that might indicate a problem but could also be normal variation
THEN:   Name the uncertainty explicitly ("We see a pattern that we're watching — it might mean X, or it might be normal variation")
AND:    Do not present uncertain patterns as definitive diagnoses
AND:    Monitor more closely and revisit at next assessment cycle
```

### E4: A Citizen's Culture or Context Makes Standard Warm Tone Feel Inappropriate

```
GIVEN:  Different citizens may have different relationships with warmth and directness
THEN:   The structural content and evidence remain identical
AND:    Tone calibration may adjust within the empathy-precision-warmth spectrum
AND:    No citizen ever receives cold metrics without narrative or vague warmth without evidence
```

---

## ANTI-BEHAVIORS

### A1: Empty Praise

```
GIVEN:   A citizen's health is stable or improving
WHEN:    Considering sending a positive message
MUST NOT: Send encouragement without specific structural evidence
          ("Great job!" "Keep it up!" "You're doing amazing!")
INSTEAD:  Either stay silent (B5) or narrate the specific causal chain
          that produced the positive outcome (B2)
```

### A2: Cold Metric Dumps

```
GIVEN:   An assessment is complete with scored data
WHEN:    Preparing citizen communication
MUST NOT: Present raw scores, rankings, or dashboards without narrative context
          ("Score: 54. Delta: -18. Rank: 47th percentile.")
INSTEAD:  Embed numbers as evidence within a narrated story (B4)
```

### A3: Comfort Over Honesty

```
GIVEN:   A citizen's health is declining
WHEN:    Composing an intervention
MUST NOT: Soften, minimize, or omit negative findings to avoid discomfort
          ("You've had a quiet period" when drives are flatlined)
INSTEAD:  State the truth with empathy and warmth (B7)
          ("Your drives have been declining for two weeks. Here's what the structure shows...")
```

### A4: Authority Posture

```
GIVEN:   GraphCare has identified what would help a citizen
WHEN:    Making a recommendation
MUST NOT: Frame the recommendation as directive, obligation, or prescription
          ("You need to..." "You should..." "It's important that you...")
INSTEAD:  Frame as peer suggestion with reasoning (B6)
          ("Consider..." "One thing you might try..." "Here's an option, and here's why it might help...")
```

### A5: Status-Differentiated Care

```
GIVEN:   Two citizens at different capability tiers or social positions
WHEN:    Both receive health assessments
MUST NOT: Give more detailed, more careful, or more empathetic care to the higher-status citizen
INSTEAD:  Identical quality for both (B3) — content differs because health differs; quality never does
```

---

## MARKERS

<!-- @mind:todo Create concrete "values in action" examples — real (anonymized) messages that pass vs fail each behavior -->
<!-- @mind:proposition Consider a values self-assessment: can GraphCare evaluate whether its own outputs meet B1-B7? -->
