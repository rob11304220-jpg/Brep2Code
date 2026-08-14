# WP-M132-001: Shell Family Evidence Review and Disposition

- Status: done
- Milestone: M132
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

## Goal

Review exactly the six completed M130/M131 `shell-v1` experimental candidates,
state the evidence boundary, and record one non-promoting disposition.

## Scope

- Re-run the frozen intake and family audits, focused test, Ruff, governance
  audit, and diff check.
- Verify all six candidate records retain their frozen row, split, hash,
  geometry, sequence, editability, and semantic evidence.
- Verify candidates remain absent from executable manifest, Harness/runtime,
  provider, training, and hosted paths.
- Compare the declared `MakeThickSolidInward` Q02 operation with the reference
  construction implementation, then record what the evidence can and cannot
  establish.
- Record exactly one disposition: retain the candidates as experimental pending
  a separately selected native-shell evidence package, or reject them. This
  workpack cannot promote or modify candidate lifecycle.

## Attribution question and sampling intent

Distinguish whether M130/M131's six fixed rows provide evidence of an
executable shell operation rather than only its final geometry and declared
logical sequence. The sample is fixed at the frozen 3/3 family-isolated split;
the stopping condition is a single bounded disposition with no new rows.

## Inputs

- `docs/workpacks/done/WP-M130-001-shell-family-design-freeze.md`
- `docs/workpacks/done/WP-M131-001-shell-family-controlled-production.md`
- `docs/corpus/sequence-paired/shell-v1-preregistration.json`
- six `case-library/self-authored/param_shell_*` experimental directories

## Code paths

- `tools/build_m131_shell_candidates.py`
- `tools/audit_sequence_paired_shell.py`
- `tests/test_sequence_paired_shell.py`

## Docs to update

- `docs/workflow/status.md`
- this workpack and the active handoff
- `docs/corpus/sequence-paired/shell-v1-evidence-review.md`

## Trace/schema changes

None. No signal bundle, provider/tool trace, manifest, storage layout, or CLI
JSON contract changes are permitted.

## Decision-package impact

- `decision_id`: no Q01--Q04 decision package applies; this is a bounded
  sequence-paired corpus-evidence disposition.
- Q01/Q02 effect: no observable fact or constrained action changes; the review
  checks whether the frozen logical action is backed by its reference build.
- Q03/Q04 effect: no gate, diagnostic, repair, or stopping-rule change.
- Evidence role: regression and negative-control review of fixed production
  evidence.
- Knowledge disposition: record a counterexample to treating a declared
  `MakeThickSolidInward` sequence as proof of native-shell execution.

## Compatibility constraints

Offline-only and default network-free. No candidate-row substitution,
preregistration change, candidate rewrite, registry/manifest, Harness/runtime,
card, provider, training, external data, hosted request, parser/helper/SDK,
IR, or generic shell-recognition change.

## Acceptance

    uv run python tools\audit_sequence_paired_intake.py docs\corpus\sequence-paired\shell-v1-preregistration.json
    uv run python tools\audit_sequence_paired_shell.py
    uv run python -m pytest tests\test_sequence_paired_shell.py
    uv run python -m ruff check .
    uv run python tools\check_governance.py
    git diff --check

## Owner completion boundary

Publish the bounded evidence-review record, capture all acceptance results,
update lifecycle records, and request independent review. The owner cannot
close the G2 workpack without that review.

## Permitted stop conditions

Independent review; frozen-input drift; an out-of-scope dependency; or a
reproducible validation blocker. Partial review is not a stop condition.

## Evidence reuse / guidance-card disposition

Record the source-linked counterexample if declared shell sequence and
reference construction diverge. It does not authorize runtime retrieval,
promotion, or a guidance card.

## Status transition

On transition, update `docs/workflow/status.md` first, then this workpack and
the active handoff. This workpack changes no module, contract, runbook, or ADR
unless the review discovers a new lasting architecture decision.

## Closure rationale

Pending independent G2 review.

## Owner evidence (2026-08-12)

- Added `docs/corpus/sequence-paired/shell-v1-evidence-review.md`, which
  confirms the fixed six-row geometry/split/semantic evidence and records the
  construction mismatch: `MakeThickSolidInward` is declared, while
  `build_shape` uses `BRepAlgoAPI_Cut` and generated scripts delegate to it.
- The sole disposition is to retain all six assets as experimental. No
  promotion is proposed; any native-shell evidence requires a new workpack.
- The frozen intake audit, shell family audit (6 records), focused test (1
  passed), Ruff, and `git diff --check` passed. Governance remains to be run
  after lifecycle records are synchronized.

## Independent G2 review and closure (2026-08-12)

Liaol independently approved the recorded scope, fixed-row evidence,
construction counterexample, experimental-only disposition, and lifecycle
alignment. The six candidates remain experimental; no promotion, manifest,
runtime, provider, training, or hosted authority follows from this closure.

Closure acceptance: intake audit, six-record family audit, focused test,
Ruff, governance audit, and `git diff --check` passed. M132 closes because it
answered the bounded evidence question and recorded the sole non-promoting
disposition; a native-shell implementation/evidence question requires a newly
selected workpack.

## Out of scope

Promotion, active case-library admission, native-shell implementation,
candidate regeneration, executable manifest change, runtime/provider/training
use, hosted requests, and any `rib-v1` or robustness-micro-family work.

## Repair hypothesis and evaluation boundary

Not a repair experiment. It is offline-only evidence review; a future native
shell construction check requires a separately selected bounded workpack.
