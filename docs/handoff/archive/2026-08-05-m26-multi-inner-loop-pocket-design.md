# Handoff: M26 multi-inner-loop pocket governance promotion

- **Date**: 2026-08-05
- **Subproject**: `brep2code`
- **Status**: done

## Goal

Evaluate a restricted lifecycle promotion for the six reviewed M26 candidates.

## Done

- M25 governance drift was reconciled across status, roadmap, catalog,
  workpack index, and the historical M25 handoff.
- ADR-0030 and the M26 six-row preregistration define the selected coverage
  gap and retain candidate-only boundaries.
- M26-002 produced six hash-stable experimental candidates and passed the 6/6 scoped family audit.
- M26-003 selected only a separate family-specific promotion proposal.
- ADR-0031 promoted exactly six frozen records to active self-authored cases;
  the scoped family audit and 69-record library replay audit passed.

## In progress

- None.

## Next

- Select a new bounded coverage gap only through a separate workpack.

## Decisions

- The selected gap is multiple inner loops, not generic multi-contour
  recognition or a face-selection extension.
- [ADR-0030](../../architecture/adr/0030-multi-inner-loop-pocket-design.md)
  fixes the grammar and boundaries.
- [ADR-0031](../../architecture/adr/0031-multi-inner-loop-pocket-governance.md)
  limits active maintenance to the six frozen records.

## Blockers

- None. The standing offline case-governance authorization applies; hosted and
  runtime changes remain out of scope.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M26-004-multi-inner-loop-pocket-governance-promotion.md` |
| Preregistration | `docs/corpus/sequence-paired/multi-inner-loop-pocket-v1-preregistration.json` |
| ADR | `docs/architecture/adr/0031-multi-inner-loop-pocket-governance.md` |
| Command | `uv run python tools/audit_sequence_paired_multi_inner_loop_pocket.py` |

## Resume prompt

```
Resume Brep2Code after completed M26-004 offline governance promotion.
Read docs/handoff/active/2026-08-05-m26-multi-inner-loop-pocket-design.md.
First action: select a new bounded coverage gap under the case-library intake contract.
```
