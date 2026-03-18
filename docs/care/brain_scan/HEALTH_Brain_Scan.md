# Brain Scan — Health: Verification Mechanics and Coverage

```
STATUS: DESIGNING
CREATED: 2026-03-18
```

---

## WHEN TO USE HEALTH (NOT TESTS)

Health checks verify runtime behavior that tests cannot catch:

| Use Health For | Why |
|----------------|-----|
| Drift over time | Needs 1000+ real ticks, not fixtures |
| Ratio health | Emergent behavior, not deterministic |
| Graph-wide state | Needs real structure, not mocks |
| Production data patterns | Test fixtures can't predict real usage |

**Tests gate completion. Health monitors runtime.**

If behavior is deterministic with known inputs -> write a test.
If behavior emerges from real data over time -> write a health check.

See `VALIDATION_Brain_Scan.md` for the full distinction.

---

## PURPOSE OF THIS FILE

This HEALTH file covers the brain scan module — specifically the runtime health of the extraction pipeline (FalkorDB connectivity and scan output validity). It exists to catch failures that only manifest with real brain data: FalkorDB crashes, empty graphs after data loss, malformed positions from unexpected node types.

Boundaries: This file verifies that the brain scan pipeline produces valid output from real data. It does NOT verify Three.js rendering quality (that requires manual browser testing), nor does it verify health assessment scores (separate module).

---

## WHY THIS PATTERN

The brain scan is a visualization tool, not a critical service. Its health checks are lightweight — verify that FalkorDB is reachable, that scans contain data, and that positions are valid numbers. The failure mode this avoids: scans silently producing empty or malformed JSON that renders as a blank screen, with no signal that the pipeline is broken.

Docking-based checks are the right tradeoff because the pipeline has exactly two meaningful boundaries: the FalkorDB read and the JSON output. Checking these two points catches the majority of real-world failures (DB down, data loss, new node types without layer mappings).

Throttling is minimal — brain scans are generated on-demand, not continuously.

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Brain_Scan.md
PATTERNS:        ./PATTERNS_Brain_Scan.md
BEHAVIORS:       ./BEHAVIORS_Brain_Scan.md
ALGORITHM:       ./ALGORITHM_Brain_Scan.md
VALIDATION:      ./VALIDATION_Brain_Scan.md
IMPLEMENTATION:  ./IMPLEMENTATION_Brain_Scan.md
THIS:            HEALTH_Brain_Scan.md (you are here)
SYNC:            ./SYNC_Brain_Scan.md
```

---

## IMPLEMENTS

This HEALTH file is a **spec**. The actual code lives in runtime:

```yaml
implements:
  runtime: services/brain_scan/health_checks.py   # To be created
  decorator: @check                                # Decorator-based registration
```

> **Separation:** HEALTH.md defines WHAT to check and WHEN to trigger. Runtime code defines HOW to check.

> **Contract:** HEALTH checks verify input/output against VALIDATION with minimal or no code changes. After changes: update runtime or add TODO to SYNC. Run HEALTH checks at throttled rates.

---

## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)

```yaml
flows_analysis:
  - flow_id: brain_scan_extraction
    purpose: If this flow fails, brain scans produce empty or invalid output — viewers see blank screens with no explanation
    triggers:
      - type: manual
        source: CLI invocation (python brain_scan_data_extractor.py {handle})
        notes: On-demand scan generation triggered by operator or health assessment pipeline
    frequency:
      expected_rate: 1-5/day
      peak_rate: 20/day (during batch scans of multiple citizens)
      burst_behavior: Sequential execution, no parallelism. FalkorDB handles one query at a time per connection.
    risks:
      - FalkorDB unreachable or crashed (V2 — nodes won't have positions if extraction fails)
      - Brain graph empty after FalkorDB data loss on restart (V2 — scan produces 0 nodes)
      - New node types without LAYER_Z mapping (V3 — nodes placed in default band, layer label may be wrong)
    notes: FalkorDB is known to crash under heavy load. Data loss on restart is a known infra issue.
```

---

## HEALTH INDICATORS SELECTED

## OBJECTIVES COVERAGE

| Objective | Indicators | Why These Signals Matter |
|-----------|------------|--------------------------|
| O1 (Make brain state visible) | scan_completeness | If the scan has 0 nodes, there's nothing to visualize |
| O2 (Anatomy layers correct) | position_validity | NaN positions crash Three.js; wrong z-bands break the metaphor |
| O4 (Pre-computed, not live) | falkordb_connectivity | If FalkorDB is down, no scan can be generated |

```yaml
health_indicators:
  - name: falkordb_connectivity
    flow_id: brain_scan_extraction
    priority: high
    rationale: FalkorDB is the single data source. If unreachable, no brain scans can be produced. Known instability under load.
  - name: scan_completeness
    flow_id: brain_scan_extraction
    priority: high
    rationale: A scan with 0 nodes is useless. Data loss on FalkorDB restart can silently empty brain graphs.
  - name: position_validity
    flow_id: brain_scan_extraction
    priority: med
    rationale: NaN coordinates crash Three.js rendering. Invalid positions from edge cases (unknown types, missing weight) should be caught.
```

---

## STATUS (RESULT INDICATOR)

```yaml
status:
  stream_destination: data/brain_scans/health_status.json
  result:
    representation: enum
    value: UNKNOWN
    updated_at: 2026-03-18T00:00:00Z
    source: falkordb_connectivity
```

---

## CHECKER INDEX

```yaml
checkers:
  - name: falkordb_connectivity
    purpose: Verify FalkorDB is reachable and the brain graph exists (V2 precondition)
    status: pending
    priority: high
  - name: scan_completeness
    purpose: Verify extracted scan has > 0 nodes (V2)
    status: pending
    priority: high
  - name: position_validity
    purpose: Verify no NaN in x/y/z coordinates and z-values match anatomy bands (V2, V3)
    status: pending
    priority: med
```

---

## INDICATOR: falkordb_connectivity

### VALUE TO CLIENTS & VALIDATION MAPPING

```yaml
value_and_validation:
  indicator: falkordb_connectivity
  client_value: Without FalkorDB, brain scans cannot be generated. Operators need to know when the database is down before attempting scans.
  validation:
    - validation_id: V2
      criteria: Every node must get a valid position — impossible if FalkorDB is unreachable
```

### HEALTH REPRESENTATION

```yaml
representation:
  selected:
    - binary
  semantics:
    binary: 1 = FalkorDB reachable and graph exists. 0 = connection failed or graph not found.
  aggregation:
    method: Direct (single check)
    display: binary
```

### DOCKS SELECTED

```yaml
docks:
  - point: dock_falkordb_read
    type: db
    payload: Connection success/failure, graph existence
```

### ALGORITHM / CHECK MECHANISM

```python
@check(
    id="falkordb_connectivity",
    triggers=[
        triggers.manual(),
    ],
    on_problem="FALKORDB_UNREACHABLE",
    task="fix_falkordb_connection",
)
def falkordb_connectivity(ctx) -> dict:
    """Check FalkorDB is reachable and brain graph exists."""
    try:
        db = FalkorDB(host=FALKORDB_HOST, port=FALKORDB_PORT)
        graph = db.select_graph(f"brain_{ctx.citizen_handle}")
        result = graph.query("MATCH (n) RETURN count(n)")
        count = result.result_set[0][0]
        if count > 0:
            return Signal.healthy(details={"node_count": count})
        return Signal.degraded(details={"node_count": 0, "reason": "Graph exists but empty"})
    except Exception as e:
        return Signal.critical(details={"error": str(e)})
```

### SIGNALS

```yaml
signals:
  healthy: FalkorDB reachable, brain graph exists with > 0 nodes
  degraded: FalkorDB reachable but brain graph is empty (possible data loss)
  critical: FalkorDB unreachable or connection error
```

### THROTTLING STRATEGY

```yaml
throttling:
  trigger: manual (before scan generation)
  max_frequency: 1/min
  burst_limit: 5
  backoff: Exponential backoff on repeated failures (1min, 5min, 15min)
```

### FORWARDINGS & DISPLAYS

```yaml
forwarding:
  targets:
    - location: data/brain_scans/health_status.json
      transport: file
      notes: Local health status file for operator inspection
display:
  locations:
    - surface: CLI
      location: stdout during scan generation
      signal: green=connected / red=unreachable
      notes: Printed before extraction begins
```

### MANUAL RUN

```yaml
manual_run:
  command: python -c "from falkordb import FalkorDB; db = FalkorDB(); print(db.select_graph('brain_dragon_slayer').query('MATCH (n) RETURN count(n)').result_set)"
  notes: Run before batch scan generation to verify FalkorDB is up
```

---

## HOW TO RUN

```bash
# Run all health checks for brain scan module
python services/brain_scan/health_checks.py --all

# Run a specific checker
python services/brain_scan/health_checks.py --check falkordb_connectivity
```

---

## KNOWN GAPS

- V1 (topology-only) is not covered by a health check — it requires static analysis of Cypher queries, better suited to a unit test
- V4 (visual property accuracy) is not covered — deterministic mapping, better suited to unit tests
- V5 (HTML renders) is not covered — requires browser testing, cannot be automated with Python health checks

<!-- @mind:todo Create health_checks.py implementing the three checkers defined above -->
<!-- @mind:todo Add scan_completeness and position_validity indicator sections when health_checks.py is implemented -->

---

## MARKERS

<!-- @mind:todo Implement services/brain_scan/health_checks.py with the three checkers defined in this spec -->
<!-- @mind:proposition Add a health check that validates scan JSON schema (required fields present, correct types) -->
