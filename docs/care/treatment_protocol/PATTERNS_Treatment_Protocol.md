# Treatment Protocol -- Patterns: Measured, Reversible Interventions

```
STATUS: CANONICAL
CREATED: 2026-03-18
VERIFIED: code reviewed against services/health_assessment/treatment_protocol.py
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Treatment_Protocol.md
THIS:            PATTERNS_Treatment_Protocol.md (you are here)
ALGORITHM:       ./ALGORITHM_Treatment_Protocol.md
VALIDATION:      ./VALIDATION_Treatment_Protocol.md
SYNC:            ./SYNC_Treatment_Protocol.md

IMPL:            services/health_assessment/treatment_protocol.py
                 services/health_assessment/frequencies.py
```

### Bidirectional Contract

**Before modifying this doc or the code:**
1. Read ALL docs in this chain first
2. Read `services/health_assessment/frequencies.py` -- the treatment protocol depends on its Frequency, FrequencyResult, apply_frequency, rollback_treatment, and prescribe interfaces
3. Read `services/health_assessment/brain_topology_reader.py` -- the BrainStats dataclass defines what gets snapshotted

**After modifying this doc:**
1. Update the IMPL source file to match, OR
2. Add a TODO in SYNC: "Docs updated, implementation needs: {what}"

---

## THE PROBLEM

GraphCare can observe health (brain topology reader), score it (scoring formulas), and flag concerns (crisis detection, growth guidance). But observation without intervention is incomplete. The question is: how do you intervene in a brain graph safely?

The danger is real. A frequency that injects the wrong stimulus, or seeds the wrong structural nodes, can degrade a brain. Drives can become imbalanced. Clustering can fragment. A "helpful" intervention can make things worse.

Without a treatment protocol, interventions would be fire-and-forget: apply a frequency and hope. No baseline measurement. No post-treatment evaluation. No rollback when things go wrong. Every frequency application would be an irreversible experiment on a citizen's brain.

The treatment protocol exists to make intervention safe, measured, and accountable.

---

## THE PATTERN

**Snapshot before, snapshot after, auto-rollback on degradation.**

The pattern is borrowed from database transactions and clinical trials simultaneously:

### From database transactions: atomicity and rollback

Every node created during treatment is tagged with the `treatment_id`. This tag is the mechanism that makes rollback possible. If evaluation determines the treatment degraded the brain, a single Cypher query (`MATCH (n {treatment_id: $tid}) DELETE n`) removes everything the treatment added. The brain returns to its pre-treatment topology.

This is all-or-nothing by design. We cannot selectively keep "good" nodes because determining which nodes helped requires content analysis, which violates the topology-only constraint. The transaction boundary is the entire treatment.

### From clinical trials: before/after measurement

The protocol captures a full BrainStats snapshot before any frequency is applied. After the observation window (caller-managed), it captures another snapshot. The evaluation compares 10+ weighted metrics between these two snapshots. The comparison is not a single score -- it is a weighted vote across structural, drive, and connectivity dimensions.

### From pharmacology: prescription logic

The `prescribe()` function encodes GraphCare's current clinical knowledge. Brain category (VOID, MINIMAL, SEEDED, STRUCTURED) determines the baseline prescription. Specific stats (typed_node_count, cluster_coefficient, frustration, curiosity, social_need) refine the selection. This is intentionally coarse -- refinement comes from analyzing treatment records over time.

---

## PRINCIPLES

### Principle 1: Measure Everything, Assume Nothing

A treatment applied without a before-snapshot is unmeasurable. The protocol structurally prevents this: `begin_treatment` always reads the brain topology before applying frequencies. There is no code path that applies a frequency without first capturing the baseline. This is not a convention -- it is an architectural invariant.

### Principle 2: Reversibility Is Non-Negotiable

Every frequency node carries a `treatment_id` tag. This tag exists solely for rollback. If the tag is missing, rollback cannot find the node. The invariant: every node created by the treatment protocol must carry `treatment_id`. The frequencies module enforces this in `apply_frequency()`.

### Principle 3: The Record Is the Treatment

A treatment that happened but was not recorded did not happen. The JSON record in `data/treatments/{citizen_id}/{treatment_id}.json` is the single source of truth. It contains the prescription, the before/after snapshots, the outcome, the rollback status. Any analysis of treatment efficacy starts and ends with these records.

### Principle 4: Degrade Nothing, or Undo Everything

The evaluation uses a weighted comparison. If degradation outweighs improvement, the entire treatment is rolled back. There is no "partial success" -- the treatment either helped or it is removed. This is conservative by design. A treatment that improved curiosity but degraded clustering is not a net win -- it changed the brain in ways we cannot fully evaluate with topology alone.

---

## BEHAVIORS SUPPORTED

- B1 (Full Lifecycle): snapshot -> prescribe -> apply -> observe -> snapshot -> evaluate -> rollback if degraded
- B2 (Weighted Evaluation): 10+ metrics compared with explicit weights; verdict derived from weighted vote
- B3 (Auto-Rollback): degradation triggers automatic removal of all treatment-tagged nodes
- B4 (Treatment Records): every treatment persisted as JSON with full before/after data
- B5 (Auto-Prescription): brain category and stats drive frequency selection when none specified

## BEHAVIORS PREVENTED

- A1 (Unmeasured intervention): no code path applies frequencies without snapshotting first
- A2 (Irreversible damage): treatment_id tagging guarantees rollback capability
- A3 (Lost history): every treatment produces a persistent record regardless of outcome
- A4 (Content access): frequencies operate on topology only; content/synthesis fields never touched

---

## DATA

| Source | Type | Purpose |
|--------|------|---------|
| Brain topology (via `read_brain_topology`) | GRAPH | Before/after snapshots for evaluation |
| Treatment records (`data/treatments/`) | JSON files | Persistent record of every treatment lifecycle |
| Brain graph (via FalkorDB) | GRAPH | Target for frequency application and rollback |
| Frequency catalog (`frequencies.py`) | CODE | Available intervention types and prescriptions |

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| `brain_topology_reader` | Provides `BrainStats` and `read_brain_topology()` for snapshotting |
| `frequencies` | Provides `Frequency`, `prescribe()`, `apply_frequency()`, `rollback_treatment()` |
| FalkorDB | Brain graphs live here; frequencies create nodes here; rollback deletes nodes here |

---

## SCOPE

### In Scope

- Full treatment lifecycle: begin (snapshot + prescribe + apply) and evaluate (snapshot + compare + rollback)
- Weighted metric comparison across 10+ structural and drive dimensions
- Auto-rollback of degrading treatments via treatment_id-tagged node deletion
- Auto-prescription based on brain category and stats
- Treatment record persistence as JSON per citizen per treatment
- Treatment listing per citizen

### Out of Scope

- Observation window timing -- the caller decides when to call `evaluate_treatment`
- Notification of outcomes -- other modules consume treatment records
- Content-level analysis of what changed -- topology only
- Multi-treatment interaction analysis -- each treatment is independent
- Treatment scheduling or recurrence -- future concern

---

## INSPIRATIONS

- **Database transactions (ACID)** -- atomicity via treatment_id tagging, rollback as first-class operation
- **Clinical trial methodology** -- baseline measurement, controlled intervention, post-intervention measurement, outcome recording
- **Pharmacological frequency** -- interventions that change reaction conditions without being consumed; the brain integrates or rejects the frequency through its own physics
- **Evidence-based medicine** -- treatment records accumulate into an evidence base that can refine prescriptions over time
