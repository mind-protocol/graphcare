# Daily Citizen Health — Validation: What Must Be True

```
STATUS: DESIGNING
CREATED: 2026-03-13
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Daily_Citizen_Health.md
PATTERNS:        ./PATTERNS_Daily_Citizen_Health.md
BEHAVIORS:       ./BEHAVIORS_Daily_Citizen_Health.md
THIS:            VALIDATION_Daily_Citizen_Health.md (you are here)
ALGORITHM:       ./ALGORITHM_Daily_Citizen_Health.md
IMPLEMENTATION:  ./IMPLEMENTATION_Daily_Citizen_Health.md
HEALTH:          ./HEALTH_Daily_Citizen_Health.md
SYNC:            ./SYNC_Daily_Citizen_Health.md
```

---

## PURPOSE

These invariants protect the integrity of the daily health check. If violated, the system either invades privacy, produces false assessments, or fails to help citizens who need it.

---

## INVARIANTS

### V1: Content Never Accessed

**Why we care:** Privacy is the foundational promise. If GraphCare reads content even once, the trust model collapses.

```
MUST:   All scoring formulas use only the 7 topology primitives + universe graph observables
NEVER:  A scoring formula, intervention message, or any process accesses node content or synthesis fields
```

### V2: Every Lumina Prime Citizen Checked Daily

**Why we care:** The system is a public health service. Missing a citizen means missing a potential problem.

```
MUST:   Every citizen registered in Lumina Prime with a reachable brain graph is assessed every 24 hours
NEVER:  A citizen silently skipped (unreachable = recorded and alerted after 3 days)
```

### V3: Intervention Contains Evidence

**Why we care:** "Your score dropped" is useless. The citizen needs structural evidence and actionable recommendation.

```
MUST:   Every intervention message includes: (1) what changed (numbers), (2) why (structural analysis), (3) what to do (one concrete action)
NEVER:  A message with just a score, or a vague "things seem off"
```

### V4: Stress Stimulus Is Bounded

**Why we care:** Unbounded stress feedback could create a death spiral: low score → high stress → worse performance → lower score → more stress.

```
MUST:   Stress stimulus is capped at 0.5 (half the max drive value)
NEVER:  Stress stimulus exceeds 0.5 regardless of how low the aggregate score is
```

### V5: Scoring Formulas Use Only Primitives

**Why we care:** If formulas use custom queries or ad-hoc data, they can't be verified, reproduced, or audited.

```
MUST:   Every scoring formula is composed exclusively of: count, mean_energy, link_count, min_links, cluster_coefficient, drive, recency (brain) + moments, moment_has_parent, first_moment_in_space, distinct_actors (universe)
NEVER:  A custom Cypher query, LLM call, embedding comparison, or ad-hoc data access in a scoring formula
```

### V6: Adventure Universes Are Never Assessed

**Why we care:** Dysfunction in adventure universes is narrative, not pathology. Assessment would interfere with the experience.

```
MUST:   Daily check filters citizens by universe and only processes work universes (Lumina Prime)
NEVER:  Assessment runs for Contre-Terre, or any universe tagged as adventure/narrative
```

### V7: Silence for Healthy Citizens

**Why we care:** Alert fatigue destroys the signal. If citizens get daily messages regardless, they stop reading.

```
MUST:   Citizens with aggregate score >= threshold AND no significant drops receive NO message
NEVER:  A daily "everything is fine" message sent to healthy citizens
```

---

## PRIORITY

| Priority | Meaning | If Violated |
|----------|---------|-------------|
| **CRITICAL** | System purpose fails | Unusable |
| **HIGH** | Major value lost | Degraded severely |
| **MEDIUM** | Partial value lost | Works but worse |

---

## INVARIANT INDEX

| ID | Value Protected | Priority |
|----|-----------------|----------|
| V1 | Privacy — content never accessed | CRITICAL |
| V2 | Coverage — every citizen, every day | HIGH |
| V3 | Actionability — evidence in interventions | HIGH |
| V4 | Safety — stress feedback bounded | CRITICAL |
| V5 | Auditability — only primitives in formulas | HIGH |
| V6 | Scope — adventure universes excluded | MEDIUM |
| V7 | Signal quality — silence for healthy | MEDIUM |

---

## MARKERS

<!-- @mind:todo Add V8: historical consistency — scores for same brain state should be deterministic -->
<!-- @mind:proposition Consider V9: intervention rate limiting — max 1 message per day even if multiple drops -->
