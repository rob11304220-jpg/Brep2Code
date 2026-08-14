"""Development-only M96 observation contract used by the M97 calibration CLI."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from brep2code.agent.observation import build_observation_context
from brep2code.brep.probes import load_model, probe_summary
from tools.audit_blind_through_observability import audit as audit_cylindrical_cut
from tools.audit_sequence_paired_prismatic_hole import load_json


M97_OBSERVATION_CONTRACT_VERSION = "m97-measured-through-hole-facts-v1"


def derive_m96_development_context(entry: dict[str, Any], *, root: Path) -> str:
    """Measure one development B-Rep and return only the frozen M96 facts."""

    if entry.get("data_split") != "development":
        raise ValueError("M97 accepts development rows only")
    directory = root / entry["candidate_directory"]
    case = load_json(directory / "case.json")
    measured = audit_cylindrical_cut(directory / case["input_step"])
    if measured.get("classification") != "through":
        raise ValueError("M97 requires a measured through cylindrical cut")
    cylinders = measured.get("cylindrical_faces")
    if not isinstance(cylinders, list) or len(cylinders) != 1:
        raise ValueError("M97 requires exactly one measured cylinder")
    cylinder = cylinders[0]
    if cylinder.get("axis") != [0.0, 0.0, 1.0]:
        raise ValueError("M97 requires a +Z cylinder axis")

    from OCP.BRepAdaptor import BRepAdaptor_Surface
    from OCP.TopoDS import TopoDS

    model = load_model(directory / case["input_step"])
    summary = probe_summary(model)
    cylinder_face = next(
        shape for entity_id, shape in model.entities.items() if entity_id == cylinder["entity_id"]
    )
    location = BRepAdaptor_Surface(TopoDS.Face_s(cylinder_face)).Cylinder().Location()
    envelope = {
        "schema_version": 1,
        "observation_session_id": "m97-development-only",
        "call_id": "measured-through-hole-facts",
        "ok": True,
        "data": {
            "kind": "measured_through_hole_facts",
            "base_bbox": summary["bbox"],
            "cylindrical_cut": {
                "radius": cylinder["radius"],
                "axis": "+Z",
                "center_xy": [round(float(location.X()), 6), round(float(location.Y()), 6)],
                "extent": "through",
            },
        },
        "error": None,
        "truncated": False,
    }
    context = build_observation_context([envelope])
    validate_m97_observation_context(context)
    return context


def validate_m97_observation_context(context: str) -> list[dict[str, Any]]:
    """Fail closed unless a provider context is exactly the frozen M96 shape."""

    try:
        payload = json.loads(context)
    except json.JSONDecodeError as exc:
        raise ValueError("M97 observation context is not JSON") from exc
    if not isinstance(payload, dict) or set(payload) != {"schema_version", "observation_transcript"}:
        raise ValueError("M97 observation context has an invalid top-level shape")
    transcript = payload["observation_transcript"]
    if payload["schema_version"] != 1 or not isinstance(transcript, list) or len(transcript) != 1:
        raise ValueError("M97 observation context requires one measured-fact envelope")
    envelope = transcript[0]
    expected_envelope = {
        "schema_version", "observation_session_id", "call_id", "ok", "data", "error", "truncated"
    }
    if not isinstance(envelope, dict) or set(envelope) != expected_envelope:
        raise ValueError("M97 observation context has an invalid envelope")
    if (
        envelope["schema_version"] != 1
        or envelope["observation_session_id"] != "m97-development-only"
        or envelope["call_id"] != "measured-through-hole-facts"
        or envelope["ok"] is not True
        or envelope["error"] is not None
        or envelope["truncated"] is not False
    ):
        raise ValueError("M97 observation context has an invalid measured-fact envelope")
    data = envelope["data"]
    if not isinstance(data, dict) or set(data) != {"kind", "base_bbox", "cylindrical_cut"}:
        raise ValueError("M97 observation context contains unsupported facts")
    if data["kind"] != "measured_through_hole_facts":
        raise ValueError("M97 observation context has an invalid fact kind")
    _validate_bbox(data["base_bbox"])
    cut = data["cylindrical_cut"]
    if not isinstance(cut, dict) or set(cut) != {"radius", "axis", "center_xy", "extent"}:
        raise ValueError("M97 observation context has an invalid cylindrical cut")
    if not _positive_number(cut["radius"]) or cut["axis"] != "+Z" or cut["extent"] != "through":
        raise ValueError("M97 observation context has invalid cylindrical cut values")
    center = cut["center_xy"]
    if not isinstance(center, list) or len(center) != 2 or not all(_number(value) for value in center):
        raise ValueError("M97 observation context has an invalid cylinder centre")
    return transcript


def _validate_bbox(value: object) -> None:
    if not isinstance(value, dict) or set(value) != {"min", "max"}:
        raise ValueError("M97 observation context has an invalid base bbox")
    for bound in (value["min"], value["max"]):
        if not isinstance(bound, list) or len(bound) != 3 or not all(_number(item) for item in bound):
            raise ValueError("M97 observation context has an invalid base bbox")


def _number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _positive_number(value: object) -> bool:
    return _number(value) and value > 0
