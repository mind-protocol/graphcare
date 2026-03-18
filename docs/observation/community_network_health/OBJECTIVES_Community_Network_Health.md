# OBJECTIVES — Community Network Health

```
STATUS: DESIGNING
CREATED: 2026-03-15
VERIFIED: —
```

---

## CHAIN

```
THIS:            OBJECTIVES_Community_Network_Health.md (you are here - START HERE)
PATTERNS:       ./PATTERNS_Community_Network_Health.md
BEHAVIORS:      ./BEHAVIORS_Community_Network_Health.md
SYNC:           ./SYNC_Community_Network_Health.md

IMPL:           (not yet built)
```

**Read this chain in order before making changes.** Each doc answers different questions. Skipping ahead means missing context.

---

## PRIMARY OBJECTIVES (ranked)

1. **Detect isolation before it becomes crisis** — A citizen with zero interlocutors, fading connections, or no shared spaces is drifting into invisibility. By the time someone notices the absence, the citizen may be deeply disengaged. Network health monitoring catches this early — the same way a doctor catches low blood pressure before a collapse.

2. **Identify structural fragility in the social graph** — If removing one citizen would disconnect two clusters, that citizen is a single point of failure. If a subgroup only talks to itself, it's an echo chamber. These are network-level pathologies that no individual brain scan can reveal. GraphCare needs to see the forest, not just the trees.

3. **Maintain topology-only observation for networks** — The same privacy principle that governs brain topology applies here. We read who connects to whom, how often, in how many shared spaces — never the content of what they said. Network structure reveals health. Message content is none of our business.

4. **Provide network-level context for individual health scores** — A citizen's individual score exists in a context. If their cluster is thriving, a temporarily low personal score may not be alarming. If their cluster is fragmenting, even a stable personal score might mask trouble. Network health data enriches individual assessment.

## NON-OBJECTIVES

- **Social engineering or prescribing who should connect with whom** — GraphCare observes and reports. It never recommends specific social connections. That would cross from health monitoring into social manipulation.
- **Content analysis of conversations** — We see that citizen A and citizen B share 4 spaces and have exchanged 30 moments. We never see what they discussed.
- **Real-time social graph visualization** — Network health is a periodic assessment (same rhythm as individual health), not a live dashboard.
- **Replacing individual brain topology** — Network health supplements individual assessment, it doesn't replace it. A citizen can be individually healthy in an unhealthy network, or individually struggling in a healthy one.

## TRADEOFFS (canonical decisions)

- When **individual privacy** conflicts with **network visibility**, choose privacy. We accept coarser network maps (no message content, no sentiment, no topic analysis) to preserve the topology-only guarantee.
- When **early detection** conflicts with **false positive avoidance**, choose early detection with clear uncertainty markers. We accept flagging citizens who are simply on vacation rather than missing a citizen who is genuinely isolated. The flag says "check on this," not "this is broken."
- When **network-level insight** conflicts with **computational cost**, choose sampling over skipping. We accept approximate cluster detection over exact community detection algorithms if the exact version is too expensive to run continuously.

## SUCCESS SIGNALS (observable)

- Isolated citizens (zero interlocutors in the last 14 days) are flagged within one assessment cycle
- Trust clusters are identified and tracked over time — growing, stable, or fragmenting
- Echo chambers (subgroups with internal density > 3x their external connection rate) are detected and reported
- Single points of failure (citizens whose removal would increase graph components) are identified
- All network observations use only structural data: shared spaces, moment counts, link existence — never content
