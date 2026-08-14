# Handoff: efficient four-track operating model

- **Date**: 2026-08-11
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M101-001-efficient-four-track-operating-model`

## Goal

Document an efficient, evidence-gated operating cadence across the existing
four tracks without changing technical or hosted boundaries.

## Done

- User selected the G1 route-governance package.
- Added ADR-0060, roadmap cadence and portfolio-maintenance routing.
- Governance and diff checks passed.

## In progress

- None; M101-001 is complete.

## Next

1. Archive this completed handoff with M101-001.
2. Await the user's selection of one candidate package from the near-term cadence.

## Decisions

- The operating model coordinates work but never authorizes runtime/provider
  activity or replaces per-track evidence gates.
- [ADR-0060](../architecture/adr/0060-efficient-four-track-operating-model.md)
  records the operating-model boundary.

## Blockers

- None.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M101-001-efficient-four-track-operating-model.md` |
| Roadmap | `docs/architecture/v1/four-track-program-roadmap.md` |
| Inputs | `docs/corpus/case-portfolio.md`, `docs/workflow/hosted-experiment-registry.md` |
| Acceptance | `uv run python tools/check_governance.py`; `git diff --check` |

## Resume prompt

```
Continue Brep2Code work: select the next bounded package after M101-001.
Read docs/handoff/active/2026-08-11-efficient-four-track-operating-model.md.
First action: read docs/workflow/status.md and select a candidate package; do
not select M98 or issue a provider request by default.
```
