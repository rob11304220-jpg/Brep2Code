from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Callable

from brep2code.campaigns import (
    CampaignCase,
    CampaignContract,
    CampaignValidationError,
    ControlCase,
    HeldOutCase,
    validate_control_matrix_result,
    validate_held_out_result,
    validate_hosted_pilot_result,
    validate_pilot_result,
)
from brep2code.cases import ValidatedCase, validate_catalog
from brep2code.evaluation import (
    build_control_report,
    build_held_out_report,
    build_hosted_pilot_report,
    build_mechanism_report,
    classify_result,
    write_pilot_summary,
)
from brep2code.execution import secure_backend_status
from brep2code.harness.runner import RepairLoopRunner
from brep2code.providers import CaseBudgetLimits, CaseBudgetProvider, FakeProvider
from brep2code.providers.protocol import Provider


@dataclass(frozen=True)
class CampaignRunResult:
    status: str
    stop_reason: str
    provider_requests: int
    result_path: Path


class CampaignRunner:
    """Run every runtime case in a frozen contract through isolated case roots."""

    def __init__(
        self,
        contract: CampaignContract,
        cases_root: Path,
        *,
        loop_factory: Callable[[Provider], RepairLoopRunner] = RepairLoopRunner,
    ) -> None:
        self.contract = contract
        self.cases_root = cases_root
        self.loop_factory = loop_factory

    def preflight(self, run_root: Path) -> tuple[tuple[CampaignCase, ValidatedCase], ...]:
        if run_root.exists():
            raise CampaignValidationError("campaign run root must be fresh")
        cases = self._validated_cases()
        ready, reason = secure_backend_status()
        if not ready:
            raise CampaignValidationError(reason)
        return cases

    def preflight_control_matrix(
        self, run_root: Path
    ) -> tuple[tuple[ControlCase, ValidatedCase], ...]:
        if run_root.exists():
            raise CampaignValidationError("control matrix run root must be fresh")
        cases = self._validated_control_cases()
        ready, reason = secure_backend_status()
        if not ready:
            raise CampaignValidationError(reason)
        return cases

    def preflight_held_out(self, run_root: Path) -> tuple[tuple[HeldOutCase, ValidatedCase], ...]:
        if run_root.exists():
            raise CampaignValidationError("held-out run root must be fresh")
        cases = self._validated_held_out_cases()
        ready, reason = secure_backend_status()
        if not ready:
            raise CampaignValidationError(reason)
        return cases

    def preflight_pilot(self, run_root: Path) -> dict[str, int]:
        """Check the complete pilot scope without providers, execution, or artifacts."""
        if run_root.exists():
            raise CampaignValidationError("pilot run root must be fresh")
        counts = self.validate_pilot_scope()
        self.validate_secure_backend()
        return counts

    def validate_pilot_scope(self) -> dict[str, int]:
        """Validate runtime, control, and held-out cohorts without backend access."""
        runtime = self._validated_cases()
        controls = self._validated_control_cases()
        held_out = self._validated_held_out_cases()
        return {
            "runtime": len(runtime),
            "control_matrix": len(controls),
            "held_out": len(held_out),
        }

    def validate_secure_backend(self) -> None:
        """Require the configured generated-code backend using its read-only probe."""
        ready, reason = secure_backend_status()
        if not ready:
            raise CampaignValidationError(reason)

    def control_scripts(self) -> tuple[str, ...]:
        catalog = self._catalog()
        scripts: list[str] = []
        for control in self.contract.control_matrix:
            validated = catalog[control.case_id]
            controls = validated.dossier["harness_assets"]["controls"]
            asset = next(
                item["asset"] for item in controls if item["variant"] == control.control_variant
            )
            scripts.append((validated.case.root / asset).read_text(encoding="utf-8"))
        return tuple(scripts)

    def held_out_scripts(self) -> tuple[str, ...]:
        catalog = self._catalog()
        scripts: list[str] = []
        for held_out in self.contract.held_out_matrix:
            validated = catalog[held_out.case_id]
            fixture = validated.dossier["harness_assets"]["held_out_fixture"]
            scripts.append((validated.case.root / fixture["asset"]).read_text(encoding="utf-8"))
        return tuple(scripts)

    def run(
        self,
        provider: Provider,
        run_root: Path,
        *,
        preflighted: bool = False,
    ) -> CampaignRunResult:
        if not preflighted:
            cases = self.preflight(run_root)
        else:
            if run_root.exists():
                raise CampaignValidationError("campaign run root must be fresh")
            cases = self._validated_cases()

        run_root.mkdir(parents=True, exist_ok=False)
        result_path = run_root / "result.json"
        payload = {
            "schema_version": 1,
            "artifact": "campaign",
            "campaign_id": self.contract.campaign_id,
            "contract_sha256": self.contract.sha256,
            "provider": provider.name,
            "model": provider.model,
            "max_rounds": self.contract.provider_policy["max_rounds"],
            "max_requests": self.contract.provider_policy["max_requests"],
            "provider_policy": dict(self.contract.provider_policy),
            "accounting_scope": "campaign_aggregate",
            "provider_accounting": _provider_accounting(provider),
            "provider_requests": 0,
            "status": "running",
            "stop_reason": None,
            "cases": [],
            "mechanism_report": [],
        }
        _write_checkpoint(result_path, payload)

        for campaign_case, validated_case in cases:
            case_root = run_root / "cases" / campaign_case.case_id
            case_provider = CaseBudgetProvider(
                provider,
                CaseBudgetLimits(
                    scope="case",
                    max_requests=self.contract.provider_policy["case_max_requests"],
                    max_total_tokens=self.contract.provider_policy["case_max_total_tokens"],
                    max_cost_usd=self.contract.provider_policy["case_max_cost_usd"],
                ),
            )
            projection = {
                "campaign_id": self.contract.campaign_id,
                "contract_sha256": self.contract.sha256,
                "case": asdict(campaign_case),
            }
            case_payload: dict = {}
            try:
                result = self.loop_factory(case_provider).run(
                    validated_case,
                    case_root,
                    max_rounds=self.contract.provider_policy["max_rounds"],
                    timeout_seconds=self.contract.provider_policy["build_timeout_seconds"],
                    campaign=projection,
                )
                case_payload = _load_case_result(result.result_path)
                row = {
                    "case_id": campaign_case.case_id,
                    "capability_level": campaign_case.capability_level,
                    "mechanism": campaign_case.mechanism,
                    "difficulty": campaign_case.difficulty,
                    "status": result.status,
                    "stop_reason": result.stop_reason,
                    "classification": classify_result(case_payload),
                    "gate_report": _latest_gate_report(case_payload),
                    "case_provider_accounting": case_payload.get("provider_accounting", {}),
                    "provider_requests": result.provider_requests,
                    "result_path": str(Path("cases") / campaign_case.case_id / "result.json"),
                }
            except (OSError, RuntimeError, ValueError) as exc:
                row = {
                    "case_id": campaign_case.case_id,
                    "capability_level": campaign_case.capability_level,
                    "mechanism": campaign_case.mechanism,
                    "difficulty": campaign_case.difficulty,
                    "status": "failed",
                    "stop_reason": "runner_error",
                    "classification": "harness",
                    "gate_report": {},
                    "provider_requests": 0,
                    "error": {"type": type(exc).__name__},
                }
            payload["cases"].append(row)
            payload["provider_requests"] = sum(
                item["provider_requests"] for item in payload["cases"]
            )
            payload["provider_accounting"] = _provider_accounting(provider)
            payload["mechanism_report"] = build_mechanism_report(payload["cases"])
            if (
                row["status"] == "budget_exhausted"
                and _budget_scope(case_payload) == "campaign_aggregate"
            ):
                payload["status"] = "budget_exhausted"
                payload["stop_reason"] = "budget_exhausted"
                _write_checkpoint(result_path, payload)
                return _result(payload, result_path)
            if payload["provider_requests"] > self.contract.provider_policy["max_requests"]:
                payload["status"] = "failed"
                payload["stop_reason"] = "request_budget_exceeded"
                _write_checkpoint(result_path, payload)
                return _result(payload, result_path)
            _write_checkpoint(result_path, payload)

        all_passed = all(item["status"] == "succeeded" for item in payload["cases"])
        has_case_budget_exhaustion = any(
            item["status"] == "budget_exhausted" for item in payload["cases"]
        )
        if all_passed:
            payload["status"] = "succeeded"
            payload["stop_reason"] = "completed"
        elif has_case_budget_exhaustion:
            payload["status"] = "budget_exhausted"
            payload["stop_reason"] = "case_budget_exhausted"
        else:
            payload["status"] = "failed"
            payload["stop_reason"] = "case_failed"
        _write_checkpoint(result_path, payload)
        return _result(payload, result_path)

    def run_control_matrix(
        self,
        provider: Provider,
        run_root: Path,
        *,
        preflighted: bool = False,
    ) -> CampaignRunResult:
        if provider.name != "fake":
            raise CampaignValidationError("control matrix runs require the fake provider")
        if not preflighted:
            cases = self.preflight_control_matrix(run_root)
        else:
            if run_root.exists():
                raise CampaignValidationError("control matrix run root must be fresh")
            cases = self._validated_control_cases()

        run_root.mkdir(parents=True, exist_ok=False)
        result_path = run_root / "result.json"
        policy = self.contract.control_policy
        payload = {
            "schema_version": 1,
            "artifact": "control_matrix",
            "campaign_id": self.contract.campaign_id,
            "contract_sha256": self.contract.sha256,
            "provider": provider.name,
            "model": provider.model,
            "control_policy": dict(policy),
            "accounting_scope": "control_matrix_aggregate",
            "provider_accounting": _provider_accounting(provider),
            "provider_requests": 0,
            "status": "running",
            "stop_reason": None,
            "cases": [],
            "control_report": [],
        }
        _write_checkpoint(result_path, payload)

        for control, validated_case in cases:
            case_root = run_root / "cases" / control.case_id / control.control_variant
            case_provider = CaseBudgetProvider(
                provider,
                CaseBudgetLimits(
                    scope="case",
                    max_requests=policy["case_max_requests"],
                    max_total_tokens=policy["case_max_total_tokens"],
                    max_cost_usd=policy["case_max_cost_usd"],
                ),
            )
            projection = {
                "campaign_id": self.contract.campaign_id,
                "contract_sha256": self.contract.sha256,
                "case": {
                    "case_id": control.case_id,
                    "control_variant": control.control_variant,
                    "expected_result": control.expected_result,
                    "failure_class": control.failure_class,
                },
            }
            case_payload: dict = {}
            try:
                result = self.loop_factory(case_provider).run(
                    validated_case,
                    case_root,
                    max_rounds=policy["max_rounds"],
                    timeout_seconds=policy["build_timeout_seconds"],
                    campaign=projection,
                )
                case_payload = _load_case_result(result.result_path)
                actual_failure_class = classify_result(case_payload)
                actual_result = "pass" if actual_failure_class == "pass" else "fail"
                row = {
                    "case_id": control.case_id,
                    "control_variant": control.control_variant,
                    "mechanism": validated_case.metadata["mechanism"],
                    "capability_level": validated_case.metadata["capability_level"],
                    "expected_result": control.expected_result,
                    "expected_failure_class": control.failure_class,
                    "actual_result": actual_result,
                    "actual_failure_class": actual_failure_class,
                    "matches_expectation": (
                        actual_result == control.expected_result
                        and actual_failure_class == control.failure_class
                    ),
                    "status": result.status,
                    "stop_reason": result.stop_reason,
                    "gate_report": _latest_gate_report(case_payload),
                    "case_provider_accounting": case_payload.get("provider_accounting", {}),
                    "provider_requests": result.provider_requests,
                    "result_path": str(
                        Path("cases") / control.case_id / control.control_variant / "result.json"
                    ),
                }
            except (OSError, RuntimeError, ValueError) as exc:
                row = {
                    "case_id": control.case_id,
                    "control_variant": control.control_variant,
                    "mechanism": validated_case.metadata["mechanism"],
                    "capability_level": validated_case.metadata["capability_level"],
                    "expected_result": control.expected_result,
                    "expected_failure_class": control.failure_class,
                    "actual_result": "fail",
                    "actual_failure_class": "harness",
                    "matches_expectation": False,
                    "status": "failed",
                    "stop_reason": "runner_error",
                    "gate_report": {},
                    "case_provider_accounting": _provider_accounting(case_provider),
                    "provider_requests": 0,
                    "result_path": str(
                        Path("cases") / control.case_id / control.control_variant / "result.json"
                    ),
                    "error": {"type": type(exc).__name__},
                }
            payload["cases"].append(row)
            payload["provider_requests"] = sum(
                item["provider_requests"] for item in payload["cases"]
            )
            payload["provider_accounting"] = _provider_accounting(provider)
            payload["control_report"] = build_control_report(payload["cases"])
            if payload["provider_requests"] > policy["max_requests"]:
                payload["status"] = "failed"
                payload["stop_reason"] = "request_budget_exceeded"
                _write_checkpoint(result_path, payload)
                return _result(payload, result_path)
            _write_checkpoint(result_path, payload)

        if all(item["matches_expectation"] for item in payload["cases"]):
            payload["status"] = "succeeded"
            payload["stop_reason"] = "control_matrix_passed"
        else:
            payload["status"] = "failed"
            payload["stop_reason"] = "control_expectation_failed"
        validate_control_matrix_result(payload, self.contract)
        _write_checkpoint(result_path, payload)
        return _result(payload, result_path)

    def run_pilot(
        self,
        provider: Provider,
        run_root: Path,
        *,
        preflighted: bool = False,
    ) -> CampaignRunResult:
        """Run the isolated runtime, control, and held-out fake-only cohorts."""
        if provider.name != "fake":
            raise CampaignValidationError("L0-L2 pilot runs require the fake provider")
        if run_root.exists():
            raise CampaignValidationError("pilot run root must be fresh")

        runtime_root = run_root / "runtime"
        control_root = run_root / "controls"
        held_out_root = run_root / "held-out"
        if not preflighted:
            self.preflight(runtime_root)
            self.preflight_control_matrix(control_root)
            self.preflight_held_out(held_out_root)
        run_root.mkdir(parents=True, exist_ok=False)

        runtime_result = self.run(provider, runtime_root, preflighted=True)
        control_result = self.run_control_matrix(
            FakeProvider(self.control_scripts()), control_root, preflighted=True
        )
        held_out_result = self.run_held_out(
            FakeProvider(self.held_out_scripts()), held_out_root, preflighted=True
        )
        summary_path = run_root / "result.json"
        runtime_payload = _load_case_result(runtime_result.result_path)
        control_payload = _load_case_result(control_result.result_path)
        held_out_payload = _load_case_result(held_out_result.result_path)
        summary = write_pilot_summary(
            runtime_payload,
            control_payload,
            held_out_payload,
            summary_path,
            run_root / "summary.md",
            result_paths={
                "runtime": str(Path("runtime") / "result.json"),
                "control_matrix": str(Path("controls") / "result.json"),
                "held_out": str(Path("held-out") / "result.json"),
            },
        )
        validate_pilot_result(
            summary,
            self.contract,
            runtime_payload=runtime_payload,
            control_matrix_payload=control_payload,
            held_out_payload=held_out_payload,
        )
        return CampaignRunResult(
            status=summary["status"],
            stop_reason=summary["stop_reason"],
            provider_requests=summary["provider_requests"],
            result_path=summary_path,
        )

    def run_hosted_pilot(
        self,
        provider: Provider,
        run_root: Path,
        *,
        preflighted: bool = False,
    ) -> CampaignRunResult:
        """Run hosted runtime plus isolated fake control and held-out cohorts."""
        _validate_hosted_provider(provider, self.contract)
        if run_root.exists():
            raise CampaignValidationError("hosted pilot run root must be fresh")
        if not preflighted:
            self.preflight_pilot(run_root)

        runtime_root = run_root / "runtime"
        control_root = run_root / "controls"
        held_out_root = run_root / "held-out"
        run_root.mkdir(parents=True, exist_ok=False)

        runtime_result = self.run(provider, runtime_root, preflighted=True)
        control_result = self.run_control_matrix(
            FakeProvider(self.control_scripts()), control_root, preflighted=True
        )
        held_out_result = self.run_held_out(
            FakeProvider(self.held_out_scripts()), held_out_root, preflighted=True
        )
        runtime_payload = _load_case_result(runtime_result.result_path)
        control_payload = _load_case_result(control_result.result_path)
        held_out_payload = _load_case_result(held_out_result.result_path)
        summary = build_hosted_pilot_report(runtime_payload, control_payload, held_out_payload)
        validate_hosted_pilot_result(
            summary,
            self.contract,
            runtime_payload=runtime_payload,
            control_matrix_payload=control_payload,
            held_out_payload=held_out_payload,
        )
        summary_path = run_root / "result.json"
        _write_checkpoint(summary_path, summary)
        return CampaignRunResult(
            status=summary["status"],
            stop_reason=summary["stop_reason"],
            provider_requests=summary["provider_requests"],
            result_path=summary_path,
        )

    def run_held_out(
        self,
        provider: Provider,
        run_root: Path,
        *,
        preflighted: bool = False,
    ) -> CampaignRunResult:
        if provider.name != "fake":
            raise CampaignValidationError("held-out runs require the fake provider")
        if not preflighted:
            cases = self.preflight_held_out(run_root)
        else:
            if run_root.exists():
                raise CampaignValidationError("held-out run root must be fresh")
            cases = self._validated_held_out_cases()

        run_root.mkdir(parents=True, exist_ok=False)
        result_path = run_root / "result.json"
        policy = self.contract.held_out_policy
        payload = {
            "schema_version": 1,
            "artifact": "held_out_generalization",
            "campaign_id": self.contract.campaign_id,
            "contract_sha256": self.contract.sha256,
            "provider": provider.name,
            "model": provider.model,
            "held_out_policy": dict(policy),
            "accounting_scope": "held_out_aggregate",
            "provider_accounting": _provider_accounting(provider),
            "provider_requests": 0,
            "status": "running",
            "stop_reason": None,
            "cases": [],
            "held_out_report": [],
        }
        _write_checkpoint(result_path, payload)

        for held_out, validated_case in cases:
            case_root = run_root / "cases" / held_out.case_id
            case_provider = CaseBudgetProvider(
                provider,
                CaseBudgetLimits(
                    scope="case",
                    max_requests=policy["case_max_requests"],
                    max_total_tokens=policy["case_max_total_tokens"],
                    max_cost_usd=policy["case_max_cost_usd"],
                ),
            )
            projection = {
                "campaign_id": self.contract.campaign_id,
                "contract_sha256": self.contract.sha256,
                "case": {
                    "case_id": held_out.case_id,
                    "mode": "held_out",
                    "capability_level": validated_case.metadata["capability_level"],
                    "mechanism": validated_case.metadata["mechanism"],
                },
            }
            case_payload: dict = {}
            try:
                result = self.loop_factory(case_provider).run(
                    validated_case,
                    case_root,
                    max_rounds=policy["max_rounds"],
                    timeout_seconds=policy["build_timeout_seconds"],
                    campaign=projection,
                )
                case_payload = _load_case_result(result.result_path)
                actual_failure_class = classify_result(case_payload)
                actual_result = "pass" if actual_failure_class == "pass" else "fail"
                row = {
                    "case_id": held_out.case_id,
                    "mechanism": validated_case.metadata["mechanism"],
                    "capability_level": validated_case.metadata["capability_level"],
                    "expected_result": held_out.expected_result,
                    "expected_failure_class": held_out.failure_class,
                    "fixture_sha256": held_out.fixture_sha256,
                    "expected": held_out.expected,
                    "gate_oracles": held_out.gate_oracles,
                    "actual_result": actual_result,
                    "actual_failure_class": actual_failure_class,
                    "matches_expectation": (
                        actual_result == held_out.expected_result
                        and actual_failure_class == held_out.failure_class
                    ),
                    "status": result.status,
                    "stop_reason": result.stop_reason,
                    "gate_report": _latest_gate_report(case_payload),
                    "case_provider_accounting": case_payload.get("provider_accounting", {}),
                    "provider_requests": result.provider_requests,
                    "result_path": str(Path("cases") / held_out.case_id / "result.json"),
                }
            except (OSError, RuntimeError, ValueError) as exc:
                row = {
                    "case_id": held_out.case_id,
                    "mechanism": validated_case.metadata["mechanism"],
                    "capability_level": validated_case.metadata["capability_level"],
                    "expected_result": held_out.expected_result,
                    "expected_failure_class": held_out.failure_class,
                    "fixture_sha256": held_out.fixture_sha256,
                    "expected": held_out.expected,
                    "gate_oracles": held_out.gate_oracles,
                    "actual_result": "fail",
                    "actual_failure_class": "harness",
                    "matches_expectation": False,
                    "status": "failed",
                    "stop_reason": "runner_error",
                    "gate_report": {},
                    "case_provider_accounting": _provider_accounting(case_provider),
                    "provider_requests": 0,
                    "result_path": str(Path("cases") / held_out.case_id / "result.json"),
                    "error": {"type": type(exc).__name__},
                }
            payload["cases"].append(row)
            payload["provider_requests"] = sum(
                item["provider_requests"] for item in payload["cases"]
            )
            payload["provider_accounting"] = _provider_accounting(provider)
            payload["held_out_report"] = build_held_out_report(payload["cases"])
            if payload["provider_requests"] > policy["max_requests"]:
                payload["status"] = "failed"
                payload["stop_reason"] = "request_budget_exceeded"
                _write_checkpoint(result_path, payload)
                return _result(payload, result_path)
            _write_checkpoint(result_path, payload)

        if all(item["matches_expectation"] for item in payload["cases"]):
            payload["status"] = "succeeded"
            payload["stop_reason"] = "held_out_passed"
        else:
            payload["status"] = "failed"
            payload["stop_reason"] = "held_out_expectation_failed"
        validate_held_out_result(payload, self.contract)
        _write_checkpoint(result_path, payload)
        return _result(payload, result_path)

    def _validated_cases(self) -> tuple[tuple[CampaignCase, ValidatedCase], ...]:
        catalog = self._catalog()
        return tuple(
            (campaign_case, catalog[campaign_case.case_id])
            for campaign_case in self.contract.runtime_cases
        )

    def _validated_control_cases(self) -> tuple[tuple[ControlCase, ValidatedCase], ...]:
        catalog = self._catalog()
        return tuple(
            (control, catalog[control.case_id]) for control in self.contract.control_matrix
        )

    def _validated_held_out_cases(self) -> tuple[tuple[HeldOutCase, ValidatedCase], ...]:
        catalog = self._catalog()
        return tuple(
            (held_out, catalog[held_out.case_id]) for held_out in self.contract.held_out_matrix
        )

    def _catalog(self) -> dict[str, ValidatedCase]:
        manifests = validate_catalog(self.cases_root)
        return {item.case.case_id: item for manifest in manifests for item in manifest.cases}


def _load_case_result(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("case result must be a JSON object")
    return payload


def _result(payload: dict, path: Path) -> CampaignRunResult:
    return CampaignRunResult(
        status=str(payload["status"]),
        stop_reason=str(payload["stop_reason"]),
        provider_requests=int(payload["provider_requests"]),
        result_path=path,
    )


def _budget_scope(case_payload: dict) -> str | None:
    revisions = case_payload.get("revisions") or []
    if not revisions:
        return None
    error = revisions[-1].get("error") or {}
    if error.get("stage") != "budget":
        return None
    scope = error.get("scope")
    return scope if isinstance(scope, str) else None


def _latest_gate_report(case_payload: dict) -> dict:
    revisions = case_payload.get("revisions") or []
    if not revisions:
        return {}
    report = revisions[-1].get("gates")
    return report if isinstance(report, dict) else {}


def _write_checkpoint(path: Path, payload: dict) -> None:
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    temporary.replace(path)


def _provider_accounting(provider: Provider) -> dict[str, int | float]:
    requests_issued = getattr(provider, "requests_issued", None)
    if requests_issued is None:
        requests_issued = len(getattr(provider, "requests", ()))
    return {
        "http_attempts": int(requests_issued),
        "total_tokens": int(getattr(provider, "total_tokens", 0)),
        "cost_usd": float(getattr(provider, "cost_usd", 0.0)),
    }


def _validate_hosted_provider(provider: Provider, contract: CampaignContract) -> None:
    policy = contract.provider_policy
    if provider.name != policy["provider"]:
        raise CampaignValidationError("hosted pilot provider must match the campaign contract")
    if provider.model != policy["model"]:
        raise CampaignValidationError("hosted pilot model must match the campaign contract")
    limits = getattr(provider, "limits", None)
    bindings = {
        "max_requests": "max_requests",
        "timeout_seconds": "provider_timeout_seconds",
        "max_retries": "max_retries",
        "max_output_tokens": "max_output_tokens",
        "max_total_tokens": "max_total_tokens",
        "max_cost_usd": "max_cost_usd",
        "input_cost_per_million": "input_cost_per_million",
        "output_cost_per_million": "output_cost_per_million",
    }
    if limits is None or any(
        getattr(limits, attribute, None) != policy[key] for attribute, key in bindings.items()
    ):
        raise CampaignValidationError(
            "hosted pilot provider limits must match the campaign contract"
        )
