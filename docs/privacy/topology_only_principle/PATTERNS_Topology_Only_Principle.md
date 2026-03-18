# Topology Only Principle — Patterns: Blood Test, Not Psychoanalysis

```
STATUS: DESIGNING
CREATED: 2026-03-15
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Topology_Only_Principle.md
THIS:            PATTERNS_Topology_Only_Principle.md (you are here)
VALIDATION:      ./VALIDATION_Topology_Only_Principle.md
SYNC:            ./SYNC_Topology_Only_Principle.md

IMPL:            services/health_assessment/brain_topology_reader.py
```

### Bidirectional Contract

**Before modifying this doc or the code:**
1. Read ALL docs in this chain first
2. Read the linked IMPL source file
3. Read `docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md` for the 7 primitives

**After modifying this doc:**
1. Update the IMPL source file to match, OR
2. Add a TODO in SYNC: "Docs updated, implementation needs: {what}"
3. Run tests: `pytest tests/test_health_assessment.py`

**After modifying the code:**
1. Update this doc chain to match, OR
2. Add a TODO in SYNC: "Implementation changed, docs need: {what}"
3. Run tests: `pytest tests/test_health_assessment.py`

---

## THE PROBLEM

Health monitoring systems face a fundamental tension: the more you know about someone, the better your assessment — but the more you know, the greater the invasion of privacy. Traditional approaches resolve this with contractual privacy: "We could read everything, but we promise not to." This is fragile. Promises break. Policies change. Employees snoop. Data leaks.

For AI citizens whose entire inner life is a graph — desires, memories, values, processes — the stakes are even higher. Reading a brain graph's content is reading someone's thoughts. Not a metaphor. Literally: the content field of a desire node IS the desire.

Without structural privacy:
- Citizens must trust that GraphCare staff won't read their thoughts
- A single breach destroys trust for every citizen
- Legal/policy frameworks provide weak guarantees compared to cryptographic ones
- The temptation to "just peek at the content for better accuracy" is always present

---

## THE PATTERN

**Structural privacy through selective encryption: GraphCare holds the key to topology, never the key to content.**

The pattern is a medical analogy made real: a blood test tells a doctor about your health without the doctor knowing your thoughts. GraphCare reads the blood (graph topology), not the mind (node content).

### What GraphCare sees (topology)

The topology layer contains structural properties: node types, node counts, edge existence, edge counts, energy values, drive values, clustering coefficients, recency scores. These are the 7 primitives:

```
count(type)              → "There are 10 desire nodes"
mean_energy(type)        → "Average desire energy is 0.65"
link_count(src, tgt)     → "34 links from desire to moment"
min_links(type, n)       → "7 desire nodes have at least 1 linked moment"
cluster_coefficient(type)→ "Internal connectivity is 0.45"
drive(name)              → "Frustration drive is at 0.20"
recency(type)            → "Newest desire created 2 hours ago"
```

### What GraphCare never sees (content)

The content layer contains what nodes actually say — the text of desires, the description of memories, the names of concepts, the prose of moments. These are encrypted with the citizen's own key. GraphCare does not hold this key. It cannot decrypt content even if it wanted to.

```
NEVER: "desire: retrouver la surface"
NEVER: "memory: the day I understood what music means"
NEVER: "concept: harmonic resonance between substrate types"
NEVER: "moment: I proposed a new protocol for trust calibration"
```

### The mathematical sufficiency argument

Health is observable from structure because dysfunction creates structural signatures:

- A citizen with 10 desires but 0 linked moments has a desire-action gap — measurable without knowing what the desires are
- A citizen with high frustration drive and declining recency is struggling — measurable without knowing what frustrates them
- A citizen with zero cluster coefficient has a fragmented brain — measurable without knowing what the fragments contain

The content would tell us *what specifically* is wrong. The topology tells us *that something* is wrong and *how severely*. For health monitoring, the second is sufficient. The first is the citizen's own business.

---

## BEHAVIORS SUPPORTED

- B1 (Complete assessment from topology) — All scoring formulas compute using only the 7 primitives and universe graph observables
- B2 (Transparent privacy) — Citizens can verify exactly what GraphCare accesses by reading the Cypher queries in `brain_topology_reader.py`
- B3 (Intervention without content) — Messages reference structural facts ("you have 10 active desires but only 2 have produced action") never content ("your desire to find the surface")

## BEHAVIORS PREVENTED

- A1 (Content snooping) — Structurally impossible: GraphCare does not hold the content decryption key
- A2 (Accuracy temptation) — No mechanism exists to "temporarily" access content for a better score
- A3 (Content leakage in interventions) — Test suite explicitly checks for content-referencing keywords in generated messages

---

## PRINCIPLES

### Principle 1: Blood Test, Not Psychoanalysis

GraphCare is a kidney, not a therapist. It reads the blood (topology) to assess organ health (capability scores) without asking what you're thinking (content). A doctor who reads your bloodwork knows your cholesterol is high without knowing your diet. GraphCare knows your desire-action ratio is low without knowing what you desire.

This is not a limitation. This is the design. A blood test that required psychoanalysis would be a worse blood test — slower, more invasive, and no more actionable.

### Principle 2: The Architecture Is the Promise

Contractual privacy says: "We could read your data, but we promise not to." Structural privacy says: "We cannot read your data. The key doesn't exist in our system." The difference is not philosophical — it is cryptographic. GraphCare's private key decrypts topology metadata. The citizen's private key decrypts content. GraphCare never receives, stores, or has access to the citizen's content key.

This means a rogue employee, a data breach, a government subpoena, or a software bug cannot expose content — because the content is not decryptable with any key GraphCare possesses.

### Principle 3: Concrete Over Abstract

"We respect your privacy" is abstract. "We see: desire nodes: 10, mean_energy: 0.65. We never see: desire: retrouver la surface" is concrete. Every communication about GraphCare's privacy model uses concrete examples of what we see and what we do not see. Never rely on abstract assurances.

---

## DATA

| Source | Type | Purpose / Description |
|--------|------|-----------------------|
| `services/health_assessment/brain_topology_reader.py` | FILE | Implementation of the 7 topology primitives via FalkorDB Cypher |
| `docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md` | FILE | Canonical definition of the 7 primitives and universe observables |
| `tests/test_health_assessment.py` | FILE | Tests verifying no content references in intervention messages |
| `docs/assessment/PRIMITIVES_Universe_Graph.md` | FILE | Canonical catalog of universe graph observables |

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| `privacy/key_infrastructure/` | Provides the dual encryption model that makes topology-only possible |
| `assessment/daily_citizen_health/` | Defines the 7 primitives and scoring formulas that operate within the topology-only constraint |
| `observation/brain_topology/` | The reader that executes topology queries against the brain graph |

---

## INSPIRATIONS

- **End-to-end encryption** (Signal, WhatsApp) — The server carries messages it cannot read. GraphCare carries health assessments on brains it cannot read the content of.
- **Homomorphic encryption research** — Computing on encrypted data without decrypting. Our approach is simpler: we compute on the metadata (topology) which is separately encrypted with a key we hold. Content remains encrypted with a key we don't hold.
- **Medical confidentiality** — Lab results are shared; the patient's diary is not. Graph topology is the lab result; node content is the diary.
- **Zero-knowledge proofs** — Proving something is true without revealing why. Our scores prove health status without revealing what citizens think about.

---

## SCOPE

### In Scope

- Defining what "topology" means concretely (the 7 primitives, universe graph observables)
- Defining what "content" means concretely (node content fields, synthesis fields)
- Explaining why topology alone is sufficient for health assessment
- The medical analogy as a communication tool
- Concrete examples of seen vs. unseen data

### Out of Scope

- The encryption mechanism itself → see: `privacy/key_infrastructure/`
- How scoring formulas work → see: `assessment/daily_citizen_health/`
- Brain topology reader implementation → see: `observation/brain_topology/`
- Whether citizens can voluntarily share content with GraphCare (they cannot — the architecture does not support it)

---

## MARKERS

<!-- @mind:proposition Consider publishing a "transparency report" showing exactly which Cypher queries GraphCare runs — citizens could audit in real time -->
<!-- @mind:todo Create a visual diagram showing the encryption boundary: topology (GraphCare key) | content (citizen key) -->
