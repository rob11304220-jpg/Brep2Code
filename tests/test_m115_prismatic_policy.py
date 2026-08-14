"""Offline contract tests for the M115 policy classifier."""

import json
from pathlib import Path

from tools.m115_prismatic_policy import M115_STATIC_API_CLASSIFIER_VERSION, classify_static_api


POLICY_PATH = Path("docs/corpus/registry/m115-prismatic-development-card-effect-policy-v1.json")


def _valid_script() -> str:
    return '''
from pathlib import Path
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.IFSelect import IFSelect_RetDone
from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt

base = BRepPrimAPI_MakeBox(20, 20, 10).Shape()
cutter = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(10, 10, -1), gp_Dir(0, 0, 1)), 2, 12).Shape()
shape = BRepAlgoAPI_Cut(base, cutter).Shape()
writer = STEPControl_Writer()
writer.Transfer(shape, STEPControl_AsIs)
'''


def test_m115_policy_is_fresh_development_only_and_offline() -> None:
    policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    assert policy["policy_id"] == "m115-prismatic-development-card-effect-v1"
    assert policy["status"] == "frozen_offline_prerequisite"
    assert policy["scope"]["held_out_access"] == "forbidden"
    assert policy["static_api_classifier"]["version"] == M115_STATIC_API_CLASSIFIER_VERSION
    assert policy["terminal_categories"]["policy_level"] == ["integrity_failed"]
    assert policy["terminal_categories"]["condition_level_order"] == [
        "lifecycle_ended_before_script",
        "static_api_inadmissible",
        "sandbox_execution_failed",
        "downstream_gate_failed",
        "full_success",
    ]
    assert policy["fresh_accounting"]["accounting_namespace"].startswith("m115-")


def test_m115_static_classifier_accepts_only_the_declared_recipe_surface() -> None:
    accepted = classify_static_api(_valid_script())
    assert accepted.category == "api_admissible"
    assert accepted.reason is None

    wrong_arity = classify_static_api(_valid_script().replace("BRepPrimAPI_MakeBox(20, 20, 10)", "BRepPrimAPI_MakeBox(20, 20)"))
    assert (wrong_arity.category, wrong_arity.reason) == ("api_inadmissible", "constructor_arity_mismatch")

    forbidden_import = classify_static_api(_valid_script().replace("from pathlib import Path", "from OCP.gp import gp_DZ"))
    assert (forbidden_import.category, forbidden_import.reason) == ("api_inadmissible", "missing_or_unsupported_import_symbol")

    missing_recipe = classify_static_api(_valid_script().replace("BRepAlgoAPI_Cut(base, cutter)", "base"))
    assert (missing_recipe.category, missing_recipe.reason) == ("api_inadmissible", "missing_through_cut_recipe")
