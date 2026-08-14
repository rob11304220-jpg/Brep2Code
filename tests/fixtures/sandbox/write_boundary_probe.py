"""Manual M5 probe: script and workspace root are read-only."""

from pathlib import Path


blocked: list[str] = []
for path in (Path("build_sequence.py"), Path("outside-output.txt")):
    try:
        path.write_text("forbidden", encoding="utf-8")
    except OSError:
        blocked.append(path.name)

print(f"blocked={sorted(blocked)}")
if sorted(blocked) != ["build_sequence.py", "outside-output.txt"]:
    raise RuntimeError(f"workspace write boundary failed: {blocked}")
