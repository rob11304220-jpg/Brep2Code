"""Build the deterministic M12 self-authored parameter-family fixtures.

This is a development-only asset generator.  It neither calls providers nor
downloads data; its output is the committed self-authored case library.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse
from OCP.BRepBndLib import BRepBndLib
from OCP.BRepFilletAPI import BRepFilletAPI_MakeChamfer, BRepFilletAPI_MakeFillet
from OCP.BRepGProp import BRepGProp
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.Bnd import Bnd_Box
from OCP.GProp import GProp_GProps
from OCP.IFSelect import IFSelect_RetDone
from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer
from OCP.TopAbs import TopAbs_EDGE, TopAbs_FACE, TopAbs_SHELL, TopAbs_SOLID
from OCP.TopExp import TopExp_Explorer
from OCP.TopoDS import TopoDS
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt


ROOT = Path(__file__).resolve().parents[1]
CASE_ROOT = ROOT / "case-library" / "self-authored"
MANIFEST_ROOT = ROOT / "case-library" / "manifests" / "self-authored"
CASE_CARD_ROOT = ROOT / "docs" / "corpus" / "cases"


@dataclass(frozen=True)
class Spec:
    family_id: str
    data_split: str
    variant: str
    parameters: dict[str, float]

    @property
    def case_id(self) -> str:
        return f"param_{self.family_id}_{self.variant}"


SPECS = (
    *(Spec("additive_boss", "development", variant, {"radius": radius, "height": height})
      for variant, radius, height in (("low", 3.0, 3.0), ("nominal", 4.0, 5.0), ("high", 5.0, 7.0))),
    *(Spec("through_hole", "development", variant, {"radius": radius, "x": x})
      for variant, radius, x in (("low", 2.0, 9.0), ("nominal", 3.0, 15.0), ("high", 4.0, 21.0))),
    *(Spec("rounded_slot", "development", variant, {"width": width, "straight_length": length})
      for variant, width, length in (("low", 3.0, 8.0), ("nominal", 4.0, 12.0), ("high", 5.0, 16.0))),
    *(Spec("fillet", "development", variant, {"radius": radius})
      for variant, radius in (("low", 0.5), ("nominal", 1.0), ("high", 1.5))),
    *(Spec("blind_hole", "held_out", variant, {"radius": radius, "depth": depth})
      for variant, radius, depth in (("low", 2.0, 3.0), ("nominal", 3.0, 5.0), ("high", 4.0, 7.0))),
    *(Spec("chamfer", "held_out", variant, {"distance": distance})
      for variant, distance in (("low", 0.5), ("nominal", 1.0), ("high", 1.5))),
)


def first_edge(shape):
    explorer = TopExp_Explorer(shape, TopAbs_EDGE)
    if not explorer.More():
        raise RuntimeError("shape has no edge")
    return TopoDS.Edge_s(explorer.Current())


def first_face(shape):
    explorer = TopExp_Explorer(shape, TopAbs_FACE)
    if not explorer.More():
        raise RuntimeError("shape has no face")
    return TopoDS.Face_s(explorer.Current())


def make_shape(spec: Spec):
    if spec.family_id == "additive_boss":
        base = BRepPrimAPI_MakeBox(30.0, 20.0, 5.0).Shape()
        boss = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(15, 10, 5), gp_Dir(0, 0, 1)), spec.parameters["radius"], spec.parameters["height"]).Shape()
        return BRepAlgoAPI_Fuse(base, boss).Shape()
    if spec.family_id in {"through_hole", "blind_hole"}:
        base = BRepPrimAPI_MakeBox(30.0, 20.0, 10.0).Shape()
        depth = 12.0 if spec.family_id == "through_hole" else spec.parameters["depth"]
        x = spec.parameters.get("x", 15.0)
        cutter = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(x, 10, -1 if spec.family_id == "through_hole" else 10 - depth), gp_Dir(0, 0, 1)), spec.parameters["radius"], depth).Shape()
        return BRepAlgoAPI_Cut(base, cutter).Shape()
    if spec.family_id == "rounded_slot":
        plate = BRepPrimAPI_MakeBox(30.0, 20.0, 5.0).Shape()
        width, length = spec.parameters["width"], spec.parameters["straight_length"]
        radius, x0 = width / 2, (30 - length) / 2
        cutter = BRepPrimAPI_MakeBox(gp_Pnt(x0, 10 - radius, -1), length, width, 7).Shape()
        for x in (x0, x0 + length):
            cylinder = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(x, 10, -1), gp_Dir(0, 0, 1)), radius, 7).Shape()
            cutter = BRepAlgoAPI_Fuse(cutter, cylinder).Shape()
        return BRepAlgoAPI_Cut(plate, cutter).Shape()
    base = BRepPrimAPI_MakeBox(24.0, 18.0, 10.0).Shape()
    if spec.family_id == "fillet":
        operation = BRepFilletAPI_MakeFillet(base)
        operation.Add(spec.parameters["radius"], first_edge(base))
        return operation.Shape()
    if spec.family_id == "chamfer":
        operation = BRepFilletAPI_MakeChamfer(base)
        operation.Add(spec.parameters["distance"], spec.parameters["distance"], first_edge(base), first_face(base))
        return operation.Shape()
    raise ValueError(f"unknown family: {spec.family_id}")


def count(shape, top_abs) -> int:
    explorer = TopExp_Explorer(shape, top_abs)
    total = 0
    while explorer.More():
        total += 1
        explorer.Next()
    return total


def expected(shape) -> dict[str, object]:
    box = Bnd_Box()
    BRepBndLib.Add_s(shape, box)
    xmin, ymin, zmin, xmax, ymax, zmax = box.Get()
    props = GProp_GProps()
    BRepGProp.VolumeProperties_s(shape, props)
    return {
        "bbox": {"min": [xmin, ymin, zmin], "max": [xmax, ymax, zmax]},
        "volume": props.Mass(),
        "counts": {
            "solid": count(shape, TopAbs_SOLID), "shell": count(shape, TopAbs_SHELL),
            "face": count(shape, TopAbs_FACE), "edge": count(shape, TopAbs_EDGE),
        },
    }


def script_text(spec: Spec) -> str:
    # The generated scripts deliberately keep each case standalone for replay.
    imports = {
        "additive_boss": "from OCP.BRepAlgoAPI import BRepAlgoAPI_Fuse\nfrom OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder\nfrom OCP.gp import gp_Ax2, gp_Dir, gp_Pnt",
        "through_hole": "from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut\nfrom OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder\nfrom OCP.gp import gp_Ax2, gp_Dir, gp_Pnt",
        "blind_hole": "from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut\nfrom OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder\nfrom OCP.gp import gp_Ax2, gp_Dir, gp_Pnt",
        "rounded_slot": "from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse\nfrom OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder\nfrom OCP.gp import gp_Ax2, gp_Dir, gp_Pnt",
        "fillet": "from OCP.BRepFilletAPI import BRepFilletAPI_MakeFillet\nfrom OCP.BRepPrimAPI import BRepPrimAPI_MakeBox\nfrom OCP.TopAbs import TopAbs_EDGE\nfrom OCP.TopExp import TopExp_Explorer\nfrom OCP.TopoDS import TopoDS",
        "chamfer": "from OCP.BRepFilletAPI import BRepFilletAPI_MakeChamfer\nfrom OCP.BRepPrimAPI import BRepPrimAPI_MakeBox\nfrom OCP.TopAbs import TopAbs_EDGE, TopAbs_FACE\nfrom OCP.TopExp import TopExp_Explorer\nfrom OCP.TopoDS import TopoDS",
    }[spec.family_id]
    helper_source = ""
    if spec.family_id in {"fillet", "chamfer"}:
        helper_source += '''\ndef first_edge(shape):
    explorer = TopExp_Explorer(shape, TopAbs_EDGE)
    if not explorer.More():
        raise RuntimeError("shape has no edge")
    return TopoDS.Edge_s(explorer.Current())
'''
    if spec.family_id == "chamfer":
        helper_source += '''\ndef first_face(shape):
    explorer = TopExp_Explorer(shape, TopAbs_FACE)
    if not explorer.More():
        raise RuntimeError("shape has no face")
    return TopoDS.Face_s(explorer.Current())
'''
    return f'''from pathlib import Path

{imports}
from OCP.IFSelect import IFSelect_RetDone
from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer

FAMILY_ID = {spec.family_id!r}
PARAMETERS = {spec.parameters!r}
{helper_source}
'''+ shape_source(spec) + '''
Path("output").mkdir(exist_ok=True)
writer = STEPControl_Writer()
writer.Transfer(shape, STEPControl_AsIs)
if writer.Write("output/model.step") != IFSelect_RetDone:
    raise RuntimeError("failed to write STEP")
'''


def shape_source(spec: Spec) -> str:
    p = spec.parameters
    if spec.family_id == "additive_boss":
        return f'''base = BRepPrimAPI_MakeBox(30.0, 20.0, 5.0).Shape()\nboss = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(15, 10, 5), gp_Dir(0, 0, 1)), {p["radius"]}, {p["height"]}).Shape()\nshape = BRepAlgoAPI_Fuse(base, boss).Shape()\n'''
    if spec.family_id == "through_hole":
        return f'''base = BRepPrimAPI_MakeBox(30.0, 20.0, 10.0).Shape()\ncutter = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt({p["x"]}, 10, -1), gp_Dir(0, 0, 1)), {p["radius"]}, 12.0).Shape()\nshape = BRepAlgoAPI_Cut(base, cutter).Shape()\n'''
    if spec.family_id == "blind_hole":
        return f'''base = BRepPrimAPI_MakeBox(30.0, 20.0, 10.0).Shape()\ncutter = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(15, 10, {10-p["depth"]}), gp_Dir(0, 0, 1)), {p["radius"]}, {p["depth"]}).Shape()\nshape = BRepAlgoAPI_Cut(base, cutter).Shape()\n'''
    if spec.family_id == "rounded_slot":
        radius, x0 = p["width"] / 2, (30 - p["straight_length"]) / 2
        return f'''plate = BRepPrimAPI_MakeBox(30.0, 20.0, 5.0).Shape()\ncutter = BRepPrimAPI_MakeBox(gp_Pnt({x0}, {10-radius}, -1), {p["straight_length"]}, {p["width"]}, 7).Shape()\nfor x in ({x0}, {x0+p["straight_length"]}):\n    cutter = BRepAlgoAPI_Fuse(cutter, BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(x, 10, -1), gp_Dir(0, 0, 1)), {radius}, 7).Shape()).Shape()\nshape = BRepAlgoAPI_Cut(plate, cutter).Shape()\n'''
    if spec.family_id == "fillet":
        return f'''base = BRepPrimAPI_MakeBox(24.0, 18.0, 10.0).Shape()\noperation = BRepFilletAPI_MakeFillet(base)\noperation.Add({p["radius"]}, first_edge(base))\nshape = operation.Shape()\n'''
    return f'''base = BRepPrimAPI_MakeBox(24.0, 18.0, 10.0).Shape()\noperation = BRepFilletAPI_MakeChamfer(base)\noperation.Add({p["distance"]}, {p["distance"]}, first_edge(base), first_face(base))\nshape = operation.Shape()\n'''


def write_step(shape, target: Path) -> None:
    writer = STEPControl_Writer()
    writer.Transfer(shape, STEPControl_AsIs)
    if writer.Write(str(target)) != IFSelect_RetDone:
        raise RuntimeError(f"failed to write {target}")


def manifest_case(spec: Spec, baseline: dict[str, object]) -> dict[str, object]:
    root = f"case-library/self-authored/{spec.case_id}"
    return {
        "case_id": spec.case_id, "tier": "P2", "family_id": spec.family_id,
        "data_split": spec.data_split, "parameters": spec.parameters,
        "input_step": f"{root}/input.step", "expected_bbox": baseline["bbox"],
        "expected_counts": baseline["counts"], "expected_volume": baseline["volume"],
        "difficulty_tags": ["m12", "parametric", spec.family_id, spec.variant],
        "reference_script": f"{root}/reference_build_sequence.py",
        "notes": f"M12 {spec.family_id} {spec.variant} parameter variant.",
    }


def case_card(spec: Spec) -> str:
    return f'''# {spec.case_id}

- Origin: self-authored M12 parameter family
- Tier: P2
- Family: `{spec.family_id}`
- Split: `{spec.data_split}`
- Variant: `{spec.variant}`
- Parameters: `{json.dumps(spec.parameters, sort_keys=True)}` mm

## Assets

- Authoritative metadata: `case-library/self-authored/{spec.case_id}/case.json`
- Target B-Rep: `case-library/self-authored/{spec.case_id}/input.step`
- Deterministic reference: `case-library/self-authored/{spec.case_id}/reference_build_sequence.py`

This case is a deterministic local reference for geometry-equivalent replay. It
does not claim a unique inverse construction history.
'''


def main() -> None:
    grouped: dict[str, list[dict[str, object]]] = {"development": [], "held_out": []}
    for spec in SPECS:
        directory = CASE_ROOT / spec.case_id
        directory.mkdir(parents=True, exist_ok=True)
        shape = make_shape(spec)
        step_path = directory / "input.step"
        write_step(shape, step_path)
        baseline = expected(shape)
        digest = hashlib.sha256(step_path.read_bytes()).hexdigest()
        metadata = {
            "case_id": spec.case_id, "status": "active", "origin": "self_authored", "tier": "P2",
            "fixture_version": 1, "family_id": spec.family_id, "data_split": spec.data_split,
            "variant": spec.variant, "parameters": spec.parameters, "input_step": "input.step",
            "reference_script": "reference_build_sequence.py", "reference_script_status": "available",
            "sha256": digest, "unit": "mm", "coordinate_frame": "right_handed_xyz; model origin at (0,0,0)",
            "summary": f"M12 {spec.family_id} {spec.variant} parameter variant.", "key_dimensions": spec.parameters,
            "expected": baseline, "feature_tags": ["m12", "parametric", spec.family_id, spec.variant],
            "case_directory": f"case-library/self-authored/{spec.case_id}", "metadata_authority": "case.json",
        }
        (directory / "case.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
        (directory / "reference_build_sequence.py").write_text(script_text(spec), encoding="utf-8")
        (CASE_CARD_ROOT / f"{spec.case_id}.md").write_text(case_card(spec), encoding="utf-8")
        grouped[spec.data_split].append(manifest_case(spec, baseline))
    for split, cases in grouped.items():
        target = MANIFEST_ROOT / f"parametric-{split.replace('_', '-')}.json"
        target.write_text(json.dumps({"schema_version": 1, "cases": cases}, indent=2) + "\n", encoding="utf-8")
    registry_path = ROOT / "docs" / "corpus" / "registry" / "self-authored.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    registry["cases"] = [
        entry for entry in registry["cases"] if not entry["case_id"].startswith("param_")
    ]
    registry["cases"].extend(
        {
            "case_id": spec.case_id,
            "status": "active",
            "tier": "P2",
            "case_record": f"case-library/self-authored/{spec.case_id}/case.json",
        }
        for spec in SPECS
    )
    registry_path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
