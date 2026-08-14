# Handoff: M25-001 face-selected dependent-cut design complete

- **Date**: 2026-08-05
- **Subproject**: `brep2code`
- **Status**: done

## Goal

Freeze a narrow B-Rep-observable boss-top face selector before any dependent-
cut candidate production.

## Done

- ADR-0028 and the six-row preregistration freeze a `SelectPlanarFace` step.
- The selector requires exactly one planar +Z face at maximum output Z on the
  boss body; wrong-face, vertical-face, and ambiguity are rejection classes.
- M25 intake audit passed; no assets were created.

## In progress

- No active workpack.

## Next

- Await user selection of M25-002 controlled production. Do not generate
  candidates or broaden the selector automatically.

## Decisions

- The bounded selector contract is defined by [ADR-0028](../../architecture/adr/0028-face-selected-dependent-cut-design.md).

## Blockers

- M25-002 requires separate user selection.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/done/WP-M25-001-face-selected-dependent-cut-design.md` |
| Preregistration | `docs/corpus/sequence-paired/face-selected-dependent-cut-v1-preregistration.json` |
| Proposed production | `docs/workpacks/backlog/WP-M25-002-face-selected-dependent-cut-controlled-production.md` |

## Resume prompt

```
Read this handoff and docs/workflow/status.md. M25-002 is not selected; do not
generate face-selected candidates without a new explicit user choice.
```
