# Handoff: M87 Block-with-hole Reference-assisted Hosted Smoke

- **Date**: 2026-08-10
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M87-001-reference-assisted-p0-block-with-hole-hosted-smoke`

## Goal

Prepare one separately authorized two-request hosted smoke for P0
`block_with_hole`, using only the qualified single-cut role of the frozen
vertical-cylinder card.

## Done

- User selected M87; no hosted authorization has been granted yet.
- Local implementation, tests, and read-only hosted preflight are complete.
  The fixed input, manifest membership, card/index hashes, configuration entry,
  report/monitor freshness, and `wsl-bwrap` absent-input preflight passed.
- The authorized run terminalized `completed` with exactly two requests. It
  returned the fixed card for `single boolean-cut tool`, passed the OCP,
  sandbox, provenance, output, and all geometry gates, and recorded no input
  access.

## In progress

- Liaol independently approved M87 on 2026-08-10.

## Next

- M87 is closed. A `three_hole_plate` hosted smoke, if selected, requires a
  new workpack, preflight, budget, and explicit authorization.

## Decisions

- M85 stays a fixed `cylinder` command; M87 must have a separate fixed command.
- Any failure is terminal and cannot advance to `three_hole_plate`.

## Blockers

- None. Any future hosted run needs a new workpack, preflight, budget, and
  explicit authorization.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M87-001-reference-assisted-p0-block-with-hole-hosted-smoke.md` |
| CLI | `brep2code/cli/__init__.py` |
| Report | `data/corpus-runs/m87-block-with-hole-reference-assisted.json` |

## Resume prompt

```
Continue M87. Complete local acceptance and read-only preflight only. Do not
make a hosted request until Liaol explicitly authorizes every listed bound.
```
