# WP-M45-001: Q03 Reconstruction-Provenance Gate Design

- Status: done
- Milestone: M45
- Owner: Codex
- Reviewer: not required (G1)
- Risk tier: G1

## Goal

Freeze the smallest Q03 design that prevents an input STEP read-and-re-export
from being counted as B-Rep-to-CAD reconstruction, while retaining the current
output and geometry gates as Harness-health evidence.

## Scope

- Define explicit result classes for `independent_reconstruction`,
  `round_trip`, and `provenance_unknown`.
- Specify the evidence required to classify direct or indirect dependence on
  the mounted input STEP.
- Specify a future execution-level control that distinguishes an independently
  constructed script from a script that depends on the mounted original.
- State how future Q01 observation may remain possible without granting the
  executed build script read access to the original STEP.
- Propose, but do not implement, the narrowest follow-on workpack.

## Attribution question and sampling intent

Can Q03 distinguish a geometrically matching output that was independently
constructed from one obtained by re-exporting the mounted input?  M44 is the
fixed positive round-trip counterexample.  This design stops after defining
classification and controls; it does not add cases, run a provider, or claim a
reconstruction rate.

## Inputs

- `docs/architecture/v1/m44-first-pass-runtime-contract-held-out-review.md`
- `docs/architecture/adr/0047-first-pass-round-trip-is-not-reconstruction.md`
- `docs/architecture/v1/runtime-boundaries.md`
- `data/records/corpus-abc_v00_00000031/revisions/20260808T022759497760Z/`

## Code paths

No production code changes.  A later G2 implementation must name its executor,
generation-policy, gate/schema, test, and report paths before modifying them.

## Docs to update

- `docs/workflow/status.md`
- this workpack and the active handoff
- `docs/corpus/knowledge/decisions/index.json`
- `docs/corpus/knowledge/decisions/q03-reconstruction-provenance-v1/decision.json`
- `docs/architecture/adr/0048-reconstruction-provenance-gate-design.md`

## Trace/schema changes

None.  The design proposes a future classification and execution-control trace,
but changes neither `signal_bundle.json` nor report schema-v3.

## Decision-package impact

- `decision_id`: `q03-reconstruction-provenance-v1`.
- Q01/Q02 effect: Q01 observations may be logged through bounded tools, but a
  Q02 build script cannot count as independent if its executed dataflow reads
  the mounted original STEP.
- Q03/Q04 effect: geometry equality remains necessary Harness evidence but is
  insufficient for reconstruction; repairs retain their existing diagnosis
  role until a separately selected implementation changes that contract.
- Evidence role: M44 is a direct round-trip counterexample; the future absent-
  input control is discriminating and direct-read detection is a regression.
- Knowledge disposition: design only; no runtime guidance card or reusable
  modeling knowledge.

## Compatibility constraints

Offline only.  No provider request, raw STEP egress, case/manifest change,
runtime access change, gate/schema change, helper, IR, SDK, or training input.
Existing executable/readability/bbox/volume/topology gates stay authoritative
for Harness health and must not be relabeled as reconstruction evidence.

## Acceptance

```powershell
uv run python -m pytest tests\test_governance_audit.py tests\test_corpus_m4.py -q
uv run python tools/check_governance.py
git diff --check
```

- The decision package defines result classes, evidence precedence, an
  execution-level discriminating control, and a fail-closed result.
- It separates logged Q01 observation from executed-script input access.
- It identifies a G2 implementation boundary and prohibits a hosted rerun.

## Evidence reuse / guidance-card disposition

Counterexample only: M44 documents that geometry-equivalent STEP round-trip is
not reconstruction.  It creates no runtime-retrievable card.

## Status transition

On closure, update `docs/workflow/status.md`, this workpack, the active
handoff, the decision index, and ADR-0048; move the workpack to `done/`.
Any follow-on implementation must begin in a new G2 workpack with an
independent reviewer.

## Closure rationale

Completed the result classes, precedence rule, fail-closed disposition, Q01/Q02
capability separation, and a future absent-input control.  The first focused
test run had 43 passing tests and one expected health-snapshot failure while
this workpack was active; after closure, the same checks must pass with no
active workpacks.  No executable Harness behavior changed.

## Out of scope

Implementing a gate, changing sandbox mounts, modifying prompts, evaluating
models, adding cases, provider use, or making any reconstruction-quality claim.

## Repair hypothesis and evaluation boundary

M44 demonstrates the mechanism directly: the generated script calls the OCP
STEP reader on `/input/model.step`, transfers the resulting shape unchanged,
and writes `output/model.step`.  The later implementation must retain this
fixture as a round-trip regression and use an absent-input execution control.
It is offline; no development or held-out hosted evaluation is selected.
