"""Offline composition of the M140 tool turn and M141 repair policy."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from brep2code.agent.guidance import GuidanceBundle
from brep2code.agent.harness import ManualHarness
from brep2code.agent.provider import FakeLLMProvider, LLMProvider
from brep2code.agent.repair_policy import ClassifiedRepairResult, ClassifiedRepairRunner
from brep2code.agent.tool_turn import ToolTurnLimits, ToolTurnLoopRunner, ToolTurnResult
from brep2code.storage.store import write_json


@dataclass(frozen=True)
class ClosedLoopReleaseResult:
    """Sanitized accounting for one offline frozen closed-loop fixture."""

    status: str
    stop_reason: str
    provider_completions: int
    initial: ToolTurnResult
    repair: ClassifiedRepairResult | None


class ClosedLoopReleaseRunner:
    """Compose existing offline-only interfaces without widening either one."""

    def __init__(self, *, harness: ManualHarness, provider: LLMProvider, limits: ToolTurnLimits | None = None) -> None:
        if not isinstance(provider, FakeLLMProvider):
            raise ValueError("ClosedLoopReleaseRunner is offline and requires FakeLLMProvider")
        self.harness = harness
        self.provider = provider
        self.limits = limits

    def run(
        self,
        record_id: str,
        *,
        input_path: Path,
        campaign_identity: dict[str, str],
        observation_session_id: str,
        guidance_bundle: GuidanceBundle,
        selected_guidance_role: str,
        timeout: int = 60,
        max_output_tokens: int | None = None,
    ) -> ClosedLoopReleaseResult:
        """Run one declared probe/card/script sequence and one eligible edit."""

        initial = ToolTurnLoopRunner(
            harness=self.harness,
            provider=self.provider,
            limits=self.limits,
        ).run(
            record_id,
            input_path=input_path,
            campaign_identity=campaign_identity,
            observation_session_id=observation_session_id,
            guidance_bundle=guidance_bundle,
            selected_guidance_role=selected_guidance_role,
            timeout=timeout,
            max_output_tokens=max_output_tokens,
        )
        if initial.harness_result is None:
            return ClosedLoopReleaseResult(initial.status, initial.stop_reason, initial.provider_requests, initial, None)

        repair = ClassifiedRepairRunner(harness=self.harness, provider=self.provider).run(initial.harness_result, timeout=timeout)
        completions = initial.provider_requests + repair.provider_requests
        if completions > 4:
            raise RuntimeError("closed-loop release exceeded four-completion ceiling")
        final_result = repair.result or initial.harness_result
        status = initial.status if repair.decision.classification == "pass" else repair.status
        stop_reason = repair.stop_reason
        payload = {
            "schema_version": 1,
            "policy": "m170-closed-loop-release-v1",
            "initial_provider_completions": initial.provider_requests,
            "repair_provider_completions": repair.provider_requests,
            "provider_completions": completions,
            "classification": repair.decision.classification,
            "route": repair.decision.route,
            "status": status,
            "stop_reason": stop_reason,
        }
        write_json(initial.harness_result.revision.traces / "closed_loop_release.json", payload)
        if final_result.revision.traces != initial.harness_result.revision.traces:
            write_json(final_result.revision.traces / "closed_loop_release.json", payload)
        return ClosedLoopReleaseResult(status, stop_reason, completions, initial, repair)
