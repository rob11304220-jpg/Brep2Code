from __future__ import annotations

from typing import Any

from brep2code.domain import SignalBundle
from brep2code.geometry.gates import dispatch_gates
from brep2code.geometry.inspect import GeometryMetrics


def compare_geometry(
    metrics: GeometryMetrics,
    expected: dict[str, Any],
    required_gates: tuple[str, ...] | list[str] = ("bbox", "volume", "topology"),
) -> SignalBundle:
    return dispatch_gates(metrics, expected, required_gates).as_signal_bundle()
