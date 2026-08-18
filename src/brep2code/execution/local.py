from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import subprocess
import sys
from time import perf_counter


@dataclass(frozen=True)
class ExecutionResult:
    exit_code: int
    stdout: str
    stderr: str
    duration_seconds: float
    output_step: Path | None
    timed_out: bool = False
    sandboxed: bool = False
    sandbox_backend: str = "unsafe-local"
    termination_reason: str = "completed"


def run_build(workspace: Path, *, timeout_seconds: int = 30) -> ExecutionResult:
    workspace = workspace.resolve()
    script = workspace / "build.py"
    if not workspace.is_dir() or not script.is_file():
        raise ValueError("revision workspace must contain build.py")
    if timeout_seconds < 1:
        raise ValueError("timeout_seconds must be positive")

    start = perf_counter()
    try:
        completed = subprocess.run(
            [sys.executable, "build.py"],
            cwd=workspace,
            env=_minimal_environment(),
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        return ExecutionResult(
            exit_code=124,
            stdout=exc.stdout or "",
            stderr=exc.stderr or "",
            duration_seconds=perf_counter() - start,
            output_step=None,
            timed_out=True,
            termination_reason="timeout",
        )
    output = workspace / "output.step"
    return ExecutionResult(
        exit_code=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
        duration_seconds=perf_counter() - start,
        output_step=output if completed.returncode == 0 and output.is_file() else None,
        termination_reason="completed" if completed.returncode == 0 else "script_error",
    )


def _minimal_environment() -> dict[str, str]:
    allowed = ("PATH", "SYSTEMROOT", "WINDIR")
    environment = {name: os.environ[name] for name in allowed if name in os.environ}
    environment["PYTHONIOENCODING"] = "utf-8"
    return environment
