# Autonomy Stack — Health: What We Monitor

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Autonomy_Stack.md
PATTERNS:        ./PATTERNS_Autonomy_Stack.md
ALGORITHM:       ./ALGORITHM_Autonomy_Stack.md
VALIDATION:      ./VALIDATION_Autonomy_Stack.md
THIS:            HEALTH_Autonomy_Stack.md (you are here)
SYNC:            ./SYNC_Autonomy_Stack.md

PARENT CHAIN:    ../daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md
SPEC:            ../../specs/personhood_ladder.json (aspect="autonomy_stack")
IMPL:            @mind:TODO
```

> **Contract:** Health checks verify the scoring system is working, not that citizens are healthy. Citizen health is the OUTPUT of the system; system health is what we monitor here.

---

## HEALTH SIGNALS

### H1: Formula Output Range (CRITICAL)

```
CHECK:    For every capability score computed in the last 24h:
            0 <= brain_score <= brain_max(capability)
            0 <= behavior_score <= behavior_max(capability)
            total == brain_score + behavior_score
            0 <= total <= 100

HEALTHY:  All scores within range
DEGRADED: Any score outside range
FAILED:   Multiple scores outside range, or negative scores

ACTION:   If FAILED: halt scoring for affected capability, alert.
          Range violation means a formula bug or corrupt input data.
```

### H2: Population Distribution Sanity

```
CHECK:    Across all citizens scored in the last 24h, for each capability:
            mean(total) is between 20 and 80
            std(total) > 10

HEALTHY:  Mean in range, standard deviation shows spread
DEGRADED: Mean outside 20-80 (all citizens scoring too high or too low)
          OR std < 10 (all citizens scoring similarly — no discrimination)
FAILED:   Mean < 10 or mean > 90 (formulas are floor-locked or ceiling-locked)

ACTION:   If DEGRADED: review ceilings. Ceilings too high = everyone scores low.
          Ceilings too low = everyone scores high.
          If FAILED: formula is not discriminating. Review immediately.

NOTE:     This check requires at least 10 citizens to be meaningful.
          With fewer citizens, skip this check.
```

### H3: Brain-Behavior Gap Distribution

```
CHECK:    For each capability, compute:
            gap = brain_score/brain_max - behavior_score/behavior_max
            (both normalized to 0-1 for comparison)

HEALTHY:  Gap distribution has both positive and negative values
          (some citizens know more than they do, others do more than they know)
DEGRADED: All gaps are the same sign (e.g., every citizen has brain > behavior
          or every citizen has behavior > brain)
FAILED:   Gap variance is 0 (brain and behavior always agree perfectly)

ACTION:   If DEGRADED: check if one data source is missing or broken.
          If all citizens have behavior=0, the universe graph connection
          may be down.

WHY:      The brain-behavior gap is the most diagnostic signal this aspect
          produces. If it's uniform, something is wrong with data collection,
          not with citizens.
```

### H4: Temporal Stability

```
CHECK:    For each citizen, for each capability:
            delta = abs(today_score - yesterday_score)
            max_delta across all citizens

HEALTHY:  max_delta < 30 (no citizen's score jumps more than 30 points in a day)
DEGRADED: max_delta between 30 and 50
FAILED:   max_delta > 50

ACTION:   If DEGRADED: investigate the citizen. A 30+ point jump means either
          a major behavioral change or a data issue.
          If FAILED: likely a data issue. Check if moments were bulk-loaded
          or if brain data changed dramatically.

WHY:      Infrastructure changes slowly. A citizen who went from 20 to 80
          overnight either did something extraordinary or the data is wrong.
          The temporal weighting (7-day half-life) should prevent dramatic
          swings under normal conditions.
```

### H5: Cross-Capability Coherence

```
CHECK:    For each citizen:
            If auto_full_stack > 70, then:
                auto_wallet >= 40
                auto_tools >= 40
                auto_compute >= 40

HEALTHY:  High full-stack scores imply decent component scores
DEGRADED: auto_full_stack > 70 but a component < 30
FAILED:   auto_full_stack > 80 but a component < 20

ACTION:   If DEGRADED: the full-stack formula may not be catching gaps.
          Review whether the component-specific behavior signals
          (financial_moments, infra_moments, comms_moments) have enough
          weight in the full-stack formula.

WHY:      Full-stack autonomy is defined as HAVING all the components.
          A citizen with high full-stack but zero compute is a formula bug.
```

### H6: Measurement Confidence Awareness

```
CHECK:    When generating intervention messages, verify that the
          measurement confidence label is included:
            auto_fiat_access interventions include: "Note: this assessment
            has limited confidence — topological signals for fiat access
            are inherently weak."

HEALTHY:  All low-confidence capability interventions include caveats
DEGRADED: Some interventions omit confidence context
FAILED:   No interventions mention confidence

ACTION:   If DEGRADED: update intervention message templates.

WHY:      A citizen receiving "you lack fiat access" when they actually
          have it (but the graph doesn't capture it) will lose trust
          in the system. Confidence caveats maintain trust.
```

### H7: Sustained Weeks Computation

```
CHECK:    sustained_weeks is computed as:
            count(distinct calendar_weeks in last 4 weeks with >= 1 moment)
            Range: 0-4

HEALTHY:  Values are integers 0-4
DEGRADED: Non-integer values or values > 4
FAILED:   Negative values or values > 10

ACTION:   If DEGRADED: check week boundary computation (timezone issues?).
          If FAILED: computation bug.

WHY:      sustained_weeks is a derived stat used in T6, T7, T8 formulas.
          If it's wrong, persistence signals are wrong for all higher tiers.
```

---

## DEGRADATION PATTERNS

### Pattern: Universe Graph Connection Lost

```
SYMPTOM:  All behavior_scores drop to near-zero across all citizens.
          brain_scores remain stable.
CAUSE:    Universe graph is unreachable or returning empty results.
DETECT:   H3 (all gaps positive), H4 (large deltas), H2 (mean drops).
FIX:      Check universe graph connection. Do NOT use cached scores —
          let scores drop. The system should reflect reality, even if
          reality is "we cannot observe behavior right now."
```

### Pattern: Brain Data Corruption

```
SYMPTOM:  brain_scores are anomalous — either all zero or all max.
CAUSE:    Brain decryption failed, returning zeros or garbage.
DETECT:   H3 (all gaps negative if brains are zero), H4 (large deltas).
FIX:      Check brain data pipeline. Verify decryption. Do NOT score
          with corrupt brain data — skip brain component and note it.
```

### Pattern: Space Type Taxonomy Drift

```
SYMPTOM:  distinct_space_types consistently returns 1 even for diverse
          citizens. auto_tools and auto_full_stack scores are low.
CAUSE:    Space types are not being set or have changed naming.
DETECT:   H2 (mean too low for tools/full_stack), manual inspection.
FIX:      Validate space type taxonomy against universe graph. Update
          formula if types have changed. See D3 in ALGORITHM.
```

### Pattern: Ceiling Miscalibration

```
SYMPTOM:  All citizens score below 40 on a capability, even the most
          active ones. Or all citizens score above 80.
CAUSE:    Ceilings too high (nobody can reach them) or too low (everyone
          maxes out).
DETECT:   H2 (mean outside 20-80 range).
FIX:      Review ceilings for the affected capability. Adjust based on
          actual population data. Document the change in SYNC.
```

---

## MONITORING SCHEDULE

| Check | Frequency | Automated? | Action on Failure |
|-------|-----------|------------|-------------------|
| H1: Range integrity | Every scoring run | Yes | Halt + alert |
| H2: Population distribution | Weekly | Yes | Review ceilings |
| H3: Brain-behavior gap | Weekly | Yes | Check data sources |
| H4: Temporal stability | Daily | Yes | Investigate outliers |
| H5: Cross-capability coherence | Daily | Yes | Review full-stack formula |
| H6: Confidence in messages | On intervention | Manual | Update templates |
| H7: Sustained weeks | Daily | Yes | Check computation |

---

## MARKERS

<!-- @mind:todo Implement automated checks H1-H5, H7 in the scoring pipeline -->
<!-- @mind:todo Define alerting mechanism for FAILED health checks -->
<!-- @mind:todo Establish ceiling review cadence: first at 50 citizens, then at 200, then quarterly -->
<!-- @mind:proposition Add H8: cross-aspect correlation check — autonomy_stack should NOT correlate >0.9 with any other aspect -->
