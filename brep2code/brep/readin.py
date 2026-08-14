"""Input discovery and STEP read-in helpers."""

from __future__ import annotations

from pathlib import Path


SUPPORTED_INPUT_EXTENSIONS = (".step", ".stp", ".iges", ".igs", ".brep")


def discover_input_file(input_dir: Path) -> Path:
    """Return the single supported CAD input in a record input directory."""

    if not input_dir.exists():
        raise FileNotFoundError(f"input directory does not exist: {input_dir}")
    candidates = sorted(
        path
        for path in input_dir.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_INPUT_EXTENSIONS
    )
    if not candidates:
        raise FileNotFoundError(f"no supported CAD input found in: {input_dir}")
    if len(candidates) > 1:
        names = ", ".join(path.name for path in candidates)
        raise ValueError(f"expected one CAD input in {input_dir}, found {len(candidates)}: {names}")
    return candidates[0]


def input_format(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in (".step", ".stp"):
        return "step"
    if suffix in (".iges", ".igs"):
        return "iges"
    if suffix == ".brep":
        return "brep"
    return "unknown"
