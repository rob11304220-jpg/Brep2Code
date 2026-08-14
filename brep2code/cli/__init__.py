"""Command line interface for Brep2Code."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import sys

from brep2code.agent.harness import ManualHarness, result_to_dict
from brep2code.asymmetric_campaign import (
    AsymmetricCampaignError,
    authorize_m182_execution,
    authorize_m179_execution,
    prepare as prepare_asymmetric_campaign,
    prepare_m179,
    prepare_m182,
    run_authorized_m182,
    run_authorized_m179,
    validate_execute_admission as validate_asymmetric_execute_admission,
    validate_m179_execute_admission,
    validate_m182_execute_admission,
)
from brep2code.campaign import CampaignError, prepare_campaign
from brep2code.agent.guidance import GuidanceBundle
from brep2code.agent.m97_observation import derive_m96_development_context, validate_m97_observation_context
from brep2code.agent.m135_epoch import (
    POLICY as M135_POLICY,
    authorize_execution_checkpoint,
    prepare_preflight_checkpoint,
    run_serial_epoch,
)
from brep2code.agent.observed_build import ObservationCall, ObservedBuildLoopRunner
from brep2code.agent.provider import (
    DeepSeekConfigurationError,
    DeepSeekProvider,
    FakeLLMProvider,
    LLMMessage,
    ProviderRequest,
    fake_replacement_response,
    fake_guidance_request,
)
from brep2code.agent.repair import (
    ProviderRequestLifecycleError,
    ProviderRequestTimeoutError,
    RepairLoopRunner,
    _complete_provider,
    repair_result_to_dict,
)
from brep2code.brep import (
    ProbeError,
    discover_input_file,
    load_model,
    probe_entity,
    probe_summary,
    probe_topology,
    sample_entity,
)
from brep2code.corpus import CaseManifest, CorpusRunner, load_case_manifest
from brep2code.corpus.report import write_corpus_report
from brep2code.corpus.runner import corpus_run_to_dict
from brep2code.cad import WslBubblewrapExecutor
from brep2code.monitor import MonitorError, observe_monitor, setup_monitor, teardown_monitor
from brep2code.storage import RecordStore


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.command == "run":
        return _run(args)
    if args.command == "probe":
        return _probe(args)
    if args.command == "repair":
        return _repair(args)
    if args.command == "corpus":
        return _corpus(args)
    if args.command == "observed-first-pass":
        return _observed_first_pass(args)
    if args.command == "reference-assisted-smoke":
        return _reference_assisted_smoke(args)
    if args.command == "reference-assisted-block-with-hole-smoke":
        return _reference_assisted_block_with_hole_smoke(args)
    if args.command == "reference-assisted-three-hole-plate-smoke":
        return _reference_assisted_three_hole_plate_smoke(args)
    if args.command == "reference-assisted-three-hole-plate-bounded-output-smoke":
        return _reference_assisted_three_hole_plate_bounded_output_smoke(args)
    if args.command == "reference-assisted-three-hole-plate-stability-smoke":
        return _reference_assisted_three_hole_plate_stability_smoke(args)
    if args.command == "reference-assisted-three-hole-plate-stability-reentry-smoke":
        return _reference_assisted_three_hole_plate_stability_reentry_smoke(args)
    if args.command == "reference-guided-through-hole-development-calibration":
        return _m97_development_calibration(args)
    if args.command == "observed-development":
        return _observed_development(args)
    if args.command == "provider-control":
        return _provider_control(args)
    if args.command == "m135-epoch-preflight":
        return _m135_epoch_preflight(args)
    if args.command == "m135-epoch-execute":
        return _m135_epoch_execute(args)
    if args.command == "campaign-prepare":
        return _campaign_prepare(args)
    if args.command == "m176-asymmetric-campaign-preflight":
        return _m176_asymmetric_campaign_preflight(args)
    if args.command == "m176-asymmetric-campaign-admission":
        return _m176_asymmetric_campaign_admission(args)
    if args.command == "m179-asymmetric-campaign-preflight":
        return _m179_asymmetric_campaign_preflight(args)
    if args.command == "m179-asymmetric-campaign-admission":
        return _m179_asymmetric_campaign_admission(args)
    if args.command == "m180-asymmetric-campaign-execute":
        return _m180_asymmetric_campaign_execute(args)
    if args.command == "m182-asymmetric-campaign-preflight":
        return _m182_asymmetric_campaign_preflight(args)
    if args.command == "m182-asymmetric-campaign-admission":
        return _m182_asymmetric_campaign_admission(args)
    if args.command == "m182-asymmetric-campaign-execute":
        return _m182_asymmetric_campaign_execute(args)
    if args.command == "monitor":
        return _monitor(args)
    parser.print_help()
    return 2


def _run(args: argparse.Namespace) -> int:
    store = RecordStore(args.data_root)
    harness = ManualHarness(store=store, executor=_executor_for(args))
    result = harness.run(
        record_id=args.record,
        script=Path(args.script) if args.script else None,
        timeout=args.timeout,
        input_path=Path(args.input) if args.input else None,
        build_without_input=args.build_without_input,
    )
    payload = result_to_dict(result)
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if result.status == "pass" else 1


def _probe(args: argparse.Namespace) -> int:
    store = RecordStore(args.data_root)
    trace_dir = None
    try:
        if args.input:
            input_path = Path(args.input)
        else:
            if not args.record:
                raise ProbeError("missing_input", "provide --input or --record")
            record = store.ensure_record(args.record)
            input_path = discover_input_file(record.input_dir)
            trace_dir = record.root / "traces"
        model = load_model(input_path)
        if args.tool == "summary":
            payload = probe_summary(model, trace_dir=trace_dir, limit_bytes=args.limit_bytes)
        elif args.tool == "topology":
            payload = probe_topology(
                model,
                selector=args.selector,
                max_entities=args.max_entities,
                trace_dir=trace_dir,
                limit_bytes=args.limit_bytes,
            )
        elif args.tool == "entity":
            payload = probe_entity(model, args.entity_id, trace_dir=trace_dir, limit_bytes=args.limit_bytes)
        elif args.tool == "sample":
            payload = sample_entity(
                model,
                args.entity_id,
                args.samples,
                trace_dir=trace_dir,
                limit_bytes=args.limit_bytes,
            )
        else:
            raise ProbeError("unknown_tool", f"unknown probe tool: {args.tool}")
    except ProbeError as exc:
        payload = exc.to_result()
    except (FileNotFoundError, ValueError) as exc:
        payload = {"ok": False, "error": {"code": exc.__class__.__name__, "message": str(exc)}}
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload.get("ok") else 1


def _repair(args: argparse.Namespace) -> int:
    store = RecordStore(args.data_root)
    if args.provider == "deepseek":
        try:
            provider = DeepSeekProvider.from_env_file(Path(args.env_file))
        except DeepSeekConfigurationError as exc:
            print(json.dumps({"status": "configuration_error", "error": str(exc)}, ensure_ascii=False))
            return 2
        harness = ManualHarness(store=store, executor=WslBubblewrapExecutor())
    else:
        if not args.fake_replacement_script:
            print(
                json.dumps(
                    {"status": "configuration_error", "error": "--fake-replacement-script is required for --provider fake"},
                    ensure_ascii=False,
                )
            )
            return 2
        replacement_script = Path(args.fake_replacement_script)
        replacement_content = replacement_script.read_text(encoding="utf-8")
        provider = FakeLLMProvider([fake_replacement_response(replacement_content)])
        harness = ManualHarness(store=store)
    runner = RepairLoopRunner(harness=harness, provider=provider)
    result = runner.run(
        record_id=args.record,
        initial_script=Path(args.script),
        input_path=Path(args.input) if args.input else None,
        max_rounds=args.max_rounds,
        timeout=args.timeout,
        provider_timeout=args.provider_timeout,
    )
    print(json.dumps(repair_result_to_dict(result), indent=2, ensure_ascii=False))
    return 0 if result.status == "pass" else 1


def _corpus(args: argparse.Namespace) -> int:
    data_root = Path(args.data_root)
    manifest = load_case_manifest(args.manifest)
    if args.case_id:
        try:
            manifest = _select_case(manifest, args.case_id)
        except ValueError as exc:
            print(json.dumps({"status": "configuration_error", "error": str(exc)}, ensure_ascii=False))
            return 2
    store = RecordStore(data_root)
    provider = None
    hosted_options: dict | None = None
    if args.provider == "deepseek":
        preflight_error = _hosted_corpus_preflight(args, manifest)
        if preflight_error is not None:
            print(json.dumps(preflight_error, ensure_ascii=False))
            return 2
        try:
            provider = DeepSeekProvider.from_env_file(Path(args.env_file))
        except DeepSeekConfigurationError as exc:
            print(json.dumps({"status": "configuration_error", "error": str(exc)}, ensure_ascii=False))
            return 2
        harness = ManualHarness(store=store, executor=WslBubblewrapExecutor())
        hosted_options = {
            "max_cases": args.max_cases,
            "max_rounds": args.max_rounds,
            "request_budget": args.request_budget,
            "provider_timeout": args.provider_timeout,
            "authorization": "explicit_cli_flag",
        }
    else:
        harness = ManualHarness(store=store, executor=_executor_for(args))
        if args.first_pass:
            missing = [case.case_id for case in manifest.cases if case.first_pass_script is None]
            if missing:
                print(
                    json.dumps(
                        {
                            "status": "configuration_error",
                            "error": f"--first-pass with --provider fake requires first_pass_script for: {', '.join(missing)}",
                        },
                        ensure_ascii=False,
                    )
                )
                return 2
            provider = FakeLLMProvider()
    runner = CorpusRunner(harness=harness)
    report_path = Path(args.report) if args.report else _default_corpus_report_path(data_root)
    result = runner.run(
        manifest,
        record_prefix=args.record_prefix,
        timeout=args.timeout,
        repair=args.repair,
        report_path=report_path,
        provider=provider,
        hosted_options=hosted_options,
        first_pass=args.first_pass,
    )
    print(json.dumps(corpus_run_to_dict(result), indent=2, ensure_ascii=False))
    return 0 if all(case.status == "pass" for case in result.cases) else 1


def _observed_first_pass(args: argparse.Namespace) -> int:
    store = RecordStore(args.data_root)
    if args.provider == "deepseek":
        if not args.authorize_hosted:
            print(json.dumps({"status": "authorization_required", "error": "--authorize-hosted is required"}))
            return 2
        if args.request_budget != 1:
            print(json.dumps({"status": "configuration_error", "error": "--request-budget must equal 1 for one observed first pass"}))
            return 2
        if args.provider_timeout < 1:
            print(json.dumps({"status": "configuration_error", "error": "--provider-timeout must be at least 1"}))
            return 2
        try:
            provider = DeepSeekProvider.from_env_file(Path(args.env_file))
        except DeepSeekConfigurationError as exc:
            print(json.dumps({"status": "configuration_error", "error": str(exc)}))
            return 2
        harness = ManualHarness(store=store, executor=WslBubblewrapExecutor())
        allow_hosted = True
    else:
        if not args.fake_replacement_script:
            print(json.dumps({"status": "configuration_error", "error": "--fake-replacement-script is required for --provider fake"}))
            return 2
        content = Path(args.fake_replacement_script).read_text(encoding="utf-8")
        provider = FakeLLMProvider([fake_replacement_response(content)])
        harness = ManualHarness(store=store)
        allow_hosted = False
    report_path = Path(args.report) if args.report else None
    policy = "q01-observation-build-v1"
    if args.phase == "prepare":
        if report_path is None:
            return _single_request_error("--report is required with --phase prepare")
        return _prepare_single_request(report_path, policy=policy, provider=provider.name, model=getattr(provider, "model", "fake-observation-build"))
    if args.phase == "execute":
        if report_path is None:
            return _single_request_error("--report is required with --phase execute")
        prepared = _load_prepared_single_request(report_path, policy)
        if prepared is None:
            return _single_request_error("report must be an existing prepared single-request checkpoint")

        def mark_issued() -> None:
            _mark_single_request_issued(report_path, prepared)

    else:
        mark_issued = None
    try:
        result = ObservedBuildLoopRunner(harness=harness, provider=provider, allow_hosted=allow_hosted).run(
            args.record,
            input_path=Path(args.input),
            observation_session_id=args.observation_session,
            observation_calls=[ObservationCall(call_id="summary-1", tool="probe_summary")],
            timeout=args.timeout,
            provider_timeout=args.provider_timeout,
            before_provider_request=mark_issued,
        )
    except (ProviderRequestTimeoutError, ProviderRequestLifecycleError) as exc:
        if report_path is not None and args.phase == "execute":
            payload = _terminal_single_request(
                _load_prepared_or_issued(report_path, policy),
                run_status="interrupted",
                interruption=_provider_interruption(args.record, exc),
            )
            write_corpus_report(report_path, payload)
            print(json.dumps(payload, indent=2, ensure_ascii=False))
            return 1
        raise
    payload = {"status": result.status, "provider_requests": result.provider_requests, "error": result.error}
    payload["telemetry"] = result.telemetry
    if result.harness_result is not None:
        payload["result"] = result_to_dict(result.harness_result)
    if report_path is not None:
        if args.phase == "execute":
            payload = _terminal_single_request(
                _load_prepared_or_issued(report_path, policy), run_status="completed", result=payload
            )
        write_corpus_report(report_path, payload)
        payload["report_path"] = str(report_path)
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if result.status == "pass" else 1


def _reference_assisted_smoke(args: argparse.Namespace) -> int:
    """Run M85's fixed two-request guidance then build state machine."""
    return _run_reference_assisted_smoke(
        args, milestone="M85", fixed_case="cylinder", fixed_role="final primitive", policy="m85-reference-assisted-v1"
    )


def _reference_assisted_block_with_hole_smoke(args: argparse.Namespace) -> int:
    """Run M87's fixed two-request single boolean-cut guidance smoke."""
    return _run_reference_assisted_smoke(
        args, milestone="M87", fixed_case="block_with_hole", fixed_role="single boolean-cut tool", policy="m87-reference-assisted-block-with-hole-v1"
    )


def _reference_assisted_three_hole_plate_smoke(args: argparse.Namespace) -> int:
    """Run M89's fixed two-request repeated boolean-cut guidance smoke."""
    return _run_reference_assisted_smoke(
        args,
        milestone="M89",
        fixed_case="three_hole_plate",
        fixed_role="repeated boolean-cut tool",
        policy="m89-reference-assisted-three-hole-plate-v1",
    )


def _reference_assisted_three_hole_plate_bounded_output_smoke(args: argparse.Namespace) -> int:
    """Run M89-003's fixed two-request bounded-output smoke."""
    return _run_reference_assisted_smoke(
        args,
        milestone="M89-003",
        fixed_case="three_hole_plate",
        fixed_role="repeated boolean-cut tool",
        policy="m89-003-three-hole-plate-bounded-output-v1",
        required_max_output_tokens=4096,
    )


def _reference_assisted_three_hole_plate_stability_smoke(args: argparse.Namespace) -> int:
    """Run M118's fresh two-request stability-only smoke."""
    return _run_reference_assisted_smoke(
        args,
        milestone="M118",
        fixed_case="three_hole_plate",
        fixed_role="repeated boolean-cut tool",
        policy="m118-three-hole-plate-stability-v1",
        required_max_output_tokens=4096,
    )


def _reference_assisted_three_hole_plate_stability_reentry_smoke(args: argparse.Namespace) -> int:
    """Run M127's fresh two-request shared stability re-entry smoke."""
    return _run_reference_assisted_smoke(
        args,
        milestone="M127",
        fixed_case="three_hole_plate",
        fixed_role="repeated boolean-cut tool",
        policy="m127-three-hole-plate-stability-reentry-v1",
        required_max_output_tokens=4096,
    )


def _m97_development_calibration(args: argparse.Namespace) -> int:
    """Run M97's frozen development-only card/no-card calibration."""

    policy_path = Path(args.policy)
    try:
        policy = json.loads(policy_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return _single_request_error(f"invalid M97 policy: {exc}")
    if policy.get("policy_id") != "reference-guided-through-hole-variation-v1-m97-003" or policy.get("status") != "frozen_before_authorization":
        return _single_request_error("M97 requires the frozen M97-003 policy")
    case_ids = policy.get("scope", {}).get("case_ids")
    if not isinstance(case_ids, list) or len(case_ids) != 3 or args.request_budget != 9 or args.max_repair_rounds != 0:
        return _single_request_error("M97 requires exactly three frozen development rows, nine requests and zero repair")
    root = Path(__file__).resolve().parents[2]
    record = json.loads((root / "docs/corpus/sequence-paired/reference-guided-through-hole-variation-v1-preregistration.json").read_text(encoding="utf-8"))
    rows = {entry["case_id"]: entry for entry in record["cases"]}
    if set(case_ids) - rows.keys() or any(rows[case_id].get("data_split") != "development" for case_id in case_ids):
        return _single_request_error("M97 policy development rows do not match the frozen preregistration")
    bundle = GuidanceBundle.from_paths(Path(args.guidance_index), Path(args.guidance_card))
    if bundle.index_sha256 != policy["guidance"]["index_sha256"] or bundle.card_sha256 != policy["guidance"]["card_sha256"]:
        return _single_request_error("M97 guidance hash drift")

    if args.provider == "deepseek":
        return _run_m97_hosted_calibration(args, case_ids=case_ids, rows=rows, bundle=bundle)

    store = RecordStore(args.data_root)
    results = []
    for case_id in case_ids:
        entry = rows[case_id]
        directory = root / entry["candidate_directory"]
        input_path = directory / "input.step"
        try:
            context = derive_m96_development_context(entry, root=root)
            validate_m97_observation_context(context)
        except (KeyError, OSError, ValueError) as exc:
            return _single_request_error(f"invalid M97 measured observation context: {exc}")
        script = (directory / "reference_build_sequence.py").read_text(encoding="utf-8")
        for condition in ("card", "baseline"):
            provider = FakeLLMProvider(
                [fake_guidance_request(role="single boolean-cut tool"), fake_replacement_response(script)]
                if condition == "card"
                else [fake_replacement_response(script)]
            )
            outcome = ObservedBuildLoopRunner(harness=ManualHarness(store=store), provider=provider).run(
                f"m97-{condition}-{case_id}", input_path=input_path,
                observation_session_id=f"m97-{condition}-{case_id}",
                observation_calls=[], observation_context=context,
                timeout=args.timeout, max_repair_rounds=0,
                guidance_bundle=bundle if condition == "card" else None,
                required_guidance_role="single boolean-cut tool" if condition == "card" else None,
            )
            results.append({"case_id": case_id, "condition": condition, "status": outcome.status, "provider_requests": outcome.provider_requests})
    if sum(item["provider_requests"] for item in results) != 9:
        return _single_request_error("M97 fake request accounting drift")
    payload = {"schema_version": 1, "policy": "m97-003-reference-guided-through-hole-development-v1", "provider": "fake", "requests_used": 9, "requests_remaining": 0, "run_status": "completed", "cases": results}
    if args.report:
        write_corpus_report(Path(args.report), payload)
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if all(item["status"] == "pass" for item in results) else 1


def _run_m97_hosted_calibration(
    args: argparse.Namespace, *, case_ids: list[str], rows: dict[str, dict], bundle: GuidanceBundle
) -> int:
    """Run M97 only from a fresh nine-request checkpoint after explicit CLI authorization."""

    policy = "m97-003-reference-guided-through-hole-development-v1"
    if not args.authorize_hosted:
        print(json.dumps({"status": "authorization_required", "error": "M97 hosted execution requires completed offline review, fresh preflight and itemized user authorization"}))
        return 2
    if args.phase is None:
        return _single_request_error("M97 hosted execution requires --phase prepare then --phase execute")
    if args.provider_timeout < 1:
        return _single_request_error("--provider-timeout must be at least 1")
    report_path = Path(args.report) if args.report else None
    if report_path is None:
        return _single_request_error("--report is required for M97 hosted execution")
    try:
        provider = DeepSeekProvider.from_env_file(Path(args.env_file))
    except DeepSeekConfigurationError as exc:
        print(json.dumps({"status": "configuration_error", "error": str(exc)}))
        return 2
    if args.phase == "prepare":
        return _prepare_m97_checkpoint(report_path, provider=provider.name, model=provider.model)
    prepared = _load_prepared_m97_checkpoint(report_path, policy)
    if prepared is None:
        return _single_request_error("report must be an existing prepared M97 checkpoint")

    issued = 0

    def mark_issued() -> None:
        nonlocal issued
        issued += 1
        _mark_m97_issued(report_path, policy, issued)

    root = Path(__file__).resolve().parents[2]
    harness = ManualHarness(store=RecordStore(args.data_root), executor=WslBubblewrapExecutor())
    results: list[dict] = []
    try:
        for case_id in case_ids:
            entry = rows[case_id]
            input_path = root / entry["candidate_directory"] / "input.step"
            context = derive_m96_development_context(entry, root=root)
            validate_m97_observation_context(context)
            for condition in ("card", "baseline"):
                outcome = ObservedBuildLoopRunner(harness=harness, provider=provider, allow_hosted=True).run(
                    f"m97-{condition}-{case_id}",
                    input_path=input_path,
                    observation_session_id=f"m97-{condition}-{case_id}",
                    observation_calls=[], observation_context=context,
                    timeout=args.timeout,
                    provider_timeout=args.provider_timeout,
                    max_repair_rounds=0,
                    guidance_bundle=bundle if condition == "card" else None,
                    required_guidance_role="single boolean-cut tool" if condition == "card" else None,
                    before_provider_request=mark_issued,
                )
                results.append({"case_id": case_id, "condition": condition, "status": outcome.status, "provider_requests": outcome.provider_requests})
    except (ProviderRequestTimeoutError, ProviderRequestLifecycleError) as exc:
        payload = _terminal_m97_checkpoint(
            _load_m97_checkpoint(report_path, policy),
            run_status="interrupted",
            cases=results,
            interruption=_provider_interruption("m97-development-calibration", exc),
        )
        write_corpus_report(report_path, payload)
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 1
    payload = _terminal_m97_checkpoint(
        _load_m97_checkpoint(report_path, policy), run_status="completed", cases=results
    )
    write_corpus_report(report_path, payload)
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if issued == 9 and all(item["status"] == "pass" for item in results) else 1


def _prepare_m97_checkpoint(report_path: Path, *, provider: str, model: str) -> int:
    if report_path.exists():
        return _single_request_error("report path must be fresh for a prepared M97 checkpoint")
    payload = {
        "schema_version": 1,
        "policy": "m97-003-reference-guided-through-hole-development-v1",
        "run_status": "running",
        "request_state": "prepared",
        "provider": provider,
        "model": model,
        "requests_used": 0,
        "requests_remaining": 9,
    }
    write_corpus_report(report_path, payload)
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def _load_prepared_m97_checkpoint(report_path: Path, policy: str) -> dict | None:
    try:
        payload = json.loads(report_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return None
    if not isinstance(payload, dict) or payload.get("schema_version") != 1 or payload.get("policy") != policy:
        return None
    if payload.get("run_status") != "running" or payload.get("request_state") != "prepared":
        return None
    if payload.get("requests_used") != 0 or payload.get("requests_remaining") != 9:
        return None
    return payload


def _load_m97_checkpoint(report_path: Path, policy: str) -> dict:
    payload = json.loads(report_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or payload.get("policy") != policy or payload.get("run_status") != "running":
        raise ValueError("M97 checkpoint changed unexpectedly")
    if payload.get("request_state") not in {"prepared", "issued"}:
        raise ValueError("M97 checkpoint request state changed unexpectedly")
    used = payload.get("requests_used")
    if not isinstance(used, int) or isinstance(used, bool) or not 0 <= used <= 9 or payload.get("requests_remaining") != 9 - used:
        raise ValueError("M97 checkpoint accounting changed unexpectedly")
    return payload


def _mark_m97_issued(report_path: Path, policy: str, count: int) -> None:
    if not 1 <= count <= 9:
        raise ValueError("M97 issued-request count exceeded nine")
    current = _load_m97_checkpoint(report_path, policy)
    if current["requests_used"] != count - 1:
        raise ValueError("M97 checkpoint request accounting changed unexpectedly")
    write_corpus_report(report_path, {**current, "request_state": "issued", "requests_used": count, "requests_remaining": 9 - count})


def _terminal_m97_checkpoint(
    base: dict, *, run_status: str, cases: list[dict], interruption: dict | None = None
) -> dict:
    payload = {**base, "run_status": run_status, "cases": cases}
    if interruption is not None:
        payload["interruption"] = interruption
    return payload


def _run_reference_assisted_smoke(
    args: argparse.Namespace,
    *,
    milestone: str,
    fixed_case: str,
    fixed_role: str,
    policy: str,
    required_max_output_tokens: int | None = None,
) -> int:
    max_output_tokens = getattr(args, "max_output_tokens", None)
    if args.case_id != fixed_case or args.guidance_role != fixed_role:
        return _single_request_error(f"{milestone} is fixed to {fixed_case} / {fixed_role}")
    if args.request_budget != 2 or args.max_repair_rounds != 0:
        return _single_request_error(f"{milestone} requires exactly two requests and zero repair rounds")
    if args.provider_timeout < 1:
        return _single_request_error("--provider-timeout must be at least 1")
    if required_max_output_tokens is not None and max_output_tokens != required_max_output_tokens:
        return _single_request_error(f"{milestone} requires --max-output-tokens {required_max_output_tokens}")
    bundle = GuidanceBundle.from_paths(Path(args.guidance_index), Path(args.guidance_card))
    store = RecordStore(args.data_root)
    if args.provider == "deepseek":
        if not args.authorize_hosted:
            print(json.dumps({"status": "authorization_required", "error": "--authorize-hosted is required"}))
            return 2
        if args.phase is None:
            return _single_request_error(f"hosted {milestone} requires --phase prepare then --phase execute")
        try:
            provider = DeepSeekProvider.from_env_file(Path(args.env_file))
        except DeepSeekConfigurationError as exc:
            print(json.dumps({"status": "configuration_error", "error": str(exc)}))
            return 2
        harness = ManualHarness(store=store, executor=WslBubblewrapExecutor())
        allow_hosted = True
    else:
        if not args.fake_replacement_script:
            return _single_request_error("--fake-replacement-script is required for --provider fake")
        provider = FakeLLMProvider([
            fake_guidance_request(role=args.guidance_role),
            fake_replacement_response(Path(args.fake_replacement_script).read_text(encoding="utf-8")),
        ])
        harness = ManualHarness(store=store)
        allow_hosted = False
    report_path = Path(args.report) if args.report else None
    if args.phase == "prepare":
        if report_path is None:
            return _single_request_error("--report is required with --phase prepare")
        return _prepare_two_request(
            report_path,
            policy=policy,
            provider=provider.name,
            model=getattr(provider, "model", "fake-reference-assisted"),
            max_output_tokens=max_output_tokens,
        )
    issued = 0
    if args.phase == "execute":
        if report_path is None:
            return _single_request_error("--report is required with --phase execute")
        prepared = _load_prepared_two_request(report_path, policy)
        if prepared is None:
            return _single_request_error("report must be an existing prepared two-request checkpoint")

        def mark_issued() -> None:
            nonlocal issued
            issued += 1
            _mark_two_request_issued(report_path, prepared, issued)
    else:
        mark_issued = None
    try:
        result = ObservedBuildLoopRunner(harness=harness, provider=provider, allow_hosted=allow_hosted).run(
            args.record, input_path=Path(args.input), observation_session_id=args.observation_session,
            observation_calls=[ObservationCall(call_id="summary-1", tool="probe_summary")], timeout=args.timeout,
            provider_timeout=args.provider_timeout, max_output_tokens=max_output_tokens,
            max_repair_rounds=0, guidance_bundle=bundle,
            required_guidance_role=args.guidance_role, before_provider_request=mark_issued,
        )
    except (ProviderRequestTimeoutError, ProviderRequestLifecycleError) as exc:
        if report_path is not None and args.phase == "execute":
            payload = _terminal_two_request(_load_two_request_state(report_path, policy), run_status="interrupted", interruption=_provider_interruption(args.record, exc))
            write_corpus_report(report_path, payload)
            print(json.dumps(payload, indent=2, ensure_ascii=False))
            return 1
        raise
    payload = {"status": result.status, "provider_requests": result.provider_requests, "error": result.error, "telemetry": result.telemetry}
    if result.harness_result is not None:
        payload["result"] = result_to_dict(result.harness_result)
    if report_path is not None:
        report = _terminal_two_request(_load_two_request_state(report_path, policy), run_status="completed", result=payload) if args.phase == "execute" else {"schema_version": 1, "policy": policy, "request_budget": 2, "requests_used": result.provider_requests, "run_status": "completed", "result": payload}
        write_corpus_report(report_path, report)
        payload["report_path"] = str(report_path)
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if result.status == "pass" else 1


def _prepare_two_request(
    report_path: Path, *, policy: str, provider: str, model: str, max_output_tokens: int | None = None
) -> int:
    if report_path.exists():
        return _single_request_error("report path must be fresh for a prepared two-request checkpoint")
    payload = {"schema_version": 1, "policy": policy, "run_status": "running", "request_state": "prepared", "provider": provider, "model": model, "max_output_tokens": max_output_tokens, "requests_used": 0, "requests_remaining": 2}
    write_corpus_report(report_path, payload)
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def _load_prepared_two_request(report_path: Path, policy: str) -> dict | None:
    try:
        payload = json.loads(report_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return None
    if not isinstance(payload, dict) or payload.get("schema_version") != 1 or payload.get("policy") != policy:
        return None
    if payload.get("run_status") != "running" or payload.get("request_state") != "prepared" or payload.get("requests_used") != 0 or payload.get("requests_remaining") != 2:
        return None
    return payload


def _load_two_request_state(report_path: Path, policy: str) -> dict:
    payload = json.loads(report_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or payload.get("policy") != policy or payload.get("run_status") != "running":
        raise ValueError("two-request checkpoint changed unexpectedly")
    if payload.get("request_state") not in {"prepared", "issued"} or payload.get("requests_used") not in {0, 1, 2}:
        raise ValueError("two-request checkpoint accounting changed unexpectedly")
    return payload


def _mark_two_request_issued(report_path: Path, prepared: dict, count: int) -> None:
    if count not in {1, 2}:
        raise ValueError("two-request issued-request count exceeded two")
    current = _load_two_request_state(report_path, prepared["policy"])
    if current.get("requests_used") != count - 1:
        raise ValueError("two-request checkpoint request accounting changed unexpectedly")
    payload = {**current, "request_state": "issued", "requests_used": count, "requests_remaining": 2 - count}
    write_corpus_report(report_path, payload)


def _terminal_two_request(base: dict, *, run_status: str, result: dict | None = None, interruption: dict | None = None) -> dict:
    payload = {**base, "run_status": run_status}
    if result is not None:
        payload["result"] = result
    if interruption is not None:
        payload["interruption"] = interruption
    return payload


def _observed_development(args: argparse.Namespace) -> int:
    """Run an explicit multi-case M48 observation-only development path."""
    manifest = load_case_manifest(args.manifest)
    selected_cases = manifest.cases
    if args.case_id:
        selected_cases = [case for case in manifest.cases if case.case_id == args.case_id]
        if not selected_cases:
            print(json.dumps({"status": "configuration_error", "error": "--case-id is not present in the manifest"}))
            return 2
    if args.max_cases < 1 or args.max_cases > len(selected_cases):
        print(json.dumps({"status": "configuration_error", "error": "--max-cases must select manifest rows"}))
        return 2
    maximum_requests = args.max_cases * (1 + args.max_rounds)
    if args.provider == "deepseek":
        if not args.authorize_hosted:
            print(json.dumps({"status": "authorization_required", "error": "--authorize-hosted is required"}))
            return 2
        if args.request_budget is None or args.request_budget < 1 or args.request_budget > maximum_requests:
            print(json.dumps({"status": "configuration_error", "error": "invalid --request-budget for selected bounds"}))
            return 2
        if args.provider_timeout < 1:
            print(json.dumps({"status": "configuration_error", "error": "--provider-timeout must be at least 1"}))
            return 2
        try:
            provider = DeepSeekProvider.from_env_file(Path(args.env_file))
        except DeepSeekConfigurationError as exc:
            print(json.dumps({"status": "configuration_error", "error": str(exc)}))
            return 2
        harness = ManualHarness(store=RecordStore(args.data_root), executor=WslBubblewrapExecutor())
        allow_hosted = True
    else:
        if not args.fake_replacement_script:
            print(json.dumps({"status": "configuration_error", "error": "--fake-replacement-script is required for --provider fake"}))
            return 2
        content = Path(args.fake_replacement_script).read_text(encoding="utf-8")
        provider = FakeLLMProvider([fake_replacement_response(content)] * maximum_requests)
        harness = ManualHarness(store=RecordStore(args.data_root), executor=_executor_for(args))
        allow_hosted = False

    cases = []
    remaining = args.request_budget if args.provider == "deepseek" else maximum_requests
    report_path = Path(args.report) if args.report else _default_corpus_report_path(Path(args.data_root))

    def checkpoint(*, run_status: str, interruption: dict | None = None) -> dict:
        payload = {
            "schema_version": 1,
            "policy": "q01-observation-development-v1",
            "run_status": run_status,
            "cases": cases,
            "requests_used": maximum_requests - remaining,
            "requests_remaining": remaining,
        }
        if interruption is not None:
            payload["interruption"] = interruption
        write_corpus_report(report_path, payload)
        return payload

    checkpoint(run_status="running")
    for case in selected_cases[: args.max_cases]:
        if remaining == 0:
            cases.append({"case_id": case.case_id, "status": "not_run", "stop_reason": "request_budget_exhausted"})
        else:
            try:
                result = ObservedBuildLoopRunner(harness=harness, provider=provider, allow_hosted=allow_hosted).run(
                    f"{args.record_prefix}-{case.case_id}",
                    input_path=case.input_step,
                    observation_session_id=f"{args.observation_session}-{case.case_id}",
                    observation_calls=[ObservationCall(call_id="summary-1", tool="probe_summary")],
                    timeout=args.timeout,
                    provider_timeout=args.provider_timeout,
                    max_repair_rounds=min(args.max_rounds, max(remaining - 1, 0)),
                )
            except (ProviderRequestTimeoutError, ProviderRequestLifecycleError) as exc:
                # The request was issued before this worker lifecycle failure, so it consumes one budget unit.
                remaining -= 1
                payload = checkpoint(
                    run_status="interrupted",
                    interruption=_provider_interruption(case.case_id, exc),
                )
                print(json.dumps(payload, indent=2, ensure_ascii=False))
                return 1
            remaining -= result.provider_requests
            payload = {"case_id": case.case_id, "tier": case.tier, "status": result.status, "provider_requests": result.provider_requests}
            payload["telemetry"] = result.telemetry
            if result.harness_result is not None:
                payload["first_pass"] = result_to_dict(result.harness_result)
            if result.repair is not None:
                payload["repair"] = repair_result_to_dict(result.repair)
            cases.append(payload)
        checkpoint(run_status="running")
    payload = checkpoint(run_status="completed")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if all(case["status"] == "pass" for case in cases) else 1


def _provider_control(args: argparse.Namespace) -> int:
    """Issue one fixed, separately authorized provider control request."""

    report_path = Path(args.report)
    if args.provider == "deepseek":
        if not args.authorize_hosted:
            print(json.dumps({"status": "authorization_required", "error": "--authorize-hosted is required"}))
            return 2
        if args.request_budget != 1:
            print(json.dumps({"status": "configuration_error", "error": "--request-budget must equal 1"}))
            return 2
        if args.provider_timeout < 1:
            print(json.dumps({"status": "configuration_error", "error": "--provider-timeout must be at least 1"}))
            return 2
        try:
            provider = DeepSeekProvider.from_env_file(Path(args.env_file))
        except DeepSeekConfigurationError as exc:
            print(json.dumps({"status": "configuration_error", "error": str(exc)}))
            return 2
        model = provider.model
    else:
        provider = FakeLLMProvider()
        model = "fake-control"

    policy = "provider-control-v1"
    if args.phase == "prepare":
        return _prepare_single_request(report_path, policy=policy, provider=provider.name, model=model)
    if args.phase == "execute":
        prepared = _load_prepared_single_request(report_path, policy)
        if prepared is None:
            return _single_request_error("report must be an existing prepared single-request checkpoint")
        _mark_single_request_issued(report_path, prepared)

    control_request = ProviderRequest(
        messages=[LLMMessage(role="user", content="Return exactly OK.")],
        model=model,
        metadata={"policy": "provider-control-v1"},
    )
    try:
        _complete_provider(provider, control_request, timeout_seconds=args.provider_timeout)
    except (ProviderRequestTimeoutError, ProviderRequestLifecycleError) as exc:
        payload = {
            "schema_version": 1,
            "policy": "provider-control-v1",
            "run_status": "interrupted",
            "requests_used": 1,
            "requests_remaining": 0,
            "interruption": _provider_interruption("provider-control", exc),
        }
        if args.phase == "execute":
            payload = _terminal_single_request(_load_prepared_or_issued(report_path, policy), run_status="interrupted", interruption=payload["interruption"])
        write_corpus_report(report_path, payload)
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 1

    payload = {
        "schema_version": 1,
        "policy": "provider-control-v1",
        "run_status": "completed",
        "provider": provider.name,
        "model": model,
        "requests_used": 1,
        "requests_remaining": 0,
    }
    if args.phase == "execute":
        payload = _terminal_single_request(_load_prepared_or_issued(report_path, policy), run_status="completed", result=payload)
    write_corpus_report(report_path, payload)
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def _single_request_error(message: str) -> int:
    print(json.dumps({"status": "configuration_error", "error": message}))
    return 2


def _prepare_single_request(report_path: Path, *, policy: str, provider: str, model: str) -> int:
    if report_path.exists():
        return _single_request_error("report path must be fresh for a prepared single-request checkpoint")
    payload = {
        "schema_version": 1,
        "policy": policy,
        "run_status": "running",
        "request_state": "prepared",
        "provider": provider,
        "model": model,
        "requests_used": 0,
        "requests_remaining": 1,
    }
    write_corpus_report(report_path, payload)
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def _load_prepared_single_request(report_path: Path, policy: str) -> dict | None:
    try:
        payload = json.loads(report_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return None
    if not isinstance(payload, dict):
        return None
    if (
        payload.get("schema_version") != 1
        or payload.get("policy") != policy
        or payload.get("run_status") != "running"
        or payload.get("request_state") != "prepared"
        or payload.get("requests_used") != 0
        or payload.get("requests_remaining") != 1
    ):
        return None
    return payload


def _load_prepared_or_issued(report_path: Path, policy: str) -> dict:
    payload = _load_prepared_single_request(report_path, policy)
    if payload is not None:
        return payload
    raw = json.loads(report_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or raw.get("policy") != policy or raw.get("request_state") != "issued":
        raise ValueError("single-request checkpoint changed unexpectedly")
    return raw


def _mark_single_request_issued(report_path: Path, prepared: dict) -> None:
    payload = {**prepared, "request_state": "issued", "requests_used": 1, "requests_remaining": 0}
    write_corpus_report(report_path, payload)


def _terminal_single_request(base: dict, *, run_status: str, result: dict | None = None, interruption: dict | None = None) -> dict:
    payload = {**base, "run_status": run_status, "request_state": "issued", "requests_used": 1, "requests_remaining": 0}
    if result is not None:
        payload["result"] = result
    if interruption is not None:
        payload["interruption"] = interruption
    return payload


def _monitor(args: argparse.Namespace) -> int:
    """Operate only monitor-owned state for an existing report."""
    try:
        if args.monitor_command == "setup":
            payload = setup_monitor(args.report, args.state, stale_after_seconds=args.stale_after)
        elif args.monitor_command == "observe":
            payload = observe_monitor(args.state)
        else:
            payload = teardown_monitor(args.state)
    except MonitorError as exc:
        print(json.dumps({"status": "monitor_error", "error": {"code": exc.code, "message": str(exc)}}))
        return 2
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def _m135_epoch_preflight(args: argparse.Namespace) -> int:
    """Prepare the local-only, fixed M135 epoch and its monitor state."""
    report_path = Path(args.report)
    monitor_path = Path(args.monitor_state)
    root = Path(__file__).resolve().parents[2]
    try:
        payload = prepare_preflight_checkpoint(report_path, monitor_path, root=root)
        monitor = setup_monitor(report_path, monitor_path, stale_after_seconds=args.stale_after)
    except (MonitorError, OSError, ValueError) as exc:
        print(json.dumps({"status": "configuration_error", "error": str(exc)}, ensure_ascii=False))
        return 2
    print(
        json.dumps(
            {
                "status": "prepared_offline",
                "policy": M135_POLICY,
                "report_path": str(report_path),
                "monitor_state_path": str(monitor_path),
                "requests_used": payload["requests_used"],
                "requests_remaining": payload["requests_remaining"],
                "monitor_status": monitor["monitor_status"],
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


def _m135_epoch_execute(args: argparse.Namespace) -> int:
    """Execute only an itemized-authorized, freshly prepared M135 epoch."""
    if not args.authorize_hosted:
        print(json.dumps({"status": "authorization_required", "error": "--authorize-hosted is required"}))
        return 2
    if args.request_budget != 18 or args.provider_timeout != 120 or args.max_repair_rounds != 0 or args.max_retry_count != 0:
        print(json.dumps({"status": "configuration_error", "error": "M135 requires 18 requests, 120s deadline, and zero repair/retry"}))
        return 2
    report_path = Path(args.report)
    monitor_path = Path(args.monitor_state)
    root = Path(__file__).resolve().parents[2]
    try:
        provider = DeepSeekProvider.from_env_file(Path(args.env_file))
        if provider.model != "deepseek-v4-pro":
            raise ValueError("M135 requires deepseek-v4-pro")
        authorize_execution_checkpoint(report_path, monitor_path=monitor_path)
        result = run_serial_epoch(
            report_path,
            root=root,
            provider=provider,
            harness=ManualHarness(store=RecordStore(args.data_root), executor=WslBubblewrapExecutor()),
            provider_timeout=args.provider_timeout,
        )
    except (DeepSeekConfigurationError, OSError, ValueError) as exc:
        print(json.dumps({"status": "configuration_error", "error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps({"status": result["run_status"], "requests_used": result["requests_used"], "requests_remaining": result["requests_remaining"]}, ensure_ascii=False))
    return 0


def _campaign_prepare(args: argparse.Namespace) -> int:
    """Prepare one M139 frozen campaign locally without provider state."""
    root = Path(__file__).resolve().parents[2]
    try:
        payload = prepare_campaign(
            Path(args.spec),
            Path(args.report),
            Path(args.monitor_state),
            root=root,
            stale_after_seconds=args.stale_after,
        )
    except (CampaignError, OSError) as exc:
        print(json.dumps({"status": "configuration_error", "error": str(exc)}, ensure_ascii=False))
        return 2
    print(
        json.dumps(
            {
                "status": "prepared_offline",
                "campaign_id": payload["campaign_id"],
                "report_path": str(args.report),
                "monitor_state_path": str(args.monitor_state),
                "requests_used": payload["requests_used"],
                "requests_remaining": payload["requests_remaining"],
            },
            ensure_ascii=False,
        )
    )
    return 0


def _m176_asymmetric_campaign_preflight(args: argparse.Namespace) -> int:
    """Prepare both fixed M176 products locally; never constructs a provider."""
    root = Path(__file__).resolve().parents[2]
    try:
        payload = prepare_asymmetric_campaign(root, stale_after_seconds=args.stale_after)
    except (AsymmetricCampaignError, OSError) as exc:
        print(json.dumps({"status": "configuration_error", "error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps({"status": payload["status"], "completion_slots_cap": payload["completion_cap"], "provider_request_cap": payload["provider_request_cap"], "main_cases": len(payload["main_case_ids"]), "annex_cases": len(payload["annex"])}, ensure_ascii=False))
    return 0


def _m176_asymmetric_campaign_admission(args: argparse.Namespace) -> int:
    """Validate both fixed checkpoints; authorization remains a future G3 action."""
    root = Path(__file__).resolve().parents[2]
    try:
        payload = validate_asymmetric_execute_admission(root)
    except (AsymmetricCampaignError, OSError) as exc:
        print(json.dumps({"status": "configuration_error", "error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps({"status": "fresh_execute_admission_candidate", "completion_slots_cap": payload["completion_cap"], "provider_request_cap": payload["provider_request_cap"]}, ensure_ascii=False))
    return 0


def _m179_asymmetric_campaign_preflight(args: argparse.Namespace) -> int:
    """Prepare M179's fresh local identities; never constructs a provider."""
    root = Path(__file__).resolve().parents[2]
    try:
        payload = prepare_m179(root, stale_after_seconds=args.stale_after)
    except (AsymmetricCampaignError, OSError) as exc:
        print(json.dumps({"status": "configuration_error", "error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps({"status": payload["status"], "policy": payload["policy"], "completion_slots_cap": payload["completion_cap"], "provider_request_cap": payload["provider_request_cap"]}, ensure_ascii=False))
    return 0


def _m179_asymmetric_campaign_admission(args: argparse.Namespace) -> int:
    """Verify M179's local-only candidate checkpoints."""
    root = Path(__file__).resolve().parents[2]
    try:
        payload = validate_m179_execute_admission(root)
    except (AsymmetricCampaignError, OSError) as exc:
        print(json.dumps({"status": "configuration_error", "error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps({"status": "fresh_execute_admission_candidate", "policy": payload["policy"], "completion_slots_cap": payload["completion_cap"], "provider_request_cap": payload["provider_request_cap"]}, ensure_ascii=False))
    return 0


def _m180_asymmetric_campaign_execute(args: argparse.Namespace) -> int:
    if not args.authorize_hosted:
        print(json.dumps({"status": "authorization_required", "error": "--authorize-hosted is required"}))
        return 2
    root = Path(__file__).resolve().parents[2]
    try:
        # This revalidates the fresh dual checkpoint before reading local
        # configuration or constructing the provider.
        authorize_m179_execution(root)
        provider = DeepSeekProvider.from_env_file(Path(args.env_file))
        if provider.model != "deepseek-v4-pro" or provider.timeout_seconds != 120:
            raise AsymmetricCampaignError("M180 requires the frozen DeepSeek V4 Pro / 120-second boundary")
        payload = run_authorized_m179(root, provider)
    except (AsymmetricCampaignError, DeepSeekConfigurationError, OSError) as exc:
        print(json.dumps({"status": "configuration_error", "error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload["status"] == "completed" else 1


def _m182_asymmetric_campaign_preflight(args: argparse.Namespace) -> int:
    root = Path(__file__).resolve().parents[2]
    try:
        payload = prepare_m182(root, stale_after_seconds=args.stale_after)
    except (AsymmetricCampaignError, OSError) as exc:
        print(json.dumps({"status": "configuration_error", "error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps({"status": payload["status"], "policy": payload["policy"], "completion_slots_cap": payload["completion_cap"], "provider_request_cap": payload["provider_request_cap"]}, ensure_ascii=False))
    return 0


def _m182_asymmetric_campaign_admission(args: argparse.Namespace) -> int:
    root = Path(__file__).resolve().parents[2]
    try:
        payload = validate_m182_execute_admission(root)
    except (AsymmetricCampaignError, OSError) as exc:
        print(json.dumps({"status": "configuration_error", "error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps({"status": "fresh_execute_admission_candidate", "policy": payload["policy"], "completion_slots_cap": payload["completion_cap"], "provider_request_cap": payload["provider_request_cap"]}, ensure_ascii=False))
    return 0


def _m182_asymmetric_campaign_execute(args: argparse.Namespace) -> int:
    if not args.authorize_hosted:
        print(json.dumps({"status": "authorization_required", "error": "--authorize-hosted is required"}))
        return 2
    root = Path(__file__).resolve().parents[2]
    try:
        authorize_m182_execution(root)
        provider = DeepSeekProvider.from_env_file(Path(args.env_file))
        if provider.model != "deepseek-v4-pro" or provider.timeout_seconds != 120:
            raise AsymmetricCampaignError("M182 requires the frozen DeepSeek V4 Pro / 120-second boundary")
        payload = run_authorized_m182(root, provider)
    except (AsymmetricCampaignError, DeepSeekConfigurationError, OSError) as exc:
        print(json.dumps({"status": "configuration_error", "error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload["status"] == "completed" else 1



_LIFECYCLE_PHASES = frozenset(
    {
        "worker_phase_unobserved",
        "worker_started",
        "http_started",
        "http_first_response_byte",
        "http_response_completed",
        "http_failed",
        "worker_failed",
    }
)


def _provider_interruption(case_id: str, exc: ProviderRequestTimeoutError | ProviderRequestLifecycleError) -> dict:
    """Build the bounded checkpoint schema for an issued provider-worker failure."""

    interruption = {
        "code": "provider_request_timeout" if isinstance(exc, ProviderRequestTimeoutError) else "provider_request_failed",
        "case_id": case_id,
        "exception_type": type(exc).__name__,
    }
    diagnostics = _sanitize_lifecycle_diagnostics(getattr(exc, "diagnostics", None))
    if diagnostics is not None:
        interruption["diagnostics"] = diagnostics
    telemetry = _sanitize_observed_telemetry(getattr(exc, "telemetry", None))
    if telemetry is not None:
        interruption["telemetry"] = telemetry
    return interruption


def _sanitize_lifecycle_diagnostics(value: object) -> dict | None:
    """Accept only M58's compact, non-sensitive lifecycle diagnostic schema."""

    if not isinstance(value, dict) or set(value) != {"last_phase", "events", "error_class"}:
        return None
    last_phase = value["last_phase"]
    error_class = value["error_class"]
    events = value["events"]
    if last_phase not in _LIFECYCLE_PHASES or not isinstance(error_class, str) or not error_class.isidentifier():
        return None
    if not isinstance(events, list):
        return None
    sanitized_events: list[dict] = []
    elapsed_ms = -1
    for event in events:
        if not isinstance(event, dict) or set(event) != {"phase", "elapsed_ms"}:
            return None
        phase = event["phase"]
        current_elapsed_ms = event["elapsed_ms"]
        if (
            phase not in _LIFECYCLE_PHASES
            or not isinstance(current_elapsed_ms, int)
            or isinstance(current_elapsed_ms, bool)
            or current_elapsed_ms < elapsed_ms
        ):
            return None
        sanitized_events.append({"phase": phase, "elapsed_ms": current_elapsed_ms})
        elapsed_ms = current_elapsed_ms
    expected_last_phase = sanitized_events[-1]["phase"] if sanitized_events else "worker_phase_unobserved"
    if last_phase != expected_last_phase:
        return None
    return {"last_phase": last_phase, "events": sanitized_events, "error_class": error_class}


def _sanitize_observed_telemetry(value: object) -> dict | None:
    """Whitelist M65's count/timing-only telemetry for terminal checkpoints."""

    if not isinstance(value, dict) or set(value) != {"schema_version", "request_timing", "context_ledger", "phase_elapsed_ms"}:
        return None
    if value["schema_version"] != 1:
        return None
    request_timing = value["request_timing"]
    ledger = value["context_ledger"]
    phases = value["phase_elapsed_ms"]
    expected_timing = {"send_offset_ms", "first_byte_offset_ms", "done_offset_ms", "token_usage"}
    expected_phases = {"input_prepare", "observation", "provider_wait", "harness", "end_to_end"}
    if not isinstance(request_timing, dict) or set(request_timing) != expected_timing:
        return None
    if request_timing["first_byte_offset_ms"] is not None or request_timing["done_offset_ms"] is not None or request_timing["token_usage"] is not None:
        return None
    if not _nonnegative_int(request_timing["send_offset_ms"]):
        return None
    if not isinstance(ledger, dict) or set(ledger) != {"message_count", "sections"} or not _nonnegative_int(ledger["message_count"]):
        return None
    sections = ledger["sections"]
    if not isinstance(sections, dict) or set(sections) != {"system_instruction", "observation_transcript"}:
        return None
    sanitized_sections = {}
    for name, counts in sections.items():
        if not isinstance(counts, dict) or set(counts) != {"chars", "utf8_bytes"}:
            return None
        if not _nonnegative_int(counts["chars"]) or not _nonnegative_int(counts["utf8_bytes"]):
            return None
        sanitized_sections[name] = {"chars": counts["chars"], "utf8_bytes": counts["utf8_bytes"]}
    if not isinstance(phases, dict) or set(phases) != expected_phases:
        return None
    if not all(value is None or _nonnegative_int(value) for value in phases.values()):
        return None
    return {
        "schema_version": 1,
        "request_timing": {
            "send_offset_ms": request_timing["send_offset_ms"],
            "first_byte_offset_ms": None,
            "done_offset_ms": None,
            "token_usage": None,
        },
        "context_ledger": {"message_count": ledger["message_count"], "sections": sanitized_sections},
        "phase_elapsed_ms": dict(phases),
    }


def _nonnegative_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _hosted_corpus_preflight(args: argparse.Namespace, manifest) -> dict | None:
    if args.repair:
        return {
            "status": "configuration_error",
            "error": "--repair is local fake-provider replay and cannot be combined with --provider deepseek",
        }
    if not args.authorize_hosted:
        return {
            "status": "authorization_required",
            "error": "--authorize-hosted is required before a hosted corpus evaluation can issue requests",
        }
    if args.max_cases is None or args.max_cases < 1:
        return {"status": "configuration_error", "error": "--max-cases must be a positive bound for hosted evaluation"}
    if args.max_rounds < 1:
        return {"status": "configuration_error", "error": "--max-rounds must be at least 1 for hosted evaluation"}
    if args.request_budget is None or args.request_budget < 1:
        return {"status": "configuration_error", "error": "--request-budget must be a positive bound for hosted evaluation"}
    if args.max_cases > len(manifest.cases):
        return {
            "status": "configuration_error",
            "error": f"--max-cases exceeds manifest size ({len(manifest.cases)})",
        }
    maximum_requests = args.max_cases * (1 + args.max_rounds) if args.first_pass else args.max_cases * args.max_rounds
    if args.request_budget > maximum_requests:
        return {
            "status": "configuration_error",
            "error": "--request-budget exceeds the selected case and generation/repair round bounds",
        }
    if args.provider_timeout < 1:
        return {"status": "configuration_error", "error": "--provider-timeout must be at least 1"}
    if shutil.which("wsl.exe") is None and shutil.which("wsl") is None:
        return {"status": "sandbox_unavailable", "error": "wsl-bwrap requires a local wsl executable"}
    return None


def _select_case(manifest: CaseManifest, case_id: str) -> CaseManifest:
    selected = tuple(case for case in manifest.cases if case.case_id == case_id)
    if not selected:
        raise ValueError(f"--case-id is not present in the manifest: {case_id}")
    return CaseManifest(path=manifest.path, schema_version=manifest.schema_version, cases=selected)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="brep2code")
    subparsers = parser.add_subparsers(dest="command")

    run = subparsers.add_parser("run", help="Create/open a record and execute one build revision.")
    run.add_argument("--record", required=True, help="Record id, for example 'demo'.")
    run.add_argument("--script", help="Optional build_sequence.py to copy into the revision workspace.")
    run.add_argument("--input", help="Optional STEP input to copy into the record input directory.")
    run.add_argument("--data-root", default="data", help="Local data root. Defaults to ./data.")
    run.add_argument("--timeout", type=int, default=60, help="Script timeout in seconds.")
    run.add_argument(
        "--build-without-input",
        action="store_true",
        help="Do not mount the record STEP for build execution; retain it only for Harness probes.",
    )
    run.add_argument(
        "--executor",
        choices=("unsafe-local", "wsl-bwrap"),
        default="unsafe-local",
        help="Execution backend. unsafe-local is not a security sandbox.",
    )
    run.add_argument(
        "--runtime-resources",
        help="Optional directory explicitly mounted read-only at /resources by wsl-bwrap.",
    )

    probe = subparsers.add_parser("probe", help="Inspect a B-Rep input with M1 probe tools.")
    probe.add_argument("--record", help="Record id whose input directory contains one CAD input.")
    probe.add_argument("--input", help="Explicit CAD input path. Overrides --record input discovery.")
    probe.add_argument("--data-root", default="data", help="Local data root. Defaults to ./data.")
    probe.add_argument(
        "--tool",
        choices=("summary", "topology", "entity", "sample"),
        default="summary",
        help="Probe tool to run.",
    )
    probe.add_argument("--selector", default="all", help="Topology selector: all, solid, shell, face, edge.")
    probe.add_argument("--entity-id", default="face:000001", help="Entity id for entity/sample probes.")
    probe.add_argument("--samples", type=int, default=4, help="Sample count for sample probe.")
    probe.add_argument("--max-entities", type=int, default=80, help="Maximum topology entities to return.")
    probe.add_argument("--limit-bytes", type=int, default=12_000, help="Maximum JSON result size.")

    repair = subparsers.add_parser("repair", help="Run a bounded fake or DeepSeek provider repair loop.")
    repair.add_argument("--record", required=True, help="Record id, for example 'demo'.")
    repair.add_argument("--script", required=True, help="Initial failing build_sequence.py path.")
    repair.add_argument("--input", help="Optional STEP input to copy into the record input directory.")
    repair.add_argument("--data-root", default="data", help="Local data root. Defaults to ./data.")
    repair.add_argument("--timeout", type=int, default=60, help="Script timeout in seconds.")
    repair.add_argument("--max-rounds", type=int, default=1, help="Maximum provider repair rounds.")
    repair.add_argument("--provider-timeout", type=int, default=120, help="Hosted provider request timeout in seconds.")
    repair.add_argument("--provider", choices=("fake", "deepseek"), default="fake")
    repair.add_argument("--env-file", default=".env", help="Ignored local provider configuration file.")
    repair.add_argument(
        "--fake-replacement-script",
        help="Required only for --provider fake: local replacement build_sequence.py.",
    )

    corpus = subparsers.add_parser("corpus", help="Run a manifest-driven local or explicitly authorized hosted corpus review.")
    corpus.add_argument("--manifest", required=True, help="Case manifest JSON path.")
    corpus.add_argument("--data-root", default="data", help="Local data root. Defaults to ./data.")
    corpus.add_argument("--report", help="Optional corpus report output path.")
    corpus.add_argument("--record-prefix", default="corpus", help="Record id prefix for per-case runs.")
    corpus.add_argument("--case-id", help="Run exactly one case id from the manifest.")
    corpus.add_argument("--timeout", type=int, default=60, help="Script timeout in seconds.")
    corpus.add_argument(
        "--executor",
        choices=("unsafe-local", "wsl-bwrap"),
        default="unsafe-local",
        help="Execution backend for explicit local corpus runs. unsafe-local is not a security sandbox.",
    )
    corpus.add_argument(
        "--runtime-resources",
        help="Optional directory explicitly mounted read-only at /resources by wsl-bwrap.",
    )
    corpus.add_argument(
        "--repair",
        action="store_true",
        help="Replay failing cases with a local fake-provider reference script when available.",
    )
    corpus.add_argument(
        "--first-pass",
        action="store_true",
        help="Generate an initial build_sequence.py from bounded B-Rep summary context before Harness execution.",
    )
    corpus.add_argument("--provider", choices=("fake", "deepseek"), default="fake")
    corpus.add_argument("--env-file", default=".env", help="Ignored local provider configuration file.")
    corpus.add_argument(
        "--authorize-hosted",
        action="store_true",
        help="Required with --provider deepseek; confirms this command may issue bounded hosted requests.",
    )
    corpus.add_argument("--max-cases", type=int, help="Required positive case bound for hosted evaluation.")
    corpus.add_argument("--max-rounds", type=int, default=1, help="Maximum provider repair rounds per hosted case.")
    corpus.add_argument("--request-budget", type=int, help="Required positive hosted provider request bound.")
    corpus.add_argument(
        "--provider-timeout",
        type=int,
        default=120,
        help="Maximum seconds for each hosted provider request before it is terminated.",
    )

    observed = subparsers.add_parser("observed-first-pass", help="Run one M48 observation-to-build first pass.")
    observed.add_argument("--record", required=True)
    observed.add_argument("--input", required=True)
    observed.add_argument("--data-root", default="data")
    observed.add_argument("--report", help="Required durable report path for an authorized hosted run.")
    observed.add_argument("--timeout", type=int, default=60)
    observed.add_argument("--provider-timeout", type=int, default=120)
    observed.add_argument("--request-budget", type=int, help="Must be 1 for the hosted single-case path.")
    observed.add_argument("--observation-session", default="observed-first-pass-v1")
    observed.add_argument("--provider", choices=("fake", "deepseek"), default="fake")
    observed.add_argument("--fake-replacement-script")
    observed.add_argument("--env-file", default=".env")
    observed.add_argument("--authorize-hosted", action="store_true")
    observed.add_argument("--phase", choices=("prepare", "execute"), help="Prepare a monitorable checkpoint or execute it.")

    reference = subparsers.add_parser("reference-assisted-smoke", help="Run the fixed M85 two-request reference-assisted P0 smoke.")
    reference.add_argument("--record", required=True)
    reference.add_argument("--input", required=True)
    reference.add_argument("--case-id", default="cylinder")
    reference.add_argument("--data-root", default="data")
    reference.add_argument("--report")
    reference.add_argument("--timeout", type=int, default=60)
    reference.add_argument("--provider-timeout", type=int, default=120)
    reference.add_argument("--request-budget", type=int, required=True)
    reference.add_argument("--max-repair-rounds", type=int, default=0)
    reference.add_argument("--observation-session", default="m85-reference-assisted-v1")
    reference.add_argument("--guidance-index", default="runtime_resources/experience-cards/index.json")
    reference.add_argument("--guidance-card", default="runtime_resources/experience-cards/cards/vertical-cylinder-construction.json")
    reference.add_argument("--guidance-role", default="final primitive")
    reference.add_argument("--provider", choices=("fake", "deepseek"), default="fake")
    reference.add_argument("--fake-replacement-script")
    reference.add_argument("--env-file", default=".env")
    reference.add_argument("--authorize-hosted", action="store_true")
    reference.add_argument("--phase", choices=("prepare", "execute"), help="Prepare a two-request durable checkpoint or execute it.")

    reference_block = subparsers.add_parser(
        "reference-assisted-block-with-hole-smoke", help="Run the fixed M87 two-request reference-assisted P0 block-with-hole smoke."
    )
    reference_block.add_argument("--record", required=True)
    reference_block.add_argument("--input", required=True)
    reference_block.add_argument("--case-id", default="block_with_hole")
    reference_block.add_argument("--data-root", default="data")
    reference_block.add_argument("--report")
    reference_block.add_argument("--timeout", type=int, default=60)
    reference_block.add_argument("--provider-timeout", type=int, default=120)
    reference_block.add_argument("--request-budget", type=int, required=True)
    reference_block.add_argument("--max-repair-rounds", type=int, default=0)
    reference_block.add_argument("--observation-session", default="m87-reference-assisted-block-with-hole-v1")
    reference_block.add_argument("--guidance-index", default="runtime_resources/experience-cards/index.json")
    reference_block.add_argument("--guidance-card", default="runtime_resources/experience-cards/cards/vertical-cylinder-construction.json")
    reference_block.add_argument("--guidance-role", default="single boolean-cut tool")
    reference_block.add_argument("--provider", choices=("fake", "deepseek"), default="fake")
    reference_block.add_argument("--fake-replacement-script")
    reference_block.add_argument("--env-file", default=".env")
    reference_block.add_argument("--authorize-hosted", action="store_true")
    reference_block.add_argument("--phase", choices=("prepare", "execute"), help="Prepare a two-request durable checkpoint or execute it.")

    reference_three_hole = subparsers.add_parser(
        "reference-assisted-three-hole-plate-smoke",
        help="Run the fixed M89 two-request reference-assisted P1 three-hole-plate smoke.",
    )
    reference_three_hole.add_argument("--record", required=True)
    reference_three_hole.add_argument("--input", required=True)
    reference_three_hole.add_argument("--case-id", default="three_hole_plate")
    reference_three_hole.add_argument("--data-root", default="data")
    reference_three_hole.add_argument("--report")
    reference_three_hole.add_argument("--timeout", type=int, default=60)
    reference_three_hole.add_argument("--provider-timeout", type=int, default=120)
    reference_three_hole.add_argument("--request-budget", type=int, required=True)
    reference_three_hole.add_argument("--max-repair-rounds", type=int, default=0)
    reference_three_hole.add_argument("--observation-session", default="m89-reference-assisted-three-hole-plate-v1")
    reference_three_hole.add_argument("--guidance-index", default="runtime_resources/experience-cards/index.json")
    reference_three_hole.add_argument("--guidance-card", default="runtime_resources/experience-cards/cards/vertical-cylinder-construction.json")
    reference_three_hole.add_argument("--guidance-role", default="repeated boolean-cut tool")
    reference_three_hole.add_argument("--provider", choices=("fake", "deepseek"), default="fake")
    reference_three_hole.add_argument("--fake-replacement-script")
    reference_three_hole.add_argument("--env-file", default=".env")
    reference_three_hole.add_argument("--authorize-hosted", action="store_true")
    reference_three_hole.add_argument("--phase", choices=("prepare", "execute"), help="Prepare a two-request durable checkpoint or execute it.")

    reference_three_hole_bounded = subparsers.add_parser(
        "reference-assisted-three-hole-plate-bounded-output-smoke",
        help="Run M89-003's fixed two-request P1 three-hole-plate bounded-output smoke.",
    )
    reference_three_hole_bounded.add_argument("--record", required=True)
    reference_three_hole_bounded.add_argument("--input", required=True)
    reference_three_hole_bounded.add_argument("--case-id", default="three_hole_plate")
    reference_three_hole_bounded.add_argument("--data-root", default="data")
    reference_three_hole_bounded.add_argument("--report")
    reference_three_hole_bounded.add_argument("--timeout", type=int, default=60)
    reference_three_hole_bounded.add_argument("--provider-timeout", type=int, default=120)
    reference_three_hole_bounded.add_argument("--request-budget", type=int, required=True)
    reference_three_hole_bounded.add_argument("--max-repair-rounds", type=int, default=0)
    reference_three_hole_bounded.add_argument("--max-output-tokens", type=int, default=4096)
    reference_three_hole_bounded.add_argument("--observation-session", default="m89-003-three-hole-plate-bounded-output-v1")
    reference_three_hole_bounded.add_argument("--guidance-index", default="runtime_resources/experience-cards/index.json")
    reference_three_hole_bounded.add_argument("--guidance-card", default="runtime_resources/experience-cards/cards/vertical-cylinder-construction.json")
    reference_three_hole_bounded.add_argument("--guidance-role", default="repeated boolean-cut tool")
    reference_three_hole_bounded.add_argument("--provider", choices=("fake", "deepseek"), default="fake")
    reference_three_hole_bounded.add_argument("--fake-replacement-script")
    reference_three_hole_bounded.add_argument("--env-file", default=".env")
    reference_three_hole_bounded.add_argument("--authorize-hosted", action="store_true")
    reference_three_hole_bounded.add_argument("--phase", choices=("prepare", "execute"), help="Prepare a two-request durable checkpoint or execute it.")

    reference_three_hole_stability = subparsers.add_parser(
        "reference-assisted-three-hole-plate-stability-smoke",
        help="Run M118's fresh two-request P1 three-hole-plate stability-only smoke.",
    )
    reference_three_hole_stability.add_argument("--record", required=True)
    reference_three_hole_stability.add_argument("--input", required=True)
    reference_three_hole_stability.add_argument("--case-id", default="three_hole_plate")
    reference_three_hole_stability.add_argument("--data-root", default="data")
    reference_three_hole_stability.add_argument("--report")
    reference_three_hole_stability.add_argument("--timeout", type=int, default=60)
    reference_three_hole_stability.add_argument("--provider-timeout", type=int, default=300)
    reference_three_hole_stability.add_argument("--request-budget", type=int, required=True)
    reference_three_hole_stability.add_argument("--max-repair-rounds", type=int, default=0)
    reference_three_hole_stability.add_argument("--max-output-tokens", type=int, default=4096)
    reference_three_hole_stability.add_argument("--observation-session", default="m118-three-hole-plate-stability-v1")
    reference_three_hole_stability.add_argument("--guidance-index", default="runtime_resources/experience-cards/index.json")
    reference_three_hole_stability.add_argument("--guidance-card", default="runtime_resources/experience-cards/cards/vertical-cylinder-construction.json")
    reference_three_hole_stability.add_argument("--guidance-role", default="repeated boolean-cut tool")
    reference_three_hole_stability.add_argument("--provider", choices=("fake", "deepseek"), default="fake")
    reference_three_hole_stability.add_argument("--fake-replacement-script")
    reference_three_hole_stability.add_argument("--env-file", default=".env")
    reference_three_hole_stability.add_argument("--authorize-hosted", action="store_true")
    reference_three_hole_stability.add_argument("--phase", choices=("prepare", "execute"), help="Prepare a two-request durable checkpoint or execute it.")

    reference_three_hole_stability_reentry = subparsers.add_parser(
        "reference-assisted-three-hole-plate-stability-reentry-smoke",
        help="Run M127's fresh two-request P1 three-hole-plate shared stability re-entry smoke.",
    )
    reference_three_hole_stability_reentry.add_argument("--record", required=True)
    reference_three_hole_stability_reentry.add_argument("--input", required=True)
    reference_three_hole_stability_reentry.add_argument("--case-id", default="three_hole_plate")
    reference_three_hole_stability_reentry.add_argument("--data-root", default="data")
    reference_three_hole_stability_reentry.add_argument("--report")
    reference_three_hole_stability_reentry.add_argument("--timeout", type=int, default=60)
    reference_three_hole_stability_reentry.add_argument("--provider-timeout", type=int, default=300)
    reference_three_hole_stability_reentry.add_argument("--request-budget", type=int, required=True)
    reference_three_hole_stability_reentry.add_argument("--max-repair-rounds", type=int, default=0)
    reference_three_hole_stability_reentry.add_argument("--max-output-tokens", type=int, default=4096)
    reference_three_hole_stability_reentry.add_argument("--observation-session", default="m127-three-hole-plate-stability-reentry-v1")
    reference_three_hole_stability_reentry.add_argument("--guidance-index", default="runtime_resources/experience-cards/index.json")
    reference_three_hole_stability_reentry.add_argument("--guidance-card", default="runtime_resources/experience-cards/cards/vertical-cylinder-construction.json")
    reference_three_hole_stability_reentry.add_argument("--guidance-role", default="repeated boolean-cut tool")
    reference_three_hole_stability_reentry.add_argument("--provider", choices=("fake", "deepseek"), default="fake")
    reference_three_hole_stability_reentry.add_argument("--fake-replacement-script")
    reference_three_hole_stability_reentry.add_argument("--env-file", default=".env")
    reference_three_hole_stability_reentry.add_argument("--authorize-hosted", action="store_true")
    reference_three_hole_stability_reentry.add_argument("--phase", choices=("prepare", "execute"), help="Prepare a two-request durable checkpoint or execute it.")

    m97 = subparsers.add_parser("reference-guided-through-hole-development-calibration", help="Run M97's fixed three-row card/no-card development calibration.")
    m97.add_argument("--data-root", default="data")
    m97.add_argument("--report")
    m97.add_argument("--timeout", type=int, default=60)
    m97.add_argument("--provider-timeout", type=int, default=120)
    m97.add_argument("--request-budget", type=int, required=True)
    m97.add_argument("--max-repair-rounds", type=int, default=0)
    m97.add_argument("--provider", choices=("fake", "deepseek"), default="fake")
    m97.add_argument("--policy", default="docs/corpus/sequence-paired/reference-guided-through-hole-variation-v1-m97-003-policy.json")
    m97.add_argument("--guidance-index", default="docs/corpus/sequence-paired/fixtures/m96-m97-guidance-index-v1.json")
    m97.add_argument("--guidance-card", default="runtime_resources/experience-cards/cards/vertical-cylinder-construction.json")
    m97.add_argument("--env-file", default=".env")
    m97.add_argument("--authorize-hosted", action="store_true")
    m97.add_argument("--phase", choices=("prepare", "execute"), help="Prepare a nine-request durable checkpoint or execute it.")

    observed_development = subparsers.add_parser(
        "observed-development", help="Run an explicit multi-case M48 observation-only development evaluation."
    )
    observed_development.add_argument("--manifest", required=True)
    observed_development.add_argument("--case-id", help="Run one named manifest case without changing manifest membership.")
    observed_development.add_argument("--data-root", default="data")
    observed_development.add_argument("--report")
    observed_development.add_argument("--record-prefix", default="observed-development")
    observed_development.add_argument("--observation-session", default="observed-development-v1")
    observed_development.add_argument("--timeout", type=int, default=60)
    observed_development.add_argument("--provider-timeout", type=int, default=120)
    observed_development.add_argument("--max-cases", type=int, required=True)
    observed_development.add_argument("--max-rounds", type=int, default=1)
    observed_development.add_argument("--request-budget", type=int)
    observed_development.add_argument("--provider", choices=("fake", "deepseek"), default="fake")
    observed_development.add_argument("--env-file", default=".env")
    observed_development.add_argument("--fake-replacement-script")
    observed_development.add_argument("--executor", choices=("unsafe-local", "wsl-bwrap"), default="unsafe-local")
    observed_development.add_argument("--runtime-resources")
    observed_development.add_argument("--authorize-hosted", action="store_true")

    control = subparsers.add_parser(
        "provider-control", help="Run one fixed provider-response control request for a separately authorized diagnosis."
    )
    control.add_argument("--report", required=True, help="Durable control report path.")
    control.add_argument("--provider", choices=("fake", "deepseek"), default="fake")
    control.add_argument("--env-file", default=".env")
    control.add_argument("--provider-timeout", type=int, default=120)
    control.add_argument("--request-budget", type=int, help="Must be 1 for the hosted control path.")
    control.add_argument("--authorize-hosted", action="store_true")
    control.add_argument("--phase", choices=("prepare", "execute"), help="Prepare a monitorable checkpoint or execute it.")

    m135 = subparsers.add_parser(
        "m135-epoch-preflight",
        help="Prepare the fixed M135 18-condition checkpoint and monitor locally; never constructs a provider.",
    )
    m135.add_argument("--report", required=True, help="Fresh M135 epoch report path.")
    m135.add_argument("--monitor-state", required=True, help="Fresh monitor-owned state path, distinct from --report.")
    m135.add_argument("--stale-after", type=int, default=300, help="Monitor stale threshold in seconds.")

    m135_execute = subparsers.add_parser("m135-epoch-execute", help="Execute the itemized-authorized frozen M135 epoch.")
    m135_execute.add_argument("--report", required=True)
    m135_execute.add_argument("--monitor-state", required=True)
    m135_execute.add_argument("--data-root", default="data")
    m135_execute.add_argument("--env-file", default=".env")
    m135_execute.add_argument("--authorize-hosted", action="store_true")
    m135_execute.add_argument("--request-budget", type=int, required=True)
    m135_execute.add_argument("--provider-timeout", type=int, default=120)
    m135_execute.add_argument("--max-repair-rounds", type=int, default=0)
    m135_execute.add_argument("--max-retry-count", type=int, default=0)

    campaign_prepare = subparsers.add_parser(
        "campaign-prepare", help="Prepare one M139 frozen campaign locally; never constructs a provider."
    )
    campaign_prepare.add_argument("--spec", required=True, help="Versioned frozen campaign JSON spec.")
    campaign_prepare.add_argument("--report", required=True, help="Fresh prepared campaign report path.")
    campaign_prepare.add_argument("--monitor-state", required=True, help="Fresh monitor-owned state path.")
    campaign_prepare.add_argument("--stale-after", type=int, default=300)

    m176_preflight = subparsers.add_parser(
        "m176-asymmetric-campaign-preflight", help="Prepare the fixed M176 dual-product campaign locally; never constructs a provider."
    )
    m176_preflight.add_argument("--stale-after", type=int, default=300)
    subparsers.add_parser(
        "m176-asymmetric-campaign-admission", help="Validate the fixed M176 checkpoints before a separate G3 authorization."
    )
    m179_preflight = subparsers.add_parser(
        "m179-asymmetric-campaign-preflight", help="Prepare M179's fresh fixed identities locally; never constructs a provider."
    )
    m179_preflight.add_argument("--stale-after", type=int, default=300)
    subparsers.add_parser(
        "m179-asymmetric-campaign-admission", help="Validate M179's fixed local checkpoints before a separate G3 authorization."
    )
    m180_execute = subparsers.add_parser("m180-asymmetric-campaign-execute", help="Require explicit authorization before future M179 hosted execution.")
    m180_execute.add_argument("--authorize-hosted", action="store_true")
    m180_execute.add_argument("--env-file", default=".env")

    m182_preflight = subparsers.add_parser("m182-asymmetric-campaign-preflight", help="Prepare M182 fresh continuation identities locally; never constructs a provider.")
    m182_preflight.add_argument("--stale-after", type=int, default=300)
    subparsers.add_parser("m182-asymmetric-campaign-admission", help="Validate M182's fixed local checkpoints before a separate G3 authorization.")
    m182_execute = subparsers.add_parser("m182-asymmetric-campaign-execute", help="Require fresh explicit authorization before M182 hosted execution.")
    m182_execute.add_argument("--authorize-hosted", action="store_true")
    m182_execute.add_argument("--env-file", default=".env")


    monitor = subparsers.add_parser("monitor", help="Observe one existing report without controlling its process.")
    monitor_subparsers = monitor.add_subparsers(dest="monitor_command", required=True)
    monitor_setup = monitor_subparsers.add_parser("setup", help="Create monitor-owned state from a report.")
    monitor_setup.add_argument("--report", required=True, help="Existing corpus report to observe read-only.")
    monitor_setup.add_argument("--state", required=True, help="Monitor-owned state file; must differ from --report.")
    monitor_setup.add_argument("--stale-after", type=int, default=300, help="Seconds before a running report requires operator action.")
    monitor_observe = monitor_subparsers.add_parser("observe", help="Observe the report once and update monitor state.")
    monitor_observe.add_argument("--state", required=True, help="Monitor-owned state file.")
    monitor_teardown = monitor_subparsers.add_parser("teardown", help="Stop local monitoring without touching the report.")
    monitor_teardown.add_argument("--state", required=True, help="Monitor-owned state file.")
    return parser


def _default_corpus_report_path(data_root: Path) -> Path:
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    return data_root / "corpus-runs" / f"{run_id}.json"


def _executor_for(args: argparse.Namespace):
    if args.executor == "wsl-bwrap":
        return WslBubblewrapExecutor(runtime_resources=Path(args.runtime_resources) if args.runtime_resources else None)
    return None


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
