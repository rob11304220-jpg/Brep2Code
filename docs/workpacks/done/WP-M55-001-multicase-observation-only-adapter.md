# WP-M55-001: Multi-Case M48 Observation-Only Adapter

- Status: done
- Milestone: M55
- Owner: Codex
- Reviewer: Liaol
- Risk tier: G2

## Goal

Extend the M52 single-case observation-only build path into a provider-agnostic
multi-case development runner that preserves M48 path-free transcript egress,
no-input build execution, bounded first-pass and repair accounting, and
checkpointed aggregate reporting entirely offline with fake/loopback providers.

## Scope

- Add a selected-manifest runner/CLI path for one observation session per case.
- Ensure every first-pass provider request contains only the bounded M48
  transcript and no raw STEP, file name, host path, reference script, or trace
  path.
- Preserve no original input mount for generated builds and any bounded repair
  attempts; retain existing geometry, provenance and provider lifecycle facts.
- Add deterministic fake/loopback tests for two or more manifest cases,
  request limits, checkpoint reporting, and egress/no-input regressions.

## Attribution question and sampling intent

This work does not evaluate a model. It verifies that M54's frozen 12-case
development split can later be exercised through the same M48 security
contract proven for M51, without silently reverting to the old corpus summary.
Stop if the existing repair contract cannot retain no-input execution or
separate first-pass/repair accounting.

## Inputs

- Existing M48 observation envelopes and M52 `ObservedBuildLoopRunner`.
- Existing self-authored manifests only; do not alter cases, splits or input
  assets.
- Fake and loopback providers only; no credential read or hosted request.

## Code paths

- `brep2code/agent/observed_build.py`
- `brep2code/agent/repair.py`
- `brep2code/cli/__init__.py`
- `brep2code/corpus/runner.py` and report helpers only when required for the
  aggregate report/checkpoint contract
- focused tests under `tests/`

## Docs to update

- `docs/architecture/v1/contracts/q01-observation-build-separation.md`
- `docs/modules/cli.md`, `docs/modules/harness.md`, and this workpack/handoff
- `docs/runbooks/llm-provider-config.md` if a new secure command is added

## Trace/schema changes

An additive aggregate report or trace projection is allowed only if it retains
separate provider lifecycle, first-pass, repair, geometry-gate, and provenance
states. Any new schema field must be documented in the relevant contract and
covered by focused regression.

## Decision-package impact

- `decision_id`: `q01-q02-observation-build-separation-v1`.
- Q01/Q02 effect: applies the frozen observation/build separation to multiple
  fixed records; it does not add tools or observations.
- Q03/Q04 effect: retains current gates and limits repair to structured
  feedback without an input mount.
- Evidence role: offline security-boundary regression, not modeling evidence.
- Knowledge disposition: no reusable modeling knowledge.

## Compatibility constraints

Default execution remains offline and credential-free. Existing corpus
`--first-pass` semantics remain unchanged; the new path must be explicit.
No provider, prompt, manifest, external-data, case, or hosted authorization
change is permitted. Reference scripts remain local controls only.

## Acceptance

```powershell
uv run python -m pytest tests\test_observed_build_loop.py tests\test_agent_m3_repair_loop.py tests\test_corpus_m4.py -q
uv run python -m pytest -m sandbox -q
uv run python -m pytest
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

## Evidence reuse / guidance-card disposition

No reusable evidence. The result is an offline security/contract regression
only and does not authorize M54 or a provider request.

## Status transition

Record implementation, all test output, and Liaol's independent review before
closing. Update status first, then workpack and handoff. On closure, M54 still
needs a fresh preflight and explicit user authorization.

## Closure rationale

Pending.

## Implementation and owner acceptance

- Added explicit `observed-development` CLI path and extended
  `ObservedBuildLoopRunner` with bounded observation-only repair.
- Added a path-filtered repair context and forced `build_without_input=True`
  for every observation-only repair execution; legacy repair and corpus
  first-pass behavior remain unchanged.
- Added multi-case CLI and repair no-input/no-path egress regressions.
- Owner acceptance: focused adapter/repair tests `13 passed in 33.81s`; full
  offline suite `164 passed in 174.50s`; Ruff, governance audit, and
  `git diff --check` passed.
- Pending: Liaol's independent G2 review.

## Independent review and closure

- Liaol independently reviewed the multi-case adapter scope, egress/no-input
  regressions, request accounting, acceptance evidence, and lifecycle records
  on 2026-08-08.
- Review outcome: approved. M55 closes as offline adapter evidence only; it
  does not itself authorize M54 or any provider request.

## Out of scope

Any hosted call; user credentials; prompt redesign; manifest/case changes;
external data; held-out evaluation; model-quality claims; or using the old
filename-bearing corpus first-pass context.

## Repair hypothesis and evaluation boundary

Offline only. The repair path must reproduce the initial generated script,
retain its original gate evidence, accept at most the configured bounded
response, and rerun without `/input/model.step`. A passing fake repair proves
only adapter wiring and capability separation.
