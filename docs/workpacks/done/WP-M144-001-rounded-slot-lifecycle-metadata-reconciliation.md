# WP-M144-001: Rounded-Slot Lifecycle Metadata Reconciliation

- Status: done
- Milestone: M144
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

> Historical note: M159 later supersedes this active-promotion conclusion for
> the three rows after their authoritative `case.json` records were explicitly
> downgraded to `experimental`. The commands and results below remain M144
> closure evidence, not a statement of the current lifecycle state.

## Entry condition

M143's metadata-only inventory found that ADR-0023 and the active registry
promote the three `param_offset_rounded_slot_*` cases, while their authoritative
`case.json` lifecycle status remains `experimental`. The user selected this
bounded reconciliation before resuming M143.

## Goal

Align only the lifecycle and reference-script declaration metadata of the three
ADR-0023-promoted offset-rounded-slot cases with their documented active
library status, then validate registry/case metadata consistency.

## Scope

- Update only `case.json` metadata for `param_offset_rounded_slot_low`,
  `param_offset_rounded_slot_nominal`, and `param_offset_rounded_slot_high` to
  match ADR-0023's active lifecycle and recorded reference-script role.
- Add a deterministic metadata consistency audit and focused regression test.
- Re-run the existing M143 metadata-only inventory to prove the conflict is
  resolved without fixture access.

## Compatibility constraints

Do not read, hash, replay, or execute any STEP fixture. Do not alter split,
parameters, baselines, sequence data, candidate sequence, reference-script
contents, registry rows, case cards, manifests, Harness, runtime, provider,
training, or hosted behavior. The cases remain absent from manifests and all
runtime/provider paths.

## Acceptance

```powershell
uv run python -m pytest tests\test_m144_rounded_slot_metadata.py tests\test_admission_profile.py -q
uv run python tools\audit_m144_rounded_slot_metadata.py
uv run python tools\audit_admission_profile.py
uv run python -m ruff check tools\audit_m144_rounded_slot_metadata.py tools\audit_admission_profile.py tests\test_m144_rounded_slot_metadata.py tests\test_admission_profile.py
uv run python tools\check_governance.py
git diff --check
```

## Owner completion boundary

Publish the three corrected metadata records, audit/test evidence, and M143
inventory result; obtain Liaol's independent G2 review, then resume M143.

## Implementation evidence

- Corrected only the lifecycle, reference-script declaration, and stale
  admission-boundary metadata of the three ADR-0023-promoted rows.
- `tools/audit_m144_rounded_slot_metadata.py` reports both
  `fixture_access=not_performed` and `script_access=not_performed`.
- The previously blocked M143 profile audit now passes with 87 active rows and
  zero inventory conflicts, while retaining held-out access as
  metadata/documentary only.
- Focused tests passed (4); focused Ruff, governance audit, and
  `git diff --check` are pending the final status-directory transition.

## Closure

Liaol completed the independent G2 review and approved closure on 2026-08-12.
The reconciliation changed only the documented case metadata declarations;
fixture/script access, split, baseline, sequence, manifest, runtime, provider,
and hosted boundaries remain unchanged.

## Permitted stop conditions

Independent review; a conflict with ADR-0023 or authoritative lifecycle
evidence; need for fixture access, split/baseline/sequence change, manifest or
runtime/provider change, hosted authority, or reproducible validation blocker.

## Status transition

Update `docs/workflow/status.md` first, then this workpack and active handoff.
On closure, archive this workpack and resume M143; do not select TRG-028.

## Out of scope

Any B-Rep or reference-script inspection/execution, case production, corpus
expansion, runtime projection, provider use, training, or hosted execution.
