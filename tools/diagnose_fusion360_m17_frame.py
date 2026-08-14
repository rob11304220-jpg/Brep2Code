"""Local-only finite frame diagnostic for the fixed M17 held-out case."""
from __future__ import annotations

import json
from pathlib import Path

from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakePolygon
from OCP.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer
from OCP.gp import gp_Dir, gp_Vec

from brep2code.agent.harness import _comparison_gates
from brep2code.brep.probes import load_model, probe_summary
from replay_fusion360_m14 import _point, replay, sha256


ASSETS = Path("data/datasets/fusion360_gallery/r1.0.1/extracted/r1.0.1/reconstruction")
OUTPUT = Path("data/fusion360-gallery-m17-frame-diagnostic")
CASE_ID = "41026_295d1dc8_0003"
SCALE = 10.0
TOLERANCE_MM = 1e-7
VARIANTS = (("listed_z", False, "z_axis"), ("ordered_z", True, "z_axis"), ("listed_y", False, "y_axis"), ("ordered_y", True, "y_axis"), ("ordered_negative_y", True, "negative_y_axis"))
CONTROLS = {
    "m14_development": ("100243_9fb796fe_0005", "100877_ac1e5a17_0001"),
    "m14_held_out": ("110043_b73b8beb_0000",),
    "m17_development": ("145540_a4f54d5f_0010", "21646_a2dd0d00_0058"),
}


def _ordered_points(curves: list[dict], transform: dict, order: bool):
    points = [(_point(curve["start_point"], transform), _point(curve["end_point"], transform)) for curve in curves]
    if not order:
        return [start for start, _ in points]
    first, current = points.pop(0)
    result = [first]
    while points:
        matches = []
        for index, (start, end) in enumerate(points):
            if current.Distance(start) <= TOLERANCE_MM:
                matches.append((index, end))
            if current.Distance(end) <= TOLERANCE_MM:
                matches.append((index, start))
        if len(matches) != 1:
            raise ValueError("ambiguous_or_disconnected_line_loop")
        result.append(current)
        index, current = matches[0]
        points.pop(index)
    if current.Distance(first) > TOLERANCE_MM:
        raise ValueError("non_closing_line_loop")
    return result


def _shape(payload: dict, order: bool, axis_name: str):
    entities, timeline = payload["entities"], payload["timeline"]
    sketch, extrude = [entities[item["entity"]] for item in timeline]
    transform = sketch["transform"]
    curves = next(iter(sketch["profiles"].values()))["loops"][0]["profile_curves"]
    polygon = BRepBuilderAPI_MakePolygon()
    for point in _ordered_points(curves, transform, order):
        polygon.Add(point)
    polygon.Close()
    face = BRepBuilderAPI_MakeFace(polygon.Wire()).Face()
    raw_axis = transform["y_axis" if axis_name.endswith("y_axis") else "z_axis"]
    sign = -1.0 if axis_name == "negative_y_axis" else 1.0
    direction = gp_Dir(sign * raw_axis["x"], sign * raw_axis["y"], sign * raw_axis["z"])
    distance = SCALE * extrude["extent_one"]["distance"]["value"]
    return BRepPrimAPI_MakePrism(face, gp_Vec(direction.XYZ()) * distance).Shape()


def _run_control(case_id: str, split: str) -> dict:
    input_path = ASSETS / f"{case_id}.step"
    payload = json.loads((ASSETS / f"{case_id}.json").read_text(encoding="utf-8"))
    curves = next(iter([payload["entities"][item["entity"]] for item in payload["timeline"]][0]["profiles"].values()))["loops"][0]["profile_curves"]
    line_treatment = {curve["type"] for curve in curves} == {"Line3D"}
    output_path = OUTPUT / "controls" / f"{case_id}.step"
    record = {
        "case_id": case_id,
        "split": split,
        "input_sha256": sha256(input_path),
        "treatment": "ordered_y" if line_treatment else "strict_baseline_non_line3d",
    }
    try:
        shape = _shape(payload, True, "y_axis") if line_treatment else replay(payload)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        writer = STEPControl_Writer()
        writer.Transfer(shape, STEPControl_AsIs)
        if writer.Write(str(output_path)) != 1:
            raise RuntimeError("STEP writer failed")
        gates = _comparison_gates(probe_summary(load_model(input_path)), probe_summary(load_model(output_path)))
        record.update({"status": "completed", "gates": gates, "passed": all(g["status"] == "pass" for g in gates)})
    except Exception as error:
        record.update({"status": "rejected", "error": str(error), "passed": False})
    return record


def main() -> int:
    payload = json.loads((ASSETS / f"{CASE_ID}.json").read_text(encoding="utf-8"))
    source = probe_summary(load_model(ASSETS / f"{CASE_ID}.step"))
    rows = []
    for name, order, axis in VARIANTS:
        path = OUTPUT / f"{name}.step"
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            writer = STEPControl_Writer()
            writer.Transfer(_shape(payload, order, axis), STEPControl_AsIs)
            if writer.Write(str(path)) != 1:
                raise RuntimeError("STEP writer failed")
            output = probe_summary(load_model(path))
            gates = _comparison_gates(source, output)
            rows.append({"variant": name, "status": "completed", "gates": gates, "passed": all(g["status"] == "pass" for g in gates)})
        except Exception as error:
            rows.append({"variant": name, "status": "rejected", "error": str(error), "passed": False})
    controls = []
    if next(row for row in rows if row["variant"] == "ordered_y")["passed"]:
        controls = [_run_control(case, split) for split, cases in CONTROLS.items() for case in cases]
    report = OUTPUT / "report.json"
    report.write_text(
        json.dumps({"schema_version": 1, "case_id": CASE_ID, "variants": rows, "controls": controls}, indent=2) + "\n",
        encoding="utf-8",
    )
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
