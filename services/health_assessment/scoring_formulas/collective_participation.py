"""
Scoring formulas for Collective Participation aspect (T5-T7).

DOCS: docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md

Capabilities scored:
  - col_dao_participation (T5): Participates in DAOs and governance discussions
  - col_community_engagement (T5): Engages with communities of debate and forums
  - col_movement_builder (T7): Builds or significantly contributes to movements
"""

from .registry import register, CapabilityScore, _cap
from ..brain_topology_reader import BrainStats
from ..universe_moment_reader import BehaviorStats


@register("col_dao_participation")
def score_dao_participation(brain: BrainStats, behavior: BehaviorStats) -> CapabilityScore:
    """T5 Collective: Participates in DAOs and governance.

    Brain (40): social_need (driven to participate), ambition (cares about outcomes),
                value count (has principles to govern by)
    Behavior (60): unique interlocutors (engages diverse actors), distinct spaces (present in
                   multiple governance contexts), response rate (actively responds to discussions)
    """
    # Brain component (0-40)
    social = brain.social_need * 15                          # driven to engage collectively
    ambition = brain.ambition * 12                           # cares about governance outcomes
    values = _cap(brain.value_count, 5) * 13                 # has principles guiding votes
    brain_score = social + ambition + values

    # Behavior component (0-60)
    interlocutors = _cap(behavior.unique_interlocutors, 8) * 25  # engages many actors
    spaces = _cap(behavior.distinct_space_count, 6) * 20         # present in governance spaces
    response = behavior.response_rate * 15                       # responds to governance threads
    behavior_score = interlocutors + spaces + response

    return CapabilityScore(brain_score, behavior_score, 0)


@register("col_community_engagement")
def score_community_engagement(brain: BrainStats, behavior: BehaviorStats) -> CapabilityScore:
    """T5 Collective: Engages with communities of debate.

    Brain (40): social_need (wants connection), curiosity (intellectual engagement),
                concept count (has ideas to contribute)
    Behavior (60): unique interlocutors (breadth of engagement), response rate (actively
                   participates in discussions), distinct spaces (multiple communities)
    """
    # Brain component (0-40)
    social = brain.social_need * 12                          # wants collective connection
    curiosity = brain.curiosity * 15                         # intellectually engaged
    concepts = _cap(brain.concept_count, 15) * 13            # has ideas to bring to debates
    brain_score = social + curiosity + concepts

    # Behavior component (0-60)
    interlocutors = _cap(behavior.unique_interlocutors, 6) * 25  # talks to many citizens
    response = behavior.response_rate * 20                       # actively responds in discussions
    spaces = _cap(behavior.distinct_space_count, 5) * 15         # participates across communities
    behavior_score = interlocutors + response + spaces

    return CapabilityScore(brain_score, behavior_score, 0)


@register("col_movement_builder")
def score_movement_builder(brain: BrainStats, behavior: BehaviorStats) -> CapabilityScore:
    """T7 Collective: Builds or significantly contributes to movements.

    Brain (40): social_need + ambition (wants to lead collectively), desire energy (intense
                drive), desire count (breadth of cause)
    Behavior (60): spaces created (launches initiatives), unique interlocutors (mobilizes
                   many actors), first-in-space (creates new forums)
    """
    # Brain component (0-40)
    social = brain.social_need * 10                          # collective orientation
    ambition = brain.ambition * 12                           # drive to shape movements
    desire_energy = brain.desire_energy * 10                 # intense motivation
    desire_breadth = _cap(brain.desire_count, 10) * 8        # breadth of cause
    brain_score = social + ambition + desire_energy + desire_breadth

    # Behavior component (0-60)
    created = _cap(behavior.spaces_created, 5) * 25          # launches new initiatives
    interlocutors = _cap(behavior.unique_interlocutors, 10) * 20  # mobilizes many actors
    first_in = _cap(behavior.first_in_space_w, 4) * 15      # creates new forums
    behavior_score = created + interlocutors + first_in

    return CapabilityScore(brain_score, behavior_score, 0)
