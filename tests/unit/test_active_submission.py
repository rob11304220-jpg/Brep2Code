import json
from pathlib import Path

import pytest

import brep2code.harness.active as active_module
from brep2code.cases import validate_case
from brep2code.execution import ExecutionResult, SandboxUnavailable
from brep2code.geometry.inspect import GeometryMetrics
from brep2code.harness import (
    ActiveBudgets,
    ActiveHarnessRunner,
    ActiveResultValidationError,
    ActiveState,
    ActiveSubmissionVerifier,
    validate_active_result,
)
from brep2code.providers import (
    FakeActionProvider,
    OpenAICompatibleConfig,
    OpenAICompatibleProvider,
    ProviderLimits,
)


class _HTTPResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return None

    def read(self, unused_amount: int | None = None):
        return json.dumps(self.payload).encode("utf-8")


def _case():
    return validate_case(Path("cases/smoke/box"), Path("cases"))


def _run_root(tmp_path: Path) -> Path:
    root = tmp_path / "run"
    root.mkdir()
    return root


def _execution(workspace: Path, *, output: bool = True) -> ExecutionResult:
    return ExecutionResult(
        exit_code=0 if output else 1,
        stdout="",
        stderr="script failed" if not output else "",
        duration_seconds=0.01,
        output_step=workspace / "output.step" if output else None,
        sandboxed=True,
        sandbox_backend="test-secure",
    )


def _metrics(*, volume_delta: float = 0.0) -> GeometryMetrics:
    return GeometryMetrics(
        bbox_min=(0.0, 0.0, 0.0),
        bbox_max=(10.0, 20.0, 30.0),
        volume=6000.0 + volume_delta,
        counts={"solid": 1, "shell": 1, "face": 6, "edge": 24},
    )


def _budgets(**overrides) -> ActiveBudgets:
    values = {
        "model_requests": 4,
        "probes": 1,
        "retrievals": 1,
        "script_submissions": 2,
        "executions": 2,
        "repairs": 1,
        "tokens": 0,
        "cost_usd": 0.0,
    }
    values.update(overrides)
    return ActiveBudgets(**values)


def test_submission_verifier_rejects_compatibility_before_execution(tmp_path: Path) -> None:
    calls = []

    def executor(workspace: Path, *, timeout_seconds: int):
        calls.append((workspace, timeout_seconds))
        return _execution(workspace)

    verifier = ActiveSubmissionVerifier(
        _case(), _run_root(tmp_path), 5, executor=executor
    )

    result = verifier("from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox")

    assert result.passed is False
    assert result.executed is False
    assert result.feedback["stage"] == "generation"
    assert calls == []
    artifact = json.loads(
        (tmp_path / "run/revision-000/result.json").read_text(encoding="utf-8")
    )
    assert artifact["status"] == "failed"
    assert artifact["feedback"]["reason"] == "unsupported_import"


def test_submission_verifier_returns_typed_execution_feedback(tmp_path: Path) -> None:
    verifier = ActiveSubmissionVerifier(
        _case(),
        _run_root(tmp_path),
        5,
        executor=lambda workspace, **_: _execution(workspace, output=False),
    )

    result = verifier("candidate = True")

    assert result.passed is False
    assert result.executed is True
    assert result.feedback == {
        "stage": "execution",
        "exit_code": 1,
        "timed_out": False,
        "termination_reason": "completed",
        "stderr": "script failed",
    }


def test_submission_verifier_returns_geometry_feedback_then_passes(tmp_path: Path) -> None:
    metrics = iter([_metrics(volume_delta=1.0), _metrics()])
    verifier = ActiveSubmissionVerifier(
        _case(),
        _run_root(tmp_path),
        5,
        executor=lambda workspace, **_: _execution(workspace),
        inspector=lambda _: next(metrics),
        observer=lambda _: {},
    )

    failed = verifier("candidate = True")
    passed = verifier("repair = True")

    assert failed.passed is False
    assert failed.feedback["stage"] == "geometry"
    assert failed.feedback["differences_from_brep"]["volume"] == 1.0
    assert passed.passed is True
    assert json.loads(
        (tmp_path / "run/revision-001/result.json").read_text(encoding="utf-8")
    )["status"] == "succeeded"


def test_active_runner_rejects_unchanged_repair_without_execution_and_can_recover(
    tmp_path: Path,
) -> None:
    case = _case()
    provider = FakeActionProvider(
        [
            {"action": "submit", "submit": {"script": "candidate = True"}},
            {"action": "submit", "submit": {"script": "candidate = True"}},
            {"action": "submit", "submit": {"script": "repair = True"}},
        ]
    )
    executions = []
    metrics = iter([_metrics(volume_delta=1.0), _metrics()])

    def factory(case, run_root, timeout_seconds):
        return ActiveSubmissionVerifier(
            case,
            run_root,
            timeout_seconds,
            executor=lambda workspace, **_: (
                executions.append(workspace.name) or _execution(workspace)
            ),
            inspector=lambda _: next(metrics),
            observer=lambda _: {},
        )

    run_root = tmp_path / "active"
    result = ActiveHarnessRunner(provider, submission_factory=factory).run(
        case,
        run_root,
        budgets=_budgets(
            model_requests=3,
            probes=0,
            retrievals=0,
            script_submissions=3,
            executions=2,
            repairs=2,
        ),
        timeout_seconds=5,
    )

    assert result.state is ActiveState.SUCCEEDED
    assert executions == ["revision-000", "revision-002"]
    assert result.usage["script_submissions"] == 3
    assert result.usage["executions"] == 2
    assert result.usage["repairs"] == 2
    unchanged = json.loads(
        (run_root / "revision-001/result.json").read_text(encoding="utf-8")
    )
    assert unchanged["status"] == "failed"
    assert unchanged["feedback"]["reason"] == "unchanged_revision"
    assert provider.requests[-1].session["feedback"]["reason"] == "unchanged_revision"
    validate_active_result(
        json.loads((run_root / "result.json").read_text(encoding="utf-8")),
        case,
        run_root,
    )


def test_active_runner_retrieves_recommended_reference_after_invalid_ocp_downcast(
    tmp_path: Path,
) -> None:
    case = _case()
    provider = FakeActionProvider(
        [
            {
                "action": "submit",
                "submit": {"script": "edge = TopoDS.Edge(shape)"},
            },
            {"action": "retrieve", "retrieve": {"topic": "TopoDS.Edge_s"}},
            {
                "action": "submit",
                "submit": {"script": "edge = TopoDS.Edge_s(shape)"},
            },
        ]
    )
    executions = []

    def factory(case, run_root, timeout_seconds):
        return ActiveSubmissionVerifier(
            case,
            run_root,
            timeout_seconds,
            executor=lambda workspace, **_: (
                executions.append(workspace.name) or _execution(workspace)
            ),
            inspector=lambda _: _metrics(),
            observer=lambda _: {},
        )

    run_root = tmp_path / "active"
    result = ActiveHarnessRunner(provider, submission_factory=factory).run(
        case,
        run_root,
        budgets=_budgets(model_requests=3),
        timeout_seconds=5,
    )

    assert result.state is ActiveState.SUCCEEDED
    assert result.usage["script_submissions"] == 2
    assert result.usage["retrievals"] == 1
    assert result.usage["executions"] == 1
    assert executions == ["revision-001"]
    feedback = provider.requests[1].session["feedback"]
    assert feedback["reason"] == "invalid_ocp_downcast"
    assert feedback["symbol"] == "TopoDS.Edge"
    assert feedback["reference_topic"] == "TopoDS.Edge_s"
    retrieved = provider.requests[2].session["tool_results"][-1]
    assert retrieved["request"]["topic"] == feedback["reference_topic"]
    assert retrieved["result"]["symbol"] == "TopoDS.Edge_s"
    rejected = json.loads(
        (run_root / "revision-000/result.json").read_text(encoding="utf-8")
    )
    assert rejected["status"] == "failed"
    assert rejected["feedback"] == feedback
    validate_active_result(
        json.loads((run_root / "result.json").read_text(encoding="utf-8")),
        case,
        run_root,
    )


def test_active_runner_retrieves_module_scope_guidance_after_local_ocp_import(
    tmp_path: Path,
) -> None:
    case = _case()
    provider = FakeActionProvider(
        [
            {
                "action": "submit",
                "submit": {
                    "script": "def inspect():\n    from OCP.Geom import Geom_Line\n"
                },
            },
            {
                "action": "retrieve",
                "retrieve": {"topic": "OCP.module_scope_imports"},
            },
            {
                "action": "submit",
                "submit": {
                    "script": "from OCP.Geom import Geom_Line\n\ndef inspect():\n    return Geom_Line\n"
                },
            },
        ]
    )
    executions = []

    def factory(case, run_root, timeout_seconds):
        return ActiveSubmissionVerifier(
            case,
            run_root,
            timeout_seconds,
            executor=lambda workspace, **_: (
                executions.append(workspace.name) or _execution(workspace)
            ),
            inspector=lambda _: _metrics(),
            observer=lambda _: {},
        )

    run_root = tmp_path / "active"
    result = ActiveHarnessRunner(provider, submission_factory=factory).run(
        case,
        run_root,
        budgets=_budgets(model_requests=3),
        timeout_seconds=5,
    )

    assert result.state is ActiveState.SUCCEEDED
    assert result.usage["script_submissions"] == 2
    assert result.usage["retrievals"] == 1
    assert result.usage["executions"] == 1
    assert executions == ["revision-001"]
    feedback = provider.requests[1].session["feedback"]
    assert feedback == {
        "stage": "generation",
        "reason": "function_local_ocp_import",
        "scope": "module",
        "reference_topic": "OCP.module_scope_imports",
        "message": "Place every OCP import at module scope; do not import OCP inside functions.",
    }
    retrieved = provider.requests[2].session["tool_results"][-1]
    assert retrieved["request"]["topic"] == feedback["reference_topic"]
    assert retrieved["result"]["symbol"] == "OCP.module_scope_imports"
    rejected = json.loads(
        (run_root / "revision-000/result.json").read_text(encoding="utf-8")
    )
    assert rejected["status"] == "failed"
    assert rejected["feedback"] == feedback


def test_active_runner_retrieves_reference_after_legacy_topods_downcast(
    tmp_path: Path,
) -> None:
    case = _case()
    provider = FakeActionProvider(
        [
            {
                "action": "submit",
                "submit": {
                    "script": (
                        "from OCP.TopoDS import topods\n"
                        "edge = topods.Edge(shape)\n"
                    )
                },
            },
            {"action": "retrieve", "retrieve": {"topic": "TopoDS.Edge_s"}},
            {
                "action": "submit",
                "submit": {
                    "script": (
                        "from OCP.TopoDS import TopoDS\n"
                        "edge = TopoDS.Edge_s(shape)\n"
                    )
                },
            },
        ]
    )
    executions = []

    def factory(case, run_root, timeout_seconds):
        return ActiveSubmissionVerifier(
            case,
            run_root,
            timeout_seconds,
            executor=lambda workspace, **_: (
                executions.append(workspace.name) or _execution(workspace)
            ),
            inspector=lambda _: _metrics(),
            observer=lambda _: {},
        )

    run_root = tmp_path / "active"
    result = ActiveHarnessRunner(provider, submission_factory=factory).run(
        case,
        run_root,
        budgets=_budgets(model_requests=3),
        timeout_seconds=5,
    )

    assert result.state is ActiveState.SUCCEEDED
    assert result.usage["script_submissions"] == 2
    assert result.usage["retrievals"] == 1
    assert result.usage["executions"] == 1
    assert executions == ["revision-001"]
    feedback = provider.requests[1].session["feedback"]
    assert feedback["reason"] == "invalid_ocp_downcast"
    assert feedback["symbol"] == "topods.Edge"
    assert feedback["replacement"] == "TopoDS.Edge_s"
    assert feedback["reference_topic"] == "TopoDS.Edge_s"
    retrieved = provider.requests[2].session["tool_results"][-1]
    assert retrieved["request"]["topic"] == feedback["reference_topic"]
    assert retrieved["result"]["symbol"] == "TopoDS.Edge_s"
    rejected = json.loads(
        (run_root / "revision-000/result.json").read_text(encoding="utf-8")
    )
    assert rejected["status"] == "failed"
    assert rejected["feedback"] == feedback


def test_active_runner_retrieves_reference_after_topexp_instance_call(
    tmp_path: Path,
) -> None:
    case = _case()
    provider = FakeActionProvider(
        [
            {
                "action": "submit",
                "submit": {
                    "script": (
                        "exp = TopExp()\n"
                        "exp.MapShapes(shape, TopAbs_EDGE, edge_map)\n"
                    )
                },
            },
            {
                "action": "retrieve",
                "retrieve": {"topic": "TopExp.MapShapes_s"},
            },
            {
                "action": "submit",
                "submit": {
                    "script": "TopExp.MapShapes_s(shape, TopAbs_EDGE, edge_map)\n"
                },
            },
        ]
    )
    executions = []

    def factory(case, run_root, timeout_seconds):
        return ActiveSubmissionVerifier(
            case,
            run_root,
            timeout_seconds,
            executor=lambda workspace, **_: (
                executions.append(workspace.name) or _execution(workspace)
            ),
            inspector=lambda _: _metrics(),
            observer=lambda _: {},
        )

    run_root = tmp_path / "active"
    result = ActiveHarnessRunner(provider, submission_factory=factory).run(
        case,
        run_root,
        budgets=_budgets(model_requests=3),
        timeout_seconds=5,
    )

    assert result.state is ActiveState.SUCCEEDED
    assert result.usage["script_submissions"] == 2
    assert result.usage["retrievals"] == 1
    assert result.usage["executions"] == 1
    assert executions == ["revision-001"]
    feedback = provider.requests[1].session["feedback"]
    assert feedback == {
        "stage": "generation",
        "reason": "ocp_static_method_suffix",
        "method": "exp.MapShapes",
        "replacement": "TopExp.MapShapes_s",
        "reference_topic": "TopExp.MapShapes_s",
        "message": "Use the OCP Python static-method binding with its _s suffix.",
    }
    retrieved = provider.requests[2].session["tool_results"][-1]
    assert retrieved["request"]["topic"] == feedback["reference_topic"]
    assert retrieved["result"]["symbol"] == "TopExp.MapShapes_s"
    rejected = json.loads(
        (run_root / "revision-000/result.json").read_text(encoding="utf-8")
    )
    assert rejected["status"] == "failed"
    assert rejected["feedback"] == feedback


def test_active_runner_retrieves_curve_reference_after_invalid_pnt_call(
    tmp_path: Path,
) -> None:
    case = _case()
    provider = FakeActionProvider(
        [
            {
                "action": "submit",
                "submit": {
                    "script": "point = BRep_Tool.Pnt_s(edge, parameter)\n"
                },
            },
            {
                "action": "retrieve",
                "retrieve": {"topic": "BRepAdaptor_Curve"},
            },
            {
                "action": "submit",
                "submit": {
                    "script": (
                        "curve = BRepAdaptor_Curve(edge)\n"
                        "point = curve.Value(parameter)\n"
                    )
                },
            },
        ]
    )
    executions = []

    def factory(case, run_root, timeout_seconds):
        return ActiveSubmissionVerifier(
            case,
            run_root,
            timeout_seconds,
            executor=lambda workspace, **_: (
                executions.append(workspace.name) or _execution(workspace)
            ),
            inspector=lambda _: _metrics(),
            observer=lambda _: {},
        )

    run_root = tmp_path / "active"
    result = ActiveHarnessRunner(provider, submission_factory=factory).run(
        case,
        run_root,
        budgets=_budgets(model_requests=3),
        timeout_seconds=5,
    )

    assert result.state is ActiveState.SUCCEEDED
    assert result.usage["script_submissions"] == 2
    assert result.usage["retrievals"] == 1
    assert result.usage["executions"] == 1
    assert executions == ["revision-001"]
    feedback = provider.requests[1].session["feedback"]
    assert feedback["reason"] == "invalid_ocp_call_signature"
    assert feedback["symbol"] == "BRep_Tool.Pnt_s"
    assert feedback["expected_arguments"] == 1
    assert feedback["actual_arguments"] == 2
    assert feedback["reference_topic"] == "BRepAdaptor_Curve"
    retrieved = provider.requests[2].session["tool_results"][-1]
    assert retrieved["request"]["topic"] == feedback["reference_topic"]
    assert retrieved["result"]["symbol"] == "BRepAdaptor_Curve"
    rejected = json.loads(
        (run_root / "revision-000/result.json").read_text(encoding="utf-8")
    )
    assert rejected["status"] == "failed"
    assert rejected["feedback"] == feedback


def test_active_runner_returns_bounded_compatibility_issues_in_one_repair(
    tmp_path: Path,
) -> None:
    case = _case()
    provider = FakeActionProvider(
        [
            {
                "action": "submit",
                "submit": {
                    "script": (
                        "edge = TopoDS.Edge(shape)\n"
                        "TopExp.MapShapes(shape, TopAbs_EDGE, edge_map)\n"
                        "point = BRep_Tool.Pnt_s(edge, parameter)\n"
                    )
                },
            },
            {"action": "retrieve", "retrieve": {"topic": "TopoDS.Edge_s"}},
            {
                "action": "retrieve",
                "retrieve": {"topic": "TopExp.MapShapes_s"},
            },
            {
                "action": "retrieve",
                "retrieve": {"topic": "BRepAdaptor_Curve"},
            },
            {
                "action": "submit",
                "submit": {
                    "script": (
                        "edge = TopoDS.Edge_s(shape)\n"
                        "TopExp.MapShapes_s(shape, TopAbs_EDGE, edge_map)\n"
                        "curve = BRepAdaptor_Curve(edge)\n"
                        "point = curve.Value(parameter)\n"
                    )
                },
            },
        ]
    )
    executions = []

    def factory(case, run_root, timeout_seconds):
        return ActiveSubmissionVerifier(
            case,
            run_root,
            timeout_seconds,
            executor=lambda workspace, **_: (
                executions.append(workspace.name) or _execution(workspace)
            ),
            inspector=lambda _: _metrics(),
            observer=lambda _: {},
        )

    run_root = tmp_path / "active"
    result = ActiveHarnessRunner(provider, submission_factory=factory).run(
        case,
        run_root,
        budgets=_budgets(model_requests=5, retrievals=3),
        timeout_seconds=5,
    )

    assert result.state is ActiveState.SUCCEEDED
    assert result.usage["script_submissions"] == 2
    assert result.usage["retrievals"] == 3
    assert result.usage["repairs"] == 1
    assert result.usage["executions"] == 1
    assert executions == ["revision-001"]
    feedback = provider.requests[1].session["feedback"]
    assert feedback["reason"] == "compatibility_errors"
    assert feedback["issues_truncated"] is False
    assert [issue["reference_topic"] for issue in feedback["issues"]] == [
        "TopoDS.Edge_s",
        "TopExp.MapShapes_s",
        "BRepAdaptor_Curve",
    ]
    retrieved_topics = [
        request.session["tool_results"][-1]["result"]["symbol"]
        for request in provider.requests[2:4]
    ]
    assert retrieved_topics == ["TopoDS.Edge_s", "TopExp.MapShapes_s"]
    assert provider.requests[4].session["tool_results"][-1]["result"]["symbol"] == (
        "BRepAdaptor_Curve"
    )
    rejected = json.loads(
        (run_root / "revision-000/result.json").read_text(encoding="utf-8")
    )
    assert rejected["status"] == "failed"
    assert rejected["feedback"] == feedback
    validate_active_result(
        json.loads((run_root / "result.json").read_text(encoding="utf-8")),
        case,
        run_root,
    )


def test_active_runner_connects_actions_to_secure_verifier_artifacts(tmp_path: Path) -> None:
    case = _case()
    provider = FakeActionProvider(
        [
            {"action": "probe", "probe": {"tool": "edge_candidates", "arguments": {}}},
            {"action": "retrieve", "retrieve": {"topic": "TopoDS.Edge_s"}},
            {"action": "submit", "submit": {"script": "candidate = True"}},
            {"action": "submit", "submit": {"script": "repair = True"}},
        ]
    )
    metrics = iter([_metrics(volume_delta=1.0), _metrics()])

    def factory(case, run_root, timeout_seconds):
        return ActiveSubmissionVerifier(
            case,
            run_root,
            timeout_seconds,
            executor=lambda workspace, **_: _execution(workspace),
            inspector=lambda _: next(metrics),
            observer=lambda _: {},
        )

    result = ActiveHarnessRunner(provider, submission_factory=factory).run(
        case, tmp_path / "active", budgets=_budgets(), timeout_seconds=5
    )

    assert result.state is ActiveState.SUCCEEDED
    assert result.usage["executions"] == 2
    assert (tmp_path / "active/revision-000/build.py").read_text() == "candidate = True"
    assert (tmp_path / "active/revision-001/build.py").read_text() == "repair = True"
    artifact = json.loads((tmp_path / "active/result.json").read_text(encoding="utf-8"))
    assert artifact["mode"] == "active"
    assert artifact["state"] == "succeeded"
    assert artifact["stop_reason"] == "passed"
    assert artifact["budgets"]["model_requests"] == 4
    assert artifact["timeout_seconds"] == 5
    validate_active_result(artifact, case, tmp_path / "active")


def test_active_runner_fails_closed_when_secure_backend_is_unavailable(tmp_path: Path) -> None:
    case = _case()
    provider = FakeActionProvider(
        [{"action": "submit", "submit": {"script": "candidate = True"}}]
    )

    def unavailable(*args, **kwargs):
        raise SandboxUnavailable("secure backend unavailable")

    def factory(case, run_root, timeout_seconds):
        return ActiveSubmissionVerifier(
            case,
            run_root,
            timeout_seconds,
            executor=unavailable,
        )

    result = ActiveHarnessRunner(provider, submission_factory=factory).run(
        case, tmp_path / "active", budgets=_budgets(), timeout_seconds=5
    )

    assert result.state is ActiveState.FAILED
    assert result.stop_reason == "sandbox_unavailable"
    assert result.usage["executions"] == 1
    artifact = json.loads(
        (tmp_path / "active/revision-000/result.json").read_text(encoding="utf-8")
    )
    assert artifact["error"]["stage"] == "sandbox"


def test_active_runner_checkpoints_provider_interruption(tmp_path: Path) -> None:
    case = _case()

    class InterruptedProvider:
        name = "fake"
        model = "interrupted"

        def choose_action(self, request):
            raise KeyboardInterrupt

    run_root = tmp_path / "active"
    with pytest.raises(KeyboardInterrupt):
        ActiveHarnessRunner(InterruptedProvider()).run(
            case, run_root, budgets=_budgets(), timeout_seconds=5
        )

    artifact = json.loads((run_root / "result.json").read_text(encoding="utf-8"))
    assert artifact["state"] == "synthesizing"
    assert artifact["terminal"] is False
    assert artifact["stop_reason"] is None
    assert artifact["usage"]["model_requests"] == 1
    assert artifact["continuation_policy"]["eligible"] is True
    validate_active_result(artifact, case, run_root)


def test_active_runner_checkpoints_hosted_malformed_usage_separately(
    tmp_path: Path,
) -> None:
    response = {
        "model": "deepseek-v4-pro",
        "choices": [{"message": {"content": "malformed private response"}}],
        "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
    }
    provider = OpenAICompatibleProvider(
        OpenAICompatibleConfig(
            provider="deepseek",
            base_url="https://provider.invalid/v1",
            api_key="secret",
            model="deepseek-v4-pro",
            thinking_mode="disabled",
        ),
        ProviderLimits(
            max_requests=2,
            timeout_seconds=3,
            max_retries=0,
            max_output_tokens=50,
            max_total_tokens=100,
            max_cost_usd=1.0,
            input_cost_per_million=1.0,
            output_cost_per_million=2.0,
        ),
        opener=lambda *args, **kwargs: _HTTPResponse(response),
    )
    run_root = tmp_path / "hosted-active"

    result = ActiveHarnessRunner(provider).run(
        _case(),
        run_root,
        budgets=_budgets(model_requests=1, tokens=100, cost_usd=1.0),
        timeout_seconds=5,
    )

    assert result.state is ActiveState.FAILED
    artifact = json.loads((run_root / "result.json").read_text(encoding="utf-8"))
    assert artifact["schema_version"] == 7
    assert artifact["usage"]["tokens"] == 15
    assert artifact["provider_accounting"]["http_attempts"] == 1
    assert artifact["provider_accounting"]["tokens"] == {
        "prompt": 10,
        "completion": 5,
        "total": 15,
    }
    assert artifact["provider_accounting"]["in_flight_requests"] == 0
    assert "private response" not in json.dumps(artifact)
    validate_active_result(artifact, _case(), run_root)
    artifact["provider_accounting"]["http_attempts"] = 0
    with pytest.raises(ActiveResultValidationError, match="request accounting drift"):
        validate_active_result(artifact, _case(), run_root)


def test_active_runner_persists_actual_usage_from_over_budget_response(
    tmp_path: Path,
) -> None:
    response = {
        "model": "deepseek-v4-pro",
        "choices": [
            {
                "message": {
                    "content": json.dumps(
                        {
                            "action": "submit",
                            "submit": {"script": "candidate = True"},
                        }
                    )
                }
            }
        ],
        "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
    }
    provider = OpenAICompatibleProvider(
        OpenAICompatibleConfig(
            provider="deepseek",
            base_url="https://provider.invalid/v1",
            api_key="secret",
            model="deepseek-v4-pro",
            thinking_mode="disabled",
        ),
        ProviderLimits(
            max_requests=1,
            timeout_seconds=3,
            max_retries=0,
            max_output_tokens=50,
            max_total_tokens=10,
            max_cost_usd=1.0,
            input_cost_per_million=1.0,
            output_cost_per_million=2.0,
        ),
        opener=lambda *args, **kwargs: _HTTPResponse(response),
    )
    run_root = tmp_path / "hosted-active"

    result = ActiveHarnessRunner(provider).run(
        _case(),
        run_root,
        budgets=_budgets(model_requests=1, tokens=10, cost_usd=1.0),
        timeout_seconds=5,
    )

    assert result.state is ActiveState.FAILED
    assert result.stop_reason == "provider_error"
    artifact = json.loads((run_root / "result.json").read_text(encoding="utf-8"))
    assert artifact["usage"]["tokens"] == 15
    assert artifact["usage"]["cost_usd"] == pytest.approx(0.00002)
    assert artifact["provider_accounting"]["tokens"] == {
        "prompt": 10,
        "completion": 5,
        "total": 15,
    }
    assert artifact["provider_accounting"]["cost_usd"] == pytest.approx(0.00002)
    assert artifact["provider_accounting"]["in_flight_requests"] == 0
    assert artifact["trace"][-1] == {
        "action": "provider",
        "error": "provider token budget exceeded",
    }
    validate_active_result(artifact, _case(), run_root)


def test_active_runner_checkpoints_execution_interruption(tmp_path: Path) -> None:
    case = _case()
    provider = FakeActionProvider(
        [{"action": "submit", "submit": {"script": "candidate = True"}}]
    )

    def interrupted(*args, **kwargs):
        raise KeyboardInterrupt

    def factory(case, run_root, timeout_seconds):
        return ActiveSubmissionVerifier(
            case,
            run_root,
            timeout_seconds,
            executor=interrupted,
        )

    run_root = tmp_path / "active"
    with pytest.raises(KeyboardInterrupt):
        ActiveHarnessRunner(provider, submission_factory=factory).run(
            case, run_root, budgets=_budgets(), timeout_seconds=5
        )

    artifact = json.loads((run_root / "result.json").read_text(encoding="utf-8"))
    assert artifact["state"] == "executing"
    assert artifact["terminal"] is False
    assert artifact["usage"]["script_submissions"] == 1
    assert artifact["usage"]["executions"] == 0
    assert json.loads(
        (run_root / "revision-000/result.json").read_text(encoding="utf-8")
    )["status"] == "execution"
    validate_active_result(artifact, case, run_root)


def test_active_runner_checkpoints_probe_interruption(
    tmp_path: Path, monkeypatch
) -> None:
    case = _case()
    provider = FakeActionProvider(
        [{"action": "probe", "probe": {"tool": "edge_candidates", "arguments": {}}}]
    )
    original_dispatch = active_module.dispatch_tool

    def interrupted(name, case, arguments=None):
        if name == "edge_candidates":
            raise KeyboardInterrupt
        return original_dispatch(name, case, arguments)

    monkeypatch.setattr(active_module, "dispatch_tool", interrupted)
    run_root = tmp_path / "active"
    with pytest.raises(KeyboardInterrupt):
        ActiveHarnessRunner(provider).run(
            case, run_root, budgets=_budgets(), timeout_seconds=5
        )

    artifact = json.loads((run_root / "result.json").read_text(encoding="utf-8"))
    assert artifact["state"] == "probing"
    assert artifact["terminal"] is False
    assert artifact["usage"]["probes"] == 1
    assert artifact["trace"] == []
    validate_active_result(artifact, case, run_root)


def test_active_runner_continues_provider_interruption(tmp_path: Path) -> None:
    case = _case()

    class InterruptedProvider:
        name = "fake"
        model = "fake-action-queue-v1"

        def choose_action(self, request):
            raise KeyboardInterrupt

    run_root = tmp_path / "active"
    with pytest.raises(KeyboardInterrupt):
        ActiveHarnessRunner(InterruptedProvider()).run(
            case, run_root, budgets=_budgets(), timeout_seconds=5
        )

    def factory(case, run_root, timeout_seconds):
        return ActiveSubmissionVerifier(
            case,
            run_root,
            timeout_seconds,
            executor=lambda workspace, **_: _execution(workspace),
            inspector=lambda _: _metrics(),
            observer=lambda _: {},
        )

    provider = FakeActionProvider(
        [{"action": "submit", "submit": {"script": "continued = True"}}]
    )
    result = ActiveHarnessRunner(provider, submission_factory=factory).continue_run(
        case, run_root, budgets=_budgets(), timeout_seconds=5
    )

    assert result.state is ActiveState.SUCCEEDED
    assert result.usage["model_requests"] == 2
    assert (run_root / "revision-000/build.py").read_text() == "continued = True"
    artifact = json.loads((run_root / "result.json").read_text(encoding="utf-8"))
    assert artifact["terminal"] is True
    assert artifact["checkpoint_index"] > 1
    validate_active_result(artifact, case, run_root)


def test_active_runner_continues_after_unknown_execution_outcome(tmp_path: Path) -> None:
    case = _case()
    initial_provider = FakeActionProvider(
        [{"action": "submit", "submit": {"script": "candidate = True"}}]
    )

    def interrupted(*args, **kwargs):
        raise KeyboardInterrupt

    def interrupted_factory(case, run_root, timeout_seconds):
        return ActiveSubmissionVerifier(
            case, run_root, timeout_seconds, executor=interrupted
        )

    run_root = tmp_path / "active"
    with pytest.raises(KeyboardInterrupt):
        ActiveHarnessRunner(
            initial_provider, submission_factory=interrupted_factory
        ).run(case, run_root, budgets=_budgets(), timeout_seconds=5)

    def passing_factory(case, run_root, timeout_seconds):
        return ActiveSubmissionVerifier(
            case,
            run_root,
            timeout_seconds,
            executor=lambda workspace, **_: _execution(workspace),
            inspector=lambda _: _metrics(),
            observer=lambda _: {},
        )

    provider = FakeActionProvider(
        [{"action": "submit", "submit": {"script": "repair = True"}}]
    )
    result = ActiveHarnessRunner(provider, submission_factory=passing_factory).continue_run(
        case, run_root, budgets=_budgets(), timeout_seconds=5
    )

    assert result.state is ActiveState.SUCCEEDED
    assert result.usage["executions"] == 2
    assert (run_root / "revision-001/build.py").read_text() == "repair = True"
    assert provider.requests[0].session["current_revision"] == "candidate = True"
    assert provider.requests[0].session["feedback"]["stage"] == "interruption"
    validate_active_result(
        json.loads((run_root / "result.json").read_text(encoding="utf-8")),
        case,
        run_root,
    )


def test_active_continuation_rejects_budget_drift(tmp_path: Path) -> None:
    case = _case()

    class InterruptedProvider:
        name = "fake"
        model = "fake-action-queue-v1"

        def choose_action(self, request):
            raise KeyboardInterrupt

    run_root = tmp_path / "active"
    with pytest.raises(KeyboardInterrupt):
        ActiveHarnessRunner(InterruptedProvider()).run(
            case, run_root, budgets=_budgets(), timeout_seconds=5
        )
    drifted = _budgets(probes=2)

    with pytest.raises(ActiveResultValidationError, match="budget drift"):
        ActiveHarnessRunner(FakeActionProvider([])).continue_run(
            case, run_root, budgets=drifted, timeout_seconds=5
        )
