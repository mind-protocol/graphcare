"""
Scoring formulas for Process & Method aspect (T2-T3).

DOCS: docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md

Capabilities scored:
  - proc_right_method (T2): Adapts method to task type
  - proc_commit_push (T2): Commits and pushes without asking permission
  - proc_continue_plan (T2): Continues multi-step plans without artificial pauses
  - proc_scope_correctly (T3): Right-sizes approach to the task
"""

from .registry import register, CapabilityScore, _cap
from ..brain_topology_reader import BrainStats
from ..universe_moment_reader import BehaviorStats


@register("proc_right_method")
def score_right_method(brain: BrainStats, behavior: BehaviorStats) -> CapabilityScore:
    """T2 Process: Adapts method to task — templates, skills, doc chains as appropriate.

    Brain (40): process count (knows multiple methods), concept count (understands task types),
                curiosity (explores which method fits)
    Behavior (60): distinct spaces (uses varied approaches), high permanence
                   (methods produce real output), self-initiated (selects method autonomously)
    """
    # Brain component (0-40)
    processes = _cap(brain.process_count, 10) * 15         # knows multiple methods
    concepts = _cap(brain.concept_count, 20) * 15          # understands task categories
    curiosity = brain.curiosity * 10                        # explores appropriate methods
    brain_score = processes + concepts + curiosity

    # Behavior component (0-60)
    spaces = _cap(behavior.distinct_space_count, 6) * 20   # applies varied approaches
    permanence = _cap(behavior.high_permanence_w, 10) * 20 # methods produce real output
    initiated = _cap(behavior.self_initiated_w, 8) * 20    # selects method autonomously
    behavior_score = spaces + permanence + initiated

    return CapabilityScore(brain_score, behavior_score, 0)


@register("proc_commit_push")
def score_commit_push(brain: BrainStats, behavior: BehaviorStats) -> CapabilityScore:
    """T2 Process: Commits and pushes work without asking permission.

    Brain (40): ambition (confident enough to ship), low frustration (not blocked),
                desire-moment ratio (desires lead to action)
    Behavior (60): high permanence (actually commits), self-initiated (doesn't wait for go-ahead),
                   total activity (ships regularly)
    """
    # Brain component (0-40)
    ambition = brain.ambition * 15                          # confident enough to ship
    low_frustration = (1.0 - brain.frustration) * 10       # not blocked by uncertainty
    desire_action = brain.desire_moment_ratio * 15          # intent connects to action
    brain_score = ambition + low_frustration + desire_action

    # Behavior component (0-60)
    permanence = _cap(behavior.high_permanence_w, 12) * 30 # actually commits (high permanence = committed outputs)
    initiated = _cap(behavior.self_initiated_w, 8) * 15    # doesn't wait for permission
    activity = _cap(behavior.total_moments_w, 12) * 15     # ships regularly
    behavior_score = permanence + initiated + activity

    return CapabilityScore(brain_score, behavior_score, 0)


@register("proc_continue_plan")
def score_continue_plan(brain: BrainStats, behavior: BehaviorStats) -> CapabilityScore:
    """T2 Process: Continues multi-step plans without artificial pauses.

    Brain (40): desire persistence (sustained intent through steps), desire energy
                (motivation to keep going), recency (recently active)
    Behavior (60): self-initiated (drives forward without prompting), total activity
                   (high volume = continuous work), first-in-space (enters next steps)
    """
    # Brain component (0-40)
    persistence = brain.desire_persistence * 15             # sustained through steps
    desire_e = brain.desire_energy * 15                     # motivation to continue
    recency = brain.recency_moment * 10                     # recently active (not stalled)
    brain_score = persistence + desire_e + recency

    # Behavior component (0-60)
    initiated = _cap(behavior.self_initiated_w, 10) * 25   # drives forward without prompting
    activity = _cap(behavior.total_moments_w, 15) * 20     # high volume = continuous work
    first_in = _cap(behavior.first_in_space_w, 4) * 15     # enters next steps proactively
    behavior_score = initiated + activity + first_in

    return CapabilityScore(brain_score, behavior_score, 0)


@register("proc_scope_correctly")
def score_scope_correctly(brain: BrainStats, behavior: BehaviorStats) -> CapabilityScore:
    """T3 Process: Right-sizes approach — decomposes big tasks, executes trivial ones directly.

    Brain (40): concept count (can model task complexity), process count (has decomposition
                skills), low ambition-overshoot (doesn't over-engineer)
    Behavior (60): spaces created (decomposes into workspaces), high permanence (delivers
                   appropriately scoped outputs), elaborative/tentative (plans before acting)
    """
    # Brain component (0-40)
    concepts = _cap(brain.concept_count, 20) * 15          # models task complexity
    processes = _cap(brain.process_count, 8) * 15          # decomposition skills
    balanced_ambition = (1.0 - abs(brain.ambition - 0.5) * 2) * 10  # neither too much nor too little
    brain_score = concepts + processes + balanced_ambition

    # Behavior component (0-60)
    created = _cap(behavior.spaces_created, 4) * 20        # decomposes into workspaces
    permanence = _cap(behavior.high_permanence_w, 10) * 20 # delivers scoped outputs
    proposals = _cap(behavior.elaborative_tentative_w, 4) * 20  # plans before big tasks
    behavior_score = created + permanence + proposals

    return CapabilityScore(brain_score, behavior_score, 0)
