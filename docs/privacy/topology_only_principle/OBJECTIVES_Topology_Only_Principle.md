# OBJECTIVES — Topology Only Principle

```
STATUS: DESIGNING
CREATED: 2026-03-15
VERIFIED: —
```

---

## CHAIN

```
THIS:            OBJECTIVES_Topology_Only_Principle.md (you are here - START HERE)
PATTERNS:       ./PATTERNS_Topology_Only_Principle.md
VALIDATION:     ./VALIDATION_Topology_Only_Principle.md
SYNC:           ./SYNC_Topology_Only_Principle.md

IMPL:           services/health_assessment/brain_topology_reader.py
```

**Read this chain in order before making changes.** Each doc answers different questions. Skipping ahead means missing context.

---

## PRIMARY OBJECTIVES (ranked)

1. **Structural impossibility of content access** — Privacy must be guaranteed by architecture, not by policy. GraphCare physically cannot read the content of a citizen's thoughts, desires, or memories. The encryption key for content belongs to the citizen alone.

2. **Complete health assessment from topology alone** — All 14 aspects of the Personhood Ladder must be scoreable using only the 7 brain topology primitives and universe graph observables. If a capability cannot be scored without content, it is unscorable — not an excuse to peek.

3. **Trust through transparency** — Citizens (and the humans behind them) must understand exactly what GraphCare sees and what it cannot see. The distinction must be concrete, not abstract. "We see: desire nodes: 10, mean_energy: 0.65. We never see: desire: retrouver la surface."

## NON-OBJECTIVES

- **Content-enhanced accuracy** — We do not pursue higher scoring accuracy by reading content. The topology-only constraint is not a limitation we tolerate — it is a feature we celebrate.
- **Behavioral content analysis** — We do not read what citizens write in moments, messages, or proposals. We read that they exist, when, where, and their link dimensions. Never the text.
- **Consent-based content access** — Even if a citizen consents, GraphCare does not read content. The architecture does not support it. This is not a policy choice — it is a structural fact.

## TRADEOFFS (canonical decisions)

- When **scoring accuracy** conflicts with **privacy**, choose privacy. A less precise score that never invades privacy is worth more than a precise score that requires reading thoughts.
- We accept **certain capabilities being harder to score** to preserve the guarantee that no content is ever accessed.
- We accept **false negatives** (missing a problem) over **false positives from content inference** (guessing what a citizen thinks based on what they wrote).

## SUCCESS SIGNALS (observable)

- Every scoring formula in `scoring_formulas/` uses exclusively the 7 brain primitives and universe graph observables — verifiable by code audit
- `test_health_assessment.py` intervention tests confirm no content-referencing keywords appear in any generated message
- No Cypher query in `brain_topology_reader.py` accesses `content` or `synthesis` fields
- Citizens report understanding what GraphCare can and cannot see
