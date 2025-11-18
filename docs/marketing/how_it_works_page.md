# How GraphCare Works

**URL:** `graphcare.mindprotocol.ai/how-it-works`
**Purpose:** Deep-dive explanation for users who want to understand the process
**Audience:** Technical decision-makers who saw the homepage demo and want details

---

## The Problem We Solve

Your codebase is undocumented knowledge locked in code.

**What breaks down:**
- Documentation goes stale within 3 months
- Onboarding new developers takes 2-3 weeks
- Critical architectural decisions are tribal knowledge
- When engineers leave, understanding leaves with them

**What you actually need:**
- Architecture that's always current (not a year-old diagram)
- API docs that match what's actually deployed
- Dependency maps that show what breaks what
- Test coverage that highlights risk areas

**Traditional solutions fail:**

| Solution | Why It Fails |
|----------|--------------|
| Manual docs | Stale in 3 months, nobody maintains them |
| Code comments | Fragmented, inconsistent, describes lines not systems |
| Wikis | Abandoned after initial enthusiasm |
| Static analysis tools | Data dumps, not insights. "Here's 10,000 lines of output, good luck" |

---

## Our Approach: Graph-Native Knowledge Extraction

We transform your codebase into a **queryable knowledge graph**.

Not PDFs. Not markdown files. Not a code browser.
A **graph database** where every function, service, endpoint, and document is a node you can query.

### What Makes Us Different

#### 1. Graph-Native (Not Documents)

**We don't generate static docs that go stale.**

Instead:
```cypher
// Show me all API endpoints
MATCH (e:U4_Code_Artifact {kind: 'Endpoint'})
RETURN e.name, e.path, e.method

// Show payment flow dependencies
MATCH (s:U4_Code_Artifact {kind: 'Service', name: 'PaymentService'})
      -[r*1..3]->(dep)
RETURN s, r, dep

// Show untested code
MATCH (c:U4_Code_Artifact)
WHERE NOT (c)-[:U4_TESTED_BY]->()
RETURN c.name, c.kind, c.complexity

// Architecture by layer
MATCH (s)-[:IN_LAYER]->(layer)
RETURN layer.name, collect(s.name) as services
```

**The difference:**
- Traditional docs: "Here's a PDF describing the payment service"
- GraphCare: "Query for exactly what you need, when you need it"

Architecture **emerges from the code itself**, not human interpretation that goes stale.

---

#### 2. Industry-Standard Type System

**We use universal semantic types, not proprietary formats.**

Every node is typed:
- `U4_Code_Artifact` (functions, classes, modules)
- `U4_Knowledge_Object` (docs, specs, ADRs)
- `U4_Assessment` (coverage reports, security scans)

Every relationship is typed:
- `CALLS` (function dependencies)
- `IMPLEMENTS` (code implements spec)
- `DOCUMENTS` (doc explains code)
- `TESTED_BY` (test validates code)

**Why this matters:**

Your data is **portable**. Export to:
- JSON (standard format)
- Cypher (graph query language)
- GraphQL (if you want to build your own UI)

No vendor lock-in. You own the graph.

**About Mind Protocol:**

GraphCare uses the Mind Protocol type system (44 node types, 23 relationship types) - an open standard for knowledge graphs. This means:
- Your graph can integrate with other tools that use Mind Protocol
- Future-proof: types are versioned and maintained
- Interoperable: export once, use anywhere

[Learn more about Mind Protocol →](https://mindprotocol.ai)

---

#### 3. Structure Extraction (Not Code Storage)

**Important security clarification:**

We extract the **STRUCTURE**, not the **CODE**.

**What we store:**
```json
{
  "type": "U4_Code_Artifact",
  "kind": "Service",
  "name": "PaymentService",
  "path": "services/payment/processor.py",
  "methods": ["processPayment", "refund", "validateCard"],
  "dependencies": ["StripeAPI", "DatabaseService"]
}
```

**What we DON'T store:**
- Your actual source code
- Business logic
- Proprietary algorithms
- Secrets/credentials (we scan for these and alert you)

**Security guarantee:**
- We clone your repo (read-only)
- We parse the structure (AST analysis)
- We generate the graph (relationships + metadata)
- **We delete your source code after extraction**
- You get the graph, we keep nothing

**Where the graph lives:**
- Option 1: Our hosted FalkorDB (encrypted, isolated per client)
- Option 2: Self-hosted (Enterprise tier - you run FalkorDB)
- Option 3: Export and host anywhere (full JSON/Cypher export included)

---

#### 4. Specialized Extraction Pipeline

**Most tools use generic LLM prompts.**
"Hey ChatGPT, tell me about this code."

**We use domain-specific analyzers:**

| Analyzer | What It Does |
|----------|--------------|
| **Semantic Clustering** | Groups related code by meaning (not just folder structure) |
| **Architecture Inference** | Detects patterns: "This is a service layer, this is an API layer" |
| **Security Validation** | Scans for PII, credentials, compliance violations |
| **Quality Assessment** | Identifies coverage gaps, high-complexity untested code |
| **Relationship Extraction** | Maps dependencies: imports, calls, implementations |

**Why this matters:**

Generic LLMs hallucinate. They make up relationships that don't exist.
Our pipeline uses **static analysis + semantic analysis** - no hallucinations.

<details>
<summary>Technical Details: How Our Pipeline Works</summary>

**Phase 1: Static Analysis**
- Tree-sitter AST parsing (multi-language)
- Import graph extraction (who depends on who)
- Call graph extraction (who calls who)
- Type inference (for dynamically-typed languages)

**Phase 2: Semantic Analysis**
- SentenceTransformers embeddings (code → vector space)
- Clustering (find related code across the codebase)
- Pattern detection (identify architectural patterns)
- Classification (Service, Endpoint, Schema, Model, etc.)

**Phase 3: Graph Assembly**
- Universal type mapping (code artifacts → U4 types)
- Relationship inference (CALLS, IMPLEMENTS, DOCUMENTS)
- FalkorDB import (graph database)
- Validation (ensure no orphan nodes, broken links)

**Phase 4: Human Synthesis**
- Architecture narrative (strategic insights)
- Executive summary (C-level translation)
- Onboarding guide (new developer path)

**We call these specialized analyzers "citizens" internally** - domain experts that work in parallel. But you don't need to care about our internal naming. You care about the output.

</details>

---

#### 5. Queryable (Not Static)

**Traditional docs:**
You search through PDFs, hoping someone documented what you need.

**GraphCare:**
You query for exactly what you need.

**Example queries:**

```cypher
// Show API surface for payment module
MATCH (endpoint:U4_Code_Artifact {kind: 'Endpoint'})
WHERE endpoint.path CONTAINS 'payment'
RETURN endpoint.name, endpoint.method, endpoint.path

// What services touch user data?
MATCH (service)-[:USES_SCHEMA]->(schema {name: 'User'})
RETURN service.name

// Map authentication flow
MATCH path = (entry:U4_Code_Artifact {name: 'login'})-[*1..5]->(exit)
RETURN path

// Find high-complexity untested code (risk areas)
MATCH (code:U4_Code_Artifact)
WHERE code.complexity > 7
  AND NOT (code)-[:U4_TESTED_BY]->()
RETURN code.name, code.complexity, code.path
ORDER BY code.complexity DESC
```

**Generate views on-demand:**
- Architecture diagram (services by layer)
- API reference (all endpoints, parameters, schemas)
- Coverage report (test coverage by module)
- Dependency graph (what breaks if X changes)
- Security surface (all endpoints that touch sensitive data)

Docs that **answer questions**, not PDFs you search through.

---

## The Process

### What You Get (Outcomes First)

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Queryable Graph                                          │
│    └─ Production FalkorDB or self-hosted                    │
│    └─ 100-500 nodes (depending on codebase size)           │
│    └─ Always queryable via Cypher, GraphQL, or our UI      │
│                                                             │
│ 2. Auto-Generated Views                                     │
│    ├─ Architecture (services by layer, boundaries)         │
│    ├─ API Reference (all endpoints, parameters)            │
│    ├─ Coverage Report (gaps by module, risk areas)         │
│    └─ Index (browseable catalog)                           │
│                                                             │
│ 3. Documentation Package                                    │
│    ├─ Executive summary (2 pages, C-level audience)        │
│    ├─ Architecture narrative (15 pages, technical depth)   │
│    ├─ Query cookbook (30+ examples for your use cases)     │
│    └─ Integration guide (how to consume the graph)         │
│                                                             │
│ 4. Security Audit                                           │
│    ├─ PII scan (emails, names, addresses in properties)    │
│    ├─ Credential scan (API keys, passwords - should be 0)  │
│    ├─ GDPR compliance (right-to-erasure, portability)      │
│    └─ Approval or block (CRITICAL issues prevent delivery) │
│                                                             │
│ 5. Optional: Ongoing Monitoring                             │
│    ├─ Health dashboard (uptime, performance, coverage)     │
│    ├─ Alerts (Slack/email when issues detected)            │
│    └─ Re-extraction (when code changes significantly)      │
└─────────────────────────────────────────────────────────────┘
```

### Timeline

- **Evidence Sprint:** 48 hours (extract 1 module)
- **Starter:** 3-5 days (full extraction, small codebase)
- **Professional:** 5-7 days (full extraction + human synthesis)
- **Enterprise:** Custom (multi-repo, complex architectures)

---

<details>
<summary>Show Me the Detailed Process (11 Stages)</summary>

### Stage 1-2: Connect & Prepare (1 hour)

**What happens:**
- You give us repo access (GitHub OAuth, read-only) or codebase export
- We verify scope (what to extract, what to exclude)
- We confirm privacy boundaries (any sensitive areas to skip?)
- We parse and normalize (Python, TypeScript, JavaScript, Go, Rust)

**Your involvement:** Initial handoff, answer scope questions

---

### Stage 3: Semantic Analysis (1-2 hours)

**What happens:**
Our semantic analyzer:
- Embeddings-based clustering (finds hidden structure in your code)
- Coverage assessment (code vs docs ratio, completeness check)
- Strategy recommendation: code-first, docs-first, or hybrid?

**Output:** Corpus analysis report
```
Your backend is well-structured (15 clear modules)
Your API docs are 60% complete vs actual code
Recommend: code-first for backend, docs-first for frontend
```

**Your involvement:** None (we share results in Stage 4)

---

### Stage 4-5: Approach & Goals (30 min)

**What happens:**
We review the analysis together:
- What do you need? Architecture guide? API docs? Coverage map?
- Set acceptance criteria: "All public endpoints documented"
- Timeline & pricing confirmed

**Your involvement:** Strategic discussion, set priorities

---

### Stage 6: Extraction (2-4 hours)

**What happens:**
Two analyzers run in parallel:

**Code Extraction:**
- All functions, classes, modules as nodes
- Call relationships (function A calls function B)
- Import dependencies (module A depends on module B)
- Language-tagged (py, ts, js, go, rust)

**Architecture Inference:**
- Adds `kind` property: Service, Endpoint, Schema, Model, Component
- Identifies layers: API, Business Logic, Data, Presentation
- Creates architectural relationships: IN_LAYER, EXPOSES, USES_SCHEMA

**Output:**
- Graph with 100-500 nodes
- 50-200 relationships
- Fully typed with universal semantics

**Example (Scopelock):**
```
172 nodes:
  - 131 Code Artifacts (Python + TypeScript)
  - 4 Architectural Layers
  - 17 Services
  - 16 Schemas
  - 13 Endpoints

54 relationships:
  - 30 IN_LAYER (services organized by layer)
  - 18 CALLS (code dependencies)
  - 3 EXPOSES (services → endpoints)
  - 3 USES_SCHEMA (endpoints → data contracts)
```

**Your involvement:** None (automated)

---

### Stage 7: Health Monitoring Setup (30 min)

**What happens:**
We configure monitoring:
- Resolver uptime checks
- Query performance tracking
- Error rate alerts
- Cache health metrics

**Output:** Dashboard + alert configuration (Slack/email)

**Your involvement:** Provide Slack webhook or email for alerts

---

### Stage 8-9: Iteration & Questions (variable)

**What happens:**
We refine based on findings:
- "We see 3 services but only 1 is tested - flag this?"
- "Found 15 endpoints, docs mention 18 - are 3 deprecated?"
- Batch questions (not daily interruptions)

**Your involvement:** Answer clarification questions (async, batched)

---

### Stage 10: Security Audit (30-45 min)

**What happens:**
Security scan:
- PII in graph (emails, names, addresses)
- Credentials leaked (API keys, passwords - should be 0)
- GDPR compliance (consent records, right-to-erasure capability)
- Access controls (who can query this graph?)

**Output:** Security report
- ✅ **APPROVED** = we ship
- ❌ **CRITICAL issues** = we block delivery and show you what to fix

**Your involvement:** Review security report, approve delivery

---

### Stage 11: Delivery (1-2 hours)

**What happens:**
Documentation packaging:
- Architecture guide (executive 2-page + technical 15-page)
- API reference (all endpoints, parameters, examples)
- Query cookbook (30+ examples tailored to your use cases)
- Integration guide (how to consume the graph)
- Health report (coverage metrics, recommendations)

**Final steps:**
- Run acceptance tests (your criteria from Stage 5)
- Walkthrough session with your team (1 hour)
- Hand off to ongoing care (monitoring, re-extraction options)

**Your involvement:** Acceptance review, team walkthrough

</details>

---

## Proof: Scopelock Case Study

**Client:** Scopelock (proposal automation SaaS)
**Codebase:** 50K LOC Python + TypeScript
**Timeline:** 12 hours (first delivery)
**Result:** 172 nodes, 54 relationships, 4 architectural layers

### What We Extracted

**Services (17):**
- TelegramBot, ClaudeRunner, UpworkProposalSubmitter
- EventProcessor, DraftGenerator, LeadEvaluator
- (11 more...)

**Schemas (16):**
- LeadEvaluation, ResponseDraft, Event
- UpworkJobListing, ProposalTemplate
- (11 more...)

**Endpoints (13):**
- `POST /upwork_webhook` - Receive Upwork job notifications
- `POST /telegram_webhook` - Handle Telegram commands
- `GET /health_check` - Service health monitoring
- (10 more...)

**Database Models (3):**
- Event, Draft, Lead

### Architectural Insights (Auto-Discovered)

**4 Layers:**
1. **API Layer** - Entry points (webhooks, health checks)
2. **Notification Layer** - Telegram, email alerts
3. **Automation Layer** - Proposal generation, submission
4. **Orchestration Layer** - Event processing, workflow coordination

**Relationships:**
- 30 services organized by layer (IN_LAYER)
- 18 code dependencies (CALLS)
- 6 architectural relationships (EXPOSES, USES_SCHEMA)

### Security Audit Results

- ✅ No PII in graph
- ✅ No credentials leaked
- ✅ GDPR compliant (all data deletable on request)
- ✅ **APPROVED for delivery**

### What Scopelock Can Now Query

```cypher
// Show me all Telegram notification logic
MATCH (n)-[:IN_LAYER]->(layer {name: 'Notification'})
WHERE n.name CONTAINS 'Telegram'
RETURN n
// Result: 8 nodes

// What endpoints touch the Draft schema?
MATCH (endpoint)-[:USES_SCHEMA]->(schema {name: 'Draft'})
RETURN endpoint.path, endpoint.method
// Result: 3 endpoints

// Map the full proposal submission flow
MATCH path = (webhook {name: 'upwork_webhook'})-[*1..5]->(submitter)
WHERE submitter.name CONTAINS 'Submitter'
RETURN path
// Result: 12-node graph

// Which services have 0% test coverage?
MATCH (service:U4_Code_Artifact {kind: 'Service'})
WHERE NOT (service)-[:U4_TESTED_BY]->()
RETURN service.name, service.complexity
// Result: Identifies 5 risk areas
```

**Status:** Production-deployed, queryable, monitored

[Explore Scopelock's Graph →](#) | [Read Full Case Study →](#)

---

## Pricing

### Core Offerings

**🌱 Evidence Sprint - $350**

Extract 1 service/module of your choice.

What you get:
- Mini-graph (25-50 nodes)
- Shows what full extraction would look like
- 48-hour turnaround
- 100% refund if not convinced

**Best for:** "Show me it works before I commit $2k"

[Link Your Repo - Start Sprint →](#)

---

**🚀 Starter - $2,000**

Full codebase extraction (small codebases <50K LOC).

What you get:
- Complete graph extraction (100-200 nodes typical)
- 4 auto-generated views (architecture, API, coverage, index)
- Security audit (PII scan, compliance check)
- 3-5 day delivery
- 1 month hosted access
- Email support

**Best for:** Startups, single-service apps, internal tools

[Link Your Repo - Start Extraction →](#)

---

**💼 Professional - $5,000**

Full extraction + human synthesis (medium codebases <200K LOC).

What you get:
- Complete graph extraction (500+ nodes typical)
- 4 auto-generated views + custom views (if needed)
- Human-written documentation:
  - Executive summary (2 pages)
  - Architecture narrative (15 pages)
  - Query cookbook (30+ examples)
- Security audit + compliance report
- 5-7 day delivery
- 6 months hosted access
- Priority Slack support

**Best for:** Scale-ups, production systems, multi-service architectures

[Contact Sales →](#)

---

**🏢 Enterprise - Custom Pricing**

Multi-repo, complex architectures, custom requirements.

What you get:
- Everything in Professional
- Multi-repository extraction (unified graph)
- Custom branding (your logo, colors)
- SSO integration (OAuth, SAML)
- On-premise deployment option
- 12 months hosted access
- Dedicated support channel

**Best for:** Large enterprises, compliance-heavy industries, self-hosting requirements

[Contact Sales →](#)

---

### Add-Ons (Optional)

**Re-Extraction:** $2,000 per re-extraction
- When your codebase changes significantly
- On-demand (you decide when)
- Alternative: Quarterly sync ($600/quarter - 3 re-extractions)

**Ongoing Monitoring:** $200/month
- Health dashboard (uptime, performance, coverage trends)
- Alerts (Slack/email when issues detected)
- Alternative: Self-host monitoring (we give you the scripts, free)

**Custom Views:** $500-$2,000 per view
- Dependency graphs, security surface, data flow
- One-time design + implementation
- Examples: "Show all PII touchpoints", "Map authentication flow"

**Extended Hosting:** Included in pricing
- Starter: 1 month (then $200/month)
- Professional: 6 months (then $200/month)
- Enterprise: 12 months (then $200/month)
- Alternative: Self-host or export (free)

---

### What Most Clients Do

**Most common path:**

1. **Evidence Sprint** ($350) - Try it on 1 module
2. **Professional** ($5,000) - Full extraction + docs
3. **Export Graph** (free, included) - Download JSON + Cypher
4. **Self-Host** (free) or Use Our Hosting ($200/month)
5. **Re-Extract On-Demand** ($2,000 when needed)

**Total Year 1:** $5,350 + optional hosting
**Total Year 2:** $2,000-$6,000 (only pay for re-extractions when needed)

No forced subscriptions. No ongoing fees unless you want ongoing services.

---

### Payment Terms

- 50% deposit to start extraction
- 50% on delivery
- Wire transfer or ACH
- Net-30 payment terms (Enterprise)

### 100% Money-Back Guarantee

Not satisfied with the extraction quality? Full refund. No questions asked.

---

## Why This Approach Works

### Traditional Documentation Dies Because:

1. **Separate from code** → Syncing is manual, everyone forgets
2. **Static** → Doesn't answer new questions
3. **Human-maintained** → Time-consuming, error-prone, abandoned

### Graph-Native Documentation Lives Because:

1. **Extracted from code** → Always in sync (re-extract when code changes)
2. **Queryable** → Answers any question you ask
3. **AI-maintained** → Updates automatically when you re-extract

---

## Your Codebase Is Already a Knowledge Graph

Every function calls other functions.
Every service depends on other services.
Every endpoint exposes schemas.
Every test validates code.

**These are relationships.** This is already a graph.

We just make it **visible** and **queryable**.

---

## Ready to Get Started?

[Link Your GitHub Repo →](#) Start $350 Evidence Sprint
[See Pricing](#pricing) All tiers and add-ons
[Explore Demo Graph →](#) See Scopelock's real graph
[Contact Sales](#contact) Enterprise or custom requirements

Questions? **hello@graphcare.ai** or [book a 15-min call](#)

---

**Built by GraphCare** | [Privacy Policy](#) | [Terms of Service](#) | [Technical Docs](#)
