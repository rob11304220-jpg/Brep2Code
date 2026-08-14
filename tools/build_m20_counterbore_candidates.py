"""Build the preregistered M20-002 counterbore candidate assets offline.

This producer reads the frozen expansion record and writes only its three
counterbore candidates.  It does not touch manifests, the registry, corpus
inputs, provider inputs, or runtime resources.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

try:  # Supports both ``python tools/...`` and package import from tests.
    from tools.audit_sequence_paired_prismatic_hole import build_shape, load_json, write_step
except ModuleNotFoundError:  # pragma: no cover - direct script entrypoint only
    from audit_sequence_paired_prismatic_hole import build_shape, load_json, write_step
from brep2code.brep.probes import load_model, probe_summary


ROOT = Path(__file__).resolve().parents[1]
EXPANSION = ROOT / "docs/corpus/sequence-paired/prismatic-hole-v1-expansion.json"
CASE_ROOT = ROOT / "case-library/self-authored"
STEP_TIMESTAMP = re.compile(r"(FILE_NAME\('Open CASCADE Shape Model',)'[^']*'")
STEP_SESSION = re.compile(r"Open CASCADE STEP translator 7\.9 \d+")


def reference_script(sequence: dict[str, Any]) -> str:
    """Return a standalone deterministic OCP reference script for one candidate."""

    operations = sequence["operations"]
    sketch, base, cut = operations
    return f'''from pathlib import Path

from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.IFSelect import IFSelect_RetDone
from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt

SEQUENCE = {sequence!r}

base = BRepPrimAPI_MakeBox({sketch["length_x"]}, {sketch["length_y"]}, {base["distance"]}).Shape()
x, y = {cut["center_xy"]!r}
through = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(x, y, -1.0), gp_Dir(0.0, 0.0, 1.0)), {cut["through_radius"]}, {base["distance"] + 2.0}).Shape()
bore = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(x, y, {base["distance"] - cut["bore_depth"]}), gp_Dir(0.0, 0.0, 1.0)), {cut["bore_radius"]}, {cut["bore_depth"] + 1.0}).Shape()
shape = BRepAlgoAPI_Cut(BRepAlgoAPI_Cut(base, through).Shape(), bore).Shape()

Path("output").mkdir(exist_ok=True)
writer = STEPControl_Writer()
writer.Transfer(shape, STEPControl_AsIs)
if writer.Write("output/model.step") != IFSelect_RetDone:
    raise RuntimeError("failed to write STEP")
'''


def candidate_metadata(entry: dict[str, Any], digest: str, expected: dict[str, Any]) -> dict[str, Any]:
    sequence = entry["sequence"]
    cut = sequence["operations"][2]
    return {
        "case_id": entry["case_id"],
        "status": "active",
        "origin": "self_authored",
        "tier": "P2",
        "fixture_version": 1,
        "family_id": entry["family_id"],
        "data_split": entry["data_split"],
        "variant": entry["variant"],
        "parameters": {
            "x": cut["center_xy"][0],
            "through_radius": cut["through_radius"],
            "bore_radius": cut["bore_radius"],
            "bore_depth": cut["bore_depth"],
        },
        "input_step": "input.step",
        "reference_script": "reference_build_sequence.py",
        "reference_script_status": "available",
        "sha256": digest,
        "unit": "mm",
        "coordinate_frame": "right_handed_xyz; model origin at (0,0,0)",
        "summary": "M20-002 preregistered counterbore candidate; development-side evidence only.",
        "key_dimensions": {
            "length_x": sequence["operations"][0]["length_x"],
            "length_y": sequence["operations"][0]["length_y"],
            "height": sequence["operations"][1]["distance"],
            **cut,
        },
        "feature_tags": ["m20", "sequence-paired", "prismatic-hole", "counterbore", entry["variant"]],
        "case_directory": f"case-library/self-authored/{entry['case_id']}",
        "metadata_authority": "case.json",
        "expected": expected,
        "sequence_pair": {
            "grammar_version": "prismatic-hole-v1",
            "oracle_provenance": "self_authored_deterministic_reference",
            "sequence": sequence,
            "candidate_sequence": "candidate_sequence.json",
        },
        "admission_boundary": "Not listed in any executable manifest and not authorized for corpus, provider, training, or runtime use.",
    }


def normalize_step_header(path: Path) -> None:
    """Remove OCP's wall-clock timestamp so committed candidate bytes are stable."""

    text = path.read_text(encoding="utf-8")
    normalized, timestamp_substitutions = STEP_TIMESTAMP.subn(r"\1'2000-01-01T00:00:00'", text, count=1)
    normalized, session_substitutions = STEP_SESSION.subn("Open CASCADE STEP translator 7.9 stable", normalized)
    if timestamp_substitutions != 1 or session_substitutions != 2:
        raise RuntimeError(f"could not normalize STEP timestamp: {path}")
    path.write_text("\n".join(line.rstrip() for line in normalized.splitlines()) + "\n", encoding="utf-8", newline="\n")


def build(expansion_path: Path = EXPANSION) -> list[str]:
    expansion = load_json(expansion_path)
    if expansion.get("selection_status") != "preregistered":
        raise ValueError("counterbore production requires a preregistered expansion record")
    entries = [entry for entry in expansion["cases"] if entry["family_id"] == "counterbore"]
    if len(entries) != 3 or any(entry["data_split"] != "development" for entry in entries):
        raise ValueError("expansion must contain exactly three development counterbore candidates")
    produced: list[str] = []
    for entry in entries:
        directory = CASE_ROOT / entry["case_id"]
        directory.mkdir(parents=True, exist_ok=True)
        sequence = entry["sequence"]
        target = directory / "input.step"
        write_step(build_shape(sequence), target)
        normalize_step_header(target)
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        expected = probe_summary(load_model(target))
        (directory / "candidate_sequence.json").write_text(
            json.dumps({"grammar_version": expansion["grammar_version"], "sequence": sequence}, indent=2) + "\n",
            encoding="utf-8",
        )
        (directory / "case.json").write_text(
            json.dumps(candidate_metadata(entry, digest, expected), indent=2) + "\n", encoding="utf-8"
        )
        (directory / "reference_build_sequence.py").write_text(reference_script(sequence), encoding="utf-8")
        produced.append(entry["case_id"])
    return produced


def main() -> None:
    print(json.dumps({"produced": build(), "status": "unregistered_active_assets"}, indent=2))


if __name__ == "__main__":
    main()
