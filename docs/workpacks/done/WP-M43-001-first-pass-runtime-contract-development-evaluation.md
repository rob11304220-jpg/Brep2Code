# WP-M43-001: First-Pass Runtime-Contract Development Evaluation

- Status: done
- Milestone: M43
- Owner: Codex
- Reviewer: Liaol (user)
- Risk tier: G3

## Goal

Evaluate whether the M42 bounded first-pass runtime contract improves
execution readiness on the frozen M10-007 development split, without making a
model-quality or held-out claim.

## Scope

- Add only the M42 runtime facts to the first-pass instruction: `/input/model.step`,
  `output/model.step`, installed `OCP` imports, and JSON full-script response.
- Complete the required read-only preflight and retain only sanitized evidence.
- Run `abc_v00_00000027` and `abc_v00_00000030` with DeepSeek V4-Pro through
  `wsl-bwrap`, at most one repair round per case, a 120-second request deadline,
  and a four-request maximum.
- Review the development evidence before proposing any held-out request.

## Attribution question and sampling intent

The fixed M10-007 development pair separates the direct sandbox host-path
failure from the non-matching unavailable-import failure.  The information
gain is whether the bounded contract moves first-pass outcomes from pre-output
failure to executable/readable output under unchanged gates.  Stop after these
two cases; do not expand the sample or alter the policy from their outcome.

## Inputs

- `docs/corpus/external/abc-v00-m10-007-development-manifest.json`
- `docs/corpus/external/abc-v00-m10-007-selection.json`
- `docs/architecture/v1/m10-012-minimal-offline-path-repair-review.md`
- `docs/corpus/knowledge/decisions/q02-first-pass-runtime-contract-v1/decision.json`

## Code paths

- `brep2code/corpus/runner.py`
- `tests/test_corpus_m4.py`

## Docs to update

- `docs/workflow/status.md`, this workpack, and active handoff
- a new sanitized M43 development review under `docs/architecture/v1/`
- `docs/runbooks/llm-provider-config.md` only if the contract changes a
  repeatable user-facing invocation

## Trace/schema changes

No schema change.  Existing schema-v3 reports and sanitized provider/execution
traces remain authoritative.

## Decision-package impact

- `decision_id`: `q02-first-pass-runtime-contract-v1`.
- Q01/Q02 effect: adds only execution-contract facts; it adds no B-Rep feature
  claim, operation helper, or reference script.
- Q03/Q04 effect: preserves existing gates and one-round repair; failures stay
  separately classified by provider, execution, output, and geometry stage.
- Evidence role: development-only discriminating and regression evidence.
- Knowledge disposition: pending review; no runtime card or helper follows
  automatically.

## Compatibility constraints

- Original STEP files, credentials, full responses, and environment snapshots
  remain local and unrecorded.
- Default commands remain offline and credential-free.
- Provider-generated scripts execute only under `wsl-bwrap`.
- Held-out case `abc_v00_00000031` is excluded and unauthorized.
- No new gate, helper, IR, SDK, manifest, asset, or sample is permitted.

## Authorization record

The user explicitly authorized this development-only run on 2026-08-08:
DeepSeek `deepseek-v4-pro`; cases 27 and 30; first-pass plus at most one repair
round; at most four requests; 120-second provider deadline; bounded probe
summary, case identifier, and runtime contract as outbound content.  Raw STEP
files do not leave the workspace.  During this run, the pre-existing summary
serializer also exposed a local absolute input path.  This was identified in
the sanitized local trace, disclosed to the user, and removed before any future
hosted request; it does not change the completed batch evidence.

## Acceptance

```powershell
uv run python -m pytest tests\test_corpus_m4.py -q -k "first_pass or hosted"
uv run python -m ruff check .
uv run python tools/check_governance.py
```

- Hashes, manifest membership, input probes, local provider configuration
  entry, WSL executor, request capacity, and unused report path pass preflight.
- The completed report records exactly at most two selected cases and at most
  four issued requests.
- Development review reports first-pass, repair, and each funnel denominator
  separately; it makes no held-out or benchmark claim.

## Evidence reuse / guidance-card disposition

Pending review.  A runtime card, helper, or policy change requires a separately
selected follow-up and cannot be inferred from this development run.

## Development evidence

The authorized batch completed at `data/corpus-runs/m43-runtime-contract-development-20260808.json` with 4/4 requests used and no provider timeout.  Case 27 first pass reached executable/readable output with volume and topology gates passing but bbox failing; its one-round repair exhausted.  Case 30 first pass failed on a typed STEP writer argument and its one-round repair passed all existing gates.  See `docs/architecture/v1/m43-first-pass-runtime-contract-development-review.md`.  The local request trace also revealed an unneeded absolute input path in the prior outbound summary; ADR-0046 removes it before any future hosted request.

## Closure rationale

The user reviewed the completed development result and explicitly authorized a
separate held-out evaluation under the sanitized summary policy.  M43 closes
without a benchmark or held-out claim; M44 owns that one-case run.

## Status transition

Update status first, then the workpack and handoff.  The user reviews the
completed development evidence independently.  Do not request or run held-out
until that review and a new explicit user authorization.

## Out of scope

Held-out execution, provider/model comparison, raw-response retention,
external download, broader prompt/context changes, helper/IR/SDK work, new
geometry gates, benchmark claims, and sample expansion.
