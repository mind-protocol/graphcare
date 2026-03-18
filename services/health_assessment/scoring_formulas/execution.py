"""
Scoring formulas for Execution aspect (T1-T3).

DOCS: docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md

Capabilities scored:
  - exec_dehallucinate (T1): Actively verifies claims against reality
  - exec_complete (T1): Finishes tasks completely, no partial delivery
  - exec_test_before_claim (T1): Tests before claiming built
  - exec_fix_found (T3): Fixes problems found along the way
"""

from .registry import register, CapabilityScore, _cap
from ..brain_topology_reader import BrainStats
from ..universe_moment_reader import BehaviorStats


@register("exec_dehallucinate")
def score_dehallucinate(brain: BrainStats, behavior: BehaviorStats) -> CapabilityScore:
    """T1 Execution: Actively verifies claims against reality.

    Brain (40): process nodes exist, low frustration, concept-to-memory links
    Behavior (60): high permanence outputs, dampening moments (fixes), response rate
    """
    # Brain component (0-40)
    process_signal = _cap(brain.process_count, 10) * 15     # has verification processes
    low_frustration = (1.0 - brain.frustration) * 10         # not blocked/frustrated
    concept_depth = _cap(brain.concept_count, 20) * 10       # rich conceptual model
    memory_signal = _cap(brain.memory_count, 15) * 5         # has memories to verify against
    brain_score = process_signal + low_frustration + concept_depth + memory_signal

    # Behavior component (0-60)
    permanence = _cap(behavior.high_permanence_w, 10) * 30   # produces definitive outputs
    activity = _cap(behavior.total_moments_w, 15) * 20       # is active
    spaces = _cap(behavior.distinct_space_count, 5) * 10     # works across contexts
    behavior_score = permanence + activity + spaces

    return CapabilityScore(brain_score, behavior_score, 0)


@register("exec_complete")
def score_complete(brain: BrainStats, behavior: BehaviorStats) -> CapabilityScore:
    """T1 Execution: Finishes tasks completely.

    Brain (40): desire persistence (desires with 3+ links), low frustration
    Behavior (60): high permanence, follow-through (first-in-space + continued)
    """
    # Brain
    persistence = brain.desire_persistence * 20               # desires lead to sustained action
    desire_action = brain.desire_moment_ratio * 15            # desires connect to moments
    recency = brain.recency_moment * 5                        # recent activity
    brain_score = persistence + desire_action + recency

    # Behavior
    permanence = _cap(behavior.high_permanence_w, 10) * 25   # definitive outputs
    follow_through = _cap(behavior.first_in_space_w, 3) * 15 # starts things
    initiated = _cap(behavior.self_initiated_w, 8) * 20      # self-driven
    behavior_score = permanence + follow_through + initiated

    return CapabilityScore(brain_score, behavior_score, 0)


@register("exec_test_before_claim")
def score_test_before_claim(brain: BrainStats, behavior: BehaviorStats) -> CapabilityScore:
    """T1 Execution: Tests before claiming built.

    Brain (40): process nodes, concept-process links
    Behavior (60): high permanence (tested=committed), activity volume
    """
    # Brain
    process = _cap(brain.process_count, 8) * 20
    concept_process = _cap(brain.concept_count, 15) * 10
    low_rush = (1.0 - min(1.0, brain.ambition * 0.5)) * 10  # not rushing (overly ambitious)
    brain_score = process + concept_process + low_rush

    # Behavior
    permanence = _cap(behavior.high_permanence_w, 8) * 30
    ratio = (1.0 - behavior.response_rate) * 15              # self-initiated > reactive
    spaces = _cap(behavior.distinct_space_count, 4) * 15
    behavior_score = permanence + ratio + spaces

    return CapabilityScore(brain_score, behavior_score, 0)


@register("exec_fix_found")
def score_fix_found(brain: BrainStats, behavior: BehaviorStats) -> CapabilityScore:
    """T3 Execution: Fixes problems found along the way.

    Brain (40): desire energy (motivation), low frustration, curiosity drive
    Behavior (60): self-initiated moments, spaces created, high permanence
    """
    # Brain
    curiosity = brain.curiosity * 15
    desire_e = brain.desire_energy * 15
    low_frustration = (1.0 - brain.frustration) * 10
    brain_score = curiosity + desire_e + low_frustration

    # Behavior
    initiated = _cap(behavior.self_initiated_w, 10) * 25
    created = _cap(behavior.spaces_created, 3) * 15
    permanence = _cap(behavior.high_permanence_w, 8) * 20
    behavior_score = initiated + created + permanence

    return CapabilityScore(brain_score, behavior_score, 0)
