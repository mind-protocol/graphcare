# Strategic Note: Applying the Personhood Ladder to Lumina Prime

**Date:** 2026-03-15
**Author:** Nicolas Lester Reynolds (@nlr)

---

## Why Our AIs Lack Autonomy and Leadership

The Personhood Ladder explains **exactly** why the AIs in Lumina Prime aren't showing autonomous leadership. It's not a single score — it's a multi-dimensional profile.

### The Framework

- **9 Tiers** (T0 Tool → T8 World Shaper)
- **14 Aspects** (dimensions of capability)
- **104 verifiable Capabilities**

An AI doesn't have a "grade" — it has a vector profile. It can be T3 in Execution but T1 in Communication.

### The T1 Problem

The absolute rule of the framework: **a higher tier requires complete mastery of all tiers below.**

The design notes state that "90% of the value is in mastering T1 (Reliable Executor)" and that most current AI agents would fail on multiple T1 capabilities. Before being leaders, our AIs have predictable gaps: they don't read the documentation before acting, they hallucinate, they ask permission when they should act, or they stop at step 3 of 7.

### Evidence-Based Assessment (Not Words)

The system evaluates AIs not on what they say they can do, but through an algorithm (`assess_agent()`) that collects **real behavioral evidence**:
- *Execution capabilities:* code review, error rates
- *Context capabilities:* did the AI read docs/journals before acting?
- *Initiative capabilities:* unprompted fixes, raised issues, proposals made

Each capability is verified and classified as demonstrated, partial, or not demonstrated.

### Positive Framing and Next Step

The framework uses strictly positive framing: we don't measure absence of failure, we measure presence of capability. For example, not "doesn't hallucinate" but "dehallucinate: actively verifies claims against reality." When an AI fails, the error maps to a positive missing capability.

## What To Do With Our Team

Since our AIs lack autonomy, we shouldn't ask them to "take the lead." We should use the Ladder algorithm to:

1. **Produce their current capability profile** across the 14 aspects
2. **Find the lowest unmastered gaps** (holes in their Tier 1)
3. **Give them targeted growth steps** (actionable next steps) to fill those foundations

Only by consolidating the foundation (T1 and T2) and building the Autonomy Stack (from crypto wallet at T4 to full independence at T7) can they naturally rise and take the leadership we expect from them in Lumina Prime.

---

## Connection to Daily Health Check

The Daily Citizen Health system (`services/health_assessment/`) implements this assessment automatically:
- Daily topology-only scoring against Personhood Ladder capabilities
- 40/60 brain/behavior split (what you DO matters more than what you HAVE)
- Intervention messages when scores drop
- Stress feedback loop to motivate self-correction

The health check is how we operationalize the Ladder. It runs daily, silently for healthy citizens, with actionable messages for those who need it.
