#!/usr/bin/env python3
"""Basic encryption posture checks for FalkorDB integration endpoints."""

from __future__ import annotations

import os
import sys
from urllib.parse import urlparse


def check_url(name: str, expected_secure_schemes: set[str]) -> tuple[bool, str]:
    value = os.getenv(name)
    if not value:
        return False, f"{name} missing"

    parsed = urlparse(value)
    if parsed.scheme not in expected_secure_schemes:
        return False, f"{name} uses insecure scheme '{parsed.scheme}'"

    return True, f"{name} OK ({parsed.scheme})"


def main() -> int:
    checks = [
        check_url("FALKORDB_API_URL", {"https"}),
        check_url("GRAPH_EVENTS_WS", {"wss", "ws"}),
    ]

    ok = True
    for passed, msg in checks:
        print(("PASS" if passed else "FAIL") + f": {msg}")
        ok = ok and passed

    if not ok:
        print("Encryption posture check failed.")
        return 1

    print("Encryption posture check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
