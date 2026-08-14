# WP-M90-002: Repeated-Feature Pattern Controlled Production

- Status: done
- Milestone: M90
- Owner: unassigned
- Reviewer: Liaol (independent)
- Risk tier: G2

## Goal

Produce only the six rows frozen by M90-001 twice in clean directories, then
audit deterministic geometry, sequence, editability and pattern invariants.

## Activation condition

M90-001 must pass intake audit and independent review; its record cannot change.

## Scope

Create the deterministic producer and family audit; retain candidates as
`experimental` and retain rejections without substitution.

## Compatibility constraints

Offline only. No executable manifest, provider, runtime, training or external-data change.

## Acceptance

Run the M90 audit, `uv run python tools/audit_case_library.py --replay`, focused
tests, Ruff, governance audit and `git diff --check`.

## Evidence reuse / guidance-card disposition

Experimental direct-case evidence only; no runtime experience card.

## Result and independent review

- 2026-08-10: all six frozen rows were built twice in clean directories with
  matching normalized STEP hashes.
- The family audit passed geometry replay, exact four-operation sequence,
  five mutations, four-instance through-cut/single-solid semantics and the
  three-development/three-held-out split; focused pytest passed.
- Reviewer Liaol approved this G2 production evidence on 2026-08-10. The
  approved result is the six fixed candidates only; no row was substituted.

## Status transition

After independent review, move to `done`; M90-003 stays backlog until selected.

## Out of scope

Changing preregistration, adding rows, promotion, manifests, provider use or hosted evaluation.
