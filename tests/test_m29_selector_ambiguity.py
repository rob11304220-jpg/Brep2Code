from __future__ import annotations

import json
from pathlib import Path

from tools.build_m29_selector_ambiguity_candidates import (
    EXPANSION,
    apply_mutation,
    build,
    build_shape,
    canonical_sequence,
    control_result,
    load_json,
    selector_result,
)


def test_m29_preregistration_has_two_fail_closed_rows() -> None:
    record = load_json(EXPANSION)
    assert [row["data_split"] for row in record["cases"]] == ["development", "held_out"]
    for row in record["cases"]:
        shape = build_shape(row)
        assert selector_result(shape, row) == {"cardinality": 2, "status": "ambiguous"}
        assert control_result(shape, row, "wrong-face-injection") == {"accepted": "false", "reason": "selector_ambiguity"}
        assert control_result(shape, row, "coordinate-tie-breaker-injection") == {"accepted": "false", "reason": "coordinate_only_support"}
        assert [operation["kind"] for operation in canonical_sequence(row)["operations"]][-1] == "FailClosedAmbiguous"


def test_m29_mutations_preserve_ambiguity() -> None:
    record = load_json(EXPANSION)
    for row in record["cases"]:
        for mutation in row["mutations"]:
            mutated = apply_mutation(row, mutation)
            assert selector_result(build_shape(mutated), mutated) == {"cardinality": 2, "status": "ambiguous"}


def test_m29_build_writes_experimental_candidates(tmp_path: Path) -> None:
    produced = build(output_root=tmp_path)
    assert produced == ["param_selector_ambiguity_twin_centered_nominal", "param_selector_ambiguity_twin_offset_nominal"]
    for row in load_json(EXPANSION)["cases"]:
        case = json.loads((tmp_path / row["candidate_directory"] / "case.json").read_text(encoding="utf-8"))
        assert case["status"] == "experimental"
        assert case["sequence_pair"]["selector_result"] == {"cardinality": 2, "status": "ambiguous"}
