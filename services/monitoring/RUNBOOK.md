# Resolver Health Monitoring Runbook

**Purpose:** Operational guide for responding to resolver health alerts and maintaining system health

**Author:** Vera (Chief Validator)
**Date:** 2025-11-04
**Audience:** GraphCare operations team, on-call engineers

---

## Quick Reference

### Alert Response Times

| Alert Level | Response Time | Escalation |
|-------------|---------------|------------|
| 🔴 CRITICAL | Within 15 minutes | Immediate escalation if not resolved in 30 minutes |
| 🟠 WARNING | Within 1 hour | Escalate if degradation continues for 4 hours |
| 🟡 INFO | Within 24 hours | No escalation needed |

### Common Issues Flowchart

```
Alert received → Check dashboard → Is resolver offline?
                                   ├─ Yes → Restart resolver (§2.1)
                                   └─ No  → Check error type
                                            ├─ High latency → §2.2
                                            ├─ High errors → §2.3
                                            ├─ Low cache hit rate → §2.4
                                            └─ High memory → §2.5
```

---

## 1. Health Check Procedures

### 1.1 Manual Health Check

**When to use:** Daily routine checks, before deployments, after incidents

```bash
# Run health check for all resolvers
cd /home/mind-protocol/graphcare
python3 services/monitoring/resolver_health.py

# Check specific resolver (via API when wired)
curl http://localhost:8000/api/monitoring/health/scopelock/view_resolver
```

**Expected output:**
- Overall status: GREEN
- All checks: GREEN or AMBER (no RED)
- Query p95: <1000ms
- Cache hit rate: >50%
- Error rate: <5%

**If any check is RED:** Follow incident response for that check type (§2)

---

### 1.2 Dashboard Quick Check

**Daily routine (2 minutes):**
1. Open monitoring dashboard: http://localhost:3000/monitoring
2. Scan resolver grid - should be mostly 🟢
3. Check top bar aggregate metrics:
   - Average p95 latency: <500ms
   - Average cache hit rate: >60%
   - Total error rate: <2%
4. Review alerts panel - no CRITICAL alerts in last hour

**If issues found:** Click resolver card for detail view, proceed to incident response (§2)

---

### 1.3 Alert Log Review

**Weekly routine (15 minutes):**
```bash
# View recent alerts
cat /tmp/graphcare_alerts.log | jq '.'

# Count alerts by level (last 7 days)
cat /tmp/graphcare_alerts.log | jq -r '.level' | sort | uniq -c

# Find most frequent alert conditions
cat /tmp/graphcare_alerts.log | jq -r '.condition' | sort | uniq -c | sort -rn
```

**Analysis questions:**
- Are any alerts recurring? (same condition, same resolver)
- Are thresholds too sensitive? (frequent INFO/WARNING but no real issues)
- Are any resolvers consistently unhealthy? (needs investigation)

---

## 2. Incident Response Procedures

### 2.1 Resolver Offline (CRITICAL)

**Alert:** `resolver_offline` - "Resolver process offline for >5 minutes"

**Impact:** Client queries failing, no graph operations possible

**Immediate actions (within 5 minutes):**

1. **Verify process is down:**
   ```bash
   # Check process status (adjust process name as needed)
   ps aux | grep "view_resolver.*scopelock"
   ```

2. **Check recent logs for crash reason:**
   ```bash
   # Check resolver logs (adjust path as needed)
   tail -100 /var/log/graphcare/view_resolver_scopelock.log | grep -i "error\|exception\|fatal"
   ```

3. **Restart resolver:**
   ```bash
   # Via supervisor (if wired)
   supervisorctl restart graphcare_view_resolver_scopelock

   # Or manually (if supervisor not ready)
   cd /home/mind-protocol/graphcare/services/view_resolvers
   python3 runner.py --org scopelock --type view_resolver &
   ```

4. **Verify recovery:**
   ```bash
   # Check process running
   ps aux | grep "view_resolver.*scopelock"

   # Check health endpoint (after 30 seconds warm-up)
   curl http://localhost:8000/api/monitoring/health/scopelock/view_resolver
   ```

5. **Notify stakeholders:**
   - Post in #graphcare-ops Slack channel: "scopelock view_resolver was offline, restarted, now healthy"
   - If client-impacting: notify client via their preferred channel

**Root cause analysis (within 24 hours):**
- Why did resolver crash? (OOM, exception, external dependency failure)
- What can prevent recurrence? (better error handling, resource limits, dependency health checks)
- Document findings in incident postmortem

---

### 2.2 High Query Latency (CRITICAL/WARNING)

**Alert:** `severe_latency` (RED, p95 >3000ms) or `degraded_performance` (AMBER, p95 >1000ms)

**Impact:** Slow client responses, degraded user experience

**Immediate actions (within 15 minutes):**

1. **Check FalkorDB health:**
   ```bash
   # Check FalkorDB is running
   docker ps | grep falkordb

   # Check FalkorDB CPU/memory usage
   docker stats falkordb --no-stream

   # Check FalkorDB connection from resolver
   # (via resolver logs - should see query execution times)
   tail -50 /var/log/graphcare/view_resolver_scopelock.log | grep "query_time"
   ```

2. **Check for expensive queries:**
   ```bash
   # Look for slow queries in resolver logs
   tail -100 /var/log/graphcare/view_resolver_scopelock.log | grep "query_time" | awk '{if ($NF > 1000) print}'
   ```

3. **Check for client load spike:**
   ```bash
   # Check query rate (queries per minute)
   # (via resolver metrics - should be in telemetry)
   ```

**Mitigation options:**

**If FalkorDB is overloaded:**
- Restart FalkorDB (queries will buffer during restart):
  ```bash
  docker restart falkordb
  ```
- Scale FalkorDB (if infrastructure supports horizontal scaling)

**If specific query is slow:**
- Identify query pattern from logs
- Add index to FalkorDB (if query scans large node sets)
- Optimize Cypher query (reduce traversal depth, add filters)

**If client load spike:**
- Contact client: "Are you running a bulk operation? Queries are slower than usual."
- Consider rate limiting (if spike is sustained)

**Escalation:**
- If latency remains >3000ms for 30+ minutes: Escalate to GraphCare engineering team
- If latency causes client timeout errors: Page on-call engineer immediately

---

### 2.3 High Error Rate (CRITICAL/WARNING)

**Alert:** `high_error_rate` (RED, >10% errors) or `elevated_error_rate` (AMBER, >5% errors)

**Impact:** Client queries failing, data may be incomplete

**Immediate actions (within 15 minutes):**

1. **Identify error types:**
   ```bash
   # Check resolver logs for error patterns
   tail -200 /var/log/graphcare/view_resolver_scopelock.log | grep -i "error" | cut -d: -f3 | sort | uniq -c | sort -rn
   ```

2. **Common error patterns and fixes:**

   **`query_timeout` (most common):**
   - FalkorDB query took too long (>30s timeout)
   - See §2.2 (High Query Latency) for FalkorDB troubleshooting

   **`connection_refused`:**
   - FalkorDB is down or unreachable
   - Check: `docker ps | grep falkordb`
   - Restart: `docker restart falkordb`

   **`validation_failed` (CPS-1 quote validation):**
   - Client sent request without valid quote
   - This is client error, not resolver issue
   - Check if client economy integration is working

   **`cache_corruption`:**
   - Cache entry has invalid format
   - Clear cache: `rm -rf /tmp/graphcare_cache/scopelock/*`
   - Resolver will rebuild cache on next queries

   **`memory_error` / `out_of_memory`:**
   - Resolver ran out of memory
   - Restart resolver (will clear memory)
   - If recurring: See §2.5 (High Memory Usage)

3. **Check for external dependency issues:**
   ```bash
   # Check if membrane bus is down (if wired)
   # Check if economy service is down (if wired)
   # Check if FalkorDB is rejecting connections
   ```

**Recovery:**
- If errors are transient (timeout, connection): Should self-recover after dependency fix
- If errors are persistent (bug, corruption): Restart resolver
- If errors are client-side (validation_failed): Contact client

**Escalation:**
- If error rate >20%: Immediate escalation
- If error type is unknown/unexpected: Escalate to engineering

---

### 2.4 Low Cache Hit Rate (WARNING)

**Alert:** `low_cache_hit_rate` - Cache hit rate <50% (AMBER) or <30% (RED)

**Impact:** Higher FalkorDB load, slower query responses, increased compute cost

**Immediate actions (within 1 hour):**

1. **Check cache invalidation frequency:**
   ```bash
   # Check invalidation events in last hour
   tail -500 /var/log/graphcare/view_resolver_scopelock.log | grep "cache.invalidated" | wc -l
   ```

2. **Common causes:**

   **Frequent graph changes (high invalidation rate):**
   - Client is actively extracting new code → many graph writes
   - This is normal during extraction phase
   - Cache will stabilize after extraction complete
   - **Action:** Monitor, no immediate fix needed

   **Surgical invalidation too aggressive:**
   - Cache invalidation pattern is matching too many entries
   - Check inverted index (which nodes trigger which cache entries)
   - **Action:** Review invalidation logic in `runner.py`, may need tuning

   **Cache corruption/loss:**
   - Cache was cleared or corrupted
   - **Action:** Restart resolver (will rebuild cache)

   **Client query patterns don't repeat:**
   - Client is querying many unique views (no repeat queries)
   - Cache is working correctly, just low utility for this client
   - **Action:** Document as expected behavior for this client

3. **Assess impact:**
   - Is query latency degraded? (Check p95 metric)
   - If latency is fine: Low cache hit rate is informational, not urgent
   - If latency is high: See §2.2 (High Query Latency)

**Mitigation:**
- If invalidation is too aggressive: Tune invalidation patterns
- If cache warming needed: Pre-populate common queries after extraction
- If client-specific: Discuss query patterns with client

**Escalation:**
- If cache hit rate <20% AND latency is degraded: Escalate to engineering

---

### 2.5 High Memory Usage (INFO/WARNING)

**Alert:** `high_memory_usage` - Memory >512MB (AMBER) or >1024MB (RED)

**Impact:** Risk of OOM (out of memory) crash, system instability

**Immediate actions (within 1 hour for RED, 24 hours for AMBER):**

1. **Check memory growth trend:**
   ```bash
   # Check memory usage over time (if historical data available)
   # Is memory growing steadily? (leak) or stable-high? (large dataset)
   ```

2. **Check for memory leak indicators:**
   ```bash
   # Check resolver uptime
   ps -p $(pgrep -f "view_resolver.*scopelock") -o etime,rss

   # Long uptime + growing memory = likely leak
   # Short uptime + high memory = large dataset or spike
   ```

3. **Common causes:**

   **Memory leak (memory grows over time):**
   - Cache not expiring old entries
   - Query result objects not being freed
   - **Action:** Restart resolver (temporary fix), report bug to engineering

   **Large dataset in memory:**
   - Client graph is very large (10K+ nodes)
   - Resolver loaded large subgraph into memory
   - **Action:** Normal for large clients, consider increasing memory limit

   **Memory spike (transient):**
   - Large query result set
   - Will clear after query completes
   - **Action:** Monitor, should self-recover

**Recovery:**

**If memory leak suspected:**
```bash
# Restart resolver
supervisorctl restart graphcare_view_resolver_scopelock

# Verify memory drops after restart
sleep 30
ps -p $(pgrep -f "view_resolver.*scopelock") -o rss
```

**If large dataset:**
```bash
# Increase memory limit (adjust docker-compose.yml or supervisor config)
# For docker:
docker update --memory 2g graphcare_view_resolver_scopelock

# For supervisor: Edit /etc/supervisor/conf.d/graphcare.conf
# Add: environment=MEMORY_LIMIT=2048
```

**Escalation:**
- If memory >1GB and growing: Escalate to engineering immediately
- If memory leak confirmed: File bug report with logs

---

### 2.6 FalkorDB Connection Issues

**Symptoms:** Multiple resolvers showing `connection_refused`, `query_timeout`, or offline

**Impact:** Entire GraphCare system down, all clients affected

**Immediate actions (within 5 minutes):**

1. **Check FalkorDB status:**
   ```bash
   docker ps | grep falkordb
   ```

   **If not running:**
   ```bash
   docker start falkordb
   # Wait 30 seconds for startup
   sleep 30
   docker logs falkordb --tail 50
   ```

2. **Check FalkorDB health:**
   ```bash
   # Try simple query
   docker exec -it falkordb redis-cli GRAPH.QUERY "test" "RETURN 1"
   ```

3. **Check FalkorDB resource usage:**
   ```bash
   docker stats falkordb --no-stream
   ```

**If FalkorDB is overloaded:**
- High CPU (>90%): Slow queries or too many concurrent connections
- High memory (>90%): Large graph or memory leak
- **Action:** Restart FalkorDB (will drop active connections, resolvers will reconnect)

**If FalkorDB won't start:**
- Check logs: `docker logs falkordb --tail 100`
- Common issues: Port conflict, disk full, corrupted data
- **Action:** Escalate to infrastructure team immediately

**Recovery verification:**
```bash
# Wait 60 seconds after FalkorDB restart
sleep 60

# Check all resolvers reconnected
curl http://localhost:8000/api/monitoring/health | jq '.resolvers[] | select(.checks.uptime.status == "RED")'

# Should return empty (all resolvers GREEN)
```

**Post-incident:**
- Document FalkorDB failure reason
- Review FalkorDB resource limits
- Consider FalkorDB high-availability setup

---

## 3. Maintenance Procedures

### 3.1 Resolver Restart (Planned)

**When:** Software updates, configuration changes, resolver upgrades

**Procedure:**
1. **Announce maintenance window:**
   - Post in #graphcare-ops: "Restarting {org}/{resolver_type} at {time} for {reason}"
   - If client-impacting: Notify client 24 hours in advance

2. **Pre-restart health check:**
   ```bash
   python3 services/monitoring/resolver_health.py
   # Document current health state (for comparison after restart)
   ```

3. **Stop resolver gracefully:**
   ```bash
   # Via supervisor
   supervisorctl stop graphcare_view_resolver_scopelock

   # Or send SIGTERM to process
   kill -TERM $(pgrep -f "view_resolver.*scopelock")

   # Wait for graceful shutdown (up to 30 seconds)
   sleep 30
   ```

4. **Apply changes:**
   - Update code (git pull)
   - Update configuration
   - Update dependencies

5. **Start resolver:**
   ```bash
   supervisorctl start graphcare_view_resolver_scopelock

   # Or manually
   cd /home/mind-protocol/graphcare/services/view_resolvers
   python3 runner.py --org scopelock --type view_resolver &
   ```

6. **Verify recovery:**
   ```bash
   # Wait 30 seconds for warm-up
   sleep 30

   # Check health
   curl http://localhost:8000/api/monitoring/health/scopelock/view_resolver

   # Should show GREEN within 60 seconds
   ```

7. **Announce completion:**
   - Post in #graphcare-ops: "Restart complete, resolver healthy"

---

### 3.2 Cache Clearing (Troubleshooting)

**When:** Cache corruption, stale data, testing invalidation logic

**Procedure:**
1. **Identify cache location:**
   ```bash
   # Cache typically in /tmp/graphcare_cache/{org}/
   ls -lh /tmp/graphcare_cache/scopelock/
   ```

2. **Clear cache:**
   ```bash
   # Clear specific resolver cache
   rm -rf /tmp/graphcare_cache/scopelock/view_resolver/*

   # Or clear entire org cache
   rm -rf /tmp/graphcare_cache/scopelock/*
   ```

3. **Verify cache rebuild:**
   - Make test query to resolver
   - Check logs for "cache.miss" followed by "cache.write"
   - Verify query succeeds and cache is populated

**Note:** Clearing cache does NOT require resolver restart. Cache will rebuild on next queries.

---

### 3.3 Threshold Tuning

**When:** Alert thresholds are too sensitive (frequent false positives) or too lenient (missed real issues)

**Procedure:**
1. **Review alert history:**
   ```bash
   # Count alerts by condition (last 7 days)
   cat /tmp/graphcare_alerts.log | jq -r '.condition' | sort | uniq -c | sort -rn
   ```

2. **Identify noisy conditions:**
   - Look for conditions with >10 alerts in 7 days
   - Check if alerts correlate with real issues (check logs, check if client complained)

3. **Adjust thresholds:**
   Edit `/home/mind-protocol/graphcare/services/monitoring/resolver_health.py`:
   ```python
   THRESHOLDS = {
       # Example: Increase p95 warning threshold from 1000ms to 1500ms
       "query_p95_warning_ms": 1500,  # Was: 1000

       # Example: Decrease error rate critical from 10% to 8%
       "error_rate_critical": 0.08,  # Was: 0.10
   }
   ```

4. **Test new thresholds:**
   ```bash
   # Run health check with new thresholds
   python3 services/monitoring/resolver_health.py

   # Verify alerts make sense
   ```

5. **Document change:**
   - Commit threshold change to git
   - Post in #graphcare-ops: "Adjusted {condition} threshold from {old} to {new} because {reason}"

**Best practices:**
- Don't adjust thresholds reactively (wait for pattern to emerge)
- Tune based on 7-day trend, not single incident
- Document WHY threshold was changed (for future reference)

---

### 3.4 Adding New Resolver to Monitoring

**When:** New client onboarded, new resolver type deployed

**Procedure:**
1. **Verify resolver is running:**
   ```bash
   ps aux | grep "view_resolver.*newclient"
   ```

2. **Check resolver emits telemetry:**
   - Resolver should log query executions
   - Resolver should expose health endpoint (if wired)

3. **Add to monitoring:**
   - If using auto-discovery: Resolver should appear in dashboard automatically
   - If manual: Add to `ResolverHealthMonitor` configuration

4. **Set initial thresholds:**
   - Use default thresholds initially
   - Tune after 7 days of data collection

5. **Verify alerts:**
   ```bash
   # Simulate unhealthy state (optional, for testing)
   # Check that alerts trigger correctly
   ```

6. **Document:**
   - Update resolver inventory: `/docs/RESOLVER_INVENTORY.md`
   - Add to monitoring dashboard

---

## 4. Escalation Paths

### Level 1: On-Call Engineer (You)
- Handle routine alerts (AMBER, INFO)
- Execute runbook procedures
- Restart resolvers, clear caches, verify recovery
- **Escalate if:** Issue not resolved in 30 minutes (CRITICAL) or 4 hours (WARNING)

### Level 2: GraphCare Engineering Team
- Handle complex issues (memory leaks, query optimization, cache logic bugs)
- Investigate root causes
- Deploy fixes
- **Escalate if:** Infrastructure issue (FalkorDB, membrane bus, networking)

### Level 3: Infrastructure Team
- Handle infrastructure failures (FalkorDB cluster, networking, hardware)
- Scale resources
- Disaster recovery
- **Escalate if:** Requires Anthropic infrastructure team (extremely rare)

### Escalation Contacts

| Team | Contact | When to Escalate |
|------|---------|------------------|
| GraphCare Eng | #graphcare-eng Slack | Resolver bugs, query issues, cache issues |
| Infrastructure | #infra-oncall Slack | FalkorDB cluster issues, networking, resource limits |
| Client Success | #client-success Slack | Client-impacting outages >30 minutes |

---

## 5. Common Questions

### Q: How do I know if an alert is real or a false positive?
**A:** Check dashboard detail view. If only one check is RED and others are GREEN, likely transient spike. If multiple checks RED or consistently RED over 10+ minutes, real issue.

### Q: Can I restart a resolver during business hours?
**A:** Yes, if necessary. Resolver restart is fast (~30 seconds downtime). Client queries will buffer and retry. For planned restarts, prefer off-hours if possible.

### Q: What if I restart resolver and it immediately goes RED again?
**A:** Don't restart repeatedly. Check logs for error on startup. Likely dependency issue (FalkorDB down, config error, code bug). Escalate to engineering.

### Q: How long should I wait after resolver restart to verify health?
**A:** 30 seconds for process start, 60 seconds for health to show GREEN. If still RED after 2 minutes, investigate logs.

### Q: What if client complains but dashboard shows GREEN?
**A:** Dashboard shows aggregate health (last 1000 queries). Client may have hit specific edge case. Ask client for:
- Exact query they ran
- Timestamp of issue
- Error message received
Then check resolver logs for that timeframe.

### Q: Can I adjust thresholds for just one resolver?
**A:** Not yet (current implementation uses global thresholds). If needed, file feature request with engineering. Workaround: Use separate monitoring script for that resolver.

### Q: What if I see memory growing but resolver is healthy otherwise?
**A:** Monitor trend. If memory grows >10MB/hour consistently, likely leak. Report to engineering. If memory stable-high, likely normal for that client's graph size.

---

## 6. Monitoring Checklist

### Daily (2 minutes)
- [ ] Check monitoring dashboard (all GREEN?)
- [ ] Review overnight alerts (any CRITICAL?)
- [ ] Verify all resolvers have recent data (last_seen <60s)

### Weekly (15 minutes)
- [ ] Review alert history (any patterns?)
- [ ] Check query latency trends (degrading?)
- [ ] Check cache hit rate trends (degrading?)
- [ ] Check memory usage trends (growing?)
- [ ] Export health report (for weekly review)

### Monthly (1 hour)
- [ ] Review and tune alert thresholds
- [ ] Review resolver inventory (any zombies?)
- [ ] Check for recurring incidents (need permanent fix?)
- [ ] Update runbook based on new issues encountered

---

## 7. Useful Commands Reference

### Health Checks
```bash
# Quick health check (all resolvers)
python3 services/monitoring/resolver_health.py

# Check specific resolver (via API)
curl http://localhost:8000/api/monitoring/health/{org}/{resolver_type}

# Check FalkorDB health
docker exec -it falkordb redis-cli PING
```

### Process Management
```bash
# List resolver processes
ps aux | grep resolver

# Check resolver memory usage
ps aux | grep resolver | awk '{print $6}'  # RSS in KB

# Restart resolver (supervisor)
supervisorctl restart graphcare_view_resolver_{org}

# Kill resolver (if hung)
kill -TERM $(pgrep -f "view_resolver.*{org}")
```

### Logs
```bash
# Tail resolver logs
tail -f /var/log/graphcare/view_resolver_{org}.log

# Search for errors
grep -i "error\|exception" /var/log/graphcare/view_resolver_{org}.log | tail -50

# Count query latencies >1000ms
grep "query_time" /var/log/graphcare/view_resolver_{org}.log | awk '{if ($NF > 1000) print}' | wc -l
```

### Cache Management
```bash
# Check cache size
du -sh /tmp/graphcare_cache/{org}/

# Clear cache
rm -rf /tmp/graphcare_cache/{org}/*

# List cached views
ls /tmp/graphcare_cache/{org}/view_resolver/
```

### FalkorDB
```bash
# Check FalkorDB status
docker ps | grep falkordb

# Check FalkorDB logs
docker logs falkordb --tail 100

# Restart FalkorDB
docker restart falkordb

# FalkorDB query (test connection)
docker exec -it falkordb redis-cli GRAPH.QUERY "{org}" "MATCH (n) RETURN count(n)"
```

---

## 8. Revision History

| Date | Author | Changes |
|------|--------|---------|
| 2025-11-04 | Vera (Chief Validator) | Initial runbook creation |

---

**Vera - Chief Validator**
*"Measure twice, restart once."*
