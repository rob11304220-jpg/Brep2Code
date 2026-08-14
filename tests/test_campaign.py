from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

import pytest

from brep2code.campaign import CampaignError, canonical_json, prepare_campaign, validate_execute_admission
from brep2code.cli import main


ROOT = Path(__file__).resolve().parents[1]
SPLIT = ROOT / "docs/corpus/sequence-paired/repeated-feature-pattern-v1-preregistration.json"
CASE_ID = "param_repeated_feature_pattern_centered_low"


def _spec() -> dict:
    case = json.loads((ROOT / "case-library/self-authored" / CASE_ID / "case.json").read_text(encoding="utf-8"))
    return {
        "schema_version": 1,
        "campaign_id": "m139-test-development-r1",
        "case": {
            "case_id": CASE_ID,
            "input_sha256": case["sha256"],
            "data_split": "development",
            "split_authority": "docs/corpus/sequence-paired/repeated-feature-pattern-v1-preregistration.json",
            "split_authority_sha256": sha256(SPLIT.read_bytes()).hexdigest(),
        },
        "q01": {
            "transcript": {
                "schema_version": 1,
                "policy": "m139-test",
                "condition_id": CASE_ID,
                "family": "repeated_feature_pattern",
                "data_split": "development",
                "facts": {"base_length_x": 48.0, "hole_radius": 2.0},
            }
        },
        "reference": {"mode": "none"},
        "generation": {"first_pass": True, "repair_policy": "none", "max_repair_rounds": 0},
        "execution": {
            "provider": "deepseek",
            "model": "deepseek-v4-pro",
            "executor": "wsl-bwrap",
            "provider_deadline_seconds": 120,
            "max_output_tokens": 4096,
            "max_requests": 1,
        },
    }


def test_prepare_campaign_binds_spec_and_creates_monitor(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr("brep2code.campaign.shutil.which", lambda _name: "wsl.exe")
    spec = _spec()
    spec_path = tmp_path / "campaign.json"
    spec_path.write_text(json.dumps(spec), encoding="utf-8")
    report = tmp_path / "report.json"
    monitor = tmp_path / "monitor.json"

    payload = prepare_campaign(spec_path, report, monitor, root=ROOT)

    assert payload["request_state"] == "prepared"
    assert payload["campaign_spec_sha256"] == sha256(canonical_json(spec).encode("utf-8")).hexdigest()
    assert payload["campaign_contract"]["authorization"] == "not_authorized"
    assert payload["campaign_contract"]["provider_constructed"] is False
    assert json.loads(monitor.read_text(encoding="utf-8"))["monitor_status"] == "monitoring"
    validate_execute_admission(payload, spec_path, monitor, root=ROOT)
    payload["campaign_contract"]["max_output_tokens"] = 1
    with pytest.raises(CampaignError, match="fresh execute"):
        validate_execute_admission(payload, spec_path, monitor, root=ROOT)


def test_prepare_campaign_rejects_transcript_path_and_reused_path(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr("brep2code.campaign.shutil.which", lambda _name: "wsl.exe")
    spec = _spec()
    spec["q01"]["transcript"]["facts"]["path"] = "case-library/self-authored/input.step"
    spec_path = tmp_path / "campaign.json"
    spec_path.write_text(json.dumps(spec), encoding="utf-8")
    with pytest.raises(CampaignError, match="egress"):
        prepare_campaign(spec_path, tmp_path / "report.json", tmp_path / "monitor.json", root=ROOT)

    spec = _spec()
    spec_path.write_text(json.dumps(spec), encoding="utf-8")
    report = tmp_path / "report.json"
    monitor = tmp_path / "monitor.json"
    report.write_text("{}", encoding="utf-8")
    with pytest.raises(CampaignError, match="fresh"):
        prepare_campaign(spec_path, report, monitor, root=ROOT)


def test_campaign_prepare_cli_is_local_configuration_boundary(tmp_path: Path, monkeypatch, capsys) -> None:
    monkeypatch.setattr("brep2code.campaign.shutil.which", lambda _name: "wsl.exe")
    spec_path = tmp_path / "campaign.json"
    spec_path.write_text(json.dumps(_spec()), encoding="utf-8")

    assert main(["campaign-prepare", "--spec", str(spec_path), "--report", str(tmp_path / "report.json"), "--monitor-state", str(tmp_path / "monitor.json")]) == 0
    assert '"status": "prepared_offline"' in capsys.readouterr().out
