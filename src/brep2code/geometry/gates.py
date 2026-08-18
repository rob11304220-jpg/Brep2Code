from __future__ import annotations

from dataclasses import asdict, dataclass
from math import isclose
from typing import Any, Callable

from brep2code.domain import Signal, SignalBundle
from brep2code.geometry.inspect import GeometryMetrics


@dataclass(frozen=True)
class GateResult:
    gate_id: str
    passed: bool
    message: str


@dataclass(frozen=True)
class GateReport:
    passed: bool
    summary: str
    required_gates: tuple[str, ...]
    results: tuple[GateResult, ...]

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)

    def as_signal_bundle(self) -> SignalBundle:
        return SignalBundle(
            passed=self.passed,
            summary=self.summary,
            signals=tuple(
                Signal(result.gate_id, result.message, result.passed)
                for result in self.results
            ),
        )


class GateDispatchError(ValueError):
    """Raised when a dossier names an unavailable or invalid gate."""


GateHandler = Callable[[GeometryMetrics, dict[str, Any], dict[str, Any], dict[str, Any]], GateResult]


def dispatch_gates(
    metrics: GeometryMetrics,
    expected: dict[str, Any],
    required_gates: tuple[str, ...] | list[str],
    *,
    observations: dict[str, Any] | None = None,
    gate_oracles: dict[str, Any] | None = None,
) -> GateReport:
    gate_ids = tuple(required_gates)
    if not gate_ids or len(gate_ids) != len(set(gate_ids)):
        raise GateDispatchError("required_gates must contain unique non-empty gate IDs")
    results = []
    observations = observations or {}
    gate_oracles = gate_oracles or {}
    for gate_id in gate_ids:
        handler = _GATE_HANDLERS.get(gate_id)
        if handler is None:
            raise GateDispatchError(f"unknown required gate {gate_id!r}")
        results.append(handler(metrics, expected, observations, gate_oracles.get(gate_id, {})))
    passed = all(result.passed for result in results)
    return GateReport(
        passed=passed,
        summary="all gates passed" if passed else "one or more gates failed",
        required_gates=gate_ids,
        results=tuple(results),
    )


def _bbox_gate(
    metrics: GeometryMetrics,
    expected: dict[str, Any],
    observations: dict[str, Any],
    oracle: dict[str, Any],
) -> GateResult:
    del observations, oracle
    target = expected["bbox"]
    passed = _vectors_close(metrics.bbox_min, target["min"]) and _vectors_close(
        metrics.bbox_max, target["max"]
    )
    return GateResult("bbox", passed, "bounding box matches" if passed else "bounding box differs")


def _volume_gate(
    metrics: GeometryMetrics,
    expected: dict[str, Any],
    observations: dict[str, Any],
    oracle: dict[str, Any],
) -> GateResult:
    del observations, oracle
    passed = isclose(metrics.volume, expected["volume"], rel_tol=1e-7, abs_tol=1e-6)
    return GateResult("volume", passed, "volume matches" if passed else "volume differs")


def _topology_gate(
    metrics: GeometryMetrics,
    expected: dict[str, Any],
    observations: dict[str, Any],
    oracle: dict[str, Any],
) -> GateResult:
    del observations, oracle
    passed = metrics.counts == expected["counts"]
    return GateResult("topology", passed, "topology matches" if passed else "topology differs")


def _semantic_gate(
    metrics: GeometryMetrics,
    expected: dict[str, Any],
    observations: dict[str, Any],
    oracle: dict[str, Any],
) -> GateResult:
    del metrics, expected
    faces = [face for face in observations.get("faces", []) if face.get("surface") == oracle.get("surface")]
    passed = len(faces) == 1
    if passed:
        face = faces[0]
        passed = isclose(face.get("radius", -1), oracle["radius"], rel_tol=1e-7, abs_tol=1e-6)
        passed = passed and _vectors_close(face.get("axis_direction", ()), oracle["axis_direction"])
    return GateResult("semantic", passed, "analytic surface matches" if passed else "analytic surface differs")


def _adjacency_gate(
    metrics: GeometryMetrics,
    expected: dict[str, Any],
    observations: dict[str, Any],
    oracle: dict[str, Any],
) -> GateResult:
    del metrics, expected
    faces = [face for face in observations.get("faces", []) if face.get("surface") == oracle.get("surface")]
    passed = len(faces) == 1
    if passed:
        extent_axis = int(oracle["axis"])
        bbox = faces[0]["bbox"]
        passed = _close(bbox["min"][extent_axis], oracle["extent_min"])
        passed = passed and _close(bbox["max"][extent_axis], oracle["extent_max"])
    return GateResult("adjacency", passed, "feature adjacency matches" if passed else "feature adjacency differs")


def _vectors_close(actual: tuple[float, ...], expected: list[float]) -> bool:
    return all(
        isclose(left, right, rel_tol=1e-7, abs_tol=1e-6)
        for left, right in zip(actual, expected, strict=True)
    )


_GATE_HANDLERS: dict[str, GateHandler] = {
    "bbox": _bbox_gate,
    "volume": _volume_gate,
    "topology": _topology_gate,
    "semantic": _semantic_gate,
    "adjacency": _adjacency_gate,
}


def _close(actual: float, expected: float) -> bool:
    return isclose(actual, expected, rel_tol=1e-7, abs_tol=1e-6)
