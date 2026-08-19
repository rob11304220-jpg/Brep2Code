from __future__ import annotations

from dataclasses import asdict
from typing import Any

from brep2code.cases import ValidatedCase
from brep2code.domain import SignalBundle
from brep2code.geometry.gates import GateDispatchError
from brep2code.geometry.inspect import GeometryMetrics


def geometry_feedback(
    metrics: GeometryMetrics, target: dict[str, Any], signals: SignalBundle
) -> dict[str, Any]:
    actual = {
        "bbox": {"min": list(metrics.bbox_min), "max": list(metrics.bbox_max)},
        "volume": metrics.volume,
        "counts": metrics.counts,
    }
    return {
        "stage": "geometry",
        "summary": signals.summary,
        "actual": actual,
        "differences_from_brep": {
            "bbox_min": [
                actual_value - target_value
                for actual_value, target_value in zip(
                    metrics.bbox_min, target["bbox"]["min"], strict=True
                )
            ],
            "bbox_max": [
                actual_value - target_value
                for actual_value, target_value in zip(
                    metrics.bbox_max, target["bbox"]["max"], strict=True
                )
            ],
            "volume": metrics.volume - target["volume"],
            "counts": {
                name: metrics.counts[name] - target["topology"][name]
                for name in target["topology"]
            },
        },
        "signals": asdict(signals),
    }


def required_gates(case: ValidatedCase) -> tuple[str, ...]:
    if case.verifier is not None:
        gates = case.verifier.get("gates", {}).get("required")
        if not isinstance(gates, list):
            raise GateDispatchError("verifier pack gates.required must be an array")
        return tuple(gates)
    if case.dossier is None:
        return ("bbox", "volume", "topology")
    harness_assets = case.dossier.get("harness_assets")
    if not isinstance(harness_assets, dict):
        raise GateDispatchError("case dossier harness_assets must be an object")
    gates = harness_assets.get("required_gates")
    if not isinstance(gates, list):
        raise GateDispatchError("case dossier required_gates must be an array")
    return tuple(gates)


def gate_oracles(case: ValidatedCase) -> dict[str, Any]:
    if case.verifier is not None:
        gates = case.verifier.get("gates", {}).get("oracles")
        if not isinstance(gates, dict):
            raise GateDispatchError("verifier pack gates.oracles must be an object")
        return gates
    if case.dossier is None:
        return {}
    harness_assets = case.dossier.get("harness_assets")
    if not isinstance(harness_assets, dict) or not isinstance(
        harness_assets.get("gate_oracles"), dict
    ):
        raise GateDispatchError("case dossier gate_oracles must be an object")
    return harness_assets["gate_oracles"]
