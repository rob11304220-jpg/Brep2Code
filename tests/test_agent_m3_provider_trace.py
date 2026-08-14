from __future__ import annotations

import json
from pathlib import Path

from brep2code.agent.provider import (
    DeepSeekConfigurationError,
    DeepSeekProvider,
    DeepSeekProviderError,
    FakeLLMProvider,
    LLMMessage,
    ProviderRequest,
    _deepseek_payload,
    _deepseek_response,
    fake_edit_response,
    fake_replacement_response,
)
from brep2code.agent.trace import append_llm_messages, write_provider_response_trace
from brep2code.storage import RecordStore


def test_fake_provider_returns_full_script_replacement() -> None:
    script = "from pathlib import Path\nPath('output/model.step').write_text('step')\n"
    provider = FakeLLMProvider([fake_replacement_response(script)])
    request = ProviderRequest(
        model="fake-repair",
        messages=[LLMMessage(role="user", content="fix missing output")],
    )

    response = provider.complete(request)

    assert provider.requests == [request]
    assert response.script_update is not None
    assert response.script_update.kind == "replace"
    assert response.script_update.path == "build_sequence.py"
    assert response.script_update.content == script


def test_fake_provider_returns_script_edit_instructions() -> None:
    provider = FakeLLMProvider([fake_edit_response("Change the export path to output/model.step.")])

    response = provider.complete(
        ProviderRequest(
            model="fake-repair",
            messages=[LLMMessage(role="user", content="repair the export path")],
        )
    )

    assert response.script_update is not None
    assert response.script_update.kind == "edit"
    assert response.script_update.instructions == "Change the export path to output/model.step."


def test_deepseek_payload_is_non_streaming_json_only_without_provider_construction() -> None:
    request = ProviderRequest(
        model="deepseek-v4-pro",
        temperature=0.2,
        messages=[LLMMessage(role="user", content="offline compatibility fixture")],
    )

    payload = _deepseek_payload(request)

    assert payload == {
        "model": "deepseek-v4-pro",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Return a json object with output_text and script_update. script_update must be "
                    "{\"kind\": \"replace\", \"content\": \"full build_sequence.py source\"}. "
                    "Use the installed cadquery-ocp bindings: import from OCP (for example OCP.BRepPrimAPI, "
                    "OCP.STEPControl, and OCP.IFSelect), never OCC.Core. Create or transform the CAD shape and export "
                    "a valid STEP to output/model.step. Match the input probe bbox, volume, and topology gates from the "
                    "repair context. Do not hand-author raw STEP text. Return only json; do not use markdown fences."
                ),
            },
            {"role": "user", "content": "offline compatibility fixture"},
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.2,
    }
    assert "stream" not in payload


def test_deepseek_payload_rejects_unenforceable_character_output_cap() -> None:
    request = ProviderRequest(
        model="deepseek-v4-pro",
        messages=[LLMMessage(role="user", content="offline compatibility fixture")],
        max_output_chars=2000,
    )

    try:
        _deepseek_payload(request)
    except DeepSeekProviderError as exc:
        assert str(exc) == "DeepSeek adapter does not support max_output_chars"
    else:
        raise AssertionError("expected an unsupported bounded-output error")


def test_deepseek_payload_maps_explicit_positive_token_cap() -> None:
    payload = _deepseek_payload(
        ProviderRequest(
            model="deepseek-v4-pro",
            messages=[LLMMessage(role="user", content="offline compatibility fixture")],
            max_output_tokens=4096,
        )
    )

    assert payload["max_tokens"] == 4096


def test_deepseek_payload_rejects_nonpositive_token_cap() -> None:
    try:
        _deepseek_payload(
            ProviderRequest(
                model="deepseek-v4-pro",
                messages=[LLMMessage(role="user", content="offline compatibility fixture")],
                max_output_tokens=0,
            )
        )
    except DeepSeekProviderError as exc:
        assert str(exc) == "max_output_tokens must be a positive integer"
    else:
        raise AssertionError("expected an invalid token cap error")


def test_deepseek_response_accepts_only_json_replace_envelope_and_safe_summary() -> None:
    response = _deepseek_response(
        {
            "id": "chatcmpl-local-fixture",
            "created": 123,
            "model": "deepseek-v4-pro",
            "untrusted_header_value": "must-not-be-retained",
            "choices": [
                {
                    "finish_reason": "stop",
                    "message": {
                        "content": json.dumps(
                            {
                                "output_text": "replacement ready",
                                "script_update": {"kind": "replace", "content": "print('ok')\n"},
                            }
                        )
                    },
                }
            ],
        },
        requested_model="deepseek-v4-pro",
    )

    assert response.script_update is not None
    assert response.script_update.content == "print('ok')\n"
    assert response.raw_summary == {"id": "chatcmpl-local-fixture", "created": 123, "model": "deepseek-v4-pro"}


def test_trace_writers_append_messages_and_sanitize_provider_response(tmp_path: Path) -> None:
    store = RecordStore(tmp_path / "data")
    record = store.ensure_record("trace-smoke")
    revision = store.create_revision(record)
    trace_dir = revision.traces
    append_llm_messages(
        trace_dir,
        [
            LLMMessage(
                role="user",
                content="x" * 20,
                metadata={"api_key": "sk-test", "safe": "kept"},
            )
        ],
        direction="request",
        limit_chars=8,
    )
    append_llm_messages(
        trace_dir,
        [LLMMessage(role="assistant", content="fixed")],
        direction="response",
        limit_chars=8,
    )
    response_path = write_provider_response_trace(
        trace_dir,
        fake_replacement_response("print('ok')"),
        limit_chars=8,
    )

    message_lines = (trace_dir / "llm_messages.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(message_lines) == 2
    first = json.loads(message_lines[0])
    assert first["direction"] == "request"
    assert first["message"]["content"] == "xxxxxxxx\n...[truncated]"
    assert first["message"]["metadata"]["api_key"] == "[redacted]"
    assert first["message"]["metadata"]["safe"] == "kept"

    provider_trace = json.loads(response_path.read_text(encoding="utf-8"))
    assert provider_trace["response"]["provider"] == "fake"
    assert provider_trace["response"]["script_update"]["kind"] == "replace"


def test_deepseek_provider_loads_ignored_env_file_and_parses_script_replacement(
    tmp_path: Path, monkeypatch
) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "DEEPSEEK_API_KEY=local-test-key\nDEEPSEEK_MODEL=deepseek-v4-pro\n",
        encoding="utf-8",
    )
    observed = {}

    class Response:
        headers: dict[str, str] = {}

        def __init__(self) -> None:
            self._body = json.dumps(
                {
                    "id": "chatcmpl-test",
                    "model": "deepseek-v4-pro",
                    "usage": {"prompt_tokens": 12, "completion_tokens": 8},
                    "choices": [
                        {
                            "finish_reason": "stop",
                            "message": {
                                "content": json.dumps(
                                    {
                                        "output_text": "replacement ready",
                                        "script_update": {"kind": "replace", "content": "print('ok')\n"},
                                    }
                                )
                            },
                        }
                    ],
                }
            ).encode("utf-8")

        def read(self, amount: int | None = None) -> bytes:
            if amount is None:
                amount = len(self._body)
            result, self._body = self._body[:amount], self._body[amount:]
            return result

        def __enter__(self):
            return self

        def __exit__(self, *_args) -> None:
            return None

    def fake_urlopen(http_request, *, timeout: int):
        observed["url"] = http_request.full_url
        observed["payload"] = json.loads(http_request.data.decode("utf-8"))
        observed["timeout"] = timeout
        return Response()

    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    monkeypatch.delenv("DEEPSEEK_MODEL", raising=False)
    monkeypatch.setattr("brep2code.agent.provider.urlrequest.urlopen", fake_urlopen)
    provider = DeepSeekProvider.from_env_file(env_file)

    first_response_bytes: list[int] = []
    response = provider.complete(
        ProviderRequest(model=provider.model, messages=[LLMMessage(role="user", content="fix")]),
        on_first_response_byte=first_response_bytes.append,
    )

    assert observed["url"] == "https://api.deepseek.com/chat/completions"
    assert observed["payload"]["model"] == "deepseek-v4-pro"
    assert observed["payload"]["response_format"] == {"type": "json_object"}
    assert "never OCC.Core" in observed["payload"]["messages"][0]["content"]
    assert response.script_update is not None
    assert response.script_update.content == "print('ok')\n"
    assert response.usage == {"prompt_tokens": 12, "completion_tokens": 8}
    assert response.raw_summary["provider_request_id_present"] is False
    assert isinstance(response.raw_summary["first_response_byte_elapsed_ms"], int)
    assert len(first_response_bytes) == 1


def test_deepseek_provider_requires_an_api_key(tmp_path: Path, monkeypatch) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text("DEEPSEEK_MODEL=deepseek-v4-flash\n", encoding="utf-8")
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)

    try:
        DeepSeekProvider.from_env_file(env_file)
    except DeepSeekConfigurationError as exc:
        assert "DEEPSEEK_API_KEY" in str(exc)
    else:
        raise AssertionError("expected missing credential configuration error")
