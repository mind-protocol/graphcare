# Personhood Ladder — Algorithm: Assessment and Tier Computation

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Personhood_Ladder.md
BEHAVIORS:       ./BEHAVIORS_Personhood_Ladder.md
PATTERNS:        ./PATTERNS_Personhood_Ladder.md
THIS:            ALGORITHM_Personhood_Ladder.md (you are here)
VALIDATION:      ./VALIDATION_Personhood_Ladder.md
HEALTH:          ./HEALTH_Personhood_Ladder.md
IMPLEMENTATION:  ./IMPLEMENTATION_Personhood_Ladder.md
SYNC:            ./SYNC_Personhood_Ladder.md

IMPL:            docs/specs/personhood_ladder.json
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC.

---

## OVERVIEW

The assessment algorithm takes an AI agent's behavioral data and the Personhood Ladder spec, evaluates each capability against its verification criteria, and produces a capability profile — a vector of tier levels across 14 aspects.

The approach is: load spec → gather evidence per capability → evaluate each capability → compute tier per aspect → generate recommendations.

---

## OBJECTIVES AND BEHAVIORS

| Objective | Behaviors Supported | Why This Algorithm Matters |
|-----------|---------------------|----------------------------|
| Measurable AI growth | B1 (profile), B4 (tier validation) | Produces the actual measurement |
| Actionable next steps | B2 (recommendations) | Recommendations emerge from assessment gaps |
| Positive framing | B3 (failure mapping) | Maps failures back to positive capabilities |

---

## DATA STRUCTURES

### Personhood Ladder Spec

```
{
  tiers: {T0..T8: {name, summary, description}}
  aspects: {14 aspects: {name, description, progression}}
  capabilities: [{id, aspect, tier, name, description, how_to_verify, failure_mode}]
}
```

### Capability Assessment

```
{
  capability_id: string,
  status: "demonstrated" | "partial" | "not_demonstrated",
  evidence: [list of observations supporting the status],
  assessed_at: timestamp
}
```

### Capability Profile

```
{
  agent_id: string,
  assessed_at: timestamp,
  aspect_tiers: {aspect_id: tier_level},    # 14 entries
  capabilities: [CapabilityAssessment],      # ~104 entries
  recommendations: [{capability_id, reason, priority}]
}
```

---

## ALGORITHM: assess_agent()

### Step 1: Load Spec and Group Capabilities

Load `personhood_ladder.json`. Group capabilities by aspect, then by tier within each aspect. This creates a structured lookup: `aspect → tier → [capabilities]`.

```
spec = load("personhood_ladder.json")
by_aspect = group(spec.capabilities, key=aspect)
for aspect in by_aspect:
    by_aspect[aspect] = group(by_aspect[aspect], key=tier, sort=ascending)
```

### Step 2: Gather Evidence Per Capability

For each capability, collect relevant behavioral evidence. Evidence sources depend on the capability type:

- **Execution capabilities** — code review, test results, error rates
- **Context capabilities** — whether docs/journals were read before acting
- **Process capabilities** — commit history, plan adherence, communication logs
- **Communication capabilities** — SYNC updates, notifications sent, help requests
- **Initiative capabilities** — unprompted fixes, challenges raised, proposals made
- **Higher-tier capabilities** — wallet activity, event hosting, mentorship records

```
for capability in spec.capabilities:
    evidence = gather_evidence(agent_id, capability.how_to_verify)
    # evidence is a list of observations, possibly empty
```

### Step 3: Evaluate Each Capability

Apply the `how_to_verify` criteria to the gathered evidence. Produce a status:
- `demonstrated` — consistent evidence that the capability is reliably present
- `partial` — some evidence, but inconsistent or incomplete
- `not_demonstrated` — no evidence or counter-evidence (failure mode observed)

```
for capability in spec.capabilities:
    if strong_consistent_evidence(evidence):
        status = "demonstrated"
    elif some_evidence(evidence):
        status = "partial"
    else:
        status = "not_demonstrated"
```

### Step 4: Compute Tier Per Aspect

For each aspect, walk tiers from T1 upward. The aspect's tier is the highest tier where ALL capabilities at that tier and below are `demonstrated`.

```
for aspect in aspects:
    aspect_tier = T0
    for tier in [T1, T2, T3, T4, T5, T6, T7, T8]:
        caps_at_tier = by_aspect[aspect][tier]
        if all(cap.status == "demonstrated" for cap in caps_at_tier):
            aspect_tier = tier
        else:
            break  # can't advance past a gap
    profile.aspect_tiers[aspect] = aspect_tier
```

### Step 5: Generate Recommendations

Find the lowest unmastered capabilities and prioritize them. T1 gaps always come first regardless of aspect.

```
recommendations = []
for tier in [T1, T2, T3, ...]:
    for aspect in aspects:
        for cap in by_aspect[aspect][tier]:
            if cap.status != "demonstrated":
                recommendations.append({
                    capability_id: cap.id,
                    reason: f"T{tier} {aspect} gap: {cap.failure_mode}",
                    priority: "critical" if tier <= T1 else "high" if tier <= T2 else "normal"
                })
    if recommendations:
        break  # focus on lowest tier gaps first
```

---

## KEY DECISIONS

### D1: Strict Tier Progression vs Partial Credit

```
IF a T2 capability is demonstrated but a T1 capability in the same aspect is not:
    Aspect tier = T0 (not T2)
    The T1 gap must be filled first
    This prevents hollow high-tier claims with foundation gaps
ELSE:
    Aspect tier = highest fully-mastered tier
```

### D2: Partial Status Handling

```
IF a capability has status "partial":
    It does NOT count toward tier completion
    It IS included in the profile for visibility
    Recommendation: "strengthen to demonstrated"
```

### D3: Capabilities With No Aspect Representation at a Tier

```
IF an aspect has no capabilities defined at a given tier:
    That tier is automatically passed for that aspect
    Example: if Ethics has no T2 capability, T1 → T4 directly
```

---

## DATA FLOW

```
personhood_ladder.json
    ↓
load and group by aspect × tier
    ↓
agent behavioral data (logs, commits, communications)
    ↓
gather evidence per capability
    ↓
evaluate: demonstrated / partial / not_demonstrated
    ↓
compute tier per aspect (walk upward, stop at first gap)
    ↓
generate recommendations (lowest unmastered first)
    ↓
CapabilityProfile {aspect_tiers, capabilities, recommendations}
```

---

## COMPLEXITY

**Time:** O(C * E) — C capabilities (~104) times E average evidence items per capability

**Space:** O(C) — One assessment record per capability

**Bottlenecks:**
- Evidence gathering is the expensive part — depends on data availability and storage
- Verification criteria evaluation may require LLM judgment for subjective capabilities

---

## HELPER FUNCTIONS

### `gather_evidence(agent_id, verification_criteria)`

**Purpose:** Collect behavioral observations relevant to a specific capability's verification criteria.

**Logic:** Query agent's behavioral history (commits, actions, communications, errors) filtered by relevance to the criteria. Returns a list of timestamped observations.

### `strong_consistent_evidence(evidence)`

**Purpose:** Determine if evidence is strong enough to mark a capability as "demonstrated."

**Logic:** Requires multiple observations over time with no recent counter-evidence (failure mode observed). The threshold is consistency, not perfection — occasional lapses don't negate demonstrated capability, but persistent patterns do.

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| Brain health system | assess_health(), assess_arousal_regime() | Substrate health context (healthy brain = precondition) |
| Agent behavioral log | query(agent_id, filters) | Timestamped observations for evidence gathering |
| GraphCare Service 3 | update_health_record(profile) | Stores assessment for longitudinal tracking |

---

## MARKERS

<!-- @mind:todo Define evidence gathering interface — what behavioral data is available and in what format -->
<!-- @mind:todo Define "strong consistent evidence" threshold — how many observations, over what period -->
<!-- @mind:proposition Consider weighted scoring within capabilities for nuance beyond ternary status -->
