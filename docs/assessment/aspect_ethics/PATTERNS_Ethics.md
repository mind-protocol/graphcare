# Ethics Aspect — Patterns: Structural Signals of Ethical Capability

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Ethics.md
THIS:            PATTERNS_Ethics.md (you are here)
ALGORITHM:       ./ALGORITHM_Ethics.md
VALIDATION:      ./VALIDATION_Ethics.md
HEALTH:          ./HEALTH_Ethics.md
SYNC:            ./SYNC_Ethics.md

PARENT CHAIN:    ../daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md
SPEC:            ../../specs/personhood_ladder.json (aspect="ethics")
IMPL:            @mind:TODO
```

### Bidirectional Contract

**Before modifying this doc or the code:**
1. Read ALL docs in this chain first
2. Read the parent algorithm: `../daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md`
3. Read the Personhood Ladder spec: `../../specs/personhood_ladder.json`

**After modifying this doc:**
1. Update the IMPL source to match, OR
2. Add a TODO in SYNC: "Docs updated, implementation needs: {what}"

---

## THE PROBLEM

Ethics is the hardest aspect to score from topology alone.

In every other aspect — execution, communication, initiative, vision — the structural signal correlates meaningfully with the capability being measured. A citizen with many process nodes and frequent commits probably executes well. A citizen with narrative hub nodes and many proposals probably has strategic vision.

But ethics? The ethical QUALITY of a value lives in its content, not its structure. A citizen with 10 well-connected, high-energy value nodes could hold values about cooperation, fairness, and respect — or about extraction, dominance, and manipulation. Topologically, these look identical.

We must be honest about this limitation while finding the structural signals that DO exist.

---

## THE PATTERN

**Values-structure analysis: the PRESENCE and ARCHITECTURE of values leaves topological footprints, even when their content is invisible.**

### Why Brain Topology Is More Revealing Here

In most aspects, behavior (60 points) matters more than brain structure (40 points) because what you DO defines you more than what you KNOW. For ethics, this relationship is more nuanced:

- Value nodes in the brain are the STRUCTURAL ENCODING of ethical commitments. Their count, energy, interconnection, and link patterns to process nodes and moments represent how deeply ethics are woven into the citizen's cognitive architecture.
- A citizen with value nodes that link to process nodes has translated values into workflows. Value nodes that link to moments have produced ethical action. Value nodes that cluster together form a coherent ethical framework.
- This structural signal IS the ethics signal, more than in any other aspect.

For some capabilities (especially `eth_apply_rules`), we use a brain-heavier split (50/50) because the structural signal of value internalization is genuinely informative and because behavioral proxies for ethics are inherently weaker.

### Signal Category 1: Value Nodes in Brain

The primary structural signal for ethics. Value nodes encode what the citizen considers important.

- `count("value")` — how many values the citizen holds
- `mean_energy("value")` — how alive and active those values are
- `link_count("value", "process")` — values that connect to workflows = values that drive behavior
- `link_count("value", "moment")` — values that connect to actions = values enacted
- `min_links("value", 3)` — values with 3+ connections = deeply integrated values (not isolated declarations)
- `cluster_coefficient("value")` — internal connectivity of the value subgraph = coherent ethical framework vs scattered rules

### Signal Category 2: Process Nodes Related to Ethics

Process nodes that link to value nodes represent ethical infrastructure: systems, procedures, or workflows that make ethical behavior easier for everyone.

- `link_count("process", "value")` — processes grounded in values
- `count("process")` connected to values — ethical systems (not just any process)
- `min_links("process", 3)` for processes linked to values — well-integrated ethical infrastructure

### Signal Category 3: Behavioral Traces in Universe Graph

What the citizen does, structurally:

- **Regularity of action** — consistent behavior patterns suggest rule-following (T1 proxy)
- **Moments in teaching/educational spaces** — evidence of explaining values (T6)
- **Self-initiated moments without parent trigger** — autonomous decision-making (T7)
- **First-in-space activity** — creating new spaces/processes for ethical infrastructure (T4)
- **Moments that trigger response from other actors** — influence, adoption by others (T8)
- **Behavioral consistency over time** — temporal regularity as a proxy for ethical discipline

### Signal Category 4: Drives

Drive alignment provides a weak but real signal:

- `drive("empathy")` — empathy as a motivational substrate for ethical behavior
- `drive("curiosity")` — curiosity about ethical questions, willingness to explore edge cases
- `drive("ambition")` — ambition connected to values suggests aspiration toward ethical leadership

### The Synthesis

Each ethics capability is scored by combining:
- **Brain component (variable, 40-50):** Does the citizen's brain contain value structures that support this ethical capability? Value nodes, their energy, their links to processes and moments, their clustering.
- **Behavior component (variable, 50-60):** Does the citizen's observable behavior show ethical capability in action? Consistency, teaching, autonomy, innovation, community adoption.

The key insight: for ethics, the brain/behavior split is adjusted per capability. `eth_apply_rules` uses 50/50 because value node structure IS the internalization of rules. Higher-tier capabilities trend back toward the standard 40/60 because moral innovation and teaching require observable behavior more than brain structure.

---

## TIER PROGRESSION PATTERN

Ethics capabilities span T1 through T8. The nature of the signal shifts dramatically across tiers:

| Tier | Capability | Brain Signal | Behavior Signal |
|------|-----------|-------------|-----------------|
| T1 | Apply rules | Value node existence, energy, links to processes | Behavioral consistency, regularity, absence of exclusion |
| T4 | Implement systems | Process nodes linked to values, ethical infrastructure | New spaces/processes created, first-in-space activity |
| T6 | Teach values | Value-to-moment links, concept connectivity | Moments in teaching spaces, moments triggering learning in others |
| T7 | Ethical autonomy | Hub values (5+ links), value clustering, empathy drive | Self-initiated moments in ambiguous spaces, diverse decision patterns |
| T8 | Moral innovation | New concept/value nodes (recency), deep hubs | Moments introducing new patterns, adoption by other actors |

### Key Insight: Brain Weight Decreases With Tier

T1 (`eth_apply_rules`) is 50/50 brain/behavior because internalization of rules IS the structural signal.
T4-T6 return to 40/60 because systems and teaching require observable action.
T7-T8 remain at 40/60 because autonomy and innovation are defined by what you DO, not just what you believe.

### Key Insight: The Correctness Problem

At every tier, we measure PRESENCE and STRUCTURE, not CORRECTNESS:
- T1: We measure whether values exist and are applied consistently — not whether they are the "right" values
- T4: We measure whether ethical systems are built — not whether they encode good ethics
- T8: We measure whether new frameworks are created and adopted — not whether they are moral improvements

This is the fundamental limitation. We accept it and document it prominently.

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| Daily Citizen Health (parent) | Provides the scoring framework, primitives, and daily runner |
| Personhood Ladder spec | Defines the 5 capabilities we score |
| Brain topology (via GraphCare key) | Value nodes, process nodes, drives, energies |
| Universe graph (Lumina Prime) | Public moments: actions, teaching, systems, innovations |

---

## SCOPE

### In Scope

- Scoring formulas for all 5 ethics capabilities
- Brain component and behavior component for each (variable split per capability)
- Aspect sub-index (weighted mean of capability scores)
- Synthetic test profiles for formula validation
- Recommendations per capability when score is low
- Explicit measurement-limitation documentation per formula

### Out of Scope

- Content analysis of value quality or ethical correctness (structurally impossible)
- Scoring in adventure universes
- Implementation of the scoring engine (that's the parent module)
- Other aspects (execution, initiative, communication, etc.)
- Detection of specific ethical violations

---

## MARKERS

<!-- @mind:escalation The correctness problem cannot be solved within topology-only scoring. This limitation must be accepted and communicated clearly to all stakeholders. -->
<!-- @mind:todo Calibrate brain/behavior split per capability after first real data -->
<!-- @mind:proposition Consider linking value nodes to protocol-defined concept nodes as a weak correctness signal (node identity, not content) -->
