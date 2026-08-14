# WP-M5-001: Runtime Sandbox Foundation

- Status: done
- Milestone: M5
- Owner: unassigned

## Goal

Replace the current cwd-only execution convention with a backend architecture that can enforce the runtime sandbox contract before any hosted provider is enabled.

## Scope

- Add a `SandboxRunner` interface and clearly label the existing subprocess executor `unsafe-local`.
- Define an execution policy with explicit read-only input/resource mounts and writable output/intermediates mounts.
- Audit a Windows-native backend and the installed WSL candidate against the contract; select one only when it demonstrably denies host/repository access and network.
- Implement the selected backend, sanitized environment, resource limits, child-process cleanup, structured sandbox errors, and trace metadata.
- Add adversarial acceptance tests for development-document reads, parent-path writes, ambient secrets, network, and descendants.

## Inputs

- `docs/architecture/v1/contracts/runtime-sandbox.md`
- `docs/architecture/adr/0006-runtime-sandbox-before-hosted-provider.md`
- `brep2code/cad/executor.py`
- `brep2code/agent/harness.py`
- `brep2code/agent/repair.py`

## Backend audit (2026-08-01)

- The host has WSL `Ubuntu-24.04`, Python 3.12.3, and `bwrap`/`unshare` available.
- The default WSL user can see the Windows repository mount and belongs to `sudo`; WSL alone is therefore **not** an approved sandbox boundary.
- No Docker or Podman command was found. A dedicated WSL virtual environment at `/home/liaol/.brep2code-runtime` now provides `cadquery-ocp`; a real box STEP smoke has passed through `WslBubblewrapExecutor`.
- The backend stages scripts into the Linux filesystem, omits Windows mounts from bubblewrap, unshares network, clears environment variables, mounts the script read-only, and allows writes only to `output/` and `intermediates/`. The WSL launcher user remains privileged outside bubblewrap, so the boundary relies on bubblewrap and still needs the remaining adversarial probes.
- Verified manually on this host: OpenCascade box smoke passes; repository, ambient-secret, and network probe values are all true; a one-second timeout returns structured exit code 124 and `timed_out: true` without an unhandled exception.
- A selected STEP is readable only at `/input/model.step`; writes to `build_sequence.py` and the workspace root are denied; a spawned child cannot create its delayed artifact after the parent sandbox exits.

## Compatibility constraints

- Existing deterministic unit and corpus tests may use explicit `unsafe-local` mode only.
- Hosted-provider execution remains unavailable until the secure backend passes acceptance probes.
- Do not grant runtime scripts repository-root, `docs/`, `.cursor/`, `AGENTS.md`, home-directory, secret, or network access.

## Acceptance

- [x] Chosen backend documents and proves every required isolation capability on the supported host.
- [x] Missing secure backend returns structured `sandbox_unavailable`; no provider-generated execution path exists yet.
- [x] `unsafe-local` is explicit in CLI/result traces; no hosted-provider flow exists yet.
- [x] Policy violations are structured and traceable without leaking secrets.
- [x] Adversarial filesystem, environment, network, timeout, input-mount, and descendant-process manual probes pass on the supported host.
- [x] `uv run python -m pytest` passes (33 passed on 2026-08-01).
- [x] `uv run python -m ruff check .` passes (2026-08-01).

## Out of scope

- Hosted-provider SDK integration.
- IR, CAD SDK, CAD workplace, or new modeling primitives.
- Dataset-scale evaluation.

## Result

`WslBubblewrapExecutor` is the selected backend for the supported Windows host. It provides read-only `/input/model.step` and explicit `/resources`, writable output/intermediates only, sanitized environment, network isolation, CPU/memory limits, timeout handling, descendant cleanup, and structured `sandbox_unavailable`, `sandbox_timeout`, and `sandbox_policy_violation` events. M3-004 must route provider-generated scripts through this backend.
