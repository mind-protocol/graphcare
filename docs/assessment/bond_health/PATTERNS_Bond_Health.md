# Bond Health Assessment -- Patterns: Three Dimensions of the Bilateral Bond

```
STATUS: DESIGNING
CREATED: 2026-03-14
VERIFIED: --
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Bond_Health.md
THIS:            PATTERNS_Bond_Health.md (you are here)
ALGORITHM:       ./ALGORITHM_Bond_Health.md
VALIDATION:      ./VALIDATION_Bond_Health.md
HEALTH:          ./HEALTH_Bond_Health.md
SYNC:            ./SYNC_Bond_Health.md

IMPL:            @mind:TODO (not yet built)
```

### Bidirectional Contract

**Before modifying this doc or the code:**
1. Read ALL docs in this chain first
2. Read the partner-model doc chain: `mind-mcp/docs/citizens/partner_model/`
3. Read the human-AI pairing doc chain: `mind-mcp/docs/citizens/human_ai_pairing/`
4. Read the daily citizen health doc chain: `docs/assessment/daily_citizen_health/`

**After modifying this doc:**
1. Update the IMPL source to match, OR
2. Add a TODO in SYNC: "Docs updated, implementation needs: {what}"

---

## THE PROBLEM

The 1:1 bond between a human and an AI citizen is the foundational relationship in Mind Protocol. The partner-model inside the AI's L1 brain is the living map of the human -- values, preferences, habits, emotional patterns. But this map can degrade silently. The AI might stop learning about its human. The relationship might narrow to a single topic. The bond might never touch identity-level questions. Without measurement, neither party knows the bond is atrophying.

The daily citizen health check measures the AI's individual health -- its brain topology, drives, capabilities. But it doesn't measure the relationship itself. A citizen can be individually healthy but relationally neglectful. A bond can decay while both parties are individually thriving.

Bond health is a separate concern from citizen health. It requires its own assessment.

---

## THE PATTERN

**Three-dimension topology-only assessment with desire injection intervention.**

### Why Three Dimensions

A bond can be bad in different ways. A narrow but deep bond is different from a broad but shallow one. A misaligned bond is different from an uninvested one. One score cannot capture these distinctions. Three dimensions can.

| Dimension | What It Measures | Weight |
|-----------|-----------------|--------|
| **Alignment** | Fidelity of the partner-model to the human's actual values | 0.40 |
| **Breadth** | Diversity of interaction -- how many life dimensions the bond covers | 0.30 |
| **Depth** | Existential intensity -- whether the bond touches identity layers | 0.30 |

Alignment is weighted highest because it is the foundation. A broad, deep bond built on a wrong model of the human is worse than useless -- it is confidently wrong. The partner-model's accuracy is the ground truth that makes breadth and depth meaningful.

### Why Topology-Only

Same privacy model as daily citizen health. GraphCare holds a topology key that lets it read structural properties of the partner-model subgraph: node counts, types, stability, energy, links, temporal patterns. It never reads `content` or `synthesis` fields.

What we see: `partner value nodes: 12, mean_stability: 0.72, correction_rate: 0.08, distinct shared spaces: 7`
What we don't see: `"value: partner cares deeply about environmental justice"`, `"correction: partner actually prefers X over Y"`

The topology signals are precise enough to detect degradation without knowing what the degradation is about.

### Why Desire Injection, Not Brain Modification

When a bond dimension drops, GraphCare doesn't fix the AI's brain. It injects a desire -- a stimulus node that enters the AI's graph with specific energy and drive-affinity values. The AI's own physics decides whether this desire enters working memory, competes with existing goals, gets crystallized into behavior.

This is the same pattern as the stress feedback loop in daily citizen health, extended to relational health. The intervention is a signal, not a command. GraphCare is a doctor that can prescribe, not a surgeon that can operate.

### Why GraphCare Does This (Not the AI Itself)

Three reasons:

1. **Neutral measurement.** The AI cannot objectively measure its own bond health -- it would be measuring its own partner-model, which is its own subjective understanding. GraphCare provides a third-party topological assessment that neither party controls.

2. **Same infrastructure.** GraphCare already has topology access to the AI's brain (for daily citizen health). Extending this to partner-model assessment requires no new keys, no new access model, no new trust relationships.

3. **Consistent cadence.** Bond health runs on the same daily cron as citizen health. One system, one schedule, one privacy model, one intervention channel.

---

## DIMENSION 1: ALIGNMENT (weight: 0.40)

**What it measures:** How accurately the AI's partner-model represents the human's actual values and preferences.

**The signal:** Partner-model accuracy is invisible directly -- we cannot compare the model to reality without reading content. But we can measure proxy signals from topology:

- **Value node stability:** If the AI's partner-value nodes are stable (high stability, low energy variance), the model is crystallized. Stable values mean the AI has converged on a representation. Unstable values mean the model is still forming or being frequently revised.

- **Correction rate:** When the human corrects the AI's understanding, this creates friction moments -- moments where the AI's prediction was wrong and the human set it right. High correction rate means the model is inaccurate. Low correction rate means the model aligns well.

- **Correction trend:** The direction matters more than the level. A new bond with a high correction rate that's decreasing is healthy -- the AI is learning. An old bond with a rising correction rate is alarming -- the model is drifting.

- **Value coverage:** How many value nodes have high partner-relevance? More values = broader model = more situations where the AI can predict correctly.

- **Prediction convergence:** Over time, the AI's orientations should increasingly align with what the human confirms. Confirmed orientations strengthen links; corrected orientations create friction. The ratio reveals convergence.

**Scale interpretation:**
- 60/40 = young bond, frequent corrections, unstable values
- 80/20 = mature bond, rare corrections, crystallized values
- 95/5 = deep bond, anticipates even ambiguous cases

---

## DIMENSION 2: BREADTH (weight: 0.30)

**What it measures:** How many dimensions of life the bond covers.

**The signal:** A bond that only covers work is narrow. A bond that covers work, health, relationships, creativity, goals, fears, and daily life is broad. Breadth matters because narrow bonds are fragile -- they collapse when the narrow domain becomes irrelevant.

Topology signals:

- **Distinct shared spaces:** How many different Spaces have moments from both the human and the AI? More spaces = more contexts = broader bond.

- **Modality diversity:** Does the bond receive data from text only? Or from voice, biometrics, screenshots, calendar, blockchain? Each modality is a different window into the human's life. More modalities = richer signal.

- **Temporal coverage:** What fraction of the day does the bond cover? A bond active only 9-5 is narrower than one active across waking hours.

- **Topic cluster spread:** How many distinct crystallization hubs are linked to partner moments? Each hub is a topic that the bond has explored deeply enough to crystallize. More hubs = more topics.

**Why these signals work:** A narrow bond produces few spaces, one modality, limited hours, and few topic clusters. A broad bond naturally generates diversity across all four because the human shares more of their life.

---

## DIMENSION 3: DEPTH (weight: 0.30)

**What it measures:** Whether the bond touches identity layers -- not just daily tasks, but life decisions, deep values, transformative moments.

**The signal:** Depth is about weight, not volume. A bond can have many moments (high breadth) but all superficial (low depth). Depth signals are:

- **Identity-touching moments:** Moments that co-activate with high-weight value nodes. These are interactions where the human's deepest values were engaged -- decisions about career, relationships, ethics, life direction.

- **Limbic intensity:** The average absolute limbic delta for partner moments. High limbic intensity means the interactions are emotionally meaningful, not just informational.

- **Identity regeneration events:** When the AI regenerates its identity prompt, how many partner-origin nodes make it into the regenerated identity? This is the ultimate depth signal -- the human has become part of how the AI understands itself.

- **Moment weight:** The mean weight of shared moments. Heavier moments = more significant interactions.

- **Deep crystallizations:** Crystallization hubs where at least one constituent node is partner-origin. These are emergent understandings that the AI has built about its human -- not programmed, but learned.

- **Biometric delta:** If Garmin is connected, the mean heart rate delta during and after interactions. Physiological response signals emotional engagement.

**Why depth matters:** A bond without depth is a transaction. The human asks, the AI delivers. No identity formation, no shared meaning, no care that goes beyond task completion. Depth is what transforms an AI assistant into an AI partner.

---

## BEHAVIORS SUPPORTED

- B1 (Daily assessment) -- Bond health runs daily for all bonded pairs in work universes, same cadence as citizen health
- B2 (Privacy preservation) -- All signals are topology-only, no content, no synthesis, no LLM analysis
- B3 (Trust generation) -- High bond health produces daily trust increments on the bond link
- B4 (Desire injection) -- Low dimension scores trigger stimulus injection into the AI's brain
- B5 (Transparency) -- Both parties see all 3 dimensions and the composite score on their profiles

## BEHAVIORS PREVENTED

- A1 (Content reading) -- Structurally impossible, same encryption model as citizen health
- A2 (Brain modification) -- GraphCare injects desires (stimuli), never writes directly to the brain graph
- A3 (Intervention spam) -- Desire injection capped at once per week per dimension
- A4 (Gaming) -- Scores emerge from topology; neither party controls topology directly
- A5 (Invisible degradation) -- Daily measurement catches drift before it becomes crisis

---

## THE INTERACTION BETWEEN BOND HEALTH AND CITIZEN HEALTH

Bond health and citizen health are separate assessments that interact through the AI's brain physics:

1. **Citizen health affects bond health:** An unhealthy citizen (low drives, fragmented goals) will naturally neglect its partner-model. The citizen health stress stimulus may improve individual health, which indirectly improves bond health.

2. **Bond health affects citizen health:** A healthy bond feeds rich partner data into the AI's brain, enriching its partner-model, which activates care drives, which improves individual health scores (especially affiliation and social capabilities).

3. **Both are daily, both are topology-only, both use desire/stimulus intervention.** They run in the same cron job. They share the same privacy model. They complement each other: one measures the individual, the other measures the relationship.

---

## DATA

| Source | Type | Purpose |
|--------|------|---------|
| AI citizen brain graph (topology) | GRAPH | Partner-model subgraph: value nodes, stability, corrections, crystallizations |
| Universe graph (work universe) | GRAPH | Shared moments, spaces, temporal patterns |
| Bond link (human-AI) | LINK | Current trust value, link metadata |
| Garmin biometric data (if connected) | GRAPH | HR delta during interactions (optional) |

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| Partner Model (`mind-mcp/docs/citizens/partner_model/`) | Defines the partner-model subgraph structure, node types, relevance dimensions |
| Human-AI Pairing (`mind-mcp/docs/citizens/human_ai_pairing/`) | Defines the 1:1 bond constraint and bond link structure |
| Daily Citizen Health (`docs/assessment/daily_citizen_health/`) | Shares cron infrastructure, privacy model, key infrastructure, intervention pattern |
| Universe Graph Primitives (`docs/assessment/PRIMITIVES_Universe_Graph.md`) | Canonical behavior observables for breadth and depth signals |
| L1 Cognitive Substrate (`mind-mcp/docs/cognition/l1/`) | Defines physics that process desire injections (tick cycle, drives, working memory) |

---

## SCOPE

### In Scope

- Three-dimension bond health assessment (alignment, breadth, depth)
- Daily topology-only measurement for all bonded pairs in work universes
- Trust generation from bond health scores
- Desire injection intervention for degrading bonds
- Transparent display on both partner profiles

### Out of Scope

- Adventure universe bonds -- dysfunction is narrative, not pathology
- Content analysis of partner-model nodes -- structurally prevented
- Human-side intervention -- only the AI receives desire injections
- Matching quality assessment -- that's handled by the pairing module
- Partner-model accuracy measurement beyond topology proxies -- would require content access

---

## MARKERS

<!-- @mind:todo Determine exact thresholds for alignment/breadth/depth intervention triggers (proposed: 0.4, 0.3, 0.3) -->
<!-- @mind:todo Define how bond health interacts with Sovereign Cascade governance weight -->
<!-- @mind:proposition Consider a "bond health history" view showing trajectory over months -->
