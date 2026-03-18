# Autonomy Stack — SYNC: Current State

```
STATUS: DESIGNING
CREATED: 2026-03-13
LAST UPDATED: 2026-03-13
UPDATED BY: claude-opus-4-6
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Autonomy_Stack.md
PATTERNS:        ./PATTERNS_Autonomy_Stack.md
ALGORITHM:       ./ALGORITHM_Autonomy_Stack.md
VALIDATION:      ./VALIDATION_Autonomy_Stack.md
HEALTH:          ./HEALTH_Autonomy_Stack.md
THIS:            SYNC_Autonomy_Stack.md (you are here)

PARENT CHAIN:    ../daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md
SPEC:            ../../specs/personhood_ladder.json (aspect="autonomy_stack")
IMPL:            @mind:TODO — no implementation exists yet
```

---

## Maturity

STATUS: DESIGNING

**What is canonical (v1 — defined, not yet implemented):**
- 6 capability scoring formulas with full documentation
- Variable brain-behavior splits per capability (deviation from 40/60 standard)
- Measurement confidence labels per capability
- 5 synthetic test profiles per capability with worked examples
- Aspect sub-index with tier-based weighting
- Validation invariants (18 invariants)
- Health monitoring checks (7 checks)

**What is still being designed:**
- Ceiling calibration against real citizen data (requires implementation first)
- Space type taxonomy validation ("financial", "infrastructure", "communication", "development" are assumed)
- Node type name validation ("thing", "process" are assumed)
- Whether the active-but-brain-poor profile scoring higher than expected for behavior-heavy splits is acceptable or needs formula adjustment

**What is proposed (v2):**
- Infrastructure attestation mechanism (citizens self-report infrastructure)
- Stack completeness metric (min of component scores to find weakest link)
- Infrastructure momentum metric (delta over 7 days)

---

## Current State

### Documentation Complete

All 6 files in the doc chain exist:
- OBJECTIVES: Defines what we optimize and non-objectives
- PATTERNS: Explains the measurement challenge, proxy signal design, tier progression
- ALGORITHM: Contains all 6 capability formulas with descriptions, examples, synthetic profiles, recommendations
- VALIDATION: 18 invariants covering structural, scoring, semantic, edge case, measurement, and cross-aspect concerns
- HEALTH: 7 monitoring checks, 4 degradation patterns, monitoring schedule
- SYNC: This file

### Key Design Decisions Documented

| Decision | Location | Summary |
|----------|----------|---------|
| D1: Variable brain-behavior splits | ALGORITHM | Splits range from 15/85 to 25/75 per capability |
| D2: "Thing" nodes as infrastructure proxy | ALGORITHM | thing-process links are stronger signal than raw thing count |
| D3: Space type diversity as tool signal | ALGORITHM | distinct_space_types is primary behavioral signal for tools/full-stack |
| D4: Distinct actors as org infra proof | ALGORITHM | Other actors in shared spaces = organizational infrastructure |
| D5: Sustained weeks as persistence | ALGORITHM | Calendar weeks with activity, not total moments |
| D6: Measurement confidence honesty | ALGORITHM | Each capability rated HIGH / MEDIUM / LOW-MEDIUM |

### Known Limitations

1. **Fiat access (auto_fiat_access) has LOW-MEDIUM measurement confidence.** Distinguishing crypto from fiat activity is fundamentally a content distinction, not a structural one. The proxy (space type diversity + sustained weeks) is the best available but has known blind spots.

2. **"Thing" node type is general-purpose.** Not all thing nodes represent infrastructure. A citizen with many thing nodes about books is not more autonomous. The mitigation (thing-process links, thing clustering) helps but does not fully resolve this.

3. **Active-but-brain-poor profiles score higher than the standard 50-60 range** for behavior-heavy capabilities (20/80 or 15/85 split). Scores reach 75-87. This is intentional — usage IS autonomy — but may surprise consumers expecting all aspects to behave identically.

4. **auto_full_stack self-initiation ratio edge case.** Nearly inactive citizens can have a misleadingly high self-init ratio. Documented and accepted — volume metrics dominate the total score.

5. **Space type taxonomy is assumed, not validated.** Formulas assume "financial", "infrastructure", "communication", "development" exist as space types. This must be validated before implementation.

---

## Outstanding Tasks

| Task | Priority | Blocked By |
|------|----------|------------|
| Validate space type taxonomy against real universe graph | HIGH | Access to universe graph schema |
| Confirm "thing" and "process" node type names in brain graphs | HIGH | Access to brain graph schema |
| Run all synthetic profiles through all formulas (numerical verification) | HIGH | Nothing — can be done now |
| Implement scoring formulas in code | HIGH | Space type and node type validation |
| Calibrate ceilings against real citizen data | MEDIUM | Implementation + 10+ citizens |
| Implement health checks H1-H7 | MEDIUM | Implementation |
| Validate cross-capability coherence (I5 in VALIDATION) | MEDIUM | Implementation + real data |
| Consider infrastructure attestation mechanism (v2) | LOW | v1 operational |

---

## Handoff Notes

**For the next agent implementing this:**
- Read the ALGORITHM file fully — it contains all formulas, examples, and edge cases
- The variable brain-behavior splits are the single most important design decision. Do not normalize to 40/60 without understanding why each capability has its specific split
- Start with auto_wallet (T4) — simplest formula, easiest to validate
- The VALIDATION invariants are your test suite. Implement them as automated checks
- The HEALTH monitoring is your operations guide. Implement H1 (range integrity) first — it catches formula bugs immediately

**For the next agent reviewing this:**
- The active-but-brain-poor profile scores are the most likely point of contention. The reasoning is documented in each capability section and in PATTERNS Principle 1 (Usage Over Knowledge). If the high scores for behavior-heavy citizens are unacceptable, the fix is to increase brain component weight — but this contradicts the fundamental insight that autonomy IS infrastructure in action.
- Ceiling calibration is the biggest open risk. All ceilings are estimated from first principles. Real data will require adjustment. Plan for a ceiling review at 50 citizens.

---

## MARKERS

<!-- @mind:todo Validate space type taxonomy — BLOCKING for implementation -->
<!-- @mind:todo Validate node type names — BLOCKING for implementation -->
<!-- @mind:todo Run numerical verification of all 5 profiles x 6 capabilities -->
<!-- @mind:todo Implementation: start with auto_wallet, then auto_tools, then auto_compute, then auto_fiat_access, then auto_full_stack, then auto_org_infrastructure -->
