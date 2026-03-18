"""
Scoring formulas for Context & Understanding aspect (T1-T3).

DOCS: docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md

Capabilities scored:
  - ctx_ground_in_reality (T1): Verifies real state before asserting anything
  - ctx_read_journal_first (T1): Reads SYNC/state/journal before any action
  - ctx_fetch_right_context (T2): Reads docs, templates, existing code before executing
  - ctx_manage_own_state (T3): Maintains coherence across long sessions using tasks/plans/memory
"""

from .registry import register, CapabilityScore, _cap
from ..brain_topology_reader import BrainStats
from ..universe_moment_reader import BehaviorStats


@register("ctx_ground_in_reality")
def score_ground_in_reality(brain: BrainStats, behavior: BehaviorStats) -> CapabilityScore:
    """T1 Context: Verifies real state before asserting anything.

    Brain (40): memory count (has references to check against), process nodes
                (verification routines), low frustration (patient enough to check)
    Behavior (60): high permanence (produces verified outputs), activity volume,
                   distinct spaces (verifies across contexts)
    """
    # Brain component (0-40)
    memory_refs = _cap(brain.memory_count, 15) * 15       # memories to verify against
    process_signal = _cap(brain.process_count, 8) * 15    # has verification processes
    low_frustration = (1.0 - brain.frustration) * 10      # patient enough to check
    brain_score = memory_refs + process_signal + low_frustration

    # Behavior component (0-60)
    permanence = _cap(behavior.high_permanence_w, 10) * 25  # verified, definitive outputs
    activity = _cap(behavior.total_moments_w, 12) * 20      # actively working (and checking)
    spaces = _cap(behavior.distinct_space_count, 5) * 15    # verifies across contexts
    behavior_score = permanence + activity + spaces

    return CapabilityScore(brain_score, behavior_score, 0)


@register("ctx_read_journal_first")
def score_read_journal_first(brain: BrainStats, behavior: BehaviorStats) -> CapabilityScore:
    """T1 Context: Reads SYNC/state/journal before any action.

    Brain (40): memory count (retains state), recency of desires (recently refreshed intent),
                concept count (conceptual model built from reading)
    Behavior (60): response rate (low = self-initiated, reads before acting),
                   first-in-space (enters new spaces informed), activity
    """
    # Brain component (0-40)
    memory = _cap(brain.memory_count, 20) * 15             # has accumulated state
    recency_desire = brain.recency_desire * 15             # recently refreshed priorities
    concepts = _cap(brain.concept_count, 15) * 10          # conceptual model from reading
    brain_score = memory + recency_desire + concepts

    # Behavior component (0-60)
    self_directed = (1.0 - behavior.response_rate) * 20    # reads first, acts from own context
    first_in = _cap(behavior.first_in_space_w, 3) * 20    # enters spaces with preparation
    activity = _cap(behavior.total_moments_w, 10) * 20     # active after reading
    behavior_score = self_directed + first_in + activity

    return CapabilityScore(brain_score, behavior_score, 0)


@register("ctx_fetch_right_context")
def score_fetch_right_context(brain: BrainStats, behavior: BehaviorStats) -> CapabilityScore:
    """T2 Context: Reads docs, templates, existing code before executing.

    Brain (40): concept count (rich mental model), process count (knows where to look),
                curiosity drive (motivated to gather info)
    Behavior (60): distinct spaces (reads across multiple sources), activity,
                   high permanence (produces well-informed outputs)
    """
    # Brain component (0-40)
    concepts = _cap(brain.concept_count, 25) * 15          # rich conceptual model
    processes = _cap(brain.process_count, 10) * 10         # knows how to gather context
    curiosity = brain.curiosity * 15                        # driven to understand
    brain_score = concepts + processes + curiosity

    # Behavior component (0-60)
    spaces = _cap(behavior.distinct_space_count, 6) * 25   # reads from many sources
    permanence = _cap(behavior.high_permanence_w, 8) * 20  # well-informed definitive outputs
    activity = _cap(behavior.total_moments_w, 12) * 15     # enough activity to gather context
    behavior_score = spaces + permanence + activity

    return CapabilityScore(brain_score, behavior_score, 0)


@register("ctx_manage_own_state")
def score_manage_own_state(brain: BrainStats, behavior: BehaviorStats) -> CapabilityScore:
    """T3 Context: Maintains coherence across long sessions using tasks/plans/memory.

    Brain (40): desire persistence (sustained intent), memory count (retains decisions),
                cluster coefficient (interconnected knowledge)
    Behavior (60): self-initiated moments (drives own continuity), spaces created
                   (organizes own workspace), high permanence (state is committed)
    """
    # Brain component (0-40)
    persistence = brain.desire_persistence * 15             # sustains intent across time
    memory = _cap(brain.memory_count, 20) * 15             # retains decisions and state
    coherence = brain.cluster_coefficient * 10              # knowledge is interconnected
    brain_score = persistence + memory + coherence

    # Behavior component (0-60)
    initiated = _cap(behavior.self_initiated_w, 10) * 25   # drives own continuity
    created = _cap(behavior.spaces_created, 3) * 15        # organizes own workspace
    permanence = _cap(behavior.high_permanence_w, 8) * 20  # state is committed, not lost
    behavior_score = initiated + created + permanence

    return CapabilityScore(brain_score, behavior_score, 0)
