from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True)
class ActionRequest:
    case_id: str
    turn_index: int
    session: dict[str, Any]


@dataclass(frozen=True)
class ActionResponse:
    provider: str
    model: str
    action: dict[str, Any]
    usage: dict[str, int | float] | None = None


class ActionProvider(Protocol):
    name: str
    model: str

    def choose_action(self, request: ActionRequest) -> ActionResponse: ...
