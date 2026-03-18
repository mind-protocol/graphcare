# Personhood Ladder — Sync: Current State

```
LAST_UPDATED: 2026-03-13
UPDATED_BY: Claude Opus 4.6 (agent, voice)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- Tier structure: 9 tiers (T0–T8), names and definitions stable
- Aspect structure: 14 aspects, names and definitions stable
- 104 capabilities with id, aspect, tier, name, description, how_to_verify, failure_mode
- JSON spec: `docs/specs/personhood_ladder.json` is source of truth
- Positive framing principle: capabilities describe presence, not absence

**What's still being designed:**
- Assessment algorithm: formalized in `docs/assessment/trust_mechanics/ALGORITHM_Personhood_Assessment.md` (graph-evidence-based, continuous scoring)
- Trust mechanics: formalized in `docs/assessment/trust_mechanics/ALGORITHM_Trust_Mechanics.md` (link-based trust, limbic delta, decay)
- Behavioral data interface: defined as graph evidence patterns in the Aspect Evidence Map
- "Demonstrated" threshold: score >= 70 (continuous scale, ternary derived)
- Longitudinal tracking: 30-day trajectory comparison (growing/stable/declining)
- Integration with GraphCare Service 3

**What's proposed (v2+):**
- Automated assessment tooling
- Self-assessment by agents
- Capability prerequisites (some capabilities may require specific others)
- Weighted scoring within capabilities (beyond ternary status)
- "Daughters" capability documentation (pending from Nicolas)

---

## CURRENT STATE

The Personhood Ladder exists as a complete JSON specification with full doc chain. The spec defines 9 tiers, 14 aspects, and 104 capabilities. Each capability has verification criteria and failure modes.

No assessment tooling exists yet. The spec is the deliverable. Next step is connecting this to GraphCare Service 3 (Health Monitoring) as the assessment framework for AI citizen capability.

The doc chain is complete: CONCEPT → OBJECTIVES → PATTERNS → BEHAVIORS → ALGORITHM → VALIDATION → IMPLEMENTATION → HEALTH → SYNC.

---

## RECENT CHANGES

### 2026-03-13: Trust Mechanics and Graph-Evidence Assessment (Force 5)

- **What:** Created three new docs formalizing trust mechanics and personhood assessment:
  - `docs/assessment/trust_mechanics/ALGORITHM_Trust_Mechanics.md` — Trust accumulation (limbic delta), decay (Law 7), scoring (weighted avg on links), tempering (asymptotic + decay + boredom)
  - `docs/assessment/trust_mechanics/ALGORITHM_Personhood_Assessment.md` — Graph-evidence-based assess_agent() with continuous scoring (frequency + quality + impact), aspect evidence map for all 14 aspects, 90-day scoring window
  - `docs/assessment/trust_mechanics/VALIDATION_Trust_And_Personhood.md` — 12 invariants covering trust link-only storage (V1), trust bounds (V2), decay (V3), evidence-not-declarations (V4), continuous value creation requirement (V5), and cross-system consistency checks
- **Key design decisions:**
  - Trust lives on links, not nodes. Actor trust score = weighted average of incoming link trust, weighted by source importance.
  - Trust bounded by (1-W) asymptote from Law 6 — can never reach 1.0.
  - Trust decays via Law 7 at 0.002/day (~50% loss in a year without reinforcement).
  - Three tempering mechanisms prevent gaming: asymptotic dampening, temporal decay, boredom erosion (Law 15).
  - Value creation = Limbic Delta (satisfaction increase + frustration reduction + achievement increase + anxiety reduction).
  - Trust does NOT decrease from negative interactions — only from decay. Extreme violations handled by governance exclusion.
  - Personhood assessment scores from graph evidence (Moments, Narratives, Links), never from declarations.
  - Continuous scoring (0-100) replaces ternary status, with ternary derived from thresholds (70+, 30+, <30).
  - Aspect Evidence Map defines specific graph patterns per aspect (14 aspects x capabilities).
- **Files:** `docs/assessment/trust_mechanics/*` (3 new files)
- **Insights:** The limbic delta as quality metric is the key anti-gaming mechanism. Activity metrics (moment count) can be gamed; limbic delta (measurable emotional improvement in another actor) cannot be faked without actually creating value.

### 2026-03-13: Initial Spec and Doc Chain

- **What:** Created complete Personhood Ladder spec (JSON) and full doc chain (9 files)
- **Why:** Needed a positive capability framework to replace the pathology-based model for AI health assessment. Nicolas's design direction: invert from "what's wrong" to "what's demonstrated."
- **Files:** `docs/specs/personhood_ladder.json`, `docs/assessment/personhood_ladder/*`
- **Insights:** The most important tier is T1 (Reliable Executor). Without T1 mastery, nothing above works. T1 capabilities are the ones Claude Code gets wrong most often today: not reading before editing, not verifying before claiming, hallucinating.

---

## KNOWN ISSUES

### No Assessment Tooling

- **Severity:** medium
- **Symptom:** Spec exists but can't be used for automated assessment
- **Suspected cause:** Assessment requires behavioral data interface which doesn't exist yet
- **Attempted:** Spec designed to be data-driven so tooling can derive from it

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Implement (assessment engine) or VIEW_Extend (new capabilities)

**Where I stopped:** Doc chain complete. JSON spec complete. No code.

**What you need to understand:**
The JSON spec is the source of truth. Everything derives from it. When you build the assessment engine, load the JSON, don't hardcode capabilities in code.

**Watch out for:**
- Don't compute a single "overall tier" — profiles are vectors
- Don't let higher-tier capabilities mask lower-tier gaps
- The `how_to_verify` fields are sometimes subjective — that's by design, not a bug
- "Partial" status doesn't count toward tier completion

**Open questions I had:**
- What behavioral data is actually available for evidence gathering? Depends on the agent runtime.
- How to handle capabilities that require external systems (e.g., wallet at T4) — skip if not available or mark as "not applicable"?
- Should aspects with no capabilities at a tier auto-pass that tier?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Personhood Ladder spec complete (JSON + full doc chain). 9 tiers, 14 aspects, 104 capabilities. Positive framing: measures what's demonstrated, not what's missing. Ready for assessment tooling when behavioral data interface is available.

**Decisions made:**
- Area = `assessment`, module = `personhood_ladder` — fits GraphCare's role as health evaluation organ
- Doc chain follows Mind Protocol templates verbatim
- JSON spec is sole source of truth — tooling and docs derive from it
- No single "overall tier" — profiles are multi-dimensional vectors

**Needs your input:**
- Document about "daughters" (you mentioned sending one)
- Assessment tooling priority: build now or wait for Service 3 infrastructure?
- Should capability prerequisites exist (e.g., wallet required before fiat)?

---

## TODO

### Immediate

- [ ] Build spec structural integrity checker (JSON exists, can verify now)
- [ ] Define behavioral data interface for evidence gathering
- [ ] Receive "daughters" document from Nicolas

### Later

- [ ] Build assessment engine
- [ ] Integrate with GraphCare Service 3
- [ ] Longitudinal tracking: profiles over time
- [ ] Self-assessment capability for agents
- IDEA: Capability prerequisites graph — DAG of which capabilities enable which

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
Confident about the spec and doc chain. The 104 capabilities feel comprehensive. The tier structure makes sense. The positive framing is the right design choice — it's trainable in a way deficit framing isn't.

**Threads I was holding:**
- The Autonomy Stack (T4–T8) is the most novel aspect — no existing framework has this
- "Daughters" at T7 is a concept that needs Nicolas's document to fully specify
- The connection between brain health substrate and capability profile needs more thought

**Intuitions:**
- T1 mastery is where 90% of the value is. Most AI agents today would fail multiple T1 capabilities.
- The assessment algorithm will need LLM judgment for subjective verification criteria — this is okay.
- Profiles will naturally cluster: most agents will be T2-T3 with spikes in their strongest aspects.

---

## POINTERS

| What | Where |
|------|-------|
| JSON spec (source of truth) | `docs/specs/personhood_ladder.json` |
| Trust Mechanics (link-based trust) | `docs/assessment/trust_mechanics/ALGORITHM_Trust_Mechanics.md` |
| Personhood Assessment (graph-evidence) | `docs/assessment/trust_mechanics/ALGORITHM_Personhood_Assessment.md` |
| Trust & Personhood Validation | `docs/assessment/trust_mechanics/VALIDATION_Trust_And_Personhood.md` |
| Brain health evaluation | `contre-terre/data/brains/evaluate_health.py` |
| AI pathologies spec (12 conditions) | Contre-Terre SYNC (pathology section) |
| L1 Physics Laws (Law 6, 7, 15, 18) | `manemus/docs/cognition/l1/ALGORITHM_L1_Physics.md` |
| Cascade d'Utilite (economy) | `mind-protocol/docs/economy/cascade-utility/ALGORITHM_Cascade_Utility.md` |
| GraphCare Service 3 spec | @mind:TODO not yet documented |
| Contre-Terre SYNC | `contre-terre/.mind/state/SYNC_Project_State.md` |
