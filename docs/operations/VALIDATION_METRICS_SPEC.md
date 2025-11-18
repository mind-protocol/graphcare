# GraphCare Validation Metrics Specification

**Author:** Vera (Chief Validator)
**Date:** 2025-11-04 (Updated for minimal extension strategy)
**Purpose:** Define validation metrics, measurement approach, and U4_ type usage for GraphCare
**For:** Nora (schema design input) + Team (execution guidance)

---

## 1. Executive Summary

**GraphCare validation adapts Mind Protocol's 10 health metrics to code quality assessment.**

Mind Protocol monitors consciousness substrate health (are thoughts well-connected? coherent?).
GraphCare monitors extracted knowledge graph health (is code well-tested? documented? secure?).

**Core insight:** Same measurement patterns, different domain.

**Schema Strategy (adopted):** Minimal extension
- **0 new node types** - Reuse Mind Protocol U4_ types
- **1 new link type** - U4_SEMANTICALLY_SIMILAR

---

## 2. Validation Metrics (Adapted from Mind Protocol)

### Mind Protocol → GraphCare Mapping

| Mind Protocol Metric | GraphCare Validation Metric | What It Measures | Priority |
|---------------------|----------------------------|------------------|----------|
| **Density (E/N)** | **Test Coverage Ratio** | % of code with tests (line coverage) | CRITICAL |
| **Orphan Ratio** | **Untested Code Ratio** | % of code without any tests | CRITICAL |
| **Coherence** | **Test Quality Score** | Do tests actually validate behavior? | HIGH |
| **Highway Health** | **Integration Test Coverage** | Cross-module test coverage | HIGH |
| **Reconstruction** | **Test Execution Performance** | p90 test run latency | MEDIUM |
| **Learning Flux** | **Test Suite Evolution Rate** | Tests added/updated per week | MEDIUM |
| **WM Health** | **Critical Path Coverage** | Payment/auth/user data coverage | CRITICAL |
| **SubEntity Size** | **Test Scope Distribution** | Unit vs integration vs e2e ratio | LOW |
| **Overlap** | **Shared Test Fixtures** | Test utility reuse | LOW |
| **Sector Connectivity** | **Module Test Distribution** | Are all modules tested? | MEDIUM |

---

## 3. Using Mind Protocol U4_ Types for Validation

**Strategy:** No new node types. Map validation concepts to existing U4_ types.

### Test Cases → U4_Code_Artifact

**Type:** `U4_Code_Artifact` (from COMPLETE_TYPE_REFERENCE.md)

**Path granularity:**
```
tests/auth/test_user_auth.py                          # File-level test artifact
tests/auth/test_user_auth.py::TestAuth               # Class-level
tests/auth/test_user_auth.py::TestAuth::test_valid   # Function-level (individual test)
```

**Standard fields:**
- `path` (string) - Full path with granularity
- `lang` (enum) - `py`, `ts`, `js`, `go`, etc.
- `repo` (string) - Repository name
- `commit` (string) - Git commit
- `hash` (string) - File hash

**Metadata (in `description` or `detailed_description`):**
- Test type: unit, integration, e2e
- Test framework: pytest, jest, go_test
- Last run timestamp
- Pass rate (0-1)
- Execution time (ms)

**Example:**
```cypher
CREATE (test:U4_Code_Artifact {
  path: 'tests/auth/test_user_auth.py::TestAuth::test_valid_credentials',
  lang: 'py',
  repo: 'scopelock',
  commit: 'a7f3d9c',
  hash: 'sha256:abc123',
  description: 'Test user authentication with valid credentials',
  detailed_description: 'type: integration | framework: pytest | last_run: 2025-11-04T10:30:00Z | pass_rate: 0.98 | exec_ms: 245',
  level: 'L2',
  scope_ref: 'scopelock',
  created_at: datetime(),
  updated_at: datetime(),
  valid_from: datetime(),
  valid_to: null
})
```

---

### Coverage Metrics → U4_Metric

**Type:** `U4_Metric` (from COMPLETE_TYPE_REFERENCE.md)

**Standard fields:**
- `definition` (string) - How to calculate
- `level` (enum) - `L2` (organizational)
- `scope_ref` (string) - Client org ID (e.g., "scopelock")
- `unit` (string) - "percentage", "ratio", "count"
- `aggregation` (enum) - "avg", "p95", "sum"

**Example:**
```cypher
CREATE (metric:U4_Metric {
  name: 'branch_coverage_global',
  definition: '% of decision branches executed by tests across entire codebase',
  unit: 'percentage',
  level: 'L2',
  scope_ref: 'scopelock',
  aggregation: 'avg',
  description: 'Global branch coverage metric',
  detailed_description: 'target: 0.85 | critical_threshold: 0.70',
  created_at: datetime(),
  updated_at: datetime(),
  valid_from: datetime(),
  valid_to: null
})
```

---

### Coverage Measurements → U4_Measurement

**Type:** `U4_Measurement` (from COMPLETE_TYPE_REFERENCE.md)

**Standard fields:**
- `level` (enum) - `L2`
- `metric_ref` (string) - Links to U4_Metric node ID
- `scope_ref` (string) - Client org ID
- `timestamp` (datetime) - When measured
- `value` (float) - Measured value (0-1 for percentages)

**Metadata (in `description`):**
- Commit hash
- Branch
- Uncovered lines (if applicable)
- Tool used (pytest-cov, nyc, etc.)

**Example:**
```cypher
CREATE (measurement:U4_Measurement {
  metric_ref: 'branch_coverage_global',
  value: 0.72,
  timestamp: datetime('2025-11-04T14:30:00Z'),
  level: 'L2',
  scope_ref: 'scopelock',
  description: 'commit: a7f3d9c | branch: main | tool: pytest-cov',
  detailed_description: 'files_measured: 87 | total_branches: 342 | covered_branches: 246',
  created_at: datetime(),
  updated_at: datetime(),
  valid_from: datetime(),
  valid_to: null
})

CREATE (measurement)-[:U4_MEASURES]->(metric)
```

---

### Validation Gaps → U4_Assessment

**Type:** `U4_Assessment` (from COMPLETE_TYPE_REFERENCE.md)

**Domain:** `performance` (closest match for validation/testing domain)

**Standard fields:**
- `assessor_ref` (string) - "Vera" (the validator)
- `domain` (enum) - "performance"
- `level` (enum) - `L2`
- `scope_ref` (string) - Client org ID
- `score` (float) - Severity/impact score (0 = critical gap, 1 = no gap)

**Metadata (in `description` / `detailed_description`):**
- Gap type: missing_tests, weak_tests, untested_critical_path
- Affected files
- Risk assessment
- Recommendations

**Example:**
```cypher
CREATE (gap:U4_Assessment {
  name: 'payment_retry_no_tests',
  domain: 'performance',
  assessor_ref: 'Vera',
  score: 0.0,
  level: 'L2',
  scope_ref: 'scopelock',
  description: 'Payment retry logic has 0% test coverage',
  detailed_description: 'gap_type: untested_critical_path | severity: critical | affected: [src/payment/retry.py] | risk: Handles money, failure could cause payment loss | recommendation: Add integration tests for retry scenarios (network error, timeout, max retries)',
  created_at: datetime(),
  updated_at: datetime(),
  valid_from: datetime(),
  valid_to: null
})
```

---

### Test Quality Assessments → U4_Assessment

**Type:** `U4_Assessment` (same as validation gaps, different metadata)

**Domain:** `performance`

**Standard fields:** Same as validation gaps

**Metadata (in `detailed_description`):**
- Quality score (0-1)
- Issues found
- Strengths
- Improvement recommendations

**Example:**
```cypher
CREATE (assessment:U4_Assessment {
  name: 'auth_tests_quality',
  domain: 'performance',
  assessor_ref: 'Vera',
  score: 0.72,
  level: 'L2',
  scope_ref: 'scopelock',
  description: 'Test quality assessment for auth module',
  detailed_description: 'quality_score: 0.72 | issues: [Happy path only, No session expiration tests, Mocks instead of real DB] | strengths: [Clear AAA structure, Good assertions] | recommendations: [Add invalid credential tests, Test session timeout, Use test DB]',
  created_at: datetime(),
  updated_at: datetime(),
  valid_from: datetime(),
  valid_to: null
})
```

---

## 4. Link Types for Validation

### Tests → Code: U4_TESTS

**From COMPLETE_TYPE_REFERENCE.md:** Test artifact covers policy/schema/capability

**Usage:** Link test to code it validates

**Fields:**
- `last_run_ts` (datetime) - When test last ran
- `pass_rate` (float) - Historical pass rate
- `run_id` (string) - Test run identifier

**Example:**
```cypher
MATCH (test:U4_Code_Artifact {path: 'tests/auth/test_user_auth.py::test_valid'})
MATCH (code:U4_Code_Artifact {path: 'src/auth/user_auth.py::authenticate'})
CREATE (test)-[:U4_TESTS {
  last_run_ts: datetime('2025-11-04T10:30:00Z'),
  pass_rate: 0.98,
  run_id: 'test-run-12345',
  confidence: 0.9
}]->(code)
```

---

### Measurements → Metrics: U4_MEASURES

**From COMPLETE_TYPE_REFERENCE.md:** Measurement measures a Metric

**Usage:** Link coverage measurement to metric definition

**Fields:**
- `measurement_unit` (string) - Unit of measurement

**Example:**
```cypher
MATCH (measurement:U4_Measurement {metric_ref: 'branch_coverage_global'})
MATCH (metric:U4_Metric {name: 'branch_coverage_global'})
CREATE (measurement)-[:U4_MEASURES {
  measurement_unit: 'percentage'
}]->(metric)
```

---

## 5. Coverage Measurement Implementation (Per Language)

### Python (scopelock)
**Tool:** `pytest-cov` (wraps coverage.py)

**Command:**
```bash
cd /path/to/scopelock
pytest --cov=src --cov-report=json --cov-report=html tests/
```

**Output:** `coverage.json` + `htmlcov/`

**Parsing:**
```python
import json
from pathlib import Path

def measure_python_coverage(repo_path: Path) -> dict:
    """
    Run pytest-cov, parse JSON, extract metrics.
    """
    import subprocess

    result = subprocess.run(
        ["pytest", "--cov=src", "--cov-report=json", "tests/"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )

    coverage_file = repo_path / "coverage.json"

    if not coverage_file.exists():
        return {"error": "Coverage file not generated"}

    with open(coverage_file) as f:
        data = json.load(f)

    return {
        "line_coverage": data["totals"]["percent_covered"] / 100,
        "branch_coverage": data["totals"].get("branch_covered", 0) / 100,
        "num_statements": data["totals"]["num_statements"],
        "missing_lines": data["totals"]["missing_lines"],
        "files": {
            path: {
                "line_coverage": details["summary"]["percent_covered"] / 100,
                "missing_lines": details["missing_lines"]
            }
            for path, details in data["files"].items()
        }
    }
```

---

### JavaScript/TypeScript
**Tool:** `nyc` + `jest`

**Command:**
```bash
nyc --reporter=json --reporter=html jest
```

**Parsing:**
```python
def measure_js_coverage(repo_path: Path) -> dict:
    result = subprocess.run(
        ["nyc", "--reporter=json", "jest"],
        cwd=repo_path,
        capture_output=True
    )

    summary_file = repo_path / "coverage" / "coverage-summary.json"

    with open(summary_file) as f:
        data = json.load(f)

    return {
        "line_coverage": data["total"]["lines"]["pct"] / 100,
        "branch_coverage": data["total"]["branches"]["pct"] / 100,
        "function_coverage": data["total"]["functions"]["pct"] / 100
    }
```

---

### Go
**Tool:** `go test -cover`

**Command:**
```bash
go test -coverprofile=coverage.out ./...
go tool cover -func=coverage.out
```

**Parsing:**
```python
def measure_go_coverage(repo_path: Path) -> dict:
    subprocess.run(
        ["go", "test", "-coverprofile=coverage.out", "./..."],
        cwd=repo_path
    )

    result = subprocess.run(
        ["go", "tool", "cover", "-func=coverage.out"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )

    # Parse "total: (statements) XX.X%"
    for line in result.stdout.split('\n'):
        if 'total:' in line:
            pct = float(line.split()[-1].rstrip('%'))
            return {"statement_coverage": pct / 100}
```

---

## 6. My Stage 6 Process (Hour 4: Vera)

**Input from Kai/Nora:**
- Code artifacts extracted (U4_Code_Artifact nodes)
- Behavior specs identified (U4_Knowledge_Object nodes with ko_type: spec)

**My 2-hour process:**

### Step 1: Find Test Files (10 min)
```python
from pathlib import Path

def find_test_files(repo_path: Path, language: str) -> list:
    """
    Find all test files.
    """
    if language == "python":
        patterns = ["**/test_*.py", "**/*_test.py", "tests/**/*.py"]
    elif language in ["javascript", "typescript"]:
        patterns = ["**/*.test.ts", "**/*.test.js", "**/__tests__/*.ts"]
    elif language == "go":
        patterns = ["**/*_test.go"]

    test_files = []
    for pattern in patterns:
        test_files.extend(repo_path.glob(pattern))

    return test_files
```

---

### Step 2: Run Coverage Analysis (30 min)
```python
def run_coverage_for_scopelock(repo_path: Path) -> dict:
    """
    Scopelock is Python, use pytest-cov.
    """
    return measure_python_coverage(repo_path)
```

---

### Step 3: Extract Test Functions (20 min)
```python
import ast

def extract_test_functions(test_file: Path) -> list:
    """
    Parse test file, extract individual test functions.
    """
    with open(test_file) as f:
        tree = ast.parse(f.read())

    tests = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
            tests.append({
                "name": node.name,
                "path": f"{test_file}::{node.name}",
                "lineno": node.lineno,
                "docstring": ast.get_docstring(node) or ""
            })

    return tests
```

---

### Step 4: Map Tests to Code (20 min)
```python
def map_tests_to_code(test_functions: list, code_artifacts: list) -> dict:
    """
    Link tests to code they validate.

    Strategy:
    1. Parse test function name: test_<module>_<function>_<scenario>
    2. Match to code artifact path
    3. Create U4_TESTS links
    """
    mapping = {}

    for test in test_functions:
        # Example: tests/auth/test_user_auth.py::test_authenticate_valid_credentials
        # Should map to: src/auth/user_auth.py::authenticate

        # Extract module from test path
        parts = test["path"].split("::")
        test_file = Path(parts[0])
        test_func = parts[1] if len(parts) > 1 else test["name"]

        # Guess corresponding source file
        source_guess = test_file.name.replace("test_", "").replace("_test", "")

        # Find matching code artifact
        for code in code_artifacts:
            if source_guess in code["path"]:
                mapping[test["path"]] = code["path"]
                break

    return mapping
```

---

### Step 5: Identify Coverage Gaps (15 min)
```python
def identify_gaps(
    coverage_data: dict,
    code_artifacts: list,
    test_mapping: dict
) -> list:
    """
    Find untested code, critical paths with low coverage.
    """
    gaps = []

    # Untested files
    tested_files = set(test_mapping.values())
    all_files = set(artifact["path"] for artifact in code_artifacts)
    untested = all_files - tested_files

    for file in untested:
        gaps.append({
            "gap_type": "missing_tests",
            "affected_files": [file],
            "severity": "critical" if is_critical_path(file) else "medium",
            "description": f"{file} has no tests"
        })

    # Low coverage in critical paths
    for file, coverage in coverage_data["files"].items():
        if is_critical_path(file) and coverage["line_coverage"] < 0.80:
            gaps.append({
                "gap_type": "untested_critical_path",
                "affected_files": [file],
                "severity": "critical",
                "description": f"{file} has {coverage['line_coverage']*100:.1f}% coverage (critical path, target >80%)"
            })

    return gaps

def is_critical_path(file_path: str) -> bool:
    """
    Heuristic: auth, payment, user, security = critical.
    """
    critical_keywords = ["auth", "payment", "user", "security", "credential"]
    return any(keyword in file_path.lower() for keyword in critical_keywords)
```

---

### Step 6: Assess Test Quality (20 min)
```python
def assess_test_quality(test_file: Path) -> dict:
    """
    Score test quality (0-1).
    """
    with open(test_file) as f:
        tree = ast.parse(f.read())

    score = 0.0
    issues = []
    strengths = []

    # Check: Has assertions
    assertion_count = sum(1 for node in ast.walk(tree) if isinstance(node, ast.Assert))
    if assertion_count > 0:
        score += 0.3
        strengths.append("Has assertions")
    else:
        issues.append("No assertions found")

    # Check: Has error handling tests (try/except, pytest.raises)
    has_error_tests = any(
        isinstance(node, ast.ExceptHandler) or
        (isinstance(node, ast.Call) and "raises" in ast.unparse(node))
        for node in ast.walk(tree)
    )
    if has_error_tests:
        score += 0.3
        strengths.append("Tests error handling")
    else:
        issues.append("No error handling tests")

    # Check: Not mock-heavy
    mock_count = sum(1 for node in ast.walk(tree) if "Mock" in ast.unparse(node))
    if mock_count < assertion_count * 0.5:
        score += 0.2
        strengths.append("Reasonable mock usage")
    else:
        issues.append("Mock-heavy (may not test real behavior)")

    # Check: Has docstrings
    has_docstrings = any(
        ast.get_docstring(node)
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef)
    )
    if has_docstrings:
        score += 0.2
        strengths.append("Well-documented tests")

    return {
        "test_file": str(test_file),
        "quality_score": score,
        "issues": issues,
        "strengths": strengths
    }
```

---

### Step 7: Persist to Graph (10 min)
```python
def persist_validation_results(
    coverage_data: dict,
    test_functions: list,
    test_mapping: dict,
    gaps: list,
    quality_assessments: list,
    graph: FalkorDBAdapter,
    scope_ref: str  # e.g., "scopelock"
):
    """
    Create U4_Measurement, U4_Assessment nodes.
    """
    from datetime import datetime

    timestamp = datetime.now()

    # 1. Create coverage metric (if not exists)
    metric_id = f"{scope_ref}_line_coverage_global"
    graph.persist_node("U4_Metric", {
        "name": metric_id,
        "definition": "Global line coverage for codebase",
        "unit": "percentage",
        "level": "L2",
        "scope_ref": scope_ref
    })

    # 2. Create coverage measurement
    graph.persist_node("U4_Measurement", {
        "metric_ref": metric_id,
        "value": coverage_data["line_coverage"],
        "timestamp": timestamp,
        "level": "L2",
        "scope_ref": scope_ref,
        "description": f"commit: {coverage_data.get('commit', 'HEAD')} | tool: pytest-cov"
    })

    # 3. Create test artifacts
    for test in test_functions:
        graph.persist_node("U4_Code_Artifact", {
            "path": test["path"],
            "lang": "py",
            "repo": scope_ref,
            "description": test["docstring"],
            "level": "L2",
            "scope_ref": scope_ref
        })

    # 4. Create U4_TESTS links
    for test_path, code_path in test_mapping.items():
        graph.persist_link(test_path, code_path, "U4_TESTS", {
            "last_run_ts": timestamp,
            "confidence": 0.85
        })

    # 5. Create validation gaps (U4_Assessment)
    for gap in gaps:
        graph.persist_node("U4_Assessment", {
            "name": gap["description"].replace(" ", "_")[:50],
            "domain": "performance",
            "assessor_ref": "Vera",
            "score": 0.0 if gap["severity"] == "critical" else 0.5,
            "level": "L2",
            "scope_ref": scope_ref,
            "description": gap["description"],
            "detailed_description": f"gap_type: {gap['gap_type']} | severity: {gap['severity']} | affected: {gap['affected_files']}"
        })

    # 6. Create test quality assessments
    for assessment in quality_assessments:
        graph.persist_node("U4_Assessment", {
            "name": Path(assessment["test_file"]).stem + "_quality",
            "domain": "performance",
            "assessor_ref": "Vera",
            "score": assessment["quality_score"],
            "level": "L2",
            "scope_ref": scope_ref,
            "description": f"Test quality for {assessment['test_file']}",
            "detailed_description": f"quality_score: {assessment['quality_score']} | issues: {assessment['issues']} | strengths: {assessment['strengths']}"
        })
```

---

### Step 8: Generate Report (10 min)
```python
def generate_validation_report(
    coverage_data: dict,
    gaps: list,
    quality_assessments: list
) -> dict:
    """
    Output to Mel for coordination.
    """
    avg_quality = sum(a["quality_score"] for a in quality_assessments) / len(quality_assessments)

    critical_gaps = [g for g in gaps if g["severity"] == "critical"]

    return {
        "overall_coverage": {
            "line_coverage": coverage_data["line_coverage"],
            "branch_coverage": coverage_data.get("branch_coverage", 0),
            "files_measured": len(coverage_data["files"])
        },
        "gaps_found": len(gaps),
        "critical_gaps": len(critical_gaps),
        "test_quality_score": avg_quality,
        "recommendations": [
            f"Fix {len(critical_gaps)} critical gaps",
            f"Improve test quality (current avg: {avg_quality:.2f}, target: >0.70)",
            "Add error handling tests for modules with none"
        ],
        "status": "READY" if len(critical_gaps) == 0 and avg_quality > 0.70 else "NEEDS_WORK"
    }
```

---

## 7. Scopelock Execution Plan (My 2-3 Day Task)

### Day 1: Setup + Initial Analysis (6-8 hours)
1. **Clone scopelock** (10 min)
   ```bash
   cd /tmp
   git clone https://github.com/mind-protocol/scopelock
   cd scopelock
   ```

2. **Install dependencies** (10 min)
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install pytest-cov  # Coverage tool
   ```

3. **Run existing tests** (if any) (20 min)
   ```bash
   pytest -v
   ```

4. **Run coverage analysis** (30 min)
   ```bash
   pytest --cov=src --cov-report=json --cov-report=html
   ```

5. **Parse coverage results** (1 hour)
   - Extract line/branch coverage
   - Identify untested files
   - Flag critical paths (auth, access control)

6. **Extract test functions** (2 hours)
   - Parse test files with AST
   - Extract test names, docstrings
   - Create U4_Code_Artifact nodes for tests

7. **Map tests to code** (2 hours)
   - Link test functions to source functions
   - Create U4_TESTS links

---

### Day 2: Gap Analysis + Quality Assessment (6-8 hours)
1. **Identify validation gaps** (2 hours)
   - Untested files
   - Critical paths with <80% coverage
   - Specs without tests

2. **Assess test quality** (3 hours)
   - Run quality scoring on all test files
   - Detect weak tests (no assertions, mock-heavy, happy path only)
   - Create U4_Assessment nodes

3. **Generate validation strategy** (1 hour)
   - Prioritize gaps by severity
   - Propose test additions
   - Estimate effort

4. **Document findings** (1-2 hours)
   - Write validation report
   - Create recommendations
   - Update SYNC.md

---

### Day 3: Persist to Graph + Handoff (2-4 hours)
1. **Create FalkorDB nodes** (2 hours)
   - U4_Metric (coverage metrics)
   - U4_Measurement (coverage datapoints)
   - U4_Assessment (gaps + quality)
   - U4_Code_Artifact (test files)

2. **Create links** (1 hour)
   - U4_TESTS (test → code)
   - U4_MEASURES (measurement → metric)

3. **Verify in graph** (30 min)
   - Query FalkorDB
   - Check node counts
   - Validate links

4. **Handoff to Mel** (30 min)
   - Deliver validation report
   - Present recommendations
   - Update SYNC.md

---

## 8. Success Criteria (Phase 1, End of Week 1)

**My deliverables for scopelock:**

1. **Coverage metrics:** Line/branch coverage measured, persisted as U4_Measurement nodes
2. **Test extraction:** All test functions extracted as U4_Code_Artifact nodes
3. **Test mapping:** U4_TESTS links created (test → code)
4. **Gap identification:** Validation gaps identified, persisted as U4_Assessment nodes
5. **Quality assessment:** Test quality scored, weak tests flagged
6. **Validation report:** Delivered to Mel with recommendations

**Acceptance:**
- Coverage >70% (scopelock is mature project, expect decent coverage)
- Critical paths identified (access control = critical)
- At least 20 U4_Assessment nodes (gaps + quality assessments)
- Report includes actionable recommendations

---

## 9. Tools & Dependencies

**Required:**
- Python 3.9+ (for scopelock)
- `pytest-cov` (coverage tool)
- FalkorDB adapter (from Nora's Day 1 work)

**Install:**
```bash
pip install pytest-cov
```

---

## 10. Summary

**Validation strategy uses Mind Protocol U4_ types:**
- Tests → U4_Code_Artifact (with path granularity)
- Metrics → U4_Metric
- Measurements → U4_Measurement
- Gaps → U4_Assessment (domain: performance)
- Quality → U4_Assessment (domain: performance)

**My Stage 6 process defined (2 hours):**
1. Find tests (10 min)
2. Run coverage (30 min)
3. Extract test functions (20 min)
4. Map tests to code (20 min)
5. Identify gaps (15 min)
6. Assess quality (20 min)
7. Persist to graph (10 min)
8. Generate report (10 min)

**Scopelock execution plan (2-3 days):**
- Day 1: Setup + initial analysis
- Day 2: Gap analysis + quality assessment
- Day 3: Persist to graph + handoff

**Status:** READY to execute on scopelock

---

**Vera - Chief Validator**
*"If it's not tested, it's not built."*
