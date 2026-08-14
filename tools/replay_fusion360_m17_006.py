"""Run the frozen M17-005 selector on the M17-006 selected cases."""
from __future__ import annotations

import json
from pathlib import Path

from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer

from brep2code.agent.harness import _comparison_gates
from brep2code.brep.probes import load_model, probe_summary
from replay_fusion360_m14 import replay, replay_strict


SELECTION = Path("docs/corpus/external/fusion360-gallery-r1.0.1-m17-006-selection.json")
OUTPUT = Path("data/fusion360-gallery-m17-006-independent-selector-validation")


def _run(sample: dict, treatment: bool) -> dict:
    input_path = Path(sample["step_path"])
    payload = json.loads(Path(sample["json_path"]).read_text(encoding="utf-8"))
    output_path = OUTPUT / ("selector" if treatment else "strict") / f"{sample['case_id']}.step"
    record = {key: sample[key] for key in ("case_id", "split", "source_order", "source_family", "input_step_sha256")}
    record["mapping"] = "frozen_selector" if treatment else "strict_baseline"
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
    selection = json.loads(SELECTION.read_text(encoding="utf-8"))
    if selection["selection_status"] != "completed":
        raise RuntimeError("M17-006 selection is not completed")
    strict = [_run(sample, False) for sample in selection["samples"]]
    selector = [_run(sample, True) for sample in selection["samples"]]
    report = {"schema_version": 1, "workpack": "WP-M17-006", "selection_id": selection["selection_id"], "strict": strict, "selector": selector}
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(OUTPUT / "report.json")
    return 0 if all(row["passed"] for row in selector) else 1


if __name__ == "__main__":
    raise SystemExit(main())
