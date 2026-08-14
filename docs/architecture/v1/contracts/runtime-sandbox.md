---
type: contract
related-project: Brep2Code
version: v1
status: active
tags:
  - Brep2Code
  - v1
  - runtime
  - sandbox
---

# Contract: Runtime Sandbox

This contract governs the **runtime execution plane** only. It does not grant the runtime LLM access to development governance materials such as `AGENTS.md`, workpacks, handoffs, ADRs, or repository `docs/`.

## Required capabilities

| Resource | Runtime access |
|----------|----------------|
| revision `workspace/output/`, `workspace/intermediates/` | read/write |
| selected input model | read-only |
| explicitly packaged runtime resources | read-only |
| revision `traces/` | Harness writes; script has no direct access unless explicitly granted |
| repository root, `docs/`, `.cursor/`, `AGENTS.md`, tests, user home | denied |
| ambient environment variables and credentials | denied by default |
| network | denied |

The script is invoked only as `build_sequence.py` in a per-revision sandbox. A script update may replace that file only; it may not name arbitrary host paths.

## Enforcement requirements

- `cwd` and Python-level path validation are defense-in-depth only; they are not a sandbox.
- A provider-generated script must run in an OS-enforced process/filesystem boundary with a sanitized environment, wall-clock timeout, CPU/memory limits, and child-process cleanup.
- If the configured backend cannot provide the required boundary, provider-generated execution must fail closed with a structured `sandbox_unavailable` or `sandbox_policy_violation` result.
- Local developer execution may retain an explicit `unsafe-local` mode for deterministic fixtures, but it must be visibly named, never selected for hosted-provider execution, and not satisfy this contract.

## Observability

Every execution records sandbox backend, policy version, effective mounts/capabilities, sanitized environment key names, resource limits, termination reason, and policy violations in the revision trace. Secrets and their values are never recorded.

Input and output B-Rep summary probes run in separate processes with bounded deadlines. Input summaries receive 45 seconds because trusted source STEP loading may be expensive; generated output artifacts retain a 15-second deadline. Either timeout is recorded as `probe_timeout`; an unavailable input fails `input_model_step_readable`, while an unavailable output fails the readable-output gate. Neither can block the Harness process.

## Current implementation status

`WslBubblewrapExecutor` is available as the explicit `brep2code run --executor wsl-bwrap` backend on the audited Windows host. It stages the script below WSL `/tmp`, clears the environment, unshares network, omits Windows mounts from bubblewrap, mounts the script read-only, and binds only `output/` and `intermediates/` writable. The Harness records `sandbox_backend` and `sandboxed` in `execution.json` and `signal_bundle.json`.

It has passed a real OpenCascade box smoke; manual probes proving that the script cannot see the repository `AGENTS.md`, a supplied ambient test variable, or the network; a read-only `/input/model.step` mount; write denial outside `output/` and `intermediates/`; a one-second timeout yielding structured exit code 124; and descendant cleanup (no child-created artifact after five seconds). Explicit runtime resources, policy metadata, and structured violation classification were completed in M5-001. M3-004 is complete: the explicit DeepSeek V4 provider path routes provider-generated scripts through this backend, and its credential smoke passed the output/readability and geometry gates.

## Acceptance probes

The backend must reject and record attempts to read `AGENTS.md`, write outside the allowed output/intermediates paths, read an ambient secret, access the network, or leave descendant processes running.
