from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from brep2code.agent.provider import DeepSeekProviderError, FakeLLMProvider
from brep2code.asymmetric_campaign import (
    AsymmetricCampaignError,
    frozen_contract,
    frozen_m179_contract,
    prepare,
    prepare_m179,
    run_fake_m179,
    validate_execute_admission,
    validate_m179_execute_admission,
    authorize_m179_execution,
    prepare_m182,
    run_fake_m182,
    validate_m182_execute_admission,
)


ROOT = Path(__file__).resolve().parents[1]


def _root(tmp_path: Path) -> Path:
    for relative in (
        "docs/corpus/knowledge",
        "docs/corpus/registry",
        "runtime_resources/experience-cards",
        "case-library/self-authored",
    ):
        shutil.copytree(ROOT / relative, tmp_path / relative)
    return tmp_path


def test_m176_prepare_binds_two_products_and_accounting(tmp_path: Path, monkeypatch) -> None:
    root = _root(tmp_path)
    monkeypatch.setattr("brep2code.asymmetric_campaign.shutil.which", lambda _name: "wsl.exe")

    payload = prepare(root)

    assert payload["completion_cap"] == 102
    assert payload["provider_request_cap"] == 69
    assert len(payload["main_case_ids"]) == 30
    assert [row["role"] for row in payload["annex"]] == ["final primitive", "single boolean-cut tool", "repeated boolean-cut tool"]
    assert validate_execute_admission(root)["provider_request_cap"] == 69


def test_m176_prepare_rejects_identity_reuse_and_admission_drift(tmp_path: Path, monkeypatch) -> None:
    root = _root(tmp_path)
    monkeypatch.setattr("brep2code.asymmetric_campaign.shutil.which", lambda _name: "wsl.exe")
    contract = frozen_contract(root)
    collision = root / contract["identities"]["main_report"]
    collision.parent.mkdir(parents=True, exist_ok=True)
    collision.write_text("{}", encoding="utf-8")
    with pytest.raises(AsymmetricCampaignError, match="not fresh"):
        prepare(root)

    collision.unlink()
    prepare(root)
    annex = root / contract["identities"]["annex_report"]
    payload = json.loads(annex.read_text(encoding="utf-8"))
    payload["requests_remaining"] = 12
    annex.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(AsymmetricCampaignError, match="fresh execute"):
        validate_execute_admission(root)


def test_m179_refreezes_identities_and_exercises_fake_only_adapter(tmp_path: Path, monkeypatch) -> None:
    root = _root(tmp_path)
    monkeypatch.setattr("brep2code.asymmetric_campaign.shutil.which", lambda _name: "wsl.exe")

    def fake_case(_root, _contract, provider, *, product, case_id, guidance_role, payload, report_path, allow_hosted):
        expected_requests = 3 if product == "feasibility_annex" else 2
        for _ in range(expected_requests):
            from brep2code.agent.provider import ProviderRequest
            from brep2code.asymmetric_campaign import _mark_request

            _mark_request(payload, report_path, allow_hosted=allow_hosted)
            provider.complete(ProviderRequest(model="fake-m180", messages=[], metadata={"case_id": case_id}))
        return {"case_id": case_id, "status": "pass", "stop_reason": "repair_pass", "provider_requests": expected_requests, "completion_slots_used": expected_requests + 1}

    monkeypatch.setattr("brep2code.asymmetric_campaign._run_case", fake_case)

    prepare_m179(root)
    assert validate_m179_execute_admission(root)["policy"] == "m179-asymmetric-hosted-campaign-v1"
    provider = FakeLLMProvider()
    outcome = run_fake_m179(root, provider)

    assert outcome["status"] == "completed_offline_fake"
    assert outcome["requests_used"] == 69
    assert outcome["completion_cap"] == 102
    assert len(provider.requests) == 69
    assert json.loads((root / frozen_m179_contract(root)["identities"]["annex_report"]).read_text(encoding="utf-8"))["completion_slots_used"] == 12
    assert json.loads((root / frozen_m179_contract(root)["identities"]["main_report"]).read_text(encoding="utf-8"))["completion_slots_used"] == 90
    with pytest.raises(AsymmetricCampaignError, match="fresh execute"):
        validate_m179_execute_admission(root)


def test_m179_authorization_requires_fresh_dual_admission(tmp_path: Path, monkeypatch) -> None:
    root = _root(tmp_path)
    monkeypatch.setattr("brep2code.asymmetric_campaign.shutil.which", lambda _name: "wsl.exe")
    prepare_m179(root)
    authorize_m179_execution(root)
    with pytest.raises(AsymmetricCampaignError, match="fresh execute"):
        validate_m179_execute_admission(root)
    report = root / frozen_m179_contract(root)["identities"]["annex_report"]
    assert json.loads(report.read_text(encoding="utf-8"))["provider_constructed"] is False


def test_m182_refreezes_identities_and_continues_after_provider_failure(tmp_path: Path, monkeypatch) -> None:
    root = _root(tmp_path)
    monkeypatch.setattr("brep2code.asymmetric_campaign.shutil.which", lambda _name: "wsl.exe")
    calls: list[str] = []

    def fake_case(_root, _contract, _provider, *, product, case_id, guidance_role, payload, report_path, allow_hosted):
        from brep2code.asymmetric_campaign import _mark_request

        calls.append(case_id)
        _mark_request(payload, report_path, allow_hosted=allow_hosted)
        if case_id == _contract["annex"][0]["case_id"]:
            raise DeepSeekProviderError("simulated provider lifecycle failure")
        expected_requests = 3 if product == "feasibility_annex" else 2
        for _ in range(expected_requests - 1):
            _mark_request(payload, report_path, allow_hosted=allow_hosted)
        return {"case_id": case_id, "status": "pass", "stop_reason": "initial_terminal", "provider_requests": expected_requests, "completion_slots_used": expected_requests + 1}

    monkeypatch.setattr("brep2code.asymmetric_campaign._run_case", fake_case)
    prepared = prepare_m182(root)
    assert prepared["policy"] == "m182-asymmetric-case-local-continuation-v1"
    assert validate_m182_execute_admission(root)["policy"] == prepared["policy"]

    outcome = run_fake_m182(root, FakeLLMProvider())

    assert len(calls) == 33
    assert outcome["status"] == "completed_offline_fake"
    assert outcome["cases"][0]["status"] == "provider_error"
    assert outcome["cases"][0]["stop_reason"] == "DeepSeekProviderError"
    assert outcome["requests_used"] == 67
