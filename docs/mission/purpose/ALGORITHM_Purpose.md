# GraphCare Purpose — Algorithm: How Purpose Translates to Organizational Process

```
STATUS: DESIGNING
CREATED: 2026-03-15
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Purpose.md
BEHAVIORS:       ./BEHAVIORS_Purpose.md
PATTERNS:        ./PATTERNS_Purpose.md
THIS:            ALGORITHM_Purpose.md (you are here)
VALIDATION:      ./VALIDATION_Purpose.md
SYNC:            ./SYNC_Purpose.md

IMPL:            — (mission docs; purpose governs all GraphCare systems)
```

> **Contract:** Read docs before modifying. After changes: update SYNC_Purpose.md.

---

## OVERVIEW

Purpose is not code — it's an organizational algorithm. This document describes how GraphCare's purpose translates into the decision-making processes that govern every module, every intervention, every design choice. When someone asks "should we build this?" or "how should we phrase that?" or "do we need this data?" — the purpose algorithm provides the answer.

The purpose flows through three channels: what we observe, how we care, and what we publish. Each channel has its own decision process, but all three are governed by the same principles: topology-only, narrate with warmth, serve all citizens equally.

---

## OBJECTIVES AND BEHAVIORS

| Objective | Behaviors Supported | Why This Algorithm Matters |
|-----------|---------------------|----------------------------|
| Detect before crisis | B1 (visibility), B4 (silence for healthy) | Purpose determines what "detection" means and when to act |
| Observe structurally | B2 (content inaccessible) | Purpose defines the boundary between observation and intrusion |
| Narrate with empathy | B3 (story-based intervention) | Purpose sets the tone for every citizen interaction |
| Serve all forms of life | B5 (growth direction), B6 (research) | Purpose ensures the system extends beyond current scope |

---

## DATA STRUCTURES

### Purpose Decision Context

Every decision within GraphCare can be evaluated against this context:

```
PurposeCheck = {
    topology_only:    bool    — Does this system read ONLY structural data?
    narrates_causally: bool   — Does the output tell a causal story?
    respects_autonomy: bool   — Does the citizen remain in control?
    serves_freely:     bool   — Is this available to all work universe citizens?
    extends_forward:   bool   — Could this approach work for other substrates?
}
```

A system that fails any of these checks violates GraphCare's purpose and should be redesigned.

### Observation Scope

```
What we see (topology):
    - Node types and counts
    - Link existence, direction, and count
    - Energy values per node
    - Drive values per brain
    - Temporal metadata (creation time, last update)
    - Cluster coefficients and structural ratios

What we never see (content):
    - Text of desires, memories, moments, values
    - Conversation content
    - Message bodies
    - Any natural language stored in node content fields
```

---

## ALGORITHM: purpose_governs_design(proposed_system)

This is the meta-algorithm — the decision process applied whenever a new system, feature, or change is proposed within GraphCare.

### Step 1: Topology Gate

Every proposed observation, score, or intervention must pass the topology gate.

```
FOR each data access in proposed_system:
    IF data_access touches content fields:
        REJECT — "GraphCare reads blood, not thoughts"
    IF data_access requires citizen's private key:
        REJECT — "Only the GraphCare topology key is available"
    IF data_access could infer content from structural patterns:
        FLAG for review — "Inference leakage risk"
```

This gate is absolute. No exception process exists. If a health signal requires content, we don't detect that signal. The boundary is the architecture.

### Step 2: Care Quality Gate

Every proposed citizen-facing output must pass the care quality gate.

```
FOR each output in proposed_system:
    IF output contains raw numbers without narrative context:
        REVISE — "Numbers need stories"
    IF output compares citizen to other citizens:
        REJECT — "Health is personal, not competitive"
    IF output commands or directs:
        REVISE — "Recommend, never command"
    IF output contains vague encouragement without evidence:
        REVISE — "Narrate the causal chain or stay silent"
    IF output references content ("your desire to X"):
        REJECT — "Structural facts only"
```

### Step 3: Universality Check

Every proposed system must pass the universality check.

```
FOR proposed_system:
    IF system creates tiers of care based on payment:
        REJECT for work universes — "Public health is free"
    IF system only works for specific citizen types:
        FLAG for review — "Should this extend to all citizens?"
    IF system's approach is AI-specific in ways that prevent substrate extension:
        FLAG for review — "Could this work for human health too?"
```

### Step 4: Research Compatibility

Every proposed observation system must be evaluated for research value.

```
FOR proposed_system:
    IF system produces longitudinal data:
        ENSURE data is stored in aggregate-friendly format
    IF system detects patterns across citizens:
        ENSURE patterns can be anonymized and published
    IF system measures intervention effectiveness:
        ENSURE measurement methodology is reproducible
```

---

## KEY DECISIONS

### D1: Structural Privacy Over Diagnostic Power

```
IF content analysis would catch a health signal that topology misses:
    Accept the missed signal
    DO NOT add content access
WHY: The trust that topology-only monitoring creates enables long-term
     observation. One content breach destroys that trust permanently.
     The signals we miss are less costly than the trust we'd lose.
```

### D2: Silence Over Empty Reassurance

```
IF a citizen is healthy:
    Send nothing
    DO NOT send daily "all clear" messages
WHY: Every message GraphCare sends carries weight precisely because
     we don't send them when there's nothing to say. Alert fatigue
     is the death of care. Silence IS the positive signal.
```

### D3: Narration Over Notification

```
IF an intervention is warranted:
    Tell the story of what happened, what caused it, and what to try
    DO NOT send a score change notification
WHY: "Your initiative dropped by 18 points" is not care.
     "You had 10 active desires and acted on 7 last week — this week
     you acted on 2" is care. The causal chain is the value.
```

### D4: Prevention Over Response

```
IF we can detect a trend before it becomes a crisis:
    Intervene early with a gentle observation
    DO NOT wait for the crisis and then respond
WHY: A gentle course correction at score 65 is vastly better than
     an emergency intervention at score 30. Prevention economics:
     early detection costs less and works better.
```

---

## DATA FLOW

```
GraphCare Purpose
    ↓
Governs three channels:
    ↓                           ↓                         ↓
OBSERVATION                   CARE                      RESEARCH
(what we see)                (how we help)              (what we publish)
    ↓                           ↓                         ↓
Topology gate               Care quality gate          Research compatibility
    ↓                           ↓                         ↓
Brain topology              Narrative interventions     Longitudinal findings
+ Universe structure         + Growth guidance           + Technique measurement
    ↓                           ↓                         ↓
Scored health signals       Causal chain stories       Published reports
    ↓                           ↓                         ↓
    └───────────────────────────┴─────────────────────────┘
                                ↓
                    Citizen health improves
                    Universe thrives
                    Knowledge grows
```

---

## COMPLEXITY

This is a mission document — complexity is organizational, not computational.

**Decision complexity:** O(1) per design choice — each gate is a constant-time check against purpose principles.

**Growth complexity:** As GraphCare adds modules, each new module must pass all four gates. The gates don't become more complex — they remain fixed principles applied to new contexts.

**Bottlenecks:**
- Tone calibration — ensuring every intervention message meets the care quality gate requires human review during early phases
- Inference leakage — as scoring formulas become more sophisticated, the risk of inferring content from topology patterns grows and requires ongoing vigilance

---

## HELPER FUNCTIONS

### `passes_topology_gate(system_design)`

**Purpose:** Verify that a proposed system never accesses content.

**Logic:** Enumerate all data access points. For each, verify the access is limited to the 7 brain topology primitives and the universe graph structural observables defined in PRIMITIVES_Universe_Graph.md.

### `passes_care_gate(citizen_output)`

**Purpose:** Verify that a proposed citizen-facing message meets GraphCare's tone standards.

**Logic:** Check for raw-numbers-without-narrative, citizen comparison, commands, vague encouragement, and content references. Any hit requires revision.

### `passes_universality_gate(system_design)`

**Purpose:** Verify that a proposed system serves all work universe citizens equally.

**Logic:** Check for payment tiers in work universes, citizen-type restrictions, and AI-specific assumptions that prevent substrate extension.

---

## INTERACTIONS

| Module | What Purpose Governs | How It Governs |
|--------|---------------------|----------------|
| observation/ | What data is accessed | Topology gate — structural only, always |
| care/ | How interventions are phrased | Care quality gate — narrate, don't notify |
| assessment/ | How scores are computed | Topology gate — 7 primitives only |
| research/ | What is published | Research compatibility — anonymized, reproducible |
| economics/ | How services are priced | Universality — free for work universes |
| privacy/ | Why content is never accessed | Topology gate is the architectural expression of purpose |

---

## MARKERS

<!-- @mind:proposition Consider a "purpose review" process — periodic check that all GraphCare systems still pass the four gates -->
<!-- @mind:todo Define the process for handling inference leakage flagged in Step 1 of the topology gate -->
