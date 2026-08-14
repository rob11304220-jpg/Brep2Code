# Handoff: M91 M90 case-metadata lifecycle alignment

- **Date**: 2026-08-10
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M91-002-m90-case-metadata-lifecycle-alignment`

## Goal

Bring the six M90 `case.json` lifecycle statements into agreement with the
already active registry and ADR-0055 without changing any executable boundary.

## Done

- G1 documentation/index alignment completed and archived separately.

## In progress

- None.

## Next

- Archive this completed handoff; select a new bounded package only on user
  direction.

## Decisions

- The correction confirms active governance status only; all six records stay
  outside executable manifests, provider inputs, training and runtime.

## Blockers

- None. Liaol independently approved the six-field scope and offline evidence
  on 2026-08-10.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M91-002-m90-case-metadata-lifecycle-alignment.md` |
| Registry | `docs/corpus/registry/self-authored.json` |
| Authority | `docs/architecture/adr/0055-repeated-feature-pattern-governance.md` |

## Resume prompt

```
Continue M91-002 M90 case-metadata lifecycle alignment. Read the active
handoff and workpack, run the declared replay/family/governance checks, then
request Liaol's independent review before closure.
```
