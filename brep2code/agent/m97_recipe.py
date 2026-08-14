"""Locally verified OCP construction recipe for M97's declared through cut."""

from __future__ import annotations

from brep2code.agent.m97_observation import validate_m97_observation_context


M97_THROUGH_CUT_RECIPE_VERSION = "m97-ocp-through-cut-v1"


def build_m97_through_cut_recipe(context: str) -> str:
    """Render the supported +Z cutter recipe from a validated observation only."""

    transcript = validate_m97_observation_context(context)
    facts = transcript[0]["data"]
    bbox = facts["base_bbox"]
    cut = facts["cylindrical_cut"]
    minimum = bbox["min"]
    maximum = bbox["max"]
    length_x = maximum[0] - minimum[0]
    length_y = maximum[1] - minimum[1]
    length_z = maximum[2] - minimum[2]
    start_z = minimum[2] - 1.0
    height = length_z + 2.0
    x, y = cut["center_xy"]
    return f'''# {M97_THROUGH_CUT_RECIPE_VERSION}: local development conformance fixture.
from pathlib import Path

from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.IFSelect import IFSelect_RetDone
from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt

base = BRepPrimAPI_MakeBox({length_x!r}, {length_y!r}, {length_z!r}).Shape()
cutter = BRepPrimAPI_MakeCylinder(
    gp_Ax2(gp_Pnt({x!r}, {y!r}, {start_z!r}), gp_Dir(0, 0, 1)), {cut["radius"]!r}, {height!r}
).Shape()
shape = BRepAlgoAPI_Cut(base, cutter).Shape()
Path("output").mkdir(exist_ok=True)
writer = STEPControl_Writer()
writer.Transfer(shape, STEPControl_AsIs)
if writer.Write("output/model.step") != IFSelect_RetDone:
    raise RuntimeError("failed to write STEP")
'''
