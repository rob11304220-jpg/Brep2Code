# Handoff: M135 Frozen Hosted Batch Epoch

- **Date**: 2026-08-12
- **Subproject**: `brep2code`
- **Status**: `active`
- **Related workpack**: `WP-M135-001-frozen-hosted-batch-epoch-preflight-and-execution`

## Goal

Preflight and, only after independent review plus itemized user authorization,
execute M134's unchanged 18-condition development epoch.

## Done

- User selected M135 and the G3 lifecycle records were created.
- Confirmed that the current CLI has no 18-condition durable epoch runner: it
  has single-, two-, and nine-request checkpoint paths only.  M135 therefore
  owns the minimal frozen runner needed to validate actual accounting.
- Confirmed M129's provider-bound instruction now rejects `cadquery`,
  `OCC.Core`, and invented/unavailable OCP symbols before execution.
- Added `m135_epoch.py`: it freezes the five-family development cohort, checks
  each selected STEP SHA-256, creates a fresh 18-request checkpoint, records
  condition terminals, and marks unissued rows on an integrity fault.
- Added offline fake-epoch tests: all 18 conditions can reach terminal `pass`
  with `18/18` request accounting; a per-condition script/API failure permits
  the next condition; an integrity fault stops unissued conditions.
- Added direct hash-checked guidance injection so the prismatic card treatment
  remains one provider request, not M97's two-request guidance-tool lifecycle.
- Passed focused epoch tests (3 passed), direct-guidance test (1 passed), fast
  suite (66 passed), affected-file Ruff, governance audit, and diff check.
- Passed the existing three-row prismatic no-input `wsl-bwrap` preflight.

## In progress

- None. M135 is stopped at its reproducible local preflight blocker.

## Next

- Wait for the user to select a new bounded remediation or re-entry workpack.
  Do not issue provider work, reuse paths/budget, skip the failed condition, or
  repair M135 in place.

## Decisions

- M134's condition-continuation versus epoch-integrity distinction remains
  unchanged; no terminal observation may change a later condition.
- A dedicated runner is required before actual 18-request accounting can be
  preflighted; existing commands cannot truthfully prove it.
- [ADR-0068](../architecture/adr/0068-frozen-epoch-checkpoint-and-transcript-contract.md)
  freezes the one-request-per-condition checkpoint and transcript boundary.

## Blockers

- Reproducible no-input `wsl-bwrap` failure at
  `axisymmetric_revolve:param_revolve_centered_low:no_card`; M135 cannot request
  hosted authorization, issue another condition, or repair this condition.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M135-001-frozen-hosted-batch-epoch-preflight-and-execution.md` |
| Frozen policy | `docs/workflow/m134-frozen-hosted-batch-epoch-policy.md` |
| Predecessor ADR | `docs/architecture/adr/0067-frozen-hosted-batch-epochs.md` |
| Epoch implementation | `brep2code/agent/m135_epoch.py` |
| Focused tests | `tests/test_m135_epoch.py` |
| Reproduce blocker | `uv run python -m pytest tests\test_m135_epoch.py -k no_card_inputs_pass_no_input_wsl_bwrap -q` |

## Resume prompt

    Resume Brep2Code from M135's blocked preflight state. Read this handoff and WP-M135-001. First action: wait for the user to select a separate bounded remediation/re-entry workpack; do not construct a provider, send data, reuse M135 paths/budget, or repair the frozen epoch in place.
