"""
Scoring formulas for Communication aspect (T1-T3).

DOCS: docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md

Capabilities scored:
  - comm_status_updates (T2): Keeps stakeholders informed
  - comm_help_request (T1): Asks for help when stuck
  - comm_coordinate (T3): Coordinates multi-agent work
"""

from .registry import register, CapabilityScore, _cap
from ..brain_topology_reader import BrainStats
from ..universe_moment_reader import BehaviorStats


@register("comm_status_updates")
def score_status_updates(brain: BrainStats, behavior: BehaviorStats) -> CapabilityScore:
    """T2 Communication: Keeps people informed.

    Brain (40): social_need drive, recency
    Behavior (60): total moments, unique interlocutors, distinct spaces
    """
    social = brain.social_need * 20
    recency = brain.recency_moment * 10
    low_frustration = (1.0 - brain.frustration) * 10
    brain_score = social + recency + low_frustration

    activity = _cap(behavior.total_moments_w, 15) * 20
    interlocutors = _cap(behavior.unique_interlocutors, 5) * 25
    spaces = _cap(behavior.distinct_space_count, 5) * 15
    behavior_score = activity + interlocutors + spaces

    return CapabilityScore(brain_score, behavior_score, 0)


@register("comm_help_request")
def score_help_request(brain: BrainStats, behavior: BehaviorStats) -> CapabilityScore:
    """T1 Communication: Asks for help when stuck.

    Brain (40): social_need (willing to reach out), low frustration (doesn't suffer silently)
    Behavior (60): response rate (engages with others), interlocutors
    """
    social = brain.social_need * 15
    awareness = _cap(brain.frustration, 0.3) * 15  # some frustration = aware of limits
    recency = brain.recency_moment * 10
    brain_score = social + awareness + recency

    response = behavior.response_rate * 20
    interlocutors = _cap(behavior.unique_interlocutors, 4) * 25
    activity = _cap(behavior.total_moments_w, 8) * 15
    behavior_score = response + interlocutors + activity

    return CapabilityScore(brain_score, behavior_score, 0)


@register("comm_coordinate")
def score_coordinate(brain: BrainStats, behavior: BehaviorStats) -> CapabilityScore:
    """T3 Communication: Coordinates multi-agent work.

    Brain (40): social_need, ambition, process count
    Behavior (60): unique interlocutors, spaces, first-in-space
    """
    social = brain.social_need * 10
    ambition = brain.ambition * 15
    process = _cap(brain.process_count, 8) * 15
    brain_score = social + ambition + process

    interlocutors = _cap(behavior.unique_interlocutors, 8) * 25
    spaces = _cap(behavior.distinct_space_count, 6) * 20
    first_in = _cap(behavior.first_in_space_w, 3) * 15
    behavior_score = interlocutors + spaces + first_in

    return CapabilityScore(brain_score, behavior_score, 0)
