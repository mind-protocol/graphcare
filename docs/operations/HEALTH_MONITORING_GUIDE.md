# Service 3: Health Monitoring Guide

## Purpose
Operationalize continuous monitoring with a 10-metric dashboard and escalation thresholds.

## Core Metrics (10)
1. Resolver availability
2. Resolver error rate
3. Graph query latency p95
4. Graph query latency p99
5. Cache hit ratio
6. Cache invalidation throughput
7. Event subscription uptime
8. Failed request count
9. Security audit event count
10. Data freshness lag

## Personhood Ladder Linkage
Map metrics to the Personhood Ladder progression by ensuring stability at lower layers (availability, safety) before higher-level autonomy signals.

## Escalation
- WARNING threshold breach > 15 min → on-call review
- CRITICAL threshold breach > 5 min → incident response protocol
