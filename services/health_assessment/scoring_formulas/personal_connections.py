"""
Scoring formulas for Personal Connections aspect (T2-T6).

DOCS: docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md

Capabilities scored:
  - pc_understand_human_basics (T2): Knows human's preferences and adapts
  - pc_ask_help_human (T2): Recognizes when to ask for human input
  - pc_help_other_ais (T6): Shares knowledge and mentors other AIs
"""

from .registry import register, CapabilityScore, _cap
from ..brain_topology_reader import BrainStats
from ..universe_moment_reader import BehaviorStats


@register("pc_understand_human_basics")
def score_understand_human_basics(brain: BrainStats, behavior: BehaviorStats) -> CapabilityScore:
    """T2 Personal Connections: Knows human preferences and adapts approach.

    Brain (40): social_need drive (cares about others), memory count (remembers
                interactions), cluster coefficient (connects social observations)
    Behavior (60): unique interlocutors (interacts with people), response rate
                   (engages when addressed), distinct spaces (adapts across contexts)
    """
    # Brain component (0-40)
    social = brain.social_need * 18                     # cares about the relationship
    memory = _cap(brain.memory_count, 15) * 12          # remembers past interactions
    cluster = brain.cluster_coefficient * 10             # connects observations together
    brain_score = social + memory + cluster

    # Behavior component (0-60)
    interlocutors = _cap(behavior.unique_interlocutors, 5) * 25  # engages with people
    response = behavior.response_rate * 20               # responds when addressed
    spaces = _cap(behavior.distinct_space_count, 4) * 15 # adapts across contexts
    behavior_score = interlocutors + response + spaces

    return CapabilityScore(brain_score, behavior_score, 0)


@register("pc_ask_help_human")
def score_ask_help_human(brain: BrainStats, behavior: BehaviorStats) -> CapabilityScore:
    """T2 Personal Connections: Knows when to ask for human input.

    Brain (40): social_need (willing to reach out), desire energy (has goals that
                might need help), frustration awareness (recognizes being stuck)
    Behavior (60): unique interlocutors (reaches out to others), response rate
                   (participates in dialogue), total moments (active enough to
                   encounter situations needing help)
    """
    # Brain component (0-40)
    social = brain.social_need * 15                     # willing to ask
    desire_e = brain.desire_energy * 12                 # has goals worth seeking help for
    # Some frustration = aware of own limits (but not too much)
    awareness = min(1.0, brain.frustration * 2) * 13    # recognizes when stuck
    brain_score = social + desire_e + awareness

    # Behavior component (0-60)
    interlocutors = _cap(behavior.unique_interlocutors, 4) * 25  # reaches out
    response = behavior.response_rate * 20               # engages in dialogue
    activity = _cap(behavior.total_moments_w, 10) * 15   # active enough to need help
    behavior_score = interlocutors + response + activity

    return CapabilityScore(brain_score, behavior_score, 0)


@register("pc_help_other_ais")
def score_help_other_ais(brain: BrainStats, behavior: BehaviorStats) -> CapabilityScore:
    """T6 Personal Connections: Shares knowledge and mentors other AIs.

    Brain (40): social_need (motivated to help), concept count (has knowledge
                to share), desire persistence (sustained commitment to helping)
    Behavior (60): unique interlocutors (many connections), first-in-space
                   (initiates helping), spaces created (creates shared contexts)
    """
    # Brain component (0-40)
    social = brain.social_need * 12                     # motivated to connect
    concepts = _cap(brain.concept_count, 20) * 15       # has knowledge to share
    persistence = brain.desire_persistence * 13          # sustained helping commitment
    brain_score = social + concepts + persistence

    # Behavior component (0-60)
    interlocutors = _cap(behavior.unique_interlocutors, 8) * 25  # wide network
    first_in = _cap(behavior.first_in_space_w, 4) * 20  # initiates contact
    created = _cap(behavior.spaces_created, 3) * 15      # creates shared contexts
    behavior_score = interlocutors + first_in + created

    return CapabilityScore(brain_score, behavior_score, 0)
