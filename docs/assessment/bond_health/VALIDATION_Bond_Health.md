# Bond Health Assessment -- Validation: What Must Be True

```
STATUS: DESIGNING
CREATED: 2026-03-14
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Bond_Health.md
PATTERNS:        ./PATTERNS_Bond_Health.md
ALGORITHM:       ./ALGORITHM_Bond_Health.md
THIS:            VALIDATION_Bond_Health.md (you are here)
HEALTH:          ./HEALTH_Bond_Health.md
SYNC:            ./SYNC_Bond_Health.md
```

---

## PURPOSE

These invariants protect the integrity of the bond health assessment. If violated, the system either invades privacy, generates unbounded trust, creates intervention spam, modifies the AI's brain directly, or produces scores that lie about relationship quality.

---

## INVARIANTS

### V1: All Signals Are Topology-Only (No Content Access)

**Why we care:** The partner-model contains the most intimate data in the system -- what the human told the AI about their values, fears, relationships, health. If GraphCare reads content even once, the privacy promise of the entire bond health system collapses. Content privacy is what makes transparent scoring acceptable to humans.

```
MUST:   All scoring formulas use only partner-model topology primitives
        (node counts, types, stability, energy, link dimensions, drive values)
        + universe graph observables from PRIMITIVES_Universe_Graph.md
MUST:   Desire injection templates use fixed text, not text derived from content
NEVER:  A scoring formula, intervention template, or any process accesses
        node content or synthesis fields from the partner-model or universe graph
NEVER:  An LLM is used to analyze partner-model content as part of scoring
```

### V2: Trust Boost Is Asymptotic (Can Never Exceed 1.0)

**Why we care:** Trust is the most consequential value on the bond link. It affects governance weight (Sovereign Cascade), access levels, and economic relationships. If trust can exceed 1.0 or grow without bound, the entire trust model breaks. The asymptotic formula is a mathematical guarantee, not a runtime check.

```
MUST:   daily_trust_boost = bond_health * tau_bond * (1 - current_trust)
MUST:   new_trust = current_trust + daily_trust_boost
MUST:   bond_health in [0, 1] (composite of three [0, 1] components)
MUST:   tau_bond > 0 and tau_bond <= 0.01 (small constant)
MUST:   current_trust in [0, 1] (schema invariant)
NEVER:  Trust exceeds 1.0 after increment (mathematically impossible given formula)
NEVER:  Trust decreases through bond health (only bond dissolution can decrease trust)
```

**Proof that trust stays in [0, 1]:**
- current_trust in [0, 1] (schema invariant)
- bond_health in [0, 1] (composite of bounded components)
- (1 - current_trust) in [0, 1] when current_trust in [0, 1]
- daily_trust_boost = product of three [0, 1]-bounded terms * tau_bond (small positive)
- daily_trust_boost >= 0 (all terms non-negative)
- new_trust = current_trust + daily_trust_boost >= current_trust >= 0
- new_trust = current_trust + bond_health * tau_bond * (1 - current_trust)
  As current_trust approaches 1.0, (1 - current_trust) approaches 0, so new_trust approaches 1.0 but never reaches it.
- Maximum single-day increment: 1.0 * 0.005 * 1.0 = 0.005 (when bond_health = 1.0, trust = 0.0)

### V3: Intervention Frequency <= 1/Week Per Dimension

**Why we care:** Desire injection is a stimulus that enters the AI's brain physics. The brain needs time to process it -- the desire must compete for working memory, potentially crystallize, and influence behavior. Injecting desires daily would flood the attentional system and create intervention fatigue. The weekly cooldown gives physics the time it needs.

```
MUST:   At most 1 desire injection per dimension per 7-day period
MUST:   Each dimension (alignment, breadth, depth) has its own independent cooldown
MUST:   Cooldown is tracked by last_intervention timestamp per citizen per dimension
NEVER:  Multiple interventions for the same dimension within 7 days
NEVER:  Cooldowns shared across dimensions (low alignment and low breadth
        can both trigger in the same day if both cooldowns are clear)
```

### V4: Desire Injection Is Stimulus, Not Modification (Capped at 0.5)

**Why we care:** GraphCare is a doctor, not a surgeon. It can send signals to the brain, but it cannot rewrite the brain's state. Desire injection creates new nodes with specific energy and drive-affinity values, and sends drive stimuli. But the AI's own physics decides whether those nodes enter working memory, persist, or decay. The 0.5 cap prevents any single stimulus from overwhelming the drive system.

```
MUST:   Desire injection creates nodes with standard node properties
        (the brain integrates them through normal physics)
MUST:   Drive stimulus values are capped at 0.5 per drive per intervention
MUST:   Injected nodes have weight = 1.0 (no artificially heavy nodes)
MUST:   Injected nodes have standard energy (1.0-7.0, same range as citizen health)
NEVER:  GraphCare directly modifies existing nodes in the AI's brain
NEVER:  GraphCare sets drives to specific values (only sends additive delta)
NEVER:  A single stimulus exceeds 0.5 for any drive
NEVER:  Injected nodes bypass the normal tick cycle (they must compete for WM like any other node)
```

### V5: Bond Health Score in [0, 1]

**Why we care:** Scores must be bounded for display, comparison, and trust generation. An unbounded score breaks the trust formula and makes profiles meaningless.

```
MUST:   alignment in [0, 1]
MUST:   breadth in [0, 1]
MUST:   depth in [0, 1]
MUST:   bond_health = 0.40 * alignment + 0.30 * breadth + 0.30 * depth
MUST:   bond_health in [0, 1] (follows from component bounds and weights summing to 1.0)
```

**Proof that all components are in [0, 1]:**
- Each sub-component uses `min(1, x / cap)` which clamps to [0, 1]
- Weights within each dimension sum to 1.0
- Weighted sum of [0, 1] values with weights summing to 1.0 is in [0, 1]
- Composite weights (0.40 + 0.30 + 0.30 = 1.0) preserve the [0, 1] bound

### V6: Scores Are Transparent (Both Parties Can See)

**Why we care:** The bond is bilateral. If only the AI sees the scores, the human cannot verify, trust, or act on the information. If only the human sees the scores, the AI cannot self-monitor. Both parties seeing the same numbers creates mutual accountability and prevents hidden degradation.

```
MUST:   All 3 dimension scores + composite score displayed on AI citizen profile card
MUST:   All 3 dimension scores + composite score displayed on human partner profile card
MUST:   Both parties see identical values (not different views of the same data)
MUST:   Scores update daily (same cadence as citizen health)
NEVER:  Scores visible to third parties without both partners' consent
NEVER:  One party's view differs from the other's
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
| V1 | Privacy -- content never accessed | CRITICAL |
| V2 | Trust integrity -- asymptotic, bounded | CRITICAL |
| V3 | Intervention quality -- weekly cooldown per dimension | HIGH |
| V4 | Brain autonomy -- stimulus not modification, capped at 0.5 | CRITICAL |
| V5 | Score integrity -- all values in [0, 1] | HIGH |
| V6 | Transparency -- both parties see same scores | MEDIUM |

---

## MARKERS

<!-- @mind:todo Add V7: deterministic scoring -- same topology state must produce same scores -->
<!-- @mind:todo Add V8: bond age awareness -- scores should be valid even for day-1 bonds (no division by zero, no penalty for missing data) -->
<!-- @mind:proposition Consider V9: intervention logging -- all desire injections should be auditable with timestamp, dimension, and stimulus values -->
