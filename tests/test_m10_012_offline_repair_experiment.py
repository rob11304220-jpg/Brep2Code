from pathlib import Path


FIXTURE_ROOT = Path(__file__).parent / "fixtures" / "sandbox"


def test_m10_012_fixed_scripts_keep_the_path_and_import_hypotheses_separate() -> None:
    baseline = (FIXTURE_ROOT / "m10_012_host_path_roundtrip.py").read_text(encoding="utf-8")
    treatment = (FIXTURE_ROOT / "m10_012_sandbox_path_roundtrip.py").read_text(encoding="utf-8")
    control = (FIXTURE_ROOT / "m10_012_import_control.py").read_text(encoding="utf-8")

    assert "input_path = r" in baseline
    assert "m10-012-host-only" in baseline
    assert 'input_path = "/input/model.step"' in treatment
    assert 'input_path = "/input/model.step"' in control
    assert "Interface_Static_SetCVal" in control
    assert "output/model.step" in baseline
    assert "output/model.step" in treatment
