# M135-009 Frozen Serial Execute Lifecycle

- **Date**: 2026-08-12
- **Workpack**: `WP-M135-009-frozen-serial-execute-lifecycle`
- **Scope**: offline-only; `FakeLLMProvider` only; no credentials or egress

## Lifecycle contract

`run_fake_serial_epoch()` accepts only `FakeLLMProvider`. For every condition
in M135's frozen order it first writes the durable `issued` checkpoint, passes
the M135-008 frozen request to the fake provider exactly once, and records one
terminal state before proceeding. A returned replacement script is executed
through `ManualHarness` with `build_without_input=True`; the supplied Harness
uses `WslBubblewrapExecutor`. Repair and retry are absent.

The runner uses these condition terminals: no replacement script is
`lifecycle_ended_before_script`; a card script failing M115 static API is
`static_api_inadmissible`; nonzero sandbox exit is
`sandbox_execution_failed`; a completed failing Harness result is
`downstream_gate_failed`; and a Harness pass is `full_success`. It stops only
on existing epoch-integrity closure, never substitutes a condition or reuses
budget.

## Offline evidence

The all-condition regression queues the 18 frozen reference scripts and
reaches `completed`, 18 used / 0 remaining, all `full_success`, with exactly
18 fake requests. The failure regression confirms that downstream-gate,
sandbox-execution and lifecycle-before-script terminals all retain serial
accounting and allow remaining frozen conditions to receive their one request.

This evidence is local Harness compatibility only. It does not authorize a
non-fake provider, a hosted request, or hosted preflight.
