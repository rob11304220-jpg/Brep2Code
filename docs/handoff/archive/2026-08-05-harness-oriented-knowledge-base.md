# Handoff: Harness-Oriented Knowledge Base Architecture

- **Date**: 2026-08-05
- **Subproject**: `brep2code`
- **Status**: done

## Goal

Reposition and organize the project knowledge base around the B-Rep-to-executable-
modeling Harness loop, rather than case-count or feature-coverage accumulation.

## Done

- Added ADR-0035 and the four-layer Q01--Q04 knowledge-base architecture.
- Defined cases as evidence assets (oracle, discriminating/negative control,
  regression, OOD robustness, native-history validation), not as knowledge units.
- Updated the knowledge, corpus, case-library and maintenance entry points; added
  an explicit decision-gap planning model to the coverage matrix.
- Preserved all case, manifest, provider and runtime authority boundaries.

## In progress

- None.

## Next

- Before selecting another case family, identify one Q01--Q04 decision gap and
  use the updated maintenance runbook to state its smallest useful evidence set.

## Decisions

- [ADR-0035](../../architecture/adr/0035-harness-oriented-knowledge-base-architecture.md)
  makes the knowledge base a development-side, traceable decision foundation.
- Existing operation units remain valid; `observables/` and `execution/` are
  future reviewed layers, not empty content to populate speculatively.

## Blockers

- None. This was documentation-only and authorizes no runtime or hosted action.

## Key paths

| Kind | Path |
|---|---|
| Architecture | `docs/architecture/v1/knowledge-base-architecture.md` |
| Decision | `docs/architecture/adr/0035-harness-oriented-knowledge-base-architecture.md` |
| Knowledge index | `docs/corpus/knowledge/README.md` |
| Procedure | `docs/runbooks/modeling-knowledge-maintenance.md` |

## Resume prompt

```
Resume after the Harness-oriented knowledge-base architecture decision.
Read ADR-0035 and docs/architecture/v1/knowledge-base-architecture.md.
Do not select cases by count; first identify a bounded Q01-Q04 decision gap.
```
