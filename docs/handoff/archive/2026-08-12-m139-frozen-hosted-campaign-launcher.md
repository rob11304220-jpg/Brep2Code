# Handoff: M139 Frozen Hosted Campaign Launcher

- **Date**: 2026-08-12
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M139-001-frozen-hosted-campaign-launcher`

## Goal

Design and locally implement the reusable, fail-closed campaign launcher that
prepares one frozen hosted campaign without provider construction or egress.

## Done

- User selected TRG-024; it is active as M139 G2 with Liaol as independent
  reviewer.
- The post-M138 route establishes the dependency order through TRG-028.
- Added ADR-0070, launcher contract/runbook, `brep2code.campaign` and the
  offline-only `campaign-prepare` CLI with focused regression coverage.

## In progress

- None.  M139 owner validation and Liaol's independent G2 review are complete.

## Next

- M140 separately consumes TRG-025 for the Harness tool-mediated agent loop.

## Decisions

- M139 is offline and credential-free.  `execute` is an admission contract
  only; no provider construction or hosted request belongs in this workpack.
- M135-011 remains immutable terminal evidence and cannot supply capacity,
  paths, authorization or a repair budget.
- The campaign spec is immutable intent; the prepared report binds its digest
  and locally re-derived identity, but remains `not_authorized`.
- Liaol approved M139's independent G2 review.  The completed workpack is
  archived; no hosted authority follows.

## Blockers

- None.

## Key paths

| Kind | Path |
|------|------|
| Workpack | `docs/workpacks/active/WP-M139-001-frozen-hosted-campaign-launcher.md` |
| Route | `docs/architecture/v1/post-m138-runtime-and-knowledge-route.md` |
| Existing epoch | `brep2code/agent/m135_epoch.py` |
| Generic CLI | `brep2code/cli/__init__.py` |
| Commands | `uv run python tools/check_governance.py`; `git diff --check` |

## Resume prompt

```
Continue Brep2Code work: implement M139's offline frozen hosted campaign launcher.
Read docs/handoff/active/2026-08-12-m139-frozen-hosted-campaign-launcher.md.
First action: map M135 and generic CLI contracts to the campaign-spec state machine before editing runtime code.
```
