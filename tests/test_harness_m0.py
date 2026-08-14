from pathlib import Path

from brep2code.agent.harness import ManualHarness
from brep2code.storage import RecordStore


def test_manual_harness_creates_passing_revision(tmp_path: Path) -> None:
    harness = ManualHarness(store=RecordStore(tmp_path))

    result = harness.run("demo")

    assert result.status == "pass"
    assert result.record.manifest.exists()
    assert (result.revision.workspace / "build_sequence.py").exists()
    assert (result.revision.output / "model.step").exists()
    assert (result.revision.traces / "stdout.txt").exists()
    assert (result.revision.traces / "stderr.txt").exists()
    assert result.revision.execution_summary.exists()
    assert result.revision.signal_bundle.exists()
    assert result.signal_bundle["execution"]["sandbox_backend"] == "unsafe-local"
    assert result.signal_bundle["execution"]["sandboxed"] is False


def test_manual_harness_preserves_failed_revision(tmp_path: Path) -> None:
    script = tmp_path / "broken_build.py"
    script.write_text("raise RuntimeError('boom')\n", encoding="utf-8")
    harness = ManualHarness(store=RecordStore(tmp_path / "data"))

    result = harness.run("broken", script=script)

    assert result.status == "fail"
    assert result.revision.signal_bundle.exists()
    assert (result.revision.traces / "stderr.txt").read_text(encoding="utf-8")
    assert not (result.revision.output / "model.step").exists()
