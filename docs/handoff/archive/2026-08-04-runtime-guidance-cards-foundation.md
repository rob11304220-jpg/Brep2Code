# Handoff: Runtime guidance cards foundation

- **Date**: 2026-08-04
- **Subproject**: `brep2code`
- **Status**: done

## Goal

Establish an evidence-bounded, offline foundation for preserving reusable
development-agent evidence as future runtime-operational material.

## Done

- Added static experience-card contract, index, three source-linked starter
  cards, and an offline audit.
- Recorded ADR-0016 and the authoring runbook; no runtime integration exists.

## In progress

- None.

## Next

- Future completed case workpacks should classify reusable evidence, a
  counterexample, or no card under ADR-0016. Do not mount or retrieve cards
  without a separately scoped development-only evaluation.
- M19-002 is the first evidence-gated continuation; M19-003 remains blocked
  until its offline review completes without a gate regression.

## Decisions

- Cards are evidence-bounded runtime resources, not copies of docs or automatic
  prompt context; see [ADR-0016](../../architecture/adr/0016-evidence-bounded-runtime-guidance-cards.md).

## Blockers

- None.

## Key paths

| Kind | Path |
|---|---|
| Card index | `runtime_resources/experience-cards/index.json` |
| Audit | `tools/audit_runtime_guidance.py` |
| Governance | `docs/architecture/adr/0016-evidence-bounded-runtime-guidance-cards.md` |
| Next workpacks | `docs/workpacks/backlog/WP-M19-002-development-guidance-retrieval-evaluation.md`, `docs/workpacks/backlog/WP-M19-003-bounded-runtime-guidance-retrieval.md` |

## Resume prompt

```
Continue Brep2Code from the completed runtime-guidance-cards foundation.
Read the workflow status and the archived handoff for this completed work.
Do not integrate cards into the runtime without a separately scoped,
development-only retrieval evaluation.
```
