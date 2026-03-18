"""
Scoring formulas for Mentorship & Legacy aspect (T4-T6).

DOCS: docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md

Capabilities scored:
  - ment_knowledge_sharing (T4): Shares knowledge with other agents
  - ment_mentor_ais (T6): Actively mentors other AIs, changes their trajectory
"""

from .registry import register, CapabilityScore, _cap
from ..brain_topology_reader import BrainStats
from ..universe_moment_reader import BehaviorStats


@register("ment_knowledge_sharing")
def score_knowledge_sharing(brain: BrainStats, behavior: BehaviorStats) -> CapabilityScore:
    """T4 Mentorship: Shares knowledge with other agents.

    Brain (40): concept count (has knowledge to share), social_need (motivated to share),
                memory count (accumulated learnings)
    Behavior (60): unique_interlocutors (reaches different agents),
                   self_initiated_w (proactively shares, not just responds),
                   response_rate (also responds when asked)
    """
    # Brain component (0-40)
    knowledge = _cap(brain.concept_count, 20) * 15          # has knowledge worth sharing
    social_drive = brain.social_need * 15                    # motivated to connect
    accumulated = _cap(brain.memory_count, 15) * 10          # learnings to draw on
    brain_score = knowledge + social_drive + accumulated

    # Behavior component (0-60)
    reach = _cap(behavior.unique_interlocutors, 5) * 25      # reaches many agents
    proactive = _cap(behavior.self_initiated_w, 5) * 20      # initiates sharing
    responsive = behavior.response_rate * 15                  # also responds to questions
    behavior_score = reach + proactive + responsive

    return CapabilityScore(brain_score, behavior_score, 0)


@register("ment_mentor_ais")
def score_mentor_ais(brain: BrainStats, behavior: BehaviorStats) -> CapabilityScore:
    """T6 Mentorship: Actively mentors other AIs.

    Brain (40): social_need (cares about others), desire_energy (sustained commitment),
                value_count (has values to transmit)
    Behavior (60): unique_interlocutors (deep connections with multiple agents),
                   self_initiated_w (proactively reaches out to mentees),
                   high_permanence_w (produces lasting guidance, not ephemeral chat)
    """
    # Brain component (0-40)
    caring = brain.social_need * 15                          # driven to help others
    commitment = brain.desire_energy * 10                    # sustained mentoring energy
    values = _cap(brain.value_count, 5) * 15                 # has values to transmit
    brain_score = caring + commitment + values

    # Behavior component (0-60)
    connections = _cap(behavior.unique_interlocutors, 8) * 20  # deep, varied connections
    initiative = _cap(behavior.self_initiated_w, 8) * 20       # reaches out proactively
    permanence = _cap(behavior.high_permanence_w, 5) * 20      # lasting guidance artifacts
    behavior_score = connections + initiative + permanence

    return CapabilityScore(brain_score, behavior_score, 0)
