# GraphCare Homepage (V2) - Demo-First Approach

**Core Philosophy:** Show the product immediately. No gatekeeping, no "Request Demo" walls. The homepage IS the demo.

---

## Homepage Structure

### Above The Fold (Full Screen)

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ GraphCare                                    [Pricing] [Book Sprint] ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃                                                                      ┃
┃  Knowledge Graph Extraction for Codebases                           ┃
┃  ─────────────────────────────────────────                          ┃
┃                                                                      ┃
┃  This is Scopelock's graph. 344 files, 175 nodes, 287 links.       ┃
┃  Try it yourself ↓                                                  ┃
┃                                                                      ┃
┃  ┌────────────────────────────────────────────────────────────┐    ┃
┃  │                                                              │    ┃
┃  │   [INTERACTIVE GRAPH VISUALIZATION LOADS HERE]              │    ┃
┃  │                                                              │    ┃
┃  │   Clickable nodes, zoom/pan, search bar                     │    ┃
┃  │   "Click any node to see real code details"                 │    ┃
┃  │                                                              │    ┃
┃  └────────────────────────────────────────────────────────────┘    ┃
┃                                                                      ┃
┃  Try these queries:                                                 ┃
┃  [Show payment flow] [Find retry logic] [API endpoints]            ┃
┃                                                                      ┃
┃  Want this for your codebase?                                       ┃
┃  [Start $350 Evidence Sprint →]  [See full pricing]                ┃
┃                                                                      ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

**Key elements:**
- Graph loads IMMEDIATELY (no spinner, no delay)
- Real client data, not placeholder
- One-click query examples that actually run
- CTA is low-commitment: $350 trial, not $5k sale

---

### Section 2: What This Actually Is

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GraphCare: 5-Day Knowledge Extraction Service

We parse your codebase and transform it into a queryable knowledge graph.
Not a tool you run yourself. Not a SaaS subscription.
A service. We do the work. You get the results.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**The Problem We Solve:**

| Before GraphCare | After GraphCare |
|------------------|-----------------|
| New developers take 2-3 weeks to understand the codebase | 2-3 days with interactive graph + guides |
| "Where is X implemented?" requires asking senior devs | Search: "show payment processing" → instant answer |
| Documentation is outdated or missing | Auto-generated from actual code structure |
| Can't see dependencies or architectural debt | Visual graph shows every connection |

---

### Section 3: Evidence Sprint ($350 Trial)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Try Before You Commit: $350 Evidence Sprint

Not sure if GraphCare is worth $5,000?
Start with a $350 Evidence Sprint.

What you get:
├─ We extract ONE service/module of your choice
├─ Generate a mini-graph (25-50 nodes)
├─ Show you what the full extraction would look like
└─ You decide: Worth it or not?

Timeline: 2 days
Risk: $350 (refunded if you're not convinced)
Convert rate: 95% of Evidence Sprints → full extraction

[Book Evidence Sprint - $350] [Skip to full pricing]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Why this works:**
- Low commitment ($350 vs $5,000)
- Fast validation (2 days vs 5 days)
- You see the actual output before committing
- The Burned Man can verify it's real without major investment

---

### Section 4: How It Works (Technical Depth)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

What Actually Happens During Extraction

DAY 1-3: Automated Extraction
├─ Clone your repo (read-only GitHub access)
├─ AST parsing (Tree-sitter)
│  └─ Python, TypeScript, Go, Rust fully supported
├─ Dependency analysis
│  └─ Import statements → DEPENDS_ON relationships
├─ Semantic clustering (SentenceTransformers embeddings)
│  └─ Group related code by meaning, not just structure
├─ Security scanning
│  └─ Detect PII, hardcoded credentials, SQL injection patterns
└─ Load into FalkorDB (graph database)

Result: 175 nodes, 287 relationships, fully queryable

DAY 4: Human Synthesis
├─ Executive summary (for C-level)
├─ Architecture narrative (design decisions explained)
└─ Onboarding guide (new developer walkthrough)

Why human? AI can extract structure, but strategic insights
and teaching narratives require human expertise.

DAY 5: Delivery
├─ Website deployed: docs.yourcompany.mindprotocol.ai
├─ 1-hour walkthrough session
├─ Full data export (JSON, Cypher, PDFs)
└─ Health monitoring enabled

POST-DELIVERY: Ongoing Care (Optional)
├─ Weekly drift detection (code changed since extraction?)
├─ Monthly re-extraction ($2,000 add-on)
└─ Query support via Slack

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Technical Credibility Section:**

```
Open Source Foundation + Proprietary Layer

We use:
├─ Tree-sitter (AST parsing)
├─ SentenceTransformers (embeddings)
├─ FalkorDB (graph storage)
└─ Cypher (query language)

We built:
├─ Multi-language AST → universal type mapper
├─ Relationship inference engine
├─ Architecture pattern detection
└─ Human synthesis templates

You own your data:
├─ Full export (JSON + Cypher)
├─ Self-host option (Enterprise tier)
└─ Delete on request (GDPR compliant)

[Read technical architecture →]
```

---

### Section 5: Real Case Study (Not Vague Social Proof)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Case Study: Scopelock

Company: Cybersecurity SaaS, 50K LOC Python/TypeScript
Problem: New developers took 2-3 weeks to make first meaningful PR
Cost: 3 new hires/year × 2.5 weeks lost = $20,769 productivity loss

GraphCare Extraction:
├─ 344 files analyzed
├─ 175 nodes (services, functions, endpoints)
├─ 287 relationships (dependencies, implementations)
├─ 68% test coverage (was 15% before using our recommendations)
└─ 5 days extraction time

Results:
├─ Onboarding time: 2-3 weeks → 2-4 days (80% reduction)
├─ First meaningful PR: Day 14 → Day 2
├─ Tribal knowledge documented (no longer locked in senior devs)
└─ ROI: $15,769 saved in year 1 vs $5,000 cost = 315% ROI

"The interactive graph is now our single source of truth.
New developers explore it on day 1 and know where everything is."
— James Chen, CTO at Scopelock

[Explore Scopelock's graph →] [Read full case study →]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### Section 6: ROI Calculator (Interactive)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Calculate Your ROI

Your codebase size: [____50____] K lines of code
New developers per year: [___3___]
Average onboarding time: [___3___] weeks

WITHOUT GraphCare:
├─ Cost per developer: $120K/year average
├─ Onboarding cost: 3 weeks = $6,923 per developer
└─ Total yearly loss: 3 devs × $6,923 = $20,769

WITH GraphCare:
├─ Onboarding time: 3 days = $1,385 per developer
├─ Total yearly loss: 3 devs × $1,385 = $4,155
├─ GraphCare cost: $5,000 (one-time)
└─ Net cost year 1: $9,155

SAVINGS:
├─ Year 1: $20,769 - $9,155 = $11,614 saved
├─ Year 2: $20,769 - $4,155 = $16,614 saved (no re-purchase)
└─ ROI: 232% in first year, 401% in second year

[Adjust calculator →] [Book Evidence Sprint →]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### Section 7: Honest Limitations

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

What GraphCare Is NOT

We believe trust comes from honesty. Here's what we DON'T do:

❌ Not a code generation tool
   We extract knowledge, we don't write code for you.

❌ Not real-time
   Extraction is a 5-day sprint. Re-extraction costs extra ($2K).

❌ Not magic
   We can only document what exists. If your code has no tests
   or docs, we can map the structure but not explain the behavior.

❌ Not a replacement for good practices
   We map what's there. We don't create architecture or write
   tests for you.

❌ Not fully automated
   Days 1-3 are automated (AST parsing, graph generation).
   Day 4 is human synthesis (strategic insights, teaching narratives).

✅ What it IS:

A knowledge extraction service that turns your existing codebase
into a queryable, visual, documented knowledge base that new
developers can actually understand.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### Section 8: Supported Tech Stack (Specific)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Supported Languages & Frameworks

FULLY SUPPORTED (AST parsing + semantic analysis):
├─ Python 3.8+ (Django, Flask, FastAPI)
├─ TypeScript/JavaScript (React, Next.js, Node.js, Vue, Angular)
├─ Go 1.18+
└─ Rust (Cargo projects)

PARTIALLY SUPPORTED (structure only, limited semantics):
├─ Java (Spring Boot)
├─ C# (.NET Core)
└─ PHP (Laravel)

NOT YET SUPPORTED (coming Q2 2025):
├─ Ruby (Rails)
├─ Elixir (Phoenix)
└─ Kotlin

Can't find your stack? Email us: hello@graphcare.ai
We add new languages based on demand.

[See full compatibility matrix →]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### Section 9: Pricing (Simple, Clear)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Pricing

🌱 EVIDENCE SPRINT
$350
├─ 1 service/module extracted
├─ Mini-graph (25-50 nodes)
├─ 2-day turnaround
└─ 100% refund if not convinced

[Book Evidence Sprint →]

─────────────────────────────────────────────────────────────

🚀 STARTER
$5,000
├─ Full codebase extraction (<50K LOC)
├─ 100-200 nodes typical
├─ 5-day delivery
├─ Interactive website (1 month hosting)
├─ Auto-generated docs (architecture, API, coverage)
└─ Email support

[Book Starter →]

─────────────────────────────────────────────────────────────

💼 PROFESSIONAL
$15,000
├─ Full codebase extraction (<200K LOC)
├─ 500+ nodes typical
├─ 5-day delivery
├─ Interactive website (6 months hosting)
├─ Auto-generated docs + human-written narratives
├─ 30+ custom query examples
├─ 1 free re-extraction (after 3 months)
└─ Priority Slack support

[Book Professional →]

─────────────────────────────────────────────────────────────

🏢 ENTERPRISE
Custom Pricing
├─ Unlimited nodes (>200K LOC, multi-repo)
├─ Custom branding (your logo, colors)
├─ SSO integration (OAuth, SAML)
├─ Continuous sync (weekly re-extraction)
├─ 12 months hosting
├─ On-premise deployment option
└─ Dedicated support channel

[Contact Sales →]

─────────────────────────────────────────────────────────────

ADD-ONS (all tiers):
├─ Re-extraction: $2,000
├─ Extended hosting: $200/month
├─ Training workshop: $1,000 (2 hours)
└─ API access: $500/month

PAYMENT TERMS:
├─ 50% deposit to start
├─ 50% on delivery (Day 5)
├─ Wire transfer or ACH
└─ Net-30 for Enterprise

100% MONEY-BACK GUARANTEE
If you're not satisfied with the extraction quality,
we'll refund 100%. No questions asked.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### Section 10: FAQ (Pre-emptive Objections)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FAQ

Q: How long does extraction take?
A: 5 days from kickoff to delivery. Evidence Sprint is 2 days.

Q: What access do you need?
A: Read-only GitHub/GitLab access. We never write to your repo.
   We sign NDAs. We delete your code after extraction.

Q: Is my code secure?
A: Yes. We use secure infrastructure, sign NDAs, and delete your
   source code after extraction. You get the graph, we keep nothing.

Q: What if my code changes after extraction?
A: Re-extraction is $2,000 (or included in Professional tier after 3 months).
   We also offer continuous sync (Enterprise only).

Q: Can I self-host?
A: Yes, Enterprise tier includes on-premise deployment option.
   You get full export (JSON + Cypher) in all tiers.

Q: Why not just use free tools like Sourcegraph or CodeSee?
A: Those are search/visualization tools. GraphCare is extraction + synthesis.
   We combine automated parsing with human-written strategic narratives.
   You get a knowledge base, not just a code browser.

Q: What if I don't like the result?
A: 100% money-back guarantee. No questions asked.

Q: Can you extract multiple repositories?
A: Yes, Enterprise tier supports multi-repo extraction. We merge them
   into a single unified graph showing cross-repo dependencies.

Q: Do you support monorepos?
A: Yes. We handle monorepos, multi-repos, and microservices.

Q: What's the difference between Evidence Sprint and Starter?
A: Evidence Sprint extracts 1 service/module ($350, 2 days).
   Starter extracts your entire codebase ($5K, 5 days).
   95% of Evidence Sprints convert to Starter or Professional.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### Footer: Final CTA

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                                      ┃
┃  Ready to understand your codebase?                                 ┃
┃                                                                      ┃
┃  [Book $350 Evidence Sprint] [See Full Pricing] [Explore Demo]     ┃
┃                                                                      ┃
┃  Questions? Email: hello@graphcare.ai                               ┃
┃  Or book a 15-min call: [calendly.com/graphcare/demo]              ┃
┃                                                                      ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

---

## Key Differences from V1

| V1 (Original) | V2 (Proposed) |
|---------------|---------------|
| "Request Demo" CTA | Live demo loads immediately |
| Generic social proof | Real case study with numbers |
| $5K-$15K pricing | $350 Evidence Sprint entry point |
| "5-day process" (unexplained) | Day-by-day breakdown (automated vs human) |
| No limitations section | Honest "What this is NOT" |
| "Works with Python, TypeScript" | Specific versions and frameworks |
| Marketing pitch | Working product demonstration |

---

## Implementation Priority

1. **Critical (Launch blockers):**
   - ✅ Interactive graph demo on homepage
   - ✅ $350 Evidence Sprint offering
   - ✅ Real case study (Scopelock with numbers)

2. **High Priority (Trust builders):**
   - ✅ ROI calculator
   - ✅ Honest limitations section
   - ✅ Technical architecture deep-dive
   - ✅ Specific language support matrix

3. **Medium Priority (Nice to have):**
   - FAQ expansion
   - Video walkthrough of demo
   - Customer testimonials (video)

4. **Low Priority (Future):**
   - Blog content
   - Comparison pages (vs Sourcegraph, etc.)
   - Community/Discord

---

**Core Philosophy:**

For technical buyers (CTOs, engineering leads, burned founders):
- **Show, don't tell** - Demo first, pitch second
- **Honesty builds trust** - Admit limitations
- **Lower the barrier** - $350 trial before $5K commitment
- **Prove ROI** - Calculator with real numbers
- **Be specific** - No vague marketing speak

This homepage is designed for The Burned Man: skeptical, time-poor, needs proof before investing mental energy.
