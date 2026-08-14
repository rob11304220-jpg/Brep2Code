"""Offline audit for the frozen ``shell-v1`` experimental family."""

from __future__ import annotations
import copy
import hashlib
import tempfile
from pathlib import Path
from typing import Any
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCP.gp import gp_Pnt
from brep2code.agent.harness import _comparison_gates
from brep2code.brep.probes import load_model, probe_summary

try:
    from tools.audit_sequence_paired_prismatic_hole import load_json, write_step
except ModuleNotFoundError:
    from audit_sequence_paired_prismatic_hole import load_json, write_step
ROOT = Path(__file__).resolve().parents[1]
EXPANSION = ROOT / "docs/corpus/sequence-paired/shell-v1-preregistration.json"


def _p(e: dict[str, Any]) -> dict[str, float]:
    p = {k: float(e["parameters"][k]) for k in ("length", "width", "height", "wall_thickness")}
    if not 0 < p["wall_thickness"] < min(p["length"], p["width"], p["height"]) / 2:
        raise ValueError("thickness_precondition_failure")
    return p


def canonical_sequence(e: dict[str, Any]) -> dict[str, Any]:
    p = _p(e)
    return {
        "operations": [
            {
                "id": "base",
                "kind": "MakeSolidBox",
                "length": p["length"],
                "width": p["width"],
                "height": p["height"],
            },
            {"id": "opening", "kind": "SelectTopFaceAsOpening", "source": "base"},
            {
                "id": "shell",
                "kind": "MakeThickSolidInward",
                "source": "base",
                "removed_face": "opening",
                "thickness": p["wall_thickness"],
            },
        ]
    }


def build_shape(e: dict[str, Any]):
    p = _p(e)
    outer = BRepPrimAPI_MakeBox(p["length"], p["width"], p["height"]).Shape()
    t = p["wall_thickness"]
    inner = BRepPrimAPI_MakeBox(
        gp_Pnt(t, t, t), p["length"] - 2 * t, p["width"] - 2 * t, p["height"] - t
    ).Shape()
    return BRepAlgoAPI_Cut(outer, inner).Shape()


def _semantic(e: dict[str, Any], s: dict[str, Any]):
    p = _p(e)
    expected = p["length"] * p["width"] * p["height"] - (p["length"] - 2 * p["wall_thickness"]) * (
        p["width"] - 2 * p["wall_thickness"]
    ) * (p["height"] - p["wall_thickness"])
    if s["counts"]["solid"] != 1 or abs(s["volume"] - expected) > 1e-5:
        raise ValueError("semantic degeneration")


def audit(record_path: Path = EXPANSION) -> list[dict[str, Any]]:
    r = load_json(record_path)
    rows = r["cases"]
    if (
        len(rows) != 6
        or {x["family_id"] for x in rows if x["data_split"] == "development"} != {"shell_symmetric"}
        or {x["family_id"] for x in rows if x["data_split"] == "held_out"} != {"shell_asymmetric"}
    ):
        raise ValueError("split_leak")
    out = []
    for e in rows:
        d = ROOT / e["candidate_directory"]
        c = load_json(d / "case.json")
        inp = d / c["input_step"]
        if (
            c["parameters"] != e["parameters"]
            or hashlib.sha256(inp.read_bytes()).hexdigest() != c["sha256"]
        ):
            raise ValueError("candidate metadata drift")
        if load_json(d / "candidate_sequence.json")["sequence"] != canonical_sequence(e):
            raise ValueError("sequence_mismatch")
        with tempfile.TemporaryDirectory() as tmp:
            o = Path(tmp) / "o.step"
            write_step(build_shape(e), o)
            s = probe_summary(load_model(o))
            _semantic(e, s)
            gates = _comparison_gates(probe_summary(load_model(inp)), s)
            if not all(g["status"] == "pass" for g in gates):
                raise ValueError("geometry replay mismatch")
            for m in e["mutations"]:
                x = copy.deepcopy(e)
                x["parameters"][m["kind"]] += m["delta"]
                q = Path(tmp) / (m["kind"] + ".step")
                write_step(build_shape(x), q)
                _semantic(x, probe_summary(load_model(q)))
        out.append({"case_id": e["case_id"], "gates": gates, "mutations": len(e["mutations"])})
    return out


if __name__ == "__main__":
    print(f"shell sequence-pair audit passed: {len(audit())} records")
