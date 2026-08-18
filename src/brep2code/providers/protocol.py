from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True)
class ProviderRequest:
    case_id: str
    round_index: int
    context: dict[str, Any]
    feedback: dict[str, Any] | None = None
    previous_script: str | None = None


@dataclass(frozen=True)
class ProviderResponse:
    provider: str
    model: str
    script: str
    usage: dict[str, int | float] | None = None


class Provider(Protocol):
    name: str
    model: str

    def generate(self, request: ProviderRequest) -> ProviderResponse: ...
