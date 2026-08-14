# WP-M136-001: M135 No-Input Sandbox Preflight Remediation

- Status: done
- Milestone: M136
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

## Goal

Diagnose and make the smallest offline-only correction for M135's reproducible
fixed-script no-input `wsl-bwrap` failure, while retaining the frozen M134
cohort, its condition identities, and the no-input security boundary.

## Scope

- Capture the failing condition's structured execution evidence and compare it
  with at least one passing no-card condition under the identical runner.
- Add a fixed-script regression that distinguishes the actual mechanism from a
  non-matching control.
- Correct only the local harness/executor, reference fixture, or test contract
  proven responsible; rerun every M135 no-card fixed-script no-input control.
- Record the repair result and re-entry prerequisites without constructing a
  provider or requesting hosted authorization.

## Attribution question and sampling intent

Does the centered-low revolve failure arise from a local no-input sandbox or
fixed-script compatibility defect, rather than a provider, prompt, card, or
epoch-policy issue? The fixed failed condition and one existing passing
no-card control are the bounded diagnostic sample. Stop once the mechanism is
classified and the complete frozen no-card control has a terminal result.

## Inputs

- `docs/workflow/m135-frozen-epoch-preflight-blocked.md`
- `docs/workflow/m134-frozen-hosted-batch-epoch-policy.md`
- `docs/architecture/adr/0067-frozen-hosted-batch-epochs.md`
- `docs/architecture/adr/0068-frozen-epoch-checkpoint-and-transcript-contract.md`
- fixed case-library assets named by `frozen_conditions()`

## Code paths

- `brep2code/agent/**`, `brep2code/cad/**`, or the single affected frozen
  reference fixture only after the diagnostic proves the responsible path.
- `tests/test_m135_epoch.py` and directly related regression tests.

## Docs to update

- `docs/workflow/status.md`
- this workpack and the active handoff
- `docs/workflow/m135-frozen-epoch-preflight-blocked.md`
- a concise repair record under `docs/workflow/`
- relevant execution contract/module/runbook only if a lasting interface or
  procedure changes

## Trace/schema changes

No provider, corpus-report, checkpoint, or CLI schema change is intended.
Local diagnostic evidence may be added to test assertions or a repair record;
it must contain no credential, provider content, or raw outbound payload.

## Decision-package impact

- `decision_id`: no Q01--Q04 package; bounded Q03 sandbox/preflight repair.
- Q01/Q02 effect: no observable, case, card, prompt, split, or sequence change.
- Q03/Q04 effect: restore or explicitly reject the local no-input executor
  preflight required before M135 can be reconsidered.
- Evidence role: fixed-script regression and non-matching control.
- Knowledge disposition: no reusable knowledge.

## Compatibility constraints

Default operation remains offline and credential-free. Retain M134's 18
condition identities, hashes, ordering, treatments, provider/model policy,
zero-repair/zero-retry policy, and no-input `wsl-bwrap` boundary. Do not
construct a provider, send data, alter any prompt/card/model/provider, issue a
request, modify an executable manifest, or reuse M135 paths/budget/authority.

## Acceptance

```powershell
uv run python -m pytest tests\test_m135_epoch.py -q
uv run python -m pytest -m fast -q
uv run python -m pytest
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

## Owner completion boundary

Publish a trace-supported root-cause/repair record, fixed-script regression and
non-matching control; pass the complete M135 no-card no-input preflight and all
listed acceptance commands; then obtain Liaol's independent G2 review. The
owner must also update the M135 re-entry record. None of this requests or
grants hosted authorization.

## Permitted stop conditions

Independent review; frozen-input drift; an out-of-scope dependency; or a
reproducible local validation blocker. Partial diagnosis, a partial fix, or
partial validation is not a stop condition.

## Evidence reuse / guidance-card disposition

No reusable knowledge and no guidance-card change.

## Status transition

Update `docs/workflow/status.md` first, then this workpack and the active
handoff. M135 remains blocked until this workpack closes and its complete
preflight is rerun freshly. The original M136 terminal review is rescheduled
as M137; it remains user-selected and is gated on a later authorized, terminal
M135 epoch.

## Out of scope

Hosted execution or authorization; prompt/card/model/provider policy changes;
new cases; condition replacement, addition, removal, or reordering; report
reuse; repair-loop behavior; held-out evaluation; or terminal epoch review.

## Repair hypothesis and evaluation boundary

Offline fixed-script diagnosis only. The mechanism must be supported by the
failed centered-low revolve trace and a passing no-card control. Preserve the
original failure result in the M135 preflight record. A passing repair proves
only local fixed-script preflight compatibility; it makes no provider quality,
epoch outcome, or hosted readiness claim.

## Owner completion evidence (2026-08-12)

Root cause and fixed/pass control evidence are recorded in
[`m136-m135-no-input-sandbox-remediation-record.md`](../../workflow/m136-m135-no-input-sandbox-remediation-record.md).
The repair makes the nine affected centered development reference scripts
self-contained and adds a repository-helper import regression assertion. The
full frozen no-card no-input control and all acceptance commands passed:
focused M135 `5 passed in 93.43s`; fast `66 passed`; full suite `243 passed in
441.71s`; Ruff, governance audit, and diff check passed. The full suite used
its independently planned 8-minute window. Await Liaol's independent G2 review
before closure; M135 remains blocked and no hosted authorization is requested.

## Closure rationale (2026-08-12)

Liaol independently approved the G2 review after checking the bounded scope,
fixed-script mechanism, preserved no-input boundary, validation evidence, and
M135/M137 lifecycle alignment. M136 closes as offline-only remediation. It
does not reactivate M135 or authorize any provider request; re-entry remains a
separately user-selected bounded package.
