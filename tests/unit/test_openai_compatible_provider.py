from __future__ import annotations

import json
from urllib import error

import pytest

from brep2code.providers import (
    ActionRequest,
    OpenAICompatibleConfig,
    OpenAICompatibleProvider,
    ProviderBudgetError,
    ProviderConfigurationError,
    ProviderError,
    ProviderLimits,
    ProviderRequest,
    deepseek_config_from_env,
)


class FakeHTTPResponse:
    def __init__(self, payload: dict) -> None:
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *args) -> None:
        return None

    def read(self, unused_amount: int | None = None) -> bytes:
        return json.dumps(self.payload).encode("utf-8")


def test_openai_compatible_contract_and_usage_accounting() -> None:
    observed = {}

    def opener(http_request, *, timeout):
        observed["url"] = http_request.full_url
        observed["authorization"] = http_request.headers["Authorization"]
        observed["timeout"] = timeout
        observed["body"] = json.loads(http_request.data)
        return FakeHTTPResponse(_response(prompt=100, completion=50))

    provider = OpenAICompatibleProvider(_config(), _limits(), opener=opener)
    response = provider.generate(_request())

    assert response.script == "print('ok')"
    assert response.usage["total_tokens"] == 150
    assert observed["url"] == "https://provider.invalid/v1/chat/completions"
    assert observed["authorization"] == "Bearer top-secret"
    assert observed["timeout"] == 3
    assert observed["body"]["max_tokens"] == 200
    assert observed["body"]["thinking"] == {"type": "disabled"}
    messages = observed["body"]["messages"]
    assert "installed OCP" in messages[0]["content"]
    assert "do not import cadquery" in messages[0]["content"]
    assert "shortest correct construction" in messages[0]["content"]
    assert "Do not manually assemble or sew faces and shells" in messages[0]["content"]
    assert "normally under 120 lines" in messages[0]["content"]
    assert "every import at module scope" in messages[0]["content"]
    assert "TopExp.FirstVertex_s" in messages[0]["content"]
    assert "output.step" in messages[0]["content"]
    task = json.loads(messages[1]["content"])
    assert task["observations"] == {"summary": "box"}
    assert task["acceptance"] == {"output": "output.step"}
    assert task["round_index"] == 0
    assert provider.requests_issued == 1
    assert provider.total_tokens == 150
    assert provider.cost_usd == pytest.approx(0.0002)


def test_openai_compatible_active_action_contract_and_prompt() -> None:
    observed = {}
    payload = _response(prompt=20, completion=10)
    payload["choices"][0]["message"]["content"] = json.dumps(
        {"action": "probe", "probe": {"tool": "edge_candidates", "arguments": {}}}
    )

    def opener(http_request, *, timeout):
        observed["body"] = json.loads(http_request.data)
        return FakeHTTPResponse(payload)

    provider = OpenAICompatibleProvider(_config(), _limits(), opener=opener)
    response = provider.choose_action(
        ActionRequest(
            case_id="filleted_box",
            turn_index=0,
            session={
                "case_id": "filleted_box",
                "unit": "mm",
                "initial_observations": {"topology": {"edge": 30}},
                "available_tools": ["edge_candidates", "ocp_symbol"],
                "budgets": {"probes": {"remaining": 1}},
                "current_revision": None,
            },
        )
    )

    assert response.action["action"] == "probe"
    assert response.usage["total_tokens"] == 30
    messages = observed["body"]["messages"]
    assert "probe" in messages[0]["content"]
    assert "The Harness, not the model, decides success" in messages[0]["content"]
    assert "Never resubmit an unchanged failed revision" in messages[0]["content"]
    task = json.loads(messages[1]["content"])
    assert task["turn_index"] == 0
    assert task["initial_observations"]["topology"] == {"edge": 30}
    assert "host" not in messages[1]["content"].lower()
    assert provider.total_tokens == 30


def test_provider_exchange_records_bounded_payloads_without_credentials() -> None:
    events = []
    provider = OpenAICompatibleProvider(
        _config(),
        _limits(),
        opener=lambda *args, **kwargs: FakeHTTPResponse(_response()),
        exchange_recorder=lambda event, attempt, payload: events.append(
            (event, attempt, payload)
        ),
    )

    provider.generate(_request())

    assert [event for event, _, _ in events] == ["request", "response"]
    request_artifact = events[0][2]
    response_artifact = events[1][2]
    serialized = json.dumps(events)
    assert request_artifact["endpoint"] == "/chat/completions"
    assert request_artifact["body"]["model"] == "model"
    assert response_artifact["model"] == "model"
    assert response_artifact["usage"]["total_tokens"] == 15
    assert "Authorization" not in serialized
    assert "top-secret" not in serialized


def test_active_action_malformed_content_is_redacted_and_accounted() -> None:
    malformed = _response()
    malformed["choices"][0]["message"]["content"] = "not-json private-action"
    provider = OpenAICompatibleProvider(
        _config(), _limits(), opener=lambda *args, **kwargs: FakeHTTPResponse(malformed)
    )

    with pytest.raises(ProviderError, match="content_not_json") as exc_info:
        provider.choose_action(ActionRequest("box", 0, {"case_id": "box"}))

    assert "private-action" not in str(exc_info.value)
    assert provider.total_tokens == 15
    assert provider.cost_usd == pytest.approx(0.00002)
    assert provider.accounting_snapshot()["tokens"] == {
        "prompt": 10,
        "completion": 5,
        "total": 15,
    }


def test_active_action_model_drift_is_rejected_and_accounted() -> None:
    drifted = _response()
    drifted["model"] = "other-model"
    provider = OpenAICompatibleProvider(
        _config(), _limits(), opener=lambda *args, **kwargs: FakeHTTPResponse(drifted)
    )

    with pytest.raises(ProviderError, match="model_identity_drift"):
        provider.choose_action(ActionRequest("box", 0, {"case_id": "box"}))
    assert provider.total_tokens == 15


def test_provider_accounting_checkpoints_in_flight_and_restores_conservatively() -> None:
    snapshots = []
    provider = OpenAICompatibleProvider(
        _config(), _limits(), opener=lambda *args, **kwargs: FakeHTTPResponse(_response())
    )
    provider.set_accounting_checkpoint(snapshots.append)
    provider.generate(_request())

    assert snapshots[0]["http_attempts"] == 1
    assert snapshots[0]["in_flight_requests"] == 1
    assert snapshots[-1]["in_flight_requests"] == 0
    restored = OpenAICompatibleProvider(
        _config(), _limits(), opener=lambda *args, **kwargs: FakeHTTPResponse(_response())
    )
    interrupted = dict(snapshots[0])
    restored.restore_accounting(interrupted)
    assert restored.requests_issued == 1
    assert restored.in_flight_requests == 0


def test_retry_is_bounded_and_each_attempt_consumes_request_budget() -> None:
    calls = 0

    def opener(http_request, *, timeout):
        nonlocal calls
        calls += 1
        if calls == 1:
            raise error.URLError("temporary")
        return FakeHTTPResponse(_response())

    provider = OpenAICompatibleProvider(_config(), _limits(max_retries=1), opener=opener)
    assert provider.generate(_request()).script == "print('ok')"
    assert calls == 2
    assert provider.requests_issued == 2


def test_repair_request_includes_feedback_and_previous_complete_script() -> None:
    observed = {}

    def opener(http_request, *, timeout):
        observed["body"] = json.loads(http_request.data)
        return FakeHTTPResponse(_response())

    provider = OpenAICompatibleProvider(_config(), _limits(), opener=opener)
    provider.generate(
        ProviderRequest(
            case_id="box",
            round_index=1,
            context={"summary": "box"},
            feedback={"stage": "execution", "stderr": "NameError"},
            previous_script="raise NameError()\n",
        )
    )

    task = json.loads(observed["body"]["messages"][1]["content"])
    assert task["feedback"] == {"stage": "execution", "stderr": "NameError"}
    assert task["previous_script"] == "raise NameError()\n"


def test_token_budget_rejects_response_after_committing_actual_usage() -> None:
    calls = 0

    def opener(*args, **kwargs):
        nonlocal calls
        calls += 1
        return FakeHTTPResponse(_response())

    provider = OpenAICompatibleProvider(
        _config(), _limits(max_total_tokens=10), opener=opener
    )
    with pytest.raises(ProviderBudgetError, match="token budget"):
        provider.generate(_request())
    assert provider.total_tokens == 15
    assert provider.cost_usd == pytest.approx(0.00002)
    assert calls == 1
    with pytest.raises(ProviderBudgetError, match="token budget"):
        provider.generate(_request())
    assert calls == 1


def test_response_at_exact_token_ceiling_succeeds_then_blocks_next_request() -> None:
    calls = 0

    def opener(*args, **kwargs):
        nonlocal calls
        calls += 1
        return FakeHTTPResponse(_response())

    provider = OpenAICompatibleProvider(
        _config(), _limits(max_total_tokens=15), opener=opener
    )

    assert provider.generate(_request()).usage["total_tokens"] == 15
    with pytest.raises(ProviderBudgetError, match="token budget"):
        provider.generate(_request())
    assert calls == 1


def test_cost_budget_rejects_response() -> None:
    provider = OpenAICompatibleProvider(
        _config(),
        _limits(max_cost_usd=0.00001),
        opener=lambda *args, **kwargs: FakeHTTPResponse(_response(prompt=100, completion=50)),
    )
    with pytest.raises(ProviderBudgetError, match="cost budget"):
        provider.generate(_request())
    assert provider.total_tokens == 150
    assert provider.cost_usd == pytest.approx(0.0002)


def test_malformed_json_contract_is_bounded_and_redacted() -> None:
    malformed = _response()
    malformed["choices"][0]["message"]["content"] = "not-json top-secret"
    provider = OpenAICompatibleProvider(
        _config(), _limits(), opener=lambda *args, **kwargs: FakeHTTPResponse(malformed)
    )

    with pytest.raises(ProviderError, match="content_not_json") as exc_info:
        provider.generate(_request())

    assert "top-secret" not in str(exc_info.value)
    assert provider.requests_issued == 1
    assert provider.total_tokens == 15
    assert provider.cost_usd == pytest.approx(0.00002)


def test_empty_content_records_safe_reasoning_shape_and_usage() -> None:
    malformed = _response(prompt=100, completion=4096)
    malformed["choices"][0]["message"] = {
        "content": "",
        "reasoning_content": "private-reasoning " * 40,
    }
    provider = OpenAICompatibleProvider(
        _config(), _limits(max_total_tokens=5000),
        opener=lambda *args, **kwargs: FakeHTTPResponse(malformed),
    )

    with pytest.raises(
        ProviderError, match="content_not_json_empty_short_reasoning_medium"
    ) as exc_info:
        provider.generate(_request())

    assert "private-reasoning" not in str(exc_info.value)
    assert provider.total_tokens == 4196
    assert provider.cost_usd == pytest.approx(0.008292)


def test_invalid_choices_still_commit_valid_provider_usage() -> None:
    malformed = _response()
    malformed["choices"] = []
    provider = OpenAICompatibleProvider(
        _config(), _limits(), opener=lambda *args, **kwargs: FakeHTTPResponse(malformed)
    )

    with pytest.raises(ProviderError, match="choices_missing_or_empty"):
        provider.generate(_request())

    assert provider.total_tokens == 15
    assert provider.cost_usd == pytest.approx(0.00002)


def test_fenced_json_contract_is_normalized() -> None:
    response = _response()
    response["choices"][0]["message"]["content"] = (
        "```JSON\n" + json.dumps({"script": "print('fenced')"}) + "\n```"
    )
    provider = OpenAICompatibleProvider(
        _config(), _limits(), opener=lambda *args, **kwargs: FakeHTTPResponse(response)
    )

    result = provider.generate(_request())

    assert result.script == "print('fenced')"
    assert provider.requests_issued == 1
    assert provider.total_tokens == 15


def test_fenced_python_script_is_normalized() -> None:
    response = _response()
    response["choices"][0]["message"]["content"] = "```python\nprint('fenced')\n```"
    provider = OpenAICompatibleProvider(
        _config(), _limits(), opener=lambda *args, **kwargs: FakeHTTPResponse(response)
    )

    result = provider.generate(_request())

    assert result.script == "print('fenced')"
    assert provider.requests_issued == 1
    assert provider.total_tokens == 15


def test_bounded_explanatory_text_around_single_fenced_script_is_normalized() -> None:
    response = _response()
    response["choices"][0]["message"]["content"] = (
        "Here is the script:\n```python\nprint('fenced')\n```\nThis writes output.step."
    )
    provider = OpenAICompatibleProvider(
        _config(), _limits(), opener=lambda *args, **kwargs: FakeHTTPResponse(response)
    )

    result = provider.generate(_request())

    assert result.script == "print('fenced')"
    assert provider.total_tokens == 15


def test_bounded_explanatory_text_around_single_fenced_json_is_normalized() -> None:
    response = _response()
    response["choices"][0]["message"]["content"] = (
        "Requested JSON follows:\n```json\n"
        + json.dumps({"script": "print('fenced-json')"})
        + "\n```"
    )
    provider = OpenAICompatibleProvider(
        _config(), _limits(), opener=lambda *args, **kwargs: FakeHTTPResponse(response)
    )

    result = provider.generate(_request())

    assert result.script == "print('fenced-json')"


@pytest.mark.parametrize(
    ("content", "diagnostic"),
    [
        ("not-json top-secret", "content_not_json_plain_text_short"),
        ("```python\nprint('one')\n```\n```python\nprint('two')\n```", "multiple_fences"),
        ("```python\nprint('unterminated')", "unterminated_fence"),
    ],
)
def test_invalid_content_reports_only_safe_shape_diagnostics(
    content: str, diagnostic: str
) -> None:
    response = _response()
    response["choices"][0]["message"]["content"] = content
    provider = OpenAICompatibleProvider(
        _config(), _limits(), opener=lambda *args, **kwargs: FakeHTTPResponse(response)
    )

    with pytest.raises(ProviderError, match=diagnostic) as exc_info:
        provider.generate(_request())

    assert "top-secret" not in str(exc_info.value)
    assert "print" not in str(exc_info.value)
    assert provider.total_tokens == 15
    assert provider.cost_usd == pytest.approx(0.00002)


def test_extra_content_fields_remain_invalid() -> None:
    response = _response()
    response["choices"][0]["message"]["content"] = json.dumps(
        {"script": "print('ok')", "note": "not allowed"}
    )
    provider = OpenAICompatibleProvider(
        _config(), _limits(), opener=lambda *args, **kwargs: FakeHTTPResponse(response)
    )

    with pytest.raises(ProviderError, match="content_fields_invalid"):
        provider.generate(_request())

    assert provider.total_tokens == 15
    assert provider.cost_usd == pytest.approx(0.00002)


def test_missing_script_reports_safe_contract_reason() -> None:
    malformed = _response()
    malformed["choices"][0]["message"]["content"] = json.dumps({"reason": "top-secret"})
    provider = OpenAICompatibleProvider(
        _config(), _limits(), opener=lambda *args, **kwargs: FakeHTTPResponse(malformed)
    )

    with pytest.raises(ProviderError, match="script_missing_or_empty") as exc_info:
        provider.generate(_request())

    assert "top-secret" not in str(exc_info.value)
    assert provider.total_tokens == 15
    assert provider.cost_usd == pytest.approx(0.00002)


def test_invalid_usage_reports_safe_contract_reason() -> None:
    malformed = _response()
    malformed["usage"]["total_tokens"] = "not-a-number"
    provider = OpenAICompatibleProvider(
        _config(), _limits(), opener=lambda *args, **kwargs: FakeHTTPResponse(malformed)
    )

    with pytest.raises(ProviderError, match="usage_fields_invalid"):
        provider.generate(_request())


def test_inconsistent_usage_totals_are_rejected_without_token_commit() -> None:
    malformed = _response()
    malformed["usage"]["total_tokens"] = 16
    provider = OpenAICompatibleProvider(
        _config(), _limits(), opener=lambda *args, **kwargs: FakeHTTPResponse(malformed)
    )

    with pytest.raises(ProviderError, match="usage_fields_invalid"):
        provider.generate(_request())
    assert provider.total_tokens == 0

    assert provider.total_tokens == 0
    assert provider.cost_usd == 0.0


def test_deepseek_configuration_requires_environment_key_and_model() -> None:
    with pytest.raises(ProviderConfigurationError, match="required"):
        deepseek_config_from_env({})
    config = deepseek_config_from_env(
        {"DEEPSEEK_API_KEY": "secret-value", "DEEPSEEK_MODEL": "deepseek-chat"},
        thinking_mode="disabled",
    )
    assert config.model == "deepseek-chat"
    assert config.thinking_mode == "disabled"
    assert "secret-value" not in repr(config)


def test_provider_configuration_rejects_unknown_thinking_mode() -> None:
    with pytest.raises(ProviderConfigurationError, match="thinking mode"):
        OpenAICompatibleConfig(
            provider="test",
            base_url="https://provider.invalid",
            api_key="top-secret",
            model="model",
            thinking_mode="automatic",
        )


def test_deepseek_configuration_reads_ignored_file_with_environment_override(
    tmp_path, monkeypatch
) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "DEEPSEEK_API_KEY=file-secret\n"
        "DEEPSEEK_MODEL=deepseek-v4-pro\n"
        "DEEPSEEK_BASE_URL=https://api.deepseek.com\n",
        encoding="utf-8",
    )
    config = deepseek_config_from_env(
        {"DEEPSEEK_MODEL": "environment-model"}, env_file=env_file
    )
    assert config.model == "environment-model"
    assert config.base_url == "https://api.deepseek.com"
    assert "file-secret" not in repr(config)


def _config() -> OpenAICompatibleConfig:
    return OpenAICompatibleConfig(
        provider="test",
        base_url="https://provider.invalid/v1",
        api_key="top-secret",
        model="model",
        thinking_mode="disabled",
    )


def _limits(**overrides) -> ProviderLimits:
    values = {
        "max_requests": 3,
        "timeout_seconds": 3,
        "max_retries": 0,
        "max_output_tokens": 200,
        "max_total_tokens": 1000,
        "max_cost_usd": 1.0,
        "input_cost_per_million": 1.0,
        "output_cost_per_million": 2.0,
    }
    values.update(overrides)
    return ProviderLimits(**values)


def _request() -> ProviderRequest:
    return ProviderRequest(case_id="box", round_index=0, context={"summary": "box"})


def _response(*, prompt: int = 10, completion: int = 5) -> dict:
    return {
        "model": "model",
        "choices": [{"message": {"content": json.dumps({"script": "print('ok')"})}}],
        "usage": {
            "prompt_tokens": prompt,
            "completion_tokens": completion,
            "total_tokens": prompt + completion,
        },
    }
