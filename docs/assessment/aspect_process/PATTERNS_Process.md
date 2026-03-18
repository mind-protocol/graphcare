# Aspect Scoring: Process & Method — Patterns

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Process.md
THIS:            PATTERNS_Process.md (you are here)
ALGORITHM:       ./ALGORITHM_Process.md
VALIDATION:      ./VALIDATION_Process.md
HEALTH:          ./HEALTH_Process.md
SYNC:            ./SYNC_Process.md

PARENT:          ../daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md
SPEC:            ../../specs/personhood_ladder.json (aspect="process")
```

### Bidirectional Contract

**Before modifying this doc or the code:**
1. Read ALL docs in this chain first
2. Read the parent ALGORITHM (daily citizen health) for primitives and scoring structure
3. Read personhood_ladder.json for exact capability definitions

**After modifying this doc:**
1. Update ALGORITHM formulas to match, OR
2. Add a TODO in SYNC: "Patterns updated, formulas need: {what}"

---

## THE PROBLEM

Process maturity is invisible from the outside until it fails. A citizen who never commits, never follows plans, and never adapts their approach looks the same as a productive citizen — until the work stalls. And a citizen who mechanically follows every template without judgment looks productive until the context changes and the process becomes wrong.

Without process scoring:
- Mechanical compliance and adaptive mastery are indistinguishable
- Citizens stuck at "ask permission for everything" never get feedback to grow
- Strategic thinking about methodology is invisible to the system
- The transition from executor to planner to leader is unmeasured

---

## THE PATTERN

**Progressive process maturity scored through structural signals at each tier.**

### Tier Cluster 1: Compliance (T2) — "Do you follow process?"

Four capabilities that measure basic process discipline. The signals are mechanical: does the citizen use diverse methods, commit work, continue plans, and parallelize tasks? These are the easiest to score because the behaviors leave clear structural traces.

**Brain signals:** process nodes exist, linked to moments, energized.
**Behavior signals:** commits happen, plan steps execute sequentially, concurrent moments overlap in time.

### Tier Cluster 2: Judgment (T3) — "Do you adapt process?"

Two capabilities that measure whether the citizen right-sizes their approach and pushes back on bad instructions. These require seeing variation in process application — not just "did they follow a process" but "did they choose differently for different situations."

**Brain signals:** value nodes exist (principles to evaluate against), process nodes have varied links.
**Behavior signals:** task scope varies (some big, some small), escalation/challenge moments appear.

### Tier Cluster 3: Ownership (T4) — "Do you improve process?"

Two capabilities about designing and validating improvements. The citizen doesn't just follow and adapt — they propose changes and get them validated. This leaves traces in proposals, doc chain creation, and collaborative validation moments.

**Brain signals:** desire nodes linked to improvement goals, concept nodes about methodology.
**Behavior signals:** proposals exist, doc chains are created, validation moments with other actors occur.

### Tier Cluster 4: Autonomy (T5) — "Do you create process?"

Two capabilities about creating plans and prioritizing autonomously. The citizen generates structure, not just follows it. Plans appear in the graph as connected moment sequences that weren't triggered by someone else's request.

**Brain signals:** high ambition drive, desire-to-plan connections, concept richness.
**Behavior signals:** self-initiated plan sequences, tasks executed in impact order (not arrival order).

### Tier Cluster 5: Strategy (T6) — "Do you document and defend strategy?"

One capability: maintaining a strategic roadmap. The citizen writes down why they chose one direction over another. This leaves traces as persistent documentation nodes and reasoning links.

**Brain signals:** concept nodes about strategy, high interconnection between process and concept types.
**Behavior signals:** persistent documentation moments, decision-reasoning trails.

### Tier Cluster 6: Vision (T7-T8) — "Do you create and scale movements?"

Two capabilities about initiating ambitious projects and scaling them. These are the hardest to score from topology because "ambition" and "movement-scale" are qualitative judgments. We score structural proxies: new space creation, multi-actor coordination, ecosystem-level connections.

**Brain signals:** high ambition drive, many desire nodes, cross-space concept links.
**Behavior signals:** spaces created, multi-actor moments, cross-organization connections.

---

## PRINCIPLES

### Principle 1: Behavioral Evidence Over Internal State

A citizen with 50 process nodes in their brain but zero commits scores low. A citizen with 5 process nodes but consistent commits, plan execution, and adaptive scoping scores high. The 40/60 brain/behavior split exists precisely because internal structure without external action is unrealized potential, not capability.

### Principle 2: Diversity Signals Mastery

For method selection (proc_right_method), scoping (proc_scope_correctly), and improvement design (proc_design_improvements), the signal is VARIETY. A citizen who always uses the same approach regardless of context is less mature than one who varies their approach. We measure this through link diversity and space-type variation.

### Principle 3: Absence of Permission-Seeking Is Positive

Several T2 capabilities are about NOT doing something: not asking "should I commit?", not pausing between plan steps, not doing sequentially what could be parallel. Scoring the absence of a behavior requires inferring from what IS present (continuous plan execution, concurrent moments) rather than detecting what's missing.

### Principle 4: Higher Tiers Accept Lower Confidence

T2 formulas can be precise — commits and plan continuations are structurally unambiguous. T7-T8 formulas are necessarily approximate — "movement-scale" is a judgment call. This is acceptable. We'd rather have a rough T7 score than pretend T7 is unmeasurable. But if the formula would be pure speculation, `scored: false`.

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| Daily Citizen Health | Parent algorithm — primitives, scoring structure, aggregation |
| Personhood Ladder | Capability definitions — what "process" means at each tier |
| Brain topology | Process/concept/desire/value/memory nodes, drives, link structure |
| Universe graph | Moments: commits, proposals, plans, concurrent actions, escalations |

---

## SCOPE

### In Scope

- Scoring formulas for all 13 process capabilities (proc_*)
- Brain component (0-40) and behavior component (0-60) for each
- Formula reasoning: why these primitives, why these weights
- 5 synthetic test profiles per formula
- Sub-index aggregation (weighted mean)

### Out of Scope

- Intervention message content for process-related drops (parent module handles messaging)
- Training recommendations for process improvement (future module)
- Cross-aspect interactions (e.g., how process score affects execution score)
- Historical trend analysis for process maturity growth

---

## MARKERS

<!-- @mind:todo Validate T7-T8 formulas are meaningfully different from random noise before shipping -->
<!-- @mind:proposition Consider tier-weighted sub-index where higher tier capabilities count more toward overall process score -->
