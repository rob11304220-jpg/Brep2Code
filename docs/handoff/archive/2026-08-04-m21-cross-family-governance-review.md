# Handoff: M21 cross-family governance review

- **Date**: 2026-08-04
- **Subproject**: `brep2code`
- **Status**: done

## Goal

Complete the user-selected, offline M20/M21 cross-family governance review
and close the associated development-document loop without promoting assets.

## Done

- Completed M21-003: compared both frozen sequence-pair evidence sets,
  recorded all backlog dispositions, and added durable document-layer and
  closure guidance.
- Added M21-004 only as a user-selected backlog proposal. It requires its own
  ADR before it can change case lifecycle or metadata.
- Verified `uv run python tools/audit_case_library.py --replay` for 42 records
  and `git diff --check`.

## In progress

- None. There is no active workpack.

## Next

1. Wait for the user to select M21-004 or another explicitly scoped backlog
   route.

## Decisions

- ADR-0019 remains limited to `prismatic-hole-v1`; ADR-0020 remains the
  prerequisite for every future cross-family expansion.
- M21-003 proposes, but does not accept, a rounded-slot governance promotion.

## Blockers

- None.

## Key paths

| Kind | Path |
|---|---|
| Completed workpack | `docs/workpacks/done/WP-M21-003-cross-family-sequence-pair-governance-review.md` |
| Completion review | `docs/architecture/v1/m21-cross-family-sequence-pair-governance-review.md` |
| Proposed workpack | `docs/workpacks/backlog/WP-M21-004-rounded-slot-governance-promotion.md` |
| Status | `docs/workflow/status.md` |

## Resume prompt

```
Resume after completed M21-003. Read the workflow status and the M21-003
review. Do not promote rounded-slot assets unless the user explicitly selects
M21-004 and its dedicated ADR is accepted.
```
