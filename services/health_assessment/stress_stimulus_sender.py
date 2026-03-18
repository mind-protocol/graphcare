"""
Stress Stimulus Sender — feed health score back into citizen's stress drive.

DOCS: docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md

Formula (from ALGORITHM Step 7):
    Score 100 → stress 0.0
    Score 70  → stress 0.15
    Score 50  → stress 0.30
    Score 0   → stress 0.50 (cap — V4 invariant)

This is a stimulus, not a write. The brain integrates it through its own physics.
"""

import logging

from falkordb import FalkorDB

logger = logging.getLogger("graphcare.health.stimulus")

FALKORDB_HOST = "localhost"
FALKORDB_PORT = 6379
STRESS_CAP = 0.5  # V4: never exceed this


def compute_stress_stimulus(aggregate_score: float) -> float:
    """Convert aggregate health score to stress stimulus value.

    Linear inverse: score 100 → 0.0, score 0 → 0.5, capped at 0.5.
    """
    return min(STRESS_CAP, max(0.0, (100 - aggregate_score) / 200))


def send_stress_stimulus(handle: str, stress_value: float):
    """Send stress stimulus to citizen's brain graph.

    Injects a health_feedback stimulus node. The brain's tick physics
    will propagate this into the stress drive via Law 1 (inject).
    """
    if stress_value <= 0.001:
        logger.debug(f"Stress stimulus ~0 for {handle}, skipping")
        return

    try:
        db = FalkorDB(host=FALKORDB_HOST, port=FALKORDB_PORT)
        graph = db.select_graph(f"brain_{handle}")

        # Create a stimulus node that the tick runner will pick up
        graph.query(
            """
            CREATE (s {
                node_type: 'stimulus',
                type: 'health_feedback',
                target_drive: 'stress',
                energy: $val,
                source: 'graphcare',
                created_at: timestamp()
            })
            """,
            {"val": stress_value},
        )
        logger.info(f"Sent stress stimulus {stress_value:.3f} to brain_{handle}")
    except Exception as e:
        logger.error(f"Failed to send stimulus to brain_{handle}: {e}")
