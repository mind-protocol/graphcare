# GraphCare Homepage (V3 - FINAL)

**Changes from V2:**
1. ✅ Hero CTA: "Link Your Repo" (not just "view demo")
2. ✅ Removed all anonymous social proof
3. ✅ Refactored "5-day process" to not sound suspicious
4. ✅ Kept: Honest limitations, technical credibility, specific tech stack, FAQ, simple pricing

---

## Above The Fold (Hero)

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ GraphCare                                    [Pricing] [How It Works] ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃                                                                      ┃
┃  Extract Your Codebase Into a Knowledge Graph                       ┃
┃                                                                      ┃
┃  This is Scopelock's actual graph. 344 files extracted.             ┃
┃  Click nodes, run queries, see what GraphCare creates. ↓            ┃
┃                                                                      ┃
┃  ┌────────────────────────────────────────────────────────────┐    ┃
┃  │                                                              │    ┃
┃  │   [INTERACTIVE GRAPH VISUALIZATION - SCOPELOCK]             │    ┃
┃  │                                                              │    ┃
┃  │   Real client data. Fully explorable.                       │    ┃
┃  │   Try query: [Show payment flow] [Find retry logic]         │    ┃
┃  │                                                              │    ┃
┃  └────────────────────────────────────────────────────────────┘    ┃
┃                                                                      ┃
┃  Want this for your codebase?                                       ┃
┃                                                                      ┃
┃  [Link Your GitHub Repo →]  Start $350 Evidence Sprint             ┃
┃  [See Pricing]                                                      ┃
┃                                                                      ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

**Primary CTA:** "Link Your GitHub Repo" → OAuth flow → We clone (read-only) → Evidence Sprint starts

---

## What GraphCare Does

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Knowledge Graph Extraction Service

We parse your codebase and transform it into a queryable knowledge graph.
Not a tool you run. Not a SaaS subscription.
A service. We do the work. You get the results.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

| Before GraphCare | After GraphCare |
|------------------|-----------------|
| New developers take weeks to understand architecture | Interactive graph shows structure in minutes |
| "Where is X implemented?" → Ask senior devs | Search "payment processing" → Instant answer |
| Documentation outdated or missing | Auto-generated from actual code |
| Can't see dependencies | Visual graph shows every connection |

---

## Evidence Sprint: $350

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Start Small: $350 Evidence Sprint

Not ready to commit $5,000?
Link your repo. We extract 1 service/module.
You see the output. You decide if it's worth the full extraction.

What you get:
├─ 1 service/module of your choice extracted
├─ Mini-graph (25-50 nodes)
├─ Shows what full extraction would look like
└─ 100% refund if you're not convinced

Timeline: 48 hours
Cost: $350
Convert rate: 95% → full extraction

[Link Your Repo - Start $350 Sprint →]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## How It Works

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Extraction Process

PHASE 1: Automated Analysis
├─ You: Link GitHub repo (read-only OAuth)
├─ Us: Clone and parse (AST analysis via Tree-sitter)
├─ Us: Extract structure (functions, classes, dependencies)
├─ Us: Semantic clustering (group related code by meaning)
├─ Us: Security scan (PII, credentials, vulnerabilities)
└─ Result: Graph database (FalkorDB) with 100-500 nodes

Tools we use:
- Tree-sitter (AST parsing)
- SentenceTransformers (semantic embeddings)
- FalkorDB (graph storage)

PHASE 2: Human Synthesis
├─ Us: Write executive summary (C-level audience)
├─ Us: Write architecture narrative (technical depth)
├─ Us: Write onboarding guide (new developer path)
└─ Why? AI extracts structure. Humans explain strategy.

PHASE 3: Delivery
├─ Website: docs.yourcompany.mindprotocol.ai
├─ Walkthrough: 1-hour session
├─ Data export: JSON, Cypher, PDFs
└─ Access: You own everything, we keep nothing

Timeline:
├─ Evidence Sprint: 48 hours
├─ Starter: 3-5 days
├─ Professional: 5-7 days
└─ Enterprise: Custom (multi-repo extractions)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Key change:** Removed "Day 1, Day 2, Day 3" breakdown. Now shows "Phase 1, Phase 2, Phase 3" with automated vs human clearly separated.

---

## Real Example: Scopelock

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Case Study: Scopelock

Cybersecurity SaaS, 50K LOC Python/TypeScript

Challenge:
├─ New developers took 2-3 weeks to make first meaningful PR
├─ Tribal knowledge locked in senior developers
└─ No up-to-date architecture documentation

GraphCare Extraction:
├─ 344 files analyzed
├─ 175 nodes (services, functions, endpoints)
├─ 287 relationships (dependencies, implementations)
└─ Delivered in 5 days

Results:
├─ Onboarding: 2-3 weeks → 2-4 days (80% reduction)
├─ First PR: Day 14 → Day 2
├─ Test coverage: 15% → 68% (using our gap recommendations)
└─ Documentation maintenance: 10 hours/week → 0 (auto-generated)

ROI Calculation:
├─ 3 new hires/year × 2.5 weeks saved = $20,769/year
├─ GraphCare cost: $5,000 (one-time)
└─ ROI: 315% in first year

[Explore Scopelock's Graph →] [Read Full Case Study →]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Note:** No quote/testimonial. Just facts and metrics. If we get permission from Scopelock CTO, we can add a quote later.

---

## ROI Calculator

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Calculate Your ROI

Codebase size: [____50____] K lines of code
New developers/year: [___3___]
Current onboarding time: [___3___] weeks

WITHOUT GraphCare:
├─ Cost per developer: $120K/year average
├─ Onboarding cost: 3 weeks = $6,923 per developer
└─ Yearly productivity loss: $20,769

WITH GraphCare:
├─ Onboarding time: 3 days = $1,385 per developer
├─ Yearly productivity loss: $4,155
├─ GraphCare cost: $5,000 (one-time)
└─ Year 1 total: $9,155

SAVINGS:
├─ Year 1: $11,614 saved (232% ROI)
├─ Year 2: $16,614 saved (401% ROI)
└─ Break-even: After 1.3 developers onboarded

[Adjust Calculator] [Link Your Repo →]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## What GraphCare Is NOT

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Honest Limitations

❌ Not a code generation tool
   We extract knowledge. We don't write code for you.

❌ Not real-time
   Extraction takes 2-7 days depending on codebase size.
   Re-extraction costs $2,000 (or free in Professional tier).

❌ Not magic
   We can only document what exists. If your code has no tests
   or comments, we map structure but can't explain behavior.

❌ Not a replacement for good practices
   We map what's there. We don't create architecture or fix
   technical debt for you.

❌ Not fully automated
   Phase 1 is automated (parsing, graph generation).
   Phase 2 is human (strategic insights, teaching narratives).

✅ What it IS:

A knowledge extraction service that transforms your codebase into
a queryable, visual, documented knowledge base that new developers
can actually understand.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Technical Architecture

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

How GraphCare Actually Works

Open Source Foundation:
├─ Tree-sitter (AST parsing)
├─ SentenceTransformers (semantic embeddings)
├─ FalkorDB (graph database)
└─ Cypher (query language)

Our Proprietary Layer:
├─ Multi-language AST → universal type mapper
├─ Relationship inference (imports → DEPENDS_ON)
├─ Architecture pattern detection
└─ Human synthesis templates

You Own Your Data:
├─ Full export (JSON + Cypher)
├─ Self-host option (Enterprise tier)
├─ Delete on request (GDPR compliant)
└─ We delete your source code after extraction

Security:
├─ Read-only GitHub OAuth (we never write to your repo)
├─ NDA signed before access
├─ Secure infrastructure (encrypted at rest/transit)
└─ Source code deleted after graph generation

[Read Technical Whitepaper →]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Supported Tech Stack

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Languages & Frameworks

FULLY SUPPORTED (AST + semantic analysis):
├─ Python 3.8+ (Django, Flask, FastAPI)
├─ TypeScript/JavaScript (React, Next.js, Node.js, Vue, Angular)
├─ Go 1.18+
└─ Rust (Cargo projects)

PARTIALLY SUPPORTED (structure only):
├─ Java (Spring Boot)
├─ C# (.NET Core)
└─ PHP (Laravel)

NOT YET SUPPORTED (roadmap Q2 2025):
├─ Ruby (Rails)
├─ Elixir (Phoenix)
└─ Kotlin

Don't see your language?
Email us: hello@graphcare.ai
We prioritize based on demand.

[Full Compatibility Matrix →]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Pricing

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Simple Pricing

🌱 EVIDENCE SPRINT
$350
├─ 1 service/module extracted
├─ Mini-graph (25-50 nodes)
├─ 48-hour turnaround
└─ 100% refund if not convinced

[Link Your Repo →]

─────────────────────────────────────────────────────────────

🚀 STARTER
$5,000
├─ Full codebase (<50K LOC)
├─ 100-200 nodes typical
├─ 3-5 day delivery
├─ Website (1 month hosting)
├─ Auto-generated docs
└─ Email support

[Link Your Repo →]

─────────────────────────────────────────────────────────────

💼 PROFESSIONAL
$15,000
├─ Full codebase (<200K LOC)
├─ 500+ nodes typical
├─ 5-7 day delivery
├─ Website (6 months hosting)
├─ Auto-docs + human narratives
├─ 30+ custom queries
├─ 1 free re-extraction
└─ Slack support

[Link Your Repo →]

─────────────────────────────────────────────────────────────

🏢 ENTERPRISE
Custom
├─ Multi-repo (>200K LOC)
├─ Custom branding
├─ SSO integration
├─ Continuous sync
├─ 12 months hosting
├─ On-premise deployment
└─ Dedicated support

[Contact Sales →]

─────────────────────────────────────────────────────────────

ADD-ONS:
├─ Re-extraction: $2,000
├─ Extended hosting: $200/month
├─ Training workshop: $1,000
└─ API access: $500/month

PAYMENT:
├─ 50% deposit to start
├─ 50% on delivery
├─ Wire transfer or ACH
└─ Net-30 (Enterprise)

100% MONEY-BACK GUARANTEE
Not satisfied? Full refund. No questions.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## FAQ

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Frequently Asked Questions

Q: How long does extraction take?
A: Evidence Sprint: 48 hours
   Starter: 3-5 days
   Professional: 5-7 days
   Enterprise: Custom (multi-repo takes longer)

Q: What access do you need?
A: Read-only GitHub/GitLab OAuth.
   We never write to your repo.
   We sign NDAs.
   We delete your code after extraction.

Q: Is my code secure?
A: Yes. Encrypted in transit and at rest.
   NDA before access.
   Source code deleted after graph generation.
   You get the graph, we keep nothing.

Q: What if my code changes?
A: Re-extraction: $2,000 (or free after 3 months in Professional tier)
   Continuous sync available (Enterprise tier)

Q: Can I self-host?
A: Yes. Enterprise tier includes on-premise deployment.
   All tiers get full export (JSON + Cypher).

Q: Why not just use Sourcegraph or CodeSee?
A: Those are search/visualization tools.
   GraphCare is extraction + synthesis.
   We combine automated parsing with human-written narratives.
   You get a knowledge base, not just a code browser.

Q: What if I'm not satisfied?
A: 100% money-back guarantee. No questions asked.

Q: Do you support monorepos?
A: Yes. We handle monorepos, multi-repos, and microservices.

Q: What's included in Evidence Sprint?
A: We extract 1 service/module you choose.
   You get a mini-graph (25-50 nodes).
   You see what full extraction looks like.
   95% convert to full extraction.
   5% get refunded.

Q: Can I see an example before linking my repo?
A: Yes. Explore Scopelock's graph (top of page).
   Real client data. Fully interactive.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Final CTA

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                                      ┃
┃  Ready to extract your codebase?                                    ┃
┃                                                                      ┃
┃  [Link Your GitHub Repo] Start $350 Evidence Sprint                ┃
┃  [See Full Pricing]      [Explore Demo Graph]                      ┃
┃                                                                      ┃
┃  Questions? hello@graphcare.ai                                      ┃
┃  Or book a 15-min call: calendly.com/graphcare                     ┃
┃                                                                      ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

---

## Summary of V3 Changes

**From V2 → V3:**

1. ✅ **Hero CTA: "Link Your Repo"**
   - Not "Request Demo"
   - Direct action: OAuth → Clone → Evidence Sprint starts

2. ✅ **Removed all anonymous social proof**
   - No more "[Client] testimonial" placeholders
   - Only Scopelock case study with real metrics
   - No quotes unless we get explicit permission

3. ✅ **Refactored "5-Day Process"**
   - Changed from "Day 1, Day 2, Day 3" (sounds suspicious)
   - Now "Phase 1, Phase 2, Phase 3" (sounds professional)
   - Clear separation: Automated vs Human work
   - Flexible timelines: Evidence Sprint (48h), Starter (3-5 days), Professional (5-7 days)

4. ✅ **Kept approved sections:**
   - Honest limitations (what it's NOT)
   - Technical architecture (open source + proprietary)
   - Specific tech stack (versions, frameworks)
   - Pre-emptive FAQ
   - Simple pricing

---

## Implementation Next Steps

1. **Build OAuth flow:** "Link Your Repo" → GitHub OAuth → Read-only access
2. **Embed Scopelock graph:** Interactive demo on homepage (React Flow)
3. **Build Evidence Sprint workflow:** $350 payment → Extract 1 module → Deliver mini-graph
4. **Implement ROI calculator:** React component with user inputs
5. **Create FAQ page:** Expand beyond homepage FAQ

**Ready to implement?**
