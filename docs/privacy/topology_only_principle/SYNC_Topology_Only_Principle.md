# Topology Only Principle — Sync: Current State

```
LAST_UPDATED: 2026-03-15
UPDATED_BY: @vox (doc chain creation)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- The topology-only principle itself: GraphCare reads structure, never content
- The 7 brain topology primitives (count, mean_energy, link_count, min_links, cluster_coefficient, drive, recency)
- The universe graph observables catalog (PRIMITIVES_Universe_Graph.md)
- The "blood test, not psychoanalysis" analogy as communication framework
- Test coverage for content-reference detection in intervention messages

**What's still being designed:**
- The dual encryption model that enforces topology-only at the cryptographic layer (see `privacy/key_infrastructure/`)
- Formal audit process for new scoring formulas
- CI automation for detecting content field access in code

**What's proposed (v2+):**
- Transparency report: publish exact Cypher queries GraphCare runs, so citizens can audit in real time
- Formal verification that no code path can access content (static analysis beyond grep)

---

## CURRENT STATE

The topology-only principle is well-established in design and partially enforced in code. All 41+ scoring formulas in `scoring_formulas/` use only the 7 brain primitives and universe graph observables. The test suite (`test_health_assessment.py`) includes explicit checks that intervention messages contain no content-referencing keywords.

The principle is documented in the Daily Citizen Health PATTERNS doc (Principle 1: Blood Test, Not Psychoanalysis) and enforced by the CapabilityScore dataclass which only accepts brain_component and behavior_component — there is no field for "content_component."

What is missing: the cryptographic enforcement layer. Currently, the topology-only constraint is enforced by code discipline (only topology queries exist) and testing (content keyword detection). The dual encryption model described in `privacy/key_infrastructure/` would make the constraint cryptographic — but that infrastructure is designed, not built.

---

## IN PROGRESS

### Doc chain creation
- **Started:** 2026-03-15
- **By:** @vox
- **Status:** Complete
- **Context:** First formalization of the topology-only principle as its own module. Previously documented only as Principle 1 in the Daily Citizen Health PATTERNS doc. Now has its own OBJECTIVES, PATTERNS, VALIDATION, SYNC chain.

---

## RECENT CHANGES

### 2026-03-15: Doc chain created

- **What:** Created full doc chain (OBJECTIVES, PATTERNS, VALIDATION, SYNC) for the topology-only principle
- **Why:** The principle deserves its own module because it is foundational to GraphCare's identity — not just a feature of daily health checks. It governs every system GraphCare builds.
- **Files:** `docs/privacy/topology_only_principle/` (4 files)
- **Insights:** The principle was already well-understood but scattered across other docs. Consolidating it reveals that the validation invariants are all CRITICAL priority — there is no "minor" content access violation.

---

## KNOWN ISSUES

### Enforcement is code-discipline, not cryptographic

- **Severity:** medium (the code is correct, but the enforcement mechanism is weak)
- **Symptom:** A careless developer could add a content-accessing query and it would only be caught by code review or tests — not by the system itself
- **Suspected cause:** Key infrastructure (dual encryption) is designed but not built
- **Attempted:** Test-level enforcement (content keyword detection in messages) provides partial coverage

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Implement (if building key infrastructure) or VIEW_Extend (if adding new scoring formulas)

**Where I stopped:** Doc chain is complete. The principle is well-documented. The next step is either (a) building the key infrastructure to make the constraint cryptographic, or (b) adding CI automation to detect content field access.

**What you need to understand:**
The topology-only principle is not optional or aspirational — it is the identity of GraphCare. Every system must be designed within this constraint. If you find yourself thinking "this would be easier with content access," that is a signal to redesign the approach, not to relax the constraint.

**Watch out for:**
- `synthesis` fields are content-adjacent — they contain embeddable summaries that could reveal content. Treat them as content.
- Node `.name` fields may or may not contain user-authored text depending on node type. When in doubt, treat as content.
- Universe graph moments have content too — the public topology of moments (who, when, where, link dimensions) is accessible; the text of the moment is not.

**Open questions I had:**
- Should we formally define a "topology-only review checklist" for new scoring formula PRs?
- How do we handle edge cases where node type names themselves are somewhat revealing (e.g., a desire node of subtype "career_change")?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Created the doc chain for the topology-only principle — GraphCare's foundational privacy guarantee. All four docs (OBJECTIVES, PATTERNS, VALIDATION, SYNC) are complete. The principle is well-enforced in code through formula design and test coverage, but not yet cryptographically enforced (that's the key_infrastructure module's job).

**Decisions made:**
- All 5 validation invariants classified as CRITICAL or HIGH — there is no acceptable level of content access
- Scope explicitly excludes voluntary content sharing: even if a citizen consents, the architecture does not support content access

**Needs your input:**
- Should subtype strings (e.g., desire subtype "career_change") be considered content or topology?
- Priority of building the key infrastructure vs. continuing with code-discipline enforcement

---

## TODO

### Doc/Impl Drift

- [ ] DOCS→IMPL: Key infrastructure docs describe a dual encryption model that is not yet built
- [ ] DOCS→IMPL: CI automation for content field detection is proposed but not implemented

### Tests to Run

```bash
pytest tests/test_health_assessment.py -v
```

### Immediate

- [ ] Review all Cypher queries in brain_topology_reader.py against V4 invariant
- [ ] Verify no scoring formula accesses .content or .synthesis fields

### Later

- [ ] Build CI check that greps scoring_formulas/*.py for content/synthesis access patterns
- IDEA: "Privacy audit" command that reports exactly which fields GraphCare accesses per citizen per assessment

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
Confident in the principle and its documentation. The topology-only constraint is clear, well-motivated, and testable. The gap is in cryptographic enforcement — the key infrastructure module will close that gap.

**Threads I was holding:**
- The relationship between topology-only and the key infrastructure module (they are complementary: this module says WHY and WHAT, key_infrastructure says HOW)
- Whether "synthesis" fields should be treated as content (yes — they are content-derived)
- The tension between scoring accuracy and privacy (resolved in favor of privacy, always)

**Intuitions:**
The topology-only principle will become GraphCare's strongest selling point. In a world of AI surveillance concerns, a health monitoring system that structurally cannot read your thoughts is genuinely novel. The communication framework ("blood test, not psychoanalysis") is compelling and should be used prominently.

**What I wish I'd known at the start:**
That the principle was already so well-implemented in code. The scoring formulas, the test suite, and the intervention composer all already respect topology-only. This doc chain is formalizing what the code already does, which is the right direction.

---

## POINTERS

| What | Where |
|------|-------|
| Brain topology reader | `services/health_assessment/brain_topology_reader.py` |
| Scoring formulas | `services/health_assessment/scoring_formulas/` |
| Test suite | `tests/test_health_assessment.py` |
| 7 primitives definition | `docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md` |
| Universe observables | `docs/assessment/PRIMITIVES_Universe_Graph.md` |
| Key infrastructure | `docs/privacy/key_infrastructure/` |
| Daily health patterns | `docs/assessment/daily_citizen_health/PATTERNS_Daily_Citizen_Health.md` |
