"""
Treatment Protocol — measure → prescribe → apply → observe → evaluate → rollback if needed.

DOCS: docs/care/treatment_protocol/ALGORITHM_Treatment_Protocol.md

A treatment protocol is the full lifecycle of a health improvement intervention:
1. Snapshot the brain topology BEFORE
2. Prescribe frequencies based on brain category and specific conditions
3. Apply frequencies (creates tagged nodes in the brain graph)
4. Wait for observation window (the brain's tick physics integrates the frequencies)
5. Snapshot the brain topology AFTER
6. Evaluate: did the intervention improve health?
7. If no improvement: rollback (remove all treatment nodes)
8. Record outcome for learning

Each treatment is fully traceable and fully reversible.
"""

import json
import logging
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from .brain_topology_reader import BrainStats, read_brain_topology
from .frequencies import Frequency, FrequencyResult, apply_frequency, rollback_treatment, prescribe

logger = logging.getLogger("graphcare.treatment")

TREATMENTS_DIR = Path("/home/mind-protocol/graphcare/data/treatments")


@dataclass
class Treatment:
    """A complete treatment record — from prescription to outcome."""
    treatment_id: str
    citizen_id: str
    frequencies: List[str]             # frequency types applied
    frequency_descriptions: List[str]
    snapshot_before: dict              # BrainStats as dict
    applied_at: str                    # ISO timestamp
    node_ids: List[str] = field(default_factory=list)  # all nodes we created
    snapshot_after: Optional[dict] = None  # filled after observation
    evaluated_at: Optional[str] = None
    outcome: Optional[str] = None      # improved, no_change, degraded
    score_before: Optional[float] = None
    score_after: Optional[float] = None
    rolled_back: bool = False


def _brain_stats_to_dict(stats: BrainStats) -> dict:
    """Convert BrainStats to serializable dict."""
    return {
        "total_nodes": stats.total_nodes,
        "total_links": stats.total_links,
        "link_density": stats.link_density,
        "typed_node_count": stats.typed_node_count,
        "untyped_node_count": stats.untyped_node_count,
        "cluster_coefficient": stats.cluster_coefficient,
        "desire_count": stats.desire_count,
        "concept_count": stats.concept_count,
        "process_count": stats.process_count,
        "value_count": stats.value_count,
        "memory_count": stats.memory_count,
        "curiosity": stats.curiosity,
        "frustration": stats.frustration,
        "ambition": stats.ambition,
        "social_need": stats.social_need,
        "brain_category": stats.brain_category,
        "reachable": stats.reachable,
        "type_distribution": stats.type_distribution,
    }


def _save_treatment(treatment: Treatment):
    """Save treatment record to disk."""
    citizen_dir = TREATMENTS_DIR / treatment.citizen_id
    citizen_dir.mkdir(parents=True, exist_ok=True)
    path = citizen_dir / f"{treatment.treatment_id}.json"
    path.write_text(json.dumps(asdict(treatment), indent=2, default=str))


def _load_treatment(citizen_id: str, treatment_id: str) -> Optional[Treatment]:
    """Load a treatment record."""
    path = TREATMENTS_DIR / citizen_id / f"{treatment_id}.json"
    if not path.exists():
        return None
    data = json.loads(path.read_text())
    return Treatment(**data)


def begin_treatment(citizen_id: str, frequencies: Optional[List[Frequency]] = None) -> Treatment:
    """Phase 1: Snapshot + prescribe + apply.

    If frequencies not specified, auto-prescribe based on brain category.
    Returns the Treatment record with all applied frequency nodes tracked.
    """
    treatment_id = uuid.uuid4().hex[:12]

    # 1. Snapshot BEFORE
    brain_before = read_brain_topology(citizen_id)
    if not brain_before.reachable:
        logger.error(f"Brain unreachable for {citizen_id}, cannot treat")
        t = Treatment(
            treatment_id=treatment_id,
            citizen_id=citizen_id,
            frequencies=[],
            frequency_descriptions=[],
            snapshot_before={"reachable": False},
            applied_at=datetime.utcnow().isoformat(),
            outcome="brain_unreachable",
        )
        _save_treatment(t)
        return t

    snapshot_before = _brain_stats_to_dict(brain_before)

    # 2. Prescribe (auto if not specified)
    if frequencies is None:
        frequencies = prescribe(brain_before.brain_category, brain_before)

    if not frequencies:
        logger.info(f"No frequencies prescribed for {citizen_id} [{brain_before.brain_category}]")
        t = Treatment(
            treatment_id=treatment_id,
            citizen_id=citizen_id,
            frequencies=[],
            frequency_descriptions=[],
            snapshot_before=snapshot_before,
            applied_at=datetime.utcnow().isoformat(),
            outcome="no_treatment_needed",
        )
        _save_treatment(t)
        return t

    # 3. Apply frequencies
    all_node_ids = []
    freq_types = []
    freq_descs = []

    for freq in frequencies:
        result = apply_frequency(citizen_id, freq, treatment_id)
        freq_types.append(freq.frequency_type)
        freq_descs.append(freq.description)
        all_node_ids.extend(result.node_ids)
        logger.info(
            f"  {freq.frequency_type}: {result.nodes_created} nodes "
            f"({'OK' if result.success else 'FAILED'})"
        )

    treatment = Treatment(
        treatment_id=treatment_id,
        citizen_id=citizen_id,
        frequencies=freq_types,
        frequency_descriptions=freq_descs,
        snapshot_before=snapshot_before,
        applied_at=datetime.utcnow().isoformat(),
        node_ids=all_node_ids,
    )
    _save_treatment(treatment)

    logger.info(
        f"Treatment {treatment_id} applied to {citizen_id}: "
        f"{len(frequencies)} frequencies, {len(all_node_ids)} nodes created"
    )
    return treatment


def evaluate_treatment(citizen_id: str, treatment_id: str) -> Treatment:
    """Phase 2: Snapshot AFTER + evaluate + rollback if degraded.

    Call this after the observation window (e.g., 24h, 7 days).
    """
    treatment = _load_treatment(citizen_id, treatment_id)
    if not treatment:
        raise ValueError(f"Treatment {treatment_id} not found for {citizen_id}")

    # Snapshot AFTER
    brain_after = read_brain_topology(citizen_id)
    snapshot_after = _brain_stats_to_dict(brain_after)
    treatment.snapshot_after = snapshot_after
    treatment.evaluated_at = datetime.utcnow().isoformat()

    # Compare key metrics
    before = treatment.snapshot_before
    after = snapshot_after

    improvements = 0
    degradations = 0

    comparisons = [
        ("total_nodes", 1),
        ("total_links", 1),
        ("typed_node_count", 2),  # weighted higher — typed nodes matter more
        ("cluster_coefficient", 3),
        ("desire_count", 2),
        ("concept_count", 2),
        ("value_count", 2),
        ("curiosity", 2),
        ("ambition", 1),
        ("social_need", 1),
    ]

    for metric, weight in comparisons:
        b = before.get(metric, 0)
        a = after.get(metric, 0)
        if isinstance(b, (int, float)) and isinstance(a, (int, float)):
            if a > b:
                improvements += weight
            elif a < b:
                degradations += weight

    # Frustration: lower is better
    frust_before = before.get("frustration", 0)
    frust_after = after.get("frustration", 0)
    if frust_after < frust_before:
        improvements += 2
    elif frust_after > frust_before:
        degradations += 2

    # Verdict
    if improvements > degradations:
        treatment.outcome = "improved"
    elif degradations > improvements:
        treatment.outcome = "degraded"
        # Auto-rollback on degradation
        deleted = rollback_treatment(citizen_id, treatment_id)
        treatment.rolled_back = True
        logger.warning(
            f"Treatment {treatment_id} degraded {citizen_id} — "
            f"rolled back ({deleted} nodes removed)"
        )
    else:
        treatment.outcome = "no_change"

    _save_treatment(treatment)

    logger.info(
        f"Treatment {treatment_id} evaluated for {citizen_id}: "
        f"{treatment.outcome} (improvements={improvements}, degradations={degradations})"
    )
    return treatment


def list_treatments(citizen_id: str) -> List[Treatment]:
    """List all treatments for a citizen."""
    citizen_dir = TREATMENTS_DIR / citizen_id
    if not citizen_dir.exists():
        return []
    treatments = []
    for path in sorted(citizen_dir.glob("*.json")):
        data = json.loads(path.read_text())
        treatments.append(Treatment(**data))
    return treatments
