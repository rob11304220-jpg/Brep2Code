# Handoff: M80 minimal P0 end-to-end revalidation

- **Date**: 2026-08-10
- **Subproject**: `brep2code`
- **Status**: `blocked`
- **Related workpack**: `WP-M80-001-minimal-p0-end-to-end-revalidation`

## Goal

Complete a new G3 preflight, then only with fresh itemized authorization run a
single provider control followed by the P0 `box` observation-to-STEP path.

## Done

- M79 is closed after Liaol's independent approval of its evidence/unknown
  matrix and `reproduction-profile-v1`.
- Liaol selected M80. Its local preflight completed without a provider request.
- The local box no-input `wsl-bwrap` control and non-secret configuration
  checks pass; all proposed report/monitor paths are fresh.

## In progress

- M80 is blocked: M70 requires an existing `run_status` report, but both M80
  hosted commands first write their report only after the provider call ends.
  A monitor cannot observe the in-flight call, so the workpack's required
  durable-monitor condition is unmet. No provider is being constructed or
  contacted.

## Next

- Select a new narrow G2 report-lifecycle workpack: it must make the control
  and observed-first-pass paths write an atomic pre-request `running`
  checkpoint that M70 can observe, with offline tests only.
- After that work is independently reviewed, reactivate M80, use new report
  paths, rerun preflight, and only then present a complete G3 authorization.

## Decisions

- Run the independent control first. Run `box` only if its control report is
  successful, parseable and terminal.
- `box` must use `observed-first-pass`, `wsl-bwrap`, one request, zero repair,
  and a fresh report/monitor pair. See
  [`M79 diagnosis`](../../workflow/m79-historical-contract-drift-diagnosis.md).

## Blockers

- M80 preflight fails because the current report lifecycle does not permit
  M70 monitoring while either authorized request is in flight. This requires a
  separately selected G2 fix before any authorization can be requested.

## Key paths

| Kind | Path |
|---|---|
| Branch | `main` |
| Workpack | `docs/workpacks/active/WP-M80-001-minimal-p0-end-to-end-revalidation.md` |
| Profile | `docs/workflow/m79-historical-contract-drift-diagnosis.md` |
| Preflight | `docs/workflow/m80-hosted-minimal-p0-preflight.md` (to be created) |

## Resume prompt

```
Continue Brep2Code M80 minimal P0 end-to-end revalidation.
Read docs/handoff/active/2026-08-10-m80-minimal-p0-end-to-end-revalidation.md,
docs/workflow/status.md, the active M80 workpack and the M79 diagnosis.
First action: select and complete a narrow G2 report-lifecycle fix that adds
monitorable pre-request checkpoints. Do not contact a provider or reactivate
M80 until that fix is independently reviewed.
```
