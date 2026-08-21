from pathlib import Path

import pytest

from brep2code.execution import run_untrusted_build
from brep2code.geometry.inspect import inspect_step


pytestmark = pytest.mark.secure


@pytest.mark.parametrize(
    ("hostile_source", "expected_reason"),
    [
        ("from pathlib import Path; Path('../escaped.txt').write_text('bad')", "script_error"),
        (
            "import os; assert 'BREP2CODE_TEST_SECRET' not in os.environ",
            "completed",
        ),
        (
            "import socket; s=socket.socket(); s.settimeout(1); "
            "assert s.connect_ex(('1.1.1.1', 53)) != 0",
            "completed",
        ),
        ("while True: pass", "timeout"),
    ],
)
def test_untrusted_scripts_are_isolated(
    tmp_path: Path, hostile_source: str, expected_reason: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    workspace = tmp_path / "revision"
    workspace.mkdir()
    (workspace / "build.py").write_text(hostile_source, encoding="utf-8")

    monkeypatch.setenv("BREP2CODE_TEST_SECRET", "not-a-secret")
    result = run_untrusted_build(workspace, timeout_seconds=1)
    assert result.sandboxed is True
    assert result.sandbox_backend == "wsl-bwrap"
    assert result.termination_reason == expected_reason
    assert not (tmp_path / "escaped.txt").exists()


def test_descendant_and_output_are_bounded(tmp_path: Path) -> None:
    workspace = tmp_path / "revision"
    workspace.mkdir()
    (workspace / "build.py").write_text(
        "import subprocess\n"
        "subprocess.Popen(['/bin/sh', '-c', 'sleep 2; echo bad > output.step'])\n"
        "open('output.step', 'wb').write(b'x' * 4096)\n",
        encoding="utf-8",
    )

    result = run_untrusted_build(workspace, timeout_seconds=1, output_limit_bytes=1024)
    assert result.termination_reason in {"output_limit", "script_error"}
    assert result.output_step is None
    assert not (workspace / "output.step").exists()


def test_memory_and_process_creation_are_bounded(tmp_path: Path) -> None:
    memory_workspace = tmp_path / "memory"
    memory_workspace.mkdir()
    (memory_workspace / "build.py").write_text(
        "bytearray(256 * 1024 * 1024)", encoding="utf-8"
    )
    memory = run_untrusted_build(memory_workspace, memory_limit_mib=64)
    assert memory.termination_reason == "script_error"

    process_workspace = tmp_path / "processes"
    process_workspace.mkdir()
    (process_workspace / "build.py").write_text(
        "import subprocess\n"
        "children = []\n"
        "for _ in range(128):\n"
        "    try:\n"
        "        children.append(subprocess.Popen(['/bin/sleep', '10']))\n"
        "    except OSError:\n"
        "        break\n"
        "else:\n"
        "    raise RuntimeError('process limit was not enforced')\n",
        encoding="utf-8",
    )
    processes = run_untrusted_build(process_workspace, timeout_seconds=3)
    assert processes.exit_code == 0, processes.stderr


def test_ocp_build_produces_readable_step(tmp_path: Path) -> None:
    workspace = tmp_path / "cad"
    workspace.mkdir()
    source = Path("tests/fixtures/fixed_box.py").read_text(encoding="utf-8")
    (workspace / "build.py").write_text(source, encoding="utf-8")

    result = run_untrusted_build(workspace)
    assert result.exit_code == 0, result.stderr
    assert result.output_step is not None
    metrics = inspect_step(result.output_step)
    assert metrics.volume == pytest.approx(6000.0)


def test_cadquery_build_produces_readable_step(tmp_path: Path) -> None:
    workspace = tmp_path / "cadquery"
    workspace.mkdir()
    source = Path("tests/fixtures/fixed_cadquery_box.py").read_text(encoding="utf-8")
    (workspace / "build.py").write_text(source, encoding="utf-8")

    result = run_untrusted_build(workspace)
    assert result.exit_code == 0, result.stderr
    assert result.output_step is not None
    metrics = inspect_step(result.output_step)
    assert metrics.volume == pytest.approx(6000.0)
