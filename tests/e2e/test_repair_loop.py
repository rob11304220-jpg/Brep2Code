from __future__ import annotations

import json
from pathlib import Path

import pytest

from brep2code.cases import validate_case
from brep2code.harness import RepairLoopRunner
from brep2code.providers import FakeProvider


pytestmark = pytest.mark.secure


BROKEN_BUILD = "raise RuntimeError('intentional first-pass failure')\n"
BOX_BUILD = '''\
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCP.IFSelect import IFSelect_RetDone
from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer

shape = BRepPrimAPI_MakeBox(10.0, 20.0, 30.0).Shape()
writer = STEPControl_Writer()
writer.Transfer(shape, STEPControl_AsIs)
if writer.Write("output.step") != IFSelect_RetDone:
    raise RuntimeError("failed to write STEP")
'''


def test_fake_provider_repairs_failed_box_and_persists_result(tmp_path: Path) -> None:
    case = validate_case(Path("cases/smoke/box"), Path("cases"))
    provider = FakeProvider([BROKEN_BUILD, BOX_BUILD])

    result = RepairLoopRunner(provider).run(case, tmp_path / "run", max_rounds=2)

    assert result.status == "succeeded"
    assert result.provider_requests == 2
    payload = json.loads(result.result_path.read_text(encoding="utf-8"))
    assert payload["status"] == "succeeded"
    assert payload["stop_reason"] == "passed"
    assert [revision["status"] for revision in payload["revisions"]] == [
        "failed",
        "succeeded",
    ]
    assert payload["revisions"][0]["feedback"]["stage"] == "execution"
    assert all(
        revision["execution"]["sandbox_backend"] == "wsl-bwrap"
        and revision["execution"]["sandboxed"] is True
        for revision in payload["revisions"]
    )
    assert "expected" not in provider.requests[0].context
    assert provider.requests[0].context["brep"]["surface_counts"] == {"plane": 6}
    assert provider.requests[1].feedback["stage"] == "execution"
    assert provider.requests[1].feedback["termination_reason"] == "script_error"
    assert provider.requests[1].previous_script == BROKEN_BUILD
    assert (tmp_path / "run/revision-000/build.py").read_text(encoding="utf-8") == BROKEN_BUILD
    assert (tmp_path / "run/revision-001/output.step").is_file()


def test_geometry_repair_receives_actual_expected_differences_and_previous_script(
    tmp_path: Path,
) -> None:
    case = validate_case(Path("cases/smoke/box"), Path("cases"))
    wrong_box = BOX_BUILD.replace("30.0).Shape()", "25.0).Shape()")
    provider = FakeProvider([wrong_box, BOX_BUILD])

    result = RepairLoopRunner(provider).run(case, tmp_path / "run", max_rounds=2)

    assert result.status == "succeeded"
    repair = provider.requests[1]
    assert repair.previous_script == wrong_box
    assert repair.feedback["stage"] == "geometry"
    assert repair.feedback["actual"]["bbox"]["max"] == [10.0, 20.0, 25.0]
    assert "expected" not in repair.feedback
    assert repair.feedback["differences_from_brep"]["bbox_max"] == [0.0, 0.0, -5.0]
    assert repair.feedback["differences_from_brep"]["volume"] == pytest.approx(-1000.0)


def test_initial_script_fails_geometry_then_one_provider_request_repairs_feature(
    tmp_path: Path,
) -> None:
    case = validate_case(Path("cases/smoke/block_with_hole"), Path("cases"))
    broken = Path("tests/fixtures/broken_block_with_hole.py").read_text(encoding="utf-8")
    fixed = Path("tests/fixtures/fixed_block_with_hole.py").read_text(encoding="utf-8")
    provider = FakeProvider([fixed])

    result = RepairLoopRunner(provider).run(
        case,
        tmp_path / "run",
        max_rounds=2,
        initial_script=broken,
    )

    assert result.status == "succeeded"
    assert result.provider_requests == 1
    payload = json.loads(result.result_path.read_text(encoding="utf-8"))
    assert payload["has_initial_script"] is True
    assert [revision["source"] for revision in payload["revisions"]] == [
        "initial_script",
        "provider",
    ]
    assert payload["revisions"][0]["status"] == "failed"
    assert payload["revisions"][0]["feedback"]["stage"] == "geometry"
    assert not (tmp_path / "run/revision-000/request.json").exists()
    repair = provider.requests[0]
    assert repair.round_index == 1
    assert repair.previous_script == broken
    assert "expected" not in repair.context
    assert repair.feedback["differences_from_brep"]["volume"] > 0
    assert (tmp_path / "run/revision-001/request.json").is_file()


def test_failed_loop_stops_at_revision_budget(tmp_path: Path) -> None:
    case = validate_case(Path("cases/smoke/box"), Path("cases"))
    result = RepairLoopRunner(FakeProvider([BROKEN_BUILD])).run(
        case, tmp_path / "run", max_rounds=1
    )

    assert result.status == "budget_exhausted"
    payload = json.loads(result.result_path.read_text(encoding="utf-8"))
    assert payload["stop_reason"] == "max_rounds"
    assert payload["provider_requests"] == 1


def test_provider_interruption_retains_terminal_checkpoint(tmp_path: Path) -> None:
    case = validate_case(Path("cases/smoke/box"), Path("cases"))
    result = RepairLoopRunner(FakeProvider([])).run(case, tmp_path / "run", max_rounds=1)

    assert result.status == "failed"
    payload = json.loads(result.result_path.read_text(encoding="utf-8"))
    assert payload["stop_reason"] == "provider_error"
    assert payload["provider_requests"] == 1
    assert payload["revisions"][0]["error"]["stage"] == "provider"
