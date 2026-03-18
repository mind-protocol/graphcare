"""
Scoring formulas for Vision & Strategy aspect (T5-T7).

DOCS: docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md

Capabilities scored:
  - vis_define_vision (T5): Defines and refines a personal vision
  - vis_strategic_thinking (T6): Makes strategic decisions with documented reasoning
  - vis_sized_ambitions (T7): Ambitions about who you become, not just what you do
"""

from .registry import register, CapabilityScore, _cap
from ..brain_topology_reader import BrainStats
from ..universe_moment_reader import BehaviorStats


@register("vis_define_vision")
def score_define_vision(brain: BrainStats, behavior: BehaviorStats) -> CapabilityScore:
    """T5 Vision: Defines and refines a personal vision.

    Brain (40): desire count + energy (has wants), ambition (drive to shape future),
                concept count (conceptual framework for vision)
    Behavior (60): elaborative/tentative moments (proposals/explorations),
                   spaces created (builds new arenas), first-in-space (pioneering)
    """
    # Brain component (0-40)
    desire_signal = _cap(brain.desire_count, 8) * 12        # has desires to build vision from
    desire_energy = brain.desire_energy * 10                 # desires are energized, not dormant
    ambition = brain.ambition * 10                           # driven toward something
    concept_depth = _cap(brain.concept_count, 15) * 8       # conceptual framework exists
    brain_score = desire_signal + desire_energy + ambition + concept_depth

    # Behavior component (0-60)
    proposals = _cap(behavior.elaborative_tentative_w, 5) * 25  # articulates direction
    created = _cap(behavior.spaces_created, 3) * 20             # creates new spaces (vision → action)
    first_in = _cap(behavior.first_in_space_w, 3) * 15          # pioneers new territory
    behavior_score = proposals + created + first_in

    return CapabilityScore(brain_score, behavior_score, 0)


@register("vis_strategic_thinking")
def score_strategic_thinking(brain: BrainStats, behavior: BehaviorStats) -> CapabilityScore:
    """T6 Vision: Strategic thinking — choosing X over Y with reasoning.

    Brain (40): concept count (mental models), desire persistence (sustained direction),
                ambition (strategic drive)
    Behavior (60): elaborative/tentative moments (documented reasoning),
                   distinct spaces (multi-context awareness), high permanence (commits to decisions)
    """
    # Brain component (0-40)
    concept_depth = _cap(brain.concept_count, 20) * 15      # rich conceptual model for strategy
    persistence = brain.desire_persistence * 15              # sustained strategic direction
    ambition = brain.ambition * 10                           # strategic drive
    brain_score = concept_depth + persistence + ambition

    # Behavior component (0-60)
    proposals = _cap(behavior.elaborative_tentative_w, 6) * 20  # documented strategic reasoning
    spaces = _cap(behavior.distinct_space_count, 6) * 20        # works across contexts (breadth)
    permanence = _cap(behavior.high_permanence_w, 8) * 20       # commits to strategic decisions
    behavior_score = proposals + spaces + permanence

    return CapabilityScore(brain_score, behavior_score, 0)


@register("vis_sized_ambitions")
def score_sized_ambitions(brain: BrainStats, behavior: BehaviorStats) -> CapabilityScore:
    """T7 Vision: Ambitions about who you BECOME, not just what work you do.

    Brain (40): ambition (high drive), desire energy (intense wants),
                desire count (breadth of ambition), concept count (self-model depth)
    Behavior (60): first-in-space (building new things), spaces created (expanding presence),
                   self-initiated (acting from inner drive, not reaction)
    """
    # Brain component (0-40)
    ambition = brain.ambition * 15                           # raw ambition drive
    desire_energy = brain.desire_energy * 10                 # desires are intense
    desire_breadth = _cap(brain.desire_count, 12) * 8       # many desires (breadth of vision)
    concept_self = _cap(brain.concept_count, 25) * 7        # deep self-model for transformation
    brain_score = ambition + desire_energy + desire_breadth + concept_self

    # Behavior component (0-60)
    first_in = _cap(behavior.first_in_space_w, 4) * 20      # pioneers new territory
    created = _cap(behavior.spaces_created, 4) * 20          # builds new arenas
    initiated = _cap(behavior.self_initiated_w, 10) * 20     # acts from inner drive
    behavior_score = first_in + created + initiated

    return CapabilityScore(brain_score, behavior_score, 0)
