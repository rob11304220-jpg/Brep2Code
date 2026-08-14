"""Pure, bounded selector for the M17 fixed Fusion Line3D promotion test."""

from __future__ import annotations

import math
from collections.abc import Mapping


TOLERANCE = 1e-6


def _dot(left: tuple[float, float, float], right: tuple[float, float, float]) -> float:
    return sum(component_left * component_right for component_left, component_right in zip(left, right, strict=True))


def _norm(vector: tuple[float, float, float]) -> float:
    return math.sqrt(_dot(vector, vector))


def _normalized(vector: tuple[float, float, float]) -> tuple[float, float, float]:
    length = _norm(vector)
    if length <= TOLERANCE:
        raise ValueError("selector_zero_length_vector")
    return tuple(component / length for component in vector)


def select_signed_axis(
    *,
    ordered_profile_normal: tuple[float, float, float],
    sketch_axes: Mapping[str, tuple[float, float, float]],
    profile_projections: Mapping[str, Mapping[str, float]],
    step_projections: Mapping[str, Mapping[str, float]],
    extent_magnitude_mm: float,
) -> str:
    """Return the uniquely evidenced signed axis, otherwise reject without fallback."""
    normal = _normalized(ordered_profile_normal)
    candidates = [
        name
        for name, axis in sketch_axes.items()
        if abs(abs(_dot(normal, _normalized(axis))) - 1.0) <= TOLERANCE
        and abs(step_projections[name]["span"] - extent_magnitude_mm) <= TOLERANCE
        and abs(profile_projections[name]["span"]) <= TOLERANCE
    ]
    if len(candidates) != 1:
        raise ValueError(f"selector_not_unique_axis: {candidates}")

    axis = candidates[0]
    profile, step = profile_projections[axis], step_projections[axis]
    if abs(profile["min"] - step["min"]) <= TOLERANCE:
        return f"+{axis}_axis"
    if abs(profile["max"] - step["max"]) <= TOLERANCE:
        return f"-{axis}_axis"
    raise ValueError("selector_profile_not_on_step_projection_boundary")
