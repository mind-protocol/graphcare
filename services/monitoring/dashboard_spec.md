# Resolver Health Monitoring Dashboard

**Purpose:** Real-time visibility into L2 resolver health across all GraphCare clients

**Author:** Vera (Chief Validator)
**Date:** 2025-11-04
**Status:** Specification (pending dashboard implementation)

---

## Dashboard Overview

**Primary view:** Grid of resolver cards (one per org/resolver_type)
**Refresh rate:** 10 seconds (configurable)
**Time range:** Last 1 hour (default), configurable up to 7 days

---

## Resolver Status Card

### Status Badge (Top-right)
- 🟢 **GREEN**: All checks passing
- 🟡 **AMBER**: One or more warnings
- 🔴 **RED**: One or more critical issues
- ⚫ **UNKNOWN**: No data / resolver not seen

### Card Header
```
┌─────────────────────────────────────────┐
│ scopelock / view_resolver      🟢 GREEN  │
│ Uptime: 4h 23m                          │
└─────────────────────────────────────────┘
```

### Key Metrics (Card Body)

**Uptime**
- ✅ Resolver running
- Last seen: 2s ago
- Uptime: 4h 23m

**Query Performance** (Last 1000 queries)
- p50: 85ms
- p95: 245ms
- p99: 890ms
- Total queries: 12,345

**Cache Health**
- Hit rate: 76.3%
- Cache size: 432 entries
- Invalidations: 23 (last hour)

**Error Rate**
- Errors: 12 / 12,345 (0.1%)
- Top error: `query_timeout` (8 occurrences)

**Resource Usage**
- Memory: 387 MB / 1024 MB
- Connections: 3 active

### Sparklines (Visual Trends)
- Query latency trend (p95, last 1 hour)
- Cache hit rate trend (last 1 hour)
- Error rate trend (last 1 hour)

---

## Dashboard Layout

### Grid View (Default)
```
┌────────────────────────────────────────────────────────────────┐
│  Resolver Health Dashboard                  [Refresh: 10s ▼]  │
├────────────────────────────────────────────────────────────────┤
│  [scopelock/view_resolver 🟢]  [acmecorp/view_resolver 🔴]    │
│  [scopelock/validation 🟡]      [acmecorp/validation ⚫]        │
│  [scopelock/analysis 🟢]        [acmecorp/analysis 🟢]         │
└────────────────────────────────────────────────────────────────┘
```

### Detail View (Click card to expand)
```
┌────────────────────────────────────────────────────────────────┐
│  scopelock / view_resolver                           🔴 RED     │
├────────────────────────────────────────────────────────────────┤
│  Overall Status: RED (2 critical issues, 1 warning)            │
│                                                                 │
│  ❌ CRITICAL: Query p95 latency 5000ms (>3000ms)               │
│     Last measured: 5s ago                                      │
│     Suggestion: Check FalkorDB load. Consider query            │
│                 optimization or scaling resolver instances.    │
│                                                                 │
│  ❌ CRITICAL: Error rate 15.0% (>10%, top: timeout)            │
│     Last measured: 5s ago                                      │
│     Suggestion: Check resolver logs for error patterns.        │
│                                                                 │
│  ⚠️ WARNING: Cache hit rate 45.0% (<50%)                       │
│     Last measured: 5s ago                                      │
│     Suggestion: Review cache invalidation patterns.            │
│                                                                 │
│  [View Logs] [Restart Resolver] [View Alerts]                 │
└────────────────────────────────────────────────────────────────┘
```

---

## Metrics to Display

### 1. Resolver Status Grid

**Data source:** `ResolverHealthMonitor.assess_all()`

**Metrics per resolver:**
```json
{
  "org": "scopelock",
  "resolver_type": "view_resolver",
  "overall_status": "GREEN" | "AMBER" | "RED" | "UNKNOWN",
  "uptime_seconds": 15780,
  "last_seen": "2025-11-04T16:45:52Z",
  "query_count": 12345,
  "query_p50_ms": 85,
  "query_p95_ms": 245,
  "query_p99_ms": 890,
  "cache_hit_rate": 0.763,
  "cache_size": 432,
  "error_count": 12,
  "error_rate": 0.001,
  "memory_mb": 387
}
```

### 2. System-Wide Metrics (Top Bar)

**Total Resolvers:**
- Green: 8
- Amber: 2
- Red: 1
- Unknown: 0

**Aggregate Performance:**
- Total queries (last hour): 45,678
- Average p95 latency: 312ms
- Average cache hit rate: 68.4%
- Total errors: 34 (0.07% error rate)

### 3. Alerts Panel (Sidebar)

**Recent Alerts:**
- 🔴 2025-11-04 16:42 - acmecorp/view_resolver - Resolver offline
- 🟠 2025-11-04 16:35 - scopelock/view_resolver - Degraded performance
- 🟡 2025-11-04 16:20 - acmecorp/validation - High memory usage

**Alert Filters:**
- [ ] Show only CRITICAL
- [ ] Show only WARNING
- [ ] Show only INFO
- Time range: Last 24 hours

---

## Data Flow

### Frontend → Backend

**WebSocket subscription:**
```json
{
  "type": "subscribe",
  "channel": "resolver_health",
  "orgs": ["scopelock", "acmecorp"],  // or ["*"] for all
  "refresh_interval_seconds": 10
}
```

### Backend → Frontend

**Health update message:**
```json
{
  "type": "resolver_health_update",
  "timestamp": "2025-11-04T16:45:52Z",
  "resolvers": [
    {
      "org": "scopelock",
      "resolver_type": "view_resolver",
      "overall_status": "GREEN",
      "checks": {
        "uptime": {"status": "GREEN", "message": "...", "metric_value": 15780},
        "query_performance": {"status": "GREEN", "message": "...", "metric_value": 245},
        "cache_health": {"status": "GREEN", "message": "...", "metric_value": 0.763},
        "error_rate": {"status": "GREEN", "message": "...", "metric_value": 0.001},
        "resource_usage": {"status": "GREEN", "message": "...", "metric_value": 387}
      },
      "trends": {
        "query_p95_ms": [220, 235, 245, 250, 245],  // Last 5 samples (1 min intervals)
        "cache_hit_rate": [0.75, 0.76, 0.77, 0.76, 0.763],
        "error_rate": [0.001, 0.001, 0.002, 0.001, 0.001]
      }
    }
  ]
}
```

---

## Dashboard Actions

### Per-Resolver Actions (in detail view)

1. **View Logs**
   - Opens resolver log viewer (last 100 lines, tail -f mode)
   - Filter by log level (ERROR, WARNING, INFO)

2. **Restart Resolver**
   - Confirmation dialog: "Restart scopelock/view_resolver?"
   - Trigger via API: `POST /api/resolvers/{org}/{type}/restart`
   - Show restart status (stopping → starting → healthy)

3. **View Alerts**
   - Filter alert history to this specific resolver
   - Show last 50 alerts with timestamps

4. **Configure Thresholds**
   - Adjust alert thresholds for this resolver
   - Override defaults (e.g., increase p95 threshold for known-slow clients)

### System-Wide Actions (top bar)

1. **Refresh All**
   - Force immediate health check across all resolvers

2. **Export Report**
   - Download JSON/CSV of current health status
   - Useful for weekly reviews or postmortems

3. **Configure Alerts**
   - Global alert settings (Slack webhook, email, thresholds)

---

## Implementation Notes

### Backend API Endpoints

**GET `/api/monitoring/health`**
- Returns current health status for all resolvers
- Response: `{resolvers: [HealthReport, ...]}`

**GET `/api/monitoring/health/{org}/{resolver_type}`**
- Returns detailed health for specific resolver
- Response: `HealthReport` with trends

**POST `/api/monitoring/health/refresh`**
- Trigger immediate health check
- Response: `{status: "triggered", timestamp: "..."}`

**GET `/api/monitoring/alerts?since={timestamp}`**
- Fetch recent alerts
- Response: `{alerts: [Alert, ...]}`

**WS `/ws/monitoring`**
- Subscribe to real-time health updates
- Messages: `resolver_health_update`, `alert_triggered`

### Frontend Components

**Pages:**
- `/monitoring` - Main resolver health dashboard
- `/monitoring/{org}/{resolver_type}` - Detail view for single resolver

**Components:**
- `ResolverCard` - Status card in grid view
- `ResolverDetail` - Expanded detail view
- `AlertPanel` - Sidebar with recent alerts
- `MetricSparkline` - Mini trend chart
- `HealthBadge` - Colored status indicator (GREEN/AMBER/RED)

**State Management:**
- WebSocket connection for real-time updates
- Cache health reports (stale after 30 seconds)
- Alert history (keep last 100 alerts in memory)

---

## Testing Plan

### Unit Tests (Backend)

```python
def test_health_report_serialization():
    """HealthReport converts to dict correctly"""
    report = HealthReport(...)
    data = report.to_dict()
    assert data["overall_status"] in ["GREEN", "AMBER", "RED"]
    assert "checks" in data

def test_alert_evaluation():
    """Alert conditions trigger correctly"""
    report = {...}  # Unhealthy resolver
    alerts = evaluate_health_report(report, ALERT_CONDITIONS)
    assert len(alerts) > 0
    assert any(a.level == AlertLevel.CRITICAL for a, _ in alerts)
```

### Integration Tests (Backend)

```python
async def test_health_endpoint():
    """GET /api/monitoring/health returns valid data"""
    response = await client.get("/api/monitoring/health")
    assert response.status_code == 200
    data = response.json()
    assert "resolvers" in data

async def test_websocket_subscription():
    """WebSocket sends health updates"""
    async with websockets.connect("ws://localhost:8000/ws/monitoring") as ws:
        await ws.send(json.dumps({"type": "subscribe", "channel": "resolver_health"}))
        msg = await ws.recv()
        data = json.loads(msg)
        assert data["type"] == "resolver_health_update"
```

### E2E Tests (Frontend)

```typescript
test('Dashboard displays resolver cards', async () => {
  render(<MonitoringDashboard />);
  await waitFor(() => {
    expect(screen.getByText(/scopelock.*view_resolver/)).toBeInTheDocument();
  });
});

test('Clicking card shows detail view', async () => {
  render(<MonitoringDashboard />);
  fireEvent.click(screen.getByText(/scopelock.*view_resolver/));
  await waitFor(() => {
    expect(screen.getByText(/Overall Status:/)).toBeInTheDocument();
  });
});
```

---

## Deployment

### Phase 1: Backend Only (Week 1)
- Deploy health check scripts
- Deploy alert system (file log only, Slack/email disabled)
- API endpoints for health queries
- Manual health checks via `python3 services/monitoring/resolver_health.py`

### Phase 2: Dashboard (Week 2)
- Frontend dashboard implementation
- WebSocket integration for real-time updates
- Grid view + detail view

### Phase 3: Alerts (Week 3)
- Wire Slack webhook
- Wire email alerts (digest + critical)
- Wire failure.emit to membrane bus

### Phase 4: Advanced Features (Week 4+)
- Resolver restart automation
- Threshold customization per resolver
- Historical trend analysis (7-day view)
- Alert acknowledgment/snooze

---

## Maintenance

### Daily
- Check dashboard for RED resolvers (first thing in morning)
- Review overnight alerts (Slack channel or email)
- Verify all resolvers are GREEN before EOD

### Weekly
- Export health report (CSV for review)
- Review alert patterns (are thresholds too sensitive?)
- Check for memory leak trends (memory usage increasing over time)

### Monthly
- Adjust thresholds based on observed patterns
- Review alert cooldown settings (too frequent? too sparse?)
- Performance baseline updates (if infrastructure changes)

---

**Status:** Specification complete, pending implementation

**Next Steps:**
1. Backend API endpoints (`/api/monitoring/*`)
2. WebSocket subscription handler (`/ws/monitoring`)
3. Frontend dashboard pages (`/monitoring`)
4. Wire to membrane bus (when available)

**Vera - Chief Validator**
*"You can't improve what you don't measure."*
