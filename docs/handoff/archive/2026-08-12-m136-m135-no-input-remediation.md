# Handoff: M136 M135 No-Input Sandbox Preflight Remediation

- **Date**: 2026-08-12
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M136-001-m135-no-input-sandbox-preflight-remediation`

## Goal

Diagnose and make the smallest offline-only repair for M135's centered-low
revolve no-input `wsl-bwrap` fixed-script preflight failure.

## Done

- Corrected M135's workpack lifecycle status to `blocked` and wrote its missing
  local preflight record.
- Reproduced the fixed failure: the designated M135 no-card preflight test
  returns `1 failed, 3 deselected in 26.48s` at
  `axisymmetric_revolve:param_revolve_centered_low:no_card`.
- User selected M136-001 as the distinct G2 offline remediation.
- ADR-0069 reschedules the unstarted terminal evidence review from M136 to
  M137; it remains downstream of fresh M135 preflight, authorization, and a
  terminal epoch.
- Diagnosed `ModuleNotFoundError: No module named 'tools'` in the no-input
  sandbox and made the nine affected centered development scripts self-contained.
- Added a forbidden repository-helper import regression assertion. Focused
  M135: 5 passed; fast: 66 passed; full suite: 243 passed in 441.71s; Ruff,
  governance audit, and diff check passed.

## In progress

- None. M136 is closed after Liaol's independent G2 approval.

## Next

- Wait for explicit user selection of a fresh M135 re-entry workpack. Do not
  construct a provider, send data, change frozen M135 policy inputs, or request
  hosted authorization.

## Decisions

- M135 remains frozen and blocked; its paths, budget, and authority cannot be
  reused.
- M136 is offline-only. A successful repair only permits a later fresh M135
  G3 preflight; it does not itself grant hosted authority.
- M137 is the renamed terminal evidence review.

## Blockers

- M135 remains blocked until a separately selected fresh G3 preflight.

## Key paths

| Kind | Path |
|---|---|
| Active workpack | `docs/workpacks/active/WP-M136-001-m135-no-input-sandbox-preflight-remediation.md` |
| M135 blocked record | `docs/workflow/m135-frozen-epoch-preflight-blocked.md` |
| M136 repair record | `docs/workflow/m136-m135-no-input-sandbox-remediation-record.md` |
| M135 test | `tests/test_m135_epoch.py` |
| M135 runner | `brep2code/agent/m135_epoch.py` |
| Rescheduling ADR | `docs/architecture/adr/0069-m135-remediation-and-terminal-review-rescheduling.md` |

## Resume prompt

    Resume M136-001. Read status.md, WP-M136-001, the M135 blocked preflight
    M136 is closed. Wait for explicit user selection of M135 re-entry; then
    use unchanged frozen inputs and a fresh G3 preflight only. Do not construct
    a provider, send data, or alter M135's frozen cohort/policy. M137 is
    terminal review only after a fresh authorized M135 epoch.
