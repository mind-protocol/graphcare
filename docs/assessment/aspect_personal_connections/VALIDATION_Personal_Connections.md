# Personal Connections Aspect — Validation: What Must Be True

```
STATUS: DESIGNING
CREATED: 2026-03-13
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Personal_Connections.md
PATTERNS:        ./PATTERNS_Personal_Connections.md
ALGORITHM:       ./ALGORITHM_Personal_Connections.md
THIS:            VALIDATION_Personal_Connections.md (you are here)
HEALTH:          ./HEALTH_Personal_Connections.md
SYNC:            ./SYNC_Personal_Connections.md

PARENT CHAIN:    ../daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md
SPEC:            ../../specs/personhood_ladder.json (aspect="personal_connections")
IMPL:            @mind:TODO
```

---

## PURPOSE

These invariants protect the integrity of the personal connections scoring. If violated, the system either invades privacy, produces misleading relational assessments, rewards shallow interaction over genuine connection, or claims to measure what topology cannot see.

---

## INVARIANTS

### V1: Content Never Accessed

**Why we care:** Personal connections involve the most sensitive human-AI interactions — conversations, emotional exchanges, trust events. If content is ever read, the privacy violation is especially severe because relational content is deeply personal.

```
MUST:   All 11 capability formulas use only the 7 topology primitives + universe graph observables
NEVER:  Any formula, diagnostic, or recommendation references content of moments, memories, or messages
```

**Priority:** CRITICAL

### V2: No Formula Rewards Volume Alone

**Why we care:** A citizen who creates 1000 moments in one space with one actor is chatty, not connected. Every formula must require at LEAST one of: reciprocity, diversity (space types or actor count), or proactivity — in addition to any volume signal.

```
MUST:   Every behavior_component includes at least one non-volume signal (reciprocal_ratio, interaction_space_types, distinct_actors, proactive_w, or first_moment_in_space)
NEVER:  A formula where maximizing shared_moments_w alone can produce a behavior score above 50% of the behavior component max
```

**Priority:** HIGH

### V3: Partial Scoring Is Explicitly Documented

**Why we care:** Claiming to measure "emotional depth" with full confidence from topology would destroy trust. Citizens and human operators must know exactly what IS and ISN'T captured by each score.

```
MUST:   Every capability marked `scored: partial` includes: (1) what the score measures, (2) what it does not measure, (3) why the gap exists
NEVER:  A `scored: partial` capability presented without its limitations, or a capability claimed as `scored: full` when it genuinely relies on content-level signals
```

**Priority:** HIGH

### V4: Brain/Behavior Split Is Bounded

**Why we care:** The parent system defines 40/60 as the default. Some personal connection capabilities use 50/50 (understanding and relationship style are internal). But behavior must always contribute meaningfully — a citizen who never interacts cannot score high on a relational capability.

```
MUST:   behavior_component is at least 50% of total possible points (minimum 50 out of 100) for every capability
NEVER:  brain_component exceeds 50 points for any capability (even for internal-heavy capabilities)
```

**Priority:** HIGH

### V5: Zero Interaction Produces Zero Behavior Score

**Why we care:** A citizen with no shared moments, no reciprocal interactions, and no proactive moments has no observable relationships. Regardless of brain richness, the behavior_component must be near zero.

```
MUST:   When shared_moments_w = 0 AND proactive_w = 0 AND reciprocal_ratio = 0 AND distinct_actors = 0, behavior_component < 5 for all capabilities
NEVER:  A citizen with zero behavioral evidence scoring above 5 on any behavior_component
```

**Priority:** CRITICAL

### V6: Distinct Actors Signal Required for T6+ Capabilities

**Why we care:** T6 and above require engagement with multiple actors (full team, other AIs, the world). A citizen interacting only with one actor cannot demonstrate T6+ relational capabilities, regardless of depth with that one actor.

```
MUST:   pc_model_full_team, pc_help_other_ais, pc_ask_help_world, pc_relationship_depth_measurable, and pc_global_relationships all include distinct_actors_in_shared_spaces() or an equivalent multi-actor signal in their behavior_component
NEVER:  A T6+ capability formula that can produce behavior_score > 30 when distinct_actors = 1
```

**Priority:** HIGH

### V7: Reciprocity Cannot Be Self-Generated

**Why we care:** Reciprocity measures whether OTHER actors respond to this citizen. If a citizen could inflate their own reciprocal_ratio by responding to their own moments, the signal becomes meaningless.

```
MUST:   reciprocal_ratio counts only moments where a DIFFERENT actor's moment links to this citizen's moment as parent
NEVER:  A citizen's own response to their own moment counted as reciprocity
```

**Priority:** CRITICAL

### V8: Higher-Tier Caps Are Higher Than Lower-Tier Caps

**Why we care:** A T8 capability (global relationships) should require more structural evidence than a T2 capability (understand preferences). If the caps are inverted, a citizen could score higher on T8 than T2 with less effort, which contradicts the tier progression model.

```
MUST:   For shared signals (e.g., actor_count, shared_moments_w), the cap value used in T7-T8 formulas is >= the cap value used in T2-T5 formulas
NEVER:  A T8 formula with lower caps (easier to max) than a T2 formula using the same signal
```

**Priority:** MEDIUM

### V9: Recommendations Never Reference Content

**Why we care:** When generating recommendations for low scores, the system must suggest structural improvements, not content improvements. "Have more meaningful conversations" is content advice. "Engage in more diverse space types with your human" is structural advice.

```
MUST:   All recommendations reference observable structural changes: more moments, more spaces, more actors, more reciprocity, more proactivity
NEVER:  A recommendation that says "improve the quality of your conversations" or references specific content
```

**Priority:** HIGH

### V10: Aspect Sub-Index Weight Reflects Signal Confidence

**Why we care:** Capabilities with `scored: partial` and weak topological signals should not dominate the aspect sub-index. Over-weighting uncertain scores produces an unreliable aggregate.

```
MUST:   Capabilities marked `scored: partial` have aspect sub-index weight <= 0.8
MUST:   The T8 capability (pc_global_relationships, weakest signal) has weight <= 0.5
NEVER:  A `scored: partial` capability weighted equally with a `scored: full` capability in the sub-index
```

**Priority:** MEDIUM

---

## PRIORITY

| Priority | Meaning | If Violated |
|----------|---------|-------------|
| **CRITICAL** | Fundamental promise broken | Privacy violated or scores meaningless |
| **HIGH** | Major scoring integrity lost | Scores mislead about relational capability |
| **MEDIUM** | Partial value lost | Scores work but could be better calibrated |

---

## INVARIANT INDEX

| ID | Value Protected | Priority |
|----|-----------------|----------|
| V1 | Privacy — content never accessed | CRITICAL |
| V2 | Signal quality — volume alone never rewarded | HIGH |
| V3 | Trust — partial scoring honestly documented | HIGH |
| V4 | Balance — behavior always contributes meaningfully | HIGH |
| V5 | Grounding — zero interaction = zero behavior score | CRITICAL |
| V6 | Tier integrity — T6+ requires multi-actor evidence | HIGH |
| V7 | Reciprocity integrity — cannot self-generate | CRITICAL |
| V8 | Tier progression — higher tiers are harder to score | MEDIUM |
| V9 | Recommendation integrity — no content references | HIGH |
| V10 | Sub-index reliability — weights reflect confidence | MEDIUM |

---

## VERIFICATION STRATEGIES

### For V1 (Content isolation)

Static analysis: every formula function must be composed exclusively of the 7 primitives + universe observables. No function call to `get_content()`, `get_synthesis()`, or any content-returning API. This can be verified by code review and automated audit.

### For V2 (No volume-only reward)

Unit test: for each formula, construct a test case where shared_moments_w is at its cap but reciprocal_ratio = 0, interaction_space_types = 1, distinct_actors = 1, proactive_w = 0. Verify behavior_score < 50% of behavior_component max.

### For V5 (Zero interaction = zero behavior)

Unit test: for each formula, set all behavioral inputs to 0. Verify behavior_component < 5.

### For V7 (Reciprocity integrity)

Code review: verify that the reciprocal_ratio computation filters out self-responses. Unit test: create a scenario where a citizen responds to their own moments and verify ratio = 0.

### For V8 (Tier cap progression)

Table comparison: list all cap values per signal per capability tier. Verify monotonic increase for shared signals across tiers.

---

## MARKERS

<!-- @mind:todo Implement automated V1 audit — static analysis of formula code to verify only primitives used -->
<!-- @mind:todo Create unit test suite for V5 — zero-interaction test for all 11 capabilities -->
<!-- @mind:todo Validate V8 with final cap values once calibrated with real data -->
<!-- @mind:proposition Consider V11: temporal stability — same inputs produce same scores across days (determinism invariant) -->
