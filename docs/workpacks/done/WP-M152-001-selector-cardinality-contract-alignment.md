# WP-M152-001: Selector-Cardinality Contract Alignment

- Status: done
- Milestone: M152
- Trigger consumed: `WP-TRG-034`
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

## Entry condition

M150 is independently approved and the user selected TRG-034. The frozen
provenance inputs are:

- M146 `development-evidence-crosswalk-v1`, SHA-256
  `abcb68630f188feae4ddc4f757617aa33f227aa0fbdd3515e33f7811267cf128`;
- M150 `case-evidence-relationships-v1`, SHA-256
  `b0e7d31511a3ced8fca0dd40ab49e071f3d1a7b08483e26df0aea7ef8bad20f3`;
- relationship IDs `selector-cardinality-development-oracle`,
  `selector-cardinality-development-discriminating`, and
  `selector-cardinality-held-out-documentary-control`.

## Goal

Create the smallest source-linked implementation-contract mapping and focused
contract/test alignment for `hm-q01-selector-cardinality-v1`.

## Complete Q01--Q04 chain

| Stage | Frozen boundary |
|---|---|
| Q01 | `planar-face-selector-cardinality-v1`: declared planar +Z maximum-output-Z predicate; only cardinality one may bind. |
| Q02 | `face-selected-dependent-cut-v1`: the bound boss top is consumed before the dependent blind cut. |
| Q03 | Selector-cardinality audit plus post-step geometry/topology gate. |
| Q04 | `selector_ambiguous` is `stop_unsupported`, zero requests; coordinate tie-break and choose-first are forbidden. |

## Scope

- Locate the existing code/contracts/tests implementing the frozen selector
  fail-closed boundary; do not inspect fixtures, scripts, or held-out assets.
- Add a versioned implementation-contract mapping with status `implemented`,
  `contract_only`, or `unsupported`, linked to this exact Q01--Q04 chain and
  validation evidence.
- Make only the smallest required contract/documentation/test change. If the
  existing code cannot represent the exact chain without broadening it, record
  `contract_only` or `unsupported` and stop rather than generalize.
- Update derived navigation with the implementation-contract mapping only; do
  not change M146/M150 source relationships.

## Decision-package impact

- `decision_id`: `q01-selector-ambiguity-v1`.
- Q01/Q02 effect: preserve exact cardinality-one binding and frozen dependent
  action boundary; no generic face recovery.
- Q03/Q04 effect: preserve audit/gates and `selector_ambiguous → stop` route.
- Evidence role: existing oracle, discriminating, and documentary held-out
  provenance only; no new evidence asset.
- Knowledge disposition: no runtime, provider, manifest, or training adoption.

## Compatibility constraints

Fail closed outside the exact frozen hypothesis. No persistent entity naming,
coordinate-only tie-break, generic selector helper, case/lifecycle/split or
manifest change, runtime projection, provider use, or hosted execution.

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

Publish the implementation-contract mapping, focused implementation/contract
and test evidence (or an explicit `contract_only`/`unsupported` disposition),
then obtain Liaol's independent G2 review.

## Permitted stop conditions

Independent review; missing exact Q01--Q04 contract; required fixture/held-out
access; or a required manifest, runtime, provider, hosted, or generic-helper
change.

## Status transition

Update status first, then workpack and handoff. On closure, archive M152; do
not activate TRG-035 or TRG-028.

## Current result

- Published
  `docs/corpus/knowledge/implementation-contract-relationships-v1.{json,md}`
  as the source-linked implementation-contract mapping for
  `hm-q01-selector-cardinality-v1`.
- Recorded the hypothesis as `contract_only`, not `implemented`: the exact
  fail-closed Q01--Q04 chain is represented across reviewed knowledge,
  family-scoped sequence/audit evidence, and the coded/tested classified
  repair-policy stop route, but the project does not yet implement a reusable
  Harness/runtime selector contract for this hypothesis.
- Updated derived navigation in
  `docs/corpus/knowledge/development-evidence-crosswalk-v1.md` and
  `docs/corpus/knowledge/README.md` without changing M146/M150 source
  relationships.
- Added `tests/test_m152_implementation_contract_mapping.py` as focused
  regression coverage for the new mapping and the fail-closed Q04 route.

## Closure rationale

Owner-side scope is complete pending independent review. Focused validation
passed with:

```powershell
uv run python -m pytest tests\test_m152_implementation_contract_mapping.py tests\test_m141_classified_repair_policy.py tests\test_m29_selector_ambiguity.py tests\test_sequence_paired_face_selected_dependent_cut.py -q
uv run python -m ruff check docs/corpus/knowledge tests/test_m152_implementation_contract_mapping.py
python tools\audit_development_evidence_crosswalk.py
python tools\audit_case_evidence_relationships.py
uv run python tools\check_governance.py
git diff --check
```

`git diff --check` reported only existing LF/CRLF warnings. No runtime,
manifest, provider, or hosted authority changed.

## Independent review

- Liaol approved the independent G2 review on 2026-08-13.
- Review result: approved. The `contract_only` disposition, source-linked
  Q01--Q04 mapping, focused regression set, relationship boundaries, and
  unchanged authority surface were accepted without requesting any capability
  widening.

## Final closure rationale

M152 closes because the smallest source-linked implementation-contract mapping
for `hm-q01-selector-cardinality-v1` is published, its bounded
`contract_only` disposition is independently approved, and all required focused
validation/audits passed. No selector generalization, runtime projection,
manifest change, provider use, or hosted authority was introduced.

## Out of scope

Any second hypothesis, generic feature/history recovery, helper/IR/SDK/runtime
card, case production, manifest change, provider use, training, or hosted work.
