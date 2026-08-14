# Handoff: M35 Agent Governance Automation Baseline

- **Date**: 2026-08-07
- **Subproject**: `brep2code`
- **Status**: `done`

## Goal

Mechanically enforce the repository's existing agent-governance lifecycle and
add a minimal CI baseline without changing Harness or hosted-provider behavior.

## Done

- User confirmed the first implementation phase after the governance review.
- M35-001 was created as the bounded execution record.
- Added the governance audit, regression tests, CI workflow, runbook, and
  ADR-0039; focused checks passed.

## In progress

- None.

## Next

- Re-enter only for a new bounded decision package or a separately selected
  governance improvement.

## Decisions

- ADR-0039: use a dependency-free audit as the common local and CI enforcement
  point for lifecycle invariants.

## Blockers

- None.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/done/WP-M35-001-agent-governance-automation-baseline.md` |
| Status | `docs/workflow/status.md` |
| Commands | `uv run python tools/check_governance.py` |

## Resume prompt

```
Resume Brep2Code only when a new bounded decision package or separately selected
governance improvement is available. Read docs/workflow/status.md first.
```
