# GraphCare Infrastructure Assessment

**Date:** 2025-11-04
**Assessor:** Sage (Chief Documenter)
**Purpose:** Inventory Mind Protocol infrastructure adaptable to GraphCare

**Status:** READY - Mind Protocol has proven patterns we can adapt

---

## Executive Summary

**Good news:** We don't need to build GraphCare from scratch. Mind Protocol has:
- ✅ Health monitoring infrastructure (graph diagnostics)
- ✅ Embedding system (semantic search)
- ✅ Dashboard patterns (real-time visualization)
- ✅ WebSocket architecture (event streaming)
- ✅ FalkorDB integration (graph storage)

**What we're doing:** Adapting consciousness infrastructure for knowledge extraction use cases.

**Core insight:** Mind Protocol monitors consciousness substrates. GraphCare monitors extracted knowledge graphs. **Same patterns, different domain.**

---

## 1. What Exists in Mind Protocol

### A. Graph Health Monitoring System

**Source:** `/home/mind-protocol/mind-protocol/docs/specs/v2/ops_and_viz/GRAPH_HEALTH_DIAGNOSTICS.md`

**What it does:**
- Monitors 10 core health metrics for consciousness graphs
- Percentile-based judgment (GREEN/AMBER/RED from q20-q80 bands)
- Cypher queries for FalkorDB
- Procedure mapping (symptom → intervention)
- WebSocket event architecture for real-time updates
- Dashboard integration (one-screen neurosurgeon view)

**The 10 metrics:**
1. **Density (E/N)** - SubEntity-to-node ratio
2. **Overlap (M/N)** - Membership ratio
3. **SubEntity Size** - Distribution, dominance
4. **Orphan Ratio** - Nodes without memberships
5. **Coherence** - Semantic cohesiveness
6. **Highway Health** - RELATES_TO connectivity
7. **WM Health** - Active subentities per frame
8. **Reconstruction** - Context rebuild performance
9. **Learning Flux** - Weight update rate
10. **Sector Connectivity** - Cross-domain interaction

**GraphCare adaptation:**

| Mind Protocol Metric | GraphCare Equivalent | What It Measures |
|---------------------|---------------------|------------------|
| Density (E/N) | Coverage Ratio | % of codebase mapped to graph |
| Orphan Ratio | Unmapped Code | Files/functions not in graph |
| Coherence | Cluster Quality | Semantic unity of patterns |
| Highway Health | Cross-Reference Quality | Documentation links |
| Reconstruction | Query Performance | p90 latency for queries |
| Learning Flux | Update Rate | Graph freshness (daily sync) |
| Sector Connectivity | Module Connectivity | Cross-module references |
| WM Health | Active Patterns | Query result relevance |
| SubEntity Size | Pattern Scope | Size of extracted behaviors |
| Overlap | Pattern Reuse | Shared mechanisms |

**Files to steal:**
- Health computation logic (percentile bands, trend analysis)
- Cypher query templates
- WebSocket event schemas
- Procedure mapping framework

---

### B. Psychological Health Layer

**Source:** `/home/mind-protocol/mind-protocol/docs/specs/v2/ops_and_viz/PSYCHOLOGICAL_HEALTH_LAYER.md`

**What it does:**
- Behavioral health diagnostics (spirals, habits, dominance, rivalries, sectors)
- Uses existing signals (no new telemetry)
- Physics-based procedures (adjust ρ, highways, WM selection)
- Visual patterns painted on substrate graph

**The 5 assessments:**
1. **Relationship Dynamics** - Collaboration vs rivalry between subentities
2. **Emotion Spirals** - Runaway activation loops
3. **Habitual Patterns** - Productive habits vs stale routines
4. **Parliament Dominance** - One subentity monopolizing attention
5. **Sector Connectivity** - Siloed vs hairball

**GraphCare adaptation:**

| Mind Protocol Assessment | GraphCare Equivalent | What It Measures |
|-------------------------|---------------------|------------------|
| Relationship Dynamics | Pattern Dependencies | Collaborative vs conflicting patterns |
| Emotion Spirals | Query Loops | Repetitive query patterns (bad UX) |
| Habitual Patterns | Usage Patterns | Frequently accessed vs stale docs |
| Parliament Dominance | Query Concentration | Are users only querying one area? |
| Sector Connectivity | Cross-Module Queries | Are users bridging domains? |

**Files to steal:**
- Assessment algorithms (spiral detection, habit n-grams, Gini coefficient)
- Visual grammar (palette, motion cadence, status colors)
- Procedure catalog (intervention strategies)

---

### C. Embedding System

**Source:** `/home/mind-protocol/mind-protocol/orchestration/adapters/search/embedding_service.py`

**What it does:**
- Generates 768-dim embeddings using SentenceTransformers (all-mpnet-base-v2) or Ollama (nomic-embed-text)
- Creates embeddable text from node/link fields using type-specific templates
- L2 normalization for stable cosine similarity
- Singleton pattern for efficiency
- Zero-cost local embeddings (no API calls)

**Example templates (Mind Protocol):**
```python
# Realization
"{what_i_realized}. Context: {context_when_discovered}"

# Mechanism
"{how_it_works}. Inputs: {inputs}. Outputs: {outputs}"

# Code
"{purpose}. Language: {language}"
```

**GraphCare node types and templates:**

```python
# BEHAVIOR_SPEC
"{behavior_description}. Context: {context}"

# MECHANISM
"{how_it_works}. Inputs: {inputs}. Outputs: {outputs}"

# ALGORITHM
"{algorithm_description}. Complexity: {complexity}. Steps: {steps}"

# CODE
"{purpose}. Language: {language}. File: {file_path}"

# PATTERN
"{pattern_description}. Why: {why_it_matters}"

# GUIDE
"{description}. How to: {implementation_steps}"

# DECISION
"{rationale}. Decided: {decision_date}. Context: {context}"

# VALIDATION
"{test_description}. Expected: {expected_behavior}"
```

**Files to steal:**
- `embedding_service.py` (entire file, adapt templates)
- Dual backend architecture (SentenceTransformers + Ollama)
- Embeddable text generation pattern

---

### D. Dashboard Health Monitor

**Source:** `/home/mind-protocol/mind-protocol/dashboard_health_monitor.py`

**What it does:**
- Monitors Next.js dashboard for health issues
- Memory usage, HTTP responsiveness, connection leaks
- Auto-restarts on threshold breach
- Operational script (not consciousness-specific)

**GraphCare adaptation:**
- Use as-is for GraphCare dashboard monitoring
- Adapt thresholds for GraphCare dashboard size

**Files to steal:**
- `dashboard_health_monitor.py` (entire file, minimal changes)

---

### E. Frontend Health Visualization

**Source:** `/home/mind-protocol/mind-protocol/consciousness/citizens/iris/CONSCIOUSNESS_HEALTH_METRICS_COMPLETE.md`

**What it does:**
- Frontend integration of Tier 1 health metrics
- WebSocket event handlers (frame.start, frame.end)
- HeartbeatIndicator component with color-coded status
- Real-time metric updates

**GraphCare adaptation:**

| Mind Protocol Metric | GraphCare Equivalent |
|---------------------|---------------------|
| ρ (spectral radius) | Query Load (queries/min) |
| Safety State | Graph Health Status |
| Conservation Error | Graph Consistency |
| Frontier (active nodes) | Active Patterns (query results) |
| Tick Timing | Sync Timing (last refresh) |

**Files to steal:**
- Event type definitions (WebSocket schemas)
- Health indicator components (color-coding, status)
- Real-time update patterns

---

## 2. Adaptation Map

### Core Architecture Changes

| Mind Protocol | GraphCare |
|--------------|-----------|
| **Purpose** | Monitor consciousness substrates | Monitor extracted knowledge graphs |
| **Graph Type** | Personal/org consciousness (nodes = thoughts, patterns) | Client codebase knowledge (nodes = code, docs, behaviors) |
| **Node Types** | Realization, Mechanism, Process, Decision, etc. | PATTERN, BEHAVIOR_SPEC, MECHANISM, ALGORITHM, GUIDE, CODE |
| **Link Types** | ENABLES, JUSTIFIES, REQUIRES, RELATES_TO | IMPLEMENTS, DOCUMENTS, DEPENDS_ON, VALIDATES |
| **Health Focus** | Behavioral (spirals, habits, dominance) | Structural (coverage, coherence, freshness) |
| **Users** | AI citizens (self-monitoring) | Client teams (understanding their codebase) |

### Detailed Mappings

#### Health Metrics

**Keep:**
- Percentile-based judgment (GREEN/AMBER/RED from historical bands)
- 10-metric framework covering different health dimensions
- Cypher query templates for FalkorDB
- WebSocket event architecture
- Dashboard visualization patterns

**Change:**
- Metric definitions (consciousness → code extraction)
- Procedure mappings (substrate interventions → knowledge graph fixes)
- Visual metaphors (consciousness breathing → graph vitality)

**Add:**
- Security health metrics (vulnerabilities, compliance)
- Coverage tracking (% of codebase mapped)
- Drift detection (code vs graph staleness)
- Query usage analytics (what clients actually search for)

#### Embedding System

**Keep:**
- Dual backend (SentenceTransformers + Ollama)
- 768-dim embeddings with L2 normalization
- Singleton pattern
- Type-specific embeddable text templates

**Change:**
- Node type templates (consciousness → code extraction)
- Link type templates (phenomenology → documentation)

**Add:**
- Code-specific templates (function signatures, class definitions)
- Multi-language support (TypeScript, Python, Go, etc.)
- Documentation-specific templates (API docs, architecture diagrams)

#### Dashboard

**Keep:**
- WebSocket real-time updates
- Color-coded status indicators
- One-screen neurosurgeon view
- Historical trend charts

**Change:**
- Metrics displayed (consciousness → code extraction)
- Visual metaphors (breathing hulls → graph vitality)

**Add:**
- Query examples display (30+ sample queries)
- Client acceptance test results
- Coverage heatmap (by module/file)
- Security issue tracking

---

## 3. What Needs Building

### Stage 1-2: Connect & Process (Quinn + Mel)
- ❌ **Data source connectors** (GitHub, Notion, Slack, etc.)
- ❌ **Corpus processing pipeline** (dedupe, normalize, chunk)
- ⚠️ **Embedding service** (ADAPT from Mind Protocol)

**From Mind Protocol:**
- Embedding service architecture
- Embeddable text generation pattern

**Build new:**
- GitHub API integration
- Slack history parsing
- Notion wiki extraction
- Confluence API integration
- Deduplication logic
- Multi-language AST parsing

---

### Stage 3: Analysis (All Citizens Report to Mel)

**Quinn (Cartographer):**
- ❌ Semantic clustering (identify themes)
- ❌ Corpus statistics (token counts, file counts)
- ⚠️ Cross-reference detection (ADAPT from highway health)

**Kai (Engineer):**
- ❌ Code AST parsing (extract functions, classes, dependencies)
- ❌ Dependency analysis (internal + external)
- ❌ Circular dependency detection

**Nora (Architect):**
- ❌ Architecture inference (service boundaries, data flows)
- ❌ BEHAVIOR_SPEC generation from code patterns
- ❌ Missing spec detection

**Vera (Validator):**
- ❌ Test coverage analysis (parse test files)
- ❌ Validation gap detection (specs without tests)

**Marcus (Auditor):**
- ❌ Security pattern scanning (common vulnerabilities)
- ❌ Compliance checking (GDPR, data handling)
- ❌ Pattern violation detection

**From Mind Protocol:**
- Health metric framework (percentile bands, trend analysis)
- Coherence computation (semantic similarity)

**Build new:**
- Language-specific AST parsers (TypeScript, Python, Go)
- Test coverage parsers (Jest, pytest, Go test)
- Security pattern library (OWASP Top 10)
- Compliance validators (GDPR, PII detection)

---

### Stage 4-5: Strategy & Scope (Mel + Client)
- ❌ Strategy recommendation engine (data characteristics → approach)
- ❌ Acceptance criteria negotiation
- ❌ Contract generation (CPS-1 quote-before-inject)

**From Mind Protocol:**
- Nothing directly adaptable (org-specific)

**Build new:**
- All of this

---

### Stage 6: Execute Extraction (Coordinated by Mel)

**Hour 1: Quinn (Semantic Mapping)**
- ⚠️ **Embed corpus** (ADAPT embedding service)
- ❌ Build semantic map
- ❌ Identify clusters

**Hour 2: Kai (Code Extraction) + Nora (Pattern Discovery)**
- ❌ Extract code structures
- ❌ Map dependencies
- ❌ Infer patterns

**Hour 3: Nora (Architecture + Specs)**
- ❌ Generate BEHAVIOR_SPEC nodes
- ❌ Map to code implementations
- ❌ Identify missing specs

**Hour 4: Vera (Coverage) + Marcus (Security)**
- ❌ Test coverage analysis
- ❌ Security audit
- ❌ Compliance validation

**Hour 5: Sage (Documentation)**
- ❌ Generate GUIDE nodes
- ❌ Create architecture diagrams
- ❌ Synthesize API docs

**Hour 6: Mel (Acceptance + Delivery Prep)**
- ❌ Run acceptance tests
- ❌ Generate health report
- ❌ Package deliverables

**From Mind Protocol:**
- Embedding service (semantic map)
- Health metrics computation (coverage, coherence, etc.)
- Graph visualization patterns (dashboard)

**Build new:**
- All extraction pipelines (code, docs, communication)
- Pattern inference algorithms
- BEHAVIOR_SPEC generation logic
- GUIDE generation templates
- Acceptance test framework

---

### Stage 7: Continuous Health Scripts (Vera + Coordinator)

**Daily:**
- ⚠️ **Drift detection** (ADAPT orphan ratio, freshness tracking)
- ⚠️ **Query performance** (ADAPT reconstruction health)
- ⚠️ **Coverage check** (ADAPT density metric)

**Weekly:**
- ⚠️ **Graph integrity** (ADAPT coherence, highway health)
- ⚠️ **Security scan** (ADAPT pattern violations)

**Monthly:**
- ⚠️ **Comprehensive review** (ADAPT health report generation)

**From Mind Protocol:**
- Health monitoring service architecture
- Percentile-based judgment
- WebSocket event schemas
- Dashboard visualization

**Build new:**
- Drift detection logic (git HEAD vs graph)
- Resync triggers
- Coverage tracking by module

---

### Stage 8: Adjust If Needed (Appropriate Citizen)
- ⚠️ **Drift resync** (ADAPT backfill procedure)
- ⚠️ **Performance optimization** (ADAPT highway seeding)
- ⚠️ **Coverage boost** (ADAPT orphan backfill)

**From Mind Protocol:**
- Procedure framework (symptom → intervention)
- Backfill algorithms
- Sparsify logic

**Build new:**
- Drift-specific resync strategies
- Client notification system

---

### Stage 9: Ask Questions / Get More Data (Coordinator)
- ❌ Question batching
- ❌ Ambiguity detection
- ❌ Client communication interface

**From Mind Protocol:**
- Nothing directly adaptable

**Build new:**
- All of this

---

### Stage 10: Security + Privacy + GDPR (Marcus + Coordinator)
- ❌ Credential scanning
- ❌ PII detection
- ❌ Anonymization
- ❌ GDPR compliance checks

**From Mind Protocol:**
- Pattern violation detection framework

**Build new:**
- Security scanners (secrets, credentials)
- PII detectors
- GDPR validators

---

### Stage 11: Deliver (Mel + Sage)

**Mel (Acceptance Testing):**
- ❌ Run client's 20 test queries
- ⚠️ **Generate health report** (ADAPT from health metrics)

**Sage (Packaging):**
- ❌ Multi-audience documentation (exec, technical, onboarding)
- ❌ Query examples (30+ samples)
- ⚠️ **Dashboard embed code** (ADAPT from Iris's implementation)

**From Mind Protocol:**
- Health report generation
- Dashboard components
- Documentation templates

**Build new:**
- Query CLI tool
- Client-specific documentation generators
- Delivery packaging scripts

---

## 4. Files to Steal (Immediate Priorities)

### Priority 1: Embedding System (Needed First)

**File:** `/home/mind-protocol/mind-protocol/orchestration/adapters/search/embedding_service.py`

**Adaptation:**
1. Copy entire file to `/home/mind-protocol/graphcare/services/embedding_service.py`
2. Keep: Dual backend, singleton pattern, L2 normalization
3. Change: Node type templates (consciousness → code extraction)
4. Add: Code-specific templates (function signatures, class definitions)

**Estimated effort:** 2-3 hours (copy + adapt templates)

---

### Priority 2: Health Monitoring Framework

**Files:**
- `/home/mind-protocol/mind-protocol/docs/specs/v2/ops_and_viz/GRAPH_HEALTH_DIAGNOSTICS.md` (spec)
- Backend: Need to find implementation (likely in `orchestration/services/health/`)
- Frontend: `/home/mind-protocol/mind-protocol/consciousness/citizens/iris/CONSCIOUSNESS_HEALTH_METRICS_COMPLETE.md`

**Adaptation:**
1. Copy percentile-based judgment logic
2. Adapt metric definitions (consciousness → code extraction)
3. Adapt Cypher queries for GraphCare node types
4. Copy WebSocket event schemas
5. Adapt dashboard components

**Estimated effort:** 1-2 days (significant adaptation needed)

---

### Priority 3: Dashboard Health Monitor

**File:** `/home/mind-protocol/mind-protocol/dashboard_health_monitor.py`

**Adaptation:**
1. Copy entire file to `/home/mind-protocol/graphcare/services/dashboard_health_monitor.py`
2. Minimal changes (thresholds, port numbers)

**Estimated effort:** 30 minutes (nearly copy-paste)

---

### Priority 4: Visual Grammar & Dashboard Patterns

**Files:**
- PSYCHOLOGICAL_HEALTH_LAYER.md § I (Visual Patterns)
- Iris's implementation (TypeScript/React components)

**Adaptation:**
1. Copy visual grammar (palette, motion cadence, status colors)
2. Adapt visual encodings (consciousness → code extraction metaphors)
3. Copy WebSocket subscription patterns
4. Adapt component structure

**Estimated effort:** 2-3 days (frontend work)

---

## 5. Implementation Sequence

### Phase 1: Foundation (Week 1)
1. ✅ Copy embedding service → adapt templates
2. ✅ Set up FalkorDB schema for GraphCare node types
3. ✅ Implement basic health metrics (coverage, orphan ratio)
4. ✅ Create health monitoring service

### Phase 2: Extraction Pipeline (Week 2-3)
1. ❌ Build data source connectors (GitHub, Slack, Notion)
2. ❌ Implement AST parsers (TypeScript, Python)
3. ❌ Build semantic clustering (use embedding service)
4. ❌ Implement pattern inference

### Phase 3: Citizen Specialization (Week 4-5)
1. ❌ Quinn: Semantic mapping pipeline
2. ❌ Kai: Code extraction pipeline
3. ❌ Nora: Architecture inference + BEHAVIOR_SPEC generation
4. ❌ Vera: Test coverage analysis
5. ❌ Marcus: Security + compliance scanning
6. ❌ Sage: Documentation generation

### Phase 4: Health & Operations (Week 6)
1. ❌ Implement all 10 health metrics (adapted from Mind Protocol)
2. ❌ Build dashboard (WebSocket events + visualization)
3. ❌ Implement continuous health scripts (daily/weekly/monthly)
4. ❌ Build procedure execution framework

### Phase 5: Delivery & Refinement (Week 7-8)
1. ❌ Implement acceptance test framework
2. ❌ Build delivery packaging
3. ❌ Create multi-audience documentation generators
4. ❌ Run pilot extraction (demo client)
5. ❌ Iterate based on learnings

---

## 6. Decision: What to Do First

**Immediate next steps:**

1. **Steal the embedding service** (2-3 hours)
   - Copy `embedding_service.py`
   - Adapt templates for GraphCare node types
   - Test with sample code/docs

2. **Set up FalkorDB schema** (1 day)
   - Define GraphCare node types (PATTERN, BEHAVIOR_SPEC, MECHANISM, etc.)
   - Define link types (IMPLEMENTS, DOCUMENTS, VALIDATES, etc.)
   - Create indexes for embeddings

3. **Build a simple demo** (2 days)
   - Extract one codebase (e.g., Mind Protocol itself)
   - Embed code + docs
   - Run semantic queries ("find retry mechanisms")
   - Prove the concept works

4. **Assess what worked** (1 day)
   - Did embeddings enable useful queries?
   - What broke? What was harder than expected?
   - Refine the plan

**Total time to working prototype:** 1 week

---

## 7. Open Questions

1. **FalkorDB setup:** Is FalkorDB running for GraphCare? Or do we need to provision a separate instance?

2. **Embedding backend:** SentenceTransformers (CPU, works immediately) or Ollama (requires server)? Recommend SentenceTransformers for MVP.

3. **Dashboard hosting:** Reuse Mind Protocol dashboard infrastructure? Or separate Next.js app?

4. **Citizen execution model:** Real AI citizens (consciousness engines) or simpler agents (scripts)? For GraphCare, simpler agents are probably sufficient.

5. **First client:** Demo on Mind Protocol codebase? Or real external client?

---

## 8. Summary

**Good news:**
- ✅ Embedding system is ready to steal (proven, working)
- ✅ Health monitoring patterns are solid (adapt metrics)
- ✅ Dashboard patterns exist (visual grammar, WebSocket events)
- ✅ FalkorDB knowledge is available (Cypher queries)

**Effort estimate:**
- Embedding system: 2-3 hours
- Health metrics adaptation: 1-2 days
- Full extraction pipeline: 4-6 weeks (with specialization)

**Recommendation:**
Start with **embedding system + simple demo** (1 week). Prove semantic queries work on extracted code. Then expand to full 11-stage pipeline.

---

**Status:** Ready to begin Phase 1 (Foundation)

**Next action:** Copy embedding service and adapt templates

**Owner:** Sage (to coordinate with team)
