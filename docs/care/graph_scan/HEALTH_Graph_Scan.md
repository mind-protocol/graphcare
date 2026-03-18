# Graph Scan — Health: Verification Mechanics and Coverage

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

See `VALIDATION_Graph_Scan.md` for the full invariant list.

---

## PURPOSE OF THIS FILE

This HEALTH file covers the Graph Scan module's runtime verification: ensuring that FalkorDB is reachable, extraction produces valid data, and positions are finite. It exists because Graph Scan is a visualization tool — not a critical service — so health coverage is minimal and focused on the basics that would make the pipeline silently fail.

**Boundaries:** This file verifies extraction pipeline health. It does NOT verify visual rendering quality, Three.js correctness in the browser, or UMAP output quality (those are better served by manual inspection and tests).

---

## WHY THIS PATTERN

Graph Scan is an offline tool run on demand, not a continuously running service. Health checks here serve a different purpose than typical service monitoring: they verify pre-conditions (is FalkorDB reachable?) and post-conditions (did extraction produce valid data?) at the time of execution.

The failure mode this avoids: extraction runs, produces a JSON with NaN positions or 0 nodes, and nobody notices until they open a blank HTML file. By checking at the docking points (FalkorDB read, JSON output), we catch failures early.

Throttling is minimal since runs are infrequent (on-demand, not scheduled).

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Graph_Scan.md
PATTERNS:        ./PATTERNS_Graph_Scan.md
BEHAVIORS:       ./BEHAVIORS_Graph_Scan.md
ALGORITHM:       ./ALGORITHM_Graph_Scan.md
VALIDATION:      ./VALIDATION_Graph_Scan.md
IMPLEMENTATION:  ./IMPLEMENTATION_Graph_Scan.md
THIS:            HEALTH_Graph_Scan.md (you are here)
SYNC:            ./SYNC_Graph_Scan.md
```

---

## IMPLEMENTS

This HEALTH file is a **spec**. The actual code lives in runtime:

```yaml
implements:
  runtime: (not yet implemented)       # Pending health check implementation
  decorator: @check                    # Decorator-based registration (future)
```

> **Separation:** HEALTH.md defines WHAT to check and WHEN to trigger. Runtime code defines HOW to check.

---

## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)

```yaml
flows_analysis:
  - flow_id: l1_brain_scan
    purpose: If FalkorDB is unreachable or the brain graph is empty, extraction silently produces garbage
    triggers:
      - type: manual
        source: CLI invocation (python brain_data_extractor.py {handle})
        notes: Run on-demand by agents or humans
    frequency:
      expected_rate: 1-5/day
      peak_rate: 20/day
      burst_behavior: No burst concern — each run is independent, no shared state
    risks:
      - FalkorDB down (V3 — positions would be undefined)
      - Empty graph (0 nodes — valid but useless)
      - UMAP failure (fallback to sphere, losing semantic topology — V2 degraded)
    notes: Not a service — no uptime requirement. Health verifies per-run correctness.
```

---

## HEALTH INDICATORS SELECTED

## OBJECTIVES COVERAGE

| Objective | Indicators | Why These Signals Matter |
|-----------|------------|--------------------------|
| O1: Make graph visible | node_extraction_nonzero | If no nodes extracted, the visualization is empty |
| O2: Semantic topology | (manual verification only) | Centroid subtraction quality can't be easily automated |
| O3: All dimensions visible | (covered by V5 tests) | Visual mapping correctness is deterministic — use tests |
| O4: Pre-computed, static | positions_finite | NaN positions would crash the renderer |

```yaml
health_indicators:
  - name: falkordb_reachable
    flow_id: l1_brain_scan
    priority: high
    rationale: If FalkorDB is unreachable, no extraction is possible. Agent or operator needs to know before attempting a scan.
  - name: node_extraction_nonzero
    flow_id: l1_brain_scan
    priority: med
    rationale: An extraction that produces 0 nodes is technically valid but useless. Indicates the brain graph is empty or the query failed silently.
  - name: positions_finite
    flow_id: l1_brain_scan
    priority: high
    rationale: NaN or Infinity in positions would render invisible/broken nodes. This is the most common silent failure mode from UMAP.
```

---

## STATUS (RESULT INDICATOR)

```yaml
status:
  stream_destination: data/graph_scans/health_status.json
  result:
    representation: enum
    value: UNKNOWN
    updated_at: 2026-03-18T00:00:00Z
    source: (not yet implemented)
```

---

## CHECKER INDEX

```yaml
checkers:
  - name: falkordb_reachable
    purpose: Verify FalkorDB is reachable before extraction (V3 precondition)
    status: pending
    priority: high
  - name: node_extraction_nonzero
    purpose: Verify extraction produced at least 1 node
    status: pending
    priority: med
  - name: positions_finite
    purpose: Verify all node positions are finite floats, no NaN (V3)
    status: pending
    priority: high
```

---

## INDICATOR: FalkorDB Reachable

### VALUE TO CLIENTS & VALIDATION MAPPING

```yaml
value_and_validation:
  indicator: falkordb_reachable
  client_value: Agents and operators know whether extraction will work before attempting it
  validation:
    - validation_id: V3
      criteria: Valid 3D positions require data — no data if FalkorDB is down
```

### HEALTH REPRESENTATION

```yaml
representation:
  selected:
    - binary
  semantics:
    binary: "1 = FalkorDB responds to ping, 0 = connection refused or timeout"
  aggregation:
    method: direct (single check)
    display: binary
```

### DOCKS SELECTED

```yaml
docks:
  - point: dock_falkordb_read
    type: db
    payload: FalkorDB connection test (ping)
```

### ALGORITHM / CHECK MECHANISM

```python
@check(
    id="falkordb_reachable",
    triggers=[
        triggers.manual(),
    ],
)
def falkordb_reachable(ctx) -> dict:
    """Check FalkorDB is reachable."""
    try:
        from falkordb import FalkorDB
        db = FalkorDB(host="localhost", port=6379)
        db.list_graphs()
        return Signal.healthy()
    except Exception as e:
        return Signal.critical(details={"error": str(e)})
```

### SIGNALS

```yaml
signals:
  healthy: FalkorDB responds to list_graphs()
  critical: Connection refused, timeout, or error
```

### THROTTLING STRATEGY

```yaml
throttling:
  trigger: manual (before each extraction run)
  max_frequency: 1/min
  burst_limit: 5
  backoff: none (manual trigger only)
```

### MANUAL RUN

```yaml
manual_run:
  command: python -c "from falkordb import FalkorDB; db=FalkorDB(); print(db.list_graphs())"
  notes: Run before extraction if uncertain about FalkorDB availability
```

---

## INDICATOR: Positions Finite

### VALUE TO CLIENTS & VALIDATION MAPPING

```yaml
value_and_validation:
  indicator: positions_finite
  client_value: Prevents invisible or broken nodes in the visualization
  validation:
    - validation_id: V3
      criteria: All node positions (x, y, z) must be finite floats, no NaN or Infinity
```

### HEALTH REPRESENTATION

```yaml
representation:
  selected:
    - binary
  semantics:
    binary: "1 = all positions finite, 0 = at least one NaN/Infinity detected"
  aggregation:
    method: all-pass (any NaN fails the whole check)
    display: binary
```

### DOCKS SELECTED

```yaml
docks:
  - point: dock_json_output
    type: file
    payload: Scan JSON with nodes[].x, nodes[].y, nodes[].z
```

### ALGORITHM / CHECK MECHANISM

```python
@check(
    id="positions_finite",
    triggers=[
        triggers.file.on_write("data/graph_scans/*_scan.json"),
    ],
)
def positions_finite(ctx) -> dict:
    """Check all node positions are finite after extraction."""
    import json, math
    scan = json.loads(ctx.payload.read_text())
    for node in scan.get("nodes", []):
        for dim in ("x", "y", "z"):
            val = node.get(dim, 0)
            if not math.isfinite(val):
                return Signal.critical(details={"node": node["id"], "dim": dim, "value": val})
    return Signal.healthy()
```

### SIGNALS

```yaml
signals:
  healthy: All positions are finite floats within expected range
  critical: At least one position is NaN, Infinity, or None
```

### THROTTLING STRATEGY

```yaml
throttling:
  trigger: After each extraction (file write)
  max_frequency: 1/min
  burst_limit: 10
  backoff: none
```

### MANUAL RUN

```yaml
manual_run:
  command: python -c "import json,math; d=json.load(open('data/graph_scans/dragon_slayer_scan.json')); print(all(math.isfinite(n['x']) and math.isfinite(n['y']) and math.isfinite(n['z']) for n in d['nodes']))"
  notes: Replace dragon_slayer with the relevant scan name
```

---

## HOW TO RUN

```bash
# Check FalkorDB reachability
python -c "from falkordb import FalkorDB; db=FalkorDB(); print('OK:', db.list_graphs())"

# Check positions after extraction
python -c "
import json, math
scan = json.load(open('data/graph_scans/dragon_slayer_scan.json'))
bad = [n['id'] for n in scan['nodes'] if not all(math.isfinite(n[d]) for d in ('x','y','z'))]
print('HEALTHY' if not bad else f'CRITICAL: {bad}')
"
```

---

## KNOWN GAPS

- V1 (topology-only) has no automated health check — needs static analysis of Cypher queries
- V2 (types mix spatially) has no automated health check — requires spatial statistics
- V5 (visual properties reflect physics) is better tested deterministically, not via health

<!-- @mind:TODO Implement health checks as actual Python functions with @check decorator -->
<!-- @mind:TODO Add V1 check: parse Cypher queries in extractor files, verify content/synthesis never in RETURN -->

---

## MARKERS

<!-- @mind:TODO Implement the health check runtime (pending infrastructure) -->
<!-- @mind:proposition Add a visual regression check: compare rendered PNG against a baseline screenshot -->
