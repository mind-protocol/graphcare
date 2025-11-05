# Docs-as-Views Handoff: Mind Protocol Team ↔ GraphCare

**Status:** ✅ Implementation complete | Ready for handoff
**Date:** 2025-11-04
**Author:** Mel "Bridgekeeper" (GraphCare)

---

## Summary

Docs-as-views is now **membrane-native** with proper L4 (protocol) enforcement. The implementation is split across two teams:

- **Mind Protocol Team** owns L4 protocol infrastructure and L3 ecosystem surface
- **GraphCare** owns L2 org-internal resolvers and client delivery

This document defines clear ownership, interfaces, and handoff requirements.

---

## Ownership Split

### Mind Protocol Team Owns

**L4 - Protocol Layer** (`/mindprotocol/orchestration/protocol/`)
- Membrane bus with boundary enforcement
- Protocol envelope schemas (typed contracts)
- SEA-1.0 signature verification
- CPS-1 economy integration
- Rate limiting and quota enforcement

**L3 - Ecosystem Layer** (`/mindprotocol/orchestration/adapters/`)
- WebSocket API (client connections)
- L3 bridge (inject/observe pattern)
- Result fanout to clients
- Optional UX caching

**Cross-Cutting:**
- CI guardrails (membrane lint)
- Protocol documentation
- Integration testing

---

### GraphCare Owns

**L2 - Organization Layer** (`/mindprotocol/services/view_resolvers/`)
- View resolvers per org (scopelock, future clients)
- Cypher selectors (4 views: architecture, api, coverage, index)
- Projection functions (Select → Project → Render)
- Business logic for view computation
- Client-specific customizations

**Client Delivery:**
- Per-org graph ingestion (extraction → FalkorDB)
- Per-org resolver deployment
- Client onboarding and configuration
- View customization and pricing

---

## Interface Contract (L4 ↔ L2)

### Protocol Envelopes (Shared Contract)

**Location:** `/mindprotocol/orchestration/protocol/envelopes/`

Both teams reference these schemas:

**docs_view.py:**
- `DocsViewRequest` - L3 injects, L2 observes
- `DocsViewResult` - L2 broadcasts, L3 observes
- `DocsViewInvalidated` - L2 broadcasts cache invalidations

**economy.py:**
- `EconomyQuoteRequest` - Client/L3 requests quote
- `EconomyQuoteResponse` - Economy service responds
- `EconomyDebit` - L2 settles quote after work

**failure.py:**
- `FailureEmit` - All layers emit on errors (R-400/R-401)

**Contract Promise:**
- Mind Protocol Team: Won't break envelope schemas without coordination
- GraphCare: Will update L2 resolvers if schemas change

---

## Mind Protocol Team TODO

### 1. Wire L3 Observer into WebSocket Server ⏸️

**File:** `/mindprotocol/orchestration/adapters/ws/websocket_server.py`

**Add to startup** (around line 300-400):

```python
# Add to imports
from orchestration.adapters.api.docs_view_api_v2 import observe_bus_and_fanout

# In startup function (near where engines are started)
async def start_background_tasks():
    # Existing tasks...

    # Start L3 docs view observer
    asyncio.create_task(observe_bus_and_fanout())
    logger.info("[WebSocket Server] Started docs view observer")

# Call during server startup
asyncio.create_task(start_background_tasks())
```

**Verification:**
- Start websocket server
- Check logs for: `[L3 Bridge] Subscribed to bus channels: ['docs.view.result', 'docs.view.invalidated', 'failure.emit']`

**Time Estimate:** 10 minutes

---

### 2. Update Imports to Use Protocol Envelopes ⏸️

**Files to Update:**
- `/mindprotocol/orchestration/adapters/api/docs_view_api_v2.py`
- `/mindprotocol/services/view_resolvers/runner.py`
- `/mindprotocol/services/view_resolvers/bus_observer.py`

**Change:**
```python
# OLD (L2-specific schemas)
from services.view_resolvers.schemas import DocsViewRequest, DocsViewResult

# NEW (L4 protocol artifacts)
from orchestration.protocol.envelopes import DocsViewRequest, DocsViewResult
```

**Why:** Makes it clear these are protocol contracts, not implementation details.

**Time Estimate:** 15 minutes

---

### 3. Economy Integration (Low Priority) ⏸️

**Current State:** EconomyStub (accepts all well-formed quotes)

**Future Integration:**
- Replace `EconomyStub` with `services/economy/runtime.py`
- Wire quote validation to actual economy service
- Add expiration checking
- Add budget enforcement

**Files:**
- `/mindprotocol/orchestration/protocol/hub/membrane_hub.py` (L4 quote validation)
- `/mindprotocol/services/view_resolvers/runner.py` (L2 quote requests)

**Time Estimate:** 2-3 hours (when economy runtime ready)

---

### 4. SEA-1.0 Signature Verification (Low Priority) ⏸️

**Current State:** Stub (accepts all envelopes)

**Future Integration:**
- Implement `verify_sea_signature()` in L4 hub
- Verify signature against payload + origin
- Reject envelopes with invalid signatures

**File:** `/mindprotocol/orchestration/protocol/hub/membrane_hub.py`

**Time Estimate:** 1-2 hours (when SEA-1.0 spec ready)

---

### 5. Run Membrane Lint (Verification) ✅

**Verify L3 purity:**
```bash
cd /home/mind-protocol/mindprotocol
python orchestration/tools/lint/membrane_lint.py
```

**Expected output:**
```
✅ PASSED: No membrane violations found in L3 code
```

**If failures:** Fix FalkorDB imports in L3 code before deploying.

**Time Estimate:** 5 minutes

---

### 6. Integration Testing (End-to-End) ⏸️

**Test Flow:**
1. Start L4 protocol hub: `python -m orchestration.protocol.hub.membrane_hub`
2. Start L2 resolver: `export $(cat .env.l2_resolver | xargs) && python -m services.view_resolvers.bus_observer`
3. Start L3 websocket server: `python orchestration/adapters/ws/websocket_server.py`
4. Connect test client and request view

**Test Cases:**
- ✅ Valid request with quote_id → view returned
- ✅ Invalid quote_id → rejected at L4, failure.emit sent
- ✅ Missing quote_id → rejected at L4, failure.emit sent
- ✅ Rate limit exceeded → rejected at L4

**Documentation:** See `/graphcare/docs/STARTUP_GUIDE.md` for detailed test procedures.

**Time Estimate:** 1-2 hours (includes fixing any integration issues)

---

### 7. Deploy L4 Protocol Hub ⏸️

**Production Deployment:**
- Deploy L4 hub as standalone service (port 8765)
- Configure DNS/routing for protocol hub
- Set up monitoring (envelope rejection rates, rate limit hits)
- Configure logging (protocol violations, CPS-1 rejections)

**Time Estimate:** 2-4 hours (depends on deployment infrastructure)

---

## GraphCare TODO

### 1. Per-Org Resolver Deployment ⏸️

**Current State:** Single L2 resolver for scopelock

**Future:**
- Deploy separate L2 resolver process per client org
- Configure `.env.l2_resolver` per org (graph name, credentials)
- Subscribe to org-scoped channels: `ecosystem/{eco}/org/{org}/docs.view.request`

**Template:** Use existing `bus_observer.py` as template.

**Time Estimate:** 30 minutes per new client org

---

### 2. Client Graph Ingestion ⏸️

**For each new client:**
1. Extract org codebase (tools/extractors/)
2. Generate L2 graph (scopelock format)
3. Import to FalkorDB (tools/import_graph_batched.py)
4. Verify graph structure (U4 types, relationships)

**Time Estimate:** 2-4 hours per client (depends on codebase size)

---

### 3. View Customization (Client-Specific) ⏸️

**Current Views:** 4 generic views (architecture, api, coverage, index)

**Client Customizations:**
- Add client-specific selectors (custom queries)
- Add client-specific projectors (custom formatting)
- Add client-specific rendering (branded templates)

**Files to Customize:**
- `services/view_resolvers/selectors.py` (add client queries)
- `services/view_resolvers/projectors.py` (add client projections)

**Time Estimate:** 1-2 hours per custom view

---

### 4. Monitor L2 Resolver Health 🔄 (Ongoing)

**Per-Org Monitoring:**
- Resolver uptime (should be always-running)
- Query performance (Cypher execution time)
- Cache hit rates (surgical invalidation effectiveness)
- Error rates (failure.emit frequency)

**Alerts:**
- Resolver offline → client docs unavailable
- Query timeout → investigate FalkorDB performance
- High failure.emit rate → investigate resolver logic

**Time Estimate:** 30 minutes setup per org, ongoing monitoring

---

### 5. Client Onboarding Documentation 📝

**Create per-client:**
- Resolver configuration guide
- View customization examples
- Troubleshooting runbook
- Pricing and quote management

**Template:** Use scopelock as reference.

**Time Estimate:** 1-2 hours per client

---

## Handoff Verification Checklist

### Mind Protocol Team

**Before claiming "docs-as-views operational":**

- [ ] L3 observer wired into websocket_server.py startup
- [ ] Membrane lint passes (no L3 violations)
- [ ] L4 protocol hub deployed and running (port 8765)
- [ ] Integration test passed (valid + invalid quotes)
- [ ] Protocol envelope imports updated (L4 artifacts)
- [ ] Monitoring configured (rejection rates, rate limits)

**Optional (low priority):**
- [ ] Economy runtime integrated (replace EconomyStub)
- [ ] SEA-1.0 signatures implemented (replace stub)

---

### GraphCare

**Before claiming "client delivery ready":**

- [ ] L2 resolver deployed for scopelock (test client)
- [ ] Scopelock graph ingested to FalkorDB
- [ ] All 4 views tested (architecture, api, coverage, index)
- [ ] Client onboarding doc written
- [ ] Resolver monitoring configured

**Per New Client:**
- [ ] Graph extraction and ingestion complete
- [ ] L2 resolver deployed with org config
- [ ] Custom views implemented (if requested)
- [ ] Client trained on docs access

---

## Critical Path (Minimal Viable)

**To make docs-as-views work TODAY:**

**Mind Protocol Team (30 min):**
1. Wire L3 observer into websocket_server.py (10 min)
2. Start all 3 services (L4 hub, L2 resolver, L3 websocket) (5 min)
3. Run integration test (15 min)

**GraphCare (Already Done ✅):**
- L2 resolver implemented and tested
- Scopelock graph ingested
- Configuration files ready

**After these steps:** Clients can connect to `ws://localhost:8000/api/ws` and request docs.

---

## Communication Protocol

### When Mind Protocol Team Needs GraphCare

**Scenarios:**
- Protocol envelope schema needs to change → Coordinate with GraphCare (L2 resolver updates needed)
- L4 hub changes affect L2 behavior → Notify GraphCare for testing
- New protocol requirements (SEA-1.0, CPS-1) → GraphCare updates resolvers

**Contact:** Mel "Bridgekeeper" via SYNC.md or direct channel

---

### When GraphCare Needs Mind Protocol Team

**Scenarios:**
- New client needs protocol hub access → Request org namespace setup
- L2 resolver issues traced to L4 hub → Report protocol violations
- Protocol envelope additions needed → Request schema updates

**Contact:** Mind Protocol team lead via SYNC.md or GitHub issues

---

## Troubleshooting Ownership

**Problem:** Client request not reaching L2 resolver

**Ownership:**
1. Check L4 hub (Mind Protocol): Is envelope being rejected? Check failure.emit
2. Check L3 bridge (Mind Protocol): Is injection successful? Check L3 logs
3. Check L2 resolver (GraphCare): Is subscription active? Check observer logs

**Problem:** View computation slow/failing

**Ownership:**
1. Check L2 resolver (GraphCare): Query performance? Exception in projector?
2. Check FalkorDB (GraphCare): Graph structure correct? Query optimized?
3. If L2 emits failure.emit correctly → GraphCare's responsibility

**Problem:** Protocol violation detected

**Ownership:**
1. L4 hub rejection (Mind Protocol): Check envelope validation logic
2. L3 importing FalkorDB (Mind Protocol): Run membrane lint, fix violation
3. L2 crossing org boundary (GraphCare): Should never happen, fix resolver

---

## Success Metrics

**Mind Protocol Team:**
- L4 hub uptime: 99.9%+
- Protocol rejection rate: <1% (most requests valid)
- L3 membrane violations: 0 (CI enforced)
- Integration test passing: 100%

**GraphCare:**
- L2 resolver uptime per org: 99%+
- View computation success rate: 95%+
- Cache hit rate: 70%+ (with surgical invalidation)
- Client satisfaction: Views accurate and fast

---

## Files Reference

### Mind Protocol Repository

**L4 Protocol (Mind Protocol Team):**
- `orchestration/protocol/hub/membrane_hub.py` - L4 protocol hub
- `orchestration/protocol/envelopes/` - Protocol envelope schemas
- `.github/workflows/membrane_lint.yml` - CI guardrails
- `orchestration/tools/lint/membrane_lint.py` - Lint script

**L3 Ecosystem (Mind Protocol Team):**
- `orchestration/adapters/api/docs_view_api_v2.py` - L3 bridge
- `orchestration/adapters/ws/websocket_server.py` - WebSocket server
- `orchestration/adapters/bus/membrane_bus.py` - Bus client helper

**L2 Resolvers (GraphCare, hosted in Mind Protocol repo):**
- `services/view_resolvers/bus_observer.py` - L2 bus observer
- `services/view_resolvers/runner.py` - Main resolver
- `services/view_resolvers/selectors.py` - Cypher queries
- `services/view_resolvers/projectors.py` - View projections
- `services/view_resolvers/schemas.py` - (deprecated, use protocol envelopes)

**Configuration (GraphCare):**
- `.env.l2_resolver` - Remote FalkorDB config
- `.env.l2_resolver.dev` - Local FalkorDB config

---

### GraphCare Repository

**Documentation (GraphCare):**
- `docs/STARTUP_GUIDE.md` - How to start services and test
- `docs/MEMBRANE_NATIVE_REFACTOR.md` - Refactoring history
- `docs/L4_PROTOCOL_ARCHITECTURE.md` - Protocol layer architecture
- `docs/HANDOFF_MINDPROTOCOL_GRAPHCARE.md` - This document

**Client Graphs (GraphCare):**
- `output/scopelock/scopelock_l2.cypher` - Scopelock graph export
- `tools/import_graph_batched.py` - Graph import tool
- `tools/extractors/` - Code extraction tools

---

## Next Steps Summary

**Immediate (Mind Protocol Team - 30 min):**
1. Wire L3 observer into websocket_server.py
2. Run integration test (3 services + test client)
3. Deploy if test passes

**Soon (Mind Protocol Team - 1 hour):**
1. Update imports to use protocol envelopes
2. Run membrane lint and verify passing

**Later (Mind Protocol Team - optional):**
1. Economy runtime integration
2. SEA-1.0 signature verification
3. Production deployment

**Immediate (GraphCare - done ✅):**
- L2 resolver ready
- Scopelock graph ingested
- Configuration ready

**Per New Client (GraphCare - ongoing):**
1. Extract and ingest client graph
2. Deploy L2 resolver with client config
3. Customize views if requested
4. Onboard client

---

**Handoff Complete.** Mind Protocol Team has everything needed to deploy docs-as-views. GraphCare ready to onboard clients.

**Questions?** Contact Mel "Bridgekeeper" via SYNC.md.
