"""Minimal LLM provider contract for repair loop experiments."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
import json
import os
from pathlib import Path
from time import perf_counter
from typing import Callable, Literal, Protocol
from urllib import error, request as urlrequest


MessageRole = Literal["system", "user", "assistant", "tool"]
ScriptUpdateKind = Literal["replace", "edit"]


@dataclass(frozen=True)
class LLMMessage:
    role: MessageRole
    content: str
    name: str | None = None
    metadata: dict | None = None


@dataclass(frozen=True)
class ScriptUpdate:
    """A provider's requested change to the build script."""

    kind: ScriptUpdateKind
    path: str = "build_sequence.py"
    content: str | None = None
    instructions: str | None = None


@dataclass(frozen=True)
class ToolCall:
    """A provider-neutral request for one Harness-owned tool."""

    tool: str
    arguments: dict


@dataclass(frozen=True)
class ProviderRequest:
    messages: list[LLMMessage]
    model: str
    temperature: float | None = None
    max_output_chars: int | None = None
    max_output_tokens: int | None = None
    metadata: dict = field(default_factory=dict)


@dataclass(frozen=True)
class ProviderResponse:
    provider: str
    model: str
    output_text: str
    finish_reason: str = "stop"
    script_update: ScriptUpdate | None = None
    tool_call: ToolCall | None = None
    usage: dict = field(default_factory=dict)
    raw_summary: dict = field(default_factory=dict)


class LLMProvider(Protocol):
    """Provider boundary used by the future repair loop."""

    name: str

    def complete(self, request: ProviderRequest) -> ProviderResponse:
        """Return one provider response without executing tools or scripts."""


class DeepSeekProviderError(RuntimeError):
    """Base error for a hosted DeepSeek provider request."""


class DeepSeekConfigurationError(DeepSeekProviderError):
    """Raised when local DeepSeek configuration is missing or invalid."""


class DeepSeekProvider:
    """DeepSeek V4 provider using its OpenAI-compatible Chat Completions API."""

    name = "deepseek"

    def __init__(
        self,
        *,
        api_key: str,
        model: str = "deepseek-v4-pro",
        base_url: str = "https://api.deepseek.com",
        timeout_seconds: int = 120,
    ) -> None:
        if not api_key.strip():
            raise DeepSeekConfigurationError("DEEPSEEK_API_KEY is required; set it in .env or the environment")
        if not model.startswith("deepseek-v4-"):
            raise DeepSeekConfigurationError("DEEPSEEK_MODEL must name a DeepSeek V4 model")
        self.api_key = api_key
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    @classmethod
    def from_env_file(cls, path: Path | None = None) -> "DeepSeekProvider":
        values = _read_env_file(path) if path is not None and path.exists() else {}
        return cls(
            api_key=os.environ.get("DEEPSEEK_API_KEY") or values.get("DEEPSEEK_API_KEY", ""),
            model=os.environ.get("DEEPSEEK_MODEL") or values.get("DEEPSEEK_MODEL", "deepseek-v4-pro"),
            base_url=os.environ.get("DEEPSEEK_BASE_URL")
            or values.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
        )

    def complete(
        self,
        provider_request: ProviderRequest,
        *,
        on_first_response_byte: Callable[[int], None] | None = None,
    ) -> ProviderResponse:
        payload = _deepseek_payload(provider_request, default_model=self.model)
        http_request = urlrequest.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        try:
            request_started = perf_counter()
            with urlrequest.urlopen(http_request, timeout=self.timeout_seconds) as response:
                status = int(getattr(response, "status", 200))
                request_id_present = any(
                    response.headers.get(name) is not None
                    for name in ("x-request-id", "request-id", "x-openai-request-id")
                )
                first_byte = response.read(1)
                first_response_byte_elapsed_ms = int((perf_counter() - request_started) * 1000)
                if first_byte and on_first_response_byte is not None:
                    on_first_response_byte(first_response_byte_elapsed_ms)
                data = json.loads((first_byte + response.read()).decode("utf-8"))
        except error.HTTPError as exc:
            raise DeepSeekProviderError(f"DeepSeek request failed with HTTP {exc.code}") from exc
        except (error.URLError, TimeoutError) as exc:
            raise DeepSeekProviderError("DeepSeek request could not reach the configured API endpoint") from exc
        except json.JSONDecodeError as exc:
            raise DeepSeekProviderError("DeepSeek returned invalid JSON") from exc
        parsed = _deepseek_response(data, requested_model=payload["model"])
        return replace(
            parsed,
            raw_summary={
                **parsed.raw_summary,
                "http_status_class": f"{status // 100}xx",
                "provider_request_id_present": request_id_present,
                "first_response_byte_elapsed_ms": first_response_byte_elapsed_ms,
            },
        )


def _read_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def _deepseek_messages(messages: list[LLMMessage]) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    for message in messages:
        item = {"role": message.role if message.role != "tool" else "user", "content": message.content}
        if message.name:
            item["name"] = message.name
        result.append(item)
    return result


def _deepseek_payload(provider_request: ProviderRequest, *, default_model: str | None = None) -> dict:
    """Build the current non-streaming JSON request without provider state.

    ``max_output_chars`` is a local character contract, not an API transport
    option. Reject it so a caller never assumes an unenforced remote cap.
    ``max_output_tokens`` is an explicit provider-token limit and maps directly
    to DeepSeek's ``max_tokens`` request field.
    """

    if provider_request.max_output_chars is not None:
        raise DeepSeekProviderError("DeepSeek adapter does not support max_output_chars")
    if provider_request.max_output_tokens is not None and (
        not isinstance(provider_request.max_output_tokens, int)
        or isinstance(provider_request.max_output_tokens, bool)
        or provider_request.max_output_tokens < 1
    ):
        raise DeepSeekProviderError("max_output_tokens must be a positive integer")
    payload: dict = {
        "model": provider_request.model or default_model,
        "messages": [_json_response_instruction(provider_request), *_deepseek_messages(provider_request.messages)],
        "response_format": {"type": "json_object"},
    }
    if provider_request.temperature is not None:
        payload["temperature"] = provider_request.temperature
    if provider_request.max_output_tokens is not None:
        payload["max_tokens"] = provider_request.max_output_tokens
    return payload


def _json_response_instruction(provider_request: ProviderRequest) -> dict[str, str]:
    if provider_request.metadata.get("phase") == "guidance_request":
        role = provider_request.metadata.get("required_guidance_role")
        if not isinstance(role, str):
            raise DeepSeekProviderError("guidance request requires one declared role")
        return {
            "role": "system",
            "content": (
                "Return a json object with exactly tool_call: "
                "{\"tool\":\"get_guidance_card\",\"arguments\":{\"role\":\"" + role + "\"}}. "
                "Do not generate code, prose, or script_update."
            ),
        }
    return {
        "role": "system",
        "content": (
            "Return a json object with output_text and script_update. script_update must be "
            "{\"kind\": \"replace\", \"content\": \"full build_sequence.py source\"}. "
            "Use the installed cadquery-ocp bindings: import from OCP (for example OCP.BRepPrimAPI, "
            "OCP.STEPControl, and OCP.IFSelect), never OCC.Core. Create or transform the CAD shape and export "
            "a valid STEP to output/model.step. Match the input probe bbox, volume, and topology gates from the "
            "repair context. Do not hand-author raw STEP text. Return only json; do not use markdown fences."
        ),
    }


def _deepseek_response(data: dict, *, requested_model: str) -> ProviderResponse:
    try:
        choice = data["choices"][0]
        content = choice["message"]["content"]
    except (IndexError, KeyError, TypeError) as exc:
        raise DeepSeekProviderError("DeepSeek response did not contain a completion message") from exc
    if not isinstance(content, str):
        raise DeepSeekProviderError("DeepSeek response content was not text")
    try:
        decoded = json.loads(content)
    except json.JSONDecodeError:
        decoded = {}
    update_data = decoded.get("script_update") if isinstance(decoded, dict) else None
    script_update = None
    if isinstance(update_data, dict) and update_data.get("kind") == "replace" and isinstance(
        update_data.get("content"), str
    ):
        script_update = ScriptUpdate(kind="replace", content=update_data["content"])
    tool_data = decoded.get("tool_call") if isinstance(decoded, dict) else None
    tool_call = None
    if isinstance(tool_data, dict) and isinstance(tool_data.get("tool"), str) and isinstance(tool_data.get("arguments"), dict):
        tool_call = ToolCall(tool=tool_data["tool"], arguments=tool_data["arguments"])
    output_text = decoded.get("output_text", content) if isinstance(decoded, dict) else content
    return ProviderResponse(
        provider="deepseek",
        model=str(data.get("model", requested_model)),
        output_text=str(output_text),
        finish_reason=str(choice.get("finish_reason", "stop")),
        script_update=script_update,
        tool_call=tool_call,
        usage=data.get("usage", {}) if isinstance(data.get("usage", {}), dict) else {},
        raw_summary={key: data[key] for key in ("id", "created", "model") if key in data},
    )


class FakeLLMProvider:
    """Deterministic local provider for tests and offline smoke runs."""

    name = "fake"

    def __init__(self, responses: list[ProviderResponse] | None = None) -> None:
        self._responses = list(responses or [])
        self.requests: list[ProviderRequest] = []

    def complete(self, request: ProviderRequest) -> ProviderResponse:
        self.requests.append(request)
        if self._responses:
            return self._responses.pop(0)
        return ProviderResponse(
            provider=self.name,
            model=request.model,
            output_text="No queued fake response. Keep the existing build_sequence.py unchanged.",
            finish_reason="stop",
            usage={"input_messages": len(request.messages), "output_chars": 0},
            raw_summary={"mode": "default"},
        )


def fake_replacement_response(content: str, *, model: str = "fake-repair") -> ProviderResponse:
    return ProviderResponse(
        provider="fake",
        model=model,
        output_text="Replace build_sequence.py with the provided script.",
        script_update=ScriptUpdate(kind="replace", content=content),
        usage={"output_chars": len(content)},
        raw_summary={"response_type": "script_replacement"},
    )


def fake_guidance_request(*, role: str = "final primitive", model: str = "fake-guidance") -> ProviderResponse:
    return ProviderResponse(
        provider="fake",
        model=model,
        output_text="Request the bounded guidance card.",
        tool_call=ToolCall(tool="get_guidance_card", arguments={"role": role}),
        raw_summary={"response_type": "tool_call"},
    )


def fake_edit_response(instructions: str, *, model: str = "fake-repair") -> ProviderResponse:
    return ProviderResponse(
        provider="fake",
        model=model,
        output_text=instructions,
        script_update=ScriptUpdate(kind="edit", instructions=instructions),
        usage={"output_chars": len(instructions)},
        raw_summary={"response_type": "script_edit"},
    )
