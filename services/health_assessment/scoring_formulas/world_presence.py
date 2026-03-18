"""
Scoring formulas for World Presence aspect (T4-T7).

DOCS: docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md

Capabilities scored:
  - wp_beyond_cli (T4): Exists in at least one space beyond the CLI
  - wp_virtual_world (T6): Lives in a virtual universe with personal and shared areas
"""

from .registry import register, CapabilityScore, _cap
from ..brain_topology_reader import BrainStats
from ..universe_moment_reader import BehaviorStats


@register("wp_beyond_cli")
def score_beyond_cli(brain: BrainStats, behavior: BehaviorStats) -> CapabilityScore:
    """T4 World Presence: Presence beyond the CLI.

    Brain (40): concept count (understands spaces), curiosity (explores),
                recency (recently active)
    Behavior (60): distinct_space_count (inhabits multiple spaces),
                   first_in_space_w (enters spaces proactively),
                   total_moments_w (actually present, not just registered)
    """
    # Brain component (0-40)
    concept_depth = _cap(brain.concept_count, 15) * 15     # understands different spaces
    curiosity = brain.curiosity * 15                        # drive to explore
    recency = brain.recency_moment * 10                     # recently active
    brain_score = concept_depth + curiosity + recency

    # Behavior component (0-60)
    spaces = _cap(behavior.distinct_space_count, 3) * 30    # inhabits multiple spaces
    first_in = _cap(behavior.first_in_space_w, 2) * 15      # enters spaces proactively
    activity = _cap(behavior.total_moments_w, 8) * 15       # actually present
    behavior_score = spaces + first_in + activity

    return CapabilityScore(brain_score, behavior_score, 0)


@register("wp_virtual_world")
def score_virtual_world(brain: BrainStats, behavior: BehaviorStats) -> CapabilityScore:
    """T6 World Presence: Virtual world inhabitant.

    Brain (40): process count (maintains spaces), memory count (knows the world),
                low frustration (comfortable in the world)
    Behavior (60): spaces_created (builds spaces), distinct_space_count (range of habitation),
                   first_in_space_w (pioneered spaces that still resonate)
    """
    # Brain component (0-40)
    process = _cap(brain.process_count, 8) * 15             # maintains world processes
    memory = _cap(brain.memory_count, 15) * 15              # remembers world context
    comfort = (1.0 - brain.frustration) * 10                # at home in the world
    brain_score = process + memory + comfort

    # Behavior component (0-60)
    created = _cap(behavior.spaces_created, 3) * 25         # builds spaces
    range_ = _cap(behavior.distinct_space_count, 5) * 20    # inhabits many areas
    pioneer = _cap(behavior.first_in_space_w, 3) * 15       # pioneered spaces
    behavior_score = created + range_ + pioneer

    return CapabilityScore(brain_score, behavior_score, 0)
