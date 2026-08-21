from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from brep2code.backends import BackendProfileId, backend_profile
from brep2code.cases import ValidatedCase
from brep2code.harness.active import ActiveBudgets, RetrievalPolicy
from brep2code.harness.active_results import (
    ActiveResultValidationError,
    validate_active_result,
    validate_provider_accounting,
)
from brep2code.providers import ProviderLimits
from brep2code.providers.task_contract import build_provider_task_contract


@dataclass(frozen=True)
class ActiveHostedAuthorization:
    hosted: bool
    observations: bool
    tool_results: bool
    revision_source: bool
    feedback: bool

    def validate(self) -> None:
        missing = [name for name, allowed in asdict(self).items() if not allowed]
        if missing:
            names = ", ".join(name.replace("_", "-") for name in missing)
            raise ActiveResultValidationError(
                f"active hosted preflight requires fresh authorization: {names}"
            )


def preflight_active_hosted(
    case: ValidatedCase,
    run_root: Path,
    *,
    provider: str,
    model: str,
    thinking_mode: str,
    budgets: ActiveBudgets,
    build_timeout_seconds: int,
    provider_limits: ProviderLimits,
    authorization: ActiveHostedAuthorization,
    retrieval_policy: RetrievalPolicy = RetrievalPolicy.BOUNDED_SEED,
    backend: BackendProfileId | str = BackendProfileId.OCP_V1,
    continuation_payload: dict[str, Any] | None = None,
    continuation_result: Path | None = None,
    require_authorization: bool = True,
) -> dict[str, Any]:
    profile = backend_profile(backend)
    task_contract = build_provider_task_contract(profile.profile_id, retrieval_policy)
    if require_authorization:
        authorization.validate()
    if retrieval_policy is RetrievalPolicy.DISABLED and budgets.retrievals != 0:
        raise ActiveResultValidationError(
            "disabled retrieval policy requires zero retrieval budget"
        )
    if provider != "deepseek" or not model:
        raise ActiveResultValidationError("active hosted provider/model is invalid")
    if thinking_mode != "disabled":
        raise ActiveResultValidationError("active hosted thinking mode must be disabled")
    if build_timeout_seconds < 1:
        raise ActiveResultValidationError("active hosted build timeout must be positive")
    if budgets.tokens < 1 or budgets.cost_usd <= 0:
        raise ActiveResultValidationError(
            "active hosted session token/cost budgets must be positive"
        )
    if budgets.tokens > provider_limits.max_total_tokens:
        raise ActiveResultValidationError("session token budget exceeds provider aggregate ceiling")
    if budgets.cost_usd > provider_limits.max_cost_usd:
        raise ActiveResultValidationError("session cost budget exceeds provider aggregate ceiling")
    maximum_attempts = budgets.model_requests * (1 + provider_limits.max_retries)
    if provider_limits.max_requests < budgets.model_requests:
        raise ActiveResultValidationError("provider requests must cover every model turn")
    if provider_limits.max_requests > maximum_attempts:
        raise ActiveResultValidationError("provider requests exceed retry capacity")
    if provider_limits.max_output_tokens > provider_limits.max_total_tokens:
        raise ActiveResultValidationError("provider output ceiling exceeds aggregate token ceiling")

    used_requests = 0
    continuation = continuation_payload is not None or continuation_result is not None
    if continuation:
        if continuation_payload is None or continuation_result is None:
            raise ActiveResultValidationError("active hosted continuation inputs are incomplete")
        if continuation_result != run_root / "result.json":
            raise ActiveResultValidationError("active hosted continuation must reuse its run root")
        validate_active_result(continuation_payload, case, run_root)
        validate_provider_accounting(continuation_payload["provider_accounting"], provider_limits)
        if continuation_payload["terminal"]:
            raise ActiveResultValidationError("active hosted continuation result is terminal")
        if continuation_payload["provider"] != provider or continuation_payload["model"] != model:
            raise ActiveResultValidationError("active hosted continuation provider/model drift")
        if continuation_payload["budgets"] != asdict(budgets):
            raise ActiveResultValidationError("active hosted continuation budget drift")
        if continuation_payload["timeout_seconds"] != build_timeout_seconds:
            raise ActiveResultValidationError("active hosted continuation timeout drift")
        if (
            continuation_payload.get("retrieval_policy", RetrievalPolicy.BOUNDED_SEED)
            != retrieval_policy
        ):
            raise ActiveResultValidationError("active hosted continuation retrieval policy drift")
        if (
            continuation_payload.get("backend_profile", BackendProfileId.OCP_V1)
            != profile.profile_id
        ):
            raise ActiveResultValidationError("active hosted continuation backend profile drift")
        used_requests = int(continuation_payload["usage"]["model_requests"])
    elif run_root.exists():
        raise ActiveResultValidationError("active hosted run root must be fresh")

    remaining_requests = budgets.model_requests - used_requests
    if remaining_requests < 1:
        raise ActiveResultValidationError("active hosted session has no remaining model requests")
    return {
        "case_id": case.case.case_id,
        "provider": provider,
        "model": model,
        "thinking_mode": thinking_mode,
        "retrieval_policy": retrieval_policy,
        "backend_profile": profile.profile_id,
        "task_contract_hash": task_contract.identity,
        "task_contract": task_contract.projection(),
        "continuation": continuation,
        "continuation_requires_fresh_authorization": continuation,
        "remaining_model_requests": remaining_requests,
        "controller_budget": asdict(budgets),
        "provider_budget": asdict(provider_limits),
        "outbound_projection": {
            "initial": [
                "case_id",
                "unit",
                "initial_observations",
                "allowed_actions",
                "available_tools",
                "session_phase",
                "retrieval_policy",
                "backend_profile",
                "current_revision",
            ],
            "iterative": ["bounded_tool_results", "typed_feedback", "current_revision"],
            "excluded": [
                "eval_references",
                "target_solution",
                "private_oracles",
                "repository_files",
                "host_paths",
                "secrets",
            ],
        },
        "authorization": asdict(authorization),
        "authorization_required": require_authorization,
    }
