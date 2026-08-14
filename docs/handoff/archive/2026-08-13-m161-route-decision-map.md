# Handoff: M161 route decision map

- **Date**: 2026-08-13
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M161-001-route-decision-map`

## Goal

Add a route-level decision-navigation map that complements the per-hypothesis
theory map and prevents deferred workpacks from being mistaken for an active
route queue.

## Done

- Drafted the map, ADR-0080, AGENTS route entry and active G1 workpack.

## In progress

- None.

## Next

- A future user-selected governance review may apply the map's disposition
  vocabulary to the deferred workpack inventory.

## Decisions

- The map is navigation only; it does not dispose of historical workpacks.
- [ADR-0080](../../architecture/adr/0080-route-decision-map.md) records the lasting routing decision.

## Blockers

- None.

## Key paths

| Kind | Path |
|---|---|
| Files | `docs/architecture/v1/route-decision-map.md`, `docs/workpacks/active/WP-M161-001-route-decision-map.md` |
| Commands | `uv run python tools/check_governance.py`; `git diff --check` |

## Resume prompt

```
Continue Brep2Code work: close M161 route decision map.
Read docs/handoff/active/2026-08-13-m161-route-decision-map.md.
First action: run the two recorded acceptance commands and resolve any failures.
```
