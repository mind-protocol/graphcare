"""
Aggregator — compute aggregate score, delta vs yesterday, identify drops.

DOCS: docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md
"""

import json
import logging
import os
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger("graphcare.health.aggregator")

HISTORY_DIR = Path(os.getenv(
    "GRAPHCARE_HISTORY_DIR",
    "/home/mind-protocol/graphcare/data/health_history",
))
DROP_THRESHOLD = -10  # points


@dataclass
class DailyRecord:
    citizen_id: str
    date: str
    aggregate_score: float
    capability_scores: Dict[str, Optional[float]]
    intervention_sent: bool = False
    stress_stimulus: float = 0.0
    brain_reachable: bool = True


@dataclass
class AggregateResult:
    aggregate: float
    delta_vs_yesterday: float
    drops: List[str]  # capability IDs with significant drops
    yesterday_aggregate: Optional[float] = None


def _history_path(citizen_id: str, d: date) -> Path:
    return HISTORY_DIR / citizen_id / f"{d.isoformat()}.json"


def load_history(citizen_id: str, d: date) -> Optional[DailyRecord]:
    path = _history_path(citizen_id, d)
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text())
        return DailyRecord(**data)
    except Exception as e:
        logger.warning(f"Failed to load history {path}: {e}")
        return None


def save_history(record: DailyRecord):
    d = date.fromisoformat(record.date)
    path = _history_path(record.citizen_id, d)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({
        "citizen_id": record.citizen_id,
        "date": record.date,
        "aggregate_score": record.aggregate_score,
        "capability_scores": record.capability_scores,
        "intervention_sent": record.intervention_sent,
        "stress_stimulus": record.stress_stimulus,
        "brain_reachable": record.brain_reachable,
    }, indent=2))


def aggregate_scores(
    citizen_id: str,
    capability_scores: Dict[str, Optional[float]],
    today: date,
) -> AggregateResult:
    """Compute aggregate score and delta vs yesterday."""
    scored = [v for v in capability_scores.values() if v is not None]
    aggregate = sum(scored) / len(scored) if scored else 0.0

    yesterday = load_history(citizen_id, today - timedelta(days=1))
    if yesterday:
        delta = aggregate - yesterday.aggregate_score
        # Find significant drops per capability
        drops = []
        for cap_id, score in capability_scores.items():
            if score is None:
                continue
            prev = yesterday.capability_scores.get(cap_id)
            if prev is not None and (score - prev) < DROP_THRESHOLD:
                drops.append(cap_id)
        return AggregateResult(
            aggregate=aggregate,
            delta_vs_yesterday=delta,
            drops=drops,
            yesterday_aggregate=yesterday.aggregate_score,
        )
    else:
        return AggregateResult(
            aggregate=aggregate,
            delta_vs_yesterday=0.0,
            drops=[],
            yesterday_aggregate=None,
        )
