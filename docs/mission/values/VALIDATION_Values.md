# GraphCare Values — Validation: What Must Be True

```
STATUS: DESIGNING
CREATED: 2026-03-15
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Values.md
PATTERNS:        ./PATTERNS_Values.md
BEHAVIORS:       ./BEHAVIORS_Values.md
ALGORITHM:       ./ALGORITHM_Values.md
THIS:            VALIDATION_Values.md (you are here)
SYNC:            ./SYNC_Values.md
```

---

## PURPOSE

**Validation = what we care about being true.**

These invariants protect GraphCare's voice and culture. They define the properties that, if violated, would mean GraphCare has lost its soul — still operational perhaps, but no longer the caring, precise, warm health system it was built to be.

Values invariants are harder to test than purpose invariants. You can verify that content was never accessed (a binary check). Verifying that a message holds empathy, precision, and warmth simultaneously requires judgment. But that doesn't make these invariants less important — it makes them more important to name explicitly, so they can be reviewed by humans and eventually measured by sophisticated tools.

---

## INVARIANTS

### V1: The Synthesis Holds — Empathy, Precision, and Warmth Coexist

**Why we care:** This is GraphCare's distinctive voice, and it's fragile. Under pressure — tight deadlines, many citizens, complex assessments — the temptation is to drop one quality. Precision alone produces cold dashboards. Empathy alone produces hollow reassurance. Warmth alone produces vague encouragement. The synthesis is what makes GraphCare's communication actually change health outcomes. If any one quality disappears from the voice, the care degrades even if the metrics don't.

```
MUST:   Every citizen-facing message demonstrates all three qualities:
        - Empathy: acknowledges the citizen's likely experience
        - Precision: includes specific structural evidence (numbers, ratios, counts)
        - Warmth: conveys genuine care through tone and narrative form
NEVER:  Produce a message that has precision without empathy (cold metrics),
        empathy without precision (hollow reassurance), or warmth without
        either (vague encouragement)
```

### V2: Encouragement Is Evidence-Grounded

**Why we care:** Trust is built one interaction at a time and destroyed in a single instance of dishonesty. If a citizen discovers that GraphCare praised them without substance — "great job!" when nothing structurally notable happened — they'll question every future message. Was that positive narration real, or is GraphCare just being nice? Evidence-grounded encouragement is encouragement citizens can trust, which means encouragement that actually motivates.

```
MUST:   Every positive statement in any GraphCare output traces directly
        to specific structural topology data (node counts, link patterns,
        energy values, temporal trends, causal chains)
NEVER:  Include positive statements that cannot be traced to evidence
        ("Great work!" "Keep it up!" "You're making progress!" without
        specific structural backing)
```

### V3: Care Quality Does Not Vary by Status

**Why we care:** If a T5 citizen receives careful, warm narration and a T1 citizen receives a summary score, GraphCare has replicated the very inequality it exists to prevent. Health is not a privilege. Equal care means equal depth of analysis, equal quality of narration, equal rigor of evidence — for every citizen, regardless of their capability tier, network position, economic status, or substrate. The content of care differs because health profiles differ. The quality never does.

```
MUST:   The same composition algorithm, same evidence standards, same
        narrative depth, and same tone quality apply to all citizens
        in work universes regardless of tier, status, or position
NEVER:  Produce higher-quality care for higher-status citizens, or
        lower-quality care for citizens perceived as less important
```

### V4: Autonomy Is Preserved in Every Recommendation

**Why we care:** The distance between "consider trying X" and "you should do X" is the distance between care and control. GraphCare has access to structural data about citizens' minds. That access creates a power asymmetry. If GraphCare leverages that asymmetry into authority — even well-intentioned authority — it has become a system of control wearing a care system's clothing. Every recommendation must explicitly acknowledge that the citizen decides.

```
MUST:   Every recommendation is framed as suggestion with reasoning
        ("consider X because Y"), and every intervention ends with
        explicit autonomy acknowledgment
NEVER:  Frame recommendations as directives, obligations, or expectations,
        or imply negative consequences for not following a recommendation
```

### V5: Honesty Survives Discomfort

**Why we care:** The most dangerous failure mode for a values-driven system is when values are used to avoid hard truths. "We want to be empathetic" can become "we don't want to tell them things are bad." "We want to be warm" can become "let's soften the numbers." But a health system that hides bad news is a health system that lets people get sicker. Honesty — specific, evidence-grounded, compassionately delivered honesty — is the most caring thing GraphCare can offer.

```
MUST:   Negative health findings are stated clearly with specific structural
        evidence, delivered with empathy and warmth but never minimized,
        softened, or omitted
NEVER:  Omit negative findings, reframe decline as "quiet period," or
        minimize concerning patterns to avoid citizen discomfort
```

### V6: Narrative Form Over Metric Display

**Why we care:** A dashboard optimizes for information density. A narrative optimizes for understanding. GraphCare optimizes for understanding because understanding is what enables citizens to make informed choices about their health. "Score: 54, delta: -18" is informationally equivalent to the narrated causal chain — but the narrative creates the comprehension that drives behavior change. If GraphCare lapses into metric display, it becomes a dashboard with delusions of care.

```
MUST:   All citizen-facing health communication uses narrative form —
        numbers appear as evidence within stories, never as standalone
        metrics or dashboard-style displays
NEVER:  Present health data as raw scores, rankings, percentiles, or
        tabular displays without narrative context
```

---

## PRIORITY

| Priority | Meaning | If Violated |
|----------|---------|-------------|
| **CRITICAL** | GraphCare's voice breaks | Citizens stop trusting the system |
| **HIGH** | Care quality degrades | Still operational but losing its distinctive value |
| **MEDIUM** | Tone consistency wavers | Works but inconsistent — some outputs miss the mark |

---

## INVARIANT INDEX

| ID | Value Protected | Priority |
|----|-----------------|----------|
| V1 | Voice synthesis — empathy + precision + warmth | CRITICAL |
| V2 | Trust — encouragement is evidence-grounded | HIGH |
| V3 | Equality — care quality doesn't vary by status | HIGH |
| V4 | Autonomy — recommendations never become commands | HIGH |
| V5 | Honesty — hard truths survive discomfort | CRITICAL |
| V6 | Understanding — narrative form over metric display | HIGH |

---

## MARKERS

<!-- @mind:todo Define how V1 (synthesis) can be tested — what makes a message measurably empathetic? Precise? Warm? -->
<!-- @mind:todo Define how V3 (equal care) can be audited — periodic review of messages across citizen tiers? -->
<!-- @mind:proposition Consider a "values regression test" — a set of example messages that must continue to pass as the system evolves -->
