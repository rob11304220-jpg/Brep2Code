from __future__ import annotations

from pathlib import Path

import pytest

from tools.audit_blind_through_observability import audit


CASES = Path("case-library/self-authored")


@pytest.mark.parametrize(
    ("case_id", "expected"),
    [
        ("param_through_hole_low", "through"),
        ("param_through_hole_nominal", "through"),
        ("param_through_hole_high", "through"),
        ("param_blind_hole_low", "blind"),
        ("param_blind_hole_nominal", "blind"),
        ("param_blind_hole_high", "blind"),
    ],
)
def test_frozen_prismatic_hole_oracles_are_classified_from_measured_facts(case_id: str, expected: str) -> None:
    assert audit(CASES / case_id / "input.step")["classification"] == expected


def test_counterbore_is_not_collapsed_to_blind_or_through() -> None:
    result = audit(CASES / "param_counterbore_nominal" / "input.step")
    assert result["classification"] == "unsupported"
    assert result["reason"] == "requires_exactly_one_cylindrical_face"


def test_report_exposes_terminal_measurements_not_reference_labels() -> None:
    result = audit(CASES / "param_blind_hole_nominal" / "input.step")
    fact = result["cylindrical_faces"][0]
    assert fact["axis"] == [0.0, 0.0, 1.0]
    assert len(fact["adjacent_planar_faces"]) == 2
    assert {item["local_footprint"] for item in fact["adjacent_planar_faces"]} == {False, True}
