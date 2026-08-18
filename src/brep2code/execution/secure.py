from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
from time import perf_counter
from uuid import uuid4

from brep2code.execution.local import ExecutionResult


class SandboxUnavailable(RuntimeError):
    pass


def secure_backend_status() -> tuple[bool, str]:
    """Return a read-only readiness result for the configured WSL backend."""
    if shutil.which("wsl.exe") is None and shutil.which("wsl") is None:
        return False, "secure execution backend unavailable: wsl.exe not found"
    command = [
        "wsl.exe",
        "-d",
        "Ubuntu-24.04",
        "--",
        "sh",
        "-lc",
        "command -v bwrap >/dev/null && command -v prlimit >/dev/null && "
        "command -v timeout >/dev/null && test -x /home/liaol/.brep2code-runtime/bin/python",
    ]
    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            timeout=10,
            check=False,
            env=_wsl_environment(),
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False, "secure execution backend unavailable: WSL2 probe failed"
    stdout = _decode(completed.stdout)
    stderr = _decode(completed.stderr)
    if _is_wsl_backend_failure(completed.returncode, stdout, stderr):
        return False, "secure execution backend unavailable: WSL2 service or distro access failed"
    if completed.returncode != 0:
        return False, "secure execution backend unavailable: bwrap/runtime prerequisites missing"
    return True, "secure execution backend ready"


def run_untrusted_build(
    workspace: Path,
    *,
    timeout_seconds: int = 30,
    memory_limit_mib: int = 2048,
    output_limit_bytes: int = 16 * 1024 * 1024,
) -> ExecutionResult:
    """Run generated code in the verified WSL2/bubblewrap boundary."""

    workspace = workspace.resolve()
    script = workspace / "build.py"
    if not workspace.is_dir() or not script.is_file():
        raise ValueError("revision workspace must contain build.py")
    if timeout_seconds < 1 or memory_limit_mib < 64 or output_limit_bytes < 1024:
        raise ValueError("sandbox limits must be positive and bounded")
    if shutil.which("wsl.exe") is None and shutil.which("wsl") is None:
        raise SandboxUnavailable("secure execution backend unavailable: wsl.exe not found")

    stage = f"/tmp/brep2code-v2/{uuid4().hex}"
    host_workspace = _wsl_path(workspace)
    file_limit_blocks = max(3, (output_limit_bytes + 511) // 512 + 1)
    wrapper = _wrapper_script(
        timeout_seconds=timeout_seconds,
        memory_limit_kib=memory_limit_mib * 1024,
        file_limit_blocks=file_limit_blocks,
        output_limit_bytes=output_limit_bytes,
    )
    command = [
        "wsl.exe",
        "-d",
        "Ubuntu-24.04",
        "--",
        "sh",
        "-s",
        "--",
        host_workspace,
        stage,
        "/home/liaol/.brep2code-runtime",
    ]
    started = perf_counter()
    try:
        completed = subprocess.run(
            command,
            input=wrapper.encode("utf-8"),
            capture_output=True,
            timeout=timeout_seconds + 10,
            check=False,
            env=_wsl_environment(),
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        raise SandboxUnavailable(
            "secure execution backend unavailable; refusing to run untrusted generated code"
        ) from exc

    stdout = _decode(completed.stdout)
    stderr = _decode(completed.stderr)
    if _is_wsl_backend_failure(completed.returncode, stdout, stderr):
        raise SandboxUnavailable(
            "secure execution backend unavailable: WSL2 service or distro access failed; "
            "run the local WSL diagnostics from docs/development.md"
        )
    if completed.returncode == 125 and "sandbox_unavailable:" in stderr:
        raise SandboxUnavailable(stderr.strip())
    timed_out = completed.returncode in {124, 137, 152}
    output = workspace / "output.step"
    return ExecutionResult(
        exit_code=completed.returncode,
        stdout=stdout,
        stderr=stderr,
        duration_seconds=perf_counter() - started,
        output_step=output if completed.returncode == 0 and output.is_file() else None,
        timed_out=timed_out,
        sandboxed=True,
        sandbox_backend="wsl-bwrap",
        termination_reason=(
            "timeout"
            if timed_out
            else "completed"
            if completed.returncode == 0
            else "output_limit"
            if completed.returncode == 153
            else "script_error"
        ),
    )


def _decode(value: bytes | None) -> str:
    raw = value or b""
    if raw.count(b"\x00") > max(1, len(raw) // 10):
        try:
            return raw.decode("utf-16-le", errors="replace").replace("\x00", "")
        except UnicodeError:
            pass
    return raw.decode("utf-8", errors="replace").replace("\x00", "")


def _is_wsl_backend_failure(returncode: int, stdout: str, stderr: str) -> bool:
    """Recognize launcher/service failures before treating output as script feedback."""
    if returncode in {-1, 0xFFFFFFFF, 0x80070005}:
        return True
    message = f"{stdout}\n{stderr}".lower().replace(" ", "")
    return "wsl/" in message and any(
        marker in message for marker in ("accessdenied", "enumeratedistros", "service/")
    )


def _wsl_path(path: Path) -> str:
    drive = path.drive.rstrip(":")
    text = path.as_posix()
    if len(drive) != 1 or len(text) < 3 or text[1:3] != ":/":
        raise ValueError("workspace must be on a Windows drive visible to WSL")
    return f"/mnt/{drive.lower()}{text[2:]}"


def _wsl_environment() -> dict[str, str]:
    allowed = ("PATH", "SYSTEMROOT", "WINDIR", "WSLENV")
    return {name: os.environ[name] for name in allowed if name in os.environ}


def _wrapper_script(
    *,
    timeout_seconds: int,
    memory_limit_kib: int,
    file_limit_blocks: int,
    output_limit_bytes: int,
) -> str:
    return f"""#!/bin/sh
set -u
host_workspace="$1"
stage="$2"
runtime_root="$3"
runtime_python="$runtime_root/bin/python"
if ! command -v bwrap >/dev/null 2>&1 || [ ! -x "$runtime_python" ]; then
  echo "sandbox_unavailable: bwrap or runtime Python missing" >&2
  exit 125
fi
umask 077
mkdir -p "$stage/workspace" "$stage/root/usr" "$stage/root/bin" \
  "$stage/root/lib" "$stage/root/lib64" "$stage/root/etc" \
  "$stage/root/runtime" "$stage/root/workspace" "$stage/root/proc" "$stage/root/dev"
touch "$stage/output.step" "$stage/workspace/output.step"
trap 'rm -rf "$stage"' EXIT HUP INT TERM
cp "$host_workspace/build.py" "$stage/workspace/build.py"
(
  ulimit -t {timeout_seconds}
  ulimit -v {memory_limit_kib}
  ulimit -f {file_limit_blocks}
  exec prlimit --nproc=64:64 -- timeout -k 2 {timeout_seconds}s bwrap \
    --unshare-all --die-with-parent --new-session --clearenv \
    --setenv PATH /runtime/bin:/usr/bin:/bin --setenv LANG C.UTF-8 \
    --ro-bind "$stage/root" / \
    --ro-bind /usr /usr --ro-bind /bin /bin --ro-bind /lib /lib \
    --ro-bind /lib64 /lib64 --ro-bind /etc /etc \
    --ro-bind "$runtime_root" /runtime \
    --ro-bind "$stage/workspace" /workspace \
    --bind "$stage/output.step" /workspace/output.step \
    --proc /proc --dev /dev --chdir /workspace \
    -- /runtime/bin/python build.py
) >"$stage/stdout.log" 2>"$stage/stderr.log"
status=$?
if [ -s "$stage/output.step" ]; then
  size=$(stat -c %s "$stage/output.step")
  if [ "$size" -gt {output_limit_bytes} ]; then
    echo "sandbox output limit exceeded" >>"$stage/stderr.log"
    status=153
  elif [ "$status" -eq 0 ]; then
    cp "$stage/output.step" "$host_workspace/output.step"
  fi
fi
head -c {output_limit_bytes} "$stage/stdout.log"
head -c {output_limit_bytes} "$stage/stderr.log" >&2
exit "$status"
"""
