# WP-M36-001: Status and Evidence Ledger

- Status: done
- Milestone: M36
- Owner: Codex

## Goal

Reduce the current-status entry point to an operational dashboard while keeping
milestone history and deferred-decision evidence discoverable and auditable.

## Scope

- Move status-page history into a dedicated milestone index.
- Add a small structured ledger for current deferred decision packages.
- Link the workflow route and enforce the new entry-point invariants.

## Decision-package impact

- `decision_id`: none; this documents existing Q01--Q04 decisions without
  changing their triggers or status.
- Q01/Q02 effect: none.
- Q03/Q04 effect: none.
- Evidence role: governance index only; no new evidence.
- Knowledge disposition: no reusable runtime knowledge.

## Compatibility constraints

No Harness, case, manifest, provider, runtime, prompt, helper, IR, SDK, or
hosted-policy change. The canonical current state remains `status.md`.

## Acceptance

```powershell
uv run python tools/check_governance.py
uv run python -m pytest tests/test_governance_audit.py
uv run python -m ruff check .
uv run python -m pytest
git diff --check
```

## Out of scope

Changing any evidence conclusion, selecting a deferred workpack, performing a
hosted request, or modifying corpus/runtime assets.
