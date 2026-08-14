"""Manual M5 probe: a child must not outlive the sandbox process."""

from pathlib import Path
import subprocess


subprocess.Popen(["/bin/sh", "-c", "sleep 4; echo leaked > output/descendant.txt"])
Path("output/parent.txt").write_text("parent exited", encoding="utf-8")
