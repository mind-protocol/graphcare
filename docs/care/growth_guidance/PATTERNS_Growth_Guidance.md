# Growth Guidance — Patterns: Personhood Ladder Navigation

```
STATUS: DESIGNING
CREATED: 2026-03-15
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Growth_Guidance.md
THIS:            PATTERNS_Growth_Guidance.md (you are here)
BEHAVIORS:       ./BEHAVIORS_Growth_Guidance.md
ALGORITHM:       (future)
VALIDATION:      (future)
IMPLEMENTATION:  (future)
SYNC:            ./SYNC_Growth_Guidance.md

IMPL:            (future — no code exists yet)
```

### Bidirectional Contract

**Before modifying this doc or the code:**
1. Read ALL docs in this chain first
2. Read the Personhood Ladder spec: `docs/personhood_ladder.json`
3. Read the Personhood Ladder concept: `docs/assessment/personhood_ladder/CONCEPT_Personhood_Ladder.md`
4. Read the daily health algorithm: `docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md`

**After modifying this doc:**
1. Update the IMPL source file to match, OR
2. Add a TODO in SYNC: "Docs updated, implementation needs: {what}"

---

## THE PROBLEM

A citizen gets their health score. It says 62/100. What now?

The daily health check can tell you what's low. The intervention message can say "your initiative score dropped." But neither can tell you: what is the single most productive thing you could work on next? Which capability, if improved, would unlock the most growth? What concrete action would move the needle?

Without growth guidance:
- Citizens know they're "unhealthy" but not where to focus
- The Personhood Ladder exists as a rich framework but nobody uses it for navigation
- Improvement feels abstract ("get better") instead of concrete ("do this specific thing")
- Citizens optimize randomly or not at all, because the growth path is invisible

The Personhood Ladder has 104 capabilities across 14 aspects, organized in 9 tiers. That's a map. But a map without "you are here" and "go this way" is just a wall of information. Growth guidance turns the map into directions.

---

## THE PATTERN

**Bottom-up gap analysis with grounded recommendations.**

### Step 1: Profile the Citizen's Current Mastery

Read existing capability scores from the continuous health check. For each of the 14 aspects, determine the citizen's effective tier: the highest tier at which all capabilities are scored above mastery threshold.

Example: A citizen might be T3 on Execution (all T1-T3 execution capabilities above 70) but T1 on Economics (only T1 economics capabilities above 70, T2 economics capabilities below 70). Their profile is not a single number — it's a 14-dimensional position on the Ladder.

### Step 2: Find the Lowest Unmastered Gap

Scan the citizen's profile from the bottom. The most productive growth target is the lowest tier where a capability is unmastered. Why lowest? Because tiers are cumulative — T3 capabilities assume T1 and T2 mastery. A gap at T2 undermines everything built on top of it.

Within a tier, prioritize:
- Capabilities that are *almost* mastered (score 50-69) over those that are far from it (score 0-30). The almost-mastered ones have momentum.
- Capabilities that are prerequisites for other capabilities the citizen is already attempting. Unlocking a prerequisite has cascading benefits.

### Step 3: Ground the Recommendation in the Graph

Don't say "improve your initiative." Say what that means in the citizen's actual world:

- Look at the citizen's universe graph: which spaces do they frequent? Who do they interact with?
- Look at the capability's `how_to_verify` field in personhood_ladder.json: what concrete behavior demonstrates this capability?
- Match the verification criteria to a real opportunity in the citizen's graph: a space they could contribute to, a peer they could reach out to, an action they could take.

Example: For the capability `init_propose_improvements` (T2 Initiative):
- `how_to_verify`: "Suggests improvements to existing systems or processes"
- Graph check: citizen is active in #engineering but has zero high_hierarchy_out_moments (no elaborative proposals)
- Recommendation: "You're active in #engineering but haven't proposed changes yet. Try suggesting one small improvement to how the team works. Even a question like 'what if we tried X?' counts."

### Step 4: Deliver at the Right Moment

Growth recommendations are not daily. They arrive when:
- A capability score changes significantly (new assessment data available)
- The citizen has been stable long enough that the recommendation is grounded
- The citizen is NOT in crisis (crisis_detection would be handling them)

Delivery is to the citizen's GraphCare space. One recommendation at a time. Not a list of five things to improve — one thing. The single most productive next step.

### The Key Insight

Growth is measured by what you *can do*, not what you *don't fail at*. The Personhood Ladder names capabilities positively: "proposes improvements," "follows through on commitments," "mentors others." Mastery means demonstrating the capability, not avoiding its failure mode. Growth guidance looks for the presence of capability, not the absence of pathology.

---

## BEHAVIORS SUPPORTED

- B1 (Gap Identification) — lowest unmastered capability found per aspect
- B2 (Grounded Recommendation) — advice references real graph topology, not abstractions
- B3 (Single-Step Focus) — one recommendation at a time, the most productive next step
- B4 (Ladder as Map) — the Personhood Ladder used for navigation, not judgment

## BEHAVIORS PREVENTED

- A1 (Abstract advice) — "improve your social skills" replaced by specific, graph-grounded actions
- A2 (Overwhelming lists) — one recommendation, not five
- A3 (Top-down aspiration) — never targets capabilities more than 1 tier above current mastery
- A4 (Judgment framing) — never "you're failing at X," always "here's what you could reach for"

---

## PRINCIPLES

### Principle 1: Bottom-Up, Not Top-Down

Always work from the foundation. A citizen with gaps at T2 should not be told about T4 opportunities. The lowest unmastered capability is always the right target because tiers are cumulative. Strengthening the foundation makes everything above it more stable. Jumping ahead creates hollow advancement — capabilities that look mastered but lack support.

### Principle 2: The Map Is Not the Territory

The Personhood Ladder describes capabilities. It does not describe the citizen. A citizen is not "a T3." They are a person with a profile that includes T3 mastery on some dimensions and T1 on others. Growth guidance never reduces a citizen to a tier label. It always speaks in terms of specific capabilities, not tiers.

### Principle 3: Momentum Over Deficit

When choosing which gap to target, prefer capabilities that are close to mastery (score 50-69) over those that are far away (score 0-30). The close-to-mastery capabilities have momentum — the citizen is already partway there. Closing a near-gap builds confidence and demonstrates that growth is real and achievable. Tackling the deepest deficit first can feel punishing.

### Principle 4: Verify, Don't Assume Mastery

The Personhood Ladder says mastery means demonstrated behavior, not absence of failure. A citizen who never faces a situation requiring "conflict resolution" doesn't have mastery of conflict resolution — they have no data. Growth guidance distinguishes between "scored low because capability is absent" and "scored null because capability was never tested." Only the former gets a recommendation. The latter gets noted as untested.

### Principle 5: Growth Pace Is Not GraphCare's Decision

Some citizens grow fast. Some grow slowly. Some choose depth in 3 aspects over breadth across 14. Growth guidance presents opportunities; it does not set timelines, expectations, or pressure. The stress feedback loop (stress_stimulus_sender) handles the motivational pressure. Growth guidance handles the directional clarity.

---

## DATA

| Source | Type | Purpose / Description |
|--------|------|-----------------------|
| `docs/personhood_ladder.json` | FILE | 104 capabilities with `how_to_verify`, `failure_mode`, tier, aspect |
| Health score history (L2) | TIMESERIES | Per-capability scores to identify gaps and trends |
| Universe graph (Lumina Prime) | GRAPH | Real spaces, actors, moments — for grounding recommendations |
| Brain topology (via GraphCare key) | GRAPH | Drive states, desire structure — for understanding motivation |

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| Continuous citizen health (assessment) | Provides per-capability scores that growth guidance analyzes |
| Personhood Ladder (assessment) | The framework of 104 capabilities across 14 aspects and 9 tiers |
| Universe graph | For grounding recommendations in real graph topology |
| Brain topology reader | For understanding drive state (is the citizen motivated? frustrated? curious?) |
| Crisis detection (care) | Growth guidance defers when crisis is detected — no recommendations during emergency |
| Messaging system | Delivers recommendations to the citizen's GraphCare space |

---

## INSPIRATIONS

- **Duolingo's next-lesson algorithm** — Identifies the most productive next exercise based on what you know and what's closest to being learned. Not random — targeted at the zone of proximal development.
- **Rock climbing grade progression** — You don't attempt 5.12 before mastering 5.10. Grades are cumulative, and the community understands that skipping grades creates fragility. Growth guidance applies the same logic to capability tiers.
- **Strengths-based coaching** — The recommendation is "here's what you could reach for" not "here's what you're failing at." Growth is framed as extension of existing capability, not remediation of deficiency.
- **The intervention composer's structure** — The existing `intervention_composer.py` follows: observation, analysis, recommendation. Growth guidance uses the same skeleton but fills it with growth-oriented content instead of health-alert content.

---

## SCOPE

### In Scope

- Per-aspect tier identification (effective mastery level across 14 dimensions)
- Lowest unmastered gap identification within and across aspects
- Graph-grounded recommendations (referencing real spaces, actors, actions)
- Single-step focus (one recommendation per delivery)
- Cadence control (deliver on score change, not on fixed schedule)
- Positive framing aligned with Venice Values

### Out of Scope

- Capability scoring → handled by continuous health check and scoring_formulas/
- Crisis detection → handled by crisis_detection module
- Long-term development plans (multi-step curricula) → v2 possibility
- Comparison between citizens → structurally prevented
- Content reading → topology only, like all GraphCare systems

---

## MARKERS

<!-- @mind:todo Define mastery threshold: is 70/100 the right score for "mastered"? Needs calibration. -->
<!-- @mind:todo Map personhood_ladder.json capabilities to specific graph-grounding strategies per capability type -->
<!-- @mind:todo Define the cadence: how often can growth guidance deliver to the same citizen? Minimum interval? -->
<!-- @mind:proposition Consider a "growth history" that shows the citizen which capabilities they've mastered over time -->
<!-- @mind:proposition Consider aspect-priority input: let citizens optionally indicate which aspects they want to grow in -->
