from __future__ import annotations

import json
from pathlib import Path

from tools.evaluate_m157_selector_ambiguity_projection import evaluate


def test_m157_ablation_is_fixed_local_and_explicitly_selects_one_card() -> None:
    result = evaluate()

    assert result["case_scope"] == [
        "param_face_selected_cut_centered_nominal",
        "param_selector_ambiguity_twin_centered_nominal",
    ]
    assert result["held_out_access"] == "not_performed"
    assert result["provider_requests"] == 0
    assert result["ablation_budget"] == 3
    assert result["arms"] == {
        "no_reference": {"ok": False, "error_code": "guidance_not_enabled"},
        "wrong_reference": {"ok": True, "returned_card_id": "vertical-cylinder-construction"},
        "explicit_reference": {"ok": True, "returned_card_id": "selector-cardinality-stop"},
    }


def test_m157_projection_record_binds_the_evaluated_artifacts() -> None:
    root = Path(__file__).resolve().parents[1]
    record = json.loads(
        (root / "docs/corpus/knowledge/runtime-projections/selector-cardinality-stop-v1.json").read_text(
            encoding="utf-8"
        )
    )
    result = evaluate()

    assert record["status"] == "experimental_offline_only"
    assert record["source"]["admission_record_sha256"] == result["source_record_sha256"]
    assert record["selected_projection"]["card_sha256"] == result["projection_card_sha256"]
    assert record["selected_projection"]["index_sha256"] == result["index_sha256"]
    assert record["offline_ablation"]["budget"] == result["ablation_budget"]
