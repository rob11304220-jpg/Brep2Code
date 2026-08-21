import json
from pathlib import Path

from brep2code.cases import validate_case
from brep2code.harness import RepairLoopRunner
from brep2code.providers import FakeProvider
from brep2code.harness.compatibility import validate_script_compatibility


def test_compatibility_accepts_installed_ocp_imports() -> None:
    assert (
        validate_script_compatibility("from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox\n") is None
    )


def test_cadquery_profile_accepts_cadquery_and_skips_ocp_binding_rules() -> None:
    assert (
        validate_script_compatibility(
            "import cadquery as cq\nresult = cq.Workplane('XY').box(1, 2, 3)\n",
            "cadquery_v1",
        )
        is None
    )


def test_backend_profile_rejects_cross_backend_import() -> None:
    feedback = validate_script_compatibility("import cadquery as cq\n", "ocp_v1")

    assert feedback == {
        "stage": "generation",
        "reason": "backend_policy_violation",
        "backend_profile": "ocp_v1",
        "module": "cadquery",
        "message": "Backend profile ocp_v1 permits CAD imports only from OCP.",
    }


def test_cadquery_profile_rejects_ocp_import() -> None:
    feedback = validate_script_compatibility(
        "from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox\n", "cadquery_v1"
    )

    assert feedback is not None
    assert feedback["reason"] == "backend_policy_violation"
    assert feedback["backend_profile"] == "cadquery_v1"


def test_compatibility_rejects_unsupported_cad_import_without_script_content() -> None:
    feedback = validate_script_compatibility(
        "from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox\n"
    )

    assert feedback == {
        "stage": "generation",
        "reason": "unsupported_import",
        "module": "OCC",
        "message": (
            "Use imports from the installed OCP package only; do not use OCC.Core, Part, "
            "FreeCAD, or cadquery."
        ),
    }


def test_compatibility_checks_all_import_aliases() -> None:
    feedback = validate_script_compatibility("import math, OCC\n")

    assert feedback is not None
    assert feedback["reason"] == "unsupported_import"
    assert feedback["module"] == "OCC"


def test_compatibility_rejects_invalid_python_as_bounded_feedback() -> None:
    assert validate_script_compatibility("from OCP import\n") == {
        "stage": "generation",
        "reason": "syntax_error",
        "message": "Generated script is not valid Python.",
    }


def test_compatibility_rejects_function_local_ocp_import() -> None:
    feedback = validate_script_compatibility(
        "def build():\n    from OCP.TopExp import TopExp\n    return TopExp\n"
    )

    assert feedback == {
        "stage": "generation",
        "reason": "function_local_ocp_import",
        "scope": "module",
        "reference_topic": "OCP.module_scope_imports",
        "message": "Place every OCP import at module scope; do not import OCP inside functions.",
    }


def test_compatibility_rejects_unsuffixed_topexp_static_method() -> None:
    feedback = validate_script_compatibility("vertex = TopExp.FirstVertex(edge)\n")

    assert feedback == {
        "stage": "generation",
        "reason": "ocp_static_method_suffix",
        "method": "TopExp.FirstVertex",
        "replacement": "TopExp.FirstVertex_s",
        "message": "Use the OCP Python static-method binding with its _s suffix.",
    }


def test_compatibility_accepts_suffixed_topexp_static_method() -> None:
    assert validate_script_compatibility("vertex = TopExp.FirstVertex_s(edge)\n") is None


def test_compatibility_recommends_allowlisted_reference_for_direct_map_shapes() -> None:
    feedback = validate_script_compatibility("TopExp.MapShapes(shape, TopAbs_EDGE, edge_map)\n")

    assert feedback is not None
    assert feedback["method"] == "TopExp.MapShapes"
    assert feedback["replacement"] == "TopExp.MapShapes_s"
    assert feedback["reference_topic"] == "TopExp.MapShapes_s"


def test_compatibility_rejects_topexp_instance_static_method() -> None:
    feedback = validate_script_compatibility(
        "def collect(shape, edge_map):\n"
        "    exp = TopExp()\n"
        "    exp.MapShapes(shape, TopAbs_EDGE, edge_map)\n"
    )

    assert feedback == {
        "stage": "generation",
        "reason": "ocp_static_method_suffix",
        "method": "exp.MapShapes",
        "replacement": "TopExp.MapShapes_s",
        "reference_topic": "TopExp.MapShapes_s",
        "message": "Use the OCP Python static-method binding with its _s suffix.",
    }


def test_compatibility_does_not_treat_unrelated_instance_as_topexp() -> None:
    assert validate_script_compatibility("exp = Explorer()\nexp.MapShapes(shape)\n") is None


def test_compatibility_rejects_unsuffixed_topods_edge_downcast() -> None:
    feedback = validate_script_compatibility("edge = TopoDS.Edge(shape)\n")

    assert feedback == {
        "stage": "generation",
        "reason": "invalid_ocp_downcast",
        "symbol": "TopoDS.Edge",
        "replacement": "TopoDS.Edge_s",
        "reference_topic": "TopoDS.Edge_s",
        "message": "Use the OCP Python downcast binding with its _s suffix.",
    }


def test_compatibility_accepts_suffixed_topods_edge_downcast() -> None:
    assert validate_script_compatibility("edge = TopoDS.Edge_s(shape)\n") is None


def test_compatibility_rejects_legacy_topods_edge_downcast() -> None:
    feedback = validate_script_compatibility(
        "from OCP.TopoDS import topods\nedge = topods.Edge(shape)\n"
    )

    assert feedback == {
        "stage": "generation",
        "reason": "invalid_ocp_downcast",
        "symbol": "topods.Edge",
        "replacement": "TopoDS.Edge_s",
        "reference_topic": "TopoDS.Edge_s",
        "message": "Use the OCP Python downcast binding with its _s suffix.",
    }


def test_compatibility_rejects_legacy_topods_import_without_call() -> None:
    feedback = validate_script_compatibility("from OCP.TopoDS import topods\n")

    assert feedback == {
        "stage": "generation",
        "reason": "invalid_ocp_downcast",
        "symbol": "topods",
        "replacement": "TopoDS",
        "reference_topic": "TopoDS.Edge_s",
        "message": "Import and use the supported OCP TopoDS binding.",
    }


def test_compatibility_rejects_invalid_brep_tool_pnt_argument_count() -> None:
    feedback = validate_script_compatibility(
        "point = BRep_Tool.Pnt_s(edge, edge.FirstParameter())\n"
    )

    assert feedback == {
        "stage": "generation",
        "reason": "invalid_ocp_call_signature",
        "symbol": "BRep_Tool.Pnt_s",
        "expected_arguments": 1,
        "actual_arguments": 2,
        "reference_topic": "BRepAdaptor_Curve",
        "message": (
            "BRep_Tool.Pnt_s reads one vertex; retrieve the approved curve "
            "adaptor reference for parameterized edge evaluation."
        ),
    }


def test_compatibility_accepts_single_argument_brep_tool_pnt_call() -> None:
    assert validate_script_compatibility("point = BRep_Tool.Pnt_s(vertex)\n") is None


def test_compatibility_does_not_guess_dynamic_brep_tool_pnt_argument_count() -> None:
    assert validate_script_compatibility("point = BRep_Tool.Pnt_s(*arguments)\n") is None


def test_compatibility_aggregates_multiple_errors_in_stable_bounded_order() -> None:
    feedback = validate_script_compatibility(
        "from OCP.TopoDS import topods\n"
        "edge = topods.Edge(shape)\n"
        "TopExp.MapShapes(shape, TopAbs_EDGE, edge_map)\n"
        "point = BRep_Tool.Pnt_s(edge, parameter)\n"
    )

    assert feedback is not None
    assert feedback["reason"] == "compatibility_errors"
    assert feedback["issues_truncated"] is False
    assert [issue["reason"] for issue in feedback["issues"]] == [
        "invalid_ocp_downcast",
        "ocp_static_method_suffix",
        "invalid_ocp_call_signature",
    ]
    assert [issue.get("symbol") or issue.get("method") for issue in feedback["issues"]] == [
        "topods.Edge",
        "TopExp.MapShapes",
        "BRep_Tool.Pnt_s",
    ]
    assert [issue["reference_topic"] for issue in feedback["issues"]] == [
        "TopoDS.Edge_s",
        "TopExp.MapShapes_s",
        "BRepAdaptor_Curve",
    ]


def test_compatibility_truncates_aggregated_errors_at_fixed_limit() -> None:
    feedback = validate_script_compatibility(
        "import OCC\n"
        "def inspect():\n    from OCP.Geom import Geom_Line\n"
        "TopExp.FirstVertex(edge)\n"
        "TopExp.LastVertex(edge)\n"
        "TopExp.MapShapes(shape, TopAbs_EDGE, edge_map)\n"
        "edge = TopoDS.Edge(shape)\n"
    )

    assert feedback is not None
    assert feedback["reason"] == "compatibility_errors"
    assert len(feedback["issues"]) == 4
    assert feedback["issues_truncated"] is True


def test_repair_loop_rejects_unsupported_import_before_execution(tmp_path, monkeypatch) -> None:
    case = validate_case(Path("cases/smoke/box"), Path("cases"))
    provider = FakeProvider(["from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox\n"])
    executed = False

    def unexpected_execution(*args, **kwargs):
        nonlocal executed
        executed = True
        raise AssertionError("unsupported imports must be rejected before execution")

    monkeypatch.setattr("brep2code.harness.runner.run_untrusted_build", unexpected_execution)
    result = RepairLoopRunner(provider).run(case, tmp_path / "run", max_rounds=1)

    assert result.status == "budget_exhausted"
    assert result.stop_reason == "max_rounds"
    assert not executed
    payload = json.loads(result.result_path.read_text(encoding="utf-8"))
    assert payload["revisions"][0]["feedback"]["reason"] == "unsupported_import"


def test_repair_loop_passes_compatibility_feedback_to_next_request(tmp_path: Path) -> None:
    case = validate_case(Path("cases/smoke/box"), Path("cases"))
    unsupported = "from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox\n"
    provider = FakeProvider([unsupported, unsupported])

    result = RepairLoopRunner(provider).run(case, tmp_path / "run", max_rounds=2)

    assert result.status == "budget_exhausted"
    assert provider.requests[1].feedback == validate_script_compatibility(unsupported)
    assert provider.requests[1].previous_script == unsupported


def test_repair_loop_passes_ocp_binding_feedback_before_execution(
    tmp_path: Path, monkeypatch
) -> None:
    case = validate_case(Path("cases/smoke/box"), Path("cases"))
    unsupported = "vertex = TopExp.FirstVertex(edge)\n"
    provider = FakeProvider([unsupported])

    monkeypatch.setattr(
        "brep2code.harness.runner.run_untrusted_build",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("binding incompatibility must fail before execution")
        ),
    )
    result = RepairLoopRunner(provider).run(case, tmp_path / "run", max_rounds=1)

    payload = json.loads(result.result_path.read_text(encoding="utf-8"))
    assert payload["revisions"][0]["feedback"]["reason"] == "ocp_static_method_suffix"
