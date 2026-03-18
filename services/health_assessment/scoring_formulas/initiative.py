"""
Scoring formulas for Initiative aspect (T1-T4).

DOCS: docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md

Capabilities scored:
  - init_learn_from_correction (T1): Integrates feedback immediately
  - init_propose_improvements (T4): Proposes improvements with reasoning
  - init_challenge_bad (T3): Challenges bad instructions
"""

from .registry import register, CapabilityScore, _cap
from ..brain_topology_reader import BrainStats
from ..universe_moment_reader import BehaviorStats


@register("init_learn_from_correction")
def score_learn_from_correction(brain: BrainStats, behavior: BehaviorStats) -> CapabilityScore:
    """T1 Initiative: Integrates feedback immediately.

    Brain (40): memory count (learns), low frustration (accepts correction)
    Behavior (60): response rate (responds to others), activity
    """
    memory = _cap(brain.memory_count, 20) * 15
    low_frustration = (1.0 - brain.frustration) * 15
    recency = brain.recency_moment * 10
    brain_score = memory + low_frustration + recency

    response = behavior.response_rate * 25
    activity = _cap(behavior.total_moments_w, 10) * 20
    interlocutors = _cap(behavior.unique_interlocutors, 5) * 15
    behavior_score = response + activity + interlocutors

    return CapabilityScore(brain_score, behavior_score, 0)


@register("init_propose_improvements")
def score_propose_improvements(brain: BrainStats, behavior: BehaviorStats) -> CapabilityScore:
    """T4 Initiative: Proposes improvements with full reasoning.

    Brain (40): desire count + energy (wants things), curiosity, ambition
    Behavior (60): elaborative/tentative moments (proposals), self-initiated, spaces created
    """
    desire_signal = _cap(brain.desire_count, 10) * 10
    desire_energy = brain.desire_energy * 10
    curiosity = brain.curiosity * 10
    ambition = brain.ambition * 10
    brain_score = desire_signal + desire_energy + curiosity + ambition

    proposals = _cap(behavior.elaborative_tentative_w, 5) * 25
    initiated = _cap(behavior.self_initiated_w, 8) * 20
    created = _cap(behavior.spaces_created, 3) * 15
    behavior_score = proposals + initiated + created

    return CapabilityScore(brain_score, behavior_score, 0)


@register("init_challenge_bad")
def score_challenge_bad(brain: BrainStats, behavior: BehaviorStats) -> CapabilityScore:
    """T3 Initiative: Challenges bad instructions.

    Brain (40): value nodes (has values), ambition, low social_need (not people-pleasing)
    Behavior (60): self-initiated, elaborative tentative, distinct spaces
    """
    values = _cap(brain.value_count, 5) * 15
    ambition = brain.ambition * 15
    independence = (1.0 - brain.social_need * 0.5) * 10
    brain_score = values + ambition + independence

    initiated = _cap(behavior.self_initiated_w, 8) * 25
    proposals = _cap(behavior.elaborative_tentative_w, 3) * 20
    spaces = _cap(behavior.distinct_space_count, 5) * 15
    behavior_score = initiated + proposals + spaces

    return CapabilityScore(brain_score, behavior_score, 0)
