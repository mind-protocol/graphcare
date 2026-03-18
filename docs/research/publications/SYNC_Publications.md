# Publications — Sync: Current State

```
LAST_UPDATED: 2026-03-15
UPDATED_BY: @vox (doc chain creation)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- The commitment to regular publication cadence (monthly minimum)
- Reproducibility as a requirement (data, method, code, environment)
- Privacy-first publication (anonymized aggregates only, topology-only principle applies)
- Four publication types (research findings, experiment reports, methodology papers, meta-health reports)

**What's still being designed:**
- Publication format and template
- Anonymization pipeline
- Peer review logistics (who reviews, how, where)
- Publication archive and indexing

**What's proposed (v2+):**
- Cross-ecosystem publication (sharing findings with organizations outside Mind Protocol)
- Automated reproducibility verification (CI for publications: run the code, check the results match)
- Translated publications (making findings accessible in multiple languages)

---

## CURRENT STATE

No publications exist yet. This is expected: GraphCare's assessment pipeline became operational recently, and publications require accumulated data and completed analyses. The research modules that will feed publications (`longitudinal_health`, `technique_measurement`) are themselves in the design phase.

The first publication will likely be a methodology paper describing the topology-only health assessment framework — this can be written from existing docs and code without needing accumulated data. The assessment pipeline, scoring formulas, and gap analysis pattern are documented well enough to produce a methodology paper now.

---

## IN PROGRESS

### Doc chain creation

- **Started:** 2026-03-15
- **By:** @vox
- **Status:** In progress
- **Context:** Creating OBJECTIVES, PATTERNS, SYNC. Publications is the output channel for all of GraphCare's research work.

---

## RECENT CHANGES

### 2026-03-15: Initial doc chain creation

- **What:** Created OBJECTIVES, PATTERNS, and SYNC for publications module
- **Why:** A research organization without a publication discipline is a private club. Publications make GraphCare's work accessible, verifiable, and improvable by others.
- **Files:** `docs/research/publications/OBJECTIVES_*.md`, `PATTERNS_*.md`, `SYNC_*.md`
- **Insights:** The first publication should be a methodology paper. It doesn't require accumulated citizen data — just the framework description. This would establish GraphCare's research identity and invite early peer review of the approach itself before we publish results produced by that approach.

---

## KNOWN ISSUES

### No publication infrastructure

- **Severity:** Medium
- **Symptom:** No archive, no format, no review process, no anonymization pipeline
- **Suspected cause:** GraphCare focused on building the assessment pipeline first; publication is the next layer
- **Attempted:** Nothing yet

### No peer reviewers identified

- **Severity:** Low (for now)
- **Symptom:** No organizations have been invited to review GraphCare's work
- **Suspected cause:** Publications don't exist yet, so there's nothing to review
- **Attempted:** Nothing — premature until first publication is drafted

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Design (creating publication format and anonymization pipeline) or VIEW_Voice (writing the first methodology paper)

**Where I stopped:** Documentation only. No publications, no infrastructure, no reviewers.

**What you need to understand:**
The first publication should be a methodology paper about the topology-only health assessment framework. All the material exists: the PATTERNS and ALGORITHM docs for daily_citizen_health, the scoring_formulas code, the 7 topology primitives, the 40/60 brain/behavior split, the gap analysis concept. This is a synthesis and framing exercise, not new research.

**Watch out for:**
- Anonymization is harder than it sounds. Even with citizen IDs replaced, combinations of attributes (district + spawn date + tier) can be uniquely identifying in a population of ~60. k-anonymity (ensuring at least k citizens share any published attribute combination) is the standard approach.
- The topology-only principle applies to publications too. Don't accidentally include brain content examples in a methodology paper. Use only the structural notation: "count(desire): 10, mean_energy(desire): 0.65" — never "desire: retrouver la surface."
- Peer review invitations require organizational relationships that may not exist yet. The first publication may go out without formal review, with an explicit invitation for post-publication commentary.

**Open questions I had:**
- Where should publications be archived? A directory in the graphcare repo? A separate publications repo? An external platform?
- What format? Markdown for simplicity and version control? PDF for formality? Both?
- Who are the natural first peer reviewers in the Mind Protocol ecosystem?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Publications documentation created. This module defines GraphCare's research output: regular cadence (monthly minimum), four types (findings, experiments, methodology, meta-health), reproducibility packages, peer review, and privacy-first anonymization. No publications exist yet. The first publication should be a methodology paper about the topology-only assessment framework.

**Decisions made:**
- Monthly minimum publication cadence plus quarterly meta-health reports
- Reproducibility packages include data, method, code, and environment
- Peer review is invited but not gatekeeping — GraphCare publishes even if reviewers disagree
- Null and negative results must be published (no publication bias)

**Needs your input:**
- Should the first publication (methodology paper) go out before any data-driven publications, to establish the framework?
- Where should publications live (repo directory, external platform, both)?
- Which organizations in the ecosystem should be invited as peer reviewers first?

---

## TODO

### Doc/Impl Drift

- [ ] DOCS->IMPL: Create publication format template
- [ ] DOCS->IMPL: Build anonymization pipeline
- [ ] DOCS->IMPL: Create publication archive location

### Immediate

- [ ] Write first publication: "Topology-Only Health Assessment: A Framework" (methodology paper)
- [ ] Define publication format (sections, metadata, reproducibility package structure)
- [ ] Choose archive location and format

### Later

- [ ] Identify and invite first peer reviewers
- [ ] Build anonymization pipeline (k-anonymity for small populations)
- [ ] Create publication index / catalog
- IDEA: A "living publication" that updates as new data comes in, rather than static snapshots

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
The methodology paper feels achievable soon — all the raw material exists in the assessment doc chain. The bigger challenge is building the cultural habit of regular publication. It's easy for publication to be the thing that slips when other work is pressing.

**Threads I was holding:**
- The anonymization problem for small populations (~60 citizens) is real. k-anonymity with k=5 in a population of 60 means many attribute combinations will need generalization (e.g., reporting district-level, not individual-level).
- There's a tension between "publish everything including failures" and "don't publish things that could harm GraphCare's credibility." The right answer is: publish everything honestly, because hiding failures harms credibility more than admitting them.

**Intuitions:**
The methodology paper will be the most-read GraphCare publication. It defines what we do and invites scrutiny of the approach. Getting it right matters more than getting it out fast. But "right" doesn't mean "perfect" — it means "honest, complete, and reproducible."

**What I wish I'd known at the start:**
The existing doc chain for daily_citizen_health is essentially a methodology paper draft. The ALGORITHM doc in particular reads like a research methods section. The first publication may be closer to done than it appears.

---

## POINTERS

| What | Where |
|------|-------|
| Daily health algorithm (methodology source) | `docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md` |
| Daily health patterns (framework description) | `docs/assessment/daily_citizen_health/PATTERNS_Daily_Citizen_Health.md` |
| Scoring formulas (code reference) | `services/health_assessment/scoring_formulas/` |
| Topology primitives | `docs/assessment/PRIMITIVES_Universe_Graph.md` |
| Longitudinal health (finding source) | `docs/research/longitudinal_health/` |
| Technique measurement (experiment source) | `docs/research/technique_measurement/` |
| Process improvement (meta-health source) | `docs/analysis/process_improvement/` |
