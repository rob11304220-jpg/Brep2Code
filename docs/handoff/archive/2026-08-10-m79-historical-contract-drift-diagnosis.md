# Handoff: M79 historical contract drift diagnosis

- **Date**: 2026-08-10
- **Subproject**: `brep2code`
- **Status**: `active`
- **Related workpack**: `WP-M79-001-historical-contract-drift-diagnosis`

## Goal

Complete an offline, privacy-preserving comparison of the earlier M51 box
success with the current/M72 request contract, then freeze a reviewed M80
reproduction profile without making a provider request.

## Done

- Liaol selected M79; `status.md` records it as the active G2 workpack.
- Wrote the initial evidence matrix and `reproduction-profile-v1` at
  `docs/workflow/m79-historical-contract-drift-diagnosis.md`.
- Confirmed M51's simple P0 `box` success, M72's P2 timeout, source-level
  single-case contract equivalence, and the intentionally unknown historic
  payload/response fields.

## In progress

- M79 awaits Liaol's independent review of the matrix, unknown-field handling,
  and frozen profile. No acceptance command has yet been run for this workpack.

## Next

- Review the M79 matrix against the committed source and retained workpack
  evidence; do not fill unknown historic fields from inference.
- Run the M79 acceptance checks, record output, and obtain Liaol's independent
  review before moving to M80 preflight.

## Decisions

- M80 must use P0 `box` through `observed-first-pass`, not M72's P2 case or
  `observed-development`; this is a minimal route regression, not a matched
  performance comparison.
- Retain M80's separate provider control because it distinguishes only a
  blanket endpoint/authentication failure. See
  [`ADR-0051`](../../architecture/adr/0051-historical-contract-diagnosis-before-p0-revalidation.md).

## Blockers

- Independent reviewer decision from Liaol is required for G2 closure.
- M80 remains unauthorized until M79 closure, a fresh G3 preflight, and
  itemized user authorization.

## Key paths

| Kind | Path |
|---|---|
| Branch | `main` |
| Workpack | `docs/workpacks/active/WP-M79-001-historical-contract-drift-diagnosis.md` |
| Diagnosis | `docs/workflow/m79-historical-contract-drift-diagnosis.md` |
| Later workpack | `docs/workpacks/backlog/WP-M80-001-minimal-p0-end-to-end-revalidation.md` |
| Commands | `uv run python -m pytest tests\\test_agent_m3_provider_trace.py tests\\test_observed_build_loop.py -q`; `uv run python -m ruff check .`; `uv run python tools\\check_governance.py`; `git diff --check` |

## Resume prompt

```
Continue Brep2Code M79 historical contract drift diagnosis.
Read docs/handoff/active/2026-08-10-m79-historical-contract-drift-diagnosis.md,
docs/workflow/status.md, docs/workpacks/active/WP-M79-001-historical-contract-drift-diagnosis.md,
and docs/workflow/m79-historical-contract-drift-diagnosis.md.
First action: independently review the evidence/unknown matrix, then run the
M79 offline acceptance checks. Do not make a provider request or activate M80.
```
