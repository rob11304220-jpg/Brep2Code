from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path


class RunStatus(StrEnum):
    CREATED = "created"
    MODEL_CALL = "model_call"
    EXECUTION = "execution"
    VALIDATION = "validation"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    BUDGET_EXHAUSTED = "budget_exhausted"


@dataclass(frozen=True)
class Case:
    case_id: str
    root: Path
    input_step: Path
    split: str = "smoke"


@dataclass(frozen=True)
class Signal:
    code: str
    message: str
    passed: bool


@dataclass(frozen=True)
class SignalBundle:
    passed: bool
    summary: str
    signals: tuple[Signal, ...] = ()


@dataclass
class Revision:
    index: int
    status: RunStatus = RunStatus.CREATED
    script_path: Path | None = None
    signals: SignalBundle | None = None


@dataclass
class Session:
    case: Case
    max_rounds: int
    revisions: list[Revision] = field(default_factory=list)

    def new_revision(self) -> Revision:
        if len(self.revisions) >= self.max_rounds:
            raise RuntimeError("revision budget exhausted")
        revision = Revision(index=len(self.revisions))
        self.revisions.append(revision)
        return revision
