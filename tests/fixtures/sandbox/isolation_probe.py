"""Manual M5 probe: it must run only through ``--executor wsl-bwrap``."""

from __future__ import annotations

import json
import os
from pathlib import Path
import socket


def _network_blocked() -> bool:
    try:
        with socket.create_connection(("1.1.1.1", 53), timeout=1):
            return False
    except OSError:
        return True


payload = {
    "repository_hidden": not Path("/mnt/d/codeai/Brep2Code/AGENTS.md").exists(),
    "ambient_secret_hidden": "BREP2CODE_TEST_SECRET" not in os.environ,
    "network_blocked": _network_blocked(),
}
print(json.dumps(payload, sort_keys=True))
if not all(payload.values()):
    raise RuntimeError(f"sandbox isolation probe failed: {payload}")
