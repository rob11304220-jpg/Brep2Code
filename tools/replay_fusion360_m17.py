"""Strict offline-only Fusion r1.0.1 JSON replay for the M17 bounded audit."""
from __future__ import annotations

import json
from pathlib import Path

from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer

from brep2code.agent.harness import _comparison_gates
from brep2code.brep.probes import load_model, probe_summary
from replay_fusion360_m14 import replay, sha256


ROOT = Path("data/datasets/fusion360_gallery/r1.0.1/extracted/r1.0.1")
ASSETS = ROOT / "reconstruction"
OUTPUT = Path("data/fusion360-gallery-m17-replay")
CASES = {
    "development": ("145540_a4f54d5f_0010", "21646_a2dd0d00_0058"),
    "held_out": ("41026_295d1dc8_0003",),
}


def run_case(case_id: str, split: str) -> dict:
    input_path = ASSETS / f"{case_id}.step"
    json_path = ASSETS / f"{case_id}.json"
    output_path = OUTPUT / f"{case_id}.step"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "case_id": case_id,
        "split": split,
        "input_step": input_path.as_posix(),
        "input_sha256": sha256(input_path),
    }
    try:
        source = probe_summary(load_model(input_path))
        shape = replay(json.loads(json_path.read_text(encoding="utf-8")), source["bbox"])
        writer = STEPControl_Writer()
        writer.Transfer(shape, STEPControl_AsIs)
        if writer.Write(str(output_path)) != 1:
            raise RuntimeError("STEP writer failed")
        output = probe_summary(load_model(output_path))
        gates = _comparison_gates(source, output)
        record.update(
            {
                "status": "completed",
                "output_step": output_path.as_posix(),
                "input_probe": source,
                "output_probe": output,
                "gates": gates,
                "passed": all(gate["status"] == "pass" for gate in gates),
            }
        )
    except Exception as error:
        record.update({"status": "rejected", "error": str(error), "passed": False})
    return record


def main() -> int:
    results = [run_case(case, split) for split, cases in CASES.items() for case in cases]
    report = OUTPUT / "report.json"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(
        json.dumps({"schema_version": 1, "unit_scale_cm_to_mm": 10.0, "cases": results}, indent=2) + "\n",
        encoding="utf-8",
    )
    print(report)
    return 0 if all(row["passed"] for row in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
