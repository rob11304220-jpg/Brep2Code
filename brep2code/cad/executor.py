"""Execution adapters for revision build_sequence.py files."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import shutil
import subprocess
import sys
from time import perf_counter
from uuid import uuid4


@dataclass(frozen=True)
class ExecutionResult:
    command: list[str]
    cwd: Path
    exit_code: int
    stdout: str
    stderr: str
    duration_seconds: float
    timed_out: bool = False
    sandbox_backend: str = "unsafe-local"
    sandboxed: bool = False
    sandbox_policy_version: str = "none"
    sandbox_capabilities: dict[str, bool] | None = None
    sandbox_mounts: list[str] | None = None
    sandbox_limits: dict[str, int] | None = None
    sandbox_termination_reason: str = "completed"
    sandbox_event: dict[str, str] | None = None
    provenance_trace_path: str | None = None
    provenance_input_accesses: list[str] | None = None
    provenance_coverage: bool = False


class ScriptExecutor:
    """Runs a build script locally.

    This adapter is intentionally named ``unsafe-local`` in execution metadata:
    setting ``cwd`` is not a filesystem or network sandbox.  It remains the
    deterministic developer/test adapter while a secure backend is selected.
    """

    def __init__(self, python_executable: str | None = None) -> None:
        self.python_executable = python_executable or sys.executable

    def run(
        self,
        workspace: Path,
        script_name: str = "build_sequence.py",
        timeout: int = 60,
        input_path: Path | None = None,
        trace_input_access: bool = False,
    ) -> ExecutionResult:
        command = [self.python_executable, script_name]
        env = os.environ.copy()
        env["BREP2CODE_WORKSPACE"] = str(workspace)
        start = perf_counter()
        try:
            completed = subprocess.run(
                command,
                cwd=workspace,
                env=env,
                text=True,
                capture_output=True,
                timeout=timeout,
                check=False,
            )
            duration = perf_counter() - start
            return ExecutionResult(
                command=command,
                cwd=workspace,
                exit_code=completed.returncode,
                stdout=completed.stdout,
                stderr=completed.stderr,
                duration_seconds=duration,
                sandbox_backend="unsafe-local",
                sandbox_capabilities={"filesystem_isolation": False, "network_isolation": False},
                sandbox_termination_reason="completed",
            )
        except subprocess.TimeoutExpired as exc:
            duration = perf_counter() - start
            return ExecutionResult(
                command=command,
                cwd=workspace,
                exit_code=124,
                stdout=exc.stdout or "",
                stderr=(exc.stderr or "") + f"\nTimed out after {timeout} seconds.",
                duration_seconds=duration,
                timed_out=True,
                sandbox_backend="unsafe-local",
                sandbox_capabilities={"filesystem_isolation": False, "network_isolation": False},
                sandbox_termination_reason="timeout",
            )


class WslBubblewrapExecutor:
    """Run a revision script in a staged WSL bubblewrap sandbox.

    The host workspace is copied into an internal WSL staging directory before
    execution.  Inside bubblewrap, only the script is read-only; ``output`` and
    ``intermediates`` are writable.  This adapter is intentionally opt-in while
    its host-specific acceptance probes are completed.
    """

    def __init__(
        self,
        *,
        distro: str = "Ubuntu-24.04",
        runtime_python: str = "/home/liaol/.brep2code-runtime/bin/python",
        runtime_root: str = "/home/liaol/.brep2code-runtime",
        staging_root: str = "/tmp/brep2code-sandbox",
        memory_limit_kib: int = 2_097_152,
        runtime_resources: Path | None = None,
    ) -> None:
        self.distro = distro
        self.runtime_python = runtime_python
        self.runtime_root = runtime_root
        self.staging_root = staging_root
        self.memory_limit_kib = memory_limit_kib
        self.runtime_resources = runtime_resources

    def run(
        self,
        workspace: Path,
        script_name: str = "build_sequence.py",
        timeout: int = 60,
        input_path: Path | None = None,
        trace_input_access: bool = False,
    ) -> ExecutionResult:
        start = perf_counter()
        script_path = workspace / script_name
        if script_name != "build_sequence.py" or not script_path.is_file():
            return _sandbox_error(
                start,
                "sandbox_policy_violation: only an existing build_sequence.py may run",
            )
        if shutil.which("wsl.exe") is None and shutil.which("wsl") is None:
            return _sandbox_error(start, "sandbox_unavailable: wsl executable not found")

        stage = f"{self.staging_root}/{uuid4().hex}"
        host_workspace = self._wsl_path(workspace)
        if host_workspace is None:
            return _sandbox_error(start, "sandbox_unavailable: unable to translate workspace path for WSL")
        host_input = self._wsl_path(input_path) if input_path is not None else ""
        if input_path is not None and host_input is None:
            return _sandbox_error(start, "sandbox_unavailable: unable to translate input path for WSL")
        host_resources = ""
        if self.runtime_resources is not None:
            if not self.runtime_resources.is_dir():
                return _sandbox_error(start, "sandbox_unavailable: runtime resources path is not a directory")
            host_resources = self._wsl_path(self.runtime_resources)
            if host_resources is None:
                return _sandbox_error(start, "sandbox_unavailable: unable to translate runtime resources path for WSL")

        trace_source = self._wsl_path(Path(__file__).with_name("provenance_trace.c")) if trace_input_access else ""
        if trace_input_access and trace_source is None:
            return _sandbox_error(start, "sandbox_unavailable: unable to translate provenance tracer path for WSL")
        wrapper = _wsl_wrapper_script(timeout=timeout, memory_limit_kib=self.memory_limit_kib)
        command = [
            "wsl.exe",
            "-d",
            self.distro,
            "--",
            "sh",
            "-s",
            "--",
            host_workspace,
            host_input,
            host_resources,
            stage,
            self.runtime_root,
            self.runtime_python,
            trace_source,
        ]
        try:
            completed = subprocess.run(
                command,
                input=wrapper.encode("utf-8"),
                capture_output=True,
                timeout=timeout + 10,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            return ExecutionResult(
                command=command,
                cwd=workspace,
                exit_code=124,
                stdout=_decode_output(exc.stdout),
                stderr=_decode_output(exc.stderr) + f"\nTimed out after {timeout} seconds.",
                duration_seconds=perf_counter() - start,
                timed_out=True,
                sandbox_backend="wsl-bwrap",
                sandboxed=True,
                sandbox_policy_version="wsl-bwrap-v1",
                sandbox_capabilities=_WSL_BWRAP_CAPABILITIES,
                sandbox_mounts=_sandbox_mounts(has_input=input_path is not None, has_resources=bool(host_resources)),
                sandbox_limits={"cpu_seconds": timeout, "memory_kib": self.memory_limit_kib},
                sandbox_termination_reason="timeout",
                sandbox_event={"code": "sandbox_timeout", "message": f"timed out after {timeout} seconds"},
            )
        duration = perf_counter() - start
        trace_path = workspace / "intermediates" / "provenance-input-access.log"
        coverage, accesses = _read_provenance_trace(trace_path) if trace_input_access else (False, None)
        return ExecutionResult(
            command=["wsl.exe", "-d", self.distro, "--", "bwrap", "build_sequence.py"],
            cwd=workspace,
            exit_code=completed.returncode,
            stdout=_decode_output(completed.stdout),
            stderr=_decode_output(completed.stderr),
            duration_seconds=duration,
            timed_out=False,
            sandbox_backend="wsl-bwrap",
            sandboxed=True,
            sandbox_policy_version="wsl-bwrap-v1",
            sandbox_capabilities=_WSL_BWRAP_CAPABILITIES,
            sandbox_mounts=_sandbox_mounts(has_input=input_path is not None, has_resources=bool(host_resources)),
            sandbox_limits={"cpu_seconds": timeout, "memory_kib": self.memory_limit_kib},
            sandbox_termination_reason="completed" if completed.returncode == 0 else "script_error",
            sandbox_event=_classify_sandbox_event(completed.returncode, _decode_output(completed.stderr)),
            provenance_trace_path=str(trace_path) if trace_input_access and trace_path.is_file() else None,
            provenance_input_accesses=accesses,
            provenance_coverage=coverage,
        )

    def _wsl_path(self, path: Path) -> str | None:
        resolved = path.resolve()
        drive = resolved.drive.rstrip(":")
        if len(drive) != 1:
            return None
        text = resolved.as_posix()
        if len(text) < 3 or text[1:3] != ":/":
            return None
        return f"/mnt/{drive.lower()}{text[2:]}"


def _sandbox_error(start: float, message: str) -> ExecutionResult:
    return ExecutionResult(
        command=[],
        cwd=Path(),
        exit_code=125,
        stdout="",
        stderr=message,
        duration_seconds=perf_counter() - start,
        sandbox_backend="unavailable",
        sandboxed=False,
        sandbox_capabilities={"filesystem_isolation": False, "network_isolation": False},
        sandbox_termination_reason="unavailable",
        sandbox_event={"code": "sandbox_unavailable", "message": message},
    )


def _decode_output(value: bytes | str | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace").replace("\ufffd", "?")
    return value


def _read_provenance_trace(path: Path) -> tuple[bool, list[str]]:
    if not path.is_file():
        return False, []
    lines = [line.strip() for line in path.read_text(encoding="utf-8", errors="replace").splitlines() if line.strip()]
    return "coverage=active" in lines, [line for line in lines if " path=/input/" in line]


def _wsl_wrapper_script(*, timeout: int, memory_limit_kib: int) -> str:
    return f'''#!/bin/sh
set -eu
host_workspace="$1"
host_input="$2"
host_resources="$3"
stage="$4"
runtime_root="$5"
runtime_python="$6"
trace_source="$7"
umask 077
mkdir -p "$stage/output" "$stage/intermediates" "$stage/input" "$stage/resources"
trap 'rm -rf "$stage"' EXIT
cp "$host_workspace/build_sequence.py" "$stage/build_sequence.py"
if [ -n "$trace_source" ]; then
  gcc -shared -fPIC -O2 -o "$stage/provenance.so" "$trace_source" -ldl
fi
if [ -n "$host_input" ]; then
  cp "$host_input" "$stage/input/model.step"
fi
if [ -n "$host_resources" ]; then
  cp -a "$host_resources/." "$stage/resources/"
fi
ulimit -t {timeout}
ulimit -v {memory_limit_kib}
bwrap --unshare-all --die-with-parent --new-session --clearenv \\
  --setenv PATH /runtime/bin:/usr/bin:/bin --setenv LANG C.UTF-8 \\
  $([ -n "$trace_source" ] && printf '%s' '--setenv LD_PRELOAD /workspace/provenance.so --setenv BREP2CODE_PROVENANCE_TRACE /workspace/intermediates/provenance-input-access.log ') \\
  --ro-bind /usr /usr --ro-bind /bin /bin --ro-bind /lib /lib --ro-bind /lib64 /lib64 --ro-bind /etc /etc \\
  --ro-bind "$runtime_root" /runtime --ro-bind "$stage" /workspace --ro-bind "$stage/input" /input --ro-bind "$stage/resources" /resources \\
  --bind "$stage/output" /workspace/output --bind "$stage/intermediates" /workspace/intermediates \\
  --proc /proc --dev /dev --chdir /workspace -- /runtime/bin/python build_sequence.py
cp -a "$stage/output/." "$host_workspace/output/"
cp -a "$stage/intermediates/." "$host_workspace/intermediates/"
'''


_WSL_BWRAP_CAPABILITIES = {
    "filesystem_isolation": True,
    "network_isolation": True,
    "sanitized_environment": True,
    "readonly_input_mount": True,
    "writable_output_mount": True,
    "writable_intermediates_mount": True,
}


def _sandbox_mounts(*, has_input: bool, has_resources: bool) -> list[str]:
    mounts = ["/workspace:ro", "/workspace/output:rw", "/workspace/intermediates:rw"]
    if has_input:
        mounts.append("/input/model.step:ro")
    if has_resources:
        mounts.append("/resources:ro")
    return mounts


def _classify_sandbox_event(exit_code: int, stderr: str) -> dict[str, str] | None:
    if exit_code == 0:
        return None
    denied_markers = ("PermissionError", "Permission denied", "Read-only file system")
    if any(marker in stderr for marker in denied_markers):
        return {
            "code": "sandbox_policy_violation",
            "message": "script attempted an operation denied by the sandbox policy",
        }
    return None
