from __future__ import annotations

import pytest

from brep2code.providers import (
    CaseBudgetLimits,
    CaseBudgetProvider,
    FakeProvider,
    ProviderBudgetError,
    ProviderResponse,
)
from brep2code.providers.protocol import ProviderRequest


def test_case_budget_provider_keeps_case_accounting_independent() -> None:
    provider = CaseBudgetProvider(
        FakeProvider(["one", "two"]),
        CaseBudgetLimits(scope="case", max_requests=2, max_total_tokens=1, max_cost_usd=1.0),
    )

    first = provider.generate(_request())
    second = provider.generate(_request())

    assert first.script == "one"
    assert second.script == "two"
    assert provider.requests_issued == 2
    assert provider.total_tokens == 0
    assert provider.cost_usd == 0.0


def test_case_budget_provider_rejects_a_third_case_request() -> None:
    provider = CaseBudgetProvider(
        FakeProvider(["one", "two", "three"]),
        CaseBudgetLimits(scope="case", max_requests=2, max_total_tokens=1, max_cost_usd=1.0),
    )
    provider.generate(_request())
    provider.generate(_request())

    with pytest.raises(ProviderBudgetError, match="case request budget"):
        provider.generate(_request())


def test_case_budget_provider_keeps_usage_counters_per_wrapper() -> None:
    shared = UsageProvider()
    first_case = CaseBudgetProvider(
        shared,
        CaseBudgetLimits(scope="case", max_requests=1, max_total_tokens=10, max_cost_usd=1.0),
    )
    second_case = CaseBudgetProvider(
        shared,
        CaseBudgetLimits(scope="case", max_requests=1, max_total_tokens=10, max_cost_usd=1.0),
    )

    first_case.generate(_request())
    second_case.generate(_request())

    assert first_case.total_tokens == 3
    assert second_case.total_tokens == 3
    assert shared.total_tokens == 6


def test_case_budget_provider_records_underlying_usage_when_generation_fails() -> None:
    provider = CaseBudgetProvider(
        FailingUsageProvider(),
        CaseBudgetLimits(scope="case", max_requests=1, max_total_tokens=10, max_cost_usd=1.0),
    )

    with pytest.raises(RuntimeError, match="invalid provider response"):
        provider.generate(_request())

    assert provider.requests_issued == 1
    assert provider.total_tokens == 5
    assert provider.cost_usd == pytest.approx(0.02)


def test_case_budget_provider_enforces_usage_from_failed_generation() -> None:
    provider = CaseBudgetProvider(
        FailingUsageProvider(),
        CaseBudgetLimits(scope="case", max_requests=1, max_total_tokens=4, max_cost_usd=1.0),
    )

    with pytest.raises(ProviderBudgetError, match="case token budget") as exc_info:
        provider.generate(_request())

    assert exc_info.value.scope == "case"
    assert provider.total_tokens == 5


class UsageProvider:
    name = "usage"
    model = "usage-test"

    def __init__(self) -> None:
        self.total_tokens = 0

    def generate(self, request: ProviderRequest) -> ProviderResponse:
        del request
        self.total_tokens += 3
        return ProviderResponse(
            provider=self.name,
            model=self.model,
            script="script",
            usage={"total_tokens": 3, "cost_usd": 0.01},
        )


class FailingUsageProvider:
    name = "usage"
    model = "usage-test"

    def __init__(self) -> None:
        self.total_tokens = 0
        self.cost_usd = 0.0

    def generate(self, request: ProviderRequest) -> ProviderResponse:
        del request
        self.total_tokens += 5
        self.cost_usd += 0.02
        raise RuntimeError("invalid provider response")


def _request() -> ProviderRequest:
    return ProviderRequest(case_id="box", round_index=0, context={})
