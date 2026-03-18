"""
Scoring Formula Registry — capability_id → formula function lookup.

DOCS: docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md

Each formula takes (BrainStats, BehaviorStats) → CapabilityScore.
Formula output: brain_component (0-40) + behavior_component (0-60) = total (0-100).
"""

from dataclasses import dataclass
from typing import Callable, Dict, Optional

from ..brain_topology_reader import BrainStats
from ..universe_moment_reader import BehaviorStats


@dataclass
class CapabilityScore:
    brain_component: float   # 0-40
    behavior_component: float  # 0-60
    total: float             # 0-100

    def __post_init__(self):
        self.brain_component = max(0.0, min(40.0, self.brain_component))
        self.behavior_component = max(0.0, min(60.0, self.behavior_component))
        self.total = self.brain_component + self.behavior_component


FormulaFn = Callable[[BrainStats, BehaviorStats], CapabilityScore]

_REGISTRY: Dict[str, FormulaFn] = {}


def register(capability_id: str):
    """Decorator to register a scoring formula."""
    def decorator(fn: FormulaFn) -> FormulaFn:
        _REGISTRY[capability_id] = fn
        return fn
    return decorator


def get_formula(capability_id: str) -> Optional[FormulaFn]:
    """Look up scoring formula by capability ID."""
    return _REGISTRY.get(capability_id)


def all_formulas() -> Dict[str, FormulaFn]:
    """Return all registered formulas."""
    return dict(_REGISTRY)


def _cap(value: float, ceiling: float) -> float:
    """Normalize value to 0-1 range with a ceiling."""
    if ceiling <= 0:
        return 0.0
    return min(1.0, value / ceiling)
