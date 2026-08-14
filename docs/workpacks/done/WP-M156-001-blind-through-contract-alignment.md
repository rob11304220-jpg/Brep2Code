# WP-M156-001: Blind-Through Contract Alignment

- Status: done
- Milestone: M156
- Trigger consumed: user-selected governed-case governance / implementation-contract gap
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

## Entry condition

The user selected the first step in the maintained post-M155 planning order.
M154 records `hm-q01-blind-through-observability-v1` as `missing_link`; M146
and M150 already identify its reviewed observable, operation, evidence roles,
and governed development cases.

## Goal

Publish the smallest source-linked implementation-contract mapping for the
reviewed blind/through observable and its frozen prismatic-hole operation,
without turning it into a runtime or generic feature-recognition claim.

## Scope

- Map `hm-q01-blind-through-observability-v1` to
  `blind-through-cylindrical-extent-v1` (Q01) and `prismatic-hole-v1` (Q02).
- Reuse only the source-linked development relationship and its stated
  documentary/held-out boundary; do not inspect or copy held-out asset detail.
- Record the existing offline audit and regression evidence, and retain an
  explicit fail-closed non-projection disposition for anything outside the
  frozen +Z single-cylinder scope.
- Refresh the derived coverage view and reader navigation; add focused
  regression coverage for the new mapping.

## Decision-package impact

- `hypothesis_id`: `hm-q01-blind-through-observability-v1`.
- `decision_id`: `q01-blind-through-observability-v1`.
- Q01/Q02 effect: only the reviewed cylindrical-extent observable and frozen
  prismatic-hole sequence are represented.
- Evidence role: development oracle/regression provenance plus the existing
  negative-control boundary; no new evidence asset or case lifecycle change.
- Counterexample and stop rule: other counts, axes, terminal-face cardinality,
  footprint combinations, and counterbore conditions remain unsupported and
  fail closed.
- Adoption boundary: development-side navigation only; no runtime, manifest,
  provider, training, IR, SDK, retrieval, or hosted authority.

## Compatibility constraints

No case, split, registry, admission record, manifest, Harness, runtime card,
reference pack, provider, or hosted change. Do not claim generic cylindrical
feature recognition, history recovery, or a reusable runtime observation
helper. Do not expand Q03/Q04 into an implemented repair path.

## Acceptance

```powershell
uv run python -m pytest tests\test_m156_blind_through_contract_mapping.py tests\test_m154_implementation_contract_coverage.py tests\test_m30_blind_through_observability.py -q
uv run python -m ruff check docs/corpus/knowledge tests/test_m156_blind_through_contract_mapping.py
python tools\audit_development_evidence_crosswalk.py
python tools\audit_case_evidence_relationships.py
uv run python tools\check_governance.py
git diff --check
```

## Owner completion boundary

Publish the bounded mapping and derived coverage/navigation updates with
focused validation evidence, then obtain Liaol's independent G2 review.

## Current result

- Published `blind-through-observability-contract-alignment-v1` in
  `implementation-contract-relationships-v1.json`, linked to the existing
  observable, operation, development, held-out-documentary, and negative-control
  relationship boundaries.
- Refreshed the M154 coverage view from `missing_link` to `contract_only` for
  the hypothesis's declared Q01/Q02 stages only. Q03/Q04 remain undeclared and
  no repair route or runtime implementation is claimed.
- Updated reader-facing mapping and crosswalk navigation, and added focused
  mapping regression coverage.

## Owner validation

The following owner-side checks passed on 2026-08-13:

```powershell
uv run python -m pytest tests\test_m156_blind_through_contract_mapping.py tests\test_m154_implementation_contract_coverage.py tests\test_m30_blind_through_observability.py -q
# 14 passed in 2.16s
uv run python -m ruff check docs/corpus/knowledge tests/test_m156_blind_through_contract_mapping.py
python tools\audit_development_evidence_crosswalk.py
python tools\audit_case_evidence_relationships.py
uv run python tools\check_governance.py
git diff --check
```

`git diff --check` reported only existing LF/CRLF conversion warnings. No
case, manifest, Harness, runtime, provider, or hosted authority changed.

## Independent review

Pending Liaol's independent G2 review of the declared-stage-only
`contract_only` disposition, relationship boundaries, validation evidence, and
status/handoff alignment.

Liaol approved the independent G2 review on 2026-08-13. The declared-stage
boundary, source-linked relationship IDs, `contract_only` disposition,
validation evidence, and non-projection constraints were accepted without any
runtime, provider, or hosted capability widening.

## Closure rationale

M156 closes because the smallest source-linked implementation-contract mapping
for the reviewed blind/through Q01/Q02 hypothesis is published, coverage and
navigation are aligned, the focused validation set passed, and Liaol completed
the independent G2 review. The mapping remains development-side
`contract_only`; it establishes neither a reusable runtime observation
contract nor Q03/Q04 repair capability.

## Permitted stop conditions

Independent review; missing exact source-linked Q01/Q02 contract; required
held-out fixture access; or any required case, manifest, Harness, runtime,
provider, hosted, or generic-helper change.

## Status transition

Update `status.md` first. On approved closure, move this workpack and its
handoff to archive; do not activate `WP-TRG-028`, the case-testing dossier, or
`WP-TRG-035`.

## Out of scope

Any additional hypothesis, code/Harness change, case production, split or
manifest change, runtime projection, provider use, training, or hosted work.
