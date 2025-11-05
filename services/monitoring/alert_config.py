"""
Alert Configuration and Management for Resolver Health Monitoring

Defines alert conditions, channels, and dispatch logic.

Alert Levels:
- 🔴 CRITICAL: Immediate action required (resolver offline, high error rate)
- 🟠 WARNING: Attention needed (degraded performance, cache issues)
- 🟡 INFO: Informational (resource usage trends)

Alert Channels:
- Slack webhook (immediate notifications)
- Email (digest and critical alerts)
- failure.emit event (protocol-native, for consciousness substrate)
- File log (for auditing)

Author: Vera (Chief Validator)
Date: 2025-11-04
"""

import json
import asyncio
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import aiohttp
from pathlib import Path

logger = logging.getLogger(__name__)


# ============================================================================
# Alert Levels and Conditions
# ============================================================================

class AlertLevel(Enum):
    """Alert severity levels"""
    CRITICAL = "CRITICAL"  # 🔴 Immediate action required
    WARNING = "WARNING"    # 🟠 Attention needed
    INFO = "INFO"          # 🟡 Informational


@dataclass
class AlertCondition:
    """Definition of an alert condition"""
    name: str
    level: AlertLevel
    description: str
    check_field: str  # Field in HealthReport to check (e.g., "uptime.status")
    trigger_value: str  # Value that triggers alert (e.g., "RED")
    cooldown_minutes: int = 5  # Minimum time between duplicate alerts


# Alert condition definitions
ALERT_CONDITIONS = [
    # CRITICAL alerts
    AlertCondition(
        name="resolver_offline",
        level=AlertLevel.CRITICAL,
        description="Resolver process offline for >5 minutes",
        check_field="uptime.status",
        trigger_value="RED",
        cooldown_minutes=5
    ),
    AlertCondition(
        name="high_error_rate",
        level=AlertLevel.CRITICAL,
        description="Error rate >10% for 5 minutes",
        check_field="error_rate.status",
        trigger_value="RED",
        cooldown_minutes=5
    ),
    AlertCondition(
        name="severe_latency",
        level=AlertLevel.CRITICAL,
        description="Query p95 >3000ms",
        check_field="query_performance.status",
        trigger_value="RED",
        cooldown_minutes=10
    ),

    # WARNING alerts
    AlertCondition(
        name="degraded_performance",
        level=AlertLevel.WARNING,
        description="Query p95 >1000ms for 10 minutes",
        check_field="query_performance.status",
        trigger_value="AMBER",
        cooldown_minutes=10
    ),
    AlertCondition(
        name="low_cache_hit_rate",
        level=AlertLevel.WARNING,
        description="Cache hit rate <50% for 30 minutes",
        check_field="cache_health.status",
        trigger_value="AMBER",
        cooldown_minutes=30
    ),
    AlertCondition(
        name="elevated_error_rate",
        level=AlertLevel.WARNING,
        description="Error rate >5%",
        check_field="error_rate.status",
        trigger_value="AMBER",
        cooldown_minutes=10
    ),

    # INFO alerts
    AlertCondition(
        name="high_memory_usage",
        level=AlertLevel.INFO,
        description="Memory usage >80%",
        check_field="resource_usage.status",
        trigger_value="AMBER",
        cooldown_minutes=30
    ),
]


# ============================================================================
# Alert Channels
# ============================================================================

@dataclass
class AlertChannel:
    """Configuration for an alert delivery channel"""
    name: str
    enabled: bool = True
    min_level: AlertLevel = AlertLevel.WARNING  # Minimum level to send


class SlackAlertChannel:
    """Send alerts to Slack via webhook"""

    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url
        self.enabled = webhook_url is not None

    async def send(self, alert: 'Alert'):
        """Send alert to Slack"""
        if not self.enabled:
            logger.debug(f"Slack alerts disabled, skipping: {alert.title}")
            return

        emoji = {
            AlertLevel.CRITICAL: ":red_circle:",
            AlertLevel.WARNING: ":warning:",
            AlertLevel.INFO: ":information_source:"
        }[alert.level]

        message = {
            "text": f"{emoji} *{alert.title}*",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"{emoji} {alert.title}"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": f"*Resolver:*\n{alert.org}/{alert.resolver_type}"},
                        {"type": "mrkdwn", "text": f"*Level:*\n{alert.level.value}"},
                        {"type": "mrkdwn", "text": f"*Condition:*\n{alert.condition}"},
                        {"type": "mrkdwn", "text": f"*Time:*\n{alert.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"}
                    ]
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Details:*\n{alert.message}"
                    }
                }
            ]
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.webhook_url, json=message, timeout=10) as response:
                    if response.status != 200:
                        logger.error(f"Slack webhook failed: {response.status}")
        except Exception as e:
            logger.error(f"Failed to send Slack alert: {e}")


class EmailAlertChannel:
    """Send alerts via email (digest or immediate)"""

    def __init__(self, smtp_config: Optional[Dict] = None):
        self.smtp_config = smtp_config
        self.enabled = smtp_config is not None

    async def send(self, alert: 'Alert'):
        """Send alert via email"""
        if not self.enabled:
            logger.debug(f"Email alerts disabled, skipping: {alert.title}")
            return

        # Email sending implementation (to be wired to SMTP)
        logger.info(f"Email alert: {alert.title} (email sending not yet wired)")


class FailureEmitChannel:
    """Send alerts as failure.emit events (protocol-native)"""

    def __init__(self, membrane_bus=None):
        self.membrane_bus = membrane_bus
        self.enabled = membrane_bus is not None

    async def send(self, alert: 'Alert'):
        """Send alert as failure.emit event"""
        if not self.enabled:
            logger.debug(f"failure.emit disabled (membrane bus not wired), skipping: {alert.title}")
            return

        # Emit failure event (to be wired to membrane bus)
        event = {
            "event_type": "failure.emit",
            "severity": alert.level.value.lower(),
            "component": f"resolver_health/{alert.org}/{alert.resolver_type}",
            "code_location": "services/monitoring/resolver_health.py",
            "message": alert.message,
            "suggestion": alert.get_suggestion(),
            "timestamp": alert.timestamp.isoformat()
        }

        logger.info(f"failure.emit: {alert.title} (membrane bus not yet wired)")
        # await self.membrane_bus.inject("failure.emit", event)


class FileLogChannel:
    """Write alerts to file for auditing"""

    def __init__(self, log_file: Path):
        self.log_file = log_file
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    async def send(self, alert: 'Alert'):
        """Write alert to log file"""
        try:
            with open(self.log_file, 'a') as f:
                f.write(json.dumps({
                    "timestamp": alert.timestamp.isoformat(),
                    "level": alert.level.value,
                    "org": alert.org,
                    "resolver_type": alert.resolver_type,
                    "condition": alert.condition,
                    "title": alert.title,
                    "message": alert.message
                }) + "\n")
        except Exception as e:
            logger.error(f"Failed to write alert to file: {e}")


# ============================================================================
# Alert Definition
# ============================================================================

@dataclass
class Alert:
    """An alert to be dispatched"""
    level: AlertLevel
    org: str
    resolver_type: str
    condition: str
    title: str
    message: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metric_value: Optional[float] = None
    threshold: Optional[float] = None

    def get_suggestion(self) -> str:
        """Get remediation suggestion based on condition"""
        suggestions = {
            "resolver_offline": "Check if resolver process crashed. Restart via supervisor or manual intervention.",
            "high_error_rate": "Check resolver logs for error patterns. Investigate FalkorDB connectivity or query issues.",
            "severe_latency": "Check FalkorDB load. Consider query optimization or scaling resolver instances.",
            "degraded_performance": "Monitor query patterns. Consider cache warming or index optimization.",
            "low_cache_hit_rate": "Review cache invalidation patterns. Check if surgical invalidation is too aggressive.",
            "elevated_error_rate": "Review error types in resolver logs. Check for transient vs persistent failures.",
            "high_memory_usage": "Check for memory leaks. Consider restarting resolver or increasing memory limits."
        }
        return suggestions.get(self.condition, "Check resolver health dashboard and logs for details.")


# ============================================================================
# Alert Manager
# ============================================================================

class AlertManager:
    """Manages alert dispatch and cooldown tracking"""

    def __init__(self):
        self.channels: List = []
        self.alert_history: Dict[str, datetime] = {}  # alert_key -> last_sent_time

    def add_channel(self, channel):
        """Add an alert channel"""
        self.channels.append(channel)

    def _should_send_alert(self, alert: Alert, condition: AlertCondition) -> bool:
        """Check if alert should be sent (considering cooldown)"""
        alert_key = f"{alert.org}/{alert.resolver_type}/{condition.name}"

        # Check cooldown
        if alert_key in self.alert_history:
            last_sent = self.alert_history[alert_key]
            cooldown_delta = timedelta(minutes=condition.cooldown_minutes)
            if datetime.utcnow() - last_sent < cooldown_delta:
                logger.debug(f"Alert {alert_key} in cooldown, skipping")
                return False

        return True

    async def dispatch(self, alert: Alert, condition: AlertCondition):
        """Dispatch alert to all appropriate channels"""
        if not self._should_send_alert(alert, condition):
            return

        # Record alert sent
        alert_key = f"{alert.org}/{alert.resolver_type}/{condition.name}"
        self.alert_history[alert_key] = datetime.utcnow()

        # Send to all channels
        for channel in self.channels:
            # Check if channel accepts this alert level
            if hasattr(channel, 'min_level'):
                # Convert to priority: CRITICAL=3, WARNING=2, INFO=1
                alert_priority = {"CRITICAL": 3, "WARNING": 2, "INFO": 1}[alert.level.value]
                channel_priority = {"CRITICAL": 3, "WARNING": 2, "INFO": 1}[channel.min_level.value]
                if alert_priority < channel_priority:
                    continue

            try:
                await channel.send(alert)
            except Exception as e:
                logger.error(f"Failed to send alert via {channel.__class__.__name__}: {e}")


# ============================================================================
# Alert Evaluation
# ============================================================================

def evaluate_health_report(report: dict, conditions: List[AlertCondition]) -> List[tuple[Alert, AlertCondition]]:
    """
    Evaluate health report against alert conditions.

    Args:
        report: HealthReport as dict
        conditions: List of AlertCondition to check

    Returns:
        List of (Alert, AlertCondition) tuples for conditions that triggered
    """
    alerts = []

    for condition in conditions:
        # Navigate to check field (e.g., "uptime.status")
        field_path = condition.check_field.split('.')
        value = report.get("checks", {})

        for part in field_path:
            if isinstance(value, dict):
                value = value.get(part)
            else:
                break

        # Check if condition triggered
        if value == condition.trigger_value:
            # Extract metric details
            check_name = field_path[0]
            check_data = report["checks"].get(check_name, {})

            alert = Alert(
                level=condition.level,
                org=report["org"],
                resolver_type=report["resolver_type"],
                condition=condition.name,
                title=f"{condition.level.value}: {condition.description}",
                message=check_data.get("message", condition.description),
                metric_value=check_data.get("metric_value"),
                threshold=check_data.get("threshold")
            )
            alerts.append((alert, condition))

    return alerts


# ============================================================================
# Example Usage / Testing
# ============================================================================

async def demo_alerts():
    """Demonstrate alert system"""
    print("=" * 80)
    print("Alert System Demo")
    print("=" * 80)

    # Create alert manager
    manager = AlertManager()

    # Add channels
    manager.add_channel(FileLogChannel(Path("/tmp/graphcare_alerts.log")))
    manager.add_channel(SlackAlertChannel(webhook_url=None))  # Disabled (no URL)
    manager.add_channel(FailureEmitChannel(membrane_bus=None))  # Disabled (no bus)

    # Simulate unhealthy health report
    unhealthy_report = {
        "org": "scopelock",
        "resolver_type": "view_resolver",
        "timestamp": datetime.utcnow().isoformat(),
        "overall_status": "RED",
        "checks": {
            "uptime": {"status": "RED", "message": "Resolver offline for 360s (>300s)", "metric_value": 360, "threshold": 300},
            "query_performance": {"status": "RED", "message": "Query p95 latency 5000ms (>3000ms)", "metric_value": 5000, "threshold": 3000},
            "cache_health": {"status": "RED", "message": "Cache hit rate 20.0% (<30%)", "metric_value": 0.2, "threshold": 0.3},
            "error_rate": {"status": "RED", "message": "Error rate 15.0% (>10%, top: timeout)", "metric_value": 0.15, "threshold": 0.1},
            "resource_usage": {"status": "GREEN", "message": "Resource usage healthy", "metric_value": 256}
        }
    }

    # Evaluate conditions
    alerts = evaluate_health_report(unhealthy_report, ALERT_CONDITIONS)
    print(f"\nFound {len(alerts)} alert conditions triggered:\n")

    # Dispatch alerts
    for alert, condition in alerts:
        print(f"🔴 {alert.level.value}: {alert.title}")
        print(f"   Condition: {condition.name}")
        print(f"   Message: {alert.message}")
        print(f"   Suggestion: {alert.get_suggestion()}\n")

        await manager.dispatch(alert, condition)

    print(f"Alerts written to /tmp/graphcare_alerts.log")
    print(f"(Slack/email/failure.emit disabled - not yet wired)")


if __name__ == "__main__":
    asyncio.run(demo_alerts())
