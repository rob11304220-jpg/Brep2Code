# Handoff: Sequence-paired prismatic-hole foundation

- **Date**: 2026-08-04
- **Subproject**: `brep2code`
- **Status**: done

## Goal

Complete M20-001: establish and validate an offline, family-isolated paired
benchmark for a planar prismatic base with one cylindrical subtractive feature.
The pilot must test whether a canonical construction sequence and three-layer
geometry/sequence/editability evidence are suitable for later controlled case
growth.

## Done

- User approved the sequence-paired route rather than continuing generic
  B-Rep-only retry growth as the primary development path.
- ADR-0018 records the restricted pilot decision and why it is not a runtime
  IR, SDK, or general B-Rep-to-history claim.
- The active M20-001 workpack and its route roadmap record scope, evidence,
  stopping condition, promotion criteria, and prohibited changes.
- The completed M17 handoff was archived; the restricted Fusion default mapping
  remains unchanged.

## In progress

- None.  M20-001 completed its offline foundation; no provider or runtime work
  is in progress.

## Next

1. If selected by the user, create a separate controlled-expansion workpack
   that retains the grammar and preregisters new whole-family held-out cases.
2. Do not promote M20 metadata or three-layer checks to global governance until
   that workpack is completed and independently reviewed.

## Decisions

- Use a restricted `Sketch -> Extrude -> CutCylinder` pilot, with through,
  blind, and counterbore variants, before any broader data production or IR
  proposal.  See [ADR-0018](../../architecture/adr/0018-sequence-paired-prismatic-hole-pilot.md).
- The three layers are pilot-only until a completed review separately promotes
  them to long-term case-library governance.
- M20-001 passed its three preregistered self-authored oracle cases but is not
  B-Rep-to-sequence or model-generation evidence; see
  [M20 review](../../architecture/v1/m20-sequence-paired-prismatic-hole-foundation-review.md).

## Blockers

- None.  External data, hosted evaluation, and M18 are intentionally outside
  this workpack, not blockers.

## Key paths

| Kind | Path |
|------|------|
| Workpack | `docs/workpacks/active/WP-M20-001-sequence-paired-prismatic-hole-foundation.md` |
| Decision | `docs/architecture/adr/0018-sequence-paired-prismatic-hole-pilot.md` |
| Route | `docs/architecture/v1/sequence-paired-prismatic-hole-roadmap.md` |
| Library | `docs/corpus/library/README.md` |
| Existing cases | `case-library/self-authored/` |

## Resume prompt

```
Continue Brep2Code M20-001 sequence-paired prismatic-hole foundation.
Read docs/handoff/active/2026-08-04-sequence-paired-prismatic-hole-foundation.md
and the completed workpack/review. First action: wait for user selection before
creating a separately scoped controlled-expansion workpack; do not promote the
pilot contract to global governance.
```
