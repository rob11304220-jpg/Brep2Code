# Handoff: case and hosted evidence portfolio

- **Date**: 2026-08-11
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M100-001-case-and-hosted-evidence-portfolio`

## Goal

Create a documentation-only portfolio for case readiness and hosted experiment
outcomes while preserving all existing evidence and authorization boundaries.

## Done

- User selected the bounded G1 documentation-governance package.
- Added case-readiness and hosted-result navigation pages, ADR-0059 and a
  maintenance runbook.
- Governance audit and diff hygiene checks passed.

## In progress

- None; M100-001 is complete.

## Next

1. Archive this completed handoff with M100-001.
2. Await user selection of any follow-up bounded workpack.

## Decisions

- The new pages are navigation projections, not registries, manifests, report
  schemas or hosted authorization records.
- Separate case cards, reference packs and runtime experience cards explicitly.
- [ADR-0059](../architecture/adr/0059-case-and-hosted-evidence-portfolio.md)
  records the lasting navigation boundary.

## Blockers

- None.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M100-001-case-and-hosted-evidence-portfolio.md` |
| Status | `docs/workflow/status.md` |
| Inputs | `docs/corpus/registry/self-authored.json`, `docs/corpus/reference-packs/`, `runtime_resources/experience-cards/`, `data/corpus-runs/` |
| Acceptance | `uv run python tools/check_governance.py`; `git diff --check` |

## Resume prompt

```
Continue Brep2Code work: select the next bounded package after M100-001.
Read docs/handoff/active/2026-08-11-case-and-hosted-evidence-portfolio.md.
First action: read docs/workflow/status.md; M100-001 is complete and no active
workpack remains.
```
