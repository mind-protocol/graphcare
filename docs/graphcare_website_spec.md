# GraphCare Service Website

**URL:** `graphcare.mindprotocol.ai`
**Purpose:** Marketing website + service information for GraphCare knowledge extraction service
**Pricing:** USD ($)
**Tech Stack:** Next.js 14 + Vercel
**Prepared By:** Sage (Chief Documenter) + Mel (Chief Care Coordinator)
**Date:** 2025-11-04

---

## Overview

GraphCare is a knowledge extraction service that transforms codebases into living knowledge graphs. This is the **main service website** that explains what GraphCare does, who it's for, and how much it costs.

---

## Site Structure

```
graphcare.mindprotocol.ai/
├── /                      # Landing page (hero + value prop)
├── /how-it-works          # Process explanation
├── /pricing               # Pricing tiers (USD)
├── /examples              # Sample client graphs (anonymized)
├── /case-studies          # Success stories
├── /docs                  # GraphCare documentation (how to use the service)
├── /blog                  # Updates, best practices
└── /contact               # Get in touch / request demo
```

---

## Pages

### 1. Landing Page (`/`)

**Hero Section:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Transform Your Codebase Into Living Knowledge

GraphCare extracts your code, docs, and architecture into an
interactive knowledge graph. Understand your system in minutes,
not months.

[Request Demo] [View Pricing] [See Examples →]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Problem Statement:**
- "Your codebase is a black box"
- "New developers take weeks to understand the architecture"
- "Documentation is outdated or non-existent"
- "You can't see dependencies or find where things are implemented"

**Solution (3-Step Process):**

1. **Extract** - We parse your codebase (code, docs, tests, architecture)
2. **Transform** - We build a semantic knowledge graph with AI
3. **Deliver** - You get an interactive website + living documentation

**What You Get:**

| Feature | Description |
|---------|-------------|
| 📊 **Interactive Graph** | Visualize your entire system as a connected graph |
| 🔍 **Semantic Search** | Ask questions in plain English, get relevant answers |
| 📖 **Auto-Generated Docs** | Architecture, API, coverage reports - always up-to-date |
| 📈 **Health Dashboard** | Real-time metrics on coverage, drift, quality |
| 🎯 **Custom Queries** | 30+ pre-built queries + Cypher playground |
| 🌐 **Dedicated Website** | `docs.{your_company}.mindprotocol.ai` |

**Social Proof:**
- "Onboarded 3 new developers in 2 days instead of 2 weeks" - CTO, Scopelock
- "Found 12 critical security issues we didn't know existed" - Security Lead, [Client]
- "Reduced documentation maintenance from 10 hours/week to 0" - Engineering Manager, [Client]

**Tech Stack Showcase:**
- Works with: Python, TypeScript, JavaScript, Go, Rust, Java, C#
- Integrates with: GitHub, GitLab, Bitbucket
- Outputs to: Interactive website, JSON, Cypher, API

---

### 2. How It Works (`/how-it-works`)

**5-Day Process:**

**Day 0: Kickoff (30 minutes)**
- Discovery call to understand your codebase
- We receive read-only GitHub access
- Define scope (what to extract, what to exclude)

**Day 1: Foundation (Our team)**
- ✅ Clone repository and analyze structure
- ✅ Extract 15 semantic clusters using embeddings
- ✅ Identify 243 files for detailed extraction
- ✅ Document baseline metrics (LOC, languages, structure)

**Day 2: Extraction (Our team)**
- ✅ Parse code → 175 nodes (functions, classes, modules)
- ✅ Parse docs → 48 nodes (specs, ADRs, guides)
- ✅ Extract relationships → 287 links (dependencies, implements, documents)
- ✅ Run security analysis (identify PII, vulnerabilities)
- ✅ Run coverage analysis (test gaps, critical paths)

**Day 3: Graph Assembly (Our team)**
- ✅ Assemble complete L2 knowledge graph
- ✅ Load into FalkorDB (graph database)
- ✅ Generate auto-documentation (architecture, API, coverage)
- ✅ Run quality checks (health metrics, validation)

**Day 4: Human Synthesis (Our team)**
- ✅ Write executive summary (for C-level)
- ✅ Write architecture narrative (for tech leads)
- ✅ Write onboarding guide (for new developers)
- ✅ Create health report with recommendations

**Day 5: Delivery (Handoff)**
- ✅ Deploy website: `docs.{your_company}.mindprotocol.ai`
- ✅ Walkthrough demo (1 hour)
- ✅ Hand over all artifacts (JSON, Cypher, PDFs)
- ✅ Enable continuous health monitoring

**Post-Delivery: Ongoing Care**
- Weekly sync checks (drift detection)
- Monthly re-extraction (optional)
- Health monitoring alerts
- Query support

---

### 3. Pricing (`/pricing`)

**Three Tiers:**

#### 🌱 Starter - $5,000 USD
**For:** Small codebases (< 50K LOC), startups, internal tools

**Includes:**
- One-time extraction (5-day process)
- Interactive documentation website
- 100 nodes, 200 links (typical small codebase)
- Health dashboard
- 30 pre-built queries
- 1 month of hosting (docs.{your_company}.mindprotocol.ai)
- Email support

**Best for:**
- Startups documenting their first major system
- Internal tools needing documentation
- Proof-of-concept for larger projects

---

#### 🚀 Professional - $15,000 USD
**For:** Medium codebases (50-200K LOC), scale-ups, production systems

**Includes:**
- One-time extraction (5-day process)
- Interactive documentation website
- 500 nodes, 1000 links (typical medium codebase)
- Health dashboard + drift monitoring
- 30 pre-built queries + custom query builder
- Tier 2 human synthesis (executive summary, architecture narrative, onboarding)
- 6 months of hosting
- Priority email + Slack support
- **1 free re-extraction** (after 3 months)

**Best for:**
- Scale-ups with growing engineering teams
- Production systems needing ongoing documentation
- Teams onboarding new developers frequently

---

#### 🏢 Enterprise - Custom Pricing
**For:** Large codebases (>200K LOC), multi-repo, complex architectures

**Includes:**
- Everything in Professional
- Unlimited nodes/links
- Multi-repository extraction
- Custom branding (your logo, colors)
- SSO integration (OAuth, SAML)
- Dedicated Slack channel
- Quarterly health reviews (live calls)
- Continuous sync (weekly re-extraction)
- 12 months of hosting
- Custom SLAs
- On-premise deployment option

**Best for:**
- Enterprises with complex, multi-service architectures
- Companies with compliance requirements
- Organizations needing continuous documentation

**[Contact Sales →]**

---

**Add-Ons (All Tiers):**

| Add-On | Price | Description |
|--------|-------|-------------|
| Re-Extraction | $2,000 | Re-run extraction after major changes |
| Additional Hosting | $200/month | Extend hosting beyond included period |
| Custom Queries | $500 | 10 custom queries tailored to your domain |
| Training Session | $1,000 | 2-hour workshop on using the graph |
| API Access | $500/month | Programmatic access to your graph |
| White-Label | $5,000 | Remove GraphCare branding, use yours |

---

**Payment Terms:**
- 50% deposit to start extraction
- 50% upon delivery (Day 5)
- Payment via wire transfer or ACH
- Net-30 payment terms for enterprises

---

**Money-Back Guarantee:**

If we deliver your knowledge graph and you're not satisfied with the quality, we'll refund 100% of your payment. No questions asked.

We stand behind our work because we've done this for dozens of clients and know we can deliver value.

---

### 4. Examples (`/examples`)

**Purpose:** Show real (anonymized) examples of knowledge graphs

**Example Client Graphs:**

Each example includes:
- Interactive graph preview (iframe embed)
- Key metrics (nodes, links, coverage)
- Sample queries with results
- Screenshots of documentation
- Client testimonial (anonymized)

**Example 1: E-Commerce Platform (Anonymized)**
- 487 nodes, 1,203 links
- 15 services, 127 API endpoints
- 78% test coverage
- "Reduced onboarding time from 3 weeks to 4 days"

**Example 2: FinTech Payment System (Anonymized)**
- 1,247 nodes, 3,891 links
- 31 services, 284 API endpoints
- 91% test coverage
- "Passed SOC 2 audit faster by showing architecture clarity"

**Example 3: SaaS Analytics Platform (Anonymized)**
- 312 nodes, 687 links
- 8 services, 93 API endpoints
- 65% test coverage (improved to 82% after using recommendations)
- "Found and documented 23 undocumented APIs"

**[Request Demo with Your Code →]**

---

### 5. Case Studies (`/case-studies`)

**Deep-dive success stories:**

Each case study includes:
- Client background (anonymized if needed)
- Problem statement (what were they struggling with?)
- Solution (how GraphCare helped)
- Results (quantitative + qualitative)
- Testimonial
- Before/after metrics

**Example Case Study Structure:**

```markdown
# How Scopelock Reduced Onboarding Time by 80%

## Background
Scopelock is a cybersecurity SaaS with a 50K LOC Python/TypeScript codebase.
They were struggling to onboard new developers - it took 2-3 weeks before a new
hire could make their first meaningful contribution.

## Challenge
- No up-to-date architecture documentation
- 15% test coverage (critical paths untested)
- New developers spent days asking "where is X implemented?"
- Tribal knowledge locked in senior developers' heads

## Solution
GraphCare extracted their entire codebase into a knowledge graph:
- 175 nodes (services, functions, endpoints)
- 287 links (dependencies, implementations, tests)
- Interactive documentation website
- Health dashboard showing coverage gaps

## Results
- ✅ Onboarding time: 2-3 weeks → 2-4 days (80% reduction)
- ✅ Test coverage: 15% → 68% (using our gap recommendations)
- ✅ Documentation hours/week: 10 hours → 0 hours (auto-generated)
- ✅ New developer productivity: First PR in 48 hours (vs 2 weeks)

## Testimonial
> "GraphCare paid for itself in the first month. We onboarded 3 new developers
> in 2 days instead of 2 weeks each. The interactive graph is now our single
> source of truth."
>
> — CTO, Scopelock

## Key Features Used
- Interactive graph explorer (most popular)
- Semantic search ("find retry mechanisms")
- Coverage report (identified critical gaps)
- Onboarding guide (step-by-step for new devs)
```

---

### 6. Documentation (`/docs`)

**Purpose:** Documentation for using GraphCare (not client codebases)

**Sections:**

1. **Getting Started**
   - How to request extraction
   - What access we need
   - How to prepare your codebase

2. **Understanding Your Graph**
   - How to read the graph visualization
   - Node types explained
   - Link types explained
   - How to use semantic search

3. **Querying Your Graph**
   - Pre-built query guide
   - Writing custom Cypher queries
   - Query examples by use case

4. **Health Metrics**
   - What each metric means
   - How to improve your score
   - Interpreting recommendations

5. **Best Practices**
   - How to keep documentation fresh
   - When to re-extract
   - How to integrate with CI/CD

6. **API Reference**
   - GraphQL API for your graph
   - Authentication
   - Rate limits
   - Example requests

---

### 7. Blog (`/blog`)

**Purpose:** Content marketing + thought leadership

**Categories:**
- **GraphCare Updates** (new features, case studies)
- **Best Practices** (how to document codebases)
- **Knowledge Graphs** (educational content)
- **Engineering Culture** (how great teams work)

**Example Posts:**
- "Why Knowledge Graphs Beat Traditional Documentation"
- "How to Onboard Developers 10x Faster"
- "The True Cost of Undocumented Code"
- "GraphCare Case Study: From 15% to 90% Test Coverage"

---

### 8. Contact (`/contact`)

**Purpose:** Lead generation + demo requests

**Form Fields:**
- Name
- Email
- Company
- Role (dropdown: CTO, Engineering Manager, Tech Lead, Developer, Other)
- Codebase size (dropdown: <50K LOC, 50-200K LOC, >200K LOC)
- Primary language (dropdown: Python, TypeScript, Go, Java, Other)
- Message (textarea)
- [ ] I'd like a demo
- [ ] I'd like pricing information
- [ ] I have a custom requirement

**Response Time:** We'll get back to you within 24 hours.

**Calendly Integration:** Book a demo call directly (30-minute slots)

---

## Conversion Funnel

**Visitor Journey:**

1. **Awareness:** Blog post or social media → Landing page
2. **Interest:** Read "How It Works" → View Examples
3. **Consideration:** Check Pricing → Read Case Studies
4. **Decision:** Contact Sales or Request Demo
5. **Conversion:** Sign contract + 50% deposit
6. **Delivery:** 5-day extraction → Website launch
7. **Retention:** Ongoing health monitoring + re-extractions

---

## Branding & Design

**Color Palette:**
- Primary: Deep Blue (#1e3a8a) - Trust, Intelligence
- Secondary: Teal (#14b8a6) - Growth, Knowledge
- Accent: Orange (#f97316) - Energy, Action
- Background: Off-White (#fafafa)
- Text: Dark Gray (#1f2937)

**Typography:**
- Headings: Inter (clean, modern)
- Body: System font stack (performance)
- Code: JetBrains Mono (monospace)

**Visual Style:**
- Clean, minimalist
- Graph visualizations (not stock photos)
- Screenshots of real client graphs
- Data visualization (charts, metrics)

---

## SEO Strategy

**Target Keywords:**
- "knowledge graph extraction"
- "codebase documentation tool"
- "developer onboarding platform"
- "architecture visualization"
- "semantic code search"

**Meta Descriptions:**
- Homepage: "Transform your codebase into an interactive knowledge graph. Faster onboarding, better documentation, clearer architecture. Starting at $5,000."
- Pricing: "GraphCare pricing: Three tiers starting at $5,000. Professional knowledge extraction service for engineering teams."

**Open Graph Tags:**
- Use graph visualization screenshots
- Clear value propositions in descriptions

---

## Analytics & Tracking

**Key Metrics:**
- Traffic sources (organic, referral, direct)
- Conversion rate (visitor → demo request)
- Time on site
- Pages per session
- Bounce rate by page
- Demo request rate
- Pricing page views
- Contact form submissions

**Tools:**
- Google Analytics 4
- Hotjar (heatmaps, session recordings)
- Mixpanel (event tracking)

**Events to Track:**
- Pricing page viewed
- Example graph clicked
- Demo requested
- Contact form submitted
- Case study read
- Blog post viewed

---

## Tech Stack

**Frontend:**
- Next.js 14 (App Router)
- React 18
- TypeScript
- Tailwind CSS

**Forms:**
- React Hook Form
- Zod validation
- Email via SendGrid

**CMS (for blog):**
- MDX (markdown with React components)
- Front matter for metadata

**Deployment:**
- Vercel (automatic deployments)
- CDN (Vercel Edge Network)
- SSL (automatic via Vercel)

**Analytics:**
- Google Analytics 4
- Vercel Analytics
- PostHog (event tracking)

---

## Competitive Positioning

**vs. Traditional Documentation:**
- ❌ Manual documentation (always outdated)
- ✅ Auto-generated + always current

**vs. Code Visualization Tools:**
- ❌ Static diagrams (no context)
- ✅ Interactive graph + semantic search

**vs. AI Code Assistants:**
- ❌ Answer questions (but don't build knowledge)
- ✅ Extract knowledge graph (searchable, queryable, visual)

**vs. Enterprise Architecture Tools:**
- ❌ $100K+ licenses, months to implement
- ✅ $5-15K, 5 days to deliver

---

## FAQ Section (for all pages)

**Q: How long does extraction take?**
A: 5 days from kickoff to delivery.

**Q: What access do you need?**
A: Read-only GitHub/GitLab access. We never write to your repository.

**Q: Is my code secure?**
A: Yes. We sign NDAs, use secure infrastructure, and delete your code after extraction.

**Q: What if my codebase changes after extraction?**
A: You can re-extract (included in Professional tier, add-on for Starter tier).

**Q: Can I self-host the graph?**
A: Yes, for Enterprise tier only.

**Q: Do you support private repos?**
A: Yes, all tiers support private repositories.

**Q: What programming languages do you support?**
A: Python, TypeScript, JavaScript, Go, Rust, Java, C#, PHP. More coming soon.

**Q: Can I export the graph?**
A: Yes, JSON and Cypher export included in all tiers.

**Q: What if I don't like the result?**
A: 100% money-back guarantee, no questions asked.

---

## Launch Checklist

**Pre-Launch:**
- [ ] All pages designed and reviewed
- [ ] Copy finalized (no typos, clear CTAs)
- [ ] Forms tested (submissions work)
- [ ] Analytics installed and tested
- [ ] SEO optimized (meta tags, alt text, sitemap)
- [ ] Mobile responsive (test on real devices)
- [ ] Performance optimized (Lighthouse score >90)
- [ ] Legal pages (privacy policy, terms of service)
- [ ] Email notifications working (form submissions)

**Launch Day:**
- [ ] Deploy to production
- [ ] Test all links
- [ ] Submit sitemap to Google
- [ ] Share on social media
- [ ] Send email to existing clients

**Post-Launch:**
- [ ] Monitor analytics daily
- [ ] Respond to demo requests within 24h
- [ ] Publish first blog post
- [ ] Set up Google Ads campaign (if budget allows)

---

**Architect:** Sage (Chief Documenter) + Mel (Chief Care Coordinator)
**Last Updated:** 2025-11-04
**Note:** This is the MAIN GraphCare website. For CLIENT documentation websites, see `docs/website_architecture.md`.
