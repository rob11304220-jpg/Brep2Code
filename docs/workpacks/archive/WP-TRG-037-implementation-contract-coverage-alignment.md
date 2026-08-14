# WP-TRG-037: Implementation-Contract Coverage Alignment

- Status: deferred
- Owner: unassigned
- Reviewer: independent reviewer required
- Risk tier: G2

## Entry condition

`WP-TRG-036` is complete or explicitly accepted, the M146 crosswalk audit
passes, and the user selects this package.

## Goal

Produce a compact coverage view of which reviewed development-side hypotheses
already have complete Q01--Q04 implementation-contract representation, and
which still stop at `contract_only` or `unsupported`.

## Scope

- Add one source-linked implementation-contract coverage layer that reuses
  existing hypothesis IDs, implementation-contract mappings, and reviewed
  validation evidence.
- Distinguish exact completed chains from missing-link, `contract_only`, and
  `unsupported` states without reinterpreting evidence or broadening any
  hypothesis boundary.
- Publish the smallest derived navigation needed to show which later routes
  still require new contract work before they may discuss runtime projection or
  hosted evaluation.

## Compatibility constraints

This package may derive status from existing mappings and reviewed evidence,
but it cannot change case authority, runtime behavior, manifest selection,
provider policy, or hosted readiness. If a hypothesis lacks an exact chain,
record that gap rather than generalize.

## Acceptance

```powershell
uv run python -m pytest tests -q
uv run python -m ruff check .
python tools\audit_development_evidence_crosswalk.py
python tools\audit_case_evidence_relationships.py
uv run python tools\check_governance.py
git diff --check
```

## Out of scope

New case production, generic capability scoring, runtime projection, provider
use, and hosted execution.
