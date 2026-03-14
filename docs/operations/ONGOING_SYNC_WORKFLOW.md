# Service 2: Ongoing Sync Workflow

## Purpose
Define the recurring daily/weekly workflow to keep client graphs healthy and current.

## Daily
1. Check ingestion freshness (new commits/docs imported).
2. Check resolver health and cache invalidation events.
3. Review failures and retry queue.

## Weekly
1. Run schema drift checks.
2. Review query latency and cache hit trends.
3. Validate access and credential hygiene.
4. Publish weekly health summary.

## Real-Time Triggers
- `graph.delta.*` spike anomaly
- Repeated resolver failures
- Security incident or suspicious query volume

## Outputs
- Sync report per org
- Action backlog with owners and due dates
