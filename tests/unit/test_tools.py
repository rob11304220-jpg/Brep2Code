from pathlib import Path

import pytest

from brep2code.cases import validate_case
from brep2code.tools import ToolError, dispatch_tool


def test_brep_observations_omit_paths_hash_and_expected_reference() -> None:
    case = validate_case(Path("cases/smoke/box"), Path("cases"))

    observations = dispatch_tool("brep_observations", case)

    assert observations["case_id"] == "box"
    assert observations["brep"]["bbox"]["max"] == [10.0, 20.0, 30.0]
    assert observations["brep"]["surface_counts"] == {"plane": 6}
    assert "expected" not in observations
    serialized = repr(observations)
    assert "input.step" not in serialized
    assert case.metadata["sha256"] not in serialized
    assert str(case.case.root) not in serialized


def test_unknown_tool_is_rejected() -> None:
    case = validate_case(Path("cases/smoke/box"), Path("cases"))
    with pytest.raises(ToolError, match="unknown tool"):
        dispatch_tool("read_repository", case)


def test_edge_candidates_are_bounded_stable_and_path_free() -> None:
    case = validate_case(Path("cases/train/filleted_box"), Path("cases"))

    result = dispatch_tool("edge_candidates", case, {})

    assert result["edges_truncated"] is False
    assert len(result["edges"]) <= case.metadata["expected"]["counts"]["edge"]
    assert [edge["edge_id"] for edge in result["edges"]] == [
        f"edge-{index:03d}" for index in range(len(result["edges"]))
    ]
    assert all(edge["length"] > 0 for edge in result["edges"])
    assert all(1 <= len(edge["adjacent_faces"]) <= 2 for edge in result["edges"])
    assert any(edge["curve"] == "circle" for edge in result["edges"])
    assert all(len(edge["parameter_range"]) == 2 for edge in result["edges"])
    assert all(edge["identity"]["scope"] == "session" for edge in result["edges"])
    assert len({edge["identity"]["geometry_key"] for edge in result["edges"]}) == len(
        result["edges"]
    )
    assert all(edge["local_orientation"] is not None for edge in result["edges"])
    assert result["face_edge_incidence"]
    assert result["parallel_edge_groups"]
    assert result["faces_truncated"] is False
    serialized = repr(result)
    assert "input.step" not in serialized
    assert str(case.case.root) not in serialized


def test_ocp_symbol_reference_is_strictly_allowlisted() -> None:
    case = validate_case(Path("cases/smoke/box"), Path("cases"))

    reference = dispatch_tool("ocp_symbol", case, {"topic": "TopoDS.Edge_s"})

    assert reference["usage"] == "edge = TopoDS.Edge_s(shape)"
    scope_reference = dispatch_tool(
        "ocp_symbol", case, {"topic": "OCP.module_scope_imports"}
    )
    assert scope_reference == {
        "symbol": "OCP.module_scope_imports",
        "summary": "Keep every OCP import at Python module scope.",
        "usage": "Move each required OCP import above all function definitions.",
        "notes": [
            "Do not import OCP inside a function or method.",
            "Import only the OCP modules and symbols required by the script.",
        ],
    }
    curve_reference = dispatch_tool(
        "ocp_symbol", case, {"topic": "BRepAdaptor_Curve"}
    )
    assert curve_reference["usage"] == "curve = BRepAdaptor_Curve(edge)"
    map_reference = dispatch_tool(
        "ocp_symbol", case, {"topic": "TopExp.MapShapes_s"}
    )
    assert "TopTools_IndexedMapOfShape" in map_reference["notes"][0]
    assert "repository" not in repr(reference).lower()
    with pytest.raises(ToolError, match="not allowlisted"):
        dispatch_tool("ocp_symbol", case, {"topic": "private target solution"})


def test_edge_candidates_classify_convex_and_concave_dihedrals() -> None:
    box = validate_case(Path("cases/smoke/box"), Path("cases"))
    blind_hole = validate_case(Path("cases/train/blind_hole_block"), Path("cases"))

    box_edges = dispatch_tool("edge_candidates", box, {})["edges"]
    blind_hole_edges = dispatch_tool("edge_candidates", blind_hole, {})["edges"]

    assert {edge["dihedral"] for edge in box_edges} == {"convex"}
    assert any(edge["dihedral"] == "concave" for edge in blind_hole_edges)
    assert any(
        edge["curve"] == "circle" and edge["curve_parameters"]["radius"] > 0
        for edge in blind_hole_edges
    )
