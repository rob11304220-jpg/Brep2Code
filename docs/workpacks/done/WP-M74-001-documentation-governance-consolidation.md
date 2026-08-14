# WP-M74-001: Documentation Governance Consolidation

- Status: done
- Milestone: M74
- Owner: Codex
- Reviewer: not required (G1)
- Risk tier: G1

## Goal

Make current-state, backlog, completed-workpack and archived-handoff semantics
unambiguous, machine-checkable and inexpensive to navigate.

## Scope

- Normalize completed and backlog workpack state fields without changing their
  historical evidence.
- Define archive-snapshot interpretation and a short current/archive navigation
  index.
- Extend the dependency-free governance audit to enforce terminal/backlog
  directory-state invariants and parse a valid status-page update date.
- Correct identified status/history wording inconsistencies and document the
  low-context reading route.

## Compatibility constraints

Documentation/governance only. Do not alter Harness, provider, runtime,
manifest, case membership, credentials, hosted authorization or evidence-ledger
decisions.

## Acceptance

```powershell
uv run python tools\check_governance.py
uv run python tools\check_governance.py --inventory
git diff --check
```

## Status transition

On completion, update `docs/workflow/status.md` first, move this workpack to
`done/` with `Status: done`, archive its handoff, and record the acceptance
output and closure rationale.

## Out of scope

Deleting historical records, rewriting historical handoff content, changing
research conclusions, automating task selection, or creating a hosted task.

## Closure rationale

- Corrected the nine terminal workpack headers that contradicted their `done/`
  location, and normalized two non-parseable backlog headers.
- Added explicit historical-snapshot semantics for archived handoffs and a
  low-context navigation document.
- Extended `tools/check_governance.py` to validate done/backlog directory
  states and the status-page update date; `--inventory` exposes compact JSON
  entry metadata without reading archive contents.
- Acceptance on 2026-08-09: `uv run python -m py_compile
  tools\\check_governance.py`, `uv run python tools\\check_governance.py`,
  `uv run python tools\\check_governance.py --inventory`, and `git diff --check`
  all passed.
