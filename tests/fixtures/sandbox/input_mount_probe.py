"""Manual M5 probe: the selected model is readable only at /input/model.step."""

from pathlib import Path


model = Path("/input/model.step")
print(f"input_readable={model.is_file()}; input_size={model.stat().st_size if model.is_file() else 0}")
if not model.is_file() or model.stat().st_size == 0:
    raise RuntimeError("sandbox input mount is unavailable")
