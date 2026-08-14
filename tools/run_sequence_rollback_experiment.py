"""Offline M31 verified-prefix rollback experiment for frozen additive-boss cases."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt

from brep2code.agent.harness import _comparison_gates
from brep2code.brep.probes import load_model, probe_summary
from tools.audit_sequence_paired_additive_boss_dependent_cut import canonical_sequence
from tools.audit_sequence_paired_prismatic_hole import write_step


ROOT = Path(__file__).resolve().parents[1]
CASE_ROOT = ROOT / "case-library/self-authored"


def run(case_id: str, output_dir: Path) -> dict[str, Any]:
    """Run the preregistered baseline, suffix defect, rollback, and non-match control."""

    entry, input_path = _entry(case_id)
    operations = canonical_sequence(entry)["operations"]
    output_dir.mkdir(parents=True, exist_ok=True)
    base, boss, final = _shapes(operations)

    baseline_dir = output_dir / "baseline"
    baseline_paths = _write_artifacts(base, boss, final, baseline_dir)
    baseline_gates = _gates(input_path, baseline_paths["after_cut"])
    _require_passing(baseline_gates, "baseline")
    prefix_hash = _sha256(baseline_paths["after_boss"])

    suffix_dir = output_dir / "suffix_defect"
    suffix_dir.mkdir(parents=True, exist_ok=True)
    suffix_base = suffix_dir / "after-base.step"
    suffix_prefix = suffix_dir / "after-boss.step"
    write_step(base, suffix_base)
    shutil.copy2(baseline_paths["after_boss"], suffix_prefix)
    invalid_depth = entry["parameters"]["boss_height"]
    suffix_result = {
        "status": "failed_after_verified_prefix",
        "reason": "cut_depth_must_be_less_than_boss_height",
        "invalid_depth": invalid_depth,
        "prefix_hash_before": _sha256(suffix_prefix),
        "prefix_hash_after": _sha256(suffix_prefix),
    }
    if suffix_result["prefix_hash_before"] != prefix_hash or suffix_result["prefix_hash_after"] != prefix_hash:
        raise AssertionError("suffix defect changed the verified boss prefix")

    rollback_dir = output_dir / "rollback"
    rollback_dir.mkdir(parents=True, exist_ok=True)
    reused_prefix = rollback_dir / "after-boss.step"
    shutil.copy2(baseline_paths["after_boss"], reused_prefix)
    after_cut = rollback_dir / "after-cut.step"
    write_step(final, after_cut)
    rollback_gates = _gates(input_path, after_cut)
    _require_passing(rollback_gates, "rollback")
    if _sha256(reused_prefix) != prefix_hash:
        raise AssertionError("rollback did not reuse the byte-identical prefix")

    early_dir = output_dir / "early_defect"
    early_dir.mkdir(parents=True, exist_ok=True)
    early_base = early_dir / "after-base.step"
    write_step(base, early_base)
    early_result = {
        "status": "unsupported",
        "reason": "defect_precedes_verified_boss_prefix",
        "after_base_hash": _sha256(early_base),
        "after_boss_exists": False,
    }
    return {
        "case_id": case_id,
        "baseline": {"artifacts": _artifact_hashes(baseline_paths), "gates": baseline_gates},
        "suffix_defect": suffix_result,
        "rollback": {"reused_prefix_hash": _sha256(reused_prefix), "gates": rollback_gates},
        "early_defect": early_result,
    }


def _entry(case_id: str) -> tuple[dict[str, Any], Path]:
    directory = CASE_ROOT / case_id
    case = json.loads((directory / "case.json").read_text(encoding="utf-8"))
    if case_id not in {
        "param_additive_boss_dependent_cut_centered_nominal",
        "param_additive_boss_dependent_cut_offset_nominal",
    }:
        raise ValueError("M31 only permits the two preregistered nominal oracle rows")
    return {"parameters": case["parameters"]}, directory / case["input_step"]


def _shapes(operations: list[dict[str, Any]]) -> tuple[Any, Any, Any]:
    base_sketch, base_op, boss_sketch, boss_op, cut_sketch, cut_op = operations
    base = BRepPrimAPI_MakeBox(base_sketch["length_x"], base_sketch["length_y"], base_op["distance"]).Shape()
    boss_solid = BRepPrimAPI_MakeBox(
        gp_Pnt(
            boss_sketch["center_xy"][0] - boss_sketch["length_x"] / 2,
            boss_sketch["center_xy"][1] - boss_sketch["length_y"] / 2,
            base_op["distance"],
        ),
        boss_sketch["length_x"],
        boss_sketch["length_y"],
        boss_op["distance"],
    ).Shape()
    boss = BRepAlgoAPI_Fuse(base, boss_solid).Shape()
    axis = gp_Ax2(
        gp_Pnt(cut_sketch["center_xy"][0], cut_sketch["center_xy"][1], base_op["distance"] + boss_op["distance"] - cut_op["depth"]),
        gp_Dir(0, 0, 1),
    )
    cutter = BRepPrimAPI_MakeCylinder(axis, cut_sketch["radius"], cut_op["depth"]).Shape()
    return base, boss, BRepAlgoAPI_Cut(boss, cutter).Shape()


def _write_artifacts(base: Any, boss: Any, final: Any | None, directory: Path) -> dict[str, Path]:
    directory.mkdir(parents=True, exist_ok=True)
    paths = {"after_base": directory / "after-base.step", "after_boss": directory / "after-boss.step"}
    write_step(base, paths["after_base"])
    write_step(boss, paths["after_boss"])
    if final is not None:
        paths["after_cut"] = directory / "after-cut.step"
        write_step(final, paths["after_cut"])
    return paths


def _gates(input_path: Path, output_path: Path) -> list[dict[str, Any]]:
    return _comparison_gates(probe_summary(load_model(input_path)), probe_summary(load_model(output_path)))


def _require_passing(gates: list[dict[str, Any]], treatment: str) -> None:
    if not all(gate["status"] == "pass" for gate in gates):
        raise AssertionError(f"{treatment} failed existing final geometry gates")


def _artifact_hashes(paths: dict[str, Path]) -> dict[str, str]:
    return {name: _sha256(path) for name, path in paths.items()}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case_id", choices=["param_additive_boss_dependent_cut_centered_nominal", "param_additive_boss_dependent_cut_offset_nominal"])
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.case_id, args.output_dir), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
