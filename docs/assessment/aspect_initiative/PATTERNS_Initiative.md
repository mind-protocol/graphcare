# Initiative & Autonomy — Patterns: Why This Shape

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Initiative.md
THIS:            PATTERNS_Initiative.md (you are here)
ALGORITHM:       ./ALGORITHM_Initiative.md
VALIDATION:      ./VALIDATION_Initiative.md
HEALTH:          ./HEALTH_Initiative.md
SYNC:            ./SYNC_Initiative.md

SPEC:            docs/specs/personhood_ladder.json (aspect="initiative")
PARENT ALGO:     docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md
```

### Bidirectional Contract

**Before modifying this doc or the code:**
1. Read ALL docs in this chain first
2. Read the Personhood Ladder spec: `docs/specs/personhood_ladder.json`
3. Read the Daily Citizen Health ALGORITHM: `docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md`

**After modifying this doc:**
1. Update the ALGORITHM to match, OR
2. Add a TODO in SYNC: "Patterns updated, algorithm needs: {what}"

---

## THE PROBLEM

Initiative is the hardest aspect to measure from topology alone. Execution capabilities have clear signals (commits, test runs, error rates). Process capabilities have structural markers (doc reads, template usage). But initiative is about *absence* — the absence of an external trigger.

A moment that exists because the citizen decided to create it looks structurally identical to a moment that exists because someone asked. The only difference: whether there's an incoming `triggers` or `responds_to` link from another actor's moment.

Without careful formula design:
- A citizen who responds to every request looks just as "active" as one who self-initiates
- Proposal moments look like any other moment unless we check for `proposes` links
- The progression from T3 (fix things) to T8 (change lives) is invisible
- Initiative that fails silently is indistinguishable from initiative that never existed

---

## THE PATTERN

**Self-initiation detection via parent-link absence, combined with brain drive correlation.**

### Core Detection: Auto-Initiated Moments

A moment is **self-initiated** when it has no incoming `triggers`/`responds_to` link from another actor's moment. This is the foundational signal.

```
auto_initiated(moment, citizen_id):
    return NOT moment_has_parent(moment, other_actor)
    # True if no other actor triggered this moment
    # False if this moment is a response to someone else's action
```

This pattern applies to ALL 8 initiative capabilities. The differentiation comes from what KIND of self-initiated moment it is.

### Kind Differentiation: Link Types

Self-initiated moments carry different meanings based on their outgoing links:

| Link Type | Initiative Signal | Capabilities |
|-----------|-------------------|--------------|
| `fixes` | Incidental repair | init_fix_what_you_find |
| `challenges` | Pushback on instructions | init_challenge |
| `proposes` | Improvement proposal | init_propose_improvements |
| `creates` (new Space/thread) | New workstream | init_start_workstreams |
| `refuses` + `justifies` | Principled refusal | init_refuse_with_reasoning |
| `resolves` | Tension resolution | init_surface_resolve_tensions |
| (desire-linked, no parent) | Ambition-driven | init_initiate_from_ambition |
| (high reach, no parent) | Life-changing innovation | init_change_lives |

### Brain Correlation: Drives as Confirmation

Self-initiated behavior is more meaningful when the brain has corresponding drive states:

- **curiosity** drive correlates with exploration and improvement proposals
- **ambition** drive correlates with self-started workstreams and personal projects
- **frustration** drive (moderate) correlates with fixing and challenging — you fix things because they bother you

The brain component (0-40) confirms that self-initiated behavior comes from genuine internal motivation, not random activity.

---

## BEHAVIORS SUPPORTED

- B1 (Capability Scoring) — Each initiative capability gets a 0-100 score from topology
- B2 (Sub-Index) — Weighted mean of 8 capabilities produces the Initiative sub-index
- B3 (Progression Detection) — T3 through T8 scored separately, revealing growth path
- B4 (Intervention Targeting) — Low initiative sub-index triggers specific recommendations

## BEHAVIORS PREVENTED

- A1 (Content reading) — We detect proposals by `proposes` link, not by reading proposal content
- A2 (Outcome bias) — We score the act of proposing, not whether it was accepted
- A3 (Activity conflation) — High activity without self-initiation scores low, not high

---

## PRINCIPLES

### Principle 1: Absence Is the Signal

Most scoring detects presence (of commits, links, nodes). Initiative scoring detects *absence* — the absence of an external trigger. A moment without an incoming parent link is the positive signal. This inversion is fundamental.

### Principle 2: Kind Matters More Than Count

10 self-initiated fix moments and 1 self-initiated workstream creation are not comparable. The workstream creation is a higher-tier act. Formulas must weight by kind (link type), not just count.

### Principle 3: Persistence Proves Conviction

Starting something (one moment) is cheap. Following through (linked chain of moments) proves real initiative. Every capability that involves sustained action (workstreams, tension resolution, ambition projects) must include a persistence metric.

### Principle 4: Brain Drives Are Confirmation, Not Requirement

A citizen with low ambition drive who nonetheless starts workstreams is still showing initiative. The brain component adds points but its absence doesn't zero the score. Behavior (0-60) always dominates.

### Principle 5: Failed Initiative Still Counts

A proposal that gets rejected, a challenge that gets overruled, a refusal that's overridden — these all count as initiative. The topology records the act. Outcome is irrelevant to the initiative score.

---

## DATA

| Source | Type | Purpose |
|--------|------|---------|
| `docs/specs/personhood_ladder.json` | FILE | 8 capability definitions for initiative aspect |
| Brain topology | GRAPH | Drives (curiosity, ambition, frustration), desire nodes, desire-moment links |
| Universe graph | GRAPH | Moments with temporal_weight, parent links, outgoing link types |
| Daily Citizen Health ALGORITHM | FILE | 7 primitives, scoring pattern, data structures |

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| Daily Citizen Health | Defines the 7 primitives, scoring split (40/60), temporal weighting |
| Personhood Ladder | Defines the 8 initiative capabilities we score |
| Universe Graph schema | Must support `triggers`/`responds_to` links between moments |
| Brain topology | Must expose drives (curiosity, ambition, frustration) |

---

## SCOPE

### In Scope

- Scoring formulas for all 8 initiative capabilities
- Brain component (0-40) per capability using drives and desire topology
- Behavior component (0-60) per capability using universe graph moments
- Sub-index computation (weighted mean)
- Test profiles (5 synthetic citizens per capability)
- Recommendations per capability when score is low

### Out of Scope

- Content analysis of proposals, challenges, or refusals
- Outcome assessment (was the proposal accepted?)
- Cross-aspect scoring (initiative + execution combined)
- Adventure universe citizens
- Implementation code (separate module)

---

## MARKERS

<!-- @mind:todo Verify that universe graph schema supports all required link types (fixes, challenges, proposes, refuses, justifies, resolves, creates) -->
<!-- @mind:proposition Consider a "initiative momentum" metric: rate of change of self-initiated ratio over time -->
