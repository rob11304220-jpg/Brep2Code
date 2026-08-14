# WP-M82-001: Generated-Script API Contract Alignment

- Status: done
- Milestone: M82
- Owner: Codex
- Reviewer: Liaol
- Risk tier: G2

## Goal

Make the supported CAD API boundary executable and fail closed before the
sandbox runs a generated `build_sequence.py`, addressing M80's classified
`cadquery` incompatibility without a retry or provider request.

## Scope

- Define a small static validator that rejects known unsupported CAD imports
  (`cadquery` and `OCC`/`OCC.Core`) before executor invocation.
- Record the validation disposition in local execution and signal evidence.
- Preserve scripts using the installed `OCP` bindings and verify both paths
  with deterministic local fixtures and fake-provider observation flow.
- Align the build-script and observation-build contracts with this gate.

## Inputs

- M80 terminal evidence: generated `box` script imported unavailable
  `cadquery`; no hosted report, budget, response, or prompt content is reused.

## Code paths

- `brep2code/cad/`
- `brep2code/agent/harness.py`
- `brep2code/agent/observed_build.py`
- `tests/test_harness_m2.py`, `tests/test_observed_build_loop.py`

## Docs to update

- `docs/architecture/v1/contracts/build-script.md`
- `docs/architecture/v1/contracts/q01-observation-build-separation.md`
- `docs/modules/harness.md`
- `docs/workflow/status.md` and active handoff

## Trace/schema changes

Additive local `execution.build_script_contract` evidence only. Do not change
provider traces, corpus reports, manifests, or stored response content.

## Decision-package impact

- `decision_id`: no package applies; this is a runtime API compatibility gate.
- Q01/Q02 effect: constrain Q02 scripts to the installed OCP API boundary.
- Q03/Q04 effect: distinguish static API rejection from sandbox/script errors.
- Evidence role: regression for the M80 incompatibility classification.
- Knowledge disposition: no reusable modeling knowledge.

## Compatibility constraints

Default operation remains offline and network-free. No provider, prompt,
executor, manifest, gate tolerance, IR, SDK, runtime retrieval, or hosted
authorization changes are in scope. OCP scripts remain valid.

## Acceptance

```powershell
uv run python -m pytest tests\test_harness_m2.py tests\test_observed_build_loop.py -q
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

## Evidence reuse / guidance-card disposition

No reusable knowledge: this is a runtime compatibility guard, not a modeling
mechanism or runtime guidance card.

## Status transition

After reviewer approval, update `status.md` first, move this workpack to
`done/`, archive the handoff, and record acceptance output. A later reference
pack/retrieval task must be separately selected.

## Owner acceptance record

- Implemented the additive `build-script-api-v1` static validation gate. A
  script importing `cadquery`, `OCC`, or `OCC.Core` now receives exit code 126,
  `contract_rejected`, and a structured `build_script_contract` disposition
  without starting an executor or provenance control.
- The bounded observation-build instruction now names the OCP-only rule. OCP
  fixture and default smoke paths remain accepted.
- 2026-08-10 owner checks passed: focused Harness/observation tests (29
  passed in 73.39s), full Ruff, and `git diff --check`. Governance audit passes
  after the lifecycle records in this workpack and handoff are saved.
- Pending independent G2 review by Liaol: verify rejection-before-execution,
  additive evidence, preserved OCP path, scope boundaries, and no hosted work.

## Independent review and closure

- Reviewer: Liaol
- Outcome: approved on 2026-08-10.
- Closure rationale: M82 turns the M80 `cadquery` incompatibility into an
  explicit local contract rejection while retaining the OCP reference path.
  It makes no provider/model-quality claim and does not retry M80 or activate
  M73. The next M83 planning/curation work remains a separate selection.

## Out of scope

Hosted retry, repair, endpoint/model/prompt modification, dependency
installation, broad allow-listing, case/manifest changes, reference retrieval,
or any new CAD helper.
