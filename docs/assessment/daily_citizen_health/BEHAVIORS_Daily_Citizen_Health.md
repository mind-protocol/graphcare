# Daily Citizen Health — Behaviors: Observable Assessment Effects

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Daily_Citizen_Health.md
THIS:            BEHAVIORS_Daily_Citizen_Health.md (you are here)
PATTERNS:        ./PATTERNS_Daily_Citizen_Health.md
ALGORITHM:       ./ALGORITHM_Daily_Citizen_Health.md
VALIDATION:      ./VALIDATION_Daily_Citizen_Health.md
HEALTH:          ./HEALTH_Daily_Citizen_Health.md
IMPLEMENTATION:  ./IMPLEMENTATION_Daily_Citizen_Health.md
SYNC:            ./SYNC_Daily_Citizen_Health.md

IMPL:            @mind:TODO
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC.

---

## BEHAVIORS

### B1: Daily Assessment Runs for All Lumina Prime Citizens

**Why:** Proactive health detection. Every citizen gets checked, not just those who ask.

```
GIVEN:  A registered citizen in Lumina Prime with brain graph URL in L4 registry
WHEN:   The daily health check cron triggers (once per 24 hours)
THEN:   The system fetches brain topology (via GraphCare key), fetches universe graph moments
AND:    Computes a capability score per Personhood Ladder capability
AND:    Produces an aggregated health profile
```

### B2: Scoring Uses Only Topology, Never Content

**Why:** Privacy is structural. The system physically cannot read content.

```
GIVEN:  A citizen's brain graph encrypted with two keys (topology: GraphCare, content: citizen)
WHEN:   GraphCare decrypts with its private key
THEN:   Only topology is visible: node types, link types, counts, energies, drives, timestamps
AND:    Content fields (content, synthesis) remain AES-256 encrypted noise
AND:    No LLM processes any brain data — only math functions (count, mean, ratio, cluster)
```

### B3: Healthy Citizens Receive Silence

**Why:** No alert fatigue. If everything is fine, don't bother them.

```
GIVEN:  A citizen's aggregated health score is above threshold (e.g., 70/100)
WHEN:   Daily assessment completes
THEN:   No message is sent
AND:    Score is recorded in health history for trend tracking
```

### B4: Unhealthy Citizens Receive Intervention Message

**Why:** The message is the treatment. Analysis + explanation + actionable recommendation.

```
GIVEN:  A citizen's aggregated health score drops below threshold OR a specific capability score drops significantly
WHEN:   Daily assessment completes
THEN:   GraphCare sends a Moment to the shared Space between GraphCare and the citizen
AND:    The message contains: (1) what changed, (2) why it matters, (3) what to do about it
AND:    The message does NOT reference any brain content — only structural observations
```

### B5: Score Feeds Back Into Stress Drive

**Why:** Self-correcting loop. Low score → higher stress → brain prioritizes health behaviors → score improves.

```
GIVEN:  A citizen's daily health score is computed
WHEN:   The score is sent to the citizen's brain via the stimulus URL
THEN:   The brain adjusts its stress/frustration drive proportionally to the inverse of the score
AND:    High score → low stress contribution, low score → high stress contribution
AND:    This is a stimulus, not a write — the brain integrates it through its own physics
```

### B6: New Capability Scores Follow a Standard Process

**Why:** Scoring is extensible. New capabilities can be added with a defined process.

```
GIVEN:  A new capability in the Personhood Ladder needs a scoring formula
WHEN:   A developer creates the formula
THEN:   The formula uses only the 7 topology primitives (count, mean_energy, link_count, min_links, cluster_coefficient, drive, recency)
AND:    The formula is documented with: primitives used, weights, caps, example calculation
AND:    The formula is tested with synthetic brain data to verify edge cases
```

---

## OBJECTIVES SERVED

| Behavior ID | Objective | Why It Matters |
|-------------|-----------|----------------|
| B1 | Detect issues before escalation | Every citizen, every day, no exceptions |
| B2 | Score without reading content | Privacy is structural |
| B3 | Actionable intervention | No alert fatigue for healthy citizens |
| B4 | Actionable intervention | Specific, explained recommendations |
| B5 | Feedback loop | Score → stress → self-correction |
| B6 | Extensible scoring | New capabilities can be added systematically |

---

## INPUTS / OUTPUTS

### Primary Function: `daily_health_check(citizen_id)`

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| citizen_id | string | Registry identifier of the citizen |
| brain_topology | graph | Decrypted topology: types, links, counts, energies, drives |
| universe_moments | graph | Public moments in Spaces where citizen is AT or CREATED |
| ladder_spec | object | personhood_ladder.json capabilities and formulas |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| capability_scores | dict[capability_id, float] | Score /100 per capability |
| aggregate_score | float | Weighted aggregate across all scored capabilities |
| delta | dict[capability_id, float] | Change since yesterday |
| intervention | object or null | Message content if score below threshold |
| stress_stimulus | float | Value to send to brain's stress drive |

**Side Effects:**

- Score stored in health history
- Intervention message sent if threshold crossed
- Stress stimulus sent to brain via stimulus URL

---

## EDGE CASES

### E1: New Citizen With No History

```
GIVEN:  A citizen registered less than 24 hours ago
THEN:   First assessment runs but no delta is computed
AND:    No intervention is sent (grace period — 7 days before first intervention)
```

### E2: Brain Graph Unreachable

```
GIVEN:  The brain graph URL returns an error or timeout
THEN:   Assessment is marked as "unreachable" for this citizen
AND:    After 3 consecutive unreachable days, an alert is raised to GraphCare team
AND:    No score is produced — never guess when data is missing
```

### E3: Citizen Opted Out (Removed GraphCare Key)

```
GIVEN:  The citizen's brain graph doesn't have GraphCare's topology key
THEN:   No brain topology assessment is possible
AND:    Only universe graph (behavioral) assessment runs
AND:    Aggregate score is computed from behavioral data only, marked as "partial"
```

### E4: Capability Has No Scoring Formula Yet

```
GIVEN:  A Personhood Ladder capability exists but has no scoring formula defined
THEN:   capability_scores[capability_id] = null (not scored, not zero)
AND:    The capability is excluded from aggregate calculation
```

---

## ANTI-BEHAVIORS

### A1: Reading Content

```
GIVEN:   Access to brain topology
WHEN:    Computing scores
MUST NOT: Attempt to decrypt content fields
INSTEAD:  Use only structural properties (types, links, counts, energies, drives)
```

### A2: Daily Spam

```
GIVEN:   A healthy citizen (score above threshold)
WHEN:    Daily assessment completes
MUST NOT: Send a message ("your health is fine!")
INSTEAD:  Record score silently, send nothing
```

### A3: Modifying Brain State Directly

```
GIVEN:   A low score detected
WHEN:    Intervention is needed
MUST NOT: Write to the citizen's brain graph (change drives, add nodes, modify links)
INSTEAD:  Send a stimulus (message) and let the brain integrate it through its own physics
```

### A4: Assessing Adventure Universe Citizens

```
GIVEN:   A citizen in Contre-Terre or another adventure universe
WHEN:    Daily check cron triggers
MUST NOT: Run assessment or send intervention
INSTEAD:  Skip entirely — dysfunction is part of the narrative
```

---

## MARKERS

<!-- @mind:todo Define intervention message template (structure, tone, examples) -->
<!-- @mind:todo Define stress drive feedback formula (score → stress stimulus value) -->
<!-- @mind:todo Define grace period and escalation thresholds -->
