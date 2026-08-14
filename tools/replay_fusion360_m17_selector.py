"""Run the fixed four-case M17 strict-versus-selector offline matrix."""
from __future__ import annotations

import json
from pathlib import Path

from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer

from brep2code.agent.harness import _comparison_gates
from brep2code.brep.probes import load_model, probe_summary
from replay_fusion360_m14 import replay, replay_strict, sha256


ASSETS = Path("data/datasets/fusion360_gallery/r1.0.1/extracted/r1.0.1/reconstruction")
OUTPUT = Path("data/fusion360-gallery-m17-selector-validation")
CASES = (("100243_9fb796fe_0005", "development"), ("100877_ac1e5a17_0001", "development"), ("145540_a4f54d5f_0010", "development"), ("41026_295d1dc8_0003", "held_out"))


def _run(case_id: str, split: str, treatment: bool) -> dict:
    input_path = ASSETS / f"{case_id}.step"
    payload = json.loads((ASSETS / f"{case_id}.json").read_text(encoding="utf-8"))
    output_path = OUTPUT / ("treatment" if treatment else "baseline") / f"{case_id}.step"
    record = {"case_id": case_id, "split": split, "input_sha256": sha256(input_path), "mapping": "selector" if treatment else "strict"}
    try:
        source = probe_summary(load_model(input_path))
        shape = replay(payload, source["bbox"]) if treatment else replay_strict(payload)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        writer = STEPControl_Writer()
        writer.Transfer(shape, STEPControl_AsIs)
        if writer.Write(str(output_path)) != 1:
            raise RuntimeError("STEP writer failed")
        gates = _comparison_gates(source, probe_summary(load_model(output_path)))
        record.update({"status": "completed", "gates": gates, "passed": all(gate["status"] == "pass" for gate in gates)})
    except Exception as error:
        record.update({"status": "rejected", "error": str(error), "passed": False})
    return record


def main() -> int:
    baseline = [_run(case_id, split, False) for case_id, split in CASES]
    treatment = [_run(case_id, split, True) for case_id, split in CASES]
    report = {"schema_version": 1, "workpack": "WP-M17-005", "baseline": baseline, "treatment": treatment}
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    baseline_expected = [True, True, True, False]
    return 0 if [row["passed"] for row in baseline] == baseline_expected and all(row["passed"] for row in treatment) else 1


if __name__ == "__main__":
    raise SystemExit(main())
