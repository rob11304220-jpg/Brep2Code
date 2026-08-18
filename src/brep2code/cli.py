from __future__ import annotations

import argparse
from contextlib import redirect_stdout
from dataclasses import asdict
import io
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

from brep2code.cases import CaseValidationError, ValidatedCase, validate_catalog
from brep2code.campaigns import (
    CampaignValidationError,
    load_campaign_contract,
    validate_hosted_pilot_result,
    validate_pilot_result,
)
from brep2code.harness import (
    ActiveBudgets,
    ActiveHarnessRunner,
    ActiveHostedAuthorization,
    ActiveResultValidationError,
    CampaignRunner,
    HarnessAction,
    RepairLoopRunner,
    preflight_active_hosted,
    validate_active_result,
)
from brep2code.execution import secure_backend_status
from brep2code.evaluation import ACTIVE_COHORT_LABELS, build_active_pilot_report
from brep2code.providers import (
    FakeActionProvider,
    FakeProvider,
    OpenAICompatibleProvider,
    ProviderConfigurationError,
    ProviderLimits,
    deepseek_config_from_env,
)


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.command == "cases" and args.cases_command == "validate":
        return _validate_cases(args.root)
    if args.command == "campaign" and args.campaign_command == "validate":
        return _validate_campaign(args.contract, args.cases_root)
    if args.command == "campaign" and args.campaign_command == "preflight":
        return _campaign_preflight(args.contract, args.cases_root, args.run_root)
    if args.command == "campaign" and args.campaign_command == "run":
        return _campaign_run(args)
    if args.command == "campaign" and args.campaign_command == "controls":
        return _campaign_controls(args)
    if args.command == "campaign" and args.campaign_command == "held-out":
        return _campaign_held_out(args)
    if args.command == "campaign" and args.campaign_command == "pilot":
        return _campaign_pilot(args)
    if args.command == "campaign" and args.campaign_command == "pilot-validate":
        return _campaign_pilot_validate(args)
    if args.command == "campaign" and args.campaign_command == "pilot-preflight":
        return _campaign_pilot_preflight(args)
    if args.command == "campaign" and args.campaign_command == "hosted-pilot-validate":
        return _campaign_hosted_pilot_validate(args)
    if args.command == "campaign" and args.campaign_command == "hosted-pilot":
        return _campaign_hosted_pilot(args)
    if args.command == "campaign" and args.campaign_command == "hosted-pilot-config-check":
        return _campaign_hosted_pilot_config_check(args)
    if args.command == "campaign" and args.campaign_command == "hosted-readiness":
        return _campaign_hosted_readiness(args)
    if args.command == "run":
        return _run(args)
    if args.command == "active-run":
        return _active_run(args)
    if args.command == "active-preflight":
        return _active_preflight(args)
    if args.command == "active-validate":
        return _active_validate(args)
    if args.command == "active-continue":
        return _active_continue(args)
    if args.command == "active-hosted-preflight":
        return _active_hosted_preflight(args)
    if args.command == "active-hosted-config-check":
        return _active_hosted_config_check(args)
    if args.command == "active-hosted-readiness":
        return _active_hosted_readiness(args)
    if args.command == "active-hosted-run":
        return _active_hosted_run(args)
    if args.command == "active-hosted-live-run":
        return _active_hosted_live_run(args)
    if args.command == "active-hosted-continue":
        return _active_hosted_continue(args)
    if args.command == "active-pilot-report":
        return _active_pilot_report(args)
    parser.print_help()
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="brep2code")
    parser.add_argument("--version", action="version", version="brep2code 0.1.0")
    commands = parser.add_subparsers(dest="command")
    cases = commands.add_parser("cases", help="Inspect and validate case assets.")
    cases_commands = cases.add_subparsers(dest="cases_command", required=True)
    validate = cases_commands.add_parser("validate", help="Validate every discovered case.")
    validate.add_argument("--root", type=Path, default=Path("cases"))
    campaign = commands.add_parser("campaign", help="Inspect and validate a campaign contract.")
    campaign_commands = campaign.add_subparsers(dest="campaign_command", required=True)
    campaign_validate = campaign_commands.add_parser(
        "validate", help="Validate a campaign against the case catalog."
    )
    campaign_validate.add_argument("--contract", type=Path, required=True)
    campaign_validate.add_argument("--cases-root", type=Path, default=Path("cases"))
    campaign_preflight = campaign_commands.add_parser(
        "preflight", help="Check a campaign locally without constructing a provider."
    )
    campaign_preflight.add_argument("--contract", type=Path, required=True)
    campaign_preflight.add_argument("--cases-root", type=Path, default=Path("cases"))
    campaign_preflight.add_argument("--run-root", type=Path, required=True)
    campaign_run = campaign_commands.add_parser(
        "run", help="Run every runtime case in a bounded campaign."
    )
    campaign_run.add_argument("--contract", type=Path, required=True)
    campaign_run.add_argument("--cases-root", type=Path, default=Path("cases"))
    campaign_run.add_argument("--run-root", type=Path, required=True)
    _add_campaign_provider_arguments(campaign_run)
    campaign_controls = campaign_commands.add_parser(
        "controls", help="Run every dossier-bound development control with fake provider assets."
    )
    campaign_controls.add_argument("--contract", type=Path, required=True)
    campaign_controls.add_argument("--cases-root", type=Path, default=Path("cases"))
    campaign_controls.add_argument("--run-root", type=Path, required=True)
    campaign_held_out = campaign_commands.add_parser(
        "held-out", help="Run the isolated held-out generalization cohort with fake fixtures."
    )
    campaign_held_out.add_argument("--contract", type=Path, required=True)
    campaign_held_out.add_argument("--cases-root", type=Path, default=Path("cases"))
    campaign_held_out.add_argument("--run-root", type=Path, required=True)
    campaign_pilot = campaign_commands.add_parser(
        "pilot", help="Run the isolated L0-L2 fake-only pilot and write its aggregate report."
    )
    campaign_pilot.add_argument("--contract", type=Path, required=True)
    campaign_pilot.add_argument("--cases-root", type=Path, default=Path("cases"))
    campaign_pilot.add_argument("--run-root", type=Path, required=True)
    campaign_pilot.add_argument("--fake-script", type=Path, action="append", required=True)
    campaign_pilot_validate = campaign_commands.add_parser(
        "pilot-validate", help="Validate a saved pilot and its three cohort results."
    )
    campaign_pilot_validate.add_argument("--contract", type=Path, required=True)
    campaign_pilot_validate.add_argument("--cases-root", type=Path, default=Path("cases"))
    campaign_pilot_validate.add_argument("--result", type=Path, required=True)
    campaign_pilot_preflight = campaign_commands.add_parser(
        "pilot-preflight", help="Check hosted L0-L2 pilot readiness without constructing providers."
    )
    _add_hosted_pilot_arguments(campaign_pilot_preflight)
    hosted_pilot_validate = campaign_commands.add_parser(
        "hosted-pilot-validate",
        help="Validate a saved mixed-provider pilot and its cohort results.",
    )
    hosted_pilot_validate.add_argument("--contract", type=Path, required=True)
    hosted_pilot_validate.add_argument("--cases-root", type=Path, default=Path("cases"))
    hosted_pilot_validate.add_argument("--result", type=Path, required=True)
    hosted_pilot = campaign_commands.add_parser(
        "hosted-pilot", help="Run the bounded mixed-provider L0-L2 hosted pilot."
    )
    _add_hosted_pilot_arguments(hosted_pilot)
    hosted_pilot_config_check = campaign_commands.add_parser(
        "hosted-pilot-config-check",
        help="Validate hosted pilot configuration without network requests or artifacts.",
    )
    _add_hosted_pilot_arguments(hosted_pilot_config_check)
    hosted_readiness = campaign_commands.add_parser(
        "hosted-readiness",
        help="Validate every hosted pilot readiness gate without requests or artifacts.",
    )
    _add_hosted_pilot_arguments(hosted_readiness)
    hosted_readiness.add_argument("--baseline-result", type=Path, required=True)
    hosted_readiness.add_argument("--check-provider-config", action="store_true")
    run = commands.add_parser("run", help="Run one bounded provider loop.")
    run.add_argument("--provider", choices=("fake", "deepseek"), default="fake")
    run.add_argument("--case-id", required=True)
    run.add_argument("--cases-root", type=Path, default=Path("cases"))
    run.add_argument("--campaign-contract", type=Path)
    run.add_argument("--run-root", type=Path, required=True)
    run.add_argument("--initial-script", type=Path)
    run.add_argument("--fake-script", type=Path, action="append")
    run.add_argument("--max-rounds", type=int, required=True)
    run.add_argument("--timeout", type=int, default=30)
    run.add_argument("--authorize-hosted", action="store_true")
    run.add_argument("--thinking-mode", choices=("disabled",))
    run.add_argument("--max-requests", type=int)
    run.add_argument("--provider-timeout", type=float)
    run.add_argument("--max-retries", type=int)
    run.add_argument("--max-output-tokens", type=int)
    run.add_argument("--max-total-tokens", type=int)
    run.add_argument("--max-cost-usd", type=float)
    run.add_argument("--input-cost-per-million", type=float)
    run.add_argument("--output-cost-per-million", type=float)
    active_run = commands.add_parser(
        "active-run", help="Run one bounded offline tool-using action session."
    )
    _add_active_arguments(active_run)
    active_preflight = commands.add_parser(
        "active-preflight", help="Validate an offline active run without creating artifacts."
    )
    _add_active_arguments(active_preflight)
    active_validate = commands.add_parser(
        "active-validate", help="Validate a saved active run and its revision artifacts."
    )
    active_validate.add_argument("--result", type=Path, required=True)
    active_validate.add_argument("--cases-root", type=Path, default=Path("cases"))
    active_continue = commands.add_parser(
        "active-continue", help="Continue one validated interrupted offline active session."
    )
    _add_active_arguments(active_continue)
    active_hosted_preflight = commands.add_parser(
        "active-hosted-preflight",
        help="Validate a hosted active plan without reading provider configuration.",
    )
    _add_active_hosted_arguments(active_hosted_preflight)
    active_hosted_config = commands.add_parser(
        "active-hosted-config-check",
        help="Validate hosted active provider configuration without network requests.",
    )
    _add_active_hosted_arguments(active_hosted_config)
    active_hosted_readiness = commands.add_parser(
        "active-hosted-readiness",
        help="Validate every hosted active readiness gate without requests or artifacts.",
    )
    _add_active_hosted_arguments(active_hosted_readiness)
    active_hosted_readiness.add_argument("--baseline-result", type=Path, required=True)
    active_hosted_readiness.add_argument("--check-provider-config", action="store_true")
    active_hosted_run = commands.add_parser(
        "active-hosted-run",
        help="Run one readiness-gated hosted active session through an HTTP stub.",
    )
    _add_active_hosted_arguments(active_hosted_run)
    active_hosted_run.add_argument("--baseline-result", type=Path, required=True)
    active_hosted_run.add_argument("--http-stub-response", type=Path, required=True)
    active_hosted_live_run = commands.add_parser(
        "active-hosted-live-run",
        help="Run one readiness-gated hosted active session over bounded HTTPS.",
    )
    _add_active_hosted_arguments(active_hosted_live_run)
    active_hosted_live_run.add_argument("--baseline-result", type=Path, required=True)
    active_hosted_continue = commands.add_parser(
        "active-hosted-continue",
        help="Continue one hosted active session through an HTTP stub.",
    )
    _add_active_hosted_arguments(active_hosted_continue)
    active_hosted_continue.add_argument("--baseline-result", type=Path, required=True)
    active_hosted_continue.add_argument("--http-stub-response", type=Path, required=True)
    active_pilot_report = commands.add_parser(
        "active-pilot-report",
        help="Aggregate a deterministic fake L2 active cohort and hosted decision gate.",
    )
    active_pilot_report.add_argument("--contract", type=Path, required=True)
    active_pilot_report.add_argument("--cases-root", type=Path, default=Path("cases"))
    active_pilot_report.add_argument("--fixed-pilot-result", type=Path, required=True)
    for label in ACTIVE_COHORT_LABELS:
        active_pilot_report.add_argument(
            f"--{label.replace('_', '-')}-result", type=Path, required=True
        )
    active_pilot_report.add_argument("--output", type=Path, required=True)
    return parser


def _validate_cases(root: Path) -> int:
    try:
        manifests = validate_catalog(root)
    except CaseValidationError as exc:
        print(json.dumps({"status": "invalid", "error": str(exc)}))
        return 1
    payload = {
        "status": "valid",
        "count": sum(len(manifest.cases) for manifest in manifests),
        "cases": [
            {
                "case_id": item.case.case_id,
                "split": item.case.split,
                "mechanism": item.metadata["mechanism"],
                "capability_level": item.metadata["capability_level"],
                "sha256": item.sha256,
            }
            for manifest in manifests
            for item in manifest.cases
        ],
    }
    print(json.dumps(payload, indent=2))
    return 0


def _validate_campaign(contract_path: Path, cases_root: Path) -> int:
    try:
        contract = load_campaign_contract(contract_path, cases_root)
    except (CaseValidationError, CampaignValidationError) as exc:
        print(json.dumps({"status": "invalid", "error": str(exc)}))
        return 1
    print(
        json.dumps(
            {
                "status": "valid",
                "campaign_id": contract.campaign_id,
                "contract_sha256": contract.sha256,
                "case_count": len(contract.cases),
                "runtime_case_count": len(contract.runtime_cases),
                "control_count": len(contract.control_matrix),
                "budget": _campaign_budget_summary(contract.provider_policy),
                "capability_ladder": list(contract.capability_ladder),
            },
            indent=2,
        )
    )
    return 0


def _campaign_preflight(contract_path: Path, cases_root: Path, run_root: Path) -> int:
    try:
        contract = load_campaign_contract(contract_path, cases_root)
        CampaignRunner(contract, cases_root).preflight(run_root)
    except (CaseValidationError, CampaignValidationError, OSError, ValueError) as exc:
        print(json.dumps({"status": "not_ready", "error": str(exc)}))
        return 1
    print(
        json.dumps(
            {
                "status": "ready",
                "campaign_id": contract.campaign_id,
                "contract_sha256": contract.sha256,
                "runtime_case_count": len(contract.runtime_cases),
                "budget": _campaign_budget_summary(contract.provider_policy),
            },
            indent=2,
        )
    )
    return 0


def _campaign_run(args: argparse.Namespace) -> int:
    try:
        contract = load_campaign_contract(args.contract, args.cases_root)
        runner = CampaignRunner(contract, args.cases_root)
        runner.preflight(args.run_root)
        provider = _campaign_provider_from_args(args, contract)
        result = runner.run(provider, args.run_root, preflighted=True)
    except (
        CaseValidationError,
        CampaignValidationError,
        OSError,
        ProviderConfigurationError,
        ValueError,
    ) as exc:
        print(json.dumps({"status": "configuration_error", "error": str(exc)}))
        return 2
    print(
        json.dumps(
            {
                "status": result.status,
                "stop_reason": result.stop_reason,
                "provider_requests": result.provider_requests,
                "result_path": str(result.result_path),
            },
            indent=2,
        )
    )
    return 0 if result.status == "succeeded" else 1


def _campaign_controls(args: argparse.Namespace) -> int:
    try:
        contract = load_campaign_contract(args.contract, args.cases_root)
        runner = CampaignRunner(contract, args.cases_root)
        runner.preflight_control_matrix(args.run_root)
        result = runner.run_control_matrix(
            FakeProvider(runner.control_scripts()), args.run_root, preflighted=True
        )
    except (
        CaseValidationError,
        CampaignValidationError,
        OSError,
        ValueError,
    ) as exc:
        print(json.dumps({"status": "configuration_error", "error": str(exc)}))
        return 2
    print(
        json.dumps(
            {
                "status": result.status,
                "stop_reason": result.stop_reason,
                "provider_requests": result.provider_requests,
                "result_path": str(result.result_path),
            },
            indent=2,
        )
    )
    return 0 if result.status == "succeeded" else 1


def _campaign_held_out(args: argparse.Namespace) -> int:
    try:
        contract = load_campaign_contract(args.contract, args.cases_root)
        runner = CampaignRunner(contract, args.cases_root)
        runner.preflight_held_out(args.run_root)
        result = runner.run_held_out(
            FakeProvider(runner.held_out_scripts()), args.run_root, preflighted=True
        )
    except (CaseValidationError, CampaignValidationError, OSError, ValueError) as exc:
        print(json.dumps({"status": "configuration_error", "error": str(exc)}))
        return 2
    print(
        json.dumps(
            {
                "status": result.status,
                "stop_reason": result.stop_reason,
                "provider_requests": result.provider_requests,
                "result_path": str(result.result_path),
            },
            indent=2,
        )
    )
    return 0 if result.status == "succeeded" else 1


def _campaign_pilot(args: argparse.Namespace) -> int:
    try:
        contract = load_campaign_contract(args.contract, args.cases_root)
        scripts = [path.read_text(encoding="utf-8") for path in args.fake_script]
        if len(scripts) != contract.provider_policy["max_requests"]:
            raise CampaignValidationError(
                "number of --fake-script values must equal campaign max_requests"
            )
        result = CampaignRunner(contract, args.cases_root).run_pilot(
            FakeProvider(scripts), args.run_root
        )
    except (CaseValidationError, CampaignValidationError, OSError, ValueError) as exc:
        print(json.dumps({"status": "configuration_error", "error": str(exc)}))
        return 2
    print(
        json.dumps(
            {
                "status": result.status,
                "stop_reason": result.stop_reason,
                "provider_requests": result.provider_requests,
                "result_path": str(result.result_path),
            },
            indent=2,
        )
    )
    return 0 if result.status == "succeeded" else 1


def _campaign_pilot_validate(args: argparse.Namespace) -> int:
    try:
        contract = load_campaign_contract(args.contract, args.cases_root)
        pilot = _read_json_object(args.result)
        result_root = args.result.parent
        runtime = _read_json_object(result_root / "runtime" / "result.json")
        controls = _read_json_object(result_root / "controls" / "result.json")
        held_out = _read_json_object(result_root / "held-out" / "result.json")
        validate_pilot_result(
            pilot,
            contract,
            runtime_payload=runtime,
            control_matrix_payload=controls,
            held_out_payload=held_out,
        )
    except (CaseValidationError, CampaignValidationError, OSError, ValueError) as exc:
        print(json.dumps({"status": "invalid", "error": str(exc)}))
        return 1
    print(
        json.dumps(
            {
                "status": "valid",
                "campaign_id": contract.campaign_id,
                "contract_sha256": contract.sha256,
                "provider_requests": pilot["provider_requests"],
                "result_path": str(args.result),
            },
            indent=2,
        )
    )
    return 0


def _campaign_pilot_preflight(args: argparse.Namespace) -> int:
    try:
        contract = load_campaign_contract(args.contract, args.cases_root)
        _validate_hosted_pilot_arguments(args, contract.provider_policy)
        cohort_counts = CampaignRunner(contract, args.cases_root).preflight_pilot(args.run_root)
    except (CaseValidationError, CampaignValidationError, OSError, ValueError) as exc:
        print(json.dumps({"status": "not_ready", "error": str(exc)}))
        return 1
    print(
        json.dumps(
            {
                "status": "ready",
                "campaign_id": contract.campaign_id,
                "contract_sha256": contract.sha256,
                "run_root": str(args.run_root),
                "thinking_mode": args.thinking_mode,
                "cohorts": {
                    "runtime": {"provider": args.provider, "case_count": cohort_counts["runtime"]},
                    "control_matrix": {
                        "provider": "fake",
                        "case_count": cohort_counts["control_matrix"],
                    },
                    "held_out": {"provider": "fake", "case_count": cohort_counts["held_out"]},
                },
                "budget": _campaign_budget_summary(contract.provider_policy),
            },
            indent=2,
        )
    )
    return 0


def _campaign_hosted_pilot_validate(args: argparse.Namespace) -> int:
    try:
        contract = load_campaign_contract(args.contract, args.cases_root)
        pilot = _read_json_object(args.result)
        result_root = args.result.parent
        runtime = _read_json_object(result_root / "runtime" / "result.json")
        controls = _read_json_object(result_root / "controls" / "result.json")
        held_out = _read_json_object(result_root / "held-out" / "result.json")
        validate_hosted_pilot_result(
            pilot,
            contract,
            runtime_payload=runtime,
            control_matrix_payload=controls,
            held_out_payload=held_out,
        )
    except (CaseValidationError, CampaignValidationError, OSError, ValueError) as exc:
        print(json.dumps({"status": "invalid", "error": str(exc)}))
        return 1
    print(
        json.dumps(
            {
                "status": "valid",
                "campaign_id": contract.campaign_id,
                "contract_sha256": contract.sha256,
                "provider_routing": pilot["provider_routing"],
                "provider_requests": pilot["provider_requests"],
                "result_path": str(args.result),
            },
            indent=2,
        )
    )
    return 0


def _campaign_hosted_pilot(args: argparse.Namespace) -> int:
    try:
        contract = load_campaign_contract(args.contract, args.cases_root)
        _validate_hosted_pilot_arguments(args, contract.provider_policy)
        runner = CampaignRunner(contract, args.cases_root)
        runner.preflight_pilot(args.run_root)
        provider = _hosted_pilot_provider_from_args(args, contract.provider_policy)
        result = runner.run_hosted_pilot(provider, args.run_root, preflighted=True)
        payload = _read_json_object(result.result_path)
    except (
        CaseValidationError,
        CampaignValidationError,
        OSError,
        ProviderConfigurationError,
        ValueError,
    ) as exc:
        print(json.dumps({"status": "configuration_error", "error": str(exc)}))
        return 2
    print(
        json.dumps(
            {
                "status": result.status,
                "stop_reason": result.stop_reason,
                "provider_requests": result.provider_requests,
                "provider_accounting": payload["provider_accounting"],
                "result_path": str(result.result_path),
            },
            indent=2,
        )
    )
    return 0 if result.status == "succeeded" else 1


def _campaign_hosted_pilot_config_check(args: argparse.Namespace) -> int:
    try:
        contract = load_campaign_contract(args.contract, args.cases_root)
        _validate_hosted_pilot_arguments(args, contract.provider_policy)
        cohort_counts = CampaignRunner(contract, args.cases_root).preflight_pilot(args.run_root)
        provider = _hosted_pilot_provider_from_args(args, contract.provider_policy)
        endpoint_host = urlsplit(provider.config.base_url).hostname
        if not endpoint_host:
            raise ProviderConfigurationError("provider endpoint host is invalid")
    except (
        CaseValidationError,
        CampaignValidationError,
        OSError,
        ProviderConfigurationError,
        ValueError,
    ) as exc:
        print(json.dumps({"status": "not_ready", "error": str(exc)}))
        return 1
    print(
        json.dumps(
            {
                "status": "ready",
                "campaign_id": contract.campaign_id,
                "contract_sha256": contract.sha256,
                "provider": provider.name,
                "model": provider.model,
                "thinking_mode": args.thinking_mode,
                "endpoint_host": endpoint_host,
                "cohort_counts": cohort_counts,
                "budget": _campaign_budget_summary(contract.provider_policy),
            },
            indent=2,
        )
    )
    return 0


def _campaign_hosted_readiness(args: argparse.Namespace) -> int:
    gate_names = (
        "campaign_contract",
        "fake_pilot_baseline",
        "scope_validation",
        "fresh_run_root",
        "secure_backend",
        "provider_configuration",
    )
    gates = {name: "not_run" for name in gate_names}
    contract = None
    cohort_counts = None
    provider = None
    endpoint_host = None
    current_gate = "campaign_contract"
    try:
        contract = load_campaign_contract(args.contract, args.cases_root)
        _validate_hosted_contract_arguments(
            args,
            contract.provider_policy,
            require_authorization=args.check_provider_config,
        )
        gates[current_gate] = "passed"

        current_gate = "fake_pilot_baseline"
        _validate_saved_fake_pilot(args.baseline_result, contract)
        gates[current_gate] = "passed"

        current_gate = "scope_validation"
        runner = CampaignRunner(contract, args.cases_root)
        cohort_counts = runner.validate_pilot_scope()
        gates[current_gate] = "passed"

        current_gate = "fresh_run_root"
        if args.run_root.exists():
            raise CampaignValidationError("candidate hosted run root must be fresh")
        gates[current_gate] = "passed"

        current_gate = "secure_backend"
        runner.validate_secure_backend()
        gates[current_gate] = "passed"

        current_gate = "provider_configuration"
        if args.check_provider_config:
            provider = _hosted_pilot_provider_from_args(args, contract.provider_policy)
            endpoint_host = urlsplit(provider.config.base_url).hostname
            if not endpoint_host:
                raise ProviderConfigurationError("provider endpoint host is invalid")
            gates[current_gate] = "passed"
        else:
            gates[current_gate] = "skipped"
    except FileNotFoundError:
        gates[current_gate] = "failed"
        return _print_readiness_failure(gates, current_gate, "required saved result is missing")
    except (
        CaseValidationError,
        CampaignValidationError,
        OSError,
        ProviderConfigurationError,
        ValueError,
    ) as exc:
        gates[current_gate] = "failed"
        return _print_readiness_failure(gates, current_gate, _safe_readiness_error(exc))

    print(
        json.dumps(
            {
                "status": "ready",
                "campaign_id": contract.campaign_id,
                "contract_sha256": contract.sha256,
                "gates": gates,
                "cohort_counts": cohort_counts,
                "provider": provider.name if provider is not None else args.provider,
                "model": provider.model if provider is not None else args.model,
                "thinking_mode": args.thinking_mode,
                "endpoint_host": endpoint_host,
                "budgets": _campaign_budget_summary(contract.provider_policy),
                "network_requests": 0,
                "artifacts_created": False,
            },
            indent=2,
        )
    )
    return 0


def _validate_saved_fake_pilot(result_path: Path, contract) -> None:
    pilot = _read_json_object(result_path)
    result_root = result_path.parent
    validate_pilot_result(
        pilot,
        contract,
        runtime_payload=_read_json_object(result_root / "runtime" / "result.json"),
        control_matrix_payload=_read_json_object(result_root / "controls" / "result.json"),
        held_out_payload=_read_json_object(result_root / "held-out" / "result.json"),
    )


def _print_readiness_failure(gates: dict[str, str], gate: str, error: str) -> int:
    print(
        json.dumps(
            {
                "status": "not_ready",
                "failed_gate": gate,
                "error": error,
                "gates": gates,
                "network_requests": 0,
                "artifacts_created": False,
            },
            indent=2,
        )
    )
    return 1


def _safe_readiness_error(exc: Exception) -> str:
    if isinstance(exc, OSError):
        return "readiness input could not be read"
    message = str(exc)
    if isinstance(exc, ProviderConfigurationError):
        if "HTTPS" in message:
            return "provider endpoint must use HTTPS"
        if "required" in message:
            return "provider and API key are required"
        if "endpoint host" in message:
            return "provider endpoint host is invalid"
        return "provider configuration is invalid"
    return re.sub(r"[A-Za-z]:[\\/][^\s\"']+", "<redacted-path>", message)


def _read_json_object(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON artifact must be an object: {path}")
    return payload


def _run(args: argparse.Namespace) -> int:
    try:
        manifests = validate_catalog(args.cases_root)
        campaign_record = None
        if args.campaign_contract is not None:
            campaign = load_campaign_contract(args.campaign_contract, args.cases_root)
            campaign_case = campaign.select_case(args.case_id, runtime_only=True)
            policy = campaign.provider_policy
            if args.max_rounds != policy["max_rounds"]:
                raise CampaignValidationError("--max-rounds must match the campaign contract")
            if args.timeout != policy["build_timeout_seconds"]:
                raise CampaignValidationError("--timeout must match the campaign contract")
            campaign_record = {
                "campaign_id": campaign.campaign_id,
                "contract_sha256": campaign.sha256,
                "case": asdict(campaign_case),
            }
        case = _select_case(manifests, args.case_id, runtime_only=True)
        provider = _provider_from_args(args)
        if args.campaign_contract is not None and args.provider == "deepseek":
            _validate_hosted_campaign_policy(args, campaign.provider_policy, provider)
        initial_script = (
            args.initial_script.read_text(encoding="utf-8") if args.initial_script else None
        )
        if initial_script is not None and not initial_script.strip():
            raise CaseValidationError("--initial-script must contain a non-empty Python script")
        result = RepairLoopRunner(provider).run(
            case,
            args.run_root,
            max_rounds=args.max_rounds,
            timeout_seconds=args.timeout,
            initial_script=initial_script,
            campaign=campaign_record,
        )
    except (
        CaseValidationError,
        CampaignValidationError,
        OSError,
        ProviderConfigurationError,
        ValueError,
    ) as exc:
        print(json.dumps({"status": "configuration_error", "error": str(exc)}))
        return 2
    print(
        json.dumps(
            {
                "status": result.status,
                "stop_reason": result.stop_reason,
                "provider_requests": result.provider_requests,
                "result_path": str(result.result_path),
            },
            indent=2,
        )
    )
    return 0 if result.status == "succeeded" else 1


def _active_run(args: argparse.Namespace) -> int:
    try:
        case, actions, budgets = _active_configuration(args)
        if args.run_root.exists():
            raise CaseValidationError("active run root must be fresh")
        result = ActiveHarnessRunner(FakeActionProvider(actions)).run(
            case,
            args.run_root,
            budgets=budgets,
            timeout_seconds=args.timeout,
        )
    except (CaseValidationError, OSError, ValueError) as exc:
        print(json.dumps({"status": "configuration_error", "error": str(exc)}))
        return 2
    print(
        json.dumps(
            {
                "status": result.state,
                "stop_reason": result.stop_reason,
                "usage": result.usage,
                "result_path": str(args.run_root / "result.json"),
            },
            indent=2,
        )
    )
    return 0 if result.state == "succeeded" else 1


def _active_preflight(args: argparse.Namespace) -> int:
    try:
        case, actions, budgets = _active_configuration(args)
        if args.run_root.exists():
            raise CaseValidationError("active run root must be fresh")
    except (CaseValidationError, OSError, ValueError) as exc:
        print(json.dumps({"status": "not_ready", "error": str(exc)}))
        return 1
    print(
        json.dumps(
            {
                "status": "ready",
                "case_id": case.case.case_id,
                "provider": "fake",
                "action_count": len(actions),
                "budgets": asdict(budgets),
                "timeout_seconds": args.timeout,
                "network_requests": 0,
                "artifacts_created": False,
            },
            indent=2,
        )
    )
    return 0


def _active_validate(args: argparse.Namespace) -> int:
    try:
        payload = _read_json_object(args.result)
        case_id = payload.get("case_id")
        if not isinstance(case_id, str):
            raise ActiveResultValidationError("active result case_id is invalid")
        case = _select_case(validate_catalog(args.cases_root), case_id, runtime_only=False)
        validate_active_result(payload, case, args.result.parent)
    except (ActiveResultValidationError, CaseValidationError, OSError, ValueError) as exc:
        print(json.dumps({"status": "invalid", "error": str(exc)}))
        return 1
    print(
        json.dumps(
            {
                "status": "valid",
                "case_id": case_id,
                "result_path": str(args.result),
                "terminal_state": payload["state"],
                "stop_reason": payload["stop_reason"],
            },
            indent=2,
        )
    )
    return 0


def _active_continue(args: argparse.Namespace) -> int:
    try:
        case = _select_case(
            validate_catalog(args.cases_root), args.case_id, runtime_only=False
        )
        payload = _read_json_object(args.run_root / "result.json")
        validate_active_result(payload, case, args.run_root)
        budgets = _active_budgets(args)
        actions = [_read_json_object(path) for path in args.fake_action]
        for action in actions:
            HarnessAction.parse(action)
        remaining_requests = budgets.model_requests - payload["usage"]["model_requests"]
        if len(actions) != remaining_requests:
            raise ActiveResultValidationError(
                "number of --fake-action values must equal remaining model requests"
            )
        _validate_action_capacity(actions, budgets, payload["usage"])
        if args.timeout < 1:
            raise CaseValidationError("--timeout must be positive")
        result = ActiveHarnessRunner(FakeActionProvider(actions)).continue_run(
            case,
            args.run_root,
            budgets=budgets,
            timeout_seconds=args.timeout,
        )
    except (
        ActiveResultValidationError,
        CaseValidationError,
        OSError,
        ValueError,
    ) as exc:
        print(json.dumps({"status": "continuation_error", "error": str(exc)}))
        return 2
    print(
        json.dumps(
            {
                "status": result.state,
                "stop_reason": result.stop_reason,
                "usage": result.usage,
                "result_path": str(args.run_root / "result.json"),
            },
            indent=2,
        )
    )
    return 0 if result.state == "succeeded" else 1


def _active_hosted_preflight(args: argparse.Namespace) -> int:
    try:
        plan, _ = _active_hosted_plan(args)
    except (ActiveResultValidationError, CaseValidationError, OSError, ValueError) as exc:
        print(json.dumps({"status": "not_ready", "error": str(exc)}))
        return 1
    print(
        json.dumps(
            {
                "status": "ready",
                **plan,
                "network_requests": 0,
                "provider_configuration_read": False,
                "artifacts_created": False,
            },
            indent=2,
        )
    )
    return 0


def _active_hosted_config_check(args: argparse.Namespace) -> int:
    try:
        plan, provider_limits = _active_hosted_plan(args)
        provider = OpenAICompatibleProvider(
            deepseek_config_from_env(
                env_file=Path(".env"), thinking_mode=args.thinking_mode
            ),
            provider_limits,
        )
        if provider.name != args.provider or provider.model != args.model:
            raise ActiveResultValidationError(
                "active hosted provider identity does not match declared plan"
            )
        endpoint_host = urlsplit(provider.config.base_url).hostname
        if not endpoint_host:
            raise ProviderConfigurationError("provider endpoint host is invalid")
    except (
        ActiveResultValidationError,
        CaseValidationError,
        OSError,
        ProviderConfigurationError,
        ValueError,
    ) as exc:
        print(json.dumps({"status": "not_ready", "error": _safe_readiness_error(exc)}))
        return 1
    print(
        json.dumps(
            {
                "status": "ready",
                **plan,
                "endpoint_host": endpoint_host,
                "network_requests": 0,
                "provider_configuration_read": True,
                "artifacts_created": False,
            },
            indent=2,
        )
    )
    return 0


def _active_hosted_readiness(args: argparse.Namespace) -> int:
    gate_names = (
        "case_session_scope",
        "fake_active_baseline",
        "saved_result_validation",
        "run_root",
        "budget_binding",
        "outbound_projection_authorization",
        "secure_backend",
        "provider_configuration",
    )
    gates = dict.fromkeys(gate_names, "skipped")
    current_gate = gate_names[0]
    endpoint_host = None
    try:
        case = _select_case(
            validate_catalog(args.cases_root), args.case_id, runtime_only=True
        )
        continuation_payload = None
        if args.continuation_result is not None:
            continuation_payload = _read_json_object(args.continuation_result)
        gates[current_gate] = "passed"

        current_gate = "fake_active_baseline"
        baseline = _read_json_object(args.baseline_result)
        if baseline.get("provider") != "fake" or baseline.get("terminal") is not True:
            raise ActiveResultValidationError(
                "active hosted readiness requires a terminal fake active baseline"
            )
        if baseline.get("state") != "succeeded":
            raise ActiveResultValidationError("fake active baseline did not succeed")
        gates[current_gate] = "passed"

        current_gate = "saved_result_validation"
        if baseline.get("case_id") != case.case.case_id:
            raise ActiveResultValidationError("fake active baseline case_id drift")
        validate_active_result(baseline, case, args.baseline_result.parent)
        if continuation_payload is not None:
            validate_active_result(
                continuation_payload, case, args.continuation_result.parent
            )
        gates[current_gate] = "passed"

        current_gate = "run_root"
        if continuation_payload is None:
            if args.run_root.exists():
                raise ActiveResultValidationError("active hosted run root must be fresh")
        elif args.continuation_result != args.run_root / "result.json":
            raise ActiveResultValidationError(
                "active hosted continuation must reuse its run root"
            )
        gates[current_gate] = "passed"

        current_gate = "budget_binding"
        budget_args = argparse.Namespace(**vars(args))
        budget_args.authorize_hosted = True
        budget_args.authorize_observations = True
        budget_args.authorize_tool_results = True
        budget_args.authorize_revision_source = True
        budget_args.authorize_feedback = True
        plan, provider_limits = _active_hosted_plan(budget_args)
        gates[current_gate] = "passed"

        current_gate = "outbound_projection_authorization"
        plan, provider_limits = _active_hosted_plan(args)
        if not all(plan["authorization"].values()):
            raise ActiveResultValidationError(
                "active hosted readiness requires fresh itemized authorization"
            )
        gates[current_gate] = "passed"

        current_gate = "secure_backend"
        ready, reason = secure_backend_status()
        if not ready:
            raise ActiveResultValidationError(reason)
        gates[current_gate] = "passed"

        current_gate = "provider_configuration"
        if args.check_provider_config:
            provider = OpenAICompatibleProvider(
                deepseek_config_from_env(
                    env_file=Path(".env"), thinking_mode=args.thinking_mode
                ),
                provider_limits,
            )
            if provider.name != args.provider or provider.model != args.model:
                raise ActiveResultValidationError(
                    "active hosted provider identity does not match declared plan"
                )
            endpoint_host = urlsplit(provider.config.base_url).hostname
            if not endpoint_host:
                raise ProviderConfigurationError("provider endpoint host is invalid")
            gates[current_gate] = "passed"
    except FileNotFoundError:
        gates[current_gate] = "failed"
        return _print_readiness_failure(
            gates, current_gate, "required saved result is missing"
        )
    except (
        ActiveResultValidationError,
        CaseValidationError,
        OSError,
        ProviderConfigurationError,
        ValueError,
    ) as exc:
        gates[current_gate] = "failed"
        return _print_readiness_failure(
            gates, current_gate, _safe_readiness_error(exc)
        )

    print(
        json.dumps(
            {
                "status": "ready",
                **plan,
                "gates": gates,
                "endpoint_host": endpoint_host,
                "network_requests": 0,
                "provider_configuration_read": args.check_provider_config,
                "artifacts_created": False,
            },
            indent=2,
        )
    )
    return 0


class _StubHTTPResponse:
    def __init__(self, payload: dict) -> None:
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *args) -> None:
        return None

    def read(self, unused_amount: int | None = None) -> bytes:
        return json.dumps(self.payload).encode("utf-8")


def _active_hosted_run(args: argparse.Namespace) -> int:
    if args.continuation_result is not None:
        print(
            json.dumps(
                {
                    "status": "configuration_error",
                    "error": "active-hosted-run requires a fresh initial run root",
                }
            )
        )
        return 2
    args.check_provider_config = True
    readiness_output = io.StringIO()
    with redirect_stdout(readiness_output):
        readiness_status = _active_hosted_readiness(args)
    if readiness_status != 0:
        print(readiness_output.getvalue(), end="")
        return readiness_status
    try:
        if not args.http_stub_response.resolve().is_relative_to(
            args.run_root.resolve().parent
        ):
            raise ActiveResultValidationError(
                "HTTP stub response must be an authorized artifact under the run-root parent"
            )
        stub_payload = _read_json_object(args.http_stub_response)
        case = _select_case(
            validate_catalog(args.cases_root), args.case_id, runtime_only=True
        )
        plan, provider_limits = _active_hosted_plan(args)
        provider = OpenAICompatibleProvider(
            deepseek_config_from_env(
                env_file=Path(".env"), thinking_mode=args.thinking_mode
            ),
            provider_limits,
            opener=lambda *unused_args, **unused_kwargs: _StubHTTPResponse(stub_payload),
        )
        if provider.name != plan["provider"] or provider.model != plan["model"]:
            raise ActiveResultValidationError(
                "active hosted provider identity does not match declared plan"
            )
        result = ActiveHarnessRunner(provider).run(
            case,
            args.run_root,
            budgets=ActiveBudgets(**plan["controller_budget"]),
            timeout_seconds=args.build_timeout,
        )
        payload = _read_json_object(args.run_root / "result.json")
        validate_active_result(payload, case, args.run_root)
    except (
        ActiveResultValidationError,
        CaseValidationError,
        OSError,
        ProviderConfigurationError,
        ValueError,
    ) as exc:
        print(
            json.dumps(
                {"status": "configuration_error", "error": _safe_readiness_error(exc)}
            )
        )
        return 2
    print(
        json.dumps(
            {
                "status": result.state,
                "stop_reason": result.stop_reason,
                "usage": payload["usage"],
                "provider_accounting": payload["provider_accounting"],
                "result_path": str(args.run_root / "result.json"),
                "network_requests": 0,
                "http_stub": True,
            },
            indent=2,
        )
    )
    return 0 if result.state == "succeeded" else 1


def _active_hosted_live_run(args: argparse.Namespace) -> int:
    if args.continuation_result is not None:
        print(
            json.dumps(
                {
                    "status": "configuration_error",
                    "error": "active-hosted-live-run requires a fresh initial run root",
                }
            )
        )
        return 2
    args.check_provider_config = True
    readiness_output = io.StringIO()
    with redirect_stdout(readiness_output):
        readiness_status = _active_hosted_readiness(args)
    if readiness_status != 0:
        print(readiness_output.getvalue(), end="")
        return readiness_status
    try:
        case = _select_case(
            validate_catalog(args.cases_root), args.case_id, runtime_only=True
        )
        plan, provider_limits = _active_hosted_plan(args)
        provider = OpenAICompatibleProvider(
            deepseek_config_from_env(
                env_file=Path(".env"), thinking_mode=args.thinking_mode
            ),
            provider_limits,
            exchange_recorder=_provider_exchange_recorder(args.run_root),
        )
        if provider.name != plan["provider"] or provider.model != plan["model"]:
            raise ActiveResultValidationError(
                "active hosted provider identity does not match declared plan"
            )
        result = ActiveHarnessRunner(provider).run(
            case,
            args.run_root,
            budgets=ActiveBudgets(**plan["controller_budget"]),
            timeout_seconds=args.build_timeout,
        )
        payload = _read_json_object(args.run_root / "result.json")
        validate_active_result(payload, case, args.run_root)
    except (
        ActiveResultValidationError,
        CaseValidationError,
        OSError,
        ProviderConfigurationError,
        ValueError,
    ) as exc:
        print(
            json.dumps(
                {"status": "configuration_error", "error": _safe_readiness_error(exc)}
            )
        )
        return 2
    print(
        json.dumps(
            {
                "status": result.state,
                "stop_reason": result.stop_reason,
                "usage": payload["usage"],
                "provider_accounting": payload["provider_accounting"],
                "result_path": str(args.run_root / "result.json"),
                "network_requests": payload["provider_accounting"]["http_attempts"],
                "http_stub": False,
                "fresh_authorization": True,
            },
            indent=2,
        )
    )
    return 0 if result.state == "succeeded" else 1


def _provider_exchange_recorder(run_root: Path):
    def record(event: str, attempt: int, payload: dict[str, object]) -> None:
        if event not in {"request", "response"} or attempt < 1:
            raise ValueError("provider exchange record is invalid")
        exchange_root = run_root / "provider-exchanges" / f"attempt-{attempt:03d}"
        exchange_root.mkdir(parents=True, exist_ok=True)
        target = exchange_root / f"{event}.json"
        temporary = target.with_suffix(".json.tmp")
        temporary.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        temporary.replace(target)

    return record


def _active_hosted_continue(args: argparse.Namespace) -> int:
    if args.continuation_result is None:
        print(
            json.dumps(
                {
                    "status": "configuration_error",
                    "error": "active-hosted-continue requires --continuation-result",
                }
            )
        )
        return 2
    args.check_provider_config = True
    readiness_output = io.StringIO()
    with redirect_stdout(readiness_output):
        readiness_status = _active_hosted_readiness(args)
    if readiness_status != 0:
        print(readiness_output.getvalue(), end="")
        return readiness_status
    try:
        if not args.http_stub_response.resolve().is_relative_to(
            args.run_root.resolve().parent
        ):
            raise ActiveResultValidationError(
                "HTTP stub response must be an authorized artifact under the run-root parent"
            )
        stub_payload = _read_json_object(args.http_stub_response)
        case = _select_case(
            validate_catalog(args.cases_root), args.case_id, runtime_only=True
        )
        plan, provider_limits = _active_hosted_plan(args)
        provider = OpenAICompatibleProvider(
            deepseek_config_from_env(
                env_file=Path(".env"), thinking_mode=args.thinking_mode
            ),
            provider_limits,
            opener=lambda *unused_args, **unused_kwargs: _StubHTTPResponse(stub_payload),
        )
        if provider.name != plan["provider"] or provider.model != plan["model"]:
            raise ActiveResultValidationError(
                "active hosted provider identity does not match declared plan"
            )
        result = ActiveHarnessRunner(provider).continue_run(
            case,
            args.run_root,
            budgets=ActiveBudgets(**plan["controller_budget"]),
            timeout_seconds=args.build_timeout,
        )
        payload = _read_json_object(args.run_root / "result.json")
        validate_active_result(payload, case, args.run_root)
    except (
        ActiveResultValidationError,
        CaseValidationError,
        OSError,
        ProviderConfigurationError,
        ValueError,
    ) as exc:
        print(
            json.dumps(
                {"status": "continuation_error", "error": _safe_readiness_error(exc)}
            )
        )
        return 2
    print(
        json.dumps(
            {
                "status": result.state,
                "stop_reason": result.stop_reason,
                "usage": payload["usage"],
                "provider_accounting": payload["provider_accounting"],
                "remaining_model_requests": (
                    plan["controller_budget"]["model_requests"]
                    - payload["usage"]["model_requests"]
                ),
                "result_path": str(args.run_root / "result.json"),
                "network_requests": 0,
                "http_stub": True,
                "fresh_authorization": True,
            },
            indent=2,
        )
    )
    return 0 if result.state == "succeeded" else 1


def _active_pilot_report(args: argparse.Namespace) -> int:
    try:
        if args.output.exists():
            raise ActiveResultValidationError("active pilot report output must be fresh")
        contract = load_campaign_contract(args.contract, args.cases_root)
        _validate_saved_fake_pilot(args.fixed_pilot_result, contract)
        fixed_pilot = _read_json_object(args.fixed_pilot_result)
        catalog = validate_catalog(args.cases_root)
        results = {}
        for label in ACTIVE_COHORT_LABELS:
            result_path = getattr(args, f"{label}_result")
            payload = _read_json_object(result_path)
            case_id = payload.get("case_id")
            if not isinstance(case_id, str):
                raise ActiveResultValidationError("active pilot result case_id is invalid")
            case = _select_case(catalog, case_id, runtime_only=False)
            validate_active_result(payload, case, result_path.parent)
            if payload["provider"] != "fake":
                raise ActiveResultValidationError("active pilot results must use fake provider")
            if label == "held_out":
                if case.case.split != "eval":
                    raise ActiveResultValidationError(
                        "active pilot held-out result must use an eval case"
                    )
            elif case.case.split == "eval":
                raise ActiveResultValidationError(
                    "active pilot non-held-out results cannot use eval cases"
                )
            if label != "controls" and case.metadata["capability_level"] != "L2":
                raise ActiveResultValidationError(
                    "active pilot L2 cohort result has wrong capability level"
                )
            results[label] = payload
        report = build_active_pilot_report(results, fixed_pilot)
        report["campaign_id"] = contract.campaign_id
        report["contract_sha256"] = contract.sha256
        args.output.parent.mkdir(parents=True, exist_ok=True)
        temporary = args.output.with_suffix(args.output.suffix + ".tmp")
        temporary.write_text(json.dumps(report, indent=2), encoding="utf-8")
        temporary.replace(args.output)
    except (
        ActiveResultValidationError,
        CampaignValidationError,
        CaseValidationError,
        OSError,
        ValueError,
    ) as exc:
        print(json.dumps({"status": "invalid", "error": _safe_readiness_error(exc)}))
        return 1
    print(
        json.dumps(
            {
                "status": report["status"],
                "stop_reason": report["stop_reason"],
                "eligible_to_request_single_pilot_authorization": report[
                    "hosted_pilot_decision_gate"
                ]["eligible_to_request_single_pilot_authorization"],
                "authorization_granted": False,
                "network_requests": 0,
                "result_path": str(args.output),
            },
            indent=2,
        )
    )
    return 0 if report["status"] == "succeeded" else 1


def _active_hosted_plan(
    args: argparse.Namespace,
) -> tuple[dict[str, object], ProviderLimits]:
    case = _select_case(validate_catalog(args.cases_root), args.case_id, runtime_only=True)
    budgets = ActiveBudgets(
        model_requests=args.max_model_requests,
        probes=args.max_probes,
        retrievals=args.max_retrievals,
        script_submissions=args.max_script_submissions,
        executions=args.max_executions,
        repairs=args.max_repairs,
        tokens=args.session_max_total_tokens,
        cost_usd=args.session_max_cost_usd,
    )
    provider_limits = ProviderLimits(
        max_requests=args.provider_max_requests,
        timeout_seconds=args.provider_timeout,
        max_retries=args.provider_max_retries,
        max_output_tokens=args.provider_max_output_tokens,
        max_total_tokens=args.provider_max_total_tokens,
        max_cost_usd=args.provider_max_cost_usd,
        input_cost_per_million=args.input_cost_per_million,
        output_cost_per_million=args.output_cost_per_million,
    )
    continuation_payload = None
    if args.continuation_result is not None:
        continuation_payload = _read_json_object(args.continuation_result)
    plan = preflight_active_hosted(
        case,
        args.run_root,
        provider=args.provider,
        model=args.model,
        thinking_mode=args.thinking_mode,
        budgets=budgets,
        build_timeout_seconds=args.build_timeout,
        provider_limits=provider_limits,
        authorization=ActiveHostedAuthorization(
            hosted=args.authorize_hosted,
            observations=args.authorize_observations,
            tool_results=args.authorize_tool_results,
            revision_source=args.authorize_revision_source,
            feedback=args.authorize_feedback,
        ),
        continuation_payload=continuation_payload,
        continuation_result=args.continuation_result,
    )
    return plan, provider_limits


def _active_configuration(
    args: argparse.Namespace,
) -> tuple[ValidatedCase, list[dict], ActiveBudgets]:
    case = _select_case(validate_catalog(args.cases_root), args.case_id, runtime_only=False)
    actions = [_read_json_object(path) for path in args.fake_action]
    if len(actions) != args.max_model_requests:
        raise CaseValidationError(
            "number of --fake-action values must equal --max-model-requests"
        )
    for action in actions:
        HarnessAction.parse(action)
    budgets = _active_budgets(args)
    _validate_action_capacity(actions, budgets)
    if args.timeout < 1:
        raise CaseValidationError("--timeout must be positive")
    return case, actions, budgets


def _active_budgets(args: argparse.Namespace) -> ActiveBudgets:
    return ActiveBudgets(
        model_requests=args.max_model_requests,
        probes=args.max_probes,
        retrievals=args.max_retrievals,
        script_submissions=args.max_script_submissions,
        executions=args.max_executions,
        repairs=args.max_repairs,
        tokens=args.max_total_tokens,
        cost_usd=args.max_cost_usd,
    )


def _validate_action_capacity(
    actions: list[dict],
    budgets: ActiveBudgets,
    usage: dict[str, int | float] | None = None,
) -> None:
    usage = usage or {name: 0 for name in asdict(budgets)}
    action_counts = {
        "probes": sum(action["action"] == "probe" for action in actions),
        "retrievals": sum(action["action"] == "retrieve" for action in actions),
        "script_submissions": sum(action["action"] == "submit" for action in actions),
    }
    for name, count in action_counts.items():
        if count > getattr(budgets, name) - usage[name]:
            raise CaseValidationError(f"fake action sequence exceeds {name} budget")


def _add_active_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--cases-root", type=Path, default=Path("cases"))
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--fake-action", type=Path, action="append", required=True)
    parser.add_argument("--max-model-requests", type=int, required=True)
    parser.add_argument("--max-probes", type=int, required=True)
    parser.add_argument("--max-retrievals", type=int, required=True)
    parser.add_argument("--max-script-submissions", type=int, required=True)
    parser.add_argument("--max-executions", type=int, required=True)
    parser.add_argument("--max-repairs", type=int, required=True)
    parser.add_argument("--max-total-tokens", type=int, required=True)
    parser.add_argument("--max-cost-usd", type=float, required=True)
    parser.add_argument("--timeout", type=int, default=30)


def _add_active_hosted_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--cases-root", type=Path, default=Path("cases"))
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--continuation-result", type=Path)
    parser.add_argument("--provider", choices=("deepseek",), required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--thinking-mode", choices=("disabled",), required=True)
    parser.add_argument("--authorize-hosted", action="store_true")
    parser.add_argument("--authorize-observations", action="store_true")
    parser.add_argument("--authorize-tool-results", action="store_true")
    parser.add_argument("--authorize-revision-source", action="store_true")
    parser.add_argument("--authorize-feedback", action="store_true")
    parser.add_argument("--max-model-requests", type=int, required=True)
    parser.add_argument("--max-probes", type=int, required=True)
    parser.add_argument("--max-retrievals", type=int, required=True)
    parser.add_argument("--max-script-submissions", type=int, required=True)
    parser.add_argument("--max-executions", type=int, required=True)
    parser.add_argument("--max-repairs", type=int, required=True)
    parser.add_argument("--session-max-total-tokens", type=int, required=True)
    parser.add_argument("--session-max-cost-usd", type=float, required=True)
    parser.add_argument("--build-timeout", type=int, required=True)
    parser.add_argument("--provider-max-requests", type=int, required=True)
    parser.add_argument("--provider-timeout", type=float, required=True)
    parser.add_argument("--provider-max-retries", type=int, required=True)
    parser.add_argument("--provider-max-output-tokens", type=int, required=True)
    parser.add_argument("--provider-max-total-tokens", type=int, required=True)
    parser.add_argument("--provider-max-cost-usd", type=float, required=True)
    parser.add_argument("--input-cost-per-million", type=float, required=True)
    parser.add_argument("--output-cost-per-million", type=float, required=True)


def _provider_from_args(args: argparse.Namespace):
    seeded_rounds = 1 if args.initial_script else 0
    provider_rounds = args.max_rounds - seeded_rounds
    if args.initial_script and args.max_rounds < 2:
        raise CaseValidationError("--initial-script requires --max-rounds of at least 2")
    if args.provider == "fake":
        scripts = [path.read_text(encoding="utf-8") for path in (args.fake_script or [])]
        if len(scripts) != provider_rounds:
            raise CaseValidationError(
                "number of --fake-script values must equal provider-generated rounds"
            )
        if args.authorize_hosted:
            raise CaseValidationError("--authorize-hosted is valid only with --provider deepseek")
        return FakeProvider(scripts)

    if not args.authorize_hosted:
        raise CaseValidationError(
            "hosted execution requires fresh explicit --authorize-hosted confirmation"
        )
    if args.fake_script:
        raise CaseValidationError("--fake-script cannot be used with --provider deepseek")
    _validate_disabled_thinking_mode(args.thinking_mode)
    if args.initial_script and not args.initial_script.resolve().is_relative_to(
        args.run_root.resolve().parent
    ):
        raise CaseValidationError(
            "hosted --initial-script must be an authorized artifact under the run-root parent"
        )
    names = (
        "max_requests",
        "provider_timeout",
        "max_retries",
        "max_output_tokens",
        "max_total_tokens",
        "max_cost_usd",
        "input_cost_per_million",
        "output_cost_per_million",
    )
    missing = [name.replace("_", "-") for name in names if getattr(args, name) is None]
    if missing:
        raise CaseValidationError(
            f"hosted execution requires explicit limits: {', '.join(missing)}"
        )
    maximum_attempts = provider_rounds * (1 + args.max_retries)
    if args.max_requests > maximum_attempts:
        raise CaseValidationError(
            f"max-requests exceeds the {maximum_attempts} attempt execution capacity"
        )
    if args.max_requests < provider_rounds:
        raise CaseValidationError("max-requests must cover every provider-generated round")
    limits = ProviderLimits(
        max_requests=args.max_requests,
        timeout_seconds=args.provider_timeout,
        max_retries=args.max_retries,
        max_output_tokens=args.max_output_tokens,
        max_total_tokens=args.max_total_tokens,
        max_cost_usd=args.max_cost_usd,
        input_cost_per_million=args.input_cost_per_million,
        output_cost_per_million=args.output_cost_per_million,
    )
    return OpenAICompatibleProvider(
        deepseek_config_from_env(
            env_file=Path(".env"), thinking_mode=args.thinking_mode
        ),
        limits,
    )


def _add_campaign_provider_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--provider", choices=("fake", "deepseek"), default="fake")
    parser.add_argument("--fake-script", type=Path, action="append")
    parser.add_argument("--authorize-hosted", action="store_true")
    parser.add_argument("--thinking-mode", choices=("disabled",))
    parser.add_argument("--max-requests", type=int)
    parser.add_argument("--provider-timeout", type=float)
    parser.add_argument("--max-retries", type=int)
    parser.add_argument("--max-output-tokens", type=int)
    parser.add_argument("--max-total-tokens", type=int)
    parser.add_argument("--max-cost-usd", type=float)
    parser.add_argument("--input-cost-per-million", type=float)
    parser.add_argument("--output-cost-per-million", type=float)


def _add_hosted_limit_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--thinking-mode", choices=("disabled",), required=True)
    parser.add_argument("--max-requests", type=int, required=True)
    parser.add_argument("--provider-timeout", type=float, required=True)
    parser.add_argument("--max-retries", type=int, required=True)
    parser.add_argument("--max-output-tokens", type=int, required=True)
    parser.add_argument("--max-total-tokens", type=int, required=True)
    parser.add_argument("--max-cost-usd", type=float, required=True)
    parser.add_argument("--input-cost-per-million", type=float, required=True)
    parser.add_argument("--output-cost-per-million", type=float, required=True)


def _add_hosted_pilot_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--cases-root", type=Path, default=Path("cases"))
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--provider", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--authorize-hosted", action="store_true")
    _add_hosted_limit_arguments(parser)


def _validate_hosted_pilot_arguments(args: argparse.Namespace, policy: dict) -> None:
    _validate_hosted_contract_arguments(args, policy, require_authorization=True)


def _validate_hosted_contract_arguments(
    args: argparse.Namespace, policy: dict, *, require_authorization: bool
) -> None:
    if require_authorization and not args.authorize_hosted:
        raise CampaignValidationError(
            "hosted pilot preflight requires explicit --authorize-hosted confirmation"
        )
    if args.provider != policy["provider"]:
        raise CampaignValidationError("--provider must match the campaign contract")
    if args.model != policy["model"]:
        raise CampaignValidationError("--model must match the campaign contract")
    _validate_disabled_thinking_mode(args.thinking_mode)
    bindings = {
        "max_requests": "max_requests",
        "provider_timeout": "provider_timeout_seconds",
        "max_retries": "max_retries",
        "max_output_tokens": "max_output_tokens",
        "max_total_tokens": "max_total_tokens",
        "max_cost_usd": "max_cost_usd",
        "input_cost_per_million": "input_cost_per_million",
        "output_cost_per_million": "output_cost_per_million",
    }
    for argument, contract_key in bindings.items():
        if getattr(args, argument) != policy[contract_key]:
            raise CampaignValidationError(
                f"--{argument.replace('_', '-')} must match the campaign contract"
            )


def _hosted_pilot_provider_from_args(args: argparse.Namespace, policy: dict):
    provider = OpenAICompatibleProvider(
        deepseek_config_from_env(
            env_file=Path(".env"), thinking_mode=args.thinking_mode
        ),
        ProviderLimits(
            max_requests=args.max_requests,
            timeout_seconds=args.provider_timeout,
            max_retries=args.max_retries,
            max_output_tokens=args.max_output_tokens,
            max_total_tokens=args.max_total_tokens,
            max_cost_usd=args.max_cost_usd,
            input_cost_per_million=args.input_cost_per_million,
            output_cost_per_million=args.output_cost_per_million,
        ),
    )
    if provider.name != policy["provider"] or provider.model != policy["model"]:
        raise CampaignValidationError(
            "hosted provider identity does not match the campaign contract"
        )
    return provider


def _campaign_provider_from_args(args: argparse.Namespace, contract):
    policy = contract.provider_policy
    if args.provider == "fake":
        scripts = [path.read_text(encoding="utf-8") for path in (args.fake_script or [])]
        if len(scripts) != policy["max_requests"]:
            raise CampaignValidationError(
                "number of --fake-script values must equal campaign max_requests"
            )
        if args.authorize_hosted:
            raise CampaignValidationError(
                "--authorize-hosted is valid only with --provider deepseek"
            )
        return FakeProvider(scripts)

    if not args.authorize_hosted:
        raise CampaignValidationError(
            "hosted execution requires fresh explicit --authorize-hosted confirmation"
        )
    if args.fake_script:
        raise CampaignValidationError("--fake-script cannot be used with --provider deepseek")
    _validate_disabled_thinking_mode(args.thinking_mode)
    bindings = {
        "max_requests": "max_requests",
        "provider_timeout": "provider_timeout_seconds",
        "max_retries": "max_retries",
        "max_output_tokens": "max_output_tokens",
        "max_total_tokens": "max_total_tokens",
        "max_cost_usd": "max_cost_usd",
        "input_cost_per_million": "input_cost_per_million",
        "output_cost_per_million": "output_cost_per_million",
    }
    missing = [name.replace("_", "-") for name in bindings if getattr(args, name) is None]
    if missing:
        raise CampaignValidationError(
            f"hosted execution requires explicit limits: {', '.join(missing)}"
        )
    for argument, contract_key in bindings.items():
        if getattr(args, argument) != policy[contract_key]:
            raise CampaignValidationError(
                f"--{argument.replace('_', '-')} must match the campaign contract"
            )
    provider = OpenAICompatibleProvider(
        deepseek_config_from_env(
            env_file=Path(".env"), thinking_mode=args.thinking_mode
        ),
        ProviderLimits(
            max_requests=args.max_requests,
            timeout_seconds=args.provider_timeout,
            max_retries=args.max_retries,
            max_output_tokens=args.max_output_tokens,
            max_total_tokens=args.max_total_tokens,
            max_cost_usd=args.max_cost_usd,
            input_cost_per_million=args.input_cost_per_million,
            output_cost_per_million=args.output_cost_per_million,
        ),
    )
    if provider.model != policy["model"]:
        raise CampaignValidationError("hosted model does not match the campaign contract")
    return provider


def _validate_hosted_campaign_policy(args: argparse.Namespace, policy: dict, provider) -> None:
    if provider.model != policy["model"]:
        raise CampaignValidationError("hosted model does not match the campaign contract")
    _validate_disabled_thinking_mode(args.thinking_mode)
    bindings = {
        "provider_timeout": "provider_timeout_seconds",
        "max_retries": "max_retries",
        "max_output_tokens": "max_output_tokens",
        "max_total_tokens": "max_total_tokens",
        "max_cost_usd": "max_cost_usd",
        "input_cost_per_million": "input_cost_per_million",
        "output_cost_per_million": "output_cost_per_million",
    }
    for argument, contract_key in bindings.items():
        if getattr(args, argument) != policy[contract_key]:
            raise CampaignValidationError(
                f"--{argument.replace('_', '-')} must match the campaign contract"
            )


def _validate_disabled_thinking_mode(value: str | None) -> None:
    if value != "disabled":
        raise CampaignValidationError(
            "hosted execution requires explicit --thinking-mode disabled"
        )


def _campaign_budget_summary(policy: dict) -> dict[str, dict[str, int | float]]:
    return {
        "campaign_aggregate": {
            "max_requests": policy["max_requests"],
            "max_total_tokens": policy["max_total_tokens"],
            "max_cost_usd": policy["max_cost_usd"],
        },
        "per_case": {
            "max_requests": policy["case_max_requests"],
            "max_total_tokens": policy["case_max_total_tokens"],
            "max_cost_usd": policy["case_max_cost_usd"],
        },
    }


def _select_case(manifests, case_id: str, *, runtime_only: bool = False) -> ValidatedCase:
    matches = [
        item
        for manifest in manifests
        for item in manifest.cases
        if item.case.case_id == case_id
        and (not runtime_only or item.case.split in {"smoke", "train"})
    ]
    if len(matches) != 1:
        scope = "runtime" if runtime_only else ""
        raise CaseValidationError(
            f"expected exactly one {scope} case named {case_id!r}".replace("  ", " ")
        )
    return matches[0]
