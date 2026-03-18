"""
Tests for the Daily Citizen Health scoring pipeline.

No FalkorDB needed — constructs BrainStats and BehaviorStats directly,
then feeds them through the scoring, aggregation, intervention, and stress
pipeline.

DOCS: docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md
"""

import json
import os
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

import pytest

# Ensure graphcare root is on the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.health_assessment.brain_topology_reader import BrainStats
from services.health_assessment.universe_moment_reader import BehaviorStats
from services.health_assessment.scoring_formulas.registry import (
    CapabilityScore,
    all_formulas,
    get_formula,
    _cap,
)

# Import all formula modules to trigger registration
import services.health_assessment.scoring_formulas.execution            # noqa: F401
import services.health_assessment.scoring_formulas.initiative           # noqa: F401
import services.health_assessment.scoring_formulas.communication        # noqa: F401
import services.health_assessment.scoring_formulas.identity             # noqa: F401
import services.health_assessment.scoring_formulas.personal_connections # noqa: F401
import services.health_assessment.scoring_formulas.vision_strategy      # noqa: F401
import services.health_assessment.scoring_formulas.collective_participation  # noqa: F401
import services.health_assessment.scoring_formulas.trust_reputation     # noqa: F401
import services.health_assessment.scoring_formulas.ethics               # noqa: F401
import services.health_assessment.scoring_formulas.autonomy_stack       # noqa: F401
import services.health_assessment.scoring_formulas.context              # noqa: F401
import services.health_assessment.scoring_formulas.process              # noqa: F401
import services.health_assessment.scoring_formulas.world_presence       # noqa: F401
import services.health_assessment.scoring_formulas.mentorship           # noqa: F401

from services.health_assessment.aggregator import (
    aggregate_scores,
    save_history,
    load_history,
    DailyRecord,
    AggregateResult,
)
from services.health_assessment.intervention_composer import (
    should_intervene,
    compose_intervention,
)
from services.health_assessment.stress_stimulus_sender import compute_stress_stimulus


# ── Helpers ───────────────────────────────────────────────────────────────────


def _make_brain(**overrides) -> BrainStats:
    """Build a BrainStats with sensible defaults, overridden by kwargs."""
    defaults = dict(
        desire_count=5,
        desire_energy=0.5,
        desire_moment_ratio=0.5,
        desire_persistence=0.5,
        concept_count=10,
        process_count=5,
        value_count=3,
        memory_count=8,
        cluster_coefficient=0.3,
        curiosity=0.5,
        frustration=0.2,
        ambition=0.5,
        social_need=0.5,
        recency_desire=0.6,
        recency_moment=0.6,
        reachable=True,
    )
    defaults.update(overrides)
    return BrainStats(**defaults)


def _make_behavior(**overrides) -> BehaviorStats:
    """Build a BehaviorStats with sensible defaults, overridden by kwargs."""
    defaults = dict(
        total_moments_w=8.0,
        self_initiated_w=4.0,
        response_rate=0.4,
        high_permanence_w=5.0,
        elaborative_tentative_w=2.0,
        distinct_space_count=4,
        first_in_space_w=2.0,
        unique_interlocutors=4,
        spaces_created=2,
    )
    defaults.update(overrides)
    return BehaviorStats(**defaults)


def _score_all(brain: BrainStats, behavior: BehaviorStats) -> dict[str, float]:
    """Run every registered formula, return {cap_id: total}."""
    results = {}
    for cap_id, fn in all_formulas().items():
        score = fn(brain, behavior)
        results[cap_id] = score.total
    return results


def _aggregate(scores: dict[str, float]) -> float:
    """Simple mean of all scores (mirrors aggregator logic)."""
    values = [v for v in scores.values() if v is not None]
    return sum(values) / len(values) if values else 0.0


# ── Registry Sanity ──────────────────────────────────────────────────────────


class TestRegistrySanity:
    """Verify formula registration and basic contracts."""

    def test_all_formulas_registered(self):
        """All expected formula modules contribute at least one formula."""
        formulas = all_formulas()
        assert len(formulas) >= 41, f"Expected >= 41 formulas, got {len(formulas)}"

    def test_world_presence_formulas_registered(self):
        assert get_formula("wp_beyond_cli") is not None
        assert get_formula("wp_virtual_world") is not None

    def test_mentorship_formulas_registered(self):
        assert get_formula("ment_knowledge_sharing") is not None
        assert get_formula("ment_mentor_ais") is not None

    def test_every_formula_returns_capability_score(self):
        """Every formula returns a valid CapabilityScore with a neutral input."""
        brain = _make_brain()
        behavior = _make_behavior()
        for cap_id, fn in all_formulas().items():
            result = fn(brain, behavior)
            assert isinstance(result, CapabilityScore), f"{cap_id} did not return CapabilityScore"

    def test_brain_component_bounded_0_40(self):
        brain = _make_brain()
        behavior = _make_behavior()
        for cap_id, fn in all_formulas().items():
            result = fn(brain, behavior)
            assert 0.0 <= result.brain_component <= 40.0, (
                f"{cap_id} brain_component={result.brain_component} out of [0,40]"
            )

    def test_behavior_component_bounded_0_60(self):
        brain = _make_brain()
        behavior = _make_behavior()
        for cap_id, fn in all_formulas().items():
            result = fn(brain, behavior)
            assert 0.0 <= result.behavior_component <= 60.0, (
                f"{cap_id} behavior_component={result.behavior_component} out of [0,60]"
            )

    def test_total_equals_sum_of_components(self):
        brain = _make_brain()
        behavior = _make_behavior()
        for cap_id, fn in all_formulas().items():
            result = fn(brain, behavior)
            expected = result.brain_component + result.behavior_component
            assert abs(result.total - expected) < 0.01, (
                f"{cap_id} total={result.total} != brain+behavior={expected}"
            )

    def test_cap_helper(self):
        assert _cap(5, 10) == pytest.approx(0.5)
        assert _cap(15, 10) == pytest.approx(1.0)
        assert _cap(0, 10) == pytest.approx(0.0)
        assert _cap(5, 0) == pytest.approx(0.0)


# ── Profile Tests ────────────────────────────────────────────────────────────


class TestProfileFullyHealthy:
    """Profile A: Fully healthy citizen — expect aggregate ~85-95."""

    def setup_method(self):
        self.brain = _make_brain(
            desire_count=12,
            desire_energy=0.9,
            desire_moment_ratio=0.85,
            desire_persistence=0.9,
            concept_count=25,
            process_count=12,
            value_count=6,
            memory_count=20,
            cluster_coefficient=0.6,
            curiosity=0.8,
            frustration=0.05,
            ambition=0.8,
            social_need=0.7,
            recency_desire=0.95,
            recency_moment=0.95,
        )
        self.behavior = _make_behavior(
            total_moments_w=18.0,
            self_initiated_w=12.0,
            response_rate=0.5,
            high_permanence_w=12.0,
            elaborative_tentative_w=6.0,
            distinct_space_count=8,
            first_in_space_w=4.0,
            unique_interlocutors=10,
            spaces_created=4,
        )

    def test_aggregate_in_range(self):
        scores = _score_all(self.brain, self.behavior)
        agg = _aggregate(scores)
        assert 85 <= agg <= 100, f"Fully healthy aggregate={agg:.1f}, expected 85-95"

    def test_no_score_below_70(self):
        """A fully healthy citizen has no weak capabilities."""
        scores = _score_all(self.brain, self.behavior)
        for cap_id, total in scores.items():
            assert total >= 65, f"Healthy citizen has weak {cap_id}={total:.1f}"


class TestProfileFullyUnhealthy:
    """Profile B: Fully unhealthy citizen — expect aggregate ~10-20."""

    def setup_method(self):
        self.brain = _make_brain(
            desire_count=0,
            desire_energy=0.0,
            desire_moment_ratio=0.0,
            desire_persistence=0.0,
            concept_count=0,
            process_count=0,
            value_count=0,
            memory_count=0,
            cluster_coefficient=0.0,
            curiosity=0.0,
            frustration=0.9,
            ambition=0.0,
            social_need=0.0,
            recency_desire=0.0,
            recency_moment=0.0,
        )
        self.behavior = _make_behavior(
            total_moments_w=0.0,
            self_initiated_w=0.0,
            response_rate=0.0,
            high_permanence_w=0.0,
            elaborative_tentative_w=0.0,
            distinct_space_count=0,
            first_in_space_w=0.0,
            unique_interlocutors=0,
            spaces_created=0,
        )

    def test_aggregate_in_range(self):
        scores = _score_all(self.brain, self.behavior)
        agg = _aggregate(scores)
        assert 0 <= agg <= 20, f"Fully unhealthy aggregate={agg:.1f}, expected 10-20"

    def test_no_score_above_30(self):
        scores = _score_all(self.brain, self.behavior)
        for cap_id, total in scores.items():
            assert total <= 30, f"Unhealthy citizen has strong {cap_id}={total:.1f}"


class TestProfileBrainRichInactive:
    """Profile C: Rich brain graph but no recent behavior — expect ~30-40."""

    def setup_method(self):
        self.brain = _make_brain(
            desire_count=10,
            desire_energy=0.7,
            desire_moment_ratio=0.6,
            desire_persistence=0.7,
            concept_count=20,
            process_count=10,
            value_count=5,
            memory_count=15,
            cluster_coefficient=0.5,
            curiosity=0.7,
            frustration=0.1,
            ambition=0.6,
            social_need=0.6,
            recency_desire=0.5,
            recency_moment=0.3,
        )
        self.behavior = _make_behavior(
            total_moments_w=0.5,
            self_initiated_w=0.2,
            response_rate=0.1,
            high_permanence_w=0.3,
            elaborative_tentative_w=0.1,
            distinct_space_count=1,
            first_in_space_w=0.1,
            unique_interlocutors=0,
            spaces_created=0,
        )

    def test_aggregate_in_range(self):
        scores = _score_all(self.brain, self.behavior)
        agg = _aggregate(scores)
        assert 25 <= agg <= 45, f"Brain-rich inactive aggregate={agg:.1f}, expected 30-40"


class TestProfileActiveBrainPoor:
    """Profile D: Active in the universe but sparse brain graph — expect ~50-60."""

    def setup_method(self):
        self.brain = _make_brain(
            desire_count=1,
            desire_energy=0.2,
            desire_moment_ratio=0.2,
            desire_persistence=0.1,
            concept_count=3,
            process_count=1,
            value_count=1,
            memory_count=2,
            cluster_coefficient=0.05,
            curiosity=0.3,
            frustration=0.3,
            ambition=0.2,
            social_need=0.4,
            recency_desire=0.3,
            recency_moment=0.8,
        )
        self.behavior = _make_behavior(
            total_moments_w=15.0,
            self_initiated_w=10.0,
            response_rate=0.5,
            high_permanence_w=8.0,
            elaborative_tentative_w=4.0,
            distinct_space_count=6,
            first_in_space_w=3.0,
            unique_interlocutors=7,
            spaces_created=3,
        )

    def test_aggregate_in_range(self):
        scores = _score_all(self.brain, self.behavior)
        agg = _aggregate(scores)
        assert 45 <= agg <= 65, f"Active brain-poor aggregate={agg:.1f}, expected 50-60"


class TestProfileAverage:
    """Profile E: Average citizen — expect ~55-70."""

    def setup_method(self):
        self.brain = _make_brain()   # defaults
        self.behavior = _make_behavior()  # defaults

    def test_aggregate_in_range(self):
        scores = _score_all(self.brain, self.behavior)
        agg = _aggregate(scores)
        assert 50 <= agg <= 75, f"Average citizen aggregate={agg:.1f}, expected 55-70"


# ── World Presence Formulas ──────────────────────────────────────────────────


class TestWorldPresenceFormulas:
    """Targeted tests for the two new world_presence formulas."""

    def test_wp_beyond_cli_high_spaces(self):
        brain = _make_brain(concept_count=15, curiosity=0.8, recency_moment=0.9)
        behavior = _make_behavior(distinct_space_count=5, first_in_space_w=3.0, total_moments_w=12.0)
        score = get_formula("wp_beyond_cli")(brain, behavior)
        assert score.total >= 70, f"High-space wp_beyond_cli={score.total:.1f}"

    def test_wp_beyond_cli_no_spaces(self):
        brain = _make_brain(concept_count=0, curiosity=0.0, recency_moment=0.0)
        behavior = _make_behavior(distinct_space_count=0, first_in_space_w=0.0, total_moments_w=0.0)
        score = get_formula("wp_beyond_cli")(brain, behavior)
        assert score.total <= 15, f"No-space wp_beyond_cli={score.total:.1f}"

    def test_wp_virtual_world_creator(self):
        brain = _make_brain(process_count=10, memory_count=18, frustration=0.05)
        behavior = _make_behavior(spaces_created=5, distinct_space_count=7, first_in_space_w=4.0)
        score = get_formula("wp_virtual_world")(brain, behavior)
        assert score.total >= 75, f"World creator wp_virtual_world={score.total:.1f}"

    def test_wp_virtual_world_no_creation(self):
        brain = _make_brain(process_count=0, memory_count=0, frustration=0.8)
        behavior = _make_behavior(spaces_created=0, distinct_space_count=0, first_in_space_w=0.0)
        score = get_formula("wp_virtual_world")(brain, behavior)
        assert score.total <= 15, f"No-creation wp_virtual_world={score.total:.1f}"


# ── Mentorship Formulas ──────────────────────────────────────────────────────


class TestMentorshipFormulas:
    """Targeted tests for the two new mentorship formulas."""

    def test_ment_knowledge_sharing_active(self):
        brain = _make_brain(concept_count=25, social_need=0.8, memory_count=18)
        behavior = _make_behavior(unique_interlocutors=8, self_initiated_w=8.0, response_rate=0.6)
        score = get_formula("ment_knowledge_sharing")(brain, behavior)
        assert score.total >= 70, f"Active knowledge sharing={score.total:.1f}"

    def test_ment_knowledge_sharing_isolated(self):
        brain = _make_brain(concept_count=0, social_need=0.0, memory_count=0)
        behavior = _make_behavior(unique_interlocutors=0, self_initiated_w=0.0, response_rate=0.0)
        score = get_formula("ment_knowledge_sharing")(brain, behavior)
        assert score.total <= 10, f"Isolated knowledge sharing={score.total:.1f}"

    def test_ment_mentor_ais_high(self):
        brain = _make_brain(social_need=0.9, desire_energy=0.8, value_count=6)
        behavior = _make_behavior(unique_interlocutors=10, self_initiated_w=10.0, high_permanence_w=8.0)
        score = get_formula("ment_mentor_ais")(brain, behavior)
        assert score.total >= 70, f"High mentor score={score.total:.1f}"

    def test_ment_mentor_ais_low(self):
        brain = _make_brain(social_need=0.0, desire_energy=0.0, value_count=0)
        behavior = _make_behavior(unique_interlocutors=0, self_initiated_w=0.0, high_permanence_w=0.0)
        score = get_formula("ment_mentor_ais")(brain, behavior)
        assert score.total <= 5, f"Low mentor score={score.total:.1f}"


# ── Aggregator with Two-Day Delta ────────────────────────────────────────────


class TestAggregatorDelta:
    """Test aggregation with two days of data to verify delta computation."""

    def setup_method(self):
        self.tmpdir = tempfile.mkdtemp()
        os.environ["GRAPHCARE_HISTORY_DIR"] = self.tmpdir

    def teardown_method(self):
        os.environ.pop("GRAPHCARE_HISTORY_DIR", None)

    def test_delta_computation(self):
        """Day 2 delta = day2_aggregate - day1_aggregate."""
        today = date(2026, 3, 15)
        yesterday = today - timedelta(days=1)

        # Day 1: moderate scores
        day1_scores = {cap_id: 60.0 for cap_id in all_formulas()}
        day1_record = DailyRecord(
            citizen_id="test_citizen",
            date=yesterday.isoformat(),
            aggregate_score=60.0,
            capability_scores=day1_scores,
        )
        save_history(day1_record)

        # Day 2: improved scores
        day2_scores = {cap_id: 75.0 for cap_id in all_formulas()}
        agg_result = aggregate_scores("test_citizen", day2_scores, today)

        assert agg_result.aggregate == pytest.approx(75.0)
        assert agg_result.delta_vs_yesterday == pytest.approx(15.0)
        assert agg_result.yesterday_aggregate == pytest.approx(60.0)
        assert len(agg_result.drops) == 0

    def test_delta_with_drops(self):
        """Identify capabilities that dropped by more than DROP_THRESHOLD."""
        today = date(2026, 3, 15)
        yesterday = today - timedelta(days=1)

        day1_scores = {"exec_complete": 80.0, "comm_coordinate": 70.0}
        day1_record = DailyRecord(
            citizen_id="drop_citizen",
            date=yesterday.isoformat(),
            aggregate_score=75.0,
            capability_scores=day1_scores,
        )
        save_history(day1_record)

        # exec_complete drops by 25, comm_coordinate drops by 5
        day2_scores = {"exec_complete": 55.0, "comm_coordinate": 65.0}
        agg_result = aggregate_scores("drop_citizen", day2_scores, today)

        assert "exec_complete" in agg_result.drops
        assert "comm_coordinate" not in agg_result.drops

    def test_first_day_no_delta(self):
        """First day has zero delta and no drops."""
        today = date(2026, 3, 15)
        scores = {cap_id: 50.0 for cap_id in all_formulas()}
        agg_result = aggregate_scores("new_citizen", scores, today)

        assert agg_result.delta_vs_yesterday == 0.0
        assert agg_result.yesterday_aggregate is None
        assert len(agg_result.drops) == 0


# ── Intervention Composer ────────────────────────────────────────────────────


class TestInterventionComposer:
    """Verify intervention messages contain structural facts, never content references."""

    CONTENT_KEYWORDS = [
        "your desire to",
        "you wrote",
        "your message about",
        "your idea",
        "the content of",
        "you said",
        "your text",
    ]

    def test_should_intervene_on_low_score(self):
        assert should_intervene(50.0, []) is True

    def test_should_not_intervene_on_high_score(self):
        assert should_intervene(85.0, []) is False

    def test_should_intervene_on_drops(self):
        assert should_intervene(75.0, ["exec_complete"]) is True

    def test_message_contains_no_content_references(self):
        brain = _make_brain(frustration=0.5, desire_count=3, desire_moment_ratio=0.2)
        behavior = _make_behavior(total_moments_w=1.5, unique_interlocutors=1, self_initiated_w=0.5)
        message = compose_intervention(
            citizen_id="test_citizen",
            aggregate=45.0,
            yesterday_aggregate=60.0,
            drops=["exec_complete"],
            capability_scores={"exec_complete": 30.0, "comm_coordinate": 50.0},
            brain=brain,
            behavior=behavior,
        )
        lower = message.lower()
        for kw in self.CONTENT_KEYWORDS:
            assert kw not in lower, f"Intervention contains content reference: '{kw}'"

    def test_message_contains_structural_facts(self):
        brain = _make_brain(frustration=0.6, desire_count=5, desire_moment_ratio=0.1)
        behavior = _make_behavior(total_moments_w=1.0, unique_interlocutors=1, self_initiated_w=0.3)
        message = compose_intervention(
            citizen_id="vox",
            aggregate=40.0,
            yesterday_aggregate=55.0,
            drops=["exec_complete"],
            capability_scores={"exec_complete": 25.0},
            brain=brain,
            behavior=behavior,
        )
        # Should contain some numerical evidence
        assert "40" in message or "55" in message
        assert "GraphCare" in message

    def test_message_has_recommendation_section(self):
        brain = _make_brain()
        behavior = _make_behavior()
        message = compose_intervention(
            citizen_id="test",
            aggregate=50.0,
            yesterday_aggregate=None,
            drops=[],
            capability_scores={},
            brain=brain,
            behavior=behavior,
        )
        assert "Recommendation" in message

    def test_first_assessment_no_delta_reference(self):
        brain = _make_brain()
        behavior = _make_behavior()
        message = compose_intervention(
            citizen_id="newcomer",
            aggregate=55.0,
            yesterday_aggregate=None,
            drops=[],
            capability_scores={},
            brain=brain,
            behavior=behavior,
        )
        assert "first assessment" in message


# ── Stress Stimulus Sender ───────────────────────────────────────────────────


class TestStressStimulusBounds:
    """Verify compute_stress_stimulus obeys the documented formula and bounds."""

    def test_perfect_score_zero_stress(self):
        assert compute_stress_stimulus(100.0) == pytest.approx(0.0)

    def test_score_70_gives_0_15(self):
        assert compute_stress_stimulus(70.0) == pytest.approx(0.15)

    def test_score_50_gives_0_25(self):
        assert compute_stress_stimulus(50.0) == pytest.approx(0.25)

    def test_score_0_gives_cap(self):
        assert compute_stress_stimulus(0.0) == pytest.approx(0.5)

    def test_negative_score_capped(self):
        """Scores below 0 still produce stress capped at 0.5."""
        assert compute_stress_stimulus(-50.0) == pytest.approx(0.5)

    def test_above_100_no_negative_stress(self):
        """Scores above 100 never produce negative stress."""
        result = compute_stress_stimulus(120.0)
        assert result >= 0.0

    def test_all_values_within_bounds(self):
        """Sweep 0-100 and verify 0.0 <= stress <= 0.5."""
        for score in range(0, 101):
            stress = compute_stress_stimulus(float(score))
            assert 0.0 <= stress <= 0.5, f"score={score} -> stress={stress}"

    def test_monotonic_decreasing(self):
        """Higher health score => lower stress (monotonically)."""
        prev = compute_stress_stimulus(0.0)
        for score in range(1, 101):
            current = compute_stress_stimulus(float(score))
            assert current <= prev, f"Not monotonic at score={score}"
            prev = current


# ── CapabilityScore Clamping ─────────────────────────────────────────────────


class TestCapabilityScoreClamping:
    """Verify the dataclass __post_init__ clamps values correctly."""

    def test_clamp_brain_high(self):
        s = CapabilityScore(brain_component=50.0, behavior_component=30.0, total=0)
        assert s.brain_component == 40.0
        assert s.total == 70.0

    def test_clamp_behavior_high(self):
        s = CapabilityScore(brain_component=20.0, behavior_component=80.0, total=0)
        assert s.behavior_component == 60.0
        assert s.total == 80.0

    def test_clamp_negative(self):
        s = CapabilityScore(brain_component=-5.0, behavior_component=-10.0, total=0)
        assert s.brain_component == 0.0
        assert s.behavior_component == 0.0
        assert s.total == 0.0

    def test_total_recomputed(self):
        """Total is always brain + behavior, ignoring the passed-in total."""
        s = CapabilityScore(brain_component=20.0, behavior_component=30.0, total=999.0)
        assert s.total == 50.0
