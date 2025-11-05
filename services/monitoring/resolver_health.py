"""
Resolver Health Monitoring for GraphCare L2 Resolvers

Monitors health metrics for L2 resolvers:
- Uptime (resolver process running, membrane bus subscription active)
- Query performance (Cypher execution time p50/p95/p99)
- Cache health (hit rate, size, invalidation rate)
- Error rate (failure.emit frequency)
- Resource usage (memory, connections)

Author: Vera (Chief Validator)
Date: 2025-11-04
"""

import time
import psutil
import asyncio
import statistics
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict, deque
from pathlib import Path
import json
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# Data Structures
# ============================================================================

@dataclass
class HealthStatus:
    """Health status for a component"""
    status: str  # "GREEN", "AMBER", "RED"
    message: str
    metric_value: Optional[float] = None
    threshold: Optional[float] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "message": self.message,
            "metric_value": self.metric_value,
            "threshold": self.threshold,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class ResolverMetrics:
    """Metrics for a single resolver"""
    org: str
    resolver_type: str  # "view_resolver", "validation_resolver", etc.

    # Uptime
    process_running: bool = False
    uptime_seconds: float = 0.0
    last_seen: Optional[datetime] = None

    # Query performance (milliseconds)
    query_latencies: deque = field(default_factory=lambda: deque(maxlen=1000))
    query_count: int = 0

    # Cache metrics
    cache_hits: int = 0
    cache_misses: int = 0
    cache_size: int = 0
    invalidations: int = 0

    # Error metrics
    error_count: int = 0
    errors_by_type: Dict[str, int] = field(default_factory=lambda: defaultdict(int))

    # Resource usage
    memory_mb: float = 0.0
    connection_count: int = 0

    def cache_hit_rate(self) -> float:
        """Calculate cache hit rate (0.0 to 1.0)"""
        total = self.cache_hits + self.cache_misses
        if total == 0:
            return 0.0
        return self.cache_hits / total

    def error_rate(self) -> float:
        """Calculate error rate (errors per query, 0.0 to 1.0)"""
        if self.query_count == 0:
            return 0.0
        return min(1.0, self.error_count / self.query_count)

    def query_p50(self) -> Optional[float]:
        """50th percentile query latency (ms)"""
        if not self.query_latencies:
            return None
        return statistics.median(self.query_latencies)

    def query_p95(self) -> Optional[float]:
        """95th percentile query latency (ms)"""
        if not self.query_latencies:
            return None
        sorted_latencies = sorted(self.query_latencies)
        idx = int(len(sorted_latencies) * 0.95)
        return sorted_latencies[idx] if idx < len(sorted_latencies) else sorted_latencies[-1]

    def query_p99(self) -> Optional[float]:
        """99th percentile query latency (ms)"""
        if not self.query_latencies:
            return None
        sorted_latencies = sorted(self.query_latencies)
        idx = int(len(sorted_latencies) * 0.99)
        return sorted_latencies[idx] if idx < len(sorted_latencies) else sorted_latencies[-1]


# ============================================================================
# Health Thresholds (configurable)
# ============================================================================

THRESHOLDS = {
    # Uptime thresholds
    "uptime_critical_seconds": 300,  # 5 minutes offline = CRITICAL
    "uptime_warning_seconds": 60,    # 1 minute offline = WARNING

    # Query performance thresholds (milliseconds)
    "query_p95_warning_ms": 1000,    # p95 > 1s = WARNING
    "query_p95_critical_ms": 3000,   # p95 > 3s = CRITICAL
    "query_p99_critical_ms": 5000,   # p99 > 5s = CRITICAL

    # Cache health thresholds
    "cache_hit_rate_warning": 0.5,   # <50% hit rate = WARNING
    "cache_hit_rate_critical": 0.3,  # <30% hit rate = CRITICAL

    # Error rate thresholds
    "error_rate_warning": 0.05,      # >5% errors = WARNING
    "error_rate_critical": 0.10,     # >10% errors = CRITICAL

    # Resource usage thresholds
    "memory_warning_mb": 512,        # >512MB = WARNING
    "memory_critical_mb": 1024,      # >1GB = CRITICAL
}


# ============================================================================
# Health Check Functions
# ============================================================================

def check_resolver_uptime(metrics: ResolverMetrics) -> HealthStatus:
    """
    Check if resolver process is running and responsive.

    Returns:
        HealthStatus with GREEN/AMBER/RED status
    """
    if not metrics.process_running:
        offline_seconds = 0
        if metrics.last_seen:
            offline_seconds = (datetime.utcnow() - metrics.last_seen).total_seconds()

        if offline_seconds > THRESHOLDS["uptime_critical_seconds"]:
            return HealthStatus(
                status="RED",
                message=f"Resolver offline for {offline_seconds:.0f}s (>{THRESHOLDS['uptime_critical_seconds']}s)",
                metric_value=offline_seconds,
                threshold=THRESHOLDS["uptime_critical_seconds"]
            )
        elif offline_seconds > THRESHOLDS["uptime_warning_seconds"]:
            return HealthStatus(
                status="AMBER",
                message=f"Resolver offline for {offline_seconds:.0f}s (>{THRESHOLDS['uptime_warning_seconds']}s)",
                metric_value=offline_seconds,
                threshold=THRESHOLDS["uptime_warning_seconds"]
            )
        else:
            return HealthStatus(
                status="AMBER",
                message=f"Resolver not running (offline {offline_seconds:.0f}s)",
                metric_value=offline_seconds
            )

    return HealthStatus(
        status="GREEN",
        message=f"Resolver running (uptime: {metrics.uptime_seconds:.0f}s)",
        metric_value=metrics.uptime_seconds
    )


def check_query_performance(metrics: ResolverMetrics) -> HealthStatus:
    """
    Check query execution performance.

    Monitors p50/p95/p99 latencies against thresholds.

    Returns:
        HealthStatus with GREEN/AMBER/RED status
    """
    p95 = metrics.query_p95()
    p99 = metrics.query_p99()

    if p95 is None:
        return HealthStatus(
            status="AMBER",
            message="No query data yet",
        )

    # Check p99 first (most critical)
    if p99 and p99 > THRESHOLDS["query_p99_critical_ms"]:
        return HealthStatus(
            status="RED",
            message=f"Query p99 latency {p99:.0f}ms (>{THRESHOLDS['query_p99_critical_ms']}ms)",
            metric_value=p99,
            threshold=THRESHOLDS["query_p99_critical_ms"]
        )

    # Check p95
    if p95 > THRESHOLDS["query_p95_critical_ms"]:
        return HealthStatus(
            status="RED",
            message=f"Query p95 latency {p95:.0f}ms (>{THRESHOLDS['query_p95_critical_ms']}ms)",
            metric_value=p95,
            threshold=THRESHOLDS["query_p95_critical_ms"]
        )
    elif p95 > THRESHOLDS["query_p95_warning_ms"]:
        return HealthStatus(
            status="AMBER",
            message=f"Query p95 latency {p95:.0f}ms (>{THRESHOLDS['query_p95_warning_ms']}ms)",
            metric_value=p95,
            threshold=THRESHOLDS["query_p95_warning_ms"]
        )

    p50 = metrics.query_p50()
    return HealthStatus(
        status="GREEN",
        message=f"Query performance good (p50: {p50:.0f}ms, p95: {p95:.0f}ms)",
        metric_value=p50
    )


def check_cache_health(metrics: ResolverMetrics) -> HealthStatus:
    """
    Check cache effectiveness.

    Monitors cache hit rate, size, and invalidation patterns.

    Returns:
        HealthStatus with GREEN/AMBER/RED status
    """
    hit_rate = metrics.cache_hit_rate()
    total_requests = metrics.cache_hits + metrics.cache_misses

    if total_requests < 10:
        return HealthStatus(
            status="AMBER",
            message=f"Insufficient cache data ({total_requests} requests)",
            metric_value=hit_rate
        )

    if hit_rate < THRESHOLDS["cache_hit_rate_critical"]:
        return HealthStatus(
            status="RED",
            message=f"Cache hit rate {hit_rate:.1%} (<{THRESHOLDS['cache_hit_rate_critical']:.0%})",
            metric_value=hit_rate,
            threshold=THRESHOLDS["cache_hit_rate_critical"]
        )
    elif hit_rate < THRESHOLDS["cache_hit_rate_warning"]:
        return HealthStatus(
            status="AMBER",
            message=f"Cache hit rate {hit_rate:.1%} (<{THRESHOLDS['cache_hit_rate_warning']:.0%})",
            metric_value=hit_rate,
            threshold=THRESHOLDS["cache_hit_rate_warning"]
        )

    return HealthStatus(
        status="GREEN",
        message=f"Cache effective (hit rate: {hit_rate:.1%}, size: {metrics.cache_size})",
        metric_value=hit_rate
    )


def check_error_rate(metrics: ResolverMetrics) -> HealthStatus:
    """
    Check error frequency and patterns.

    Monitors failure.emit frequency and error types.

    Returns:
        HealthStatus with GREEN/AMBER/RED status
    """
    error_rate = metrics.error_rate()

    if metrics.query_count < 10:
        return HealthStatus(
            status="AMBER",
            message=f"Insufficient query data ({metrics.query_count} queries)",
            metric_value=error_rate
        )

    if error_rate > THRESHOLDS["error_rate_critical"]:
        top_error = max(metrics.errors_by_type.items(), key=lambda x: x[1])[0] if metrics.errors_by_type else "unknown"
        return HealthStatus(
            status="RED",
            message=f"Error rate {error_rate:.1%} (>{THRESHOLDS['error_rate_critical']:.0%}, top: {top_error})",
            metric_value=error_rate,
            threshold=THRESHOLDS["error_rate_critical"]
        )
    elif error_rate > THRESHOLDS["error_rate_warning"]:
        return HealthStatus(
            status="AMBER",
            message=f"Error rate {error_rate:.1%} (>{THRESHOLDS['error_rate_warning']:.0%})",
            metric_value=error_rate,
            threshold=THRESHOLDS["error_rate_warning"]
        )

    return HealthStatus(
        status="GREEN",
        message=f"Error rate healthy ({error_rate:.1%}, {metrics.error_count}/{metrics.query_count})",
        metric_value=error_rate
    )


def check_resource_usage(metrics: ResolverMetrics) -> HealthStatus:
    """
    Check resource consumption (memory, connections).

    Returns:
        HealthStatus with GREEN/AMBER/RED status
    """
    memory_mb = metrics.memory_mb

    if memory_mb > THRESHOLDS["memory_critical_mb"]:
        return HealthStatus(
            status="RED",
            message=f"Memory usage {memory_mb:.0f}MB (>{THRESHOLDS['memory_critical_mb']}MB)",
            metric_value=memory_mb,
            threshold=THRESHOLDS["memory_critical_mb"]
        )
    elif memory_mb > THRESHOLDS["memory_warning_mb"]:
        return HealthStatus(
            status="AMBER",
            message=f"Memory usage {memory_mb:.0f}MB (>{THRESHOLDS['memory_warning_mb']}MB)",
            metric_value=memory_mb,
            threshold=THRESHOLDS["memory_warning_mb"]
        )

    return HealthStatus(
        status="GREEN",
        message=f"Resource usage healthy (memory: {memory_mb:.0f}MB, connections: {metrics.connection_count})",
        metric_value=memory_mb
    )


# ============================================================================
# Comprehensive Health Assessment
# ============================================================================

@dataclass
class HealthReport:
    """Comprehensive health report for a resolver"""
    org: str
    resolver_type: str
    timestamp: datetime

    uptime: HealthStatus
    query_performance: HealthStatus
    cache_health: HealthStatus
    error_rate: HealthStatus
    resource_usage: HealthStatus

    def overall_status(self) -> str:
        """
        Calculate overall status (worst of all checks).

        RED > AMBER > GREEN
        """
        statuses = [
            self.uptime.status,
            self.query_performance.status,
            self.cache_health.status,
            self.error_rate.status,
            self.resource_usage.status
        ]

        if "RED" in statuses:
            return "RED"
        elif "AMBER" in statuses:
            return "AMBER"
        else:
            return "GREEN"

    def to_dict(self) -> dict:
        """Serialize to dict for JSON export"""
        return {
            "org": self.org,
            "resolver_type": self.resolver_type,
            "timestamp": self.timestamp.isoformat(),
            "overall_status": self.overall_status(),
            "checks": {
                "uptime": self.uptime.to_dict(),
                "query_performance": self.query_performance.to_dict(),
                "cache_health": self.cache_health.to_dict(),
                "error_rate": self.error_rate.to_dict(),
                "resource_usage": self.resource_usage.to_dict()
            }
        }


def assess_resolver_health(metrics: ResolverMetrics) -> HealthReport:
    """
    Run all health checks and generate comprehensive report.

    Args:
        metrics: Current resolver metrics

    Returns:
        HealthReport with all check results
    """
    return HealthReport(
        org=metrics.org,
        resolver_type=metrics.resolver_type,
        timestamp=datetime.utcnow(),
        uptime=check_resolver_uptime(metrics),
        query_performance=check_query_performance(metrics),
        cache_health=check_cache_health(metrics),
        error_rate=check_error_rate(metrics),
        resource_usage=check_resource_usage(metrics)
    )


# ============================================================================
# Metrics Collection (to be wired to resolvers)
# ============================================================================

class ResolverHealthMonitor:
    """
    Collects and tracks resolver health metrics.

    Will be wired to:
    - Membrane bus (for event-driven metrics collection)
    - L2 resolvers (for telemetry injection)
    - Alert system (for threshold violations)
    """

    def __init__(self):
        self.metrics: Dict[Tuple[str, str], ResolverMetrics] = {}
        self.alerts_sent: Dict[str, datetime] = {}
        self.alert_cooldown_seconds = 300  # 5 minutes between duplicate alerts

    def get_or_create_metrics(self, org: str, resolver_type: str) -> ResolverMetrics:
        """Get metrics for a resolver, creating if needed"""
        key = (org, resolver_type)
        if key not in self.metrics:
            self.metrics[key] = ResolverMetrics(org=org, resolver_type=resolver_type)
        return self.metrics[key]

    def record_query(self, org: str, resolver_type: str, latency_ms: float, success: bool = True):
        """Record a query execution"""
        metrics = self.get_or_create_metrics(org, resolver_type)
        metrics.query_count += 1
        metrics.query_latencies.append(latency_ms)
        if not success:
            metrics.error_count += 1

    def record_cache_access(self, org: str, resolver_type: str, hit: bool):
        """Record a cache access (hit or miss)"""
        metrics = self.get_or_create_metrics(org, resolver_type)
        if hit:
            metrics.cache_hits += 1
        else:
            metrics.cache_misses += 1

    def record_error(self, org: str, resolver_type: str, error_type: str):
        """Record an error occurrence"""
        metrics = self.get_or_create_metrics(org, resolver_type)
        metrics.error_count += 1
        metrics.errors_by_type[error_type] += 1

    def update_process_status(self, org: str, resolver_type: str, running: bool, memory_mb: float = 0.0):
        """Update resolver process status"""
        metrics = self.get_or_create_metrics(org, resolver_type)
        metrics.process_running = running
        metrics.memory_mb = memory_mb
        if running:
            metrics.last_seen = datetime.utcnow()

    def assess_all(self) -> List[HealthReport]:
        """Run health checks on all monitored resolvers"""
        reports = []
        for metrics in self.metrics.values():
            report = assess_resolver_health(metrics)
            reports.append(report)

            # Check if alerts needed
            self._check_alerts(report)

        return reports

    def _check_alerts(self, report: HealthReport):
        """Check if alerts should be sent for this report"""
        # Implementation will be added when alert system is wired
        # For now, just log RED status
        if report.overall_status() == "RED":
            logger.error(f"CRITICAL: {report.org}/{report.resolver_type} health is RED")
            for check_name, check_result in [
                ("uptime", report.uptime),
                ("query_performance", report.query_performance),
                ("cache_health", report.cache_health),
                ("error_rate", report.error_rate),
                ("resource_usage", report.resource_usage)
            ]:
                if check_result.status == "RED":
                    logger.error(f"  - {check_name}: {check_result.message}")


# ============================================================================
# Testing / Demo
# ============================================================================

def demo_health_checks():
    """Demonstrate health monitoring with sample data"""
    print("=" * 80)
    print("Resolver Health Monitoring Demo")
    print("=" * 80)

    # Create sample metrics (simulating a healthy resolver)
    healthy_metrics = ResolverMetrics(org="scopelock", resolver_type="view_resolver")
    healthy_metrics.process_running = True
    healthy_metrics.uptime_seconds = 3600
    healthy_metrics.query_count = 100
    healthy_metrics.query_latencies.extend([50, 75, 100, 120, 150] * 20)  # p95 ~150ms
    healthy_metrics.cache_hits = 80
    healthy_metrics.cache_misses = 20
    healthy_metrics.error_count = 2
    healthy_metrics.memory_mb = 256

    report = assess_resolver_health(healthy_metrics)
    print(f"\nHealthy Resolver: {report.org}/{report.resolver_type}")
    print(f"Overall Status: {report.overall_status()}")
    print(json.dumps(report.to_dict(), indent=2))

    # Create sample metrics (simulating an unhealthy resolver)
    print("\n" + "=" * 80)
    unhealthy_metrics = ResolverMetrics(org="scopelock", resolver_type="view_resolver")
    unhealthy_metrics.process_running = True
    unhealthy_metrics.uptime_seconds = 3600
    unhealthy_metrics.query_count = 100
    unhealthy_metrics.query_latencies.extend([500, 1000, 2000, 3500, 5000] * 20)  # p95 ~5000ms
    unhealthy_metrics.cache_hits = 20
    unhealthy_metrics.cache_misses = 80
    unhealthy_metrics.error_count = 15
    unhealthy_metrics.errors_by_type["timeout"] = 10
    unhealthy_metrics.errors_by_type["validation_failed"] = 5
    unhealthy_metrics.memory_mb = 1200

    report = assess_resolver_health(unhealthy_metrics)
    print(f"\nUnhealthy Resolver: {report.org}/{report.resolver_type}")
    print(f"Overall Status: {report.overall_status()}")
    print(json.dumps(report.to_dict(), indent=2))


if __name__ == "__main__":
    # Run demo
    demo_health_checks()
