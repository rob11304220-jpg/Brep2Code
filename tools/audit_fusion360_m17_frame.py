"""Emit the fixed-case, offline-only M17 Line3D frame-evidence audit."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
from typing import Any

from brep2code.brep.probes import load_model, probe_summary


ASSETS = Path("data/datasets/fusion360_gallery/r1.0.1/extracted/r1.0.1/reconstruction")
DEFAULT_OUTPUT = Path("data/fusion360-gallery-m17-frame-evidence")
SCALE_MM_PER_CM = 10.0
TOLERANCE = 1e-6
CASES = (
    ("100243_9fb796fe_0005", "development", "m14"),
    ("100877_ac1e5a17_0001", "development", "m14"),
    ("145540_a4f54d5f_0010", "development", "m17"),
    ("41026_295d1dc8_0003", "held_out", "m17"),
)


def _round(value: float) -> float:
    value = round(float(value), 6)
    return 0.0 if abs(value) < TOLERANCE else value


def _vector(value: dict[str, Any]) -> tuple[float, float, float]:
    return tuple(float(value[coordinate]) for coordinate in ("x", "y", "z"))


def _dot(left: tuple[float, float, float], right: tuple[float, float, float]) -> float:
    return sum(component_left * component_right for component_left, component_right in zip(left, right, strict=True))


def _cross(left: tuple[float, float, float], right: tuple[float, float, float]) -> tuple[float, float, float]:
    return (
        left[1] * right[2] - left[2] * right[1],
        left[2] * right[0] - left[0] * right[2],
        left[0] * right[1] - left[1] * right[0],
    )


def _norm(vector: tuple[float, float, float]) -> float:
    return math.sqrt(_dot(vector, vector))


def _normalize(vector: tuple[float, float, float]) -> tuple[float, float, float]:
    length = _norm(vector)
    if length < TOLERANCE:
        raise ValueError("zero-length vector")
    return tuple(component / length for component in vector)


def _subtract(left: tuple[float, float, float], right: tuple[float, float, float]) -> tuple[float, float, float]:
    return tuple(component_left - component_right for component_left, component_right in zip(left, right, strict=True))


def _world_point(point: dict[str, Any], transform: dict[str, Any]) -> tuple[float, float, float]:
    origin = _vector(transform["origin"])
    axes = tuple(_vector(transform[f"{name}_axis"]) for name in ("x", "y", "z"))
    coordinates = tuple(float(point.get(name, 0.0)) for name in ("x", "y", "z"))
    return tuple(
        SCALE_MM_PER_CM * (origin[index] + sum(coordinates[axis] * axes[axis][index] for axis in range(3)))
        for index in range(3)
    )


def _ordered_loop(curves: list[dict[str, Any]], transform: dict[str, Any]) -> list[tuple[float, float, float]]:
    segments = [(_world_point(curve["start_point"], transform), _world_point(curve["end_point"], transform)) for curve in curves]
    first, current = segments.pop(0)
    points = [first]
    while segments:
        matches = []
        for index, (start, end) in enumerate(segments):
            if _norm(_subtract(current, start)) <= TOLERANCE:
                matches.append((index, end))
            if _norm(_subtract(current, end)) <= TOLERANCE:
                matches.append((index, start))
        if len(matches) != 1:
            raise ValueError("ambiguous_or_disconnected_line_loop")
        index, current = matches[0]
        points.append(current)
        segments.pop(index)
    if _norm(_subtract(current, first)) > TOLERANCE:
        raise ValueError("non_closing_line_loop")
    return points


def _newell_normal(points: list[tuple[float, float, float]]) -> tuple[float, float, float]:
    normal = [0.0, 0.0, 0.0]
    for point, following in zip(points, points[1:] + points[:1], strict=True):
        normal[0] += (point[1] - following[1]) * (point[2] + following[2])
        normal[1] += (point[2] - following[2]) * (point[0] + following[0])
        normal[2] += (point[0] - following[0]) * (point[1] + following[1])
    return _normalize(tuple(normal))


def _projection_range(points: list[tuple[float, float, float]], axis: tuple[float, float, float]) -> dict[str, float]:
    values = [_dot(point, axis) for point in points]
    return {"min": _round(min(values)), "max": _round(max(values)), "span": _round(max(values) - min(values))}


def _bbox_corners(bbox: dict[str, list[float]]) -> list[tuple[float, float, float]]:
    return [tuple(corner) for corner in itertools.product(*zip(bbox["min"], bbox["max"], strict=True))]


def _listed_continuity(curves: list[dict[str, Any]], transform: dict[str, Any]) -> dict[str, Any]:
    gaps = []
    for curve, following in zip(curves, curves[1:] + curves[:1], strict=True):
        endpoint = _world_point(curve["end_point"], transform)
        next_start = _world_point(following["start_point"], transform)
        gaps.append(_round(_norm(_subtract(endpoint, next_start))))
    return {"continuous": all(gap <= TOLERANCE for gap in gaps), "end_to_next_start_gaps_mm": gaps}


def _source_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _case_row(case_id: str, split: str, cohort: str) -> dict[str, Any]:
    json_path = ASSETS / f"{case_id}.json"
    step_path = ASSETS / f"{case_id}.step"
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    sketch, extrude = [payload["entities"][item["entity"]] for item in payload["timeline"]]
    transform = sketch["transform"]
    curves = next(iter(sketch["profiles"].values()))["loops"][0]["profile_curves"]
    if {curve["type"] for curve in curves} != {"Line3D"}:
        raise ValueError(f"{case_id}: expected Line3D only")

    axes = {name: _normalize(_vector(transform[f"{name}_axis"])) for name in ("x", "y", "z")}
    ordered_points = _ordered_loop(curves, transform)
    normal = _newell_normal(ordered_points)
    input_probe = probe_summary(load_model(step_path))
    input_corners = _bbox_corners(input_probe["bbox"])
    profile_projections = {name: _projection_range(ordered_points, axis) for name, axis in axes.items()}
    step_projections = {name: _projection_range(input_corners, axis) for name, axis in axes.items()}
    extent_mm = SCALE_MM_PER_CM * float(extrude["extent_one"]["distance"]["value"])
    alignments = {name: _round(_dot(normal, axis)) for name, axis in axes.items()}
    matching_axes = [
        name
        for name in axes
        if abs(abs(alignments[name]) - 1.0) <= TOLERANCE
        and abs(step_projections[name]["span"] - extent_mm) <= TOLERANCE
        and profile_projections[name]["span"] <= TOLERANCE
    ]
    if len(matching_axes) != 1:
        raise ValueError(f"{case_id}: selector is not unique: {matching_axes}")
    selected_axis = matching_axes[0]
    selected_profile = profile_projections[selected_axis]
    selected_step = step_projections[selected_axis]
    if abs(selected_profile["min"] - selected_step["min"]) <= TOLERANCE:
        selected_sign = "+"
    elif abs(selected_profile["max"] - selected_step["max"]) <= TOLERANCE:
        selected_sign = "-"
    else:
        raise ValueError(f"{case_id}: profile plane is not on a STEP projection boundary")

    return {
        "case_id": case_id,
        "split": split,
        "cohort": cohort,
        "sources": {
            "native_history_json": json_path.as_posix(),
            "input_step": step_path.as_posix(),
            "input_step_sha256": _source_sha256(step_path),
            "json_fields": [
                "entities[Sketch].transform.origin",
                "entities[Sketch].transform.{x_axis,y_axis,z_axis}",
                "entities[Sketch].profiles[*].loops[0].profile_curves[*]",
                "entities[ExtrudeFeature].extent_one.distance.value",
            ],
            "step_probe": "brep2code.brep.probes.probe_summary(...).bbox",
        },
        "transform": {
            "origin_cm": [_round(value) for value in _vector(transform["origin"])],
            "normalized_axes": {name: [_round(value) for value in axis] for name, axis in axes.items()},
            "dot_products": {
                "x_y": _round(_dot(axes["x"], axes["y"])),
                "x_z": _round(_dot(axes["x"], axes["z"])),
                "y_z": _round(_dot(axes["y"], axes["z"])),
            },
            "right_handedness": _round(_dot(_cross(axes["x"], axes["y"]), axes["z"])),
        },
        "profile_loop": {
            "curve_count": len(curves),
            "listed_endpoint_continuity": _listed_continuity(curves, transform),
            "endpoint_ordered_continuity": True,
            "endpoint_ordered_normal": [_round(value) for value in normal],
            "ordered_normal_dot_axis": alignments,
            "profile_projection_mm": profile_projections,
        },
        "extent": {
            "source_distance_cm": _round(float(extrude["extent_one"]["distance"]["value"])),
            "magnitude_mm": _round(extent_mm),
            "source_type": extrude["extent_one"]["type"],
            "taper_angle": _round(float(extrude["extent_one"]["taper_angle"]["value"])),
        },
        "input_step": {"bbox_mm": input_probe["bbox"], "axis_projection_mm": step_projections},
        "candidate_selector": {
            "selected_signed_axis": f"{selected_sign}{selected_axis}_axis",
            "uniquely_matches_profile_normal": True,
            "step_span_equals_source_extent": True,
            "profile_on_selected_projection_boundary": True,
        },
    }


def _markdown(report: dict[str, Any]) -> str:
    lines = [
        "# M17-004 Fusion Line3D Frame-Evidence Audit",
        "",
        "Offline-only evidence from the fixed four cases. This report does not run a replay treatment or change parser behavior.",
        "",
        "| Case | Split | Listed loop | Ordered profile normal | Extent (mm) | STEP span matching extent | Candidate |",
        "|---|---|---|---|---:|---|---|",
    ]
    for row in report["cases"]:
        continuity = "continuous" if row["profile_loop"]["listed_endpoint_continuity"]["continuous"] else "non-continuous"
        normal = row["profile_loop"]["ordered_normal_dot_axis"]
        normal_axis = max(normal, key=lambda name: abs(normal[name]))
        spans = row["input_step"]["axis_projection_mm"]
        matching = [name for name, projection in spans.items() if abs(projection["span"] - row["extent"]["magnitude_mm"]) <= TOLERANCE]
        lines.append(
            f"| `{row['case_id']}` | {row['split']} | {continuity} | {normal_axis}_axis ({normal[normal_axis]:g}) | "
            f"{row['extent']['magnitude_mm']:g} | {', '.join(matching)}_axis | `{row['candidate_selector']['selected_signed_axis']}` |"
        )
    lines.extend(
        [
            "",
            "## Candidate selector",
            "",
            "For a single transformed Line3D outer loop with a zero-taper one-sided distance extent, order only the existing endpoints; choose the unique sketch axis whose ordered-loop normal is parallel, whose input-STEP bbox projection span equals the source extent magnitude, and whose transformed profile is on a matching projection boundary. Choose `+axis` when the profile is at the lower boundary and `-axis` when it is at the upper boundary.",
            "",
            "All four fixed rows select uniquely: `+z_axis` for the three development controls and `+y_axis` for the held-out control. This distinguishes the held-out mapping without treating its non-continuous listed curve order as a direction signal.",
            "",
            "## Decision boundary",
            "",
            "The fixed evidence supports nominating this explicit selector for a separate promotion workpack only. It is not a parser change: M17-003 remains the gate-outcome evidence that unconditional `ordered_y` regresses every Line3D control. Any promotion workpack must retain these four hash-locked cases, run the existing gates, and define non-regression controls before changing replay behavior.",
            "",
            "## Source traceability",
            "",
            "Each JSON row records native-history field paths, the SHA-256 of its input STEP, and the existing `probe_summary(...).bbox` source for the projection calculation. Units are normalized from Fusion cm to mm with factor 10.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    cases = [_case_row(*case) for case in CASES]
    report = {
        "schema_version": 1,
        "workpack": "WP-M17-004",
        "scope": "fixed four-case, offline-only Line3D frame evidence",
        "unit_scale_cm_to_mm": SCALE_MM_PER_CM,
        "cases": cases,
        "conclusion": {
            "status": "candidate_selector_nominated_for_separate_promotion_workpack",
            "selector": "unique profile-normal axis with STEP projected span equal to source extent; sign from profile boundary",
            "mapping_policy_changed": False,
            "replay_treatment_run": False,
        },
    }
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (args.output / "report.md").write_text(_markdown(report), encoding="utf-8")
    print(args.output / "report.json")
    print(args.output / "report.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
