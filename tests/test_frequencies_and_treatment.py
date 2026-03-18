"""
Tests for Frequencies, Treatment Protocol, and Brain Categories.

No FalkorDB needed — constructs objects directly and tests logic.

DOCS: docs/care/frequencies/VALIDATION_Frequencies.md
      docs/care/treatment_protocol/VALIDATION_Treatment_Protocol.md
      docs/assessment/brain_topology/VALIDATION_Brain_Topology.md
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from services.health_assessment.brain_topology_reader import BrainStats
from services.health_assessment.universe_moment_reader import BehaviorStats
from services.health_assessment.frequencies import (
    Frequency,
    FrequencyResult,
    focus,
    calm,
    expand,
    root,
    surge,
    ambition,
    prescribe,
    FREQUENCY_CATALOG,
)
from services.health_assessment.intervention_composer import (
    compose_intervention,
)


# ── Helpers ──────────────────────────────────────────────────────────────────


def _brain(category: str, **overrides) -> BrainStats:
    """Build a BrainStats that lands in the given category."""
    profiles = {
        "VOID": dict(total_nodes=0, total_links=0, typed_node_count=0,
                      untyped_node_count=0, reachable=True),
        "MINIMAL": dict(total_nodes=3, total_links=0, typed_node_count=3,
                        untyped_node_count=0, health_feedback_count=3,
                        has_health_feedback=True,
                        type_distribution={"health_feedback": 3}, reachable=True),
        "SEEDED": dict(total_nodes=213, total_links=402, typed_node_count=4,
                       untyped_node_count=209, cluster_coefficient=0.009,
                       type_distribution={"backstory": 1, "universe": 1,
                                          "citizen": 1, "district": 1},
                       has_backstory=True, reachable=True),
        "STRUCTURED": dict(total_nodes=200, total_links=500, typed_node_count=50,
                           untyped_node_count=150, cluster_coefficient=0.3,
                           curiosity=0.5, ambition=0.4, social_need=0.3,
                           desire_count=8, concept_count=15, value_count=5,
                           process_count=7, reachable=True),
    }
    defaults = profiles[category]
    defaults.update(overrides)
    return BrainStats(**defaults)


def _behavior(**overrides) -> BehaviorStats:
    return BehaviorStats(**overrides)


# ── Brain Categories ─────────────────────────────────────────────────────────


class TestBrainCategories:
    """V2: Categories are mutually exclusive and cover all states."""

    def test_void(self):
        b = _brain("VOID")
        assert b.brain_category == "VOID"

    def test_minimal(self):
        b = _brain("MINIMAL")
        assert b.brain_category == "MINIMAL"

    def test_seeded(self):
        b = _brain("SEEDED")
        assert b.brain_category == "SEEDED"

    def test_structured(self):
        b = _brain("STRUCTURED")
        assert b.brain_category == "STRUCTURED"

    def test_unreachable_is_void(self):
        b = BrainStats(reachable=False)
        assert b.brain_category == "VOID"

    def test_small_no_links_is_minimal(self):
        b = BrainStats(total_nodes=5, total_links=0, reachable=True)
        assert b.brain_category == "MINIMAL"

    def test_large_untyped_is_seeded(self):
        b = BrainStats(total_nodes=100, total_links=200,
                       typed_node_count=2, untyped_node_count=98, reachable=True)
        assert b.brain_category == "SEEDED"

    def test_typed_with_drives_is_structured(self):
        b = BrainStats(total_nodes=100, total_links=200,
                       typed_node_count=20, curiosity=0.3, ambition=0.2,
                       social_need=0.1, reachable=True)
        assert b.brain_category == "STRUCTURED"


# ── Frequency Dataclass ──────────────────────────────────────────────────────


class TestFrequencyDataclass:
    """Frequency objects have the right fields and defaults."""

    def test_focus_defaults(self):
        f = focus()
        assert f.frequency_type == "focus"
        assert f.profile == "focalisant"
        assert f.brand == "graphcare"
        assert "curiosity" in f.target_drives
        assert f.duration_hours == 168

    def test_calm_negative_frustration(self):
        f = calm(0.4)
        assert f.target_drives["frustration"] == pytest.approx(-0.4)

    def test_root_has_structural_nodes(self):
        f = root()
        assert len(f.structural_nodes) == 5
        types = [n["type"] for n in f.structural_nodes]
        assert "desire" in types
        assert "concept" in types
        assert "value" in types
        assert "process" in types

    def test_root_is_permanent(self):
        f = root()
        assert f.duration_hours is None

    def test_surge_multi_drive(self):
        f = surge(0.2)
        assert len(f.target_drives) == 3
        assert f.target_drives["curiosity"] == pytest.approx(0.2)
        assert f.target_drives["ambition"] == pytest.approx(0.16)

    def test_custom_intensity(self):
        f = focus(0.8)
        assert f.target_drives["curiosity"] == pytest.approx(0.8)


# ── Catalog ──────────────────────────────────────────────────────────────────


class TestFrequencyCatalog:
    """Catalog contains all expected frequencies."""

    def test_catalog_has_6_entries(self):
        assert len(FREQUENCY_CATALOG) == 6

    def test_catalog_keys(self):
        expected = {"focus", "calm", "expand", "root", "surge", "ambition"}
        assert set(FREQUENCY_CATALOG.keys()) == expected

    def test_all_catalog_entries_return_frequency(self):
        for name, factory in FREQUENCY_CATALOG.items():
            f = factory() if name != "root" else factory()
            assert isinstance(f, Frequency), f"{name} didn't return Frequency"


# ── Auto-Prescription ────────────────────────────────────────────────────────


class TestPrescription:
    """Auto-prescription matches brain category to the right frequencies."""

    def test_void_gets_root_and_surge(self):
        b = _brain("VOID")
        freqs = prescribe(b.brain_category, b)
        types = [f.frequency_type for f in freqs]
        assert "root" in types
        assert "surge" in types

    def test_minimal_gets_root_and_focus(self):
        b = _brain("MINIMAL")
        freqs = prescribe(b.brain_category, b)
        types = [f.frequency_type for f in freqs]
        assert "root" in types
        assert "focus" in types

    def test_seeded_sparse_gets_root_focus_expand(self):
        b = _brain("SEEDED")
        freqs = prescribe(b.brain_category, b)
        types = [f.frequency_type for f in freqs]
        assert "root" in types      # typed_node_count < 10
        assert "focus" in types     # cluster_coefficient < 0.02
        assert "expand" in types    # social_need < 0.1

    def test_structured_frustrated_gets_calm(self):
        b = _brain("STRUCTURED", frustration=0.6)
        freqs = prescribe(b.brain_category, b)
        types = [f.frequency_type for f in freqs]
        assert "calm" in types

    def test_structured_healthy_gets_nothing(self):
        b = _brain("STRUCTURED", frustration=0.1, curiosity=0.5,
                   social_need=0.3, ambition=0.2)
        freqs = prescribe(b.brain_category, b)
        assert len(freqs) == 0

    def test_prescription_never_returns_none(self):
        for cat in ["VOID", "MINIMAL", "SEEDED", "STRUCTURED"]:
            b = _brain(cat)
            freqs = prescribe(b.brain_category, b)
            assert isinstance(freqs, list)
            for f in freqs:
                assert isinstance(f, Frequency)


# ── Intervention Composer: Stratification ────────────────────────────────────


class TestInterventionStratified:
    """Each brain category produces a different intervention message."""

    def _compose(self, brain: BrainStats) -> str:
        return compose_intervention(
            citizen_id="test",
            aggregate=5.0,
            yesterday_aggregate=None,
            drops=[],
            capability_scores={"exec_test_before_claim": 25.0},
            brain=brain,
            behavior=_behavior(),
        )

    def test_void_mentions_empty(self):
        msg = self._compose(_brain("VOID"))
        assert "[VOID]" in msg
        assert "empty" in msg.lower()

    def test_minimal_mentions_health_feedback(self):
        msg = self._compose(_brain("MINIMAL"))
        assert "[MINIMAL]" in msg

    def test_seeded_mentions_nodes_and_links(self):
        msg = self._compose(_brain("SEEDED"))
        assert "[SEEDED]" in msg
        assert "213 nodes" in msg
        assert "402 links" in msg

    def test_structured_mentions_drives(self):
        msg = self._compose(_brain("STRUCTURED"))
        assert "[STRUCTURED]" in msg
        assert "curiosity" in msg.lower()

    def test_all_messages_end_with_graphcare(self):
        for cat in ["VOID", "MINIMAL", "SEEDED", "STRUCTURED"]:
            msg = self._compose(_brain(cat))
            assert msg.strip().endswith("— GraphCare")

    def test_no_content_references(self):
        forbidden = ["your desire to", "you wrote", "the content of"]
        for cat in ["VOID", "MINIMAL", "SEEDED", "STRUCTURED"]:
            msg = self._compose(_brain(cat)).lower()
            for kw in forbidden:
                assert kw not in msg, f"[{cat}] contains '{kw}'"


# ── FrequencyResult ──────────────────────────────────────────────────────────


class TestFrequencyResult:
    """FrequencyResult reports success/failure correctly."""

    def test_success_with_nodes(self):
        r = FrequencyResult(success=True, nodes_created=3, node_ids=["a", "b", "c"])
        assert r.success
        assert r.nodes_created == 3

    def test_failure_with_error(self):
        r = FrequencyResult(success=False, nodes_created=0, error="connection refused")
        assert not r.success
        assert "connection" in r.error
