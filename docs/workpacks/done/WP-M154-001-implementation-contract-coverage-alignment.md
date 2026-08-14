# WP-M154-001: Implementation-Contract Coverage Alignment

- Status: done
- Milestone: M154
- Trigger consumed: `WP-TRG-037`
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

## Entry condition

M153 is complete, the M146 crosswalk audit passes, and the user selected
TRG-037.

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

## Decision-package impact

- `decision_id`: none; M154 derives a coverage view from existing reviewed
  mappings and evidence only.
- Q01/Q02 and Q03/Q04 effects: none.
- Evidence role: navigation and maintenance-only coverage status.
- Knowledge disposition: no runtime, provider, manifest, or hosted authority
  change.

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

## Owner completion boundary

Publish the implementation-contract coverage layer, its compact navigation,
validation evidence, and obtain Liaol's independent G2 review.

## Current result

- Added
  `docs/corpus/knowledge/implementation-contract-coverage-v1.{json,md}` as a
  source-linked development-side coverage layer over all five reviewed M146
  hypotheses.
- Recorded `hm-q01-selector-cardinality-v1` as `contract_only` with a complete
  represented Q01--Q04 chain linked to the published M152 mapping.
- Recorded the remaining four reviewed hypotheses as `missing_link`, making
  explicit that reviewed crosswalk evidence exists but no published
  implementation-contract mapping currently states an exact chain for them.
- Updated
  `docs/corpus/knowledge/development-evidence-crosswalk-v1.md` and
  `docs/corpus/knowledge/README.md` so readers can find the compact coverage
  view without treating it as runtime or hosted authority.
- Added `tests/test_m154_implementation_contract_coverage.py` as focused
  regression coverage for the new artifact.

## Validation record

Focused validation passed on 2026-08-13 with:

```powershell
uv run python -m pytest tests\test_m154_implementation_contract_coverage.py tests\test_m152_implementation_contract_mapping.py -q
uv run python -m ruff check docs/corpus/knowledge tests/test_m154_implementation_contract_coverage.py tests/test_m152_implementation_contract_mapping.py
python tools\audit_development_evidence_crosswalk.py
python tools\audit_case_evidence_relationships.py
uv run python tools\check_governance.py
git diff --check
```

`git diff --check` reported only existing LF/CRLF warnings.

## Independent review

- Liaol approved the independent G2 review on 2026-08-13.
- Review result: approved. The compact coverage layer, `missing_link`
  interpretation, focused regression set, unchanged authority boundary, and
  deferred-successor semantics were accepted without requesting any capability
  widening.

## Closure rationale

M154 closes because the implementation-contract coverage layer, compact
navigation, focused regression coverage, and validation record are complete and
independently approved. The work makes implementation-contract coverage status
explicit for all five reviewed hypotheses without changing any case,
manifest, runtime, provider, or hosted authority.

## Permitted stop conditions

Independent review; missing exact source-linked implementation-contract
provenance; required fixture/held-out access; or a required manifest, runtime,
provider, hosted, or hypothesis-generalization change.

## Status transition

Update `docs/workflow/status.md` first, then this workpack and active handoff.
On closure, archive M154 and do not activate TRG-038, TRG-028, or TRG-035
automatically.

## Out of scope

New case production, new implementation-contract mapping content, generic
capability scoring, runtime projection, provider use, and hosted execution.
