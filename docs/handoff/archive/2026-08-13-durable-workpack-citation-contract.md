# Handoff: Durable workpack citation contract

- **Date**: 2026-08-13
- **Subproject**: `brep2code`
- **Status**: `active`
- **Related workpack**: `WP-M165-001-durable-workpack-citation-contract`

## Goal

Freeze the durable citation contract for completed and archived workpacks.

## Done

- Confirmed that no prior active workpack or handoff exists.
- Created M165 as the first user-selected governance-series package.

## In progress

- Define the permitted stable-document reference classes and exceptions.

## Next

- Update workpack governance and low-context navigation.
- Run the G1 governance audit and `git diff --check`.

## Decisions

- The workpack remains an execution ledger; stable records own current facts,
  route decisions, contracts and evidence interpretation.

## Blockers

- None.

## Key paths

| Kind | Path |
|------|------|
| Files | `docs/workflow/workpack-governance.md`, `docs/workflow/navigation.md` |
| Files | `docs/workpacks/active/WP-M165-001-durable-workpack-citation-contract.md` |
| Commands | `uv run python tools/check_governance.py`; `git diff --check` |

## Resume prompt

```
Continue Brep2Code work: complete M165 durable workpack citation contract.
Read docs/handoff/active/2026-08-13-durable-workpack-citation-contract.md.
First action: update the governance and navigation documents, then run acceptance.
```
