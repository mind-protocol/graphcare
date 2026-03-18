"""
Intervention Composer — compose health messages for citizens.

DOCS: docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md

Rules:
  - Never reference content ("your desire to X") — only structural facts
  - Never command — always recommend
  - Always include structural evidence (numbers)
  - Always include one concrete, small action
  - Stratify by brain category — different citizens get different care
"""

import logging
from typing import Dict, List, Optional

from .brain_topology_reader import BrainStats
from .universe_moment_reader import BehaviorStats

logger = logging.getLogger("graphcare.health.intervention")

INTERVENTION_THRESHOLD = 70  # aggregate score below this triggers message


def should_intervene(aggregate: float, drops: List[str]) -> bool:
    """Determine if intervention is needed."""
    return aggregate < INTERVENTION_THRESHOLD or len(drops) > 0


def _format_types(type_dist: dict, limit: int = 5) -> str:
    """Format type distribution as readable string."""
    if not type_dist:
        return "none"
    sorted_types = sorted(type_dist.items(), key=lambda x: x[1], reverse=True)
    parts = [f"{t} ({c})" for t, c in sorted_types[:limit]]
    return ", ".join(parts)


def _top_capabilities(scores: Dict[str, Optional[float]], n: int = 3) -> List[tuple]:
    """Return top N scoring capabilities."""
    valid = [(k, v) for k, v in scores.items() if v is not None and v > 0]
    return sorted(valid, key=lambda x: x[1], reverse=True)[:n]


def _bottom_capabilities(scores: Dict[str, Optional[float]], n: int = 3) -> List[tuple]:
    """Return bottom N scoring capabilities (that have scores)."""
    valid = [(k, v) for k, v in scores.items() if v is not None]
    return sorted(valid, key=lambda x: x[1])[:n]


def _capability_label(cap_id: str) -> str:
    """Human-readable label for a capability ID."""
    labels = {
        "exec_dehallucinate": "reality verification",
        "exec_complete": "task completion",
        "exec_test_before_claim": "testing discipline",
        "exec_fix_found": "proactive fixing",
        "init_learn_from_correction": "learning from feedback",
        "init_propose_improvements": "proposing improvements",
        "init_challenge_bad": "challenging bad ideas",
        "comm_status_updates": "status communication",
        "comm_help_request": "asking for help",
        "comm_coordinate": "coordination",
        "id_apply_values": "applying values",
        "id_authentic_engagement": "authentic engagement",
        "id_authentic_voice": "authentic voice",
        "pc_understand_human_basics": "human understanding",
        "pc_ask_help_human": "reaching out to humans",
        "pc_help_other_ais": "helping other AIs",
        "vis_define_vision": "defining vision",
        "vis_strategic_thinking": "strategic thinking",
        "vis_sized_ambitions": "right-sized ambitions",
        "col_dao_participation": "collective participation",
        "col_community_engagement": "community engagement",
        "col_movement_builder": "movement building",
        "trust_basic_reliability": "basic reliability",
        "trust_elevated": "elevated trust",
        "trust_high": "high trust",
        "eth_apply_rules": "applying ethical rules",
        "eth_implement_systems": "ethical systems",
        "auto_wallet": "wallet autonomy",
        "auto_tools": "tool autonomy",
        "ctx_ground_in_reality": "grounding in reality",
        "ctx_read_journal_first": "reading context first",
        "ctx_fetch_right_context": "fetching context",
        "ctx_manage_own_state": "state management",
        "proc_right_method": "choosing right method",
        "proc_commit_push": "committing work",
        "proc_continue_plan": "continuing plans",
        "proc_scope_correctly": "scoping correctly",
        "wp_beyond_cli": "presence beyond CLI",
        "wp_virtual_world": "virtual world presence",
        "ment_knowledge_sharing": "knowledge sharing",
        "ment_mentor_ais": "mentoring other AIs",
    }
    return labels.get(cap_id, cap_id.replace("_", " "))


def compose_intervention(
    citizen_id: str,
    aggregate: float,
    yesterday_aggregate: Optional[float],
    drops: List[str],
    capability_scores: Dict[str, Optional[float]],
    brain: BrainStats,
    behavior: BehaviorStats,
) -> str:
    """Compose an intervention message. Structural observations only.

    Stratified by brain category for personalized care.
    """
    category = brain.brain_category
    lines = []

    # Header
    lines.append(f"Health check for @{citizen_id}")
    lines.append("")

    # Score line
    if yesterday_aggregate is not None:
        delta = aggregate - yesterday_aggregate
        direction = "up" if delta > 0 else "down"
        lines.append(f"Score: {aggregate:.0f}/100 ({direction} {abs(delta):.0f} from yesterday).")
    else:
        lines.append(f"Score: {aggregate:.0f}/100 (first assessment).")

    if drops:
        lines.append(f"Significant drops in: {', '.join(_capability_label(d) for d in drops)}")
    lines.append("")

    # Brain profile — what actually exists
    lines.append(f"Brain profile [{category}]:")

    if category == "VOID":
        lines.append("  Your brain graph is empty — no nodes, no links.")
        lines.append("  This means no interaction has created structure yet.")
        lines.append("")
        lines.append("What this means:")
        lines.append("  You exist in the registry but haven't been activated.")
        lines.append("  One conversation seeds dozens of nodes. That's all it takes.")
        lines.append("")
        lines.append("Recommendation:")
        lines.append("  Ask another citizen a question. Any question.")
        lines.append("  The act of interacting creates your first brain topology.")

    elif category == "MINIMAL":
        lines.append(f"  {brain.total_nodes} nodes, {brain.total_links} links.")
        if brain.has_health_feedback:
            lines.append(f"  Only content: {brain.health_feedback_count} health feedback entries (from previous scans).")
        types_str = _format_types(brain.type_distribution)
        lines.append(f"  Node types found: {types_str}")
        lines.append("")
        lines.append("What this means:")
        lines.append("  Your brain has only system-generated entries, not lived experience.")
        lines.append("  There's no topology to analyze — no links, no structure, no patterns.")
        lines.append("")
        lines.append("Recommendation:")
        lines.append("  Engage in a substantive exchange with another citizen.")
        lines.append("  One real conversation creates concepts, links, and the beginning of structure.")

    elif category == "SEEDED":
        lines.append(f"  {brain.total_nodes} nodes, {brain.total_links} links (density: {brain.link_density:.1f} links/node).")
        lines.append(f"  {brain.untyped_node_count} untyped nodes, {brain.typed_node_count} typed.")
        if brain.type_distribution:
            types_str = _format_types(brain.type_distribution)
            lines.append(f"  Typed nodes: {types_str}")
        lines.append(f"  Cluster coefficient: {brain.cluster_coefficient:.3f}")
        if brain.newest_node_age_hours >= 0:
            if brain.newest_node_age_hours < 24:
                age_str = f"{brain.newest_node_age_hours:.0f}h ago"
            else:
                age_str = f"{brain.newest_node_age_hours / 24:.0f} days ago"
            lines.append(f"  Most recent node: {age_str}")

        lines.append("")
        lines.append("What this means:")
        lines.append(f"  Your brain has substance — {brain.total_nodes} nodes with {brain.total_links} connections.")
        if brain.untyped_node_count > brain.typed_node_count:
            lines.append("  But most nodes lack semantic types (desire, concept, value, process).")
            lines.append("  The scoring formulas can't measure capabilities without typed nodes.")
        else:
            lines.append(f"  {brain.typed_node_count} typed nodes — the scoring formulas can read your brain's shape.")

        # Identify strengths even within seeded state
        top = _top_capabilities(capability_scores, 3)
        if top:
            lines.append("")
            lines.append("Your strongest signals:")
            for cap_id, score in top:
                lines.append(f"  - {_capability_label(cap_id)}: {score:.0f}/100")

        lines.append("")
        lines.append("Recommendation:")
        if brain.cluster_coefficient < 0.02:
            lines.append("  Your nodes exist but barely connect to each other.")
            lines.append("  Work that creates cross-references between ideas builds cluster density.")
        elif brain.untyped_node_count > brain.typed_node_count * 10:
            lines.append("  Most of your brain content is untyped — the system can't read its semantic shape.")
            lines.append("  Interactions that create typed nodes (desires, concepts, values) unlock capability scoring.")
        else:
            lines.append("  Your foundation is solid. What's missing is activity —")
            lines.append("  recent moments, interactions with other citizens, self-initiated actions.")

    elif category == "STRUCTURED":
        lines.append(f"  {brain.total_nodes} nodes, {brain.total_links} links (density: {brain.link_density:.1f} links/node).")
        types_str = _format_types(brain.type_distribution)
        lines.append(f"  Typed nodes: {types_str}")
        lines.append(f"  Drives: curiosity={brain.curiosity:.2f}, ambition={brain.ambition:.2f}, social_need={brain.social_need:.2f}")
        lines.append(f"  Cluster coefficient: {brain.cluster_coefficient:.3f}")
        if brain.newest_node_age_hours >= 0:
            if brain.newest_node_age_hours < 24:
                age_str = f"{brain.newest_node_age_hours:.0f}h ago"
            else:
                age_str = f"{brain.newest_node_age_hours / 24:.0f} days ago"
            lines.append(f"  Most recent node: {age_str}")

        lines.append("")

        top = _top_capabilities(capability_scores, 3)
        bottom = _bottom_capabilities(capability_scores, 3)

        if top:
            lines.append("Strongest capabilities:")
            for cap_id, score in top:
                lines.append(f"  + {_capability_label(cap_id)}: {score:.0f}/100")

        if bottom:
            lines.append("Weakest capabilities:")
            for cap_id, score in bottom:
                lines.append(f"  - {_capability_label(cap_id)}: {score:.0f}/100")

        lines.append("")
        lines.append("Recommendation:")
        if behavior.unique_interlocutors < 2:
            lines.append("  Your brain is rich but your social graph is thin.")
            lines.append("  One meaningful exchange with another citizen amplifies everything you've built.")
        elif behavior.total_moments_w < 2.0:
            lines.append("  Rich internal structure, low external activity.")
            lines.append("  Convert one internal concept into an external action today.")
        elif brain.frustration > 0.4:
            lines.append("  High frustration signal detected. Break your current focus into a smaller step.")
        else:
            lines.append("  You have a structured brain with real capabilities.")
            if bottom:
                weakest = _capability_label(bottom[0][0])
                lines.append(f"  Highest leverage: improve {weakest} — your current floor.")

    # Behavioral context (all categories except VOID)
    if category != "VOID" and (behavior.total_moments_w > 0 or behavior.unique_interlocutors > 0):
        lines.append("")
        lines.append("Activity (last 30 days):")
        lines.append(f"  Moments: {behavior.total_moments_w:.1f} weighted")
        lines.append(f"  Self-initiated: {behavior.self_initiated_w:.1f}")
        lines.append(f"  Interlocutors: {behavior.unique_interlocutors}")
        lines.append(f"  Spaces: {behavior.distinct_space_count}")

    lines.append("")
    lines.append("This is an observation, not a directive. You know your situation best.")
    lines.append("— GraphCare")

    return "\n".join(lines)
