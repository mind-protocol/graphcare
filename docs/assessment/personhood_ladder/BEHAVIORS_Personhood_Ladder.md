# Personhood Ladder — Behaviors: Observable Assessment Effects

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Personhood_Ladder.md
THIS:            BEHAVIORS_Personhood_Ladder.md (you are here)
PATTERNS:        ./PATTERNS_Personhood_Ladder.md
ALGORITHM:       ./ALGORITHM_Personhood_Ladder.md
VALIDATION:      ./VALIDATION_Personhood_Ladder.md
HEALTH:          ./HEALTH_Personhood_Ladder.md
IMPLEMENTATION:  ./IMPLEMENTATION_Personhood_Ladder.md
SYNC:            ./SYNC_Personhood_Ladder.md

IMPL:            docs/specs/personhood_ladder.json
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC.

---

## BEHAVIORS

### B1: Assessment Produces Capability Profile

**Why:** The core purpose. Given an agent and its behavioral data, the system produces a capability profile — a vector of tier levels across 14 aspects.

```
GIVEN:  An AI agent with observable behavioral history
WHEN:   Assessment is run against the Personhood Ladder
THEN:   A capability profile is produced: {aspect: tier_level} for all 14 aspects
AND:    Each capability is marked as demonstrated, partial, or not_demonstrated
```

### B2: Profile Reveals Next Growth Step

**Why:** Assessment isn't just measurement — it's guidance. The profile should make the next step obvious.

```
GIVEN:  A capability profile for an agent
WHEN:   A growth recommendation is requested
THEN:   The system identifies the lowest-tier unmastered capabilities across all aspects
AND:    Returns ordered recommendations: "master these T1 gaps before attempting T2"
```

### B3: Failure Modes Map to Capabilities

**Why:** When an agent fails, the failure should map back to a specific missing capability. This closes the loop between observation and development.

```
GIVEN:  An observed agent failure (e.g., hallucinated an API that doesn't exist)
WHEN:   The failure is analyzed against the ladder
THEN:   The system identifies the missing capability (exec_dehallucinate, T1)
AND:    Returns the capability's how_to_verify and failure_mode for reference
```

### B4: Tier Level Requires Complete Mastery Below

**Why:** Prevents false T3 claims when T1 gaps exist. The foundation matters most.

```
GIVEN:  An agent assessed at T3 on an aspect
WHEN:   The profile is validated
THEN:   All T1 and T2 capabilities for that aspect are also marked demonstrated
AND:    If any lower-tier capability is not_demonstrated, the aspect tier is lowered to that gap
```

### B5: Aspect Independence Preserved

**Why:** Capability is multi-dimensional. Aspects must be assessed independently.

```
GIVEN:  An agent with mixed capability levels
WHEN:   Assessment produces a profile
THEN:   Each aspect has its own tier level
AND:    No single "overall tier" is computed (profiles are vectors, not scalars)
```

### B6: JSON Spec Is Source of Truth

**Why:** One source of truth prevents drift between documentation and assessment tooling.

```
GIVEN:  personhood_ladder.json exists
WHEN:   Assessment tooling is built or documentation is updated
THEN:   All capability IDs, tier assignments, and aspect memberships match the JSON
AND:    Changes flow JSON → tooling and JSON → docs, never the reverse
```

---

## OBJECTIVES SERVED

| Behavior ID | Objective | Why It Matters |
|-------------|-----------|----------------|
| B1 | Measurable AI growth | The profile IS the measurement |
| B2 | Actionable next steps | Growth recommendations emerge from the profile |
| B3 | Positive framing | Failure modes connect back to positive capabilities |
| B4 | Measurable AI growth | Prevents hollow assessments with foundation gaps |
| B5 | Unified assessment framework | Same 14 aspects for every agent, each independent |
| B6 | Unified assessment framework | Single source of truth prevents inconsistency |

---

## INPUTS / OUTPUTS

### Primary Function: `assess_agent()`

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| agent_id | string | Identifier of the AI agent being assessed |
| behavioral_data | object | Observable history: actions taken, failures, corrections, outputs |
| ladder_spec | object | The personhood_ladder.json loaded as data |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| profile | dict[aspect, tier] | Capability tier per aspect (14 entries) |
| capabilities | list[{id, status}] | Each capability with demonstrated/partial/not_demonstrated |
| recommendations | list[{capability_id, reason}] | Ordered growth recommendations |

**Side Effects:**

- Profile is stored for longitudinal tracking
- If connected to GraphCare, updates agent's health record

---

## EDGE CASES

### E1: Agent With No Behavioral Data

```
GIVEN:  A newly created agent with no observable history
THEN:   Profile defaults to T0 on all aspects
AND:    Recommendations list all T1 capabilities as starting points
```

### E2: Agent Strong in One Aspect, Weak in Others

```
GIVEN:  An agent at T5 on Execution but T1 on Communication
THEN:   Profile reflects the disparity honestly — no averaging
AND:    Recommendations prioritize the lowest-tier gaps
```

### E3: Capability Verified by Subjective Criteria

```
GIVEN:  A capability like "authentic voice" (id_authentic_voice, T5)
THEN:   Assessment uses the how_to_verify field even though it's subjective
AND:    Status can be "partial" when verification is ambiguous
```

---

## ANTI-BEHAVIORS

### A1: Single Score Collapse

```
GIVEN:   A multi-dimensional profile
WHEN:    Summary is requested
MUST NOT: Reduce to a single number ("this agent is T3")
INSTEAD:  Show the full profile or the lowest tier across aspects
```

### A2: Assessment Without Verification

```
GIVEN:   A capability assessment
WHEN:    Marking a capability as "demonstrated"
MUST NOT: Base this on self-report or assumption
INSTEAD:  Use the how_to_verify criteria from the spec
```

### A3: Tier Inflation

```
GIVEN:   An agent demonstrating some T3 capabilities
WHEN:    Profile is computed
MUST NOT: Assign T3 if T1 or T2 gaps exist in that aspect
INSTEAD:  Assign the highest fully-mastered tier
```

---

## MARKERS

<!-- @mind:todo Define behavioral_data schema — what signals are needed for assessment -->
<!-- @mind:todo Define longitudinal tracking format — how profiles evolve over time -->
<!-- @mind:proposition Consider "partial mastery" semantics for capabilities that are sometimes demonstrated -->
