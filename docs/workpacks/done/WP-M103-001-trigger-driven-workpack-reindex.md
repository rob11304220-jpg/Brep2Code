# WP-M103-001: Trigger-Driven Workpack Reindex

- Status: done
- Milestone: M103
- Owner: Codex
- Reviewer: not required (G1)
- Risk tier: G1

## Goal

Replace the historical milestone identifiers on unstarted or trigger-blocked
workpacks with stable semantic trigger identifiers, while preserving completed
workpacks and historical evidence as immutable audit records.

## Scope

- Introduce a `deferred/` workpack state directory for future packages that
  cannot be selected until a documented trigger is met.
- Reindex the eligible pending packages as `WP-TRG-*`; remove their legacy M
  metadata and update current navigation links.
- Archive the obsolete fixed-development hosted rerun package as historical
  timeout evidence; it must not be reactivated under its former scope.
- Record that a new M number is allocated only when a user selects and an
  owner activates a fresh bounded execution package.

## Compatibility constraints

No provider, runtime, manifest, case, card, pack, report, policy, gate, or
execution behavior changes. Completed workpacks and their historical M labels
remain immutable evidence.

## Acceptance

```powershell
uv run python tools\check_governance.py
git diff --check
```

## Status transition

Update `status.md` first, then complete the migration, ADR, handoff and
current-route references. Close only after the governance audit passes.

## Out of scope

Selecting a deferred package, satisfying a technical trigger, changing any
hosted authorization boundary, or revising historical results.

## Closure rationale

- Created the semantic `WP-TRG-001` through `WP-TRG-010` deferred queue and
  documented its trigger-to-new-M activation rule.
- Moved the obsolete development-split hosted rerun plan to `archive/` as
  non-runnable timeout evidence; its original reports and historical labels
  remain preserved there.
- Updated current route, ledger, portfolio and workpack navigation links.
- Acceptance on 2026-08-11: `uv run python tools/check_governance.py` and
  `git diff --check` passed.
