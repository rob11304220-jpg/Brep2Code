from __future__ import annotations

import json
from pathlib import Path

import pytest

from brep2code.cases import load_manifest
from brep2code.evaluation import write_evaluation_summary
from brep2code.harness import RepairLoopRunner
from brep2code.providers import FakeProvider


pytestmark = pytest.mark.secure


def test_frozen_eval_case_produces_json_and_markdown_summary(tmp_path: Path) -> None:
    manifest = load_manifest(Path("cases/manifests/eval.json"), Path("cases"))
    assert manifest.split == "eval"
    case = manifest.cases[0]
    script = Path("tests/fixtures/fixed_cylinder.py").read_text(encoding="utf-8")
    result = RepairLoopRunner(FakeProvider([script])).run(
        case, tmp_path / "runs" / case.case.case_id, max_rounds=1
    )
    result_payload = json.loads(result.result_path.read_text(encoding="utf-8"))

    summary = write_evaluation_summary(
        [result_payload], tmp_path / "evaluation.json", tmp_path / "evaluation.md"
    )

    assert summary["counts"] == {"pass": 1}
    assert summary["mechanism_report"] == [
        {
            "mechanism": "analytic_surface",
            "capability_level": "L0",
            "case_ids": ["cylinder"],
            "case_count": 1,
            "status_counts": {"succeeded": 1},
            "classification_counts": {"pass": 1},
        }
    ]
    assert (tmp_path / "evaluation.json").is_file()
    markdown = (tmp_path / "evaluation.md").read_text(encoding="utf-8")
    assert "| cylinder | succeeded | pass | 1 |" in markdown
