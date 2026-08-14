# Handoff: M49 post-M48 closed-loop roadmap

- **Date**: 2026-08-08
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M49-001-post-m48-closed-loop-roadmap`

## Goal

Record the user-selected progression from M48 to a real, secure LLM closed
loop before controlled model variants and external-data evaluation.

## Done

- M48 structured observation and no-input build capability is closed.
- User accepted the identified risks and selected the closed-loop-first route.

## In progress

- M49 G1 documentation and contract alignment are complete.

## Next

- Name an independent reviewer, then select the G2 offline
  observation-to-provider integration and semantic-fix workpack.
- Do not start the next G2 workpack until an independent reviewer is named.

## Decisions

- Use offline fake-provider integration before any real LLM call.
- Keep reference scripts/models as local controls only; never give them to the LLM.
- Treat hosted LLM calls and hosted evaluation as separately authorized G3 work.

## Blockers

- The next G2 semantic/integration work requires an independent reviewer.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M49-001-post-m48-closed-loop-roadmap.md` |
| Roadmap | `docs/architecture/v1/post-m48-closed-loop-roadmap.md` |
| Contract | `docs/architecture/v1/contracts/q01-observation-build-separation.md` |

## Resume prompt

```
Continue M49 documentation only. Read the active workpack and this handoff.
First action: add the post-M48 closed-loop roadmap, then run its G1 acceptance
commands. Do not start a G2/G3 implementation without its selected workpack
and independent reviewer.
```
