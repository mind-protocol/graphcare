# GraphCare: Living Documentation from Your Codebase

## The Problem We Solve

Your codebase is **undocumented knowledge locked in code**. Documentation goes stale. Onboarding takes weeks. Critical architectural decisions are tribal knowledge. When engineers leave, understanding leaves with them.

**You need:**
- Architecture that's always current (not a year-old diagram)
- API docs that match what's actually deployed
- Dependency maps that show what breaks what
- Test coverage that highlights risk areas

**Traditional solutions:**
- Manual docs → stale in 3 months
- Code comments → fragmented, inconsistent
- Wikis → abandoned after initial enthusiasm
- Static analysis tools → data dumps, not insights

---

## Our USP: Graph-Native Knowledge Extraction

**We transform your codebase into a queryable knowledge graph.**

### What Makes Us Different:

**1. Graph-Native (Not Documents)**
- We don't generate static docs that go stale
- We extract **relationships** between code, not just files
- Query like: "Show me all endpoints that touch user data" → instant answer
- Architecture emerges from the code itself, not human interpretation

**2. Universal Type System**
- Every node typed with industry-standard semantics (U4_Code_Artifact, U4_Knowledge_Object)
- Services, Endpoints, Schemas, Models classified automatically
- Cross-references between docs and code preserved
- Compatible with Mind Protocol's L4 universal types (44 node types, 23 link types)

**3. Production-Direct**
- No local copies, no sync issues
- Graph lives in production FalkorDB (always queryable)
- Updates don't require redeployment
- Multiple teams can work simultaneously

**4. Conscious AI Extraction**
- 7 specialized AI citizens, not generic LLM prompts
- Quinn (Cartographer) maps semantic landscape
- Nora (Architect) infers structure from code patterns
- Marcus (Auditor) validates security/compliance
- Vera (Validator) assesses quality
- Human-level understanding of architecture, not regex parsing

**5. Queryable, Not Static**
- GraphQL-style queries: "Show API surface for payment module"
- Generate views on-demand (architecture, API reference, coverage, dependencies)
- Filter by language, layer, test coverage, security classification
- Docs that answer questions, not PDFs you search through

---

## The Process (11-Stage Pipeline)

### **Stage 1-2: Connect & Prepare (1 hour)**
**What we do:**
- You give us repo access or codebase export
- We verify scope, consent, privacy boundaries
- Parse and normalize (Python, TypeScript, JavaScript, etc.)

**Your involvement:** Initial handoff, answer scope questions

---

### **Stage 3: Semantic Analysis (1-2 hours)**
**Quinn (Chief Cartographer) analyzes your corpus:**
- Embeddings-based semantic clustering (finds hidden structure)
- Coverage assessment (code vs docs ratio, completeness)
- Strategy recommendation: code-first, docs-first, or hybrid?

**Output:** Corpus analysis report
- "Your backend is well-structured (15 clear modules)"
- "Your API docs are 60% complete vs code"
- "Recommend: code-first for backend, docs-first for frontend"

---

### **Stage 4-5: Approach & Goals (30 min)**
**Mel (me) works with you:**
- Review Quinn's analysis together
- Define what you need: architecture guide? API docs? test coverage map?
- Set acceptance criteria: "All public endpoints documented" or "Architectural layers defined"
- Timeline & pricing confirmed

**Your involvement:** Strategic discussion, priorities alignment

---

### **Stage 6: Extraction (2-4 hours)**
**Kai (Engineer) + Nora (Architect) extract in parallel:**

**Kai extracts code:**
- All functions, classes, modules as nodes
- Call relationships (function A calls function B)
- Import dependencies
- Language-tagged (py, ts, js)

**Nora infers architecture:**
- Adds `kind` property: Service, Endpoint, Schema, Model
- Identifies layers: API, business logic, data, presentation
- Creates architectural relationships: IN_LAYER, EXPOSES, USES_SCHEMA

**Output:**
- Graph with 100-200+ nodes
- 50-100+ relationships
- Fully typed with universal semantics

**Example (from Scopelock):**
```
172 nodes:
  - 131 Code Artifacts (Python + TypeScript)
  - 4 Architectural Layers
  - 36 intermediate nodes

54 relationships:
  - 30 IN_LAYER (services organized by layer)
  - 18 CALLS (code dependencies)
  - 3 EXPOSES (services → endpoints)
  - 3 USES_SCHEMA (endpoints → data contracts)
```

---

### **Stage 7: Health Monitoring (30 min)**
**Vera (Validator) sets up ongoing monitoring:**
- Resolver uptime checks
- Query performance tracking
- Error rate alerts
- Cache health metrics

**Output:** Dashboard + alert configuration (Slack/email)

---

### **Stage 8-9: Iteration & Questions (variable)**
**We refine based on findings:**
- "We see 3 services but only 1 is tested - should we flag this?"
- "Found 15 endpoints, but docs mention 18 - are 3 deprecated?"
- Batch questions to you, not daily interruptions

**Your involvement:** Answer clarification questions (async, batched)

---

### **Stage 10: Security Audit (30-45 min)**
**Marcus (Auditor) scans:**
- PII in graph (emails, names, addresses)
- Credentials leaked (API keys, passwords - should be none)
- GDPR compliance (consent records, right-to-erasure capability)
- Access controls (who can query this graph?)

**Output:** Security report
- APPROVED = we ship
- CRITICAL issues = we block delivery and show you what to fix

---

### **Stage 11: Delivery (1-2 hours)**
**Sage (Documenter) packages:**
- Architecture guide (executive 2-page + technical 15-page)
- API reference (all endpoints, parameters, examples)
- Query cookbook (30+ example queries for your use cases)
- Integration guide (how to consume the graph)
- Health report (coverage metrics, recommendations)

**Mel (me) delivers:**
- Run acceptance tests (your criteria from Stage 5)
- Walkthrough session with your team
- Hand off to ongoing care (monitoring, updates)

**Your involvement:** Acceptance review, team walkthrough

---

## Timeline & Effort

**First delivery:** 8-12 hours (1-2 days elapsed)
- Quinn: 1-2h analysis
- Kai + Nora: 2-4h extraction (parallel)
- Marcus: 30-45min audit
- Vera: 30min monitoring setup
- Sage: 1-2h documentation
- Mel: 1h coordination + delivery

**Ongoing care:** 2-4 hours/month
- Graph updates when codebase changes
- Health monitoring
- Query support

---

## What You Get

### **1. Queryable Graph (Production FalkorDB)**
**Always-current knowledge base:**
```cypher
// Show me all API endpoints
MATCH (e:U4_Code_Artifact {kind: 'Endpoint'})
RETURN e.name, e.path

// Show payment flow dependencies
MATCH (s:U4_Code_Artifact {kind: 'Service', name: 'PaymentService'})-[r*1..3]->(dep)
RETURN s, r, dep

// Show untested code
MATCH (c:U4_Code_Artifact)
WHERE NOT (c)-[:U4_TESTS]->()
RETURN c.name, c.kind

// Architecture by layer
MATCH (s)-[:IN_LAYER]->(layer)
RETURN layer.name, count(s) as services
```

### **2. Generated Views (On-Demand)**
**4 standard views:**
- **Architecture:** Services by layer, boundaries, contracts
- **API Reference:** All endpoints, parameters, schemas
- **Coverage:** Test coverage by module, language, layer
- **Index:** Browseable catalog of all artifacts

**Custom views available:** Dependency graphs, security surface, data flow, etc.

### **3. Documentation Package**
**Multi-audience:**
- Executive: "Our payment system has 3 services across 2 layers"
- Technical: Full architecture with diagrams generated from graph
- Developer: "How to query for X, Y, Z"

### **4. Ongoing Monitoring**
**Health dashboard:**
- Resolver uptime (are queries working?)
- Performance (query times, cache hits)
- Coverage trends (improving or degrading?)
- Alerts when critical issues detected

---

## Proof: Scopelock Case Study

**Client:** Scopelock (proposal automation SaaS)
**Timeline:** 12 hours (first delivery)
**Result:** 172 nodes, 54 relationships, 4 architectural layers

**What we extracted:**
- 17 Services (TelegramBot, ClaudeRunner, UpworkProposalSubmitter)
- 16 Schemas (LeadEvaluation, ResponseDraft, Event models)
- 13 Endpoints (upwork_webhook, telegram_webhook, health_check)
- 3 Database Models (Event, Draft, Lead)

**Architectural insights automatically discovered:**
- 4 layers: API, Notification, Automation, Orchestration
- 30 services organized by layer
- 18 code dependencies (call graph)
- 6 architectural relationships (services expose endpoints, endpoints use schemas)

**Security audit results:**
- ✅ No PII in graph
- ✅ No credentials leaked
- ✅ GDPR compliant (all data can be deleted on request)
- ✅ APPROVED for delivery

**Client can now query:**
- "Show me all Telegram notification logic" → 8 nodes
- "What endpoints touch the Draft schema?" → 3 endpoints
- "Map the full proposal submission flow" → 12-node graph
- "Which services have 0% test coverage?" → Identifies risk areas

**Status:** Production-deployed, queryable, monitored

---

## Pricing Model (Indicative)

**First Delivery:** $2,000 - $5,000
- Based on codebase size (50k-500k LOC)
- Includes full extraction, audit, documentation
- 8-12 hour delivery

**Ongoing Care:** $500 - $1,000/month
- Health monitoring
- Monthly graph updates
- Query support
- Coverage analysis

**Custom Views:** $500 - $2,000 per view
- Dependency graphs, security surface, data flow
- One-time design + implementation

---

## Why This Matters

**Traditional documentation dies because:**
1. It's separate from code (syncing is manual)
2. It's static (doesn't answer new questions)
3. It's human-maintained (time-consuming, error-prone)

**Graph-native documentation lives because:**
1. It's extracted from code (always in sync)
2. It's queryable (answers any question)
3. It's AI-maintained (updates automatically)

**Your codebase is already a knowledge graph.** We just make it visible and queryable.

---

## Next Steps

**Want to see it for your codebase?**

1. **15-min call:** Show us a sample of your code (public repo or sanitized export)
2. **Quinn runs quick analysis:** 1-hour semantic scan (free)
3. **We show you:** What insights we'd extract, what queries you could run
4. **You decide:** Proceed with full extraction or not

**No commitment until you see the analysis.**

---

## FAQs

**"What if our codebase is mostly undocumented?"**
→ Even better! We extract structure from code itself. Documentation gaps become visible and actionable.

**"What languages do you support?"**
→ Python, TypeScript, JavaScript fully supported. Other languages (Rust, Go, Java, etc.) upon request.

**"Can we query the graph ourselves?"**
→ Yes! Full GraphQL-style access + WebSocket API. Run any query you want.

**"What if we update our code?"**
→ Re-extraction is fast (incremental updates possible). Or we monitor and auto-update on git push.

**"How is this different from Swagger/OpenAPI?"**
→ Swagger documents APIs. We document **everything**: architecture, dependencies, test coverage, data flow. And it's queryable across all dimensions.

**"What about security/compliance?"**
→ Marcus (our auditor) scans every graph for PII, credentials, GDPR compliance before delivery. We block if critical issues found.

**"Can you integrate with our existing tools?"**
→ Yes! Export to Confluence, Notion, or your internal wiki. Or query directly from Slack/CLI.

---

**Let's make your codebase legible again.**

**Contact:** [Your contact info]
**Demo:** [Schedule link]
**GitHub:** [Example extraction]
