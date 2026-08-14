# WP-M91-002: M90 Case-Metadata Lifecycle Alignment

- Status: done
- Milestone: M91
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

## Goal

Align the lifecycle boundary in the six active M90 repeated-feature-pattern
case records with ADR-0055 and the authoritative self-authored registry.

## Scope

- Change only the `admission_boundary` field in the six promoted M90
  `case.json` records from experimental/unregistered wording to active
  governance wording.
- State explicitly that the records remain absent from executable manifests,
  provider inputs, training and runtime resources.

## Compatibility constraints

Do not change geometry, input hashes, numerical baselines, reference scripts,
candidate sequences, registry pointers, manifests, Harness behavior, provider
configuration, hosted authorization, training, or runtime resources.

## Acceptance

```powershell
uv run python tools\audit_case_library.py --replay
uv run python tools\audit_sequence_paired_repeated_feature_pattern.py
uv run python tools\check_governance.py
git diff --check
```

## Status transition

After owner acceptance, Liaol independently verifies the six-file scope,
unchanged hashes/geometry/manifests, audit outputs and boundary wording. Only
then update `status.md`, move this workpack to `done/`, and archive its
handoff.

## Out of scope

Any new case, split move, manifest admission, provider or hosted request,
runtime projection, training input, generic pattern claim, or ADR change.

## Owner acceptance

- Updated only the `admission_boundary` field in the six M90 case records.
  Each now records active self-authored governance status under ADR-0055 while
  preserving exclusion from executable manifests, provider inputs, training,
  and runtime resources.
- Owner validation on 2026-08-10 passed:
  `audit_sequence_paired_repeated_feature_pattern.py` (6 records),
  `audit_case_library.py --replay`, `check_governance.py`, `git diff --check`,
  and a six-record JSON/boundary equality check.

## Independent review required

Liaol must independently confirm that only the six declared lifecycle fields
changed; the registry remains active, and geometry, hashes, scripts, candidate
sequences, manifests, provider/runtime boundaries, and split membership are
unchanged. This review cannot authorize any hosted request.

## Independent review and closure

- Reviewer: Liaol
- Outcome: approved on 2026-08-10.
- Review scope: confirmed that the diff changes only the six declared
  `admission_boundary` fields; the active registry, geometry, hashes, scripts,
  candidate sequences, manifests, split membership, and provider/runtime
  exclusions remain unchanged.
- Closure rationale: the M90 lifecycle statements now agree with ADR-0055 and
  the authoritative registry without expanding any executable or hosted
  boundary.
