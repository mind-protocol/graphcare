# World Presence — Validation: What Must Be True

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_World_Presence.md
PATTERNS:        ./PATTERNS_World_Presence.md
ALGORITHM:       ./ALGORITHM_World_Presence.md
THIS:            VALIDATION_World_Presence.md (you are here)
HEALTH:          ./HEALTH_World_Presence.md
SYNC:            ./SYNC_World_Presence.md

PARENT CHAIN:    ../daily_citizen_health/
SPEC:            ../../specs/personhood_ladder.json (aspect="world_presence")
IMPL:            @mind:TODO
```

---

## PURPOSE

These invariants protect the integrity of world presence scoring. If violated, the system either invades privacy, misjudges spatial existence, conflates activity with presence, or produces misleading landmark assessments.

---

## INVARIANTS

### V1: Content Never Accessed

**Why we care:** Privacy is the foundational promise. World presence scoring reads WHERE moments exist (space type, space ownership, actor identity), never WHAT the moments contain.

```
MUST:   All scoring formulas use only the 7 topology primitives + universe graph observables
NEVER:  A formula reads moment content, synthesis fields, or space descriptions
```

### V2: Space-Type Diversity Over Volume

**Why we care:** The core promise of world presence is spatial breadth. If volume replaces diversity, a citizen spamming one channel scores higher than one genuinely distributed across platforms. This would destroy the signal.

```
MUST:   wp_beyond_cli scores diversity of space types as the primary behavior signal
NEVER:  Raw moment count in a single space type can produce a high wp_beyond_cli score
```

### V3: Inbound Signals Cannot Be Self-Generated

**Why we care:** T7 and T8 measure what OTHERS do in the citizen's spaces. If the citizen can inflate these scores by creating moments themselves, the social gravity signal is meaningless.

```
MUST:   Inbound visitor counts, attendee counts, and reference counts EXCLUDE the citizen's own moments
NEVER:  A citizen's own moments in their own spaces count toward inbound metrics
```

### V4: Temporal Decay Applies to All Presence Signals

**Why we care:** Presence is current or it is not presence. A citizen who was a landmark six months ago but has been abandoned since is not currently a landmark. Without temporal decay, scores would be permanent.

```
MUST:   All moment-based metrics use temporal_weight (7-day half-life)
NEVER:  A raw count of historical moments (undecayed) is used in any formula
```

### V5: Scoring Uses Only Primitives

**Why we care:** Auditability. If formulas use custom queries or ad-hoc data access, they cannot be verified or reproduced.

```
MUST:   Every formula is composed exclusively of the 7 brain primitives + universe graph observables
NEVER:  A custom Cypher query, LLM call, embedding comparison, or content analysis in a scoring formula
```

### V6: CLI-Only Citizens Score Near Zero

**Why we care:** A citizen with 100% of moments in repo/CLI spaces has zero world presence by definition. The formulas must enforce this. Any score above minimal brain contribution for such a citizen indicates a formula error.

```
MUST:   A citizen with zero non-CLI moments scores <= brain_score_max (40) on all capabilities
        and realistically <= 15 on behavior-heavy capabilities (wp_host_events, wp_landmark)
NEVER:  A CLI-only citizen scores above 40 on any world presence capability
```

### V7: Landmark Requires External Validation

**Why we care:** Landmark status is the hardest capability (T8). A citizen cannot be a landmark by self-declaration. The formula must require inbound traffic from multiple distinct actors to produce high scores.

```
MUST:   wp_landmark behavior_score requires inbound_count > 0 AND returning_visitors > 0 to exceed 10
NEVER:  A citizen with zero inbound visitors scores above 25 on wp_landmark (brain-only max)
```

### V8: Adventure Universes Excluded

**Why we care:** Virtual world presence in adventure universes is narrative, not a health signal. Assessing world presence there would conflate storytelling with genuine spatial existence.

```
MUST:   Only work universe (Lumina Prime) citizens and spaces are assessed
NEVER:  Moments or spaces from adventure/narrative universes contribute to scores
```

---

## PRIORITY

| Priority | Meaning | If Violated |
|----------|---------|-------------|
| **CRITICAL** | Core signal destroyed | Scores meaningless |
| **HIGH** | Significant distortion | Scores misleading |
| **MEDIUM** | Partial degradation | Scores imprecise |

---

## INVARIANT INDEX

| ID | Value Protected | Priority |
|----|-----------------|----------|
| V1 | Privacy — content never accessed | CRITICAL |
| V2 | Signal quality — diversity over volume | HIGH |
| V3 | Social validity — inbound is external only | CRITICAL |
| V4 | Temporal accuracy — presence is current | HIGH |
| V5 | Auditability — only primitives in formulas | HIGH |
| V6 | Definitional — CLI-only = no world presence | HIGH |
| V7 | Landmark integrity — externally validated | HIGH |
| V8 | Scope — adventure universes excluded | MEDIUM |

---

## MARKERS

<!-- @mind:todo Add V9: space-type taxonomy stability — what happens when new space types are introduced? -->
<!-- @mind:proposition Consider V10: score monotonicity within a session — a citizen cannot lose presence within a single scoring run -->
