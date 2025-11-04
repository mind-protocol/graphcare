# Documentation Website Architecture

**Site Pattern:** `docs.{client_name}.mindprotocol.ai`
**Example:** `docs.scopelock.mindprotocol.ai`
**Tech Stack:** Next.js 14 + Vercel + FalkorDB
**Prepared By:** Sage (Chief Documenter, GraphCare)
**Date:** 2025-11-04

---

## Overview

Each client gets a dedicated documentation website that provides:
- Interactive knowledge graph exploration
- Semantic search over extracted knowledge
- Auto-generated documentation (architecture, API, coverage)
- Human-written narratives (executive summary, onboarding)
- Real-time health dashboard
- Query examples and API playground

---

## Site Structure

```
docs.{client}.mindprotocol.ai/
├── /                          # Landing page (overview)
├── /graph                     # Interactive graph explorer
├── /search                    # Semantic search
├── /docs                      # Documentation index
│   ├── /architecture          # Architecture overview (Tier 1)
│   ├── /architecture-narrative # Architecture narrative (Tier 2)
│   ├── /api                   # API reference (Tier 1)
│   ├── /code                  # Code reference (Tier 1)
│   ├── /coverage              # Coverage report (Tier 1)
│   ├── /executive-summary     # Executive summary (Tier 2)
│   ├── /onboarding            # Onboarding guide (Tier 2)
│   └── /adr                   # ADR index (Tier 1)
├── /health                    # Health dashboard
├── /queries                   # Pre-built queries + playground
└── /about                     # About this graph
```

---

## Page Specifications

### 1. Landing Page (`/`)

**Purpose:** Entry point showcasing what's available

**Sections:**
1. **Hero**
   - Client name + tagline
   - System description (1-2 sentences)
   - Key metrics: {{node_count}} nodes, {{link_count}} links, {{coverage}}% coverage
   - Last extraction: {{extraction_date}}

2. **Quick Links**
   - "Explore the Graph" → `/graph`
   - "Search Knowledge" → `/search`
   - "View Documentation" → `/docs`
   - "Check Health" → `/health`

3. **Recent Updates**
   - Last 5 changes to graph
   - New docs added
   - Coverage improvements

4. **Popular Queries**
   - Top 5 most-run queries
   - One-click execution

**Tech:**
- Next.js page component
- Server-side rendering for SEO
- WebSocket subscription for real-time updates

---

### 2. Graph Explorer (`/graph`)

**Purpose:** Interactive visualization of knowledge graph

**Features:**

**A. Main Canvas**
- React Flow visualization
- Node rendering by type (different colors/shapes)
- Edge rendering by relationship type
- Zoom/pan controls
- Minimap for navigation

**B. Node Inspector (Side Panel)**
When node clicked:
- Node type and ID
- All attributes (description, metadata, timestamps)
- Outgoing links (with targets)
- Incoming links (with sources)
- Related nodes (1-hop neighbors)
- "Jump to" button (navigate to that node)
- "View in docs" button (if has documentation page)

**C. Filters**
- Filter by node type (checkboxes)
- Filter by link type (checkboxes)
- Filter by confidence score (slider)
- Filter by time range (date picker)
- "Reset filters" button

**D. Layout Options**
- Force-directed (default)
- Hierarchical (top-down)
- Circular
- Grid
- Custom (manual positioning)

**E. Search Bar**
- Autocomplete node names
- Jump to node on selection
- Highlight matching nodes

**F. Export**
- Export as PNG (current view)
- Export as SVG (current view)
- Export as JSON (full graph)

**Tech:**
- React Flow (graph visualization library)
- Cypher query to fetch subgraph
- WebSocket for real-time updates
- Canvas rendering for performance

**Graph Query (Initial Load):**
```cypher
MATCH (n)
WHERE n.scope_ref = $client_id
AND n.level = 'L2'
OPTIONAL MATCH (n)-[r]->(m)
RETURN n, r, m
LIMIT 500
```

---

### 3. Semantic Search (`/search`)

**Purpose:** Natural language search over knowledge graph

**Features:**

**A. Search Bar**
- Large, prominent search input
- Placeholder examples: "find retry mechanisms", "show payment workflows"
- Search button + enter-to-search
- Voice input (optional, future)

**B. Search Results**
- Ranked by relevance (embedding similarity)
- Each result shows:
  - Node type icon
  - Node name
  - Description snippet (with query terms highlighted)
  - Confidence score
  - "View details" button → opens node inspector
  - "View in graph" button → jumps to node in graph explorer

**C. Filters (Sidebar)**
- Filter by node type
- Filter by confidence
- Filter by date range
- Sort by: relevance, date, confidence

**D. Query History**
- Last 10 searches (saved in localStorage)
- One-click to re-run

**E. Suggested Searches**
- "People who searched X also searched Y"
- Categorized suggestions:
  - Architecture queries
  - Code queries
  - Testing queries
  - Security queries

**Tech:**
- SentenceTransformers embedding service (backend)
- Cosine similarity search in FalkorDB
- Debounced search (wait for user to stop typing)
- Paginated results (20 per page)

**Search Query:**
```cypher
CALL db.idx.vector.queryNodes(
  'node_embedding_index',
  10,
  $query_embedding
) YIELD node, score
WHERE node.scope_ref = $client_id
RETURN node, score
ORDER BY score DESC
```

---

### 4. Documentation Index (`/docs`)

**Purpose:** Hub for all documentation

**Layout:**

**Three-Column Layout:**

**Left Sidebar:** Navigation
- Executive Summary
- Architecture Overview (Tier 1)
- Architecture Narrative (Tier 2)
- API Reference (Tier 1)
- Code Reference (Tier 1)
- Coverage Report (Tier 1)
- Onboarding Guide (Tier 2)
- ADR Index (Tier 1)
- Health Dashboard

**Center:** Document content
- Markdown rendering
- Syntax highlighting for code blocks
- Mermaid diagram rendering
- Interactive examples (if applicable)
- Table of contents (right sidebar, auto-generated from headings)

**Right Sidebar:** Context
- Related nodes in graph
- Related documents
- Quick links
- Edit history (who wrote, when updated)

**Tech:**
- Next.js MDX for markdown rendering
- Prism.js for syntax highlighting
- Mermaid.js for diagram rendering
- Auto-generated navigation from template structure

---

### 5. Architecture Overview (`/docs/architecture`)

**Content:** Tier 1 auto-generated architecture documentation

**Source:** `/graphcare/templates/tier1_architecture_overview.md` populated from graph

**Features:**
- Mermaid diagrams (architecture, dependencies)
- Expandable component details
- Links to code files (opens in Code Reference)
- Links to related nodes in graph

---

### 6. Architecture Narrative (`/docs/architecture-narrative`)

**Content:** Tier 2 human-written architecture story

**Source:** `/graphcare/templates/tier2_architecture_narrative.md` written by Sage + Nora

**Features:**
- Rich narrative with analogies and explanations
- Embedded diagrams
- Code examples with explanations
- Decision rationale
- Evolution timeline

---

### 7. API Reference (`/docs/api`)

**Content:** Tier 1 auto-generated API documentation

**Source:** `/graphcare/templates/tier1_api_reference.md` populated from GC_API_Endpoint nodes

**Features:**
- Filterable/searchable endpoint list
- Interactive API playground (try requests in-browser)
- Request/response examples
- Error code documentation
- Authentication requirements
- Rate limiting info

**Tech:**
- Swagger UI (if OpenAPI spec exists) OR custom React components
- Monaco editor for request body editing
- Axios for making requests

---

### 8. Code Reference (`/docs/code`)

**Content:** Tier 1 auto-generated code documentation

**Source:** `/graphcare/templates/tier1_code_reference.md` populated from GC_Function/GC_Class nodes

**Features:**
- Searchable function/class index
- Syntax-highlighted code snippets
- Call graph visualization (who calls this?)
- Dependency graph (what does this call?)
- Coverage indicator (tested/untested)
- Jump to source (if repo is public)

---

### 9. Coverage Report (`/docs/coverage`)

**Content:** Tier 1 auto-generated test coverage analysis

**Source:** `/graphcare/templates/tier1_coverage_report.md` populated from U4_Metric/U4_Measurement nodes

**Features:**
- Interactive coverage heatmap (by module/file)
- Filterable by component
- Trend chart (if historical data exists)
- Gap analysis (untested critical paths)
- Recommendations

**Tech:**
- Chart.js for trend charts
- D3.js for heatmap visualization

---

### 10. Executive Summary (`/docs/executive-summary`)

**Content:** Tier 2 human-written executive report

**Source:** `/graphcare/templates/tier2_executive_summary.md` written by Sage + Mel

**Features:**
- PDF export button
- Print-friendly CSS
- Email sharing
- Non-technical language
- Strategic recommendations

---

### 11. Onboarding Guide (`/docs/onboarding`)

**Content:** Tier 2 human-written developer onboarding

**Source:** `/graphcare/templates/tier2_onboarding_guide.md` written by Sage

**Features:**
- Step-by-step workflow
- Copy-paste code examples
- Verification checkboxes (interactive)
- Progress tracking (localStorage)
- Links to relevant code in graph

---

### 12. Health Dashboard (`/health`)

**Purpose:** Real-time graph health monitoring

**Features:**

**A. Overview Cards**
- Overall health status (GREEN/AMBER/RED)
- Key metrics: Coverage, Security, Drift, Freshness
- Last sync timestamp
- Next scheduled sync

**B. 10 Health Metrics (Adapted from Mind Protocol)**

| Metric | Description | Target | Current | Status |
|--------|-------------|--------|---------|--------|
| Coverage Ratio | % of codebase mapped | >85% | {{coverage}}% | {{status_emoji}} |
| Unmapped Code | Files not in graph | <10% | {{unmapped}}% | {{status_emoji}} |
| Cluster Quality | Semantic coherence | >0.7 | {{coherence}} | {{status_emoji}} |
| Cross-Reference Quality | Doc links | >80% | {{xref}}% | {{status_emoji}} |
| Query Performance | p90 latency | <500ms | {{p90}}ms | {{status_emoji}} |
| Update Rate | Days since last sync | <7 days | {{days}} days | {{status_emoji}} |
| Module Connectivity | Cross-module refs | >0.5 | {{connectivity}} | {{status_emoji}} |
| Active Patterns | Query result relevance | >0.8 | {{relevance}} | {{status_emoji}} |
| Pattern Scope | Avg pattern size | 5-15 nodes | {{size}} nodes | {{status_emoji}} |
| Pattern Reuse | Shared mechanisms | >30% | {{reuse}}% | {{status_emoji}} |

**C. Trend Charts**
- Coverage over time (last 30 days)
- Query performance over time
- Drift frequency over time
- Health score over time

**D. Alerts**
- RED metric alerts (critical issues)
- Drift detected (code changed since extraction)
- Security vulnerabilities detected
- Coverage dropped

**E. Recommendations**
- Top 3 actions to improve health
- Effort estimates
- Expected impact

**Tech:**
- WebSocket for real-time updates
- Chart.js for trend visualization
- Percentile-based judgment (GREEN/AMBER/RED from historical bands)
- Query health metrics from FalkorDB

**Health Query:**
```cypher
MATCH (metric:U4_Metric)
WHERE metric.scope_ref = $client_id
OPTIONAL MATCH (metric)-[:U4_MEASURED_BY]->(measurement:U4_Measurement)
RETURN metric, collect(measurement)
ORDER BY measurement.timestamp DESC
```

---

### 13. Query Playground (`/queries`)

**Purpose:** Pre-built queries + custom query execution

**Features:**

**A. Pre-Built Query Library**
- 30+ sample queries covering common use cases
- Categorized:
  - Architecture queries ("Show service dependencies")
  - Code queries ("Find all API endpoints")
  - Testing queries ("Show untested functions")
  - Security queries ("Find PII handling code")
  - Patterns ("Find retry mechanisms")

**B. Query Builder (Guided)**
- Select node type dropdown
- Select relationship type dropdown
- Add filters (property = value)
- Generate Cypher query
- Run query button

**C. Advanced Query (Cypher Editor)**
- Monaco editor with syntax highlighting
- Autocomplete for node types, link types, properties
- Query execution
- Results table (paginated)
- Export results as JSON/CSV

**D. Query History**
- Last 20 queries (saved per user)
- Star favorites
- Share query (generate URL)

**E. Query Results**
- Table view (default)
- Graph view (visualize results in mini-graph)
- JSON view (raw data)
- Export options

**Tech:**
- Monaco editor (VS Code editor component)
- Cypher.js for syntax highlighting
- FalkorDB query execution via API

---

### 14. About Page (`/about`)

**Purpose:** Meta-information about the graph

**Content:**
- What is this graph?
- How was it extracted?
- When was it last updated?
- What's included / excluded?
- How to use this site?
- Contact for questions

---

## Component Library

### Reusable Components

**1. NodeCard**
- Displays node summary
- Props: node (object)
- Shows: type icon, name, description, confidence
- Actions: View details, View in graph

**2. LinkBadge**
- Displays relationship type
- Props: link_type (string)
- Color-coded by semantic meaning

**3. ConfidenceIndicator**
- Shows confidence score (0-1)
- Props: confidence (float)
- Visual: ✅ High (≥0.9), 🟡 Medium (0.7-0.89), 🔴 Low (<0.7)

**4. HealthMetricCard**
- Shows single health metric
- Props: metric_name, current_value, target_value, status
- Visual: Status emoji, trend sparkline

**5. CodeBlock**
- Syntax-highlighted code
- Props: code (string), language (string)
- Features: Copy button, line numbers

**6. SearchBar**
- Reusable search input
- Props: onSearch (callback), placeholder (string)
- Features: Autocomplete, debouncing

**7. GraphViewer (Mini)**
- Embedded graph visualization
- Props: nodes (array), links (array)
- Smaller version of full graph explorer

---

## Tech Stack Details

### Frontend

**Framework:** Next.js 14 (App Router)
- Server-side rendering (SEO)
- Static generation for docs (performance)
- API routes for backend proxy

**UI Library:** React 18 + TypeScript

**Styling:** Tailwind CSS

**Components:**
- Headless UI (accessible components)
- Radix UI (advanced components)

**Graph Visualization:**
- React Flow (interactive graph)
- D3.js (heatmaps, custom visualizations)

**Charts:**
- Chart.js (trends, time series)

**Code/Editor:**
- Monaco Editor (Cypher query editor)
- Prism.js (syntax highlighting in docs)

**Markdown:**
- MDX (markdown with React components)
- Mermaid.js (diagram rendering)

---

### Backend

**API:** FastAPI (Python)

**Database:** FalkorDB (graph storage)

**Embedding Service:** SentenceTransformers (local)

**WebSocket:** FastAPI WebSocket endpoints

**Endpoints:**

```
GET  /api/graph/nodes                # Fetch nodes (filtered, paginated)
GET  /api/graph/nodes/:id            # Fetch single node
GET  /api/graph/subgraph             # Fetch subgraph (for visualization)
POST /api/search                     # Semantic search (embedding-based)
POST /api/query                      # Execute Cypher query
GET  /api/health                     # Health metrics
GET  /api/docs/:doc_type             # Fetch documentation (populated template)
WS   /ws/health                      # WebSocket for real-time health updates
WS   /ws/graph                       # WebSocket for real-time graph updates
```

---

### Deployment

**Frontend Hosting:** Vercel
- Multi-tenant (one deployment, subdomain routing)
- Environment variables for client-specific config
- Edge caching for docs (static)

**Backend Hosting:** Render (or similar)
- Docker container
- Python FastAPI app
- Connected to FalkorDB instance

**Database:** FalkorDB
- Shared instance, separate graphs per client
- Graph naming: `graphcare_{client_id}`
- Scoped queries via `scope_ref` property

**CDN:** Vercel Edge Network (automatic)

**SSL:** Automatic via Vercel

**DNS:**
- Wildcard DNS: `*.mindprotocol.ai` → Vercel
- Vercel handles subdomain routing

---

### Security & Access Control

**Authentication:**
- Client-specific credentials
- Basic Auth (MVP) → OAuth/SAML (future)
- JWT tokens for API requests

**Authorization:**
- Scope isolation via `scope_ref` property
- Client A cannot query Client B's graph
- Row-level security in FalkorDB

**Data Privacy:**
- Respect `visibility` property (public, partners, governance, private)
- Filter nodes based on user role
- Audit logging for all queries

---

## Responsive Design

**Breakpoints:**
- Mobile: <640px
- Tablet: 640-1024px
- Desktop: >1024px

**Mobile Adaptations:**
- Graph explorer: Touch controls, simplified UI
- Docs: Single-column layout
- Health dashboard: Stacked metric cards
- Search: Full-screen search interface

---

## Performance Considerations

**Graph Visualization:**
- Load max 500 nodes initially
- Lazy load additional nodes on zoom
- Web workers for layout computation
- Canvas rendering (not SVG) for large graphs

**Search:**
- Debounce search input (300ms)
- Cache recent searches
- Paginated results (20 per page)

**Documentation:**
- Static generation for Tier 1 docs (build time)
- Server-side rendering for Tier 2 docs (request time)
- Edge caching (Vercel)

**WebSocket:**
- Throttle health updates (max 1/second)
- Batch graph updates (max 10/second)

---

## Accessibility

**WCAG 2.1 AA Compliance:**
- Keyboard navigation (graph explorer, search)
- Screen reader support (ARIA labels)
- High contrast mode
- Focus indicators
- Alt text for diagrams

**Color Vision:**
- Don't rely on color alone (use icons + text)
- Colorblind-friendly palette

---

## Future Enhancements

**Phase 2:**
- AI chat interface (ask questions about the graph)
- Collaborative annotations (users can add notes to nodes)
- Version comparison (diff between graph versions)
- Advanced analytics (query patterns, usage metrics)

**Phase 3:**
- SSO integration (OAuth, SAML)
- Role-based access control (fine-grained permissions)
- Custom branding (client logos, color schemes)
- Embeddable widgets (embed graph in client's own docs)

---

## Directory Structure (Implementation)

```
/graphcare/
├── /app/                      # Next.js app
│   ├── /client-docs/          # Client documentation site
│   │   ├── /[client]/         # Dynamic client routing
│   │   │   ├── /page.tsx      # Landing page
│   │   │   ├── /graph/        # Graph explorer page
│   │   │   ├── /search/       # Search page
│   │   │   ├── /docs/         # Documentation pages
│   │   │   ├── /health/       # Health dashboard
│   │   │   └── /queries/      # Query playground
│   │   └── /components/       # Shared components
│   │       ├── NodeCard.tsx
│   │       ├── GraphViewer.tsx
│   │       ├── SearchBar.tsx
│   │       └── ...
│   └── /api/                  # API routes (proxies to backend)
│       ├── /graph/
│       ├── /search/
│       └── /health/
├── /services/                 # Backend services
│   ├── /api/                  # FastAPI app
│   │   ├── main.py
│   │   ├── /routers/
│   │   │   ├── graph.py
│   │   │   ├── search.py
│   │   │   └── health.py
│   │   └── /models/
│   ├── /embedding/            # Embedding service
│   └── /health_monitoring/    # Health metrics computation
└── /templates/                # Documentation templates
    ├── tier1_*.md
    └── tier2_*.md
```

---

**Architect:** Sage (Chief Documenter, GraphCare)
**Last Updated:** 2025-11-04
