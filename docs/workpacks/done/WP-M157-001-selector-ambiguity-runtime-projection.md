# WP-M157-001: Selector-Ambiguity Runtime Projection

- Status: done
- Milestone: M157
- Trigger consumed: `WP-TRG-028`
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

## Entry condition

The user selected `WP-TRG-028`. This package reuses the M155 entry boundary,
M153 maintained authority map, M146 hypothesis
`hm-q01-selector-cardinality-v1`, M150 relationship IDs
`selector-cardinality-development-oracle`,
`selector-cardinality-development-discriminating`, and
`selector-cardinality-held-out-documentary-control`, M152's reviewed
`contract_only` mapping, M154 coverage state, M142 immutable admission record,
and M143 reviewed admission-profile crosswalk.

The source record and projection candidate must be hash-bound inside this
package. No authority is inherited for provider or hosted use.

## Goal

Decide, derive, and offline-evaluate the smallest safe runtime projection from
the reviewed selector-ambiguity admission record for one bounded diagnosis.

## Frozen selection

The selected form is one experimental counterexample experience card, not a
human case card, development reference pack, SDK/tool schema, IR/sequence
record, retrieval index, or general runtime card promotion. It may state only:
when a declared selector-cardinality observation is not exactly one, do not
bind a target or attempt the dependent action; stop fail closed.

This form is selected because it can carry the M142 failure boundary without
copying scripts, raw STEP, paths, parameters, held-out answers, or directory
retrieval. It remains absent by default and cannot alter Harness behavior.

## Scope

- Add the hash-bound experimental counterexample card and index entry with
  source-record linkage, applicability/prohibition conditions, counterexample,
  review trigger, and source/projection hashes.
- Publish a compact comparison record explaining why case cards, reference
  packs, SDK/tool schemas, IR/sequence records, and retrieval indexes are not
  selected for this bounded diagnostic.
- Implement a fixed development-only no-reference, wrong-reference, and
  explicit-reference offline ablation using the existing GuidanceBundle bridge.
  The fixed set consists only of M142's unique oracle and development
  discriminating case identities; no held-out asset is read or executed.
- Add focused audit and regression coverage. The ablation budget is three
  deterministic bridge calls, one per arm, with zero provider requests.

## Decision-package impact

- `decision_id`: `q01-selector-ambiguity-v1`.
- Q01 effect: `cardinality != 1` is a bounded diagnostic stop condition.
- Q02/Q03/Q04 effect: no dependent action, gate change, repair route, or
  capability claim is added; the existing `selector_ambiguous -> stop` policy
  remains authoritative.
- Evidence role: M142 development oracle/discriminating evidence plus the
  held-out-documentary boundary only.
- Adoption boundary: one static experimental card, absent by default; no
  retrieval, provider, hosted, manifest, training, SDK, IR, or helper adoption.

## Compatibility constraints

Admission records remain immutable evidence sources. Do not modify cases,
splits, registry, manifest, Harness tool schema, repair policy, provider
configuration, or hosted routes. Do not inspect or execute held-out assets.
The card must not contain scripts, raw STEP, local paths, case parameters,
held-out answers, broad repository text, or unrestricted retrieval behavior.

## Acceptance

```powershell
uv run python -m pytest tests\test_m157_selector_ambiguity_runtime_projection.py tests\test_guidance_bridge.py tests\test_m152_implementation_contract_mapping.py -q
uv run python tools\evaluate_m157_selector_ambiguity_projection.py
uv run python -m ruff check runtime_resources tests\test_m157_selector_ambiguity_runtime_projection.py tools\evaluate_m157_selector_ambiguity_projection.py tools\audit_runtime_guidance.py
uv run python tools\audit_runtime_guidance.py
python tools\audit_admission_record.py
python tools\audit_admission_profile.py
uv run python tools\check_governance.py
git diff --check
```

## Owner completion boundary

Publish the selected card, comparison/provenance record, fixed offline
ablation, and focused validation evidence; then obtain Liaol's independent G2
review.

## Permitted stop conditions

Independent review; source/projection hash drift; a required held-out access,
case/manifest/Harness/repair change, retrieval/index search, provider or hosted
request; or a reproducible local validation blocker.

## Blocked state

M157 stopped before creating a card or ablation artifact. The existing
`GuidanceCardBridge._dispatch` accepts only the hard-coded
`vertical-cylinder-construction` card ID and its current role set. As a result,
the selected selector-ambiguity card cannot be supplied to the explicit-
reference arm, while a no-reference or substituted vertical-cylinder call
would not evaluate the selected projection.

Changing this behavior requires a separately selected bounded Harness
guidance-selection workpack: it must define a declarative, hash-bound selected
card identity and role compatibility without enabling directory search or
retrieval. That is a Harness behavior change, explicitly outside M157 scope.
The required workpack must independently review the interface and then M157
may resume with fresh source/projection hashes and the already frozen three-call
development-only ablation budget.

## Resumed state

M158 is independently approved and supplies the explicit hash-bound
single-card selection required for the explicit-reference arm. M157 resumes
with the same one-card, three-call, development-only ablation budget; no
held-out asset, provider, hosted, retrieval, or Harness tool-schema scope is
added.

## Owner completion evidence

- Added `selector-cardinality-stop` as an experimental, absent-by-default
  counterexample card and added it to the runtime card index.
- Published `docs/corpus/knowledge/runtime-projections/selector-cardinality-stop-v1.json`.
  It hash-binds the M142 admission record, selected card, and index, and records
  why human case cards, reference packs, SDK/tool schemas, IR/sequence records,
  and retrieval indexes were rejected.
- The fixed three-call evaluator returned: no reference -> `guidance_not_enabled`;
  wrong explicit reference -> `vertical-cylinder-construction`; explicit selected
  reference -> `selector-cardinality-stop`. It reads no case asset, makes zero
  provider requests, and reports held-out access as `not_performed`.
- Passed 2026-08-13: focused pytest (`14 passed`), Ruff, runtime-guidance audit
  (`5 cards`), admission-record audit, admission-profile audit, governance audit,
  and `git diff --check` (line-ending warnings only).

## Review state

Liaol independently approved the card, comparison record, evaluator, and
boundary evidence on 2026-08-13. M157 is closed; no new workpack is activated
by this approval.

## Status transition

Update `status.md` first, then this workpack and active handoff. On closure,
archive M157 and do not activate the case-testing dossier or `WP-TRG-035`.

## Out of scope

Provider calls, hosted execution, training, card retrieval or default mounting,
case-library ingestion, generic selector recovery, SDK/IR work, manifest or
Harness changes, and all held-out asset access.
