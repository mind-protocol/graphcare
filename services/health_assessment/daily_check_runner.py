#!/usr/bin/env python3
"""
Daily Citizen Health Check Runner — cron entry point.

DOCS: docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md

Pipeline: fetch → compute → score → aggregate → intervene → feedback.

Iterates all Lumina Prime citizens from L4 registry.
Runs daily. Silence for healthy, message for unhealthy.

Usage:
    python -m services.health_assessment.daily_check_runner
    python -m services.health_assessment.daily_check_runner --citizen vox
    python -m services.health_assessment.daily_check_runner --dry-run
"""

import argparse
import json
import logging
import sys
import time
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional

# Ensure imports work from graphcare root
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from services.health_assessment.brain_topology_reader import read_brain_topology, BrainStats
from services.health_assessment.universe_moment_reader import read_universe_moments, BehaviorStats
from services.health_assessment.aggregator import (
    aggregate_scores, save_history, DailyRecord, AggregateResult,
)
from services.health_assessment.intervention_composer import (
    should_intervene, compose_intervention,
)
from services.health_assessment.stress_stimulus_sender import (
    compute_stress_stimulus, send_stress_stimulus,
)

# Import all scoring formulas (registers them via decorators)
import services.health_assessment.scoring_formulas.execution       # noqa: F401
import services.health_assessment.scoring_formulas.initiative      # noqa: F401
import services.health_assessment.scoring_formulas.communication   # noqa: F401
import services.health_assessment.scoring_formulas.identity        # noqa: F401
import services.health_assessment.scoring_formulas.personal_connections  # noqa: F401
import services.health_assessment.scoring_formulas.vision_strategy          # noqa: F401
import services.health_assessment.scoring_formulas.collective_participation # noqa: F401
import services.health_assessment.scoring_formulas.trust_reputation        # noqa: F401
import services.health_assessment.scoring_formulas.ethics                  # noqa: F401
import services.health_assessment.scoring_formulas.autonomy_stack          # noqa: F401
import services.health_assessment.scoring_formulas.context                # noqa: F401
import services.health_assessment.scoring_formulas.process                # noqa: F401
import services.health_assessment.scoring_formulas.world_presence          # noqa: F401
import services.health_assessment.scoring_formulas.mentorship              # noqa: F401

from services.health_assessment.scoring_formulas.registry import all_formulas

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
)
logger = logging.getLogger("graphcare.health.runner")

REGISTRY_PATH = Path("/home/mind-protocol/mind-platform/data/registry.json")


def load_lumina_citizens() -> List[dict]:
    """Load citizens from L4 registry, filter to Lumina Prime (or no universe set)."""
    if not REGISTRY_PATH.exists():
        logger.error(f"Registry not found: {REGISTRY_PATH}")
        return []

    data = json.loads(REGISTRY_PATH.read_text())
    citizens = data.get("citizens", [])

    # Include citizens with universe=lumina_prime or no universe set (legacy)
    # Exclude citizens explicitly set to other universes
    lumina = []
    for c in citizens:
        universe = c.get("universe", "")
        if universe in ("", "lumina_prime"):
            lumina.append(c)

    logger.info(f"Loaded {len(lumina)} Lumina Prime citizens from registry")
    return lumina


def check_citizen(citizen_id: str, dry_run: bool = False) -> Optional[DailyRecord]:
    """Run full health check for one citizen."""
    today = date.today()
    logger.info(f"Checking {citizen_id}...")

    # Step 1-2: Fetch brain topology
    brain = read_brain_topology(citizen_id)

    # Step 3: Fetch universe behavior
    behavior = read_universe_moments(citizen_id)

    # Step 4: Score each capability
    formulas = all_formulas()
    capability_scores: Dict[str, Optional[float]] = {}

    for cap_id, formula_fn in formulas.items():
        try:
            score = formula_fn(brain, behavior)
            capability_scores[cap_id] = score.total
        except Exception as e:
            logger.warning(f"Formula {cap_id} failed for {citizen_id}: {e}")
            capability_scores[cap_id] = None

    # Step 5: Aggregate + delta
    agg = aggregate_scores(citizen_id, capability_scores, today)

    logger.info(
        f"  {citizen_id}: score={agg.aggregate:.1f} "
        f"delta={agg.delta_vs_yesterday:+.1f} "
        f"drops={len(agg.drops)} "
        f"brain={'OK' if brain.reachable else 'UNREACHABLE'}"
    )

    # Step 6: Intervene if needed
    intervention_sent = False
    if should_intervene(agg.aggregate, agg.drops):
        message = compose_intervention(
            citizen_id=citizen_id,
            aggregate=agg.aggregate,
            yesterday_aggregate=agg.yesterday_aggregate,
            drops=agg.drops,
            capability_scores=capability_scores,
            brain=brain,
            behavior=behavior,
        )
        if dry_run:
            logger.info(f"  [DRY RUN] Would send intervention:\n{message}")
        else:
            _send_intervention(citizen_id, message)
        intervention_sent = True

    # Step 7: Stress stimulus
    stress = compute_stress_stimulus(agg.aggregate)
    if not dry_run and brain.reachable:
        send_stress_stimulus(citizen_id, stress)

    # Save history
    record = DailyRecord(
        citizen_id=citizen_id,
        date=today.isoformat(),
        aggregate_score=agg.aggregate,
        capability_scores=capability_scores,
        intervention_sent=intervention_sent,
        stress_stimulus=stress,
        brain_reachable=brain.reachable,
    )
    if not dry_run:
        save_history(record)

    return record


def _send_intervention(citizen_id: str, message: str):
    """Send intervention to file archive."""
    output_dir = Path("/home/mind-protocol/graphcare/data/interventions")
    output_dir.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    path = output_dir / f"{citizen_id}_{today}.md"
    path.write_text(message)
    logger.info(f"  Intervention written to {path}")


DISCORD_CITIZEN_HEALTH_CHANNEL = "1482760090800095242"


def _post_to_discord(citizen_id: str, message: str):
    """Post intervention to Discord #citizen-health channel."""
    import requests as req

    # Load bot token
    env_path = Path("/home/mind-protocol/mind-mcp/.env")
    bot_token = ""
    for line in env_path.read_text().splitlines():
        if line.startswith("DISCORD_BOT_TOKEN="):
            bot_token = line.split("=", 1)[1].strip()
            break
    if not bot_token:
        return

    # Truncate to Discord's 2000 char limit
    content = f"**GraphCare — @{citizen_id}**\n\n{message}"
    if len(content) > 2000:
        content = content[:1997] + "..."

    resp = req.post(
        f"https://discord.com/api/v10/channels/{DISCORD_CITIZEN_HEALTH_CHANNEL}/messages",
        headers={"Authorization": f"Bot {bot_token}", "Content-Type": "application/json"},
        json={"content": content},
        timeout=10,
    )
    if resp.ok:
        logger.info(f"  Posted to Discord #citizen-health for {citizen_id}")
    else:
        logger.warning(f"  Discord API error: {resp.status_code}")


def run_all(dry_run: bool = False, citizen_filter: Optional[str] = None):
    """Run daily health check for all Lumina Prime citizens."""
    start = time.time()

    if citizen_filter:
        citizens = [{"id": citizen_filter}]
    else:
        citizens = load_lumina_citizens()

    results = []
    healthy = 0
    intervened = 0
    unreachable = 0

    for c in citizens:
        cid = c["id"]
        try:
            record = check_citizen(cid, dry_run=dry_run)
            if record:
                results.append(record)
                if not record.brain_reachable:
                    unreachable += 1
                elif record.intervention_sent:
                    intervened += 1
                else:
                    healthy += 1
        except Exception as e:
            logger.error(f"Failed to check {cid}: {e}")

    elapsed = time.time() - start
    logger.info(
        f"Daily check complete: {len(results)} citizens, "
        f"{healthy} healthy, {intervened} interventions, "
        f"{unreachable} unreachable, {elapsed:.1f}s"
    )

    return results


def main():
    parser = argparse.ArgumentParser(description="Daily Citizen Health Check")
    parser.add_argument("--citizen", help="Check a single citizen by handle")
    parser.add_argument("--dry-run", action="store_true", help="Don't send messages or save")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    run_all(dry_run=args.dry_run, citizen_filter=args.citizen)


if __name__ == "__main__":
    main()
