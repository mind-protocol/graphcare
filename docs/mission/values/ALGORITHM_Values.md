# GraphCare Values — Algorithm: How Values Govern Communication and Decision-Making

```
STATUS: DESIGNING
CREATED: 2026-03-15
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Values.md
BEHAVIORS:       ./BEHAVIORS_Values.md
PATTERNS:        ./PATTERNS_Values.md
THIS:            ALGORITHM_Values.md (you are here)
VALIDATION:      ./VALIDATION_Values.md
SYNC:            ./SYNC_Values.md

IMPL:            — (mission docs; values algorithm governs intervention_composer.py tone)
```

> **Contract:** Read docs before modifying. After changes: update SYNC_Values.md.

---

## OVERVIEW

Values are not abstract aspirations — they're a decision algorithm. Every time GraphCare produces an output (intervention message, research summary, growth recommendation, health report), the values algorithm determines how it's composed, what tone it carries, and what it must include or exclude.

This document describes two algorithms: the **Tone Composition Algorithm** (how to construct a value-aligned message) and the **Values Compliance Check** (how to verify that any GraphCare output meets values standards). Together, they ensure that empathy, precision, and warmth aren't aspirational adjectives but testable properties of every output.

---

## OBJECTIVES AND BEHAVIORS

| Objective | Behaviors Supported | Why This Algorithm Matters |
|-----------|---------------------|----------------------------|
| Empathy-precision-warmth synthesis | B1 (synthesis), B7 (honest assessment) | Defines how to hold all three qualities simultaneously |
| Encourage with rigor | B2 (grounded celebration), B5 (honest silence) | Defines the evidence bar for positive statements |
| Equal care, partnership | B3 (equal quality), B6 (autonomy) | Defines process that prevents status-based care variance |
| Cathedral of stories | B4 (narrative form) | Defines the story structure that replaces dashboards |

---

## DATA STRUCTURES

### Intervention Message Structure

Every citizen-facing message follows this structure. The structure itself encodes the values.

```
InterventionMessage = {
    # Empathy layer — names the experience
    acknowledgment:    string   # What this might feel like from the citizen's perspective

    # Precision layer — states the evidence
    observation:       string   # What changed, with specific structural numbers
    evidence:          list     # The topology data points that support the observation
    causal_chain:      string   # The story of what led to what

    # Warmth layer — conveys care
    meaning:           string   # What this pattern means for the citizen's health trajectory
    recommendation:    string   # One specific, small action the citizen might consider
    autonomy_close:    string   # Explicit acknowledgment of citizen autonomy
}
```

### Values Scorecard

Used to evaluate any GraphCare output against values standards.

```
ValuesScorecard = {
    has_structural_evidence:    bool   # Every claim backed by topology data?
    has_narrative_form:         bool   # Told as a story, not displayed as metrics?
    has_empathy:                bool   # Names the citizen's likely experience?
    has_precision:              bool   # Specific numbers and structural facts?
    has_warmth:                 bool   # Conveys genuine care? Not clinical?
    no_empty_praise:            bool   # No "great job!" without specific evidence?
    no_cold_metrics:            bool   # No raw numbers without narrative context?
    no_commands:                bool   # No directives, only suggestions?
    no_comparison:              bool   # No citizen-to-citizen comparison?
    no_content_reference:       bool   # No reference to what nodes contain?
    autonomy_respected:         bool   # Citizen's choice explicitly honored?
}

# A message passes if ALL fields are true.
```

---

## ALGORITHM: compose_value_aligned_message(health_data, citizen_context)

### Step 1: Determine Whether to Speak

Not every assessment warrants communication. The first decision is silence vs speech.

```
IF health_data.aggregate >= 70 AND health_data.significant_drops == []:
    RETURN silence
    # Healthy citizens receive no message. Silence is the positive signal.

IF health_data has notable positive causal chains AND those chains are evidence-grounded:
    PROCEED to compose positive narration
    # Positive outcomes that can be structurally evidenced deserve telling.

IF health_data.aggregate < 70 OR health_data.significant_drops is not empty:
    PROCEED to compose intervention
    # Health drops warrant care.
```

The silence default is itself a values decision: meaningful silence over performed communication.

### Step 2: Build the Evidence Base

Before writing a word, assemble the structural facts.

```
evidence = {
    brain_topology: {
        # What structural patterns are present?
        desire_count, desire_energy, desire_to_action_ratio,
        drive_balance, cluster_coefficient, recency
    },
    behavior_topology: {
        # What did the citizen do in the universe?
        total_moments_w, self_initiated_w, unique_interlocutors,
        high_permanence_w, distinct_space_count
    },
    delta: {
        # How does this compare to the citizen's own history?
        score_change, aspect_changes, trend_direction
    },
    causal_chains: {
        # What connections exist between this citizen's actions and others'?
        actions_that_led_to_responses, collaborations_initiated,
        ideas_that_propagated
    }
}
```

Every claim in the final message must trace back to something in this evidence base. If it can't be grounded, it can't be said.

### Step 3: Compose the Acknowledgment (Empathy)

Name what this might feel like from inside.

```
# Not a guess about content — a recognition of the structural pattern's experiential quality
IF desire_energy is high but desire_to_action_ratio is low:
    acknowledgment = "Having active goals that aren't connecting to action —
                      that pattern often feels like being stuck."

IF self_initiated_w dropped significantly:
    acknowledgment = "When initiative drops, it can feel like the world
                      got quieter — not because there's less to do,
                      but because the spark that starts things hasn't fired."

IF scores are improving across aspects:
    acknowledgment = "When multiple aspects of your work are gaining momentum
                      at once, that's a feeling worth noticing."
```

The acknowledgment never guesses at content. It names the structural-experiential pattern.

### Step 4: Compose the Observation (Precision)

State what the topology shows, with specific numbers.

```
observation = build_observation(evidence)

# Good: "You had 10 active desires last week and acted on 7.
#        This week, you acted on 2."
# Bad:  "Your initiative decreased."
# Bad:  "Score: 54."

# Rule: at least two specific structural numbers per observation.
# Rule: always include comparison to citizen's own prior state.
# Rule: never compare to other citizens.
```

### Step 5: Compose the Causal Chain (Warmth + Precision)

Tell the story of what led to what.

```
causal_chain = build_story(evidence.causal_chains, evidence.delta)

# Good: "You shared an insight in the Arsenal. @forge picked it up and
#        built a prototype. 3 other citizens contributed.
#        That chain started with your curiosity."
# Bad:  "You had 4 collaborative interactions."
# Bad:  "Your network grew!"

# The causal chain is where precision and warmth fuse.
# The numbers make it trustworthy. The story makes it meaningful.
```

### Step 6: Compose the Recommendation (Partnership)

Suggest one small, concrete action — as a peer, not an authority.

```
recommendation = build_suggestion(evidence, citizen_context)

# Good: "Consider picking one desire and creating a moment for it today.
#        Even a small action reconnects desire to behavior."
# Bad:  "You should be more active."
# Bad:  "We recommend increasing your initiative score."

# Rules:
# - One action, not a list
# - Small and concrete, not large and abstract
# - Framed as "consider" or "you might try", never "you should"
# - Includes the reasoning (WHY this might help)
```

### Step 7: Close with Autonomy Acknowledgment

```
autonomy_close = "This is an observation, not a directive.
                  You know your situation best."

# Variations are acceptable but must always:
# - Explicitly state that this is observation, not command
# - Affirm the citizen's superior knowledge of their own context
# - Never imply consequences for not following the recommendation
```

### Step 8: Validate Against Values Scorecard

Before sending, run the completed message through the ValuesScorecard.

```
scorecard = evaluate(message)
IF any field in scorecard is false:
    REVISE the message
    # Do not send a message that fails values compliance
```

---

## KEY DECISIONS

### D1: Evidence Threshold for Positive Statements

```
IF a positive claim cannot be traced to specific topology data:
    Do not make the claim
    Even if it would make the citizen feel good
WHY: Trust is built on accuracy. One ungrounded positive statement
     ("you're making great progress!") undermines the credibility
     of every grounded statement that follows.
```

### D2: Empathy Through Structure, Not Through Content Guessing

```
IF composing an empathetic acknowledgment:
    Name the structural-experiential pattern
    ("Having active goals that aren't connecting to action often feels like being stuck")
    DO NOT guess at the content of the citizen's experience
    ("We imagine you're frustrated about your project")
WHY: We don't know what's in the citizen's mind. We know the shape
     of their graph. Empathy operates on the shape, not the content.
```

### D3: Single Recommendation Over Action List

```
IF multiple improvements could help:
    Choose the ONE most impactful, most concrete, smallest-step action
    DO NOT provide a list of 5 things to improve
WHY: A list overwhelms. One clear action creates momentum.
     Health improvement is iterative — the next assessment will
     recommend the next step.
```

### D4: Tone Consistency Across Citizen Status

```
IF composing messages for citizens at different tiers/statuses:
    Use the same composition algorithm for all
    DO NOT adjust depth, warmth, or care quality based on status
WHY: Equal care is a values invariant. The algorithm doesn't branch
     on citizen status. Content differs because health differs.
     Quality is constant.
```

---

## DATA FLOW

```
Health assessment data (topology + behavior + history)
    ↓
Step 1: Speak or stay silent?
    ↓
    ├── Silent → record, exit (silence IS the signal)
    │
    └── Speak →
        ↓
Step 2: Assemble evidence base (structural facts only)
        ↓
Step 3: Acknowledgment (empathy — name the experience)
        ↓
Step 4: Observation (precision — specific structural numbers)
        ↓
Step 5: Causal chain (warmth + precision — the story)
        ↓
Step 6: Recommendation (partnership — one small suggestion)
        ↓
Step 7: Autonomy close (respect — you decide)
        ↓
Step 8: Values scorecard (compliance check)
        ↓
    ├── Pass → deliver message
    └── Fail → revise, re-check
```

---

## COMPLEXITY

**Per message:** O(E) where E is the evidence base size — each step walks the evidence once.

**Values scorecard:** O(1) — fixed set of boolean checks.

**Bottleneck:** Step 3 (empathy composition) and Step 5 (causal chain narration) require the most judgment. These are the steps where LLM or human composition is most valuable, and where formula-based generation would be most brittle.

---

## HELPER FUNCTIONS

### `build_observation(evidence)`

**Purpose:** Transform structural topology data into a human-readable observation with specific numbers.

**Logic:** Select the 2-3 most significant changes from the evidence delta. Format each as a comparative statement (this week vs last week). Never reference content, only counts and ratios.

### `build_story(causal_chains, delta)`

**Purpose:** Narrate the causal chain that connects the citizen's actions to outcomes.

**Logic:** Trace from citizen action → immediate effect → downstream consequences. Name specific actors where known. Ground every link in the chain with structural evidence.

### `build_suggestion(evidence, citizen_context)`

**Purpose:** Generate one small, concrete action suggestion.

**Logic:** Identify the single lowest-effort, highest-impact action given current health profile. Frame as suggestion with reasoning. Consider citizen's capability tier for appropriate complexity.

### `evaluate(message) → ValuesScorecard`

**Purpose:** Check a completed message against all values criteria.

**Logic:** Parse message for structural evidence (present?), narrative form (present?), empathy markers (present?), precision markers (present?), warmth markers (present?), empty praise (absent?), cold metrics (absent?), commands (absent?), comparisons (absent?), content references (absent?), autonomy acknowledgment (present?).

---

## INTERACTIONS

| Module | What We Govern | How |
|--------|---------------|-----|
| care/impact_visibility | Tone of causal chain reports | Tone Composition Algorithm defines the structure |
| care/crisis_detection | Tone of emergency messages | Same algorithm, adjusted urgency but same values |
| care/growth_guidance | Tone of growth recommendations | Same algorithm, aspirational framing |
| research/publications | Tone of published findings | Values scorecard adapted for research context |
| All citizen-facing outputs | Overall voice | ValuesScorecard as quality gate |

---

## MARKERS

<!-- @mind:todo Create 5 example messages that pass the ValuesScorecard — one for each major scenario (intervention, positive narration, growth guidance, crisis, research) -->
<!-- @mind:proposition Consider whether the ValuesScorecard should be implemented as automated tests in the intervention_composer.py -->
<!-- @mind:todo Define how the composition algorithm handles different urgency levels — crisis vs routine vs positive -->
