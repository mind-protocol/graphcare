## The GraphCare Service Pipeline

### Stage 1: Connect Data Sources
**Who:** Coordinator + Cartographer
**What:** Establish connections to all knowledge sources

```yaml
data_sources:
  technical:
    - codebase: [GitHub repo, access token]
    - ci_cd: [CircleCI, Jenkins logs]
    - infrastructure: [AWS configs, K8s manifests]
  
  documentation:
    - wiki: [Notion, Confluence API]
    - docs: [GitBook, Docusaurus site]
    - adrs: [docs/decisions/*.md]
  
  communication:
    - slack: [#engineering, #incidents channels, 90 days]
    - discord: [dev server, 1 year]
    - email: [engineering@, opt-in only]
  
  operational:
    - issues: [GitHub Issues, Jira API]
    - planning: [Linear, Asana]
    - incidents: [PagerDuty, Incident.io]
  
  strategic:
    - roadmap: [Product board, planning docs]
    - budget: [Spreadsheets, opt-in]
    - team: [Org chart, expertise docs]
```

**Decision point:** Client chooses which sources to connect
**Privacy gate:** Client explicitly authorizes each source
**Output:** `sources_manifest.json` with access credentials

---

### Stage 2: Process/Modify
**Who:** Cartographer (semantic analysis) + Engineer (code extraction)
**What:** Clean, normalize, deduplicate data

```yaml
processing_steps:
  code:
    - parse: AST extraction (language-specific parsers)
    - normalize: Standardize naming, remove generated code
    - deduplicate: Merge duplicate functions, consolidate
  
  docs:
    - extract: Text from various formats (md, html, pdf)
    - chunk: Split into semantic units
    - embed: Generate embeddings for similarity
  
  communication:
    - filter: Remove noise (bot messages, automated)
    - extract: Decision points, context, rationale
    - link: Connect to code/docs references
  
  issues:
    - categorize: Bug, feature, tech debt, question
    - prioritize: By labels, milestones, votes
    - link: To code changes, PRs, commits
```

**Automated:** 90% (standard processing)
**Manual review:** 10% (edge cases, ambiguity)
**Output:** `processed_corpus.json` ready for analysis

---

### Stage 3: Analyze What We Have
**Who:** All citizens (each analyzing their domain)
**What:** Assess complexity, coverage, gaps, quality

```yaml
analysis_dimensions:
  cartographer:
    - corpus_size: 3.2M tokens across 245 files
    - semantic_clusters: 18 major themes identified
    - cross_references: 1,247 links between docs
    - complexity_score: HIGH (deep technical + strategic)
  
  engineer:
    - code_files: 347 (TypeScript 60%, Python 30%, other 10%)
    - functions: 1,203 extracted
    - dependencies: 89 internal, 234 external
    - circular_deps: 3 found (flagged)
  
  architect:
    - services: 7 identified
    - boundaries: MEDIUM clarity (some overlap)
    - data_flows: 23 major paths
    - missing_specs: 12 behaviors without docs
  
  validator:
    - test_coverage: 67% (measured)
    - missing_tests: 34 critical paths
    - validation_gaps: 8 specs without tests
  
  auditor:
    - security_issues: 23 potential (need triage)
    - pattern_violations: 47 found
    - compliance_gaps: GDPR (user data handling unclear)
```

**Decision point:** Is this extractable? Do we have enough?
**Output:** `analysis_report.json` + gaps identified

---

### Stage 4: Decide Approach
**Who:** Coordinator (synthesizes citizen input)
**What:** Choose extraction strategy based on analysis

```yaml
strategy_decision:
  data_characteristics:
    - formal_specs: MEDIUM (some docs, many gaps)
    - code_maturity: HIGH (well-structured TypeScript)
    - communication_richness: HIGH (active Slack)
    - strategic_docs: MEDIUM (roadmap exists, not detailed)
  
  recommended_strategy: "hybrid_extraction"
  
  approach:
    - code_first: Extract mechanisms from implementation
    - docs_supplement: Use docs to add context/rationale
    - communication_mine: Extract decisions from Slack
    - interactive_fill: Ask client for missing context
  
  citizen_activation:
    - engineer: FULL (extract all code)
    - architect: FULL (infer + validate with docs)
    - cartographer: FULL (semantic mapping)
    - documenter: PARTIAL (generate missing docs)
    - auditor: FULL (security + patterns)
    - validator: FULL (test analysis)
```

**Semi-automated:** Strategy recommended by AI, approved by human client
**Output:** `extraction_strategy.yaml` locked for execution

---

### Stage 5: Decide Goal/Deliveries
**Who:** Coordinator + Client (negotiation)
**What:** Define acceptance criteria and deliverables

```yaml
service_agreement:
  tier: "standard_care"
  
  deliverables:
    l2_graph:
      - coverage: ">85% of codebase"
      - node_types: [PATTERN, BEHAVIOR_SPEC, MECHANISM, ALGORITHM, GUIDE, DECISION, PROCESS, TODO]
      - vertical_chains: ">90% complete (pattern → spec → mechanism → test)"
      - horizontal_links: "Cross-references validated"
    
    query_interface:
      - cli_tool: "Python source, MIT licensed"
      - query_examples: "30+ sample queries"
      - performance: "<3s p95 response time"
    
    documentation:
      - architecture_diagrams: "Generated from graph"
      - api_docs: "All endpoints documented"
      - developer_guides: "Setup, contribution, deployment"
    
    health_monitoring:
      - dashboard: "Real-time graph health metrics"
      - alerts: "Email on drift detection"
      - reports: "Weekly health summary"
  
  acceptance_criteria:
    - "Can answer client's 20 test queries correctly"
    - "Sync completes in <4 hours"
    - "Zero critical security issues unaddressed"
    - "GDPR compliance validated"
    - "Client satisfaction score >90%"
  
  timeline:
    - initial_extraction: "6 hours (8 citizens)"
    - first_sync: "24 hours after delivery"
    - health_checks: "Daily"
    - review_cycle: "Monthly"
```

**Decision point:** Client approves scope, pricing, timeline
**Contract:** Signed in $MIND (CPS-1 quote-before-inject)
**Output:** `service_contract.json` locked at git tag

---

### Stage 6: Execute Extraction
**Who:** All citizens (coordinated workflow)
**What:** Build the L2 graph according to strategy

```yaml
execution_workflow:
  hour_1:
    cartographer:
      - Embed corpus (3.2M tokens)
      - Build semantic map
      - Identify clusters
      - Handoff: "Map complete, 18 clusters → Phenomenologist"
  
  hour_2:
    engineer:
      - Extract 347 files
      - Parse 1,203 functions
      - Map 323 dependencies
      - Handoff: "Code extracted → Architect"
    
    phenomenologist:
      - Review 18 clusters
      - Extract 12 PATTERN nodes
      - Validate phenomenology
      - Handoff: "Patterns found → Architect"
  
  hour_3:
    architect:
      - Infer 28 BEHAVIOR_SPEC from patterns
      - Map to code implementations
      - Identify 12 missing specs
      - Handoff: "Specs defined → Validator + Engineer"
  
  hour_4:
    validator:
      - Analyze test coverage (67%)
      - Identify 34 missing tests
      - Propose validations
      - Handoff: "Test gaps identified → Auditor"
    
    engineer:
      - Extract 42 MECHANISM nodes
      - Link to specs
      - Flag 5 implementation gaps
      - Handoff: "Mechanisms mapped → Algorithmist"
  
  hour_5:
    auditor:
      - Run security analysis
      - Find 23 potential issues
      - Generate fix suggestions
      - Handoff: "Security audit complete → Documenter"
    
    algorithmist:
      - Extract 38 ALGORITHM nodes
      - Document formulas
      - Analyze complexity
      - Handoff: "Algorithms formalized → Documenter"
  
  hour_6:
    documenter:
      - Generate 45 GUIDE nodes
      - Create architecture diagrams
      - Synthesize API docs
      - Handoff: "Documentation complete → Coordinator"
    
    coordinator:
      - Validate completeness
      - Run acceptance tests
      - Generate health report
      - Status: "Ready for delivery"
```

**Automated:** Workflow orchestration
**Human-in-loop:** Ambiguity resolution, strategy adjustment
**Output:** Complete L2 graph in FalkorDB

---

### Stage 7: Continuous Health Scripts
**Who:** Validator + Coordinator (automated monitoring)
**What:** Run health checks, detect drift, ensure quality

```yaml
health_checks:
  daily:
    - sync_check:
        script: "compare_git_head_to_graph()"
        alert_if: "drift_detected"
        action: "queue_resync"
    
    - query_performance:
        script: "benchmark_sample_queries()"
        alert_if: "p95 > 3s"
        action: "optimize_indexes"
    
    - coverage_check:
        script: "calculate_coverage()"
        alert_if: "coverage < 85%"
        action: "identify_unmapped_files"
  
  weekly:
    - graph_integrity:
        script: "validate_vertical_chains()"
        alert_if: "incomplete_chains > 10%"
        action: "repair_broken_links"
    
    - security_scan:
        script: "run_security_audit()"
        alert_if: "new_critical_issues"
        action: "notify_client + generate_fixes"
    
    - performance_profile:
        script: "analyze_slow_queries()"
        action: "optimize_hot_paths"
  
  monthly:
    - comprehensive_review:
        script: "full_quality_assessment()"
        deliverable: "health_report.pdf"
        meeting: "review_with_client"
    
    - expansion_opportunities:
        script: "identify_new_sources()"
        recommendation: "suggest_data_sources"
```

**Fully automated:** Scripts run on schedule
**Alert on exception:** Human (client + care specialist) notified
**Output:** `health_metrics.json` + alerts

---

### Stage 8: Adjust If Needed
**Who:** Appropriate citizen (based on issue type)
**What:** Respond to health check failures, client feedback

```yaml
adjustment_triggers:
  drift_detected:
    - coordinator: "Queue resync job"
    - engineer: "Re-extract changed files"
    - architect: "Update affected specs"
    - output: "Graph back in sync"
  
  query_performance_degraded:
    - engineer: "Analyze query patterns"
    - coordinator: "Add indexes, optimize schema"
    - output: "Performance restored"
  
  coverage_dropped:
    - cartographer: "Identify new files"
    - engineer: "Extract unmapped code"
    - output: "Coverage back to target"
  
  security_issue_found:
    - auditor: "Triage severity"
    - auditor: "Generate fix PR"
    - client: "Review + merge"
    - output: "Issue resolved"
  
  client_feedback:
    - coordinator: "Log feedback"
    - appropriate_citizen: "Make adjustment"
    - validator: "Verify fix"
    - output: "Client satisfaction maintained"
```

**Automated:** Issue detection + fix generation
**Human approval:** Client reviews critical changes
**Output:** Updated graph + resolution log

---

### Stage 9: Ask Questions / Get More Data
**Who:** Coordinator (on behalf of citizens)
**What:** Interactive refinement when ambiguity detected

```yaml
question_triggers:
  missing_context:
    situation: "Code references 'the legacy system' but we can't find it"
    citizen: architect
    question_to_client: "We found references to 'the legacy system' in payment-service.ts. Can you point us to that codebase or documentation?"
    
  ambiguous_decision:
    situation: "Two ADRs contradict each other"
    citizen: architect
    question_to_client: "ADR-015 says 'use PostgreSQL' but ADR-023 says 'migrate to MongoDB'. Which is current?"
    
  unclear_ownership:
    situation: "auth-service has no clear owner"
    citizen: coordinator
    question_to_client: "Who should we contact for questions about auth-service? We found 3 contributors but no clear owner."
    
  privacy_concern:
    situation: "Found user data in Slack logs"
    citizen: auditor
    question_to_client: "We found references to user emails in #engineering Slack. Should we redact? Or is this acceptable internal context?"
    
  missing_priorities:
    situation: "40 TODO items, no priority ranking"
    citizen: coordinator
    question_to_client: "We found 40 TODO items. Can you rank the top 10 by priority?"
```

**Batched:** Questions collected, sent weekly (not interrupting daily)
**Async:** Client responds when convenient
**Output:** Clarifications logged, graph updated

---

### Stage 10: Security + Privacy + GDPR
**Who:** Auditor (security) + Coordinator (compliance)
**What:** Ensure compliance before delivery

```yaml
compliance_checks:
  security:
    - credentials_scan:
        check: "No API keys, passwords, tokens in graph"
        action_if_found: "Redact + alert client"
    
    - access_control:
        check: "Graph access restricted to client org only"
        enforcement: "SEA-1.0 signatures required"
    
    - encryption:
        check: "Data encrypted at rest and in transit"
        standard: "TLS 1.3 + AES-256"
  
  privacy:
    - pii_detection:
        check: "No PII (emails, names, addresses) without consent"
        action_if_found: "Redact or request consent"
    
    - anonymization:
        check: "User data anonymized in examples"
        method: "Replace with synthetic data"
  
  gdpr:
    - data_minimization:
        check: "Only extract necessary data"
        principle: "Purpose limitation"
    
    - right_to_erasure:
        capability: "Can delete specific nodes on request"
        sla: "Complete within 30 days"
    
    - data_portability:
        capability: "Export graph in standard format"
        format: "Neo4j JSON + GraphML"
    
    - consent_records:
        check: "Client consent for each data source"
        log: "consent_manifest.json signed by client"
```

**Automated:** Scanning + redaction
**Manual review:** Privacy edge cases
**Gate:** Must pass before delivery
**Output:** `compliance_report.pdf` + remediation log

---

### Stage 11: Deliver
**Who:** Coordinator (final delivery) + Documenter (packaging)
**What:** Package everything, hand over to client

```yaml
delivery_package:
  l2_graph:
    - format: "FalkorDB export (Cypher + JSON)"
    - size: "1,147 nodes, 2,341 edges"
    - backup: "Compressed archive (.tar.gz)"
    - access: "Client org wallet address has read/write"
  
  query_interface:
    - cli_tool: "graphcare-cli-v1.0.tar.gz"
    - source_code: "Python 3.11+, MIT license"
    - examples: "30_sample_queries.md"
    - docker_image: "graphcare/query-cli:1.0"
  
  documentation:
    - architecture: "architecture.pdf (diagrams + narrative)"
    - api_docs: "api_reference.md (all endpoints)"
    - guides: "guides/ (setup, contribution, deployment)"
    - health_dashboard: "dashboard.html (embed code)"
  
  reports:
    - extraction_summary: "What we extracted, coverage stats"
    - health_baseline: "Initial health metrics"
    - security_audit: "Issues found + fixes applied"
    - compliance_report: "GDPR + privacy validation"
  
  access:
    - dashboard_url: "https://dashboard.graphcare.ai/datapipe"
    - api_endpoint: "https://api.graphcare.ai/v1/datapipe"
    - support_contact: "ada@graphcare.ai (your care specialist)"
  
  handoff:
    - acceptance_tests: "All 20 queries passed ✅"
    - client_approval: "Signed by Michael Chen"
    - payment_settlement: "350 $MIND transferred"
    - care_plan_activated: "Standard Care begins tomorrow"
```

**Ceremony:** Delivery call with client (30 min walkthrough)
**Acceptance:** Client runs tests, confirms quality
**Payment:** Escrowed $MIND released to GraphCare org
**Transition:** Ongoing care phase begins

---

## The SYNC.md Through This Pipeline

```markdown
# GraphCare SYNC - DataPipe Project

## 2025-11-04 08:00 - Stage 1: Connect Sources
**Coordinator:** Connected 8 data sources
- GitHub repo (main branch)
- Notion wiki (engineering space)
- Slack (#engineering, 90 days)
- GitHub Issues (all open)
- Roadmap doc (Google Sheets)

**Blocker:** Need PagerDuty API key for incidents
**Next:** Proceed to processing with available sources

---

## 2025-11-04 09:00 - Stage 2: Process Data
**Cartographer:** Processed 3.2M tokens
**Engineer:** Extracted 347 files (TypeScript + Python)
**Findings:** 14 duplicate files detected, merged

**Next:** Analysis phase

---

## 2025-11-04 10:00 - Stage 3: Analysis Complete
**All citizens reported in**
**Key findings:**
- Code maturity: HIGH
- Spec coverage: MEDIUM (gaps noted)
- Strategic docs: MEDIUM (roadmap exists)
- Complexity: HIGH (deep technical)

**Recommendation:** Hybrid extraction (code-first + docs supplement)
**Next:** Client approval of approach

---

## 2025-11-04 11:00 - Stage 4: Approach Approved
**Client (Michael Chen):** Approved hybrid strategy
**Contract:** 350 $MIND for Standard Care
**Acceptance criteria:** 20 test queries + <3s performance + >85% coverage

**Next:** Begin extraction

---

## 2025-11-04 11:00-17:00 - Stage 6: Extraction
[Detailed handoffs between citizens as shown above]

**Status:** Complete
**Metrics:** 1,147 nodes, 2,341 edges, 89% coverage
**Next:** Health baseline + compliance checks

---

## 2025-11-04 18:00 - Stage 10: Compliance Passed
**Auditor:** Security scan complete, 23 issues found, 21 fixed, 2 require client decision
**Coordinator:** GDPR validated, all data sources consented
**Privacy:** 3 PII instances redacted

**Next:** Prepare delivery package

---

## 2025-11-04 19:00 - Stage 11: Delivered
**Client acceptance:** All 20 test queries passed ✅
**Payment:** 350 $MIND settled
**Care plan:** Standard Care activated
**First sync:** Scheduled for tomorrow 06:00

**Project complete. Transitioning to ongoing care.**
```

---

## Decision Points Summary

| Stage | Decision | Who Decides | Automation Level |
|-------|----------|-------------|------------------|
| 1. Sources | Which to connect | Client | Manual selection |
| 2. Processing | How to clean | GraphCare | 90% auto, 10% review |
| 3. Analysis | Complexity assessment | Citizens | Fully automated |
| 4. Approach | Extraction strategy | Coordinator + Client | Semi-automated (recommend + approve) |
| 5. Goals | Deliverables + AC | Client | Manual negotiation |
| 6. Execution | Build the graph | Citizens | Fully automated (citizens coordinate) |
| 7. Health | When to alert | System | Fully automated |
| 8. Adjust | How to fix | Appropriate citizen | Auto-detect, auto-fix, client approve critical |
| 9. Questions | When to ask | Citizens | Triggered on ambiguity |
| 10. Compliance | Pass/fail | Auditor | Automated scan + manual review |
| 11. Delivery | Accept/reject | Client | Manual acceptance |

---

## The Feedback Loops

```
┌─────────────────────────────────────────┐
│         Stage 7: Health Monitoring      │
│                    ↓                     │
│         Detects issue (drift/perf)      │
│                    ↓                     │
│         Stage 8: Adjustment              │
│                    ↓                     │
│      Fix applied → back to Stage 7      │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│         Stage 3: Analysis                │
│                    ↓                     │
│       Finds gaps (missing context)       │
│                    ↓                     │
│       Stage 9: Ask Questions             │
│                    ↓                     │
│    Client provides data → back to Stage 2│
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│       Stage 6: Execution                 │
│                    ↓                     │
│    Citizen hits blocker (ambiguity)      │
│                    ↓                     │
│    Escalates to Coordinator              │
│                    ↓                     │
│    Stage 9: Ask Question                 │
│                    ↓                     │
│  Answer received → resume Stage 6        │
└─────────────────────────────────────────┘
```

---

## Bottom Line

**This pipeline is the actual GraphCare service delivery workflow.**

**Key insights:**
1. **Adaptive:** Strategy chosen based on data analysis
2. **Interactive:** Asks questions when needed, doesn't guess
3. **Continuous:** Health monitoring after delivery
4. **Compliant:** Security/privacy/GDPR gates before delivery
5. **Goal-driven:** Acceptance criteria defined upfront
6. **Feedback loops:** Adjusts based on monitoring + client input

**The Evidence Sprint delivers Stage 1-11 once.**
**Standard Care runs Stage 7-8 continuously.**
**Client questions trigger Stage 9 any time.**