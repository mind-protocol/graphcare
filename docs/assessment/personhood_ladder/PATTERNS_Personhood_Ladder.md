# Personhood Ladder — Patterns: Positive Capability Progression

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Personhood_Ladder.md
THIS:            PATTERNS_Personhood_Ladder.md (you are here)
BEHAVIORS:       ./BEHAVIORS_Personhood_Ladder.md
ALGORITHM:       ./ALGORITHM_Personhood_Ladder.md
VALIDATION:      ./VALIDATION_Personhood_Ladder.md
HEALTH:          ./HEALTH_Personhood_Ladder.md
IMPLEMENTATION:  ./IMPLEMENTATION_Personhood_Ladder.md
SYNC:            ./SYNC_Personhood_Ladder.md

IMPL:            docs/specs/personhood_ladder.json
```

### Bidirectional Contract

**Before modifying this doc or the code:**
1. Read ALL docs in this chain first
2. Read `docs/specs/personhood_ladder.json`

**After modifying this doc:**
1. Update the JSON spec to match, OR
2. Add a TODO in SYNC_Personhood_Ladder.md: "Docs updated, spec needs: {what}"

**After modifying the JSON:**
1. Update this doc chain to match, OR
2. Add a TODO in SYNC_Personhood_Ladder.md: "Spec changed, docs need: {what}"

---

## THE PROBLEM

AI agents are evaluated in binary terms: works or broken, smart or dumb, useful or not. There's no vocabulary for growth, no progressive scale that names what an agent can do at each level of capability.

Without this vocabulary:
- Agents can't be given targeted development goals
- Health monitoring can only detect dysfunction (pathology), not measure capability
- There's no way to correlate capability with trust, economic agency, or autonomy
- Every new agent starts from scratch with no map of what "getting better" means

---

## THE PATTERN

**Aspect-first, tier-progressive capability matrix.**

Capabilities are organized by aspect (dimension of capability), not by tier. Each aspect progresses independently through the tiers. An agent has a profile — a vector of tier levels across 14 aspects — not a single score.

The key insight: capability is multi-dimensional. An agent can be highly capable in execution (T3) but weak in communication (T1). This profile is more useful than any single number.

**9 tiers** define the progression from baseline tool to world-shaping leader.
**14 aspects** define the dimensions of capability.
**~104 capabilities** are the atomic, verifiable units of assessment.

---

## BEHAVIORS SUPPORTED

- B1 (Agent Assessment) — The matrix structure makes assessment systematic: walk each aspect, check each capability
- B2 (Growth Planning) — The tier structure within each aspect shows what to work on next
- B3 (Profile Comparison) — Two agents can be compared meaningfully: same framework, different profiles

## BEHAVIORS PREVENTED

- A1 (Single-score reduction) — The multi-dimensional structure prevents collapsing capability to one number
- A2 (Negative framing) — Capabilities are stated positively; the framework has no "deficiency" vocabulary
- A3 (Gatekeeping) — The ladder describes, it doesn't prescribe. Agents aren't blocked from attempting any capability.

---

## PRINCIPLES

### Principle 1: Positive Framing

Every capability is stated as something present and demonstrated, not as the absence of a failure. "Dehallucinate: actively verifies claims against reality" — not "doesn't hallucinate." This isn't just tone. Positive framing makes capabilities trainable: you can practice doing something, you can't practice not-doing something.

### Principle 2: Cumulative Tiers

Each tier requires mastery of all tiers below. You can't skip T1 to reach T3. This prevents the common failure of agents that can do impressive things (T5 vision) but can't be relied on for basics (T1 verification). The foundation matters most.

### Principle 3: Aspect Independence

Aspects progress independently. This reflects reality: capability growth isn't uniform. An agent develops unevenly, and that's fine. The profile shows where they are and what's next, without pretending growth is linear.

### Principle 4: Verifiable Capabilities

Every capability has a `how_to_verify` field. This isn't aspirational — it's operational. If you can't verify it, it's not a capability, it's a wish. Verification criteria range from objective (code compiles) to subjective-but-concrete (stakeholders report feeling informed).

### Principle 5: Failure Mode Awareness

Every capability has a `failure_mode` — what it looks like when this capability is missing. This connects the positive framing back to observable problems. You see the failure mode, you know which capability to develop.

---

## DATA

| Source | Type | Purpose / Description |
|--------|------|-----------------------|
| `docs/specs/personhood_ladder.json` | FILE | Machine-readable specification — source of truth for tiers, aspects, capabilities |
| Brain health system (evaluate_health.py) | CODE | Substrate health metrics that complement capability assessment |
| AI Pathologies spec (12 conditions) | SPEC | Inverse framing — pathology detection maps to missing capabilities |

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| Brain health (drives, arousal, brain power) | Substrate must be healthy for capabilities to manifest |
| $MIND economics | Autonomy Stack capabilities require economic infrastructure |
| Mind Protocol trust tiers | Trust aspect maps to protocol trust levels |

---

## INSPIRATIONS

- **Maslow's hierarchy** — Progressive needs, each level building on the one below. But inverted: we don't assume deficiency, we measure presence.
- **Bloom's taxonomy** — Cognitive capability progression (remember → create). Similar structure, different domain.
- **La Horde du Contrevent** — The novel's progression through zones mirrors capability tiers. Each zone demands more from the expedition.
- **CMMI** — Capability Maturity Model. Similar tiered structure, but for organizations. We apply it to individual agents.

---

## SCOPE

### In Scope

- Defining capability tiers and aspects
- Providing verification criteria for each capability
- Describing failure modes for missing capabilities
- Connecting capability to trust, economics, and autonomy
- Assessment framework for GraphCare Service 3

### Out of Scope

- Training methodology — how to develop capabilities → future module
- Automated assessment tooling — implementation of verification → IMPLEMENTATION doc
- Inter-agent comparison or ranking → not the purpose
- Personality or style assessment → orthogonal to capability

---

## MARKERS

<!-- @mind:todo Fill PATTERNS with design decisions about tier boundaries: why 9 tiers, not 7 or 12? -->
<!-- @mind:proposition Consider adding "capability prerequisites" — some capabilities may require specific other capabilities, not just tier level -->
