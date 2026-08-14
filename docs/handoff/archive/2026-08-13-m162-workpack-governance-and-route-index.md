# Handoff: M162 workpack governance and route index

- **Date**: 2026-08-13
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M162-001-workpack-governance-and-route-index`

## Goal

Establish workpack execution-ledger governance and a first route-disposition
index for the current closed-loop cluster.

## Done

- Drafted the governance document, current-cluster index, ADR and entry links.

## In progress

- None.

## Next

- A future selected inventory review may classify historical deferred clusters
  and migrate their navigation to durable authorities.

## Decisions

- [ADR-0081](../../architecture/adr/0081-workpack-execution-ledger-governance.md) makes durable authority promotion mandatory at closure.

## Blockers

- None.

## Key paths

| Kind | Path |
|---|---|
| Files | `docs/workflow/workpack-governance.md`, `docs/workflow/workpack-route-disposition-index.md` |
| Commands | `uv run python tools/check_governance.py`; `git diff --check` |

## Resume prompt

```
Continue Brep2Code work: close M162 workpack governance and route index.
Read docs/handoff/active/2026-08-13-m162-workpack-governance-and-route-index.md.
First action: archive consumed TRG-038, then run the acceptance commands.
```
