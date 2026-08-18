from __future__ import annotations

import json
from pathlib import Path
from typing import Any


FAILURE_CLASSES = frozenset(
    {"generation", "execution", "geometry", "provider", "budget", "harness"}
)


def classify_result(result: dict[str, Any]) -> str:
    if result.get("status") == "succeeded":
        return "pass"
    if result.get("stop_reason") == "provider_error":
        return "provider"
    last_revision = (result.get("revisions") or [])[-1] if result.get("revisions") else {}
    gates = last_revision.get("gates") or {}
    if gates and gates.get("passed") is False:
        return "geometry"
    if result.get("status") == "budget_exhausted":
        return "budget"
    last = last_revision
    feedback = last.get("feedback") or {}
    if feedback.get("stage") == "generation":
        return "generation"
    if feedback.get("stage") == "execution":
        stderr = str(feedback.get("stderr", ""))
        return "generation" if "SyntaxError" in stderr else "execution"
    if feedback.get("stage") in {"geometry", "validation"}:
        return "geometry"
    return "provider"


def write_evaluation_summary(
    results: list[dict[str, Any]], json_path: Path, markdown_path: Path
) -> dict[str, Any]:
    rows = [
        {
            "case_id": result["case_id"],
            "mechanism": result.get("mechanism"),
            "capability_level": result.get("capability_level"),
            "status": result["status"],
            "classification": classify_result(result),
            "provider_requests": result["provider_requests"],
        }
        for result in results
    ]
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["classification"]] = counts.get(row["classification"], 0) + 1
    summary = {
        "schema_version": 1,
        "cases": rows,
        "counts": counts,
        "mechanism_report": build_mechanism_report(rows),
    }
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    lines = [
        "# Evaluation Summary",
        "",
        "| Case | Status | Classification | Requests |",
        "|---|---|---|---:|",
        *[
            f"| {row['case_id']} | {row['status']} | {row['classification']} | {row['provider_requests']} |"
            for row in rows
        ],
        "",
    ]
    markdown_path.write_text("\n".join(lines), encoding="utf-8")
    return summary


def build_mechanism_report(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str], dict[str, Any]] = {}
    for result in results:
        mechanism = result.get("mechanism")
        capability_level = result.get("capability_level")
        if not isinstance(mechanism, str) or not isinstance(capability_level, str):
            raise ValueError("evaluation result must declare mechanism and capability_level")
        key = (mechanism, capability_level)
        group = groups.setdefault(
            key,
            {
                "mechanism": mechanism,
                "capability_level": capability_level,
                "case_ids": [],
                "case_count": 0,
                "status_counts": {},
                "classification_counts": {},
            },
        )
        group["case_ids"].append(result["case_id"])
        group["case_count"] += 1
        status = str(result["status"])
        classification = result.get("classification") or classify_result(result)
        group["status_counts"][status] = group["status_counts"].get(status, 0) + 1
        group["classification_counts"][classification] = (
            group["classification_counts"].get(classification, 0) + 1
        )
    return [groups[key] for key in sorted(groups)]


def build_control_report(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str, str], dict[str, Any]] = {}
    for result in results:
        mechanism = result.get("mechanism")
        capability_level = result.get("capability_level")
        cohort = result.get("control_variant")
        if not all(isinstance(value, str) for value in (mechanism, capability_level, cohort)):
            raise ValueError("control result must declare mechanism, capability_level, and control_variant")
        key = (mechanism, capability_level, cohort)
        group = groups.setdefault(
            key,
            {
                "mechanism": mechanism,
                "capability_level": capability_level,
                "control_variant": cohort,
                "case_ids": [],
                "case_count": 0,
                "actual_failure_class_counts": {},
                "expectation_matches": 0,
            },
        )
        group["case_ids"].append(result["case_id"])
        group["case_count"] += 1
        actual_failure_class = str(result.get("actual_failure_class", "unknown"))
        group["actual_failure_class_counts"][actual_failure_class] = (
            group["actual_failure_class_counts"].get(actual_failure_class, 0) + 1
        )
        group["expectation_matches"] += int(bool(result.get("matches_expectation")))
    return [groups[key] for key in sorted(groups)]


def build_held_out_report(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Summarize held-out outcomes without merging them into runtime results."""
    groups: dict[tuple[str, str], dict[str, Any]] = {}
    for result in results:
        mechanism = result.get("mechanism")
        capability_level = result.get("capability_level")
        if not all(isinstance(value, str) for value in (mechanism, capability_level)):
            raise ValueError("held-out result must declare mechanism and capability_level")
        key = (mechanism, capability_level)
        group = groups.setdefault(
            key,
            {
                "mechanism": mechanism,
                "capability_level": capability_level,
                "case_ids": [],
                "case_count": 0,
                "actual_failure_class_counts": {},
                "expectation_matches": 0,
            },
        )
        group["case_ids"].append(result["case_id"])
        group["case_count"] += 1
        actual_failure_class = str(result.get("actual_failure_class", "unknown"))
        group["actual_failure_class_counts"][actual_failure_class] = (
            group["actual_failure_class_counts"].get(actual_failure_class, 0) + 1
        )
        group["expectation_matches"] += int(bool(result.get("matches_expectation")))
    return [groups[key] for key in sorted(groups)]


def build_pilot_report(
    runtime: dict[str, Any], control_matrix: dict[str, Any], held_out: dict[str, Any]
) -> dict[str, Any]:
    """Aggregate the independent fake-only L0-L2 pilot cohorts."""
    payloads = {
        "runtime": runtime,
        "control_matrix": control_matrix,
        "held_out": held_out,
    }
    expected_artifacts = {
        "runtime": "campaign",
        "control_matrix": "control_matrix",
        "held_out": "held_out_generalization",
    }
    for cohort, payload in payloads.items():
        if payload.get("artifact") != expected_artifacts[cohort]:
            raise ValueError(f"pilot {cohort} artifact is invalid")
        if payload.get("provider") != "fake":
            raise ValueError("pilot cohorts must use the fake provider")

    metadata = {
        (payload.get("campaign_id"), payload.get("contract_sha256"))
        for payload in payloads.values()
    }
    if len(metadata) != 1:
        raise ValueError("pilot cohorts must bind the same campaign contract")
    campaign_id, contract_sha256 = next(iter(metadata))
    if not isinstance(campaign_id, str) or not isinstance(contract_sha256, str):
        raise ValueError("pilot cohorts must declare campaign metadata")

    runtime_rows = _pilot_rows(runtime, "runtime")
    control_rows = _pilot_rows(control_matrix, "control_matrix")
    held_out_rows = _pilot_rows(held_out, "held_out")
    runtime_ids = [row["case_id"] for row in runtime_rows]
    held_out_ids = [row["case_id"] for row in held_out_rows]
    if set(runtime_ids) & set(held_out_ids):
        raise ValueError("pilot runtime and held-out case scopes overlap")

    capability_report = _build_capability_pilot_report(
        runtime_rows, control_rows, held_out_rows
    )
    accounting = _sum_accounting(
        payload.get("provider_accounting", {}) for payload in payloads.values()
    )
    status, stop_reason = _pilot_status(payloads.values())
    return {
        "schema_version": 1,
        "artifact": "l0_l2_fake_pilot",
        "campaign_id": campaign_id,
        "contract_sha256": contract_sha256,
        "provider": "fake",
        "accounting_scope": "pilot_cohort_aggregate",
        "provider_accounting": accounting,
        "provider_requests": sum(
            int(payload.get("provider_requests", 0)) for payload in payloads.values()
        ),
        "status": status,
        "stop_reason": stop_reason,
        "runtime_case_ids": runtime_ids,
        "held_out_case_ids": held_out_ids,
        "control_count": len(control_rows),
        "cohorts": {
            "runtime": _pilot_cohort_summary(runtime, runtime_rows),
            "control_matrix": _pilot_cohort_summary(control_matrix, control_rows),
            "held_out": _pilot_cohort_summary(held_out, held_out_rows),
        },
        "capability_report": capability_report,
    }


def build_hosted_pilot_report(
    runtime: dict[str, Any], control_matrix: dict[str, Any], held_out: dict[str, Any]
) -> dict[str, Any]:
    """Aggregate hosted runtime with fake control and held-out cohorts."""
    payloads = {
        "runtime": runtime,
        "control_matrix": control_matrix,
        "held_out": held_out,
    }
    expected = {
        "runtime": ("campaign", "deepseek"),
        "control_matrix": ("control_matrix", "fake"),
        "held_out": ("held_out_generalization", "fake"),
    }
    for cohort, payload in payloads.items():
        artifact, provider = expected[cohort]
        if payload.get("artifact") != artifact:
            raise ValueError(f"hosted pilot {cohort} artifact is invalid")
        if payload.get("provider") != provider:
            raise ValueError(f"hosted pilot {cohort} provider routing is invalid")
        if not isinstance(payload.get("model"), str) or not payload["model"]:
            raise ValueError(f"hosted pilot {cohort} model is invalid")

    metadata = {
        (payload.get("campaign_id"), payload.get("contract_sha256"))
        for payload in payloads.values()
    }
    if len(metadata) != 1:
        raise ValueError("hosted pilot cohorts must bind the same campaign contract")
    campaign_id, contract_sha256 = next(iter(metadata))
    if not isinstance(campaign_id, str) or not isinstance(contract_sha256, str):
        raise ValueError("hosted pilot cohorts must declare campaign metadata")

    runtime_rows = _pilot_rows(runtime, "runtime")
    control_rows = _pilot_rows(control_matrix, "control_matrix")
    held_out_rows = _pilot_rows(held_out, "held_out")
    runtime_ids = [row["case_id"] for row in runtime_rows]
    held_out_ids = [row["case_id"] for row in held_out_rows]
    if set(runtime_ids) & set(held_out_ids):
        raise ValueError("hosted pilot runtime and held-out case scopes overlap")

    cohorts = {
        cohort: {
            **_pilot_cohort_summary(payload, _pilot_rows(payload, cohort)),
            "provider": payload["provider"],
            "model": payload["model"],
            "result_path": str(
                {
                    "runtime": Path("runtime") / "result.json",
                    "control_matrix": Path("controls") / "result.json",
                    "held_out": Path("held-out") / "result.json",
                }[cohort]
            ),
        }
        for cohort, payload in payloads.items()
    }
    accounting = _sum_accounting(
        payload.get("provider_accounting", {}) for payload in payloads.values()
    )
    status, stop_reason = _pilot_status(payloads.values())
    return {
        "schema_version": 1,
        "artifact": "l0_l2_hosted_pilot",
        "campaign_id": campaign_id,
        "contract_sha256": contract_sha256,
        "provider": "mixed",
        "provider_routing": {
            cohort: {"provider": payload["provider"], "model": payload["model"]}
            for cohort, payload in payloads.items()
        },
        "accounting_scope": "pilot_cohort_aggregate",
        "provider_accounting": accounting,
        "provider_requests": sum(
            int(payload.get("provider_requests", 0)) for payload in payloads.values()
        ),
        "status": status,
        "stop_reason": stop_reason,
        "runtime_case_ids": runtime_ids,
        "held_out_case_ids": held_out_ids,
        "control_count": len(control_rows),
        "cohorts": cohorts,
        "capability_report": _build_capability_pilot_report(
            runtime_rows, control_rows, held_out_rows
        ),
    }
def write_pilot_summary(
    runtime: dict[str, Any],
    control_matrix: dict[str, Any],
    held_out: dict[str, Any],
    json_path: Path,
    markdown_path: Path,
    *,
    result_paths: dict[str, str] | None = None,
) -> dict[str, Any]:
    summary = build_pilot_report(runtime, control_matrix, held_out)
    for cohort, result_path in (result_paths or {}).items():
        if cohort in summary["cohorts"]:
            summary["cohorts"][cohort]["result_path"] = result_path
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    lines = [
        "# L0-L2 Fake-Only Pilot",
        "",
        f"Status: `{summary['status']}`",
        "",
        "| Capability | Mechanism | Runtime cases | Controls | Held-out cases |",
        "|---|---|---:|---:|---:|",
    ]
    lines.extend(
        f"| {row['capability_level']} | {row['mechanism']} | "
        f"{row['runtime_case_count']} | {row['control_count']} | "
        f"{row['held_out_case_count']} |"
        for row in summary["capability_report"]
    )
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return summary


def _pilot_rows(payload: dict[str, Any], cohort: str) -> list[dict[str, Any]]:
    rows = payload.get("cases")
    if not isinstance(rows, list) or not all(isinstance(row, dict) for row in rows):
        raise ValueError(f"pilot {cohort} cases must be an array of objects")
    return rows


def _pilot_status(payloads: Any) -> tuple[str, str]:
    statuses = [payload.get("status") for payload in payloads]
    if all(status == "succeeded" for status in statuses):
        return "succeeded", "completed"
    if any(status == "budget_exhausted" for status in statuses):
        return "budget_exhausted", "cohort_budget_exhausted"
    return "failed", "cohort_failed"


def _pilot_cohort_summary(payload: dict[str, Any], rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "status": payload.get("status"),
        "stop_reason": payload.get("stop_reason"),
        "case_count": len(rows),
        "case_ids": [row["case_id"] for row in rows],
        "provider_requests": int(payload.get("provider_requests", 0)),
        "provider_accounting": dict(payload.get("provider_accounting", {})),
    }


def _build_capability_pilot_report(
    runtime_rows: list[dict[str, Any]],
    control_rows: list[dict[str, Any]],
    held_out_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str], dict[str, Any]] = {}
    for cohort, rows in (
        ("runtime", runtime_rows),
        ("control_matrix", control_rows),
        ("held_out", held_out_rows),
    ):
        for row in rows:
            mechanism = row.get("mechanism")
            capability_level = row.get("capability_level")
            if not isinstance(mechanism, str) or not isinstance(capability_level, str):
                raise ValueError(f"pilot {cohort} row must declare mechanism and capability_level")
            key = (mechanism, capability_level)
            group = groups.setdefault(
                key,
                {
                    "mechanism": mechanism,
                    "capability_level": capability_level,
                    "runtime_case_ids": [],
                    "runtime_case_count": 0,
                    "runtime_status_counts": {},
                    "control_count": 0,
                    "control_expectation_matches": 0,
                    "held_out_case_ids": [],
                    "held_out_case_count": 0,
                    "held_out_expectation_matches": 0,
                },
            )
            if cohort == "runtime":
                group["runtime_case_ids"].append(row["case_id"])
                group["runtime_case_count"] += 1
                status = str(row.get("status"))
                group["runtime_status_counts"][status] = (
                    group["runtime_status_counts"].get(status, 0) + 1
                )
            elif cohort == "control_matrix":
                group["control_count"] += 1
                group["control_expectation_matches"] += int(
                    bool(row.get("matches_expectation"))
                )
            else:
                group["held_out_case_ids"].append(row["case_id"])
                group["held_out_case_count"] += 1
                group["held_out_expectation_matches"] += int(
                    bool(row.get("matches_expectation"))
                )
    return [
        groups[key]
        for key in sorted(groups, key=lambda item: (int(item[1][1:]), item[0]))
    ]


def _sum_accounting(accountings: Any) -> dict[str, int | float]:
    totals: dict[str, int | float] = {
        "http_attempts": 0,
        "total_tokens": 0,
        "cost_usd": 0.0,
    }
    for accounting in accountings:
        for key in totals:
            value = accounting.get(key, 0)
            totals[key] += value
    return totals
