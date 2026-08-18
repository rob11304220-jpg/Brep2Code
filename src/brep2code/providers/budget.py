from __future__ import annotations

from dataclasses import dataclass

from brep2code.providers.openai_compatible import ProviderBudgetError
from brep2code.providers.protocol import Provider, ProviderRequest, ProviderResponse


@dataclass(frozen=True)
class CaseBudgetLimits:
    scope: str
    max_requests: int
    max_total_tokens: int
    max_cost_usd: float

    def __post_init__(self) -> None:
        if self.scope != "case":
            raise ValueError("case budget scope must be 'case'")
        if self.max_requests < 1 or self.max_total_tokens < 1 or self.max_cost_usd <= 0:
            raise ValueError("case budget limits must be positive")


class CaseBudgetProvider:
    """Expose independent case accounting over one aggregate provider."""

    def __init__(self, provider: Provider, limits: CaseBudgetLimits) -> None:
        self._provider = provider
        self.limits = limits
        self.name = provider.name
        self.model = provider.model
        self.requests_issued = 0
        self.total_tokens = 0
        self.cost_usd = 0.0

    def generate(self, provider_request: ProviderRequest) -> ProviderResponse:
        if self.requests_issued >= self.limits.max_requests:
            raise ProviderBudgetError("case request budget exhausted", scope="case")
        self.requests_issued += 1
        provider_tokens_before = getattr(self._provider, "total_tokens", None)
        provider_cost_before = getattr(self._provider, "cost_usd", None)
        try:
            response = self._provider.generate(provider_request)
        except ProviderBudgetError as exc:
            self._record_provider_delta(provider_tokens_before, provider_cost_before)
            raise ProviderBudgetError(str(exc), scope="campaign_aggregate") from exc
        except Exception:
            self._record_provider_delta(provider_tokens_before, provider_cost_before)
            self._enforce_case_budget()
            raise
        usage = response.usage or {}
        total_tokens = int(usage.get("total_tokens", 0))
        request_cost = float(usage.get("cost_usd", 0.0))
        self.total_tokens += total_tokens
        self.cost_usd += request_cost
        self._enforce_case_budget()
        return response

    def _record_provider_delta(
        self, tokens_before: object, cost_before: object
    ) -> None:
        tokens_after = getattr(self._provider, "total_tokens", None)
        cost_after = getattr(self._provider, "cost_usd", None)
        if isinstance(tokens_before, int) and isinstance(tokens_after, int):
            self.total_tokens += max(0, tokens_after - tokens_before)
        if isinstance(cost_before, int | float) and isinstance(cost_after, int | float):
            self.cost_usd += max(0.0, float(cost_after) - float(cost_before))

    def _enforce_case_budget(self) -> None:
        if self.total_tokens > self.limits.max_total_tokens:
            raise ProviderBudgetError("case token budget exceeded", scope="case")
        if self.cost_usd > self.limits.max_cost_usd:
            raise ProviderBudgetError("case cost budget exceeded", scope="case")
