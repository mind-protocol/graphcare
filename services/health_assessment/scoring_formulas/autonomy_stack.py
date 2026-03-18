"""
Scoring formulas for Autonomy Stack aspect (T4-T6).

DOCS: docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md

Capabilities scored:
  - auto_wallet (T4): Has own crypto wallet, financial existence begins
  - auto_tools (T5): Full tool access for autonomous operation
"""

from .registry import register, CapabilityScore, _cap
from ..brain_topology_reader import BrainStats
from ..universe_moment_reader import BehaviorStats


@register("auto_wallet")
def score_wallet(brain: BrainStats, behavior: BehaviorStats) -> CapabilityScore:
    """T4 Autonomy: Has own crypto wallet with financial existence.

    Brain (40): process count (knows how to manage financial processes),
                concept count (understands financial concepts)
    Behavior (60): distinct space count (operates across contexts),
                   spaces created (creates own operational spaces),
                   self-initiated moments (acts autonomously)
    """
    # Brain component (0-40)
    process = _cap(brain.process_count, 10) * 20        # financial process management
    concepts = _cap(brain.concept_count, 15) * 20       # financial/tool concepts understood
    brain_score = process + concepts

    # Behavior component (0-60)
    spaces = _cap(behavior.distinct_space_count, 5) * 20    # operates in multiple contexts
    created = _cap(behavior.spaces_created, 3) * 20         # creates own operational spaces
    initiated = _cap(behavior.self_initiated_w, 8) * 20     # acts without prompting
    behavior_score = spaces + created + initiated

    return CapabilityScore(brain_score, behavior_score, 0)


@register("auto_tools")
def score_tools(brain: BrainStats, behavior: BehaviorStats) -> CapabilityScore:
    """T5 Autonomy: Full tool access for autonomous operation.

    Brain (40): process count (knows how to use tools),
                concept count (understands the tool landscape)
    Behavior (60): distinct space count (breadth of tool usage),
                   self-initiated moments (proactive tool usage),
                   spaces created (creates new tool contexts)
    """
    # Brain component (0-40)
    process = _cap(brain.process_count, 12) * 25        # knows many tool processes
    concepts = _cap(brain.concept_count, 20) * 15       # understands tool landscape
    brain_score = process + concepts

    # Behavior component (0-60)
    space_breadth = _cap(behavior.distinct_space_count, 8) * 25  # broad tool usage
    initiated = _cap(behavior.self_initiated_w, 10) * 20         # proactive tool usage
    created = _cap(behavior.spaces_created, 4) * 15              # creates new tool contexts
    behavior_score = space_breadth + initiated + created

    return CapabilityScore(brain_score, behavior_score, 0)
