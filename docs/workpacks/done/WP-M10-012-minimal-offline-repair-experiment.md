# WP-M10-012: Minimal Offline Sandbox-Path Repair Experiment

- Status: done
- Milestone: M10
- Owner: unassigned

## Goal

Test whether a minimal, deterministic path/trace compatibility intervention can reproduce and correct the two trace-supported sandbox input-path failures without hiding original Harness evidence or changing production behavior.

## Trigger condition

`WP-M10-011` is completed and confirms the two `direct` M10-008 sandbox input-path cases remain one locally reproducible mechanism in the attribution ledger.

## Scope

- Preregister fixed scripts reproducing the host-path failure for the evidenced family and a non-matching import-failure control.
- Compare the failing host-path form with `/input/model.step` under the existing `wsl-bwrap` executor.
- Preserve original gate statuses, signal bundles, and execution traces; report whether the intervention makes the fixed script executable/readable without calling a provider.
- Publish a sanitized review that limits its claim to deterministic execution compatibility and repair-signal usefulness.

## Compatibility constraints

- No provider request, prompt/context change, hosted policy comparison, held-out run, production helper, probe, gate, schema, manifest, or default-command change.
- The non-matching unavailable-import control must preserve its previous failure behavior.
- A successful fixed-script experiment is not evidence of first-pass model improvement.

## Acceptance

- Both qualifying path cases reproduce the original sandbox failure with trace support before the intervention.
- The `/input/model.step` variant is tested under the same executor and retains complete original gate-level evidence.
- The non-matching import control does not gain a false pass from the path intervention.
- The review either closes the hypothesis or registers a separately preregistered development-only hosted-policy candidate; it never authorizes that candidate or a held-out request.

## Docs to update

Update the attribution ledger, repair-experiment review, status, handoff, workpack index, and ADR/runbook only if the experiment establishes a lasting governance boundary.

## Out of scope

Production helper implementation, generic path abstraction, prompt/context edits, provider calls, held-out evaluation, IR, SDK, or benchmark claims.

## Completion

The two path baselines reproduced their trace-supported failures under `wsl-bwrap`; the `/input/model.step` variants produced readable output for both cases.  The non-matching unavailable-import control retained the same import failure after its path was corrected.  The resulting conclusion is limited to deterministic sandbox compatibility and repair-signal usefulness; see [the review](../../architecture/v1/m10-012-minimal-offline-path-repair-review.md).
