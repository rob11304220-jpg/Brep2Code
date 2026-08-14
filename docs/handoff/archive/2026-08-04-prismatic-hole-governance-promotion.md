# Handoff: Prismatic-hole governance promotion

- **Date**: 2026-08-04
- **Subproject**: `brep2code`
- **Status**: done

## Goal

M20-003 completed: it promoted only the validated `prismatic-hole-v1`
sequence-pair metadata into durable self-authored case-library governance, with
no runtime or automatic-admission change.

## Done

- M20-002 completed with all preregistered nine cases passing its three layers.
- User explicitly authorized the separately scoped governance-promotion work.
- ADR-0019 and M20-003 define the limited promotion boundary.
- Nine records now carry scoped metadata; 42 active self-authored cases replay
  and audit successfully.  Counterbore cases are absent from all manifests.

## In progress

- No M20 work remains in progress.

## Next

1. Await explicit user direction before proposing a second paired family.

## Decisions

- Promotion is limited to `prismatic-hole-v1`; no general sequence metadata or
  IR is introduced.  See [ADR-0019](../../architecture/adr/0019-prismatic-hole-sequence-pair-governance.md).

## Blockers

- None.

## Key paths

| Kind | Path |
|------|------|
| Workpack | `docs/workpacks/done/WP-M20-003-prismatic-hole-governance-promotion.md` |
| ADR | `docs/architecture/adr/0019-prismatic-hole-sequence-pair-governance.md` |
| Audit | `tools/audit_case_library.py` |
| Review | `docs/architecture/v1/m20-prismatic-hole-governance-promotion-review.md` |

## Resume prompt

```
Continue after M20-003. Read the completion review and workflow status; wait
for explicit user direction before proposing a second sequence-paired family.
```
