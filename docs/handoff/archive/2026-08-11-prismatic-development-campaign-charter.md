# Handoff: Prismatic Development Campaign Charter

- **Date**: 2026-08-11
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M120-001-prismatic-development-campaign-charter`

## Goal

Freeze one planning-only prismatic development campaign charter under the
completed M115 successor policy, without reopening hosted scope or creating
preflight/authorization authority.

## Done

- Read the current hosted-evaluation framing, the `WP-TRG-016` trigger, and
  the completed M115 successor-policy records.
- Drafted
  `docs/workflow/m120-prismatic-development-campaign-charter.md` with the
  bounded question, development-row scope, limited egress, interpretation
  table, planned report/monitor paths, and old-route noise check.
- Updated `status.md` and the current hosted candidate plan so prismatic
  charter drafting is treated as completed offline preparation rather than a
  pending route.

## In progress

- None.

## Next

- Await explicit user selection of a new bounded package. If hosted progress is
  chosen, the next shared entry remains `WP-TRG-005`; only after that gate
  reopens may a fresh prismatic G3 readiness/preflight package carry this
  charter forward.

## Decisions

- M120 freezes a planning-only charter, not a runnable campaign. It chooses no
  provider authority, requests no authorization, and reuses no M97 or M118
  capacity.

## Blockers

- Shared hosted-stability re-entry remains unmet.

## Key paths

| Kind | Path |
|------|------|
| Workpack | `docs/workpacks/done/WP-M120-001-prismatic-development-campaign-charter.md` |
| Charter | `docs/workflow/m120-prismatic-development-campaign-charter.md` |
| Policy | `docs/corpus/registry/m115-prismatic-development-card-effect-policy-v1.json` |
| Commands | `python tools\check_governance.py` |

## Resume prompt

```
M120-001 is closed. Read docs/workflow/status.md and wait for a user-selected
bounded package. If hosted progress is chosen, start with WP-TRG-005 rather
than reopening old prismatic trigger routes.
```
