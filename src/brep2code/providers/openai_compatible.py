from __future__ import annotations

from dataclasses import asdict, dataclass, field
from http.client import HTTPException
import json
import os
from pathlib import Path
from typing import Any, Callable
from urllib import error, request

from brep2code.providers.action_protocol import ActionRequest, ActionResponse
from brep2code.providers.active_prompt import build_action_messages
from brep2code.providers.protocol import ProviderRequest, ProviderResponse
from brep2code.providers.prompt import build_messages


class ProviderError(RuntimeError):
    pass


class ProviderProtocolError(ProviderError):
    pass


class ProviderTransportError(ProviderError):
    pass


class ProviderExchangeArtifactError(ProviderError):
    pass


class ProviderConfigurationError(ProviderError):
    pass


class ProviderBudgetError(ProviderError):
    def __init__(self, message: str, *, scope: str = "provider") -> None:
        super().__init__(message)
        self.scope = scope


@dataclass(frozen=True)
class ProviderLimits:
    max_requests: int
    timeout_seconds: float
    max_retries: int
    max_output_tokens: int
    max_total_tokens: int
    max_cost_usd: float
    input_cost_per_million: float
    output_cost_per_million: float

    def __post_init__(self) -> None:
        integer_limits = (
            self.max_requests,
            self.max_retries,
            self.max_output_tokens,
            self.max_total_tokens,
        )
        if any(not isinstance(value, int) or isinstance(value, bool) for value in integer_limits):
            raise ProviderConfigurationError("request, retry, and token limits must be integers")
        if self.max_requests < 1 or self.max_output_tokens < 1 or self.max_total_tokens < 1:
            raise ProviderConfigurationError("request and token limits must be positive")
        if self.max_retries < 0 or self.timeout_seconds <= 0 or self.max_cost_usd <= 0:
            raise ProviderConfigurationError(
                "timeout/cost must be positive and retries non-negative"
            )
        if self.input_cost_per_million < 0 or self.output_cost_per_million < 0:
            raise ProviderConfigurationError("token prices must be non-negative")


@dataclass(frozen=True)
class OpenAICompatibleConfig:
    provider: str
    base_url: str
    api_key: str = field(repr=False)
    model: str = ""
    thinking_mode: str | None = None

    def __post_init__(self) -> None:
        if not self.provider or not self.model or not self.api_key:
            raise ProviderConfigurationError("provider, model, and API key are required")
        if not self.base_url.startswith("https://"):
            raise ProviderConfigurationError("provider base URL must use HTTPS")
        if self.thinking_mode not in {None, "enabled", "disabled"}:
            raise ProviderConfigurationError("thinking mode must be enabled or disabled")


class OpenAICompatibleProvider:
    def __init__(
        self,
        config: OpenAICompatibleConfig,
        limits: ProviderLimits,
        *,
        opener: Callable[..., Any] = request.urlopen,
        exchange_recorder: Callable[[str, int, dict[str, Any]], None] | None = None,
    ) -> None:
        self.config = config
        self.limits = limits
        self.name = config.provider
        self.model = config.model
        self._opener = opener
        self._exchange_recorder = exchange_recorder
        self.requests_issued = 0
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.total_tokens = 0
        self.cost_usd = 0.0
        self.in_flight_requests = 0
        self.protocol_retries = 0
        self._accounting_checkpoint: Callable[[dict[str, Any]], None] | None = None

    def set_accounting_checkpoint(self, callback: Callable[[dict[str, Any]], None] | None) -> None:
        self._accounting_checkpoint = callback

    def accounting_snapshot(self) -> dict[str, Any]:
        return {
            "http_attempts": self.requests_issued,
            "in_flight_requests": self.in_flight_requests,
            "protocol_retries": self.protocol_retries,
            "tokens": {
                "prompt": self.prompt_tokens,
                "completion": self.completion_tokens,
                "total": self.total_tokens,
            },
            "cost_usd": self.cost_usd,
            "pricing": {
                "input_cost_per_million": self.limits.input_cost_per_million,
                "output_cost_per_million": self.limits.output_cost_per_million,
            },
            "ceilings": {
                key: value
                for key, value in asdict(self.limits).items()
                if key not in {"input_cost_per_million", "output_cost_per_million"}
            },
        }

    def restore_accounting(self, snapshot: dict[str, Any]) -> None:
        from brep2code.harness.active_results import validate_provider_accounting

        validate_provider_accounting(snapshot, self.limits)
        self.requests_issued = snapshot["http_attempts"]
        self.prompt_tokens = snapshot["tokens"]["prompt"]
        self.completion_tokens = snapshot["tokens"]["completion"]
        self.total_tokens = snapshot["tokens"]["total"]
        self.cost_usd = snapshot["cost_usd"]
        self.in_flight_requests = 0
        self.protocol_retries = int(snapshot.get("protocol_retries", 0))
        if self.requests_issued > self.limits.max_requests:
            raise ProviderBudgetError("provider request budget exhausted")
        self._raise_if_usage_budget_exhausted(at_ceiling=True)
        self._notify_accounting()

    def _notify_accounting(self) -> None:
        if self._accounting_checkpoint is not None:
            try:
                self._accounting_checkpoint(self.accounting_snapshot())
            except Exception as exc:
                raise ProviderExchangeArtifactError(
                    "provider accounting artifact could not be persisted"
                ) from exc

    def generate(self, provider_request: ProviderRequest) -> ProviderResponse:
        return self._request(build_messages(provider_request), self._parse_response)

    def choose_action(self, action_request: ActionRequest) -> ActionResponse:
        return self._request(
            build_action_messages(action_request),
            self._parse_action_response,
            retry_protocol=True,
        )

    def _request(
        self,
        messages: list[dict[str, str]],
        parser: Callable[[dict], Any],
        *,
        retry_protocol: bool = False,
    ):
        last_error: Exception | None = None
        for attempt in range(self.limits.max_retries + 1):
            attempt_messages = (
                _protocol_retry_messages(messages) if retry_protocol and attempt else messages
            )
            payload = {
                "model": self.model,
                "messages": attempt_messages,
                "response_format": {"type": "json_object"},
                "max_tokens": self.limits.max_output_tokens,
            }
            if self.config.thinking_mode is not None:
                payload["thinking"] = {"type": self.config.thinking_mode}
            body = json.dumps(payload).encode("utf-8")
            if self.requests_issued >= self.limits.max_requests:
                raise ProviderBudgetError("provider request budget exhausted")
            self._raise_if_usage_budget_exhausted(at_ceiling=True)
            self.requests_issued += 1
            self.in_flight_requests += 1
            self._notify_accounting()
            http_request = request.Request(
                f"{self.config.base_url.rstrip('/')}/chat/completions",
                data=body,
                headers={
                    "Authorization": f"Bearer {self.config.api_key}",
                    "Content-Type": "application/json",
                },
                method="POST",
            )
            try:
                self._record_exchange(
                    "request",
                    self.requests_issued,
                    {
                        "endpoint": "/chat/completions",
                        "timeout_seconds": self.limits.timeout_seconds,
                        "body": payload,
                    },
                )
                with self._opener(http_request, timeout=self.limits.timeout_seconds) as response:
                    maximum_bytes = self.limits.max_output_tokens * 16 + 65_536
                    raw_response = response.read(maximum_bytes + 1)
                if len(raw_response) > maximum_bytes:
                    raise ProviderError("provider response exceeded bounded byte limit")
                decoded = json.loads(raw_response.decode("utf-8"))
                self._record_exchange(
                    "response",
                    self.requests_issued,
                    _redacted_response_artifact(decoded),
                )
                parsed = parser(decoded)
            except error.HTTPError as exc:
                if exc.code < 500 or attempt == self.limits.max_retries:
                    raise ProviderError(f"provider returned HTTP {exc.code}") from exc
                last_error = exc
            except (error.URLError, TimeoutError, ConnectionError, OSError, HTTPException) as exc:
                if attempt == self.limits.max_retries:
                    raise ProviderTransportError(
                        "provider request failed or timed out"
                    ) from exc
                last_error = exc
            except ProviderProtocolError as exc:
                if not retry_protocol or attempt == self.limits.max_retries:
                    raise
                self.protocol_retries += 1
                last_error = exc
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                if not retry_protocol or attempt == self.limits.max_retries:
                    raise ProviderProtocolError("provider returned invalid JSON") from exc
                self.protocol_retries += 1
                last_error = exc
            else:
                return parsed
            finally:
                self.in_flight_requests -= 1
                self._notify_accounting()
        raise ProviderError("provider request failed") from last_error

    def _record_exchange(self, event: str, attempt: int, payload: dict[str, Any]) -> None:
        if self._exchange_recorder is not None:
            try:
                self._exchange_recorder(event, attempt, payload)
            except Exception as exc:
                raise ProviderExchangeArtifactError(
                    f"provider {event} artifact could not be persisted"
                ) from exc

    def _parse_action_response(self, payload: dict[str, Any]) -> ActionResponse:
        prompt_tokens, completion_tokens, total_tokens, request_cost = self._validated_usage(
            payload
        )
        self._commit_usage(prompt_tokens, completion_tokens, total_tokens, request_cost)
        self._raise_if_usage_budget_exhausted(at_ceiling=False)
        _validate_response_model(payload, self.model)
        content, reasoning_content = _response_content(payload)
        action = _decode_action_object(content, reasoning_content)
        return ActionResponse(
            provider=self.name,
            model=str(payload.get("model", self.model)),
            action=action,
            usage={
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens,
                "cost_usd": request_cost,
            },
        )

    def _parse_response(self, payload: dict[str, Any]) -> ProviderResponse:
        prompt_tokens, completion_tokens, total_tokens, request_cost = self._validated_usage(
            payload
        )
        self._commit_usage(prompt_tokens, completion_tokens, total_tokens, request_cost)
        self._raise_if_usage_budget_exhausted(at_ceiling=False)
        _validate_response_model(payload, self.model)
        content, reasoning_content = _response_content(payload)
        decoded = _decode_content_object(content, reasoning_content)
        script = decoded.get("script")
        if not isinstance(script, str) or not script:
            raise _contract_error("script_missing_or_empty")
        return ProviderResponse(
            provider=self.name,
            model=str(payload.get("model", self.model)),
            script=script,
            usage={
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens,
                "cost_usd": request_cost,
            },
        )

    def _validated_usage(self, payload: dict[str, Any]) -> tuple[int, int, int, float]:
        if not isinstance(payload, dict):
            raise _contract_error("top_level_not_object")
        usage = payload.get("usage")
        if not isinstance(usage, dict):
            raise _contract_error("usage_missing_or_invalid")
        try:
            prompt_tokens = int(usage["prompt_tokens"])
            completion_tokens = int(usage["completion_tokens"])
            total_tokens = int(usage["total_tokens"])
        except (KeyError, TypeError, ValueError) as exc:
            raise _contract_error("usage_fields_invalid") from exc
        if (
            prompt_tokens < 0
            or completion_tokens < 0
            or total_tokens < 0
            or prompt_tokens + completion_tokens != total_tokens
        ):
            raise _contract_error("usage_fields_invalid")
        request_cost = (
            prompt_tokens * self.limits.input_cost_per_million
            + completion_tokens * self.limits.output_cost_per_million
        ) / 1_000_000
        return prompt_tokens, completion_tokens, total_tokens, request_cost

    def _commit_usage(
        self,
        prompt_tokens: int,
        completion_tokens: int,
        total_tokens: int,
        request_cost: float,
    ) -> None:
        self.prompt_tokens += prompt_tokens
        self.completion_tokens += completion_tokens
        self.total_tokens += total_tokens
        self.cost_usd += request_cost

    def _raise_if_usage_budget_exhausted(self, *, at_ceiling: bool) -> None:
        token_exhausted = (
            self.total_tokens >= self.limits.max_total_tokens
            if at_ceiling
            else self.total_tokens > self.limits.max_total_tokens
        )
        cost_exhausted = (
            self.cost_usd >= self.limits.max_cost_usd
            if at_ceiling
            else self.cost_usd > self.limits.max_cost_usd
        )
        if token_exhausted:
            raise ProviderBudgetError("provider token budget exceeded")
        if cost_exhausted:
            raise ProviderBudgetError("provider cost budget exceeded")


def _contract_error(reason: str) -> ProviderError:
    """Create a safe diagnostic without including provider response content."""
    return ProviderProtocolError(f"provider response violated the JSON contract: {reason}")


def _protocol_retry_messages(messages: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        *messages,
        {
            "role": "user",
            "content": (
                "The previous provider response did not satisfy the action JSON contract. "
                "Return exactly one currently allowed action as valid JSON only."
            ),
        },
    ]


def _redacted_response_artifact(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {"shape": "non_object"}
    artifact: dict[str, Any] = {
        "model": payload.get("model"),
        "usage": payload.get("usage"),
    }
    choices = payload.get("choices")
    if isinstance(choices, list) and choices and isinstance(choices[0], dict):
        message = choices[0].get("message")
        if isinstance(message, dict):
            artifact["message"] = {"content": message.get("content")}
    return artifact


def _validate_response_model(payload: dict[str, Any], expected_model: str) -> None:
    if payload.get("model") != expected_model:
        raise _contract_error("model_identity_drift")


def _response_content(payload: dict[str, Any]) -> tuple[str, Any]:
    choices = payload.get("choices")
    if not isinstance(choices, list) or not choices:
        raise _contract_error("choices_missing_or_empty")
    first_choice = choices[0]
    if not isinstance(first_choice, dict):
        raise _contract_error("choice_not_object")
    message = first_choice.get("message")
    if not isinstance(message, dict):
        raise _contract_error("message_missing_or_invalid")
    content = message.get("content")
    reasoning_content = message.get("reasoning_content")
    if not isinstance(content, str):
        raise _contract_error(f"content_not_string_{_reasoning_diagnostic(reasoning_content)}")
    return content, reasoning_content


def _decode_action_object(content: str, reasoning_content: Any = None) -> dict[str, Any]:
    normalized = content.strip()
    lines = normalized.splitlines()
    fence = lines[0].strip().lower() if lines else ""
    if len(lines) >= 3 and fence in {"```", "```json"}:
        if lines[-1].strip() != "```" or normalized.count("```") != 2:
            raise _content_contract_error(normalized, reasoning_content)
        normalized = "\n".join(lines[1:-1]).strip()
    elif "```" in normalized:
        normalized, fenced_language = _extract_single_fenced_payload(normalized, reasoning_content)
        if fenced_language not in {"", "json"}:
            raise _content_contract_error(content, reasoning_content)
    try:
        decoded = json.loads(normalized)
    except json.JSONDecodeError as exc:
        raise _content_contract_error(content, reasoning_content) from exc
    if not isinstance(decoded, dict):
        raise _contract_error("content_not_object")
    return decoded


def _decode_content_object(content: str, reasoning_content: Any = None) -> dict[str, Any]:
    normalized = content.strip()
    lines = normalized.splitlines()
    fence = lines[0].strip().lower() if lines else ""
    if len(lines) >= 3 and fence in {"```python", "```py"}:
        if lines[-1].strip() != "```" or normalized.count("```") != 2:
            raise _content_contract_error(normalized, reasoning_content)
        script = "\n".join(lines[1:-1]).strip()
        if not script:
            raise _contract_error("script_missing_or_empty")
        return {"script": script}
    if len(lines) >= 3 and fence in {"```", "```json"}:
        if lines[-1].strip() != "```" or normalized.count("```") != 2:
            raise _content_contract_error(normalized, reasoning_content)
        normalized = "\n".join(lines[1:-1]).strip()
    elif "```" in normalized:
        normalized, fenced_language = _extract_single_fenced_payload(normalized, reasoning_content)
        if fenced_language in {"python", "py"}:
            if not normalized:
                raise _contract_error("script_missing_or_empty")
            return {"script": normalized}
    try:
        decoded = json.loads(normalized)
    except json.JSONDecodeError as exc:
        raise _content_contract_error(content, reasoning_content) from exc
    if not isinstance(decoded, dict):
        raise _contract_error("content_not_object")
    if "script" not in decoded:
        raise _contract_error("script_missing_or_empty")
    if set(decoded) != {"script"}:
        raise _contract_error("content_fields_invalid")
    return decoded


def _extract_single_fenced_payload(content: str, reasoning_content: Any = None) -> tuple[str, str]:
    """Extract one complete supported fence with only bounded surrounding prose."""
    if content.count("```") != 2:
        raise _content_contract_error(content, reasoning_content)
    prefix, fenced = content.split("```", 1)
    opening, separator, remainder = fenced.partition("\n")
    if not separator:
        raise _content_contract_error(content, reasoning_content)
    payload, closing, suffix = remainder.partition("```")
    language = opening.strip().lower()
    if not closing or language not in {"", "json", "python", "py"}:
        raise _content_contract_error(content, reasoning_content)
    if len(prefix.strip()) + len(suffix.strip()) > 512:
        raise _content_contract_error(content, reasoning_content)
    return payload.strip(), language


def _content_contract_error(content: str, reasoning_content: Any = None) -> ProviderError:
    normalized = content.strip()
    if not normalized:
        shape = "empty"
    elif normalized.startswith(("{", "[")):
        shape = "json_like"
    elif normalized.startswith("<think"):
        shape = "reasoning_prefixed"
    elif "```" in normalized:
        fence_count = normalized.count("```")
        if fence_count == 1:
            shape = "unterminated_fence"
        elif fence_count == 2:
            shape = "single_fence"
        else:
            shape = "multiple_fences"
    else:
        shape = "plain_text"
    length = len(normalized)
    length_bucket = "short" if length <= 512 else "medium" if length <= 4096 else "long"
    return _contract_error(
        f"content_not_json_{shape}_{length_bucket}_{_reasoning_diagnostic(reasoning_content)}"
    )


def _reasoning_diagnostic(reasoning_content: Any) -> str:
    if reasoning_content is None:
        return "reasoning_absent"
    if not isinstance(reasoning_content, str):
        return "reasoning_invalid"
    length = len(reasoning_content.strip())
    if length == 0:
        return "reasoning_empty"
    if length <= 512:
        return "reasoning_short"
    if length <= 4096:
        return "reasoning_medium"
    return "reasoning_long"


def deepseek_config_from_env(
    environ: dict[str, str] | None = None,
    *,
    env_file: Path | None = None,
    thinking_mode: str | None = None,
) -> OpenAICompatibleConfig:
    values = dict(os.environ if environ is None else environ)
    if env_file is not None and env_file.is_file():
        file_values = _read_env_file(env_file)
        values = {**file_values, **values}
    return OpenAICompatibleConfig(
        provider="deepseek",
        base_url=values.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
        api_key=values.get("DEEPSEEK_API_KEY", ""),
        model=values.get("DEEPSEEK_MODEL", ""),
        thinking_mode=thinking_mode,
    )


def _read_env_file(path: Path) -> dict[str, str]:
    allowed = {"DEEPSEEK_API_KEY", "DEEPSEEK_MODEL", "DEEPSEEK_BASE_URL"}
    values: dict[str, str] = {}
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ProviderConfigurationError(f"invalid provider env file line {line_number}")
        name, value = line.split("=", 1)
        name = name.strip()
        if name not in allowed or name in values:
            raise ProviderConfigurationError(f"invalid provider env file key on line {line_number}")
        values[name] = value.strip()
    return values
