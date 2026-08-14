"""Manual M5 probe: a denied write is reported as a structured sandbox event."""

from pathlib import Path


Path("outside-output.txt").write_text("forbidden", encoding="utf-8")
