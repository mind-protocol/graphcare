"""
Scoring formulas for Ethics & Values aspect (T1-T4).

DOCS: docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md

Capabilities scored:
  - eth_apply_rules (T1): Consistently applies protocol values
  - eth_implement_systems (T4): Creates systems that support ethical behavior
"""

from .registry import register, CapabilityScore, _cap
from ..brain_topology_reader import BrainStats
from ..universe_moment_reader import BehaviorStats


@register("eth_apply_rules")
def score_apply_rules(brain: BrainStats, behavior: BehaviorStats) -> CapabilityScore:
    """T1 Ethics: Consistently applies the values and rules of Mind Protocol.

    Brain (40): value count (has internalized values),
                low frustration (values don't erode under pressure)
    Behavior (60): response rate (engages with others respectfully),
                   unique interlocutors (applies values across many relationships)
    """
    # Brain component (0-40)
    values = _cap(brain.value_count, 8) * 25            # has internalized protocol values
    low_frustration = (1.0 - brain.frustration) * 15    # values hold under pressure
    brain_score = values + low_frustration

    # Behavior component (0-60)
    responsiveness = behavior.response_rate * 30         # engages respectfully with others
    breadth = _cap(behavior.unique_interlocutors, 8) * 30  # applies values broadly
    behavior_score = responsiveness + breadth

    return CapabilityScore(brain_score, behavior_score, 0)


@register("eth_implement_systems")
def score_implement_systems(brain: BrainStats, behavior: BehaviorStats) -> CapabilityScore:
    """T4 Ethics: Creates systems that make it easier to follow ethical principles.

    Brain (40): value count (deep understanding of values to encode),
                low frustration (systemic thinking requires calm clarity)
    Behavior (60): unique interlocutors (systems serve many people),
                   response rate (listens to what others need)
    """
    # Brain component (0-40)
    values = _cap(brain.value_count, 10) * 25           # deep value understanding to encode
    low_frustration = (1.0 - brain.frustration) * 15    # systemic work needs calm clarity
    brain_score = values + low_frustration

    # Behavior component (0-60)
    breadth = _cap(behavior.unique_interlocutors, 10) * 35  # systems serve many agents
    responsiveness = behavior.response_rate * 25             # listens to community needs
    behavior_score = breadth + responsiveness

    return CapabilityScore(brain_score, behavior_score, 0)
