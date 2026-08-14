"""Build only M94's six preregistered through-hole candidates offline."""

from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

from brep2code.brep.probes import load_model, probe_summary

try:  # Supports both ``python tools/...`` and package import from tests.
    from tools.audit_sequence_paired_prismatic_hole import write_step
    from tools.audit_sequence_paired_reference_guided_through_hole_variation import EXPANSION, ROOT, build_shape, canonical_sequence
    from tools.build_m20_counterbore_candidates import normalize_step_header
except ModuleNotFoundError:  # pragma: no cover - direct script entrypoint only
    from audit_sequence_paired_prismatic_hole import write_step
    from audit_sequence_paired_reference_guided_through_hole_variation import EXPANSION, ROOT, build_shape, canonical_sequence
    from build_m20_counterbore_candidates import normalize_step_header


def _write(entry: dict[str, Any], path: Path) -> str:
    write_step(build_shape(entry), path)
    normalize_step_header(path)
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _stable(entry: dict[str, Any]) -> None:
    with tempfile.TemporaryDirectory(prefix="brep2code-m95-a-") as first, tempfile.TemporaryDirectory(prefix="brep2code-m95-b-") as second:
        left, right = Path(first) / "model.step", Path(second) / "model.step"
        if _write(entry, left) != _write(entry, right) or left.read_bytes() != right.read_bytes():
            raise RuntimeError(f"hash nondeterminism: {entry['case_id']}")


def _reference_script(entry: dict[str, Any]) -> str:
    sequence = canonical_sequence(entry)
    return f'''# Deterministic local oracle only. Not provider, runtime, or training input.
from pathlib import Path

from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.IFSelect import IFSelect_RetDone
from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt

SEQUENCE = {sequence!r}
base = BRepPrimAPI_MakeBox(30.0, 20.0, 10.0).Shape()
radius, x = {entry["parameters"]["radius"]!r}, {entry["parameters"]["x"]!r}
cutter = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(x, 10.0, -1.0), gp_Dir(0.0, 0.0, 1.0)), radius, 12.0).Shape()
shape = BRepAlgoAPI_Cut(base, cutter).Shape()
Path("output").mkdir(exist_ok=True)
writer = STEPControl_Writer()
writer.Transfer(shape, STEPControl_AsIs)
if writer.Write("output/model.step") != IFSelect_RetDone:
    raise RuntimeError("failed to write STEP")
'''


def _metadata(entry: dict[str, Any], digest: str, expected: dict[str, Any]) -> dict[str, Any]:
    return {
        "case_id": entry["case_id"],
        "status": "experimental",
        "origin": "self_authored",
        "tier": "P1",
        "fixture_version": 1,
        "family_id": entry["family_id"],
        "data_split": entry["data_split"],
        "variant": entry["variant"],
        "parameters": entry["parameters"],
        "input_step": "input.step",
        "reference_script_status": "available",
        "reference_script": "reference_build_sequence.py",
        "sha256": digest,
        "unit": "mm",
        "expected": expected,
        "sequence_pair": {"grammar_version": "reference-guided-through-hole-variation-v1", "oracle_provenance": "self_authored_deterministic_reference", "sequence": canonical_sequence(entry), "candidate_sequence": "candidate_sequence.json"},
        "admission_boundary": "Experimental candidate only; absent from manifest, provider, training, runtime and registry paths. Reference script and row parameters are local oracle material only.",
    }


def build(expansion_path: Path = EXPANSION, output_root: Path = ROOT) -> list[str]:
    record = json.loads(expansion_path.read_text(encoding="utf-8"))
    rows = record.get("cases")
    if record.get("selection_status") != "preregistered_before_candidate_production" or not isinstance(rows, list) or len(rows) != 6:
        raise ValueError("M95 production requires exactly six preregistered rows")
    produced = []
    for entry in rows:
        _stable(entry)
        directory = output_root / entry["candidate_directory"]
        directory.mkdir(parents=True, exist_ok=True)
        target = directory / "input.step"
        digest = _write(entry, target)
        expected = probe_summary(load_model(target))
        (directory / "candidate_sequence.json").write_text(json.dumps({"grammar_version": record["grammar_version"], "sequence": canonical_sequence(entry)}, indent=2) + "\n", encoding="utf-8")
        (directory / "case.json").write_text(json.dumps(_metadata(entry, digest, expected), indent=2) + "\n", encoding="utf-8")
        (directory / "reference_build_sequence.py").write_text(_reference_script(entry), encoding="utf-8")
        produced.append(entry["case_id"])
    return produced


if __name__ == "__main__":
    print(json.dumps({"produced": build(), "status": "experimental_candidates"}, indent=2))
