# Handoff: M135 runner-contract re-entry

- **Date**: 2026-08-12
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `none`

## Goal

Freeze the missing M135 request-to-Harness-terminal runner contract. All work
remains offline and credential-free; actual DeepSeek execution remains
unapproved.

## Done

- Archived M135-002 through M135-007, leaving no active workpack until the
  user selected M135-008.
- Added local-only M135 epoch preflight, condition and path-free transcript
  hashing, checkpoint/report contracts, CLI coverage and documentation.
- Verified `uv run python -m pytest tests\\test_m135_epoch.py -q` (8 passed),
  `uv run python -m ruff check .`, `uv run python tools\\check_governance.py`
  and `git diff --check`.

## In progress

- M135-008 is complete: the exact system instruction, one-request prismatic
  card injection, no-input Harness route and terminal mapping are frozen and
  have independent G3 review approval.

## Next

1. Only after a separately user-selected serial-lifecycle workpack passes
   offline validation may a fresh hosted-preflight workpack be selected.
2. Request itemized hosted authorization only after that fresh preflight
   pass offline validation, create a fresh hosted preflight workpack.  Request
   itemized user authorization only after that fresh preflight passes.

## Decisions

- Do not add a provider-only execute command: treating a returned script as
  success would bypass the required no-input `wsl-bwrap` Harness/CAD gate.
- Preserve the user's unrelated `.tmp-m127-*` files; they are excluded from
  the M135 commit.
- Existing M135 report/monitor paths cannot be reused for a hosted run; a
  future preflight needs fresh paths and fresh authorization.

## Blockers

- Hosted execution cannot be authorized: this offline contract, a separate
  serial lifecycle workpack and a fresh hosted preflight must all finish
  first; no authorization has been requested.
- None for the completed runner-contract workpack.

## Key paths

| Kind | Path |
|---|---|
| Branch | `main` |
| Status | `docs/workflow/status.md` |
| Blocker record | `docs/workflow/m135-007-frozen-epoch-execute-lifecycle.md` |
| Epoch code | `brep2code/agent/m135_epoch.py` |
| CLI | `brep2code/cli/__init__.py` |
| Tests | `tests/test_m135_epoch.py` |
| Commands | `uv run python -m pytest tests\\test_m135_epoch.py -q`; `uv run python -m ruff check .`; `uv run python tools\\check_governance.py` |

## Resume prompt

```
Continue Brep2Code work only after the user selects the next bounded M135
serial-lifecycle workpack.
Read docs/workflow/status.md and the most recent active handoff.
First action: do not infer hosted authorization from M135-008 closure.
```
