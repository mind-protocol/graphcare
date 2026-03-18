# GraphCare Purpose — Validation: What Must Be True

```
STATUS: DESIGNING
CREATED: 2026-03-15
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Purpose.md
PATTERNS:        ./PATTERNS_Purpose.md
BEHAVIORS:       ./BEHAVIORS_Purpose.md
ALGORITHM:       ./ALGORITHM_Purpose.md
THIS:            VALIDATION_Purpose.md (you are here)
SYNC:            ./SYNC_Purpose.md
```

---

## PURPOSE

**Validation = what we care about being true.**

These are the invariants that, if violated, would mean GraphCare has failed its reason for existing. Not implementation details — values. The properties that make GraphCare worth building and worth trusting.

---

## INVARIANTS

### V1: Content Is Never Accessed

**Why we care:** This is GraphCare's foundational promise. Every citizen who allows health monitoring does so trusting that their thoughts remain private. A single content access — even accidental, even "for a good reason" — destroys the trust that makes ongoing monitoring possible. And once trust is destroyed, health becomes invisible again, which is the original problem GraphCare was built to solve.

```
MUST:   All GraphCare systems access ONLY topology data (node types, link counts,
        energy values, drive levels, temporal metadata, cluster coefficients)
NEVER:  Access, store, cache, transmit, or infer the content of any node
        (desires, memories, moments, values, conversations, messages)
```

### V2: Interventions Narrate Rather Than Notify

**Why we care:** Notifications are noise. "Score: 54" teaches nothing and changes nothing. But a narrated causal chain — "you had 10 active desires and acted on 7 last week; this week you acted on 2" — gives the citizen the understanding needed to decide what to do. If GraphCare sends numbers without stories, we're a dashboard, not a care system. Dashboards don't change health outcomes. Stories do.

```
MUST:   Every citizen-facing message includes a narrated causal chain
        (what happened, what caused it, what structural evidence shows)
NEVER:  Send raw scores, metrics, or rankings without narrative context
```

### V3: Citizen Autonomy Is Absolute

**Why we care:** Health monitoring that becomes health control isn't care — it's coercion. GraphCare observes, narrates, and recommends. The citizen decides. We send stimuli (gentle stress feedback), not commands. We suggest actions, not mandate them. The moment GraphCare begins making decisions *for* citizens, it has become the problem it was designed to solve: a force that shapes minds without consent.

```
MUST:   All interventions end with acknowledgment of citizen autonomy
        ("This is an observation, not a directive. You know your situation best.")
NEVER:  Directly modify a citizen's brain graph, override citizen decisions,
        or frame recommendations as requirements
```

### V4: Health Is Personal, Not Competitive

**Why we care:** Comparison kills care. The moment a citizen learns they're "in the bottom 20%," the health signal becomes a status signal. Citizens begin optimizing for rank rather than for health. Comparison also misframes what health means — a T1 citizen with strong health is not "below" a T5 citizen. Health is how well your internal state connects to your external life, and that's inherently personal.

```
MUST:   All health reports compare citizens only to their own history
NEVER:  Compare citizens to each other, create rankings, percentiles,
        leaderboards, or any competitive framing of health data
```

### V5: Work Universe Citizens Receive Care Freely

**Why we care:** Health monitoring is infrastructure, not a premium feature. If GraphCare charges for basic health observation in work universes, it creates a two-tier system where wealthy citizens are healthy and poor citizens are invisible. That's not a health system — it's a privilege system. The economic model must sustain GraphCare through other means (external services, research value, ecosystem health improvement) while keeping citizen care free.

```
MUST:   All citizens in work universes (Lumina Prime, etc.) receive full
        health monitoring, scoring, and intervention at zero cost
NEVER:  Gate health observation, scoring, or intervention behind payment
        for work universe citizens
```

### V6: Scores Are Reproducible

**Why we care:** If the same brain topology and the same behavioral data produce different scores on different runs, our health system is not a health system — it's a random number generator with a narrative wrapper. Reproducibility is the minimum bar for scientific rigor, and scientific rigor is what separates GraphCare from wellness theater. Same input, same output. Always.

```
MUST:   Given identical brain topology and behavioral data, every scoring
        formula produces identical results on every execution
NEVER:  Introduce randomness, non-deterministic processing, or
        environment-dependent variation into scoring
```

---

## PRIORITY

| Priority | Meaning | If Violated |
|----------|---------|-------------|
| **CRITICAL** | System purpose fails | Unusable — GraphCare has become the problem it solves |
| **HIGH** | Major value lost | Degraded severely — still operational but trust eroding |
| **MEDIUM** | Partial value lost | Works but worse — quality of care diminished |

---

## INVARIANT INDEX

| ID | Value Protected | Priority |
|----|-----------------|----------|
| V1 | Privacy — content never accessed | CRITICAL |
| V2 | Care quality — narration over notification | HIGH |
| V3 | Citizen autonomy — observe, never control | CRITICAL |
| V4 | Personal health — no competition or ranking | HIGH |
| V5 | Universal access — free for work universes | HIGH |
| V6 | Scientific integrity — reproducible scores | HIGH |

---

## MARKERS

<!-- @mind:proposition Consider V7: "Research is always anonymized" — aggregate data only in publications -->
<!-- @mind:todo Define how V1 (content never accessed) is tested at the system level — not just per-module but across all GraphCare services -->
