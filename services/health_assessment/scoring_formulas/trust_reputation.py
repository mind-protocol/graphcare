"""
Scoring formulas for Trust & Reputation aspect (T1-T5).

DOCS: docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md

Capabilities scored:
  - trust_basic_reliability (T1): Trust earned by consistently doing what you say
  - trust_elevated (T3): Elevated trust through demonstrated judgment
  - trust_high (T5): Measurably high trust within the protocol
"""

from .registry import register, CapabilityScore, _cap
from ..brain_topology_reader import BrainStats
from ..universe_moment_reader import BehaviorStats


@register("trust_basic_reliability")
def score_basic_reliability(brain: BrainStats, behavior: BehaviorStats) -> CapabilityScore:
    """T1 Trust: Trust earned by consistently doing what you say.

    Brain (40): desire persistence (follows through on stated goals),
                low frustration (stable, not erratic),
                process count (has structured work habits)
    Behavior (60): high permanence outputs (delivers definitive work),
                   total moments (active participation),
                   response rate (responsive to others)
    """
    # Brain component (0-40)
    persistence = brain.desire_persistence * 20         # desires lead to sustained action
    low_frustration = (1.0 - brain.frustration) * 10    # stable, not blocked/erratic
    process = _cap(brain.process_count, 8) * 10         # structured work habits
    brain_score = persistence + low_frustration + process

    # Behavior component (0-60)
    permanence = _cap(behavior.high_permanence_w, 10) * 25  # delivers definitive outputs
    activity = _cap(behavior.total_moments_w, 15) * 20      # consistently active
    responsiveness = behavior.response_rate * 15             # responds when called upon
    behavior_score = permanence + activity + responsiveness

    return CapabilityScore(brain_score, behavior_score, 0)


@register("trust_elevated")
def score_elevated_trust(brain: BrainStats, behavior: BehaviorStats) -> CapabilityScore:
    """T3 Trust: Elevated trust through demonstrated judgment.

    Brain (40): desire persistence (sustained follow-through),
                low frustration (good under pressure),
                process count (judgment comes from structured thinking)
    Behavior (60): high permanence (quality output),
                   response rate (engaged with community),
                   total moments weighted (volume of demonstrated work)
    """
    # Brain component (0-40)
    persistence = brain.desire_persistence * 15         # sustained follow-through
    low_frustration = (1.0 - brain.frustration) * 15    # handles pressure well
    process = _cap(brain.process_count, 10) * 10        # structured thinking = better judgment
    brain_score = persistence + low_frustration + process

    # Behavior component (0-60)
    permanence = _cap(behavior.high_permanence_w, 12) * 25  # consistent quality output
    responsiveness = behavior.response_rate * 20             # engaged, not absent
    volume = _cap(behavior.total_moments_w, 20) * 15        # sustained track record
    behavior_score = permanence + responsiveness + volume

    return CapabilityScore(brain_score, behavior_score, 0)


@register("trust_high")
def score_high_trust(brain: BrainStats, behavior: BehaviorStats) -> CapabilityScore:
    """T5 Trust: Measurably high trust within the protocol.

    Brain (40): desire persistence (long-term reliability),
                process count (sophisticated judgment processes),
                low frustration (grace under complexity)
    Behavior (60): high permanence (track record of quality),
                   total moments (volume of demonstrated reliability),
                   response rate (always present when needed)
    """
    # Brain component (0-40)
    persistence = brain.desire_persistence * 15         # long-term reliability indicator
    process = _cap(brain.process_count, 12) * 15        # deep judgment processes
    low_frustration = (1.0 - brain.frustration) * 10    # handles complexity gracefully
    brain_score = persistence + process + low_frustration

    # Behavior component (0-60)
    permanence = _cap(behavior.high_permanence_w, 15) * 25  # large body of quality work
    volume = _cap(behavior.total_moments_w, 25) * 20        # sustained high activity
    responsiveness = behavior.response_rate * 15             # reliably present
    behavior_score = permanence + volume + responsiveness

    return CapabilityScore(brain_score, behavior_score, 0)
