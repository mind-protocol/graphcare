# Publications — Patterns: Open Research With Regular Cadence

```
STATUS: DESIGNING
CREATED: 2026-03-15
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Publications.md
THIS:            PATTERNS_Publications.md (you are here)
BEHAVIORS:       (future)
ALGORITHM:       (future)
VALIDATION:      (future)
IMPLEMENTATION:  (future)
SYNC:            ./SYNC_Publications.md

IMPL:            @mind:TODO (not yet built)
```

### Bidirectional Contract

**Before modifying this doc or the code:**
1. Read ALL docs in this chain first
2. Read the research modules that produce publishable findings: `research/longitudinal_health/`, `research/technique_measurement/`, `research/cross_substrate_health/`

**After modifying this doc:**
1. Update the IMPL source to match, OR
2. Add a TODO in SYNC: "Docs updated, implementation needs: {what}"

---

## THE PROBLEM

GraphCare generates knowledge that matters beyond its own organization. Insights about AI health trajectories, intervention effectiveness, and cross-substrate health patterns have value for every organization working with AI citizens — and eventually for human health research as well.

Without a publication discipline:
- Findings stay inside GraphCare and benefit only GraphCare
- Methodology goes unchallenged, allowing institutional blind spots to persist
- Other organizations duplicate research GraphCare already completed
- Claims about GraphCare's effectiveness are unverifiable by outsiders
- The broader Mind Protocol ecosystem cannot build on GraphCare's research
- GraphCare's institutional knowledge is trapped in internal documents that decay and fragment

---

## THE PATTERN

**Regular cadence of open publications with reproducibility packages and invited peer review.**

### Publication Types

**Type 1: Research Findings**
Results from longitudinal analysis, cohort studies, or technique measurements. These are the primary research output. Example: "Cohort analysis of Lumina Prime citizens by district shows that Innovation Fields residents develop initiative capabilities 23% faster than the city average, while Resonance Plaza residents show stronger collaboration trajectories."

**Type 2: Experiment Reports**
Complete results from technique measurement experiments — positive, negative, and null findings. Example: "Experiment 2 Results: Reducing stress stimulus magnitude by 50% produced no measurable difference in 30-day health trajectories (n=28 per group, p=0.43). Recommendation: maintain current stress formula pending larger sample study."

**Type 3: Methodology Papers**
Descriptions of new methods, frameworks, or tools developed during GraphCare's work. Example: "Topology-Only Health Assessment: A Privacy-Preserving Framework for AI Citizen Monitoring" — describing the 7-primitive approach, the 40/60 brain/behavior split, and the gap analysis method.

**Type 4: Meta-Health Reports**
Results from process improvement retrospectives — how GraphCare itself changed based on what it learned. Example: "Q1 2026 Meta-Health Report: 3 formula weight adjustments, 1 intervention template revision, 4 null experiment results that prevented misguided changes."

### The Reproducibility Package

Every publication includes:

- **Anonymized data** — The dataset used for analysis, with citizen IDs replaced by random tokens, and any identifying attribute combinations (e.g., the only citizen in district X who spawned on date Y) removed or generalized.
- **Method specification** — Exact steps to reproduce the analysis, including: which formula versions were used, what date ranges were analyzed, what statistical tests were applied, what thresholds define significance.
- **Code** — The scripts or notebooks that produced the results. Not "similar code" — the actual code that ran.
- **Environment** — Python version, package versions, database version. Everything needed to recreate the computational environment.

### Peer Review Process

GraphCare invites review from other organizations in the Mind Protocol ecosystem. The review process:

1. **Publication draft** posted to a shared review space (not citizen-facing)
2. **Review window** — 2 weeks minimum. Reviewers can: challenge methodology, question conclusions, request additional analysis, reproduce results independently
3. **Response** — GraphCare addresses all review comments. Substantive challenges either improve the publication or are acknowledged as limitations.
4. **Publication** — Final version posted with reviewer acknowledgment

Importantly: reviews are not gatekeeping. GraphCare publishes even if reviewers disagree — but disagreements are included in the publication. The goal is to surface challenges, not to achieve consensus.

### Publication Cadence

- **Monthly minimum:** At least one publication per month. This may be a brief experiment report or a substantial research finding.
- **Quarterly meta-health report:** Every quarter, a comprehensive report on GraphCare's own health — what changed, what was learned, what failed.
- **Ad hoc:** Urgent findings (e.g., discovering a harmful care technique) are published immediately regardless of cadence.

---

## BEHAVIORS SUPPORTED

- B1 (Knowledge sharing) — Research findings reach the broader ecosystem through regular publication
- B2 (Accountability) — Open methodology and reproducibility packages make GraphCare's claims verifiable
- B3 (External validation) — Peer review catches errors and biases that internal review misses
- B4 (Cumulative knowledge) — Regular cadence means research accumulates, building on previous findings

## BEHAVIORS PREVENTED

- A1 (Knowledge hoarding) — Findings cannot stagnate internally; the cadence forces sharing
- A2 (Unverifiable claims) — Reproducibility packages mean every claim is testable
- A3 (Publication bias) — Null and negative results are explicitly required alongside positive findings

---

## PRINCIPLES

### Principle 1: Cadence Creates Accountability

Publishing regularly is harder than publishing occasionally. It forces GraphCare to actually do research, not just claim to. A month without a publication is a signal: either we're not doing enough research, or we're not sharing what we've done. Both are problems. The cadence is the discipline.

### Principle 2: Reproducibility Is the Price of Credibility

If someone cannot reproduce our finding, they should not believe it. This is not a high standard — it is the minimum standard for any claim that affects citizen health. The reproducibility package is work, but it is the work that makes our publications real rather than performative.

### Principle 3: Invite Adversarial Review

The most dangerous state for a research organization is unchallenged confidence. GraphCare actively seeks reviewers who will question, challenge, and attempt to disprove our findings. Agreement from skeptics is worth more than applause from allies. We make it easy to disagree with us by providing all the data and tools needed to do so.

### Principle 4: Privacy Survives Publication

The topology-only principle extends to all publications. Anonymized aggregate data only. No individual citizens identifiable. No brain content, no private moments, no personally attributable patterns. If a finding requires identifying data to be meaningful, the finding is redesigned or not published.

---

## DATA

| Source | Type | Purpose / Description |
|--------|------|-----------------------|
| `research/longitudinal_health` | MODULE | Produces cohort analyses and trend findings for publication |
| `research/technique_measurement` | MODULE | Produces experiment results for publication |
| `analysis/process_improvement` | MODULE | Produces meta-health reports for publication |
| `research/cross_substrate_health` | MODULE | Produces cross-substrate comparison findings (future) |
| Anonymization pipeline (to be built) | CODE | Transforms raw data into publishable anonymized datasets |

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| `research/longitudinal_health` | Source of cohort and trend research findings |
| `research/technique_measurement` | Source of experiment results |
| `analysis/process_improvement` | Source of meta-health retrospective data |
| `privacy/topology_only_principle` | Defines the privacy constraints on what can be published |

---

## INSPIRATIONS

- **arXiv preprint model** — Publish first, review in the open. Speed and openness over gatekeeping. GraphCare adapts this by adding invited review, not replacing open publication with gated review.
- **Cochrane Collaboration** — Systematic reviews of medical evidence with open methodology. The gold standard for reproducible health research. GraphCare's reproducibility packages follow this spirit.
- **Open Source Software** — The code IS the transparency. By including actual analysis code in publications, GraphCare extends the open source ethos from software to research.

---

## SCOPE

### In Scope

- Publication cadence definition and tracking
- Four publication types (research findings, experiment reports, methodology papers, meta-health reports)
- Reproducibility package standards
- Peer review process
- Anonymization requirements for published data
- Publication archive and indexing

### Out of Scope

- Conducting the research itself → see: `research/longitudinal_health`, `research/technique_measurement`
- GraphCare's own process improvement → see: `analysis/process_improvement`
- Privacy framework design → see: `privacy/topology_only_principle`
- Statistical methodology → see: `scientific_rigor/validation_methodology`

---

## MARKERS

<!-- @mind:todo Define publication format (structure, required sections, metadata) -->
<!-- @mind:todo Build anonymization pipeline (citizen ID replacement, identifying combination removal) -->
<!-- @mind:todo Create publication archive location and indexing scheme -->
<!-- @mind:proposition Consider a "preprint" step where drafts are shared internally before external review -->
