# WP-M160-001: Rounded-Slot Audit Deregistration Alignment

- Status: done
- Milestone: M160
- Trigger consumed: M158 second re-entry blocker
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

## Entry condition

M159 independently approved the deregistration of the three experimental
offset-rounded-slot rows. The full suite then showed that
`assert_m21_sequence_pairs` still treats every historical M21 expansion entry
as active registry membership.

## Goal

Align the M21 case-library metadata audit with current lifecycle authority:
the three promoted rounded-slot rows remain active; the three experimental
offset-rounded-slot rows remain valid historical expansion evidence but must
be absent from the active registry.

## Scope

- Change only M21 audit/test expectations in `tools/audit_case_library.py` and
  its focused tests to distinguish active registry evidence from historical
  experimental expansion entries.
- Add a fail-closed check that rejects an active registry row whose metadata is
  experimental, while accepting the exact three M159-deregistered historical
  entries as non-active evidence.
- Update the M21/M159 reader-facing contract wording and record the durable
  audit interpretation in an ADR.

## Compatibility constraints

Do not modify registry rows, any `case.json`, fixtures, scripts, splits,
sequences, manifests, Harness, runtime resources, provider configuration,
repair policy, or hosted routes. Do not read or execute fixtures/scripts.
This package changes metadata-audit interpretation only.

## Acceptance

```powershell
uv run python -m pytest tests\test_case_library_m12.py tests\test_m159_offset_rounded_slot_deregistration.py tests\test_admission_profile.py -q
uv run python tools\audit_case_library.py
uv run python tools\audit_m159_offset_rounded_slot_deregistration.py
uv run python -m pytest -q
uv run python -m ruff check tools\audit_case_library.py tests\test_case_library_m12.py
uv run python tools\check_governance.py
git diff --check
```

## Owner completion boundary

Publish the narrow M21 audit alignment, regression evidence, ADR, and full
suite terminal result; then obtain Liaol's independent G2 review. M158 remains
blocked until that review approves M160.

## Current result

- Updated the M21 audit to distinguish its three active development entries
  (`case_record`) from the three retained experimental entries
  (`candidate_directory`).
- The audit now requires active rounded-slot membership to match only the three
  active entries and fails closed if any M159-deregistered experimental entry
  appears in the active registry.
- Added regression coverage, ADR-0077, and a current-state note on the M21
  review without changing registry, case metadata, assets, or runtime scope.

## Owner validation

The following checks passed on 2026-08-13:

```powershell
uv run python -m pytest tests\test_case_library_m12.py tests\test_m159_offset_rounded_slot_deregistration.py tests\test_admission_profile.py -q
# 10 passed in 1.06s
uv run python tools\audit_case_library.py
# case-library audit passed: 84 records, 18 M12 parameter cases
uv run python tools\audit_m159_offset_rounded_slot_deregistration.py
uv run python -m pytest -q
# 284 passed in 502.06s
uv run python -m ruff check tools\audit_case_library.py tests\test_case_library_m12.py
uv run python tools\check_governance.py
git diff --check
```

The M159 audit reported `fixture_access=not_performed` and
`script_access=not_performed`. `git diff --check` reported only LF/CRLF
conversion warnings.

## Independent review

Pending Liaol's independent G2 review of the active-versus-experimental M21
audit interpretation, the exact three-row fail-closed deregistration check,
ADR-0077, and full-suite evidence.

Liaol approved the independent G2 review on 2026-08-13. The active-versus-
experimental M21 interpretation, exact three-row fail-closed check, ADR-0077,
and 284-test full-suite evidence were accepted without lifecycle, asset,
runtime, provider, or hosted scope widening.

## Closure rationale

M160 closes because the current audit correctly distinguishes active registry
evidence from retained experimental history, all focused and full validation
passed, and Liaol independently approved the bounded audit interpretation.

## Permitted stop conditions

Independent review; any required case/registry/fixture/script/manifest/Harness
or provider/hosted change; an attempt to generalize to other experimental
families; or a reproducible validation blocker.

## Status transition

Update `status.md` first, then this workpack and active handoff. On approved
closure, archive M160 and resume M158; do not resume M157 automatically.

## Out of scope

Lifecycle changes, asset access, family promotion, manifest changes, runtime
projection, retrieval, provider use, training, or hosted execution.
