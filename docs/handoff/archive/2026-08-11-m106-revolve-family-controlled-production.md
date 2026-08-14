# Handoff: M106 Revolve Family Controlled Production

- **Date**: 2026-08-11
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M106-001-revolve-family-controlled-production`

## Goal

Generate and audit only the six M105-frozen `revolve-v1` experimental
candidates, retaining all split and lifecycle boundaries.

## Done

- User selected the former `WP-TRG-013`; it is active as M106-001.
- Six frozen experimental candidates passed controlled production and audit.
- Liaol approved independent G2 review and closure on 2026-08-11.

## In progress

- None.

## Next

- Await an explicit user selection before activating `WP-TRG-014` or another
  bounded package.

## Decisions

- M105's preregistration and ADR-0063 are immutable inputs.
- Candidates remain experimental and outside registry, manifest, provider and
  runtime scope.

## Blockers

- Full replay-audit blocker: an existing active-library reference replay did
  not create `output/model.step`. Do not replace rows or broaden the grammar.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M106-001-revolve-family-controlled-production.md` |
| Freeze | `docs/corpus/sequence-paired/revolve-v1-preregistration.json` |
| ADR | `docs/architecture/adr/0063-revolve-v1-design-freeze.md` |

## Resume prompt

```
Continue Brep2Code M106-001 revolve-family controlled production.
Read docs/handoff/active/2026-08-11-m106-revolve-family-controlled-production.md and the frozen preregistration.
First action: implement deterministic candidate production and an audit for exactly the six frozen rows; do not alter the preregistration or call a provider.
```
