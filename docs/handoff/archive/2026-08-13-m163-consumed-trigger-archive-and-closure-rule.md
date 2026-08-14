# Handoff: M163 consumed-trigger archive and closure rule

- **Date**: 2026-08-13
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M163-001-consumed-trigger-archive-and-closure-rule`

## Goal

Apply the permanent closure rule to six verified consumed triggers and add the durable-conclusion/disposition field to the workpack template.

## Done

- Verified the consumed relationships against M154 and M157 records.
- Drafted the template and disposition-index updates.

## In progress

- None.

## Next

- Select a separate review before classifying any unconsumed historical route.

## Decisions

- Consumed trigger records are archived only after their durable successor is verified.

## Blockers

- None.

## Key paths

| Kind | Path |
|---|---|
| Files | `docs/workflow/workpack-route-disposition-index.md`, `docs/workpacks/archive/` |
| Commands | `uv run python tools/check_governance.py`; `git diff --check` |

## Resume prompt

```
Continue Brep2Code work: close M163 consumed-trigger archive and closure rule.
Read docs/handoff/active/2026-08-13-m163-consumed-trigger-archive-and-closure-rule.md.
First action: move verified consumed triggers to archive, then run acceptance.
```
