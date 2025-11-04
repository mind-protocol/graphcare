# GraphCare Extraction Workflow - Practical Implementation

**Author:** Mel "Bridgekeeper" - Chief Care Coordinator
**Date:** 2025-11-04
**Purpose:** Step-by-step operational workflow for client knowledge graph extraction

---

## Directory Structure

```
/home/mind-protocol/graphcare/
├── orchestration/          # Extraction pipeline code
│   ├── extraction/         # AST parsers, classifiers
│   ├── analysis/          # Coverage, security, quality
│   ├── docs/              # Documentation generator
│   └── adapters/          # FalkorDB, embedding service
├── app/
│   └── client-docs/       # Next.js website template
├── docs/                  # GraphCare documentation
├── citizens/              # Citizen identities (CLAUDE.md, SYNC.md)
└── orgs/                  # CLIENT WORK DIRECTORY
    └── {client_name}/     # One directory per client
        ├── repo/          # Cloned client repository
        ├── extraction/    # Extraction pipeline outputs
        ├── docs/          # Generated documentation
        ├── reports/       # Analysis reports
        └── config/        # Client-specific configuration
```

---

## Scopelock Extraction Workflow (Step-by-Step)

### Stage 0: Client Setup (One-Time)

**Owner:** Mel
**Time:** 15-30 minutes

```bash
# 1. Create client directory structure
cd /home/mind-protocol/graphcare
mkdir -p orgs/scopelock/{repo,extraction,docs,reports,config}

# 2. Clone client repository
cd orgs/scopelock/repo
git clone https://github.com/mind-protocol/scopelock.git .

# 3. Create client configuration
cd ../config
cat > extraction_config.yaml << 'EOF'
client:
  name: "scopelock"
  graph_name: "scopelock"
  scope_ref: "org_scopelock"
  level: "L2"

repository:
  path: "/home/mind-protocol/graphcare/orgs/scopelock/repo"
  main_branch: "main"
  ignore_patterns:
    - "node_modules/"
    - "__pycache__/"
    - ".git/"
    - "*.pyc"
    - "venv/"

extraction:
  languages:
    - python
  include_tests: true
  include_docs: true
  min_confidence_auto_accept: 0.9

quality_gates:
  min_coverage_critical: 0.80
  min_coverage_overall: 0.70
  max_critical_vulnerabilities: 0
  max_high_vulnerabilities: 5

deliverables:
  graph_export: true
  documentation_site: true
  cli_tool: true
  health_dashboard: true
EOF

# 4. Create FalkorDB graph
python -c "
from orchestration.adapters.storage.falkordb_adapter import FalkorDBAdapter

adapter = FalkorDBAdapter()
adapter.create_graph('scopelock')
print('✅ Graph created: scopelock')
"
```

**Output:** Client directory structure created, repo cloned, config defined, FalkorDB graph initialized

---

### Stage 1: Corpus Analysis (Quinn)

**Owner:** Quinn
**Time:** 2-4 hours
**Working Directory:** `/home/mind-protocol/graphcare/orgs/scopelock/`

**Step 1: Initial Repository Scan**

```bash
cd /home/mind-protocol/graphcare

# Run corpus analyzer
python orchestration/extraction/corpus_analyzer.py \
  --repo orgs/scopelock/repo \
  --config orgs/scopelock/config/extraction_config.yaml \
  --output orgs/scopelock/reports/corpus_analysis.json
```

**Output:** `orgs/scopelock/reports/corpus_analysis.json`

```json
{
  "file_count": 45,
  "language_distribution": {
    "python": 38,
    "markdown": 5,
    "yaml": 2
  },
  "total_lines": 8234,
  "code_lines": 6421,
  "comment_lines": 1102,
  "doc_lines": 711,
  "doc_to_code_ratio": 0.11,
  "estimated_complexity": "medium"
}
```

---

**Step 2: Document Classification**

```bash
# Classify documentation files
python orchestration/extraction/type_classifier.py \
  --repo orgs/scopelock/repo \
  --file-types markdown,rst,txt \
  --output orgs/scopelock/extraction/doc_classification.json
```

**Output:** `orgs/scopelock/extraction/doc_classification.json`

```json
[
  {
    "file": "README.md",
    "type": "U4_Knowledge_Object",
    "ko_type": "guide",
    "confidence": 0.95,
    "reason": "README pattern, getting started content"
  },
  {
    "file": "docs/architecture.md",
    "type": "U4_Knowledge_Object",
    "ko_type": "spec",
    "confidence": 0.88,
    "reason": "Architecture documentation pattern"
  }
]
```

---

**Step 3: Semantic Clustering**

```bash
# Generate embeddings and cluster
python orchestration/extraction/semantic_clusterer.py \
  --repo orgs/scopelock/repo \
  --config orgs/scopelock/config/extraction_config.yaml \
  --output orgs/scopelock/extraction/semantic_clusters.json
```

**Output:** `orgs/scopelock/extraction/semantic_clusters.json`

```json
{
  "clusters": [
    {
      "cluster_id": "cluster_0",
      "label": "authentication_authorization",
      "member_count": 12,
      "coherence": 0.82,
      "members": [
        "scopelock/auth/jwt_handler.py",
        "scopelock/auth/permissions.py",
        "docs/security.md"
      ]
    },
    {
      "cluster_id": "cluster_1",
      "label": "repository_access_control",
      "member_count": 8,
      "coherence": 0.76,
      "members": [
        "scopelock/core/access_manager.py",
        "scopelock/models/repository.py"
      ]
    }
  ]
}
```

---

**Step 4: Create U4_Subentity Nodes (Semantic Clusters)**

```bash
# Insert clusters to FalkorDB
python orchestration/extraction/insert_clusters.py \
  --graph scopelock \
  --clusters orgs/scopelock/extraction/semantic_clusters.json \
  --scope-ref org_scopelock
```

**Output:** U4_Subentity nodes created in `scopelock` graph

---

**Quinn's Deliverable:**
- `orgs/scopelock/reports/corpus_analysis.json` - Overview of codebase
- `orgs/scopelock/extraction/doc_classification.json` - Classified documentation
- `orgs/scopelock/extraction/semantic_clusters.json` - Identified themes
- FalkorDB: U4_Subentity nodes (semantic clusters) + U4_Knowledge_Object nodes (docs)

**Handoff to:** Kai (corpus stats inform code extraction priority)

---

### Stage 2: Code Extraction (Kai)

**Owner:** Kai
**Time:** 4-6 hours
**Working Directory:** `/home/mind-protocol/graphcare/orgs/scopelock/`

**Step 1: Python AST Extraction**

```bash
cd /home/mind-protocol/graphcare

# Extract code structure
python orchestration/extraction/python_extractor.py \
  --repo orgs/scopelock/repo \
  --config orgs/scopelock/config/extraction_config.yaml \
  --output orgs/scopelock/extraction/code_structure.json
```

**Output:** `orgs/scopelock/extraction/code_structure.json`

```json
{
  "files": [
    {
      "path": "scopelock/auth/jwt_handler.py",
      "classes": [
        {
          "name": "JWTHandler",
          "methods": ["encode", "decode", "verify"],
          "line": 15,
          "complexity": 8
        }
      ],
      "functions": [
        {
          "name": "create_token",
          "params": ["user_id", "expiry"],
          "returns": "str",
          "line": 45,
          "complexity": 3
        }
      ],
      "imports": [
        {"module": "jwt", "type": "external"},
        {"module": "datetime", "type": "stdlib"}
      ]
    }
  ],
  "summary": {
    "total_files": 38,
    "total_classes": 24,
    "total_functions": 156,
    "avg_complexity": 4.2,
    "max_complexity": 15
  }
}
```

---

**Step 2: Dependency Graph Construction**

```bash
# Build dependency graph
python orchestration/extraction/dependency_graph.py \
  --code-structure orgs/scopelock/extraction/code_structure.json \
  --output orgs/scopelock/extraction/dependencies.json
```

**Output:** `orgs/scopelock/extraction/dependencies.json`

```json
{
  "nodes": [
    {"id": "scopelock/auth/jwt_handler.py", "type": "module"},
    {"id": "scopelock/core/access_manager.py", "type": "module"}
  ],
  "edges": [
    {
      "source": "scopelock/core/access_manager.py",
      "target": "scopelock/auth/jwt_handler.py",
      "type": "U4_DEPENDS_ON",
      "dependency_type": "build_time"
    }
  ],
  "circular_dependencies": [
    {
      "cycle": ["module_a.py", "module_b.py", "module_a.py"],
      "severity": "medium"
    }
  ]
}
```

---

**Step 3: Insert to FalkorDB**

```bash
# Insert code structure to graph
python orchestration/extraction/insert_code.py \
  --graph scopelock \
  --code-structure orgs/scopelock/extraction/code_structure.json \
  --dependencies orgs/scopelock/extraction/dependencies.json \
  --scope-ref org_scopelock
```

**Output:**
- U4_Code_Artifact nodes (files, classes, functions with path granularity)
- U4_DEPENDS_ON links (imports, calls)

---

**Step 4: Generate Embeddings for Code**

```bash
# Generate embeddings for all code artifacts
python orchestration/extraction/embed_code.py \
  --graph scopelock \
  --embedding-service-url http://localhost:8001
```

**Output:** All U4_Code_Artifact nodes have `embedding` field populated

---

**Kai's Deliverable:**
- `orgs/scopelock/extraction/code_structure.json` - AST extraction results
- `orgs/scopelock/extraction/dependencies.json` - Dependency graph
- FalkorDB: U4_Code_Artifact nodes + U4_DEPENDS_ON links
- `orgs/scopelock/reports/code_quality.md` - Complexity, circular deps

**Handoff to:** Nora (code structure for architecture inference), Vera (code paths for coverage)

---

### Stage 3: Architecture Inference (Nora)

**Owner:** Nora
**Time:** 3-4 hours
**Working Directory:** `/home/mind-protocol/graphcare/orgs/scopelock/`

**Step 1: Infer Architecture Components**

```bash
# Analyze code structure to infer architecture
python orchestration/analysis/architecture_inference.py \
  --graph scopelock \
  --dependencies orgs/scopelock/extraction/dependencies.json \
  --output orgs/scopelock/extraction/architecture.json
```

**Output:** `orgs/scopelock/extraction/architecture.json`

```json
{
  "components": [
    {
      "name": "Authentication Layer",
      "type": "service",
      "modules": ["scopelock/auth/*"],
      "responsibilities": "JWT handling, permission checks",
      "dependencies": ["Core Layer"]
    },
    {
      "name": "Core Layer",
      "type": "service",
      "modules": ["scopelock/core/*"],
      "responsibilities": "Access control logic, repository management"
    }
  ],
  "pattern": "layered_architecture",
  "confidence": 0.85
}
```

---

**Step 2: Extract/Infer Behavior Specs**

```bash
# Extract behavior specs from docs + docstrings
python orchestration/analysis/behavior_spec_extractor.py \
  --graph scopelock \
  --docs orgs/scopelock/repo/docs \
  --output orgs/scopelock/extraction/behavior_specs.json
```

**Output:** `orgs/scopelock/extraction/behavior_specs.json`

```json
[
  {
    "spec_id": "spec_auth_001",
    "name": "JWT Token Generation",
    "description": "System must generate secure JWT tokens for authenticated users",
    "preconditions": ["User authenticated", "User has valid credentials"],
    "postconditions": ["JWT token returned", "Token contains user_id and expiry"],
    "success_criteria": "Token validates successfully and contains correct claims",
    "implemented_by": ["scopelock/auth/jwt_handler.py::JWTHandler::encode"],
    "confidence": 0.92
  }
]
```

---

**Step 3: Insert Architecture to FalkorDB**

```bash
# Insert architecture components and behavior specs
python orchestration/extraction/insert_architecture.py \
  --graph scopelock \
  --architecture orgs/scopelock/extraction/architecture.json \
  --behavior-specs orgs/scopelock/extraction/behavior_specs.json \
  --scope-ref org_scopelock
```

**Output:**
- U4_Subentity nodes (kind: functional - for architecture components)
- U4_Knowledge_Object nodes (ko_type: spec - for behavior specs)
- U4_IMPLEMENTS links (code → spec)

---

**Step 4: Generate Architecture Diagrams**

```bash
# Generate C4 diagrams
python orchestration/docs/generate_diagrams.py \
  --graph scopelock \
  --output orgs/scopelock/docs/diagrams/
```

**Output:**
- `orgs/scopelock/docs/diagrams/architecture_context.svg`
- `orgs/scopelock/docs/diagrams/architecture_components.svg`
- `orgs/scopelock/docs/diagrams/dependency_graph.svg`

---

**Nora's Deliverable:**
- `orgs/scopelock/extraction/architecture.json` - Inferred architecture
- `orgs/scopelock/extraction/behavior_specs.json` - Extracted/inferred specs
- FalkorDB: Architecture components + behavior specs + implementation links
- `orgs/scopelock/docs/diagrams/` - C4 diagrams

**Handoff to:** Vera (behavior specs for validation), Sage (diagrams for documentation)

---

### Stage 4: Coverage & Security Analysis (Vera + Marcus, Parallel)

#### Vera: Coverage Analysis

**Owner:** Vera
**Time:** 2-3 hours

**Step 1: Run Coverage Tools**

```bash
cd /home/mind-protocol/graphcare/orgs/scopelock/repo

# Run pytest with coverage
pytest --cov=scopelock --cov-report=json --cov-report=html

# Copy coverage results
cp coverage.json ../../extraction/coverage.json
cp -r htmlcov ../../reports/coverage_html/
```

---

**Step 2: Extract Coverage Metrics**

```bash
cd /home/mind-protocol/graphcare

# Parse coverage and create metrics
python orchestration/analysis/coverage_pipeline.py \
  --graph scopelock \
  --coverage orgs/scopelock/extraction/coverage.json \
  --code-structure orgs/scopelock/extraction/code_structure.json
```

**Output:**
- U4_Metric nodes (coverage_line, coverage_branch, coverage_path)
- U4_Measurement nodes (coverage values per file/function)
- U4_MEASURES links (measurement → code artifact)

---

**Step 3: Identify Coverage Gaps**

```bash
# Generate gap report
python orchestration/analysis/coverage_gap_analyzer.py \
  --graph scopelock \
  --behavior-specs orgs/scopelock/extraction/behavior_specs.json \
  --output orgs/scopelock/reports/coverage_gaps.md
```

**Output:** `orgs/scopelock/reports/coverage_gaps.md`

```markdown
# Coverage Gap Analysis - Scopelock

## Summary
- Overall coverage: 72%
- Critical path coverage: 85%
- Untested functions: 24

## Critical Gaps

### 1. JWT Token Verification (HIGH PRIORITY)
- Function: `scopelock/auth/jwt_handler.py::JWTHandler::verify`
- Coverage: 0%
- Criticality: HIGH (authentication logic)
- Recommendation: Add integration tests for token validation

### 2. Access Control Decision Engine
- Function: `scopelock/core/access_manager.py::AccessManager::check_permission`
- Coverage: 45%
- Missing branches: Error handling, edge cases
- Recommendation: Add unit tests for permission denial scenarios
```

---

**Vera's Deliverable:**
- `orgs/scopelock/extraction/coverage.json` - Raw coverage data
- `orgs/scopelock/reports/coverage_html/` - HTML coverage report
- FalkorDB: Coverage metrics + measurements
- `orgs/scopelock/reports/coverage_gaps.md` - Gap analysis

---

#### Marcus: Security Analysis

**Owner:** Marcus
**Time:** 2-3 hours

**Step 1: Run Security Scanners**

```bash
cd /home/mind-protocol/graphcare/orgs/scopelock/repo

# Bandit (Python security)
bandit -r scopelock -f json -o ../../extraction/bandit_results.json

# Safety (dependency audit)
safety check --json --output ../../extraction/safety_results.json

# TruffleHog (secret detection)
trufflehog filesystem . --json > ../../extraction/trufflehog_results.json
```

---

**Step 2: Parse Security Results**

```bash
cd /home/mind-protocol/graphcare

# Parse and insert to graph
python orchestration/analysis/security_pipeline.py \
  --graph scopelock \
  --bandit orgs/scopelock/extraction/bandit_results.json \
  --safety orgs/scopelock/extraction/safety_results.json \
  --trufflehog orgs/scopelock/extraction/trufflehog_results.json
```

**Output:**
- U4_Assessment nodes (domain: security, severity scores)
- U4_EVIDENCED_BY links (assessment → code artifact)

---

**Step 3: Generate Security Report**

```bash
# Create security report
python orchestration/analysis/security_report_generator.py \
  --graph scopelock \
  --output orgs/scopelock/reports/security_report.md
```

**Output:** `orgs/scopelock/reports/security_report.md`

```markdown
# Security Analysis - Scopelock

## Executive Summary
- CRITICAL vulnerabilities: 0 ✅
- HIGH vulnerabilities: 2 ⚠️
- MEDIUM vulnerabilities: 5
- LOW vulnerabilities: 8

## Critical Findings

### None ✅

## High Priority Findings

### 1. Hardcoded Secret Detected
- **Severity:** HIGH
- **File:** `scopelock/config/settings.py:15`
- **Issue:** JWT secret key appears to be hardcoded
- **Remediation:** Move to environment variable
- **Status:** OPEN

### 2. SQL Injection Risk
- **Severity:** HIGH
- **File:** `scopelock/core/query_builder.py:45`
- **Issue:** User input concatenated into SQL query
- **Remediation:** Use parameterized queries
- **Status:** OPEN
```

---

**Marcus's Deliverable:**
- `orgs/scopelock/extraction/bandit_results.json` - Security scan results
- `orgs/scopelock/extraction/safety_results.json` - Dependency audit
- FalkorDB: Security assessments
- `orgs/scopelock/reports/security_report.md` - Findings + remediation

---

### Stage 5: Documentation Generation (Sage)

**Owner:** Sage
**Time:** 3-4 hours
**Working Directory:** `/home/mind-protocol/graphcare/orgs/scopelock/`

**Step 1: Generate Auto-Documentation**

```bash
cd /home/mind-protocol/graphcare

# Generate markdown docs from graph
python orchestration/docs/generator.py \
  --graph scopelock \
  --templates orchestration/docs/templates \
  --output orgs/scopelock/docs/generated
```

**Output:** `orgs/scopelock/docs/generated/`
- `architecture.md` - Architecture overview
- `api_reference.md` - API documentation
- `code_reference.md` - Function/class reference
- `dependencies.md` - Dependency analysis
- `coverage.md` - Coverage report
- `security.md` - Security findings

---

**Step 2: Write Human Narratives**

**Sage manually writes:**

`orgs/scopelock/docs/narratives/executive_summary.md`
```markdown
# Scopelock - Executive Summary

Scopelock is a repository access control system that provides fine-grained
permission management for code repositories. The system is built on a layered
architecture with strong separation between authentication, authorization,
and core access control logic.

## Key Strengths
- Well-structured authentication layer (JWT-based)
- Clear separation of concerns (layered architecture)
- 72% overall test coverage (above industry average)

## Areas for Improvement
- 2 HIGH-severity security issues require immediate attention
- Several critical functions lack test coverage
- Dependency audit shows 1 outdated package with known CVE
```

---

**Step 3: Build Next.js Website**

```bash
cd /home/mind-protocol/graphcare/app/client-docs

# Build site for scopelock
npm run build -- --client=scopelock

# Deploy to Vercel
vercel deploy --prod \
  --name docs-scopelock \
  --alias docs.scopelock.mindprotocol.ai
```

**Output:** Website live at `docs.scopelock.mindprotocol.ai`

---

**Sage's Deliverable:**
- `orgs/scopelock/docs/generated/` - Auto-generated documentation
- `orgs/scopelock/docs/narratives/` - Human-written summaries
- Website deployed: `docs.scopelock.mindprotocol.ai`

---

### Stage 6: Quality Gate Validation (Mel)

**Owner:** Mel
**Time:** 1-2 hours

**Step 1: Run Acceptance Queries**

```bash
cd /home/mind-protocol/graphcare

# Run 20 acceptance queries
python orchestration/validation/acceptance_tests.py \
  --graph scopelock \
  --queries orgs/scopelock/config/acceptance_queries.yaml \
  --output orgs/scopelock/reports/acceptance_results.json
```

**Output:** `orgs/scopelock/reports/acceptance_results.json`

```json
{
  "total_queries": 20,
  "passed": 20,
  "failed": 0,
  "pass_rate": 1.0,
  "results": [
    {
      "query_id": "Q1",
      "description": "Find all authentication-related code",
      "status": "PASS",
      "result_count": 12
    }
  ]
}
```

---

**Step 2: Quality Gate Checklist**

```bash
# Run quality gate validation
python orchestration/validation/quality_gates.py \
  --graph scopelock \
  --config orgs/scopelock/config/extraction_config.yaml \
  --output orgs/scopelock/reports/quality_gates.md
```

**Output:** `orgs/scopelock/reports/quality_gates.md`

```markdown
# Quality Gate Results - Scopelock

## CRITICAL Gates (MUST PASS)
- ✅ Acceptance queries: 20/20 passed
- ✅ Critical path coverage: 85% (target: 80%)
- ❌ CRITICAL vulnerabilities: 0 (target: 0)
- ⚠️  HIGH vulnerabilities: 2 (target: 0)

## IMPORTANT Gates (DOCUMENT IF FAIL)
- ⚠️  Overall coverage: 72% (target: 85%)
- ✅ GDPR compliance: Validated
- ✅ Documentation complete: Yes

## Decision
**CONDITIONAL APPROVAL** - Ship with remediation plan for 2 HIGH vulnerabilities

## Remediation Required Before Production
1. Fix hardcoded JWT secret (scopelock/config/settings.py:15)
2. Fix SQL injection risk (scopelock/core/query_builder.py:45)
```

---

**Mel's Decision:**
- **CONDITIONAL APPROVAL** - Deliver graph + documentation
- **REMEDIATION PLAN** - Client must fix 2 HIGH vulnerabilities before production deployment
- **DELIVERY PACKAGE:** Graph export, website, CLI tool, security fixes as PRs

---

### Stage 7: Delivery Package Assembly

**Owner:** Mel + Sage
**Time:** 1 hour

```bash
cd /home/mind-protocol/graphcare

# Create delivery package
mkdir -p orgs/scopelock/delivery

# 1. Export FalkorDB graph
python orchestration/export/graph_exporter.py \
  --graph scopelock \
  --output orgs/scopelock/delivery/graph_export.cypher

# 2. Package CLI tool
python orchestration/export/cli_packager.py \
  --graph scopelock \
  --output orgs/scopelock/delivery/scopelock_cli.tar.gz

# 3. Generate delivery manifest
cat > orgs/scopelock/delivery/MANIFEST.md << 'EOF'
# Scopelock Knowledge Graph - Delivery Package

## Included Assets

### 1. FalkorDB Graph Export
- **File:** `graph_export.cypher`
- **Nodes:** 543
- **Links:** 1,247
- **Size:** 2.3 MB

### 2. Documentation Website
- **URL:** https://docs.scopelock.mindprotocol.ai
- **Features:** Graph explorer, semantic search, auto-generated docs, narratives

### 3. Query CLI Tool
- **File:** `scopelock_cli.tar.gz`
- **Usage:** `./scopelock_cli query "find authentication logic"`
- **Docs:** See README in archive

### 4. Reports
- Architecture analysis
- Coverage report (72% overall, 85% critical paths)
- Security report (0 CRITICAL, 2 HIGH, 5 MEDIUM, 8 LOW)

## Acceptance Criteria Results
✅ All 20 test queries passed

## Quality Gates
- ✅ CRITICAL: No blocking issues
- ⚠️  IMPORTANT: 2 HIGH vulnerabilities require remediation

## Remediation Plan
See `reports/security_report.md` for details on:
1. Hardcoded JWT secret (HIGH)
2. SQL injection risk (HIGH)

Pull requests provided in `delivery/security_fixes/`

## Support
Contact: graphcare@mindprotocol.ai
EOF

# 4. Archive delivery package
cd orgs/scopelock
tar -czf delivery_package.tar.gz delivery/
```

---

## Summary: Practical File Locations

**After full extraction, scopelock directory structure:**

```
/home/mind-protocol/graphcare/orgs/scopelock/
├── repo/                           # Cloned repository
│   └── (scopelock source code)
├── config/
│   ├── extraction_config.yaml      # Extraction configuration
│   └── acceptance_queries.yaml     # 20 test queries
├── extraction/                     # Pipeline intermediate data
│   ├── corpus_analysis.json
│   ├── doc_classification.json
│   ├── semantic_clusters.json
│   ├── code_structure.json
│   ├── dependencies.json
│   ├── architecture.json
│   ├── behavior_specs.json
│   ├── coverage.json
│   ├── bandit_results.json
│   ├── safety_results.json
│   └── trufflehog_results.json
├── docs/                          # Generated documentation
│   ├── generated/                 # Auto-generated from graph
│   │   ├── architecture.md
│   │   ├── api_reference.md
│   │   ├── code_reference.md
│   │   └── ...
│   ├── narratives/                # Human-written
│   │   ├── executive_summary.md
│   │   ├── architecture_narrative.md
│   │   └── onboarding_guide.md
│   └── diagrams/                  # Generated SVG diagrams
│       ├── architecture_context.svg
│       └── dependency_graph.svg
├── reports/                       # Analysis reports
│   ├── corpus_analysis.json
│   ├── code_quality.md
│   ├── coverage_gaps.md
│   ├── security_report.md
│   ├── acceptance_results.json
│   ├── quality_gates.md
│   └── coverage_html/             # HTML coverage report
└── delivery/                      # Delivery package
    ├── graph_export.cypher        # FalkorDB export
    ├── scopelock_cli.tar.gz       # CLI tool
    ├── security_fixes/            # Pull requests
    └── MANIFEST.md                # Delivery manifest
```

**FalkorDB:**
- Graph: `scopelock`
- Nodes: U4_Code_Artifact, U4_Knowledge_Object, U4_Subentity, U4_Metric, U4_Measurement, U4_Assessment
- Links: U4_DEPENDS_ON, U4_IMPLEMENTS, U4_DOCUMENTS, U4_MEASURES, U4_TESTS, U4_SEMANTICALLY_SIMILAR

**Website:**
- URL: `docs.scopelock.mindprotocol.ai`
- Deployed to: Vercel
- Source: `/home/mind-protocol/graphcare/app/client-docs/`

---

## Next Client: Repeat Process

For each new client:
1. `mkdir -p orgs/{client_name}/{repo,extraction,docs,reports,config}`
2. Clone repository
3. Create `extraction_config.yaml`
4. Create FalkorDB graph `graphcare_{client_name}`
5. Run extraction pipeline
6. Generate documentation
7. Deploy website to `docs.{client_name}.mindprotocol.ai`
8. Quality gates → Deliver

---

**End of Extraction Workflow**
