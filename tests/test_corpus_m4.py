from __future__ import annotations

import json
from pathlib import Path
import re
from types import SimpleNamespace

from brep2code.cli import _build_parser, main
from brep2code.corpus import CorpusRunner, load_case_manifest
from brep2code.corpus.report import write_corpus_report
from brep2code.corpus.runner import CorpusCaseResult, CorpusRunResult, _repair_failure_type, corpus_run_to_dict
from brep2code.agent.provider import DeepSeekProvider, DeepSeekProviderError, FakeLLMProvider, LLMMessage, ProviderRequest
from brep2code.agent.repair import RepairLoopResult, RepairLoopRunner, _complete_provider
from brep2code.cad import WslBubblewrapExecutor
from brep2code.storage import RecordStore


FIXTURE_ROOT = Path(__file__).parent / "fixtures"
P0_MANIFEST = Path("case-library/manifests/self-authored/p0.json")
P1_MANIFEST = Path("case-library/manifests/self-authored/p1.json")
P2_MANIFEST = Path("case-library/manifests/self-authored/p2.json")
P3_MANIFEST = Path("case-library/manifests/self-authored/p3.json")
ABC_SELECTION = Path("docs/corpus/external/abc-v00-m8-001-selection.json")
ABC_MANIFEST = Path("docs/corpus/external/abc-v00-m8-001-manifest.json")
ABC_DEVELOPMENT_MANIFEST = Path("docs/corpus/external/abc-v00-m9-001-development-manifest.json")
ABC_HELD_OUT_MANIFEST = Path("docs/corpus/external/abc-v00-m9-001-held-out-manifest.json")
ABC_M10_SELECTION = Path("docs/corpus/external/abc-v00-m10-003-selection.json")
ABC_M10_DEVELOPMENT_MANIFEST = Path("docs/corpus/external/abc-v00-m10-003-development-manifest.json")
ABC_M10_HELD_OUT_MANIFEST = Path("docs/corpus/external/abc-v00-m10-003-held-out-manifest.json")
ABC_M10_SECOND_SELECTION = Path("docs/corpus/external/abc-v00-m10-007-selection.json")
ABC_M10_SECOND_DEVELOPMENT_MANIFEST = Path("docs/corpus/external/abc-v00-m10-007-development-manifest.json")
ABC_M10_SECOND_HELD_OUT_MANIFEST = Path("docs/corpus/external/abc-v00-m10-007-held-out-manifest.json")
ABC_M10_THIRD_SELECTION = Path("docs/corpus/external/abc-v00-m10-010-selection.json")
ABC_M10_THIRD_DEVELOPMENT_MANIFEST = Path("docs/corpus/external/abc-v00-m10-010-development-manifest.json")
ABC_M10_THIRD_HELD_OUT_MANIFEST = Path("docs/corpus/external/abc-v00-m10-010-held-out-manifest.json")


def test_load_case_manifest_resolves_p0_cases() -> None:
    manifest = load_case_manifest(P0_MANIFEST)

    assert manifest.schema_version == 1
    assert [case.case_id for case in manifest.cases] == ["box", "cylinder", "block_with_hole"]
    assert all(case.input_step.is_absolute() for case in manifest.cases)
    assert manifest.cases[0].expected_counts == {"solid": 1, "shell": 1, "face": 6, "edge": 24}
    assert manifest.cases[1].reference_script is not None


def test_run_parser_exposes_opt_in_no_input_build_mode() -> None:
    args = _build_parser().parse_args(["run", "--record", "fixture", "--build-without-input"])

    assert args.build_without_input is True


def test_schema_v3_report_projects_additive_provenance_object() -> None:
    provenance = {
        "version": "reconstruction-provenance-v1",
        "classification": "round_trip",
        "coverage": True,
        "coverage_attestation": {"normal_run": True},
        "normal_trace_path": "traces/provenance-input-access.log",
        "normal_input_accesses": ["pid=42 path=/input/model.step"],
        "absent_input_control": {"status": "not_run", "reason": "normal_input_read"},
    }
    case = CorpusCaseResult(
        case_id="fixture",
        tier="P0",
        record_id="corpus-fixture",
        revision_id="revision",
        status="pass",
        gate_statuses={"script_exit_code": "pass"},
        failure_type=None,
        signal_bundle_path="signal_bundle.json",
        probes={},
        provenance=provenance,
        observation={"schema_version": 1, "session_id": "obs-1", "transcript_sha256": "a" * 64},
    )
    result = CorpusRunResult(
        run_id="run",
        manifest_path="manifest.json",
        report_path=None,
        cases=(case,),
        summary={},
        generation_policy={"id": "first-pass-summary-v1"},
    )

    payload = corpus_run_to_dict(result)

    assert payload["schema_version"] == 3
    assert payload["cases"][0]["provenance"] == provenance
    assert payload["cases"][0]["observation"]["session_id"] == "obs-1"


def test_load_case_manifest_resolves_p1_cases() -> None:
    manifest = load_case_manifest(P1_MANIFEST)

    assert manifest.schema_version == 1
    assert [case.case_id for case in manifest.cases] == [
        "filleted_block",
        "chamfered_block",
        "three_hole_plate",
        "box_cylinder_union",
    ]
    assert all(case.tier == "P1" for case in manifest.cases)
    assert all(case.input_step.is_absolute() for case in manifest.cases)
    assert all(case.reference_script is not None for case in manifest.cases)
    assert "array" in manifest.cases[2].difficulty_tags


def test_load_case_manifest_resolves_expanded_p2_and_p3_cases() -> None:
    p2_manifest = load_case_manifest(P2_MANIFEST)
    p3_manifest = load_case_manifest(P3_MANIFEST)

    assert len(p2_manifest.cases) == 9
    assert len(p3_manifest.cases) == 5
    assert all(case.tier == "P2" and case.reference_script is not None for case in p2_manifest.cases)
    assert all(case.tier == "P3" and case.reference_script is not None for case in p3_manifest.cases)


def test_abc_m8_selection_and_local_manifest_are_auditable_without_data_files() -> None:
    selection = json.loads(ABC_SELECTION.read_text(encoding="utf-8"))
    manifest = json.loads(ABC_MANIFEST.read_text(encoding="utf-8"))

    assert selection["dataset_id"] == "abc"
    assert selection["upstream_release"] == "v00"
    assert selection["license_review"]["redistribution_permitted"] is False
    assert selection["normalization"]["transform_applied"] is None
    samples = selection["samples"]
    assert len(samples) == 12
    assert [sample["split"] for sample in samples].count("development") == 8
    assert [sample["split"] for sample in samples].count("held_out") == 4
    assert len({sample["source_sample_id"] for sample in samples}) == 12
    assert all(re.fullmatch(r"[0-9a-f]{64}", sample["source_sha256"]) for sample in samples)
    assert all(sample["local_storage"].startswith("data/datasets/abc/v00/") for sample in samples)

    cases = manifest["cases"]
    assert len(cases) == 12
    assert [case["case_id"] for case in cases] == [sample["case_id"] for sample in samples]
    assert all(case["input_step"].startswith("data/datasets/abc/v00/") for case in cases)
    assert all("reference_script" not in case and "first_pass_script" not in case for case in cases)
    assert all(case["expected_bbox"] and case["expected_counts"] and case["expected_volume"] for case in cases)


def test_abc_m9_split_manifests_preserve_the_m8_selection_without_fixtures() -> None:
    selection = json.loads(ABC_SELECTION.read_text(encoding="utf-8"))
    all_cases = json.loads(ABC_MANIFEST.read_text(encoding="utf-8"))["cases"]
    development_cases = json.loads(ABC_DEVELOPMENT_MANIFEST.read_text(encoding="utf-8"))["cases"]
    held_out_cases = json.loads(ABC_HELD_OUT_MANIFEST.read_text(encoding="utf-8"))["cases"]

    selected_ids = [sample["case_id"] for sample in selection["samples"]]
    development_ids = [case["case_id"] for case in development_cases]
    held_out_ids = [case["case_id"] for case in held_out_cases]

    assert development_ids == selected_ids[:8]
    assert held_out_ids == selected_ids[8:]
    assert development_ids + held_out_ids == [case["case_id"] for case in all_cases]
    assert set(development_ids).isdisjoint(held_out_ids)
    for cases in (development_cases, held_out_cases):
        assert all(case["input_step"].startswith("data/datasets/abc/v00/") for case in cases)
        assert all("reference_script" not in case and "first_pass_script" not in case for case in cases)
        assert all(case["expected_bbox"] and case["expected_counts"] and case["expected_volume"] for case in cases)


def test_abc_m10_increment_is_bounded_split_preserving_and_fixture_free() -> None:
    selection = json.loads(ABC_M10_SELECTION.read_text(encoding="utf-8"))
    development_cases = json.loads(ABC_M10_DEVELOPMENT_MANIFEST.read_text(encoding="utf-8"))["cases"]
    held_out_cases = json.loads(ABC_M10_HELD_OUT_MANIFEST.read_text(encoding="utf-8"))["cases"]

    assert selection["selection_status"] == "completed"
    assert selection["selection_policy"]["scan_start_source_sample_id"] == "00000023"
    assert selection["selection_policy"]["scan_cutoff_source_sample_id"] == "00000026"
    assert selection["license_review"]["redistribution_permitted"] is False
    samples = selection["samples"]
    assert [sample["source_sample_id"] for sample in samples] == ["00000023", "00000024", "00000026"]
    assert [sample["split"] for sample in samples] == ["development", "development", "held_out"]
    assert selection["rejected_candidates"] == [
        {"source_sample_id": "00000025", "reason": "solid_count_not_one", "solid_count": 3}
    ]
    assert all(re.fullmatch(r"[0-9a-f]{64}", sample["source_sha256"]) for sample in samples)

    development_ids = [case["case_id"] for case in development_cases]
    held_out_ids = [case["case_id"] for case in held_out_cases]
    assert development_ids == ["abc_v00_00000023", "abc_v00_00000024"]
    assert held_out_ids == ["abc_v00_00000026"]
    assert development_ids + held_out_ids == [sample["case_id"] for sample in samples]
    assert set(development_ids).isdisjoint(held_out_ids)
    for cases in (development_cases, held_out_cases):
        assert all(case["input_step"].startswith("data/datasets/abc/v00/") for case in cases)
        assert all("reference_script" not in case and "first_pass_script" not in case for case in cases)
        assert all(case["expected_bbox"] and case["expected_counts"] and case["expected_volume"] for case in cases)


def test_abc_m10_second_increment_continues_prior_cutoff_without_fixtures() -> None:
    selection = json.loads(ABC_M10_SECOND_SELECTION.read_text(encoding="utf-8"))
    development_cases = json.loads(ABC_M10_SECOND_DEVELOPMENT_MANIFEST.read_text(encoding="utf-8"))["cases"]
    held_out_cases = json.loads(ABC_M10_SECOND_HELD_OUT_MANIFEST.read_text(encoding="utf-8"))["cases"]

    assert selection["selection_status"] == "completed"
    assert selection["selection_policy"]["scan_start_source_sample_id"] == "00000027"
    assert selection["selection_policy"]["scan_cutoff_source_sample_id"] == "00000031"
    assert [sample["source_sample_id"] for sample in selection["samples"]] == ["00000027", "00000030", "00000031"]
    assert [sample["split"] for sample in selection["samples"]] == ["development", "development", "held_out"]
    assert selection["rejected_candidates"] == [
        {"source_sample_id": "00000028", "reason": "solid_count_not_one", "solid_count": 3},
        {"source_sample_id": "00000029", "reason": "solid_count_not_one", "solid_count": 2},
    ]
    assert all(re.fullmatch(r"[0-9a-f]{64}", sample["source_sha256"]) for sample in selection["samples"])
    assert [case["case_id"] for case in development_cases] == ["abc_v00_00000027", "abc_v00_00000030"]
    assert [case["case_id"] for case in held_out_cases] == ["abc_v00_00000031"]
    for cases in (development_cases, held_out_cases):
        assert all(case["input_step"].startswith("data/datasets/abc/v00/") for case in cases)
        assert all("reference_script" not in case and "first_pass_script" not in case for case in cases)
        assert all(case["expected_bbox"] and case["expected_counts"] and case["expected_volume"] for case in cases)


def test_abc_m10_third_increment_uses_verified_cache_but_remains_bounded_and_fixture_free() -> None:
    selection = json.loads(ABC_M10_THIRD_SELECTION.read_text(encoding="utf-8"))
    development_cases = json.loads(ABC_M10_THIRD_DEVELOPMENT_MANIFEST.read_text(encoding="utf-8"))["cases"]
    held_out_cases = json.loads(ABC_M10_THIRD_HELD_OUT_MANIFEST.read_text(encoding="utf-8"))["cases"]

    assert selection["selection_status"] == "completed"
    assert selection["selection_policy"]["scan_start_source_sample_id"] == "00000032"
    assert selection["selection_policy"]["scan_cutoff_source_sample_id"] == "00000035"
    assert selection["selection_policy"]["cache_boundary"].startswith("complete ignored local cache")
    assert [sample["source_sample_id"] for sample in selection["samples"]] == ["00000032", "00000033", "00000035"]
    assert [sample["split"] for sample in selection["samples"]] == ["development", "development", "held_out"]
    assert selection["rejected_candidates"] == [
        {"source_sample_id": "00000034", "reason": "solid_count_not_one", "solid_count": 3}
    ]
    assert all(re.fullmatch(r"[0-9a-f]{64}", sample["source_sha256"]) for sample in selection["samples"])
    assert [case["case_id"] for case in development_cases] == ["abc_v00_00000032", "abc_v00_00000033"]
    assert [case["case_id"] for case in held_out_cases] == ["abc_v00_00000035"]
    for cases in (development_cases, held_out_cases):
        assert all(case["input_step"].startswith("data/datasets/abc/v00/") for case in cases)
        assert all("reference_script" not in case and "first_pass_script" not in case for case in cases)
        assert all(case["expected_bbox"] and case["expected_counts"] and case["expected_volume"] for case in cases)


def test_corpus_cli_keeps_unsafe_default_and_exposes_wsl_bwrap_opt_in() -> None:
    parser = _build_parser()

    default_args = parser.parse_args(["corpus", "--manifest", "example.json"])
    secure_args = parser.parse_args(["corpus", "--manifest", "example.json", "--executor", "wsl-bwrap"])

    assert default_args.executor == "unsafe-local"
    assert secure_args.executor == "wsl-bwrap"


def test_load_case_manifest_rejects_duplicate_case_ids(tmp_path: Path) -> None:
    manifest_path = tmp_path / "cases.json"
    manifest_path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "cases": [
                    {
                        "case_id": "dup",
                        "tier": "P0",
                        "input_step": "case-library/self-authored/box/input.step",
                    },
                    {
                        "case_id": "dup",
                        "tier": "P0",
                        "input_step": "case-library/self-authored/box/input.step",
                    },
                ],
            }
        ),
        encoding="utf-8",
    )

    try:
        load_case_manifest(manifest_path)
    except ValueError as exc:
        assert "duplicate case_id" in str(exc)
    else:
        raise AssertionError("expected duplicate case_id validation failure")


def test_corpus_runner_writes_compact_report(tmp_path: Path) -> None:
    manifest = load_case_manifest(P0_MANIFEST)
    runner = CorpusRunner()
    runner.harness.store = RecordStore(tmp_path / "data")

    result = runner.run(
        manifest,
        record_prefix="test-corpus",
        report_path=tmp_path / "report.json",
    )

    assert result.summary["total_cases"] == 3
    assert result.summary["by_status"]["pass"] == 1
    assert result.summary["by_status"]["fail"] == 2
    assert (tmp_path / "report.json").exists()
    payload = json.loads((tmp_path / "report.json").read_text(encoding="utf-8"))
    assert payload["schema_version"] == 1
    assert payload["cases"][0]["case_id"] == "box"
    assert payload["cases"][0]["gate_statuses"]["script_exit_code"] == "pass"
    assert payload["cases"][1]["failure_type"] == "gate_failure"


def test_corpus_runner_executes_p1_manifest(tmp_path: Path) -> None:
    manifest = load_case_manifest(P1_MANIFEST)
    runner = CorpusRunner()
    runner.harness.store = RecordStore(tmp_path / "data")

    result = runner.run(
        manifest,
        record_prefix="test-p1-corpus",
        report_path=tmp_path / "p1-report.json",
    )

    assert result.summary["total_cases"] == 4
    assert result.summary["by_status"] == {"fail": 4}
    assert result.summary["by_tier"] == {"P1": {"fail": 4}}
    assert {case.failure_type for case in result.cases} == {"gate_failure"}
    assert (tmp_path / "p1-report.json").exists()


def test_corpus_runner_replays_reference_script_with_fake_provider(tmp_path: Path) -> None:
    manifest_path = tmp_path / "cylinder.json"
    manifest_path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "cases": [
                    {
                        "case_id": "cylinder",
                        "tier": "P0",
                        "input_step": "case-library/self-authored/cylinder/input.step",
                        "reference_script": (
                            "case-library/self-authored/cylinder/reference_build_sequence.py"
                        ),
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    runner = CorpusRunner()
    runner.harness.store = RecordStore(tmp_path / "data")

    result = runner.run(load_case_manifest(manifest_path), record_prefix="repair-corpus", repair=True)

    assert result.cases[0].status == "fail"
    assert result.cases[0].repair is not None
    assert result.cases[0].repair["status"] == "pass"
    assert [attempt["status"] for attempt in result.cases[0].repair["attempts"]] == ["fail", "pass"]


def test_corpus_cli_runs_fake_first_pass_and_writes_v3_report(tmp_path: Path, capsys) -> None:
    report_path = tmp_path / "first-pass.json"

    exit_code = main(
        [
            "corpus",
            "--manifest",
            str(P0_MANIFEST),
            "--case-id",
            "cylinder",
            "--first-pass",
            "--report",
            str(report_path),
            "--data-root",
            str(tmp_path / "data"),
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["schema_version"] == 3
    assert payload["generation_policy"]["id"] == "first-pass-summary-v1"
    generation = payload["cases"][0]["primary_generation"]
    assert generation["status"] == "pass"
    assert generation["provider_requests"] == 1
    assert generation["duration_seconds"] >= 0
    assert generation["probe_summary"]["ok"] is True
    assert payload["cases"][0]["repair"] is None
    assert payload["cases"][0]["fake_provider_replay"] is None
    trace_dir = Path(generation["signal_bundle_path"]).parent / "traces"
    assert (trace_dir / "provider_response.json").exists()
    assert "test-key" not in (trace_dir / "provider_response.json").read_text(encoding="utf-8")
    request_trace = (trace_dir / "llm_messages.jsonl").read_text(encoding="utf-8")
    assert "/input/model.step" in request_trace
    assert "output/model.step" in request_trace
    assert "not OCC.Core" in request_trace
    assert str(Path("case-library/self-authored/cylinder/input.step").resolve()) not in request_trace


def test_first_pass_failure_uses_distinct_fake_replay_field(tmp_path: Path) -> None:
    manifest_path = tmp_path / "first-pass-failure.json"
    manifest_path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "cases": [
                    {
                        "case_id": "cylinder",
                        "tier": "P0",
                        "input_step": "case-library/self-authored/cylinder/input.step",
                        "first_pass_script": "case-library/test-support/first_pass_broken.py",
                        "reference_script": "case-library/self-authored/cylinder/reference_build_sequence.py",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    runner = CorpusRunner()
    runner.harness.store = RecordStore(tmp_path / "data")
    result = runner.run(load_case_manifest(manifest_path), first_pass=True, repair=True, provider=FakeLLMProvider())
    payload = corpus_run_to_dict(result)

    assert payload["schema_version"] == 3
    case = payload["cases"][0]
    assert case["primary_generation"]["status"] == "fail"
    assert case["repair"] is None
    assert case["fake_provider_replay"]["status"] == "pass"


def test_fake_first_pass_refuses_missing_manifest_script_without_running(tmp_path: Path, capsys) -> None:
    exit_code = main(
        [
            "corpus",
            "--manifest",
            str(P0_MANIFEST),
            "--case-id",
            "box",
            "--first-pass",
            "--data-root",
            str(tmp_path / "data"),
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 2
    assert payload["status"] == "configuration_error"
    assert "first_pass_script" in payload["error"]
    assert not (tmp_path / "data").exists()


def test_first_pass_input_probe_failure_does_not_call_provider_or_consume_budget(tmp_path: Path, monkeypatch) -> None:
    manifest_path = tmp_path / "input-probe-failure.json"
    manifest_path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "cases": [
                    {
                        "case_id": "box",
                        "tier": "P0",
                        "input_step": "case-library/self-authored/box/input.step",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    class NoCallProvider:
        model = "no-call"

        def complete(self, _request):
            raise AssertionError("provider must not run after an input-probe failure")

    monkeypatch.setattr(
        "brep2code.corpus.runner.safe_probe_summary",
        lambda *_args, **_kwargs: {
            "ok": False,
            "input": "box.step",
            "error": {"code": "probe_timeout", "message": "timed out"},
        },
    )
    runner = CorpusRunner()
    runner.harness.store = RecordStore(tmp_path / "data")

    result = runner.run(load_case_manifest(manifest_path), first_pass=True, provider=NoCallProvider())
    payload = corpus_run_to_dict(result)
    generation = payload["cases"][0]["primary_generation"]

    assert generation["status"] == "not_run"
    assert generation["failure_type"] == "input_probe_failure"
    assert generation["provider_requests"] == 0
    assert generation["error"]["code"] == "input_probe_failure"


def test_first_pass_hosted_budget_includes_generation_request(tmp_path: Path, capsys) -> None:
    exit_code = main(
        [
            "corpus",
            "--manifest",
            str(P0_MANIFEST),
            "--case-id",
            "cylinder",
            "--first-pass",
            "--provider",
            "deepseek",
            "--authorize-hosted",
            "--max-cases",
            "1",
            "--max-rounds",
            "1",
            "--request-budget",
            "3",
            "--data-root",
            str(tmp_path / "data"),
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 2
    assert payload["status"] == "configuration_error"
    assert "request-budget" in payload["error"]


def test_corpus_runner_replays_p1_reference_script_with_fake_provider(tmp_path: Path) -> None:
    manifest_path = tmp_path / "three-hole.json"
    manifest_path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "cases": [
                    {
                        "case_id": "three_hole_plate",
                        "tier": "P1",
                        "input_step": "case-library/self-authored/three_hole_plate/input.step",
                        "reference_script": (
                            "case-library/self-authored/three_hole_plate/reference_build_sequence.py"
                        ),
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    runner = CorpusRunner()
    runner.harness.store = RecordStore(tmp_path / "data")

    result = runner.run(load_case_manifest(manifest_path), record_prefix="repair-p1", repair=True)

    assert result.cases[0].status == "fail"
    assert result.cases[0].repair is not None
    assert result.cases[0].repair["status"] == "pass"
    assert [attempt["status"] for attempt in result.cases[0].repair["attempts"]] == ["fail", "pass"]


def test_corpus_cli_runs_manifest_and_writes_report(tmp_path: Path, capsys) -> None:
    exit_code = main(
        [
            "corpus",
            "--manifest",
            str(P0_MANIFEST),
            "--data-root",
            str(tmp_path / "data"),
            "--report",
            str(tmp_path / "corpus-report.json"),
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 1
    assert payload["summary"]["total_cases"] == 3
    assert payload["report_path"] == str(tmp_path / "corpus-report.json")


def test_corpus_cli_selects_exact_case_without_running_other_manifest_cases(tmp_path: Path, capsys) -> None:
    exit_code = main(
        [
            "corpus",
            "--manifest",
            str(P0_MANIFEST),
            "--case-id",
            "box",
            "--data-root",
            str(tmp_path / "data"),
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["summary"]["total_cases"] == 1
    assert payload["cases"][0]["case_id"] == "box"


def test_corpus_cli_rejects_unknown_case_id_without_running(tmp_path: Path, capsys) -> None:
    exit_code = main(
        [
            "corpus",
            "--manifest",
            str(P0_MANIFEST),
            "--case-id",
            "missing",
            "--data-root",
            str(tmp_path / "data"),
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 2
    assert payload["status"] == "configuration_error"
    assert not (tmp_path / "data").exists()


def test_corpus_cli_refuses_hosted_requests_without_explicit_authorization(tmp_path: Path, capsys) -> None:
    exit_code = main(
        [
            "corpus",
            "--manifest",
            str(P0_MANIFEST),
            "--provider",
            "deepseek",
            "--data-root",
            str(tmp_path / "data"),
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 2
    assert payload["status"] == "authorization_required"


def test_corpus_cli_refuses_hosted_requests_without_request_budget(tmp_path: Path, capsys) -> None:
    exit_code = main(
        [
            "corpus",
            "--manifest",
            str(P0_MANIFEST),
            "--provider",
            "deepseek",
            "--authorize-hosted",
            "--max-cases",
            "1",
            "--data-root",
            str(tmp_path / "data"),
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 2
    assert payload["status"] == "configuration_error"
    assert "--request-budget" in payload["error"]


def test_corpus_cli_refuses_nonpositive_provider_timeout(tmp_path: Path, capsys) -> None:
    exit_code = main(
        [
            "corpus",
            "--manifest",
            str(P0_MANIFEST),
            "--provider",
            "deepseek",
            "--authorize-hosted",
            "--max-cases",
            "1",
            "--request-budget",
            "1",
            "--provider-timeout",
            "0",
            "--data-root",
            str(tmp_path / "data"),
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 2
    assert payload["status"] == "configuration_error"
    assert "--provider-timeout" in payload["error"]


def test_corpus_runner_requires_secure_executor_for_hosted_provider() -> None:
    runner = CorpusRunner()
    manifest = load_case_manifest(P0_MANIFEST)

    try:
        runner.run(
            manifest,
            provider=FakeLLMProvider(),
            hosted_options={"max_cases": 1, "max_rounds": 1, "request_budget": 1, "authorization": "test"},
        )
    except ValueError as exc:
        assert "WslBubblewrapExecutor" in str(exc)
    else:
        raise AssertionError("expected hosted evaluation to reject unsafe-local executor")


def test_hosted_report_payload_is_versioned_and_sanitized() -> None:
    result = CorpusRunResult(
        run_id="hosted-run",
        manifest_path="case-library/manifests/self-authored/p0.json",
        report_path=None,
        cases=(),
        summary={"total_cases": 0},
        evaluation={
            "mode": "hosted",
            "provider": "deepseek",
            "model": "deepseek-v4-flash",
            "request_budget": 1,
            "requests_used": 0,
        },
    )

    payload = corpus_run_to_dict(result)

    assert payload["schema_version"] == 2
    assert payload["evaluation"]["provider"] == "deepseek"
    assert "api_key" not in payload["evaluation"]


def test_hosted_repair_failure_taxonomy_classifies_sandbox_refusal() -> None:
    assert _repair_failure_type(
        {"status": "not_run", "error": {"code": "sandbox_unavailable", "message": "unavailable"}}
    ) == "sandbox"


def test_fake_provider_completion_remains_in_process_and_deterministic() -> None:
    provider = FakeLLMProvider()
    response = _complete_provider(
        provider,
        ProviderRequest(messages=[LLMMessage(role="user", content="test")], model="fake"),
        timeout_seconds=1,
    )

    assert response.provider == "fake"
    assert len(provider.requests) == 1


def test_deepseek_provider_completion_uses_serializable_bounded_worker() -> None:
    provider = DeepSeekProvider(api_key="test-key", base_url="http://127.0.0.1:1")

    try:
        _complete_provider(
            provider,
            ProviderRequest(messages=[LLMMessage(role="user", content="test")], model="deepseek-v4-flash"),
            timeout_seconds=1,
        )
    except DeepSeekProviderError as exc:
        assert "DeepSeek" in str(exc)
    else:
        raise AssertionError("expected loopback provider request to fail")


def test_deepseek_timeout_terminates_and_joins_worker(monkeypatch, tmp_path: Path) -> None:
    process = _TimeoutProcess()
    monkeypatch.setattr("brep2code.agent.repair.mp.get_context", lambda _method: _TimeoutContext(process))
    initial = tmp_path / "broken_build.py"
    initial.write_text("raise RuntimeError('boom')\n", encoding="utf-8")
    runner = RepairLoopRunner(provider=DeepSeekProvider(api_key="test-key"))
    runner.harness.store = RecordStore(tmp_path / "data")

    result = runner.run("deadline", initial, max_rounds=1, provider_timeout=7)

    assert result.status == "provider_error"
    assert result.stop_reason == "provider_request_timeout"
    assert result.provider_requests == 1
    assert process.started is True
    assert process.join_timeouts == [7, None]
    assert process.terminated is True
    trace_dir = Path(result.attempts[0].signal_bundle_path).parent / "traces"
    assert not (trace_dir / "provider_response.json").exists()


def test_loopback_provider_failure_counts_issued_request_and_writes_no_response_trace(tmp_path: Path) -> None:
    initial = tmp_path / "broken_build.py"
    initial.write_text("raise RuntimeError('boom')\n", encoding="utf-8")
    runner = RepairLoopRunner(provider=DeepSeekProvider(api_key="test-key", base_url="http://127.0.0.1:1"))
    runner.harness.store = RecordStore(tmp_path / "data")

    result = runner.run("loopback-error", initial, max_rounds=1, provider_timeout=5)

    assert result.status == "provider_error"
    assert result.stop_reason == "provider_request_failed"
    assert result.error is not None and result.error["code"] == "provider_request_failed"
    assert result.provider_requests == 1
    trace_dir = Path(result.attempts[0].signal_bundle_path).parent / "traces"
    assert not (trace_dir / "provider_response.json").exists()


def test_hosted_report_counts_timeout_request_when_case_is_checkpointed(tmp_path: Path) -> None:
    manifest = load_case_manifest(P0_MANIFEST)
    runner = _ProviderErrorCorpusRunner(_FailingHostedHarness(tmp_path))
    report_path = tmp_path / "hosted-checkpoint.json"

    result = runner.run(
        manifest,
        report_path=report_path,
        provider=DeepSeekProvider(api_key="test-key"),
        hosted_options={
            "max_cases": 1,
            "max_rounds": 1,
            "request_budget": 1,
            "provider_timeout": 120,
            "authorization": "test",
        },
    )

    assert result.run_status == "completed"
    assert result.evaluation is not None and result.evaluation["requests_used"] == 1
    payload = json.loads(report_path.read_text(encoding="utf-8"))
    assert payload["run_status"] == "completed"
    assert payload["evaluation"]["requests_used"] == 1
    assert payload["cases"][0]["repair"]["error"]["code"] == "provider_request_timeout"


def test_corpus_report_replaces_atomically(tmp_path: Path) -> None:
    report_path = tmp_path / "report.json"

    write_corpus_report(report_path, {"run_status": "running"})

    assert json.loads(report_path.read_text(encoding="utf-8")) == {"run_status": "running"}
    assert list(tmp_path.glob(".report.json.*.tmp")) == []


def test_corpus_runner_checkpoints_completed_cases_on_interruption(tmp_path: Path) -> None:
    manifest = load_case_manifest(P0_MANIFEST)
    runner = CorpusRunner(harness=_InterruptingHarness(tmp_path))
    report_path = tmp_path / "checkpoint.json"

    try:
        runner.run(manifest, record_prefix="checkpoint", report_path=report_path)
    except RuntimeError as exc:
        assert str(exc) == "simulated interruption"
    else:
        raise AssertionError("expected simulated interruption")

    payload = json.loads(report_path.read_text(encoding="utf-8"))
    assert payload["run_status"] == "interrupted"
    assert payload["interruption"] == {
        "code": "runner_exception",
        "case_id": "cylinder",
        "exception_type": "RuntimeError",
    }
    assert [case["case_id"] for case in payload["cases"]] == ["box"]
    assert payload["summary"]["by_status"] == {"pass": 1}


def test_corpus_runner_keeps_running_checkpoint_after_external_force_stop(tmp_path: Path) -> None:
    manifest = load_case_manifest(P0_MANIFEST)
    runner = CorpusRunner(harness=_ExternallyStoppedHarness(tmp_path))
    report_path = tmp_path / "running-checkpoint.json"

    try:
        runner.run(manifest, record_prefix="external-stop", report_path=report_path)
    except _ExternalForceStop:
        pass
    else:
        raise AssertionError("expected simulated external force stop")

    payload = json.loads(report_path.read_text(encoding="utf-8"))
    assert payload["run_status"] == "running"
    assert "interruption" not in payload
    assert [case["case_id"] for case in payload["cases"]] == ["box"]


def test_default_corpus_and_fake_repair_never_construct_deepseek_provider(monkeypatch, tmp_path: Path, capsys) -> None:
    def fail_if_constructed(*_args, **_kwargs):
        raise AssertionError("default offline paths must not construct DeepSeekProvider")

    monkeypatch.setattr("brep2code.cli.DeepSeekProvider.from_env_file", fail_if_constructed)

    default_exit = main(
        [
            "corpus",
            "--manifest",
            str(P0_MANIFEST),
            "--case-id",
            "box",
            "--data-root",
            str(tmp_path / "default-data"),
        ]
    )
    default_payload = json.loads(capsys.readouterr().out)
    replacement = Path("case-library/self-authored/cylinder/reference_build_sequence.py")
    repair_exit = main(
        [
            "corpus",
            "--manifest",
            str(P0_MANIFEST),
            "--case-id",
            "cylinder",
            "--repair",
            "--data-root",
            str(tmp_path / "repair-data"),
        ]
    )
    repair_payload = json.loads(capsys.readouterr().out)

    assert replacement.exists()
    assert default_exit == 0
    assert default_payload["run_status"] == "completed"
    assert repair_exit == 1
    assert repair_payload["cases"][0]["repair"]["status"] == "pass"


class _InterruptingHarness:
    def __init__(self, tmp_path: Path) -> None:
        self._tmp_path = tmp_path
        self._calls = 0

    def run(self, record_id: str, *, input_path: Path, timeout: int):
        self._calls += 1
        if self._calls == 2:
            raise RuntimeError("simulated interruption")
        signal_bundle = {
            "gates": [{"name": "script_exit_code", "status": "pass"}],
            "probes": {"input_summary": {"ok": True}},
        }
        revision = SimpleNamespace(
            revision_id="revision-1",
            signal_bundle=self._tmp_path / "signal_bundle.json",
        )
        return SimpleNamespace(status="pass", revision=revision, signal_bundle=signal_bundle)


class _ExternalForceStop(BaseException):
    pass


class _ExternallyStoppedHarness(_InterruptingHarness):
    def run(self, record_id: str, *, input_path: Path, timeout: int):
        self._calls += 1
        if self._calls == 2:
            raise _ExternalForceStop()
        self._calls -= 1
        return super().run(record_id, input_path=input_path, timeout=timeout)


class _TimeoutProcess:
    def __init__(self) -> None:
        self.started = False
        self.terminated = False
        self.join_timeouts: list[int | None] = []

    def start(self) -> None:
        self.started = True

    def join(self, timeout: int | None = None) -> None:
        self.join_timeouts.append(timeout)

    def is_alive(self) -> bool:
        return not self.terminated

    def terminate(self) -> None:
        self.terminated = True


class _TimeoutContext:
    def __init__(self, process: _TimeoutProcess) -> None:
        self._process = process

    def Queue(self):
        return SimpleNamespace()

    def Process(self, **_kwargs) -> _TimeoutProcess:
        return self._process


class _FailingHostedHarness:
    def __init__(self, tmp_path: Path) -> None:
        self.executor = WslBubblewrapExecutor()
        self._tmp_path = tmp_path

    def run(self, record_id: str, *, input_path: Path, timeout: int):
        signal_bundle = {
            "gates": [{"name": "script_exit_code", "status": "fail"}],
            "probes": {"input_summary": {"ok": True}},
            "execution": {"sandboxed": True},
        }
        revision = SimpleNamespace(
            revision_id="primary-failure",
            signal_bundle=self._tmp_path / "signal_bundle.json",
        )
        return SimpleNamespace(status="fail", revision=revision, signal_bundle=signal_bundle)


class _ProviderErrorCorpusRunner(CorpusRunner):
    def _run_provider_repair(self, **_kwargs) -> RepairLoopResult:
        return RepairLoopResult(
            status="provider_error",
            attempts=[],
            stop_reason="provider_request_timeout",
            error={"code": "provider_request_timeout", "message": "simulated timeout"},
            provider_requests=1,
        )
