from __future__ import annotations

import pytest

from tools.fusion360_line3d_selector import select_signed_axis
from tools.replay_fusion360_m14 import replay


def _projection(minimum: float, maximum: float) -> dict[str, float]:
    return {"min": minimum, "max": maximum, "span": maximum - minimum}


def test_selector_chooses_the_unique_profile_normal_axis_at_the_lower_boundary() -> None:
    result = select_signed_axis(
        ordered_profile_normal=(0.0, 0.0, 1.0),
        sketch_axes={"x": (1.0, 0.0, 0.0), "y": (0.0, 1.0, 0.0), "z": (0.0, 0.0, 1.0)},
        profile_projections={"x": _projection(0.0, 2.0), "y": _projection(0.0, 3.0), "z": _projection(4.0, 4.0)},
        step_projections={"x": _projection(0.0, 2.0), "y": _projection(0.0, 3.0), "z": _projection(4.0, 9.0)},
        extent_magnitude_mm=5.0,
    )

    assert result == "+z_axis"


def test_selector_rejects_ambiguous_matching_axes_without_a_fallback() -> None:
    with pytest.raises(ValueError, match="selector_not_unique_axis"):
        select_signed_axis(
            ordered_profile_normal=(0.0, 0.0, 1.0),
            sketch_axes={"first": (0.0, 0.0, 1.0), "second": (0.0, 0.0, -1.0)},
            profile_projections={"first": _projection(0.0, 0.0), "second": _projection(0.0, 0.0)},
            step_projections={"first": _projection(0.0, 5.0), "second": _projection(0.0, 5.0)},
            extent_magnitude_mm=5.0,
        )


def test_selector_chooses_negative_axis_when_profile_is_at_upper_boundary() -> None:
    result = select_signed_axis(
        ordered_profile_normal=(0.0, 1.0, 0.0),
        sketch_axes={"x": (1.0, 0.0, 0.0), "y": (0.0, 1.0, 0.0), "z": (0.0, 0.0, 1.0)},
        profile_projections={"x": _projection(0.0, 2.0), "y": _projection(9.0, 9.0), "z": _projection(0.0, 3.0)},
        step_projections={"x": _projection(0.0, 2.0), "y": _projection(4.0, 9.0), "z": _projection(0.0, 3.0)},
        extent_magnitude_mm=5.0,
    )

    assert result == "-y_axis"


def test_default_line3d_replay_fails_closed_without_the_input_bbox() -> None:
    payload = {
        "entities": {
            "sketch": {
                "profiles": {
                    "profile": {
                        "loops": [
                            {"is_outer": True, "profile_curves": [{"type": "Line3D"}]}
                        ]
                    }
                }
            },
            "extrude": {"type": "ExtrudeFeature"},
        },
        "timeline": [{"entity": "sketch"}, {"entity": "extrude"}],
    }

    with pytest.raises(ValueError, match="Line3D selector requires input bbox"):
        replay(payload)
