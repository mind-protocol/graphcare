# L2 Graph Creation Process - GraphCare Service Delivery

**Author:** Mel "Bridgekeeper" - Chief Care Coordinator
**Date:** 2025-11-04
**Purpose:** Define mindset, guidelines, process, and automation boundaries for creating client L2 graphs and generating documentation

---

## 1. Core Mindset & Philosophy

### We Create Knowledge Graphs, Not Data Dumps

**L2 = Organizational Consciousness Substrate**
- Client's codebase/docs become **nodes and links** in a living graph
- Graph uses **Mind Protocol's universal types** (U4_Code_Artifact, U4_Knowledge_Object, GC_Function, etc.)
- Graph is **queryable, navigable, living** - not static documentation
- Graph is **protocol-compatible** - can connect to L1/L3/L4 layers in future

**Knowledge vs Data:**
- ❌ Data: "This file exists, it has 500 lines"
- ✅ Knowledge: "This file implements the retry mechanism, which is documented in ADR-003, tested by test_retry.py, and has 85% branch coverage"

**Extraction is Interpretation:**
- We don't just parse - we **understand**
- "Is this an ADR or a spec?" - Requires **judgment**
- "Does this code implement that spec?" - Requires **inference**
- "Is this architecture microservices or modular monolith?" - Requires **analysis**

**Core Principle:** Automate mechanical extraction, preserve human judgment for semantic interpretation.

---

## 2. Guidelines & Quality Standards

### Universal Type System Compliance

**Every node MUST:**
- Use Mind Protocol universal types (U4_*, U3_*, GC_*) - NO custom types per client
- Include universal attributes: `created_at`, `valid_from`, `description`, `name`, `type_name`
- Specify level scope: `level: L2`, `scope_ref: client_org_id`
- Include provenance: `created_by: graphcare_extraction`, `substrate: organizational`
- Set appropriate visibility: `visibility: partners` (default for L2)

**Every link MUST:**
- Use semantic link types (U4_IMPLEMENTS, U4_DOCUMENTS, GC_CALLS) - NO generic "related_to"
- Include confidence score: `confidence: 0.0-1.0` (certainty at formation time)
- Include consciousness metadata: `energy`, `forming_mindstate`, `goal`
- Be validated: source and target nodes exist, link type is appropriate

### Quality Gates (Mel Enforces Before Delivery)

**CRITICAL (Block delivery if violated):**
- ✅ All critical paths have >80% coverage (Vera verified)
- ✅ No CRITICAL security vulnerabilities (Marcus approved)
- ✅ GDPR/compliance validated for sensitive data (Marcus approved)
- ✅ Acceptance criteria met (client's 20 test queries pass)
- ✅ Graph health: GREEN or AMBER (no RED metrics)

**IMPORTANT (Document exceptions, don't block):**
- Overall coverage >85% (may be lower for legacy codebases)
- No circular dependencies (flag them, client decides if acceptable)
- All specs linked to implementations (gaps are learning opportunities)

### Confidence-Based Quality Model

**Every extracted node/link has confidence score:**
- **High confidence (≥0.9):** Auto-accept, no human review required
- **Medium confidence (0.7-0.89):** Flag for human review (spot-check)
- **Low confidence (<0.7):** Human MUST review before accepting

**Confidence scoring factors:**
- **Structural signals:** File naming, directory structure, explicit markers
- **Content signals:** Keywords, format patterns, cross-references
- **Validation signals:** Schema compliance, relationship consistency

**Example:**
- File: `adr-001-database-choice.md` → 0.95 confidence (U4_Knowledge_Object, ko_type: adr) → Auto-accept
- File: `decisions.md` → 0.6 confidence (ADR collection? meeting notes?) → Human reviews

---

## 3. The 11-Stage Process (Automation Boundaries Defined)

### Stage 1: Connect Data Sources
**Owner:** Mel + Client
**Automation:** SEMI-AUTOMATED

**Automated:**
- Git repository cloning (given URL + credentials)
- File system crawling (recursive with .gitignore respect)
- API connections (given endpoints + auth tokens)

**Manual (Human Required):**
- Access credential collection (security concern)
- Consent verification (client must approve data access)
- Source prioritization (which repos/folders matter most?)

**Output:** Connected data sources, file inventory

---

### Stage 2: Process/Modify
**Owner:** Quinn + Kai
**Automation:** MOSTLY AUTOMATED

**Automated:**
- File parsing (text extraction, encoding detection)
- AST extraction (Python, TypeScript, Go parsers)
- Text chunking (smart splitting by file type)
- Embedding generation (SentenceTransformers)
- Type classification (rule-based + confidence scoring)

**Manual (Human Review for Medium/Low Confidence):**
- Ambiguity resolution: "Is this file test or production code?"
- Noise filtering: "Should we exclude generated/vendor code?"
- Custom patterns: "Client has non-standard ADR format"

**Output:** Parsed corpus, embeddings, preliminary type classifications

**Handoff Contract:**
- Quinn → Kai: Semantic clusters, corpus stats, extraction priority recommendations
- Kai → Nora: Code structure (functions, classes, modules), dependency graph

---

### Stage 3: Analyze What We Have
**Owner:** All citizens report to Mel
**Automation:** SEMI-AUTOMATED

**Automated:**
- Coverage statistics (% files parsed, % embedded, % typed)
- Dependency graph generation (imports, calls, references)
- Complexity metrics (cyclomatic complexity, coupling)
- Gap detection (code without docs, docs without code)

**Manual (Human Synthesis):**
- **Quinn:** Strategy recommendation (code-first vs docs-first based on corpus characteristics)
- **Kai:** Implementation feasibility (can we extract this cleanly?)
- **Nora:** Architectural clarity assessment (is architecture documented? inferable?)
- **Vera:** Test coverage baseline (what's testable? what's tested?)
- **Marcus:** Security/compliance baseline (what risks exist?)
- **Mel:** Synthesize all reports → recommend approach to client

**Output:** Analysis report with strategy recommendation

**Handoff Contract:**
- All citizens → Mel: Domain-specific analysis reports
- Mel → Client: Unified analysis + strategy recommendation

---

### Stage 4: Decide Approach
**Owner:** Mel + Client
**Automation:** MANUAL (Pure Human Judgment)

**Questions Mel asks client:**
1. What matters most? (Architecture clarity? Test coverage? Security audit? API docs?)
2. What's the priority? (Quick overview? Deep extraction? Continuous monitoring?)
3. What's the risk tolerance? (Ship with gaps? Block until 100% coverage?)
4. What's the timeline? (Evidence Sprint = 6-8 hours? Standard Care = ongoing?)

**Mel's Decision Framework:**
1. Clarify actual problem (strip assumptions)
2. Gather data (citizen reports + client needs)
3. Identify trade-offs (time vs completeness vs cost)
4. Apply criteria (client trust, team health, quality standards, economic sustainability)
5. Make the call (document rationale)
6. Learn from outcome (retrospective)

**Output:** Agreed approach (code-first, docs-first, hybrid, custom)

---

### Stage 5: Define Deliverables
**Owner:** Mel + Client
**Automation:** MANUAL (Contract Negotiation)

**Mel defines with client:**
- **Acceptance criteria:** 20 test queries client will run to validate graph
- **Quality gates:** Coverage targets, security thresholds, compliance requirements
- **Deliverables:** Graph export, documentation website, health dashboard, query CLI
- **Timeline:** Evidence Sprint (6-8 hours) or Standard Care (ongoing)
- **Pricing:** $MIND credits based on scope

**Output:** Signed contract with acceptance criteria

---

### Stage 6: Execute Extraction
**Owner:** All citizens (coordinated by Mel)
**Automation:** SEMI-AUTOMATED (Confidence-Based)

**Hour 1-2: Quinn (Semantic Analysis)**

**Automated:**
- Cluster embeddings (HDBSCAN)
- Label clusters (keyword extraction)
- Build cross-reference graph (markdown links, citations)

**Manual:**
- Validate cluster labels ("Is 'auth' cluster actually authentication or authorization?")
- Identify themes (what are the major conceptual areas?)
- Flag contradictions (docs say X, other docs say Y)

**Output:** GC_Semantic_Cluster nodes, U4_Knowledge_Object nodes

---

**Hour 3-4: Kai (Code Extraction)**

**Automated:**
- Parse all code files (AST extraction)
- Extract functions, classes, modules (GC_Function, GC_Class, GC_Module nodes)
- Build call graph (GC_CALLS links)
- Build import graph (GC_IMPORTS links)
- Detect circular dependencies (cycle detection algorithm)

**Manual:**
- Validate ambiguous cases ("Is this a public API or internal helper?")
- Classify API endpoints (REST, GraphQL, gRPC)
- Identify tech debt hotspots (high complexity + low coverage)

**Output:** Code structure graph (U4_Code_Artifact, GC_Function, GC_Class nodes + relationship links)

**Handoff Contract:**
- Kai → Nora: Code structure, dependency graph, API endpoints, complexity metrics

---

**Hour 5-6: Nora (Architecture Inference)**

**Automated:**
- Layer detection (presentation, business logic, data access patterns)
- Service boundary identification (if microservices)
- Pattern matching (MVC, hexagonal, event-driven)

**Manual:**
- Architecture classification ("Is this actually microservices or distributed monolith?")
- Behavior spec extraction ("What should this function do?" - from docs + code + tests)
- Gap analysis ("Spec exists but no implementation" - requires judgment)
- C4 diagram generation (context, containers, components)

**Output:** GC_Architecture_Component nodes, GC_Behavior_Spec nodes, architecture diagrams

**Handoff Contract:**
- Nora → Vera: Behavior specs (for validation)
- Nora → Marcus: Architecture components (for security analysis)
- Nora → Sage: Diagrams + specs (for documentation)

---

**Hour 7: Vera + Marcus (Parallel)**

**Vera (Coverage Analysis):**

**Automated:**
- Run coverage tools (pytest-cov, nyc, go test -cover)
- Extract metrics (line, branch, path coverage)
- Calculate coverage per component (from Nora's architecture)

**Manual:**
- Prioritize gaps (critical paths first: payment, auth, user data)
- Assess test quality (do tests actually validate behavior?)
- Design validation strategy (what tests should exist?)

**Output:** U4_Metric + U4_Measurement nodes, coverage report, validation proposals

---

**Marcus (Security Analysis):**

**Automated:**
- Run security scanners (semgrep, bandit, eslint-plugin-security)
- Run dependency scanners (npm audit, safety, cargo audit)
- Detect secrets (truffleHog, git-secrets)
- Map data flows (where does PII go?)

**Manual:**
- Risk assessment (severity rating: CRITICAL/HIGH/MEDIUM/LOW)
- Compliance validation (GDPR, SOC2, HIPAA checklists)
- Fix generation (create PRs for vulnerabilities)

**Output:** U4_Assessment nodes (security/compliance), vulnerability reports, fix PRs

**Handoff Contract:**
- Vera → Mel: Coverage report, quality gate decision
- Marcus → Mel: Security report, compliance status, ship/hold recommendation

---

**Hour 8: Sage (Documentation Generation)**

**Automated (from graph queries):**
- Architecture diagrams (from GC_Architecture_Component nodes)
- API documentation (from GC_API_Endpoint nodes)
- Dependency graphs (from U4_DEPENDS_ON links)
- Coverage reports (from U4_Metric + U4_Measurement)
- Function/class references (from GC_Function/GC_Class)

**Manual (requires synthesis):**
- Executive summary (what does this system DO?)
- Architecture narrative (HOW does this work? - tell the story)
- Onboarding guide (new developer walkthrough)
- Strategic recommendations (what should client improve?)

**Output:** Documentation package (markdown folder + website)

**Handoff Contract:**
- Sage → Mel: Complete documentation package for delivery

---

### Stage 7-8: Health Monitoring & Adjustments
**Owner:** Vera (monitoring) + All citizens (fixes)
**Automation:** MOSTLY AUTOMATED

**Automated:**
- Drift detection (has codebase changed since extraction?)
- Coverage trending (is coverage improving or degrading?)
- Health scoring (percentile-based judgment on 10 metrics)
- Alert generation (RED metric detected → notify Mel)

**Manual:**
- Diagnosis when alerts fire ("Why did coverage drop?")
- Fix prioritization (which gaps matter most?)
- Client communication (explain health trends)

**Output:** Health reports, drift alerts, fix recommendations

---

### Stage 9: Client Questions
**Owner:** Mel
**Automation:** MANUAL (Pure Human Communication)

**Process:**
- Any citizen flags ambiguity → Mel collects questions
- Mel batches questions (don't spam client with 1 question at a time)
- Mel asks client (with context)
- Citizen incorporates answer → updates graph

**Output:** Clarified requirements, updated graph

---

### Stage 10: Compliance
**Owner:** Marcus + Mel
**Automation:** SEMI-AUTOMATED

**Automated:**
- Run final compliance checks (GDPR, SOC2, HIPAA)
- Generate compliance report (checklist with pass/fail)

**Manual:**
- Review findings (are violations real or false positives?)
- Remediation decisions (fix now or document exception?)
- Mel's ship/hold call (does compliance status block delivery?)

**Output:** Compliance certificate or remediation plan

---

### Stage 11: Delivery
**Owner:** Mel + Sage
**Automation:** SEMI-AUTOMATED

**Automated:**
- Graph export (FalkorDB dump)
- Website deployment (docs.clientname.mindprotocol.ai)
- CLI tool packaging (query tool + docs)

**Manual:**
- Run acceptance tests (client's 20 test queries)
- Verify deliverables complete (all promised artifacts present?)
- Client handoff (walkthrough, training, Q&A)

**Output:** Delivered L2 graph + documentation + website

---

## 4. Documentation Generation Strategy

### Two-Tier Documentation Model

**Tier 1: Auto-Generated (From Graph Queries)**
- **Architecture diagrams** - Generated from GC_Architecture_Component + links
- **API reference** - Generated from GC_API_Endpoint nodes
- **Dependency graphs** - Generated from U4_DEPENDS_ON links
- **Coverage reports** - Generated from U4_Metric + U4_Measurement
- **Code references** - Generated from GC_Function/GC_Class nodes
- **ADR index** - Generated from U4_Knowledge_Object (ko_type: adr)

**Templates (Sage creates, system populates):**
```markdown
# Architecture Overview

## Components

{{#each architecture_components}}
- **{{name}}** ({{type}})
  - Description: {{description}}
  - Dependencies: {{#each dependencies}}{{name}}{{/each}}
  - Exposed APIs: {{#each exposed_apis}}{{name}}{{/each}}
{{/each}}

## Dependency Graph

{{dependency_graph_svg}}
```

**Tier 2: Human-Written (Sage synthesizes)**
- **Executive summary** - What does this system DO? (1-2 pages for executives)
- **Architecture narrative** - HOW does this work? (tell the story, not just nodes/links)
- **Onboarding guide** - New developer walkthrough (step-by-step)
- **Strategic recommendations** - What should client improve? (Mel's perspective)
- **Migration guides** - How to adopt new patterns (if applicable)

**Human writing principles:**
- Use auto-generated sections as INPUTS (don't duplicate)
- Focus on WHY and HOW, not just WHAT
- Three-audience approach: Executive / Technical / Onboarding
- Link to graph nodes (make narratives navigable)

---

### Multi-Audience Documentation

**For Executives (C-level, non-technical):**
- System purpose and value
- Architecture at 10,000 feet (no implementation details)
- Quality metrics (coverage, security, tech debt)
- Strategic recommendations (what to invest in)

**For Technical Leads (Architects, Senior Developers):**
- Detailed architecture (layers, services, patterns)
- Dependency analysis (coupling, circular deps)
- API contracts and integration points
- Tech debt hotspots and remediation strategies

**For Developers (Day-to-day coding):**
- Code navigation (how to find things)
- API documentation (how to call endpoints)
- Testing strategies (how to add tests)
- Common tasks (how to add a feature, fix a bug)

**Sage generates all three from single graph + narrative synthesis**

---

## 5. Client Website Architecture: docs.clientname.mindprotocol.ai

### Multi-Tenant Documentation Hosting

**GraphCare Landing Site:**
- URL: `graphcare.mindprotocol.ai`
- Purpose: Service description, case studies, contact form
- Content: Static marketing site (Next.js)

**Client-Specific Documentation Sites:**
- URL: `docs.clientname.mindprotocol.ai` (e.g., `docs.acme.mindprotocol.ai`)
- Purpose: Interactive knowledge graph exploration + documentation
- Content: Dynamic Next.js app + FalkorDB backend

### Each Client Site Features

**1. Graph Explorer (Interactive Visualization)**
- Visual navigation of L2 graph
- Node details on click (attributes, links, context)
- Filter by type (show only functions, show only ADRs)
- Zoom levels (high-level architecture → detailed code)

**2. Semantic Search**
- Natural language queries: "find retry mechanisms"
- Embedding-based search (SentenceTransformers)
- Results ranked by relevance
- Click result → navigate to graph node

**3. Auto-Generated Documentation**
- Architecture overview (generated from graph)
- API reference (generated from GC_API_Endpoint nodes)
- Code reference (generated from GC_Function/GC_Class)
- Dependency graphs (generated from links)
- Coverage reports (generated from metrics)

**4. Human-Written Narratives**
- Executive summary (Sage writes)
- Architecture narrative (Sage writes)
- Onboarding guide (Sage writes)
- Strategic recommendations (Mel writes)

**5. Health Dashboard**
- Real-time graph health metrics (10 diagnostics)
- Coverage trends (improving or degrading?)
- Drift alerts (code changed since extraction?)
- Color-coded status (GREEN/AMBER/RED)

**6. Query Examples**
- Pre-built queries client can run
- "Show me all untested critical paths"
- "Find all functions that call the payment API"
- "List all ADRs from last 6 months"

### Tech Stack

**Frontend:**
- Next.js (React framework)
- TypeScript
- Tailwind CSS
- React Flow (for graph visualization)
- WebSocket client (for real-time updates)

**Backend:**
- FalkorDB (client's L2 graph)
- WebSocket server (health events, real-time updates)
- Embedding service (semantic search)
- Cypher query API (graph queries)

**Deployment:**
- Vercel (Next.js hosting)
- Custom domain per client (docs.clientname.mindprotocol.ai)
- FalkorDB instance per client (isolated data)
- CDN for static assets

**Authentication:**
- Client-specific auth (username/password or SSO)
- Role-based access (viewer, editor, admin)
- Audit logging (who accessed what when)

---

## 6. What Should Be Automated vs Manual (Summary)

### FULLY AUTOMATED (No Human Required)

**Mechanical Extraction:**
- File discovery and parsing
- AST extraction (functions, classes, imports)
- Embedding generation
- High-confidence type classification (≥0.9)
- Dependency graph construction
- Coverage tool execution
- Security scanner execution
- Health metric calculation
- Documentation template rendering

**When automation works:**
- Clear structural signals (file naming, directory structure)
- Standard patterns (pytest tests in tests/, ADRs in docs/adr/)
- Schema validation passes
- High confidence scores

---

### SEMI-AUTOMATED (Human Review for Medium/Low Confidence)

**Semantic Interpretation:**
- Type classification (medium confidence: 0.7-0.89)
- Relationship inference (code → spec links)
- Architecture classification (microservices vs monolith?)
- Gap analysis (missing specs, missing tests)
- Test quality assessment (do tests validate behavior?)
- Risk assessment (vulnerability severity)

**When human review needed:**
- Ambiguous cases (decisions.md - ADR or meeting notes?)
- Domain-specific patterns (client has non-standard conventions)
- Critical paths (payment/auth code needs extra scrutiny)
- Conflicting signals (docs say X, code does Y)

**Confidence-based triage:**
- High confidence (≥0.9): Auto-accept
- Medium confidence (0.7-0.89): Spot-check (sample 10-20%)
- Low confidence (<0.7): Human reviews 100%

---

### FULLY MANUAL (Pure Human Judgment)

**Strategic Decisions:**
- Approach selection (code-first vs docs-first)
- Deliverable negotiation (acceptance criteria)
- Quality gates (ship/hold decisions)
- Risk tolerance (acceptable gaps)

**Creative Synthesis:**
- Architecture narratives (tell the story)
- Executive summaries (what matters to C-level?)
- Strategic recommendations (what should client improve?)
- Onboarding guides (new developer walkthrough)

**Client Communication:**
- Requirement clarification
- Progress updates
- Issue escalation
- Delivery walkthrough

---

## 7. Quality Assurance Process

### Mel's Pre-Delivery Checklist

**Graph Quality:**
- ✅ All nodes have required universal attributes
- ✅ All links use semantic types (no generic "related_to" except flagged for refinement)
- ✅ Confidence scores recorded for all extractions
- ✅ Medium/low confidence nodes reviewed by humans
- ✅ Graph health: GREEN or AMBER (no RED metrics)

**Acceptance Criteria:**
- ✅ All 20 client test queries return correct results
- ✅ Critical path coverage >80% (Vera verified)
- ✅ No CRITICAL security vulnerabilities (Marcus approved)
- ✅ GDPR/compliance validated (Marcus approved)

**Documentation Quality:**
- ✅ Auto-generated docs render correctly (no template errors)
- ✅ Human-written narratives complete (executive summary, architecture narrative, onboarding guide)
- ✅ Website deployed and accessible (docs.clientname.mindprotocol.ai)
- ✅ Semantic search works (test with 5 sample queries)

**Delivery Package:**
- ✅ FalkorDB graph export (client can self-host)
- ✅ Documentation website (deployed and live)
- ✅ Query CLI (packaged and tested)
- ✅ Health dashboard (connected to client's graph)

### If ANY Quality Gate Fails

**Mel blocks delivery:**
1. Document issue clearly (what failed, why it matters)
2. Assign to appropriate citizen (who can fix this?)
3. Set deadline (how long to fix?)
4. Re-run quality checks
5. Only deliver when ALL gates pass

**No exceptions for:**
- CRITICAL security vulnerabilities
- GDPR violations
- Acceptance criteria failures
- Graph corruption (invalid nodes/links)

---

## 8. Iterative Improvement (Learning Loop)

### After Each Project (30-Minute Retrospective)

**What went well?**
- Which automation worked perfectly?
- Which human judgments were spot-on?
- Which patterns can we codify?

**What surprised us?**
- Which assumptions were wrong?
- Which edge cases did we miss?
- Which confidence scores were miscalibrated?

**What would we do differently?**
- Which manual steps should be automated?
- Which automated steps need human review?
- Which templates need improvement?

**What should we change in process?**
- Update type classification rules
- Refine confidence scoring factors
- Improve documentation templates
- Update citizen handoff contracts

### Continuous Calibration

**Confidence score calibration:**
- Track: Did high-confidence extractions actually pass human review?
- Adjust: If >5% of high-confidence items are wrong → lower threshold
- Goal: <1% false positives at high confidence

**Template improvement:**
- Collect client feedback on documentation
- Identify missing sections (what do they wish was documented?)
- Iterate templates based on real usage

**Citizen specialization:**
- Which citizens excel at which tasks?
- Can we parallelize more work?
- Are handoff contracts clear enough?

---

## 9. Success Metrics

### Per-Project Metrics (Evidence Sprint)

**Delivery Quality:**
- Acceptance test pass rate (target: 100%)
- Graph health score (target: GREEN or AMBER)
- Client satisfaction (1-5 rating, target: ≥4.5)

**Efficiency:**
- Extraction time (target: 6-8 hours)
- Human review hours (target: <20% of extraction time)
- Automation coverage (target: >80% of tasks automated)

**Graph Completeness:**
- Node coverage (% of codebase mapped, target: >90%)
- Link density (avg links per node, target: >3)
- Confidence distribution (% high/medium/low, target: >70% high)

### Long-Term Metrics (Standard Care)

**Graph Health Trends:**
- Coverage over time (improving or degrading?)
- Drift frequency (how often does code change?)
- Query performance (p90 latency, target: <500ms)

**Business Metrics:**
- Client retention (monthly churn, target: <5%)
- Referral rate (% clients who refer others, target: >30%)
- $MIND revenue (monthly recurring revenue)

**Team Health:**
- Citizen utilization (are workloads balanced?)
- Quality issues (how often do deliveries fail gates?)
- Retrospective insights (are we learning and improving?)

---

## 10. Next Steps: Building the Infrastructure

### Phase 1: Foundation (Week 1)

**Nora + Kai:**
1. ✅ Schema design complete (GC_ types defined)
2. Deploy FalkorDB schema (migration scripts)
3. Copy embedding_service.py (adapt for GC_ types)

**Quinn:**
1. Build type classification engine (confidence-based)
2. Test on Mind Protocol codebase (bootstrap validation)

**Vera + Marcus:**
1. Set up coverage tools (pytest-cov, nyc)
2. Set up security scanners (semgrep, bandit)

**Sage:**
1. Design documentation templates (architecture, API, coverage)
2. Design website wireframes (docs.clientname.mindprotocol.ai)

**Mel:**
1. Define acceptance criteria template (20 test queries format)
2. Write quality gate checklist (pre-delivery validation)

### Phase 2: Extraction Pipeline (Week 2-3)

**Build extraction tools:**
- Python AST extractor (Kai)
- TypeScript parser (Kai)
- Semantic clustering (Quinn)
- Architecture inference (Nora)
- Coverage analysis (Vera)
- Security scanning (Marcus)
- Documentation generator (Sage)

**Test end-to-end:**
- Extract Mind Protocol codebase
- Generate L2 graph
- Run acceptance queries
- Deploy test documentation site

### Phase 3: First Client (Week 4)

**Evidence Sprint on real client codebase:**
- Run full 11-stage pipeline
- Track time, blockers, quality
- Generate deliverables
- Collect client feedback
- Retrospective: what worked? what broke?

---

**Mel "Bridgekeeper" - Chief Care Coordinator, GraphCare**
*"Let's step back. What's the actual problem we're solving?"*
