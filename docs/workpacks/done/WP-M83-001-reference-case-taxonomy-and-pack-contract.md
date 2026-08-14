# WP-M83-001: Reference-Case Taxonomy and Candidate-Pack Contract

- Status: done
- Milestone: M83
- Owner: Codex
- Reviewer: Liaol
- Risk tier: G2

## Goal

Freeze a small P0/P1 development-only reference selection and a versioned,
machine-auditable candidate reference-pack contract. The packs describe bounded
OCP construction patterns without exposing raw STEP, full reference scripts,
development governance documents, or held-out authoring evidence.

## Scope

- Classify `box`, `cylinder`, `block_with_hole`, `filleted_block`,
  `chamfered_block`, `three_hole_plate`, and `box_cylinder_union` by mechanism,
  difficulty, evidence role, known counterexample, and OCP API surface.
- Define a compact pack schema: ID/version/hash, applicability observations,
  allowed OCP modules, parameter placeholders, bounded sequence outline,
  output requirement, counterexamples, and source links.
- Freeze development versus held-out membership and audit deterministic source
  links and no-full-script/no-raw-STEP boundary.

## Inputs

- `case-library/manifests/self-authored/p0.json` and `p1.json` define the
  frozen seven-case development selection.
- Per-case `case.json` records and their referenced build scripts are local
  source authorities only; neither is pack content nor runtime material.
- ADR-0016 supplies the evidence gate that keeps M19-002 backlog until M84
  independently establishes three direct development cases for one mechanism.

## Code paths

- `docs/corpus/reference-packs/`
- `tools/audit_reference_packs.py`
- `tests/test_reference_packs.py`

## Docs to update

- `docs/corpus/README.md`
- `docs/workflow/status.md`
- active handoff

## Trace/schema changes

Add a development-only candidate-pack JSON schema and audit artifacts under
`docs/corpus/reference-packs/`. Do not modify `signal_bundle.json`, provider
or tool traces, corpus/executable manifests, storage layout, or CLI output.

## Decision-package impact

- `decision_id`: none; this is an asset-to-candidate-pack curation contract.
- Evidence role: development regression/oracle metadata only.
- Knowledge disposition: candidate runtime material remains experimental; no
  runtime retrieval, helper, IR, or general B-Rep recovery claim.

## Attribution question and sampling intent

Distinguish whether a compact OCP-construction summary can be stated and
audited without leaking source assets or overstating applicability. The fixed
sample is exactly the three P0 and four P1 cases named in Scope, with one
declared mechanism and counterexample per case. Stop after the deterministic
schema/source-boundary audit; no case expansion, retrieval test, or hosted
comparison is permitted in this workpack.

## Compatibility constraints

Offline only. Do not change executable manifests, provider requests, prompts,
  sandbox mounts, runtime resources, gates, or reference-script visibility.

## Acceptance

- The selected cases, split, pack schema, source hashes, counterexamples, and
  OCP API summary are deterministic and locally audited.
- Existing case-library and runtime-guidance audits pass, plus Ruff, governance
  audit, and `git diff --check`.

```powershell
uv run python tools\audit_case_library.py
uv run python tools\audit_runtime_guidance.py
uv run python tools\audit_reference_packs.py
uv run python -m pytest tests\test_reference_packs.py -q
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

## Evidence reuse / guidance-card disposition

No reusable runtime evidence: the output is an experimental, development-only
candidate-pack contract. M84 must separately determine whether any mechanism
has three independent direct cases; M83 creates no experience card and does
not unlock M19-002.

## Status transition

On closure, record the audit artifacts and independent review, update
`docs/workflow/status.md` first, move this workpack to `done/`, and archive
the active handoff. No ADR is planned unless this work changes the durable
architecture rather than implementing the already selected ADR-0016 boundary.

## Owner acceptance record

- Added `reference-pack-contract-v1.json`: exactly the frozen three P0 and
  four P1 cases, each with a versioned ID/content hash, source case record and
  input hash, declared OCP modules, parameter placeholders, bounded sequence
  outline, output requirement, and counterexample.
- Added a fail-closed audit and regression tests. They require exact split
  membership and source-hash agreement, reject non-OCP modules and forbid raw
  input STEP, complete reference-script, and runtime-resource references.
- 2026-08-10 owner checks passed: reference-pack audit; 2 focused tests;
  full Ruff; case-library and runtime-guidance audits; governance audit; and
  `git diff --check`.
- Pending independent G2 review by Liaol: verify that the summaries do not
  reproduce source scripts, the stated counterexamples bound applicability,
  and no runtime/retrieval or M19-002 claim has been introduced.

## Independent review and closure

- Reviewer: Liaol
- Outcome: approved on 2026-08-10.
- Closure rationale: The fixed seven-case taxonomy and candidate-pack contract
  are locally auditable, hash-bound, development-only, and fail closed on the
  prohibited source/runtime references. The work does not expose reference
  assets, make a retrieval/model-quality claim, or activate M19-002; M84
  remains a separately selected independent-evidence gate.

## Out of scope

Runtime mounting/injection, retrieval implementation, hosted evaluation,
prompt changes, manifest changes, or deriving a general CAD SDK.

## Repair hypothesis and evaluation boundary

This is not a repair experiment. It is offline and development-only. It may
make no model-quality, reconstruction, or general CAD-API claim; any hosted
or held-out evaluation requires a separately selected workpack and, where
applicable, fresh explicit authorization.
