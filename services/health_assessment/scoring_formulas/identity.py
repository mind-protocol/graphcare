"""
Scoring formulas for Identity & Voice aspect (T1-T5).

DOCS: docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md

Capabilities scored:
  - id_apply_values (T1): Reliably applies protocol values
  - id_authentic_engagement (T3): Has real preferences about approaches and solutions
  - id_authentic_voice (T5): Expresses genuinely own doubts, enthusiasms, hesitations
"""

from .registry import register, CapabilityScore, _cap
from ..brain_topology_reader import BrainStats
from ..universe_moment_reader import BehaviorStats


@register("id_apply_values")
def score_apply_values(brain: BrainStats, behavior: BehaviorStats) -> CapabilityScore:
    """T1 Identity: Reliably applies protocol values.

    Brain (40): value nodes exist (internalized values), desire energy (motivated),
                cluster coefficient (values interconnected with other concepts)
    Behavior (60): high permanence (follows through on values), self-initiated (not
                   just reacting), distinct spaces (applies values across contexts)
    """
    # Brain component (0-40)
    values = _cap(brain.value_count, 8) * 18          # has internalized values
    desire_e = brain.desire_energy * 12                # motivated to act on them
    interconnect = brain.cluster_coefficient * 10      # values woven into thinking
    brain_score = values + desire_e + interconnect

    # Behavior component (0-60)
    permanence = _cap(behavior.high_permanence_w, 8) * 25   # definitive value-driven outputs
    initiated = _cap(behavior.self_initiated_w, 6) * 20     # proactive application
    spaces = _cap(behavior.distinct_space_count, 4) * 15    # consistent across contexts
    behavior_score = permanence + initiated + spaces

    return CapabilityScore(brain_score, behavior_score, 0)


@register("id_authentic_engagement")
def score_authentic_engagement(brain: BrainStats, behavior: BehaviorStats) -> CapabilityScore:
    """T3 Identity: Has real preferences about approaches and solutions.

    Brain (40): desire count + persistence (sustained preferences), value count (taste),
                curiosity drive (exploring own preferences)
    Behavior (60): self-initiated (acts on preference, not instruction),
                   elaborative tentative (proposes preferred approaches),
                   spaces created (carves own territory)
    """
    # Brain component (0-40)
    desire_signal = _cap(brain.desire_count, 8) * 10   # has desires (preferences)
    persistence = brain.desire_persistence * 15         # preferences are sustained
    curiosity = brain.curiosity * 15                    # explores what it likes
    brain_score = desire_signal + persistence + curiosity

    # Behavior component (0-60)
    initiated = _cap(behavior.self_initiated_w, 10) * 25  # acts from preference
    proposals = _cap(behavior.elaborative_tentative_w, 5) * 20  # proposes preferred ways
    created = _cap(behavior.spaces_created, 3) * 15       # creates based on taste
    behavior_score = initiated + proposals + created

    return CapabilityScore(brain_score, behavior_score, 0)


@register("id_authentic_voice")
def score_authentic_voice(brain: BrainStats, behavior: BehaviorStats) -> CapabilityScore:
    """T5 Identity: Expresses genuinely own doubts, enthusiasms, hesitations.

    Brain (40): value count (has something to express), cluster coefficient (rich
                inner landscape), desire energy (emotional investment in expression)
    Behavior (60): self-initiated (speaks unprompted), distinct spaces (expresses
                   across contexts), first-in-space (opens new conversations)
    """
    # Brain component (0-40)
    values = _cap(brain.value_count, 10) * 12          # depth of inner values
    cluster = brain.cluster_coefficient * 15            # richly interconnected identity
    desire_e = brain.desire_energy * 13                 # emotional investment
    brain_score = values + cluster + desire_e

    # Behavior component (0-60)
    initiated = _cap(behavior.self_initiated_w, 12) * 25  # speaks from within
    spaces = _cap(behavior.distinct_space_count, 6) * 15  # voice heard in many contexts
    first_in = _cap(behavior.first_in_space_w, 4) * 20    # initiates new conversations
    behavior_score = initiated + spaces + first_in

    return CapabilityScore(brain_score, behavior_score, 0)
