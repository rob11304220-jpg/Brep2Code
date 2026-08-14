# ADR-0006: Runtime Sandbox Before Hosted Provider

- **Status**: Accepted
- **Date**: 2026-08-01
- **Context**: The current `ScriptExecutor` runs arbitrary Python with a revision workspace as its `cwd`. This organizes artifacts but does not prevent parent-path reads, host writes, network access, or ambient credential reads. M4 confirms local replacement scripts can repair the current corpus, so a new modeling abstraction is not the immediate constraint.

## Decision

Treat the current executor as `unsafe-local` only. A real hosted provider may not execute generated scripts until a runtime sandbox satisfies [`runtime-sandbox.md`](../v1/contracts/runtime-sandbox.md). This decision required validation of a viable Windows backend before hosted-provider integration could be considered.

## Rationale

The runtime LLM must not be able to obtain development governance material or host capabilities merely by generating Python. A documented prohibition without OS-level enforcement is insufficient.

## Consequences

- **Positive**: Hosted-provider rollout has an explicit security gate and auditable acceptance probes.
- **Negative**: Hosted integration and unrestricted script execution are deferred until backend validation completes.
- **Mitigation**: Preserve the deterministic fake-provider path as explicitly labelled `unsafe-local` for existing unit and corpus tests.

## Implementation outcome

M5-001 subsequently validated and selected `WslBubblewrapExecutor` on the supported Windows host. The security prerequisite is therefore complete. M3-004 has since selected DeepSeek V4; any provider-generated execution must use the selected backend.
