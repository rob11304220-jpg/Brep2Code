from __future__ import annotations

from collections.abc import Iterable
from copy import deepcopy
from typing import Any

from brep2code.providers.action_protocol import ActionRequest, ActionResponse


class FakeActionProvider:
    """Deterministic offline provider backed by a finite action queue."""

    name = "fake"
    model = "fake-action-queue-v1"

    def __init__(self, actions: Iterable[dict[str, Any]]) -> None:
        self._actions = iter(actions)
        self.requests: list[ActionRequest] = []

    def choose_action(self, request: ActionRequest) -> ActionResponse:
        self.requests.append(request)
        try:
            action = deepcopy(next(self._actions))
        except StopIteration as exc:
            raise RuntimeError("fake provider action queue exhausted") from exc
        return ActionResponse(
            provider=self.name,
            model=self.model,
            action=action,
            usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
        )
