# Handoff: M22-002 multi-contour pocket production complete

- **Date**: 2026-08-05
- **Subproject**: `brep2code`
- **Status**: done

## Goal

Preserve the reviewed `multi-contour-pocket-v1` evidence until a separately
selected M22-004 governance-promotion workpack.

## Done

- The producer generated exactly six preregistered experimental candidates,
  three centered development and three offset held-out, with clean-directory
  byte-stable normalized STEP hashes.
- All six passed existing geometry gates, exact four-operation sequence,
  containment, single-solid, blind-annular-volume, outer-extent, editability,
  and split-isolation checks.
- Family audit passed 6/6; focused tests passed 4; the 45-record case-library
  replay audit, Ruff, and `git diff --check` passed.
- Candidates remain unregistered and absent from manifests, provider,
  training, and runtime paths. No runtime card or knowledge-unit promotion was
  made.
- M22-003 completed and created the bounded `multi-contour-pocket-v1`
  knowledge unit. It selected only M22-004; it did not promote a candidate.

## In progress

- No active workpack.

## Next

1. Await explicit selection of M22-004.
2. If selected, require a dedicated ADR before auditing a potential
   family-specific governance promotion.

## Decisions

- M22-002 validates only a self-authored deterministic-oracle grammar. It
  does not establish general multi-contour recognition, native history, or
  B-Rep-to-sequence recovery.
- M22-003 must determine whether a bounded knowledge unit is justified or a
  no-reusable-knowledge outcome is more accurate. See [M22-002 review](../../architecture/v1/m22-multi-contour-pocket-controlled-production-review.md).

## Blockers

- M22-004 requires separate user selection.

## Key paths

| Kind | Path |
|---|---|
| Completed workpack | `docs/workpacks/done/WP-M22-002-multi-contour-pocket-controlled-production.md` |
| Review | `docs/architecture/v1/m22-multi-contour-pocket-controlled-production-review.md` |
| Producer | `tools/build_m22_multi_contour_pocket_candidates.py` |
| Audit | `tools/audit_sequence_paired_multi_contour_pocket.py` |
| M22-003 review | `docs/architecture/v1/m22-cross-family-dependency-review.md` |
| Completed successor workpack | `docs/workpacks/done/WP-M22-004-multi-contour-pocket-governance-promotion.md` |

## Resume prompt

```
Await explicit selection of M22-004. Read this handoff, the M22-003 review,
the frozen preregistration, and ADR-0022. Do not promote candidates, modify a
manifest, or begin a successor family before a dedicated ADR is accepted.
```
