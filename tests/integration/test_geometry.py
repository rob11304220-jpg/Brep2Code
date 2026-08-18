from pathlib import Path

import pytest

from brep2code.cases import validate_case
from brep2code.geometry.compare import compare_geometry
from brep2code.geometry.gates import GateDispatchError, dispatch_gates
from brep2code.geometry.inspect import inspect_step
from brep2code.geometry.observe import observe_step


def test_box_geometry_matches_case_contract() -> None:
    validated = validate_case(Path("cases/smoke/box"), Path("cases"))
    metrics = inspect_step(validated.case.input_step)

    assert metrics.bbox_min == (0.0, 0.0, 0.0)
    assert metrics.bbox_max == (10.0, 20.0, 30.0)
    assert compare_geometry(metrics, validated.metadata["expected"]).passed


def test_gate_dispatcher_returns_only_declared_gate_results() -> None:
    validated = validate_case(Path("cases/smoke/box"), Path("cases"))
    metrics = inspect_step(validated.case.input_step)

    report = dispatch_gates(metrics, validated.metadata["expected"], ["bbox", "volume"])

    assert report.passed is True
    assert report.required_gates == ("bbox", "volume")
    assert [result.gate_id for result in report.results] == ["bbox", "volume"]
    assert [signal.code for signal in report.as_signal_bundle().signals] == ["bbox", "volume"]


@pytest.mark.parametrize(
    "case_path",
    [
        Path("cases/eval/cylinder"),
        Path("cases/smoke/block_with_hole"),
        Path("cases/train/blind_hole_block"),
        Path("cases/train/filleted_box"),
    ],
)
def test_l0_l1_semantic_and_adjacency_gates_match_case_oracles(case_path: Path) -> None:
    validated = validate_case(case_path, Path("cases"))
    metrics = inspect_step(validated.case.input_step)
    harness = validated.dossier["harness_assets"]

    report = dispatch_gates(
        metrics,
        validated.metadata["expected"],
        harness["required_gates"],
        observations=observe_step(validated.case.input_step),
        gate_oracles=harness["gate_oracles"],
    )

    assert report.passed is True
    assert {result.gate_id for result in report.results} >= {"bbox", "volume", "topology"}


def test_fillet_observation_exposes_selected_edge_radius_and_axis() -> None:
    validated = validate_case(Path("cases/train/filleted_box"), Path("cases"))
    observations = observe_step(validated.case.input_step)

    assert observations["surface_counts"] == {"cylinder": 1, "plane": 6}
    fillet = next(face for face in observations["faces"] if face["surface"] == "cylinder")
    assert fillet["radius"] == 2.0
    assert fillet["axis_direction"] == [1.0, 0.0, 0.0]


def test_gate_dispatcher_rejects_undeclared_implementation() -> None:
    validated = validate_case(Path("cases/smoke/box"), Path("cases"))
    metrics = inspect_step(validated.case.input_step)

    with pytest.raises(GateDispatchError, match="unknown required gate"):
        dispatch_gates(metrics, validated.metadata["expected"], ["not_registered"])


def test_block_with_hole_observations_expose_bounded_cylindrical_feature() -> None:
    validated = validate_case(Path("cases/smoke/block_with_hole"), Path("cases"))

    observations = observe_step(validated.case.input_step)

    assert observations["bbox"] == {
        "min": [0.0, 0.0, 0.0],
        "max": [20.0, 20.0, 8.0],
    }
    assert observations["surface_counts"] == {"cylinder": 1, "plane": 6}
    cylinder = next(face for face in observations["faces"] if face["surface"] == "cylinder")
    assert cylinder["radius"] == 4.0
    assert cylinder["axis_direction"] == [0.0, 0.0, 1.0]
    assert cylinder["bbox"] == {
        "min": [6.0, 6.0, 0.0],
        "max": [14.0, 14.0, 8.0],
    }
    assert observations["faces_truncated"] is False
