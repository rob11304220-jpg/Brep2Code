# WP-M159-001: Offset Rounded-Slot Lifecycle Deregistration

- Status: done
- Milestone: M159
- Trigger consumed: M158 lifecycle-reconciliation blocker
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

## Entry condition

The user selected reconciliation of the three active-registry rows whose
authoritative `case.json` records are already changed to `experimental` with
unavailable reference scripts. The frozen cases are
`param_offset_rounded_slot_low`, `param_offset_rounded_slot_nominal`, and
`param_offset_rounded_slot_high`.

## Goal

Restore lifecycle consistency by treating the per-case metadata as
authoritative and removing only the three downgraded rows from the active
self-authored registry.

## Scope

- Remove the three specified rows from `docs/corpus/registry/self-authored.json`.
- Refresh the admission-profile registry source hash and its metadata-only
  inventory expectation from 87 to 84 active rows.
- Replace the now-obsolete current-state M144 audit assertion with an M159
  metadata-only deregistration audit that verifies the rows are absent from the
  active registry and remain experimental/unavailable in case metadata.
- Publish an ADR recording that M159 supersedes M144's active-promotion
  conclusion for these three rows only; update navigation with the re-entry
  relationship to M158/M157.

## Compatibility constraints

Do not modify the three `case.json` files, fixtures, scripts, hashes, splits,
parameters, sequence data, case cards, manifests, Harness, runtime resources,
provider configuration, repair policy, or hosted routes. The audit must read
only registry and case JSON metadata and report no fixture/script access.

## Acceptance

```powershell
uv run python -m pytest tests\test_m159_offset_rounded_slot_deregistration.py tests\test_admission_profile.py -q
uv run python tools\audit_m159_offset_rounded_slot_deregistration.py
uv run python tools\audit_admission_profile.py
uv run python -m ruff check tools\audit_m159_offset_rounded_slot_deregistration.py tests\test_m159_offset_rounded_slot_deregistration.py tests\test_admission_profile.py
uv run python tools\check_governance.py
git diff --check
```

## Owner completion boundary

Publish the registry de-registration, refreshed profile provenance, M159 audit,
ADR, and focused validation evidence; then obtain Liaol's independent G2
review. M158 and M157 remain blocked until that review completes.

## Current result

- Removed only the three downgraded offset-rounded-slot rows from the active
  self-authored registry. The user-provided `case.json` changes remain intact
  and were not edited by M159.
- Refreshed the admission-profile registry hash and active-row expectation to
  84, restoring zero inventory conflicts.
- Added the metadata-only M159 deregistration audit and ADR-0076; M144 is now
  marked as historical for these rows rather than as current lifecycle state.

## Owner validation

The following checks passed on 2026-08-13:

```powershell
uv run python -m pytest tests\test_m159_offset_rounded_slot_deregistration.py tests\test_admission_profile.py -q
# 4 passed in 0.31s
uv run python tools\audit_m159_offset_rounded_slot_deregistration.py
uv run python tools\audit_admission_profile.py
uv run python -m ruff check tools\audit_m159_offset_rounded_slot_deregistration.py tests\test_m159_offset_rounded_slot_deregistration.py tests\test_admission_profile.py
uv run python tools\check_governance.py
git diff --check
```

Both metadata-only audits reported `fixture_access=not_performed`; the M159
audit also reported `script_access=not_performed`. `git diff --check` reported
only LF/CRLF conversion warnings.

## Independent review

Pending Liaol's independent G2 review of the case-metadata authority decision,
three-row registry de-registration, profile provenance refresh, and unchanged
asset/runtime/provider boundaries.

Liaol approved the independent G2 review on 2026-08-13. The case-metadata
authority decision, three-row de-registration, 84-row profile provenance, and
unchanged asset/runtime/provider boundaries were accepted without requesting
lifecycle re-promotion or scope widening.

## Closure rationale

M159 closes because the active registry now matches the authoritative
experimental case metadata, focused validation and metadata-only audits pass,
and Liaol independently approved the bounded deregistration. The result
neither promotes nor changes any asset, manifest, Harness, runtime, provider,
or hosted surface.

## Permitted stop conditions

Independent review; a conflict with case metadata authority; any need to read
fixtures/scripts or change case metadata, split, manifest, Harness, runtime,
provider, hosted, retrieval, SDK, IR, or repair behavior; or a reproducible
local validation blocker.

## Status transition

Update `status.md` first, then this workpack and active handoff. On approved
closure, archive M159 and resume M158; do not activate M157, case testing, or
`WP-TRG-035` automatically.

## Out of scope

Lifecycle re-promotion, reference-script restoration, fixture/script access,
case production, manifest changes, runtime projection, provider use, training,
or hosted execution.
