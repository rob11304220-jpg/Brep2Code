# Handoff: M27 oriented rounded-slot design

- **Date**: 2026-08-05
- **Subproject**: `brep2code`
- **Status**: done

## Goal

Complete the restricted governance promotion for the six reviewed M27
oriented-rounded-slot candidates.

## Done

- M26 governance promotion is complete and its handoff is archived.
- ADR-0032 and the M27 six-row preregistration define only +X/+Y
  axis-aligned rounded-slot frames.
- The reusable M24 intake audit passed the frozen record.
- M27-002 produced six hash-stable experimental candidates and passed the 6/6
  scoped family audit.
- M27-003 selected only a separate family-specific promotion proposal.
- ADR-0033 promoted exactly the six frozen records to active self-authored
  cases; the family audit and 75-record library replay audit passed.

## In progress

- None.

## Next

- Select a new bounded coverage gap only through a separate workpack.

## Decisions

- The selected gap is profile orientation ambiguity, not arbitrary rotation or
  generic sketch-frame inference.
- [ADR-0032](../../architecture/adr/0032-oriented-rounded-slot-design.md)
  limits the grammar to declared +X and +Y axes.
- [ADR-0033](../../architecture/adr/0033-oriented-rounded-slot-governance.md)
  limits active maintenance to the six frozen records.

## Blockers

- None. The standing offline case-governance authorization applies; hosted and
  runtime changes remain out of scope.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/done/WP-M27-004-oriented-rounded-slot-governance-promotion.md` |
| Preregistration | `docs/corpus/sequence-paired/oriented-rounded-slot-v1-preregistration.json` |
| ADR | `docs/architecture/adr/0033-oriented-rounded-slot-governance.md` |
| Command | `uv run python tools/audit_sequence_paired_oriented_rounded_slot.py` |

## Resume prompt

```
Resume Brep2Code after completed M27 offline governance promotion.
Read docs/handoff/active/2026-08-05-m27-oriented-rounded-slot-design.md.
First action: select a new bounded coverage gap under the case-library intake contract.
```
