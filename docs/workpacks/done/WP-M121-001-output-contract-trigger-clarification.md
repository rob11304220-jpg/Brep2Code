# WP-M121-001: Output-Contract Trigger Clarification

- Status: done
- Milestone: M121
- Owner: Codex
- Reviewer: not required (G1)
- Risk tier: G1

## Goal

Record whether M118's terminal hosted-stability result activates the deferred
output-contract route, and align the current routing documents and registry
with that bounded conclusion.

## Scope

- Review only retained local route/workpack/terminal evidence around M80,
  M117, and M118.
- State whether `WP-TRG-005` is now admissible.
- Update only the hosted-stability roadmap, experiment registry, status page,
  and one compact clarification record.

## Compatibility constraints

Offline and documentation-only. No provider construction, preflight,
authorization, request, retry, policy mutation, manifest change, runtime
change, or trigger activation.

## Acceptance

```powershell
python tools\check_governance.py
git diff --check
```

## Status transition

Update `status.md` first, then record the clarification artifact, workpack, and
handoff. Close after governance audit and diff checks pass.

## Owner acceptance

- Added
  [`m121-output-contract-trigger-clarification.md`](../../architecture/v1/m121-output-contract-trigger-clarification.md)
  to state explicitly that M118's `missing_script_update` terminal result does
  not satisfy `WP-TRG-005`'s activation condition.
- Updated the hosted-stability row in
  [`four-track-program-roadmap.md`](../../architecture/v1/four-track-program-roadmap.md)
  and added M118 to
  [`hosted-experiment-registry.md`](../../workflow/hosted-experiment-registry.md)
  so current routing and terminal evidence agree.
- Updated `status.md` so the repository now says plainly that `TRG-005`
  remains unmet and cannot be selected directly from M118.

## Closure rationale

The next hosted-stability move is no longer ambiguous: `TRG-005` is still
deferred, and any future hosted re-entry needs a newly selected bounded
package rather than a direct route continuation.

## Out of scope

Designing that future re-entry package, changing the output contract, adding
repair logic, or making any hosted request.
