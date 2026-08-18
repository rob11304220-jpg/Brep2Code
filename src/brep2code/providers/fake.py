from __future__ import annotations

from collections.abc import Iterable

from brep2code.providers.protocol import ProviderRequest, ProviderResponse


class FakeProvider:
    """Deterministic offline provider backed by a finite script queue."""

    name = "fake"
    model = "fake-script-queue-v1"

    def __init__(self, scripts: Iterable[str]) -> None:
        self._scripts = iter(scripts)
        self.requests: list[ProviderRequest] = []

    def generate(self, request: ProviderRequest) -> ProviderResponse:
        self.requests.append(request)
        try:
            script = next(self._scripts)
        except StopIteration as exc:
            raise RuntimeError("fake provider script queue exhausted") from exc
        return ProviderResponse(
            provider=self.name,
            model=self.model,
            script=script,
            usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
        )
