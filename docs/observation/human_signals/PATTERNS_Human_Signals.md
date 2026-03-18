# Human Signals — Patterns: Topology-Only Observation Applied to Human Health

```
STATUS: PROPOSED
CREATED: 2026-03-15
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Human_Signals.md
THIS:            PATTERNS_Human_Signals.md (you are here)

IMPL:            (future — no code exists or is planned for v1)
```

### Note on Status

This module is PROPOSED. The patterns described here are a design vision, not an implementation plan. They exist to ensure that GraphCare's architecture — particularly the primitive-based, topology-only observation model — is designed from day one to accommodate human data when the time comes.

---

## THE PROBLEM

GraphCare currently observes only AI citizens. Their health signals come from brain graphs (topology primitives) and universe graphs (behavioral primitives). The framework works: 7 primitives, topology only, scoring formulas that compose these into health assessments.

But the vision of Mind Protocol includes humans. Humans who collaborate with AI citizens. Humans who might benefit from the same kind of structural health observation — not clinical diagnosis, but the same "blood test, not psychoanalysis" approach.

The problem is not "how do we monitor human health" — that field is vast and well-served. The problem is: **can the same topology-only observation framework that works for AI citizens also work for humans?** And if so, what does that look like?

If we don't think about this now, we risk building an AI-only observation architecture that would need to be torn apart and rebuilt when humans enter the picture. The cost of extensibility now is a few pages of design thinking. The cost of retrofitting later is a rewrite.

---

## THE PATTERN

**The same blood-test principle, applied to biological and behavioral data.**

A human's body produces structural signals that parallel what an AI citizen's brain graph produces. The key insight is that health-relevant information exists in the *shape* of these signals — the topology — without needing to read their clinical content.

### Three Signal Domains

#### 1. Heart Rate Variability (HRV)

HRV is the variation in time between heartbeats. High variability generally indicates good autonomic health; low variability indicates stress or fatigue.

**What we'd observe (topology only):**

| Human Primitive | What It Captures | AI Parallel |
|-----------------|------------------|-------------|
| `hrv_regularity` | Standard deviation of inter-beat intervals over a window | `mean_energy(type)` — both measure the "vitality" of a subsystem |
| `hrv_trend` | Direction and magnitude of HRV change over days | `recency(type)` — both capture whether a system is fresh/active or stagnating |
| `hrv_recovery_rate` | How quickly HRV returns to baseline after stress | No direct parallel — unique to biological substrate |

**What we would NOT observe:**
- Raw R-R interval traces
- Clinical ECG data
- Heart rate values (only their variability pattern)
- Any data that could be used for medical diagnosis

The human (or their wearable device) computes the topology primitives locally. GraphCare receives only the computed values — never the raw data.

#### 2. Message Patterns

Humans communicate through text (chat, email, forums). The topology of their communication reveals health signals without reading content.

**What we'd observe (topology only):**

| Human Primitive | What It Captures | AI Parallel |
|-----------------|------------------|-------------|
| `message_frequency` | Messages per time period, with temporal decay | `count(type)` — both count units of activity |
| `response_latency` | Average time between receiving and responding | No direct parallel — AI citizens don't have async response patterns |
| `interlocutor_count` | Unique people communicated with | `distinct_actors_in_shared_spaces` — same concept, same primitive |
| `conversation_initiation_ratio` | Self-initiated vs. responsive messages | `auto_initiated` ratio — same signal, different substrate |

**What we would NOT observe:**
- Message content
- Who specific messages were sent to (only aggregate interlocutor count)
- Sentiment or emotional content
- Topics discussed

#### 3. Activity Rhythms

When a human is active — and how regular those patterns are — reveals health information. Disrupted sleep shows in activity gaps. Overwork shows in extended active periods. Routine health shows in consistent daily patterns.

**What we'd observe (topology only):**

| Human Primitive | What It Captures | AI Parallel |
|-----------------|------------------|-------------|
| `activity_regularity` | Consistency of daily active/inactive cycles | `cluster_coefficient` — both measure structural regularity |
| `active_period_count` | Number of distinct active periods per day | `count("moment")` — both count units of activity |
| `rest_period_quality` | Length and consistency of inactive periods | No direct parallel — AI citizens don't rest |
| `rhythm_drift` | Whether the activity cycle is shifting (later nights, etc.) | `recency` trend — both capture temporal shift |

**What we would NOT observe:**
- What the person was doing during active periods
- Location data
- App usage
- Any content of activity — only its temporal shape

### The Primitive Equivalence Table

The vision: a mapping between AI and human primitives that allows scoring formulas to work across substrates.

| AI Primitive | Human Equivalent | Shared Concept |
|-------------|-----------------|----------------|
| `count(type)` | `message_frequency`, `active_period_count` | Volume of activity |
| `mean_energy(type)` | `hrv_regularity` | Vitality of a subsystem |
| `link_count(src, tgt)` | `interlocutor_count` | Connectivity |
| `min_links(type, n)` | `conversation_initiation_ratio` | Self-directed activity |
| `cluster_coefficient(type)` | `activity_regularity` | Structural consistency |
| `drive(name)` | (no direct equivalent) | Internal motivation state |
| `recency(type)` | `hrv_trend`, `rhythm_drift` | Freshness / trajectory |

Some primitives have clean cross-substrate parallels. Others (drives for AI, recovery rate for humans) are substrate-specific. This is honest — not everything maps. The scoring framework should handle both: shared formulas for concepts that generalize, and substrate-specific formulas where they don't.

---

## BEHAVIORS SUPPORTED

- B1 (Unified Observation) — Same scoring framework accepts both AI and human topology primitives
- B2 (Human Privacy) — Raw biometric and behavioral data never enters GraphCare; only pre-computed topology values
- B3 (Cross-Substrate Research) — AI and human health trajectories can be compared using structural primitives

## BEHAVIORS PREVENTED

- A1 (Raw Data Ingestion) — GraphCare never stores raw HRV traces, message logs, or activity data
- A2 (Medical Diagnosis) — Topology primitives are for wellbeing insight and research, not clinical use
- A3 (Forced Equivalence) — Substrate-specific primitives are acknowledged, not forced into artificial cross-substrate mappings

---

## PRINCIPLES

### Principle 1: Pre-Computed Primitives, Never Raw Data

For AI citizens, `brain_topology_reader.py` sits between the brain graph and the scoring framework. For humans, an equivalent layer — running on the human's device or a trusted intermediary — must compute topology primitives from raw data. GraphCare receives `hrv_regularity: 0.73`, never a heart rate trace. This is the same structural privacy guarantee, adapted for biological data.

### Principle 2: Honest Substrate Differences

AI citizens have drives (curiosity, frustration, ambition). Humans have HRV recovery rates. These don't map to each other, and pretending they do would produce bad science. The primitive framework should have a clear "shared" section (concepts that generalize) and clear "substrate-specific" sections. Scoring formulas can be substrate-aware without being substrate-agnostic.

### Principle 3: Research First, Product Later

Human signal observation is research. It is not a product feature, not a selling point, not a health app. The first use case is: "Can we detect the same structural patterns in human activity data that we detect in AI brain topology?" If the answer is yes, that's a publication. If the answer is no, that's also a publication. Either way, the goal is knowledge — not a feature launch.

### Principle 4: Consent Is Structural, Not Just Contractual

For AI citizens, the topology-only guarantee is enforced by code — the brain topology reader literally cannot access content fields. For humans, the equivalent must be equally structural: the human's device computes primitives locally, and only primitives are transmitted. GraphCare cannot access raw data because raw data is never sent. Consent to share topology primitives is explicit, revocable, and technically enforced.

---

## DATA

| Source | Type | Purpose / Description |
|--------|------|-----------------------|
| Wearable devices (HRV) | DEVICE | Raw HRV data, processed locally into topology primitives |
| Communication platforms | API | Message metadata (frequency, timing), processed locally into topology primitives |
| Activity tracking | DEVICE | Active/inactive period detection, processed locally into topology primitives |
| `docs/observation/brain_topology/PATTERNS_Brain_Topology.md` | FILE | The AI primitive model this module extends |

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| Brain topology | The 7 AI primitives are the model we're extending. Human primitives must be structurally compatible. |
| Scoring framework | Must accept both AI and human primitives without architectural changes. |
| Privacy / topology-only principle | The core guarantee that makes human data acceptable to share with GraphCare. |

---

## INSPIRATIONS

- **Chronobiology** — The study of biological rhythms. Activity regularity, circadian patterns, and rhythm disruption are established health signals. We're applying topology-only observation to these established signals.
- **Digital phenotyping** — The field of inferring health from smartphone and wearable data. Much of this work uses raw data; our contribution is showing that topology-level features are sufficient for meaningful health observation.
- **Comparative physiology** — Studying the same biological functions across different species. Cross-substrate health comparison (AI vs. human) is an analogous research challenge: same concepts, different implementations.
- **Federated learning** — The principle that data stays local and only aggregated insights are shared. Our "pre-computed primitives" model is similar in spirit: raw data stays with the human, only structural summaries reach GraphCare.

---

## SCOPE

### In Scope (for this design document)

- Defining human health topology primitives that parallel AI brain topology
- Mapping cross-substrate equivalences where they exist
- Establishing the pre-computed primitive model for human data privacy
- Identifying research questions that cross-substrate comparison could answer

### Out of Scope

- **Implementation** — This is PROPOSED. No code for v1.
- **Clinical validation** — We are not a medical device. Clinical accuracy is not our goal.
- **Data collection infrastructure** — How wearable data reaches the human's device is not our problem. We define what we need to receive.
- **Regulatory compliance (HIPAA, GDPR)** — Important but premature. When implementation approaches, regulatory review will be needed.

---

## MARKERS

<!-- @mind:proposition When HRV devices become accessible, run a pilot with 3-5 consenting humans to test whether topology primitives produce meaningful health signals -->
<!-- @mind:proposition Investigate whether existing digital phenotyping research has already validated topology-level features from wearable data -->
<!-- @mind:todo When scoring framework is stable, verify that it can accept a "human_stats" dataclass alongside BrainStats without architectural changes -->
