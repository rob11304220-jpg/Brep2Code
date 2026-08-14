# WP-M42-001: First-Pass Runtime-Contract Decision Design

- Status: done
- Milestone: M42
- Owner: Codex
- Reviewer: not required (G1 design-only)
- Risk tier: G1

## Goal

Preregister the smallest offline design that can distinguish first-pass
runtime-contract incompatibility from B-Rep-to-CAD modeling failure.  It must
not claim model improvement or initiate a provider request.

## Scope

- Freeze the causal question, fixed policy, candidate evidence funnel, and
  development/held-out ordering for a possible later hosted comparison.
- Specify a minimal runtime contract limited to sandbox input reference,
  output location, installed OCP import compatibility, and execution
  expectations already supported by local evidence.
- Define the control conditions, failure taxonomy, stopping rules, and the
  exact conditions under which a separate G3 hosted evaluation may be selected.

## Attribution question and sampling intent

Can a concise, traceable runtime contract reduce first-pass failures before
script execution without being mistaken for an improvement in B-Rep modeling?
The later experiment, if selected, must use a preregistered low-complexity
external development split and an untouched held-out split.  Stop rather than
expand samples if the development comparison does not yield attributable,
gate-level evidence.

## Inputs

- `docs/architecture/v1/m10-012-minimal-offline-path-repair-review.md`
- `docs/architecture/v1/m10-external-attribution-ledger.md`
- `docs/runbooks/llm-provider-config.md`
- `docs/architecture/v1/runtime-boundaries.md`

## Code paths

No production code path changes.  A later G3 workpack must name any proposed
prompt/template, report, test, or corpus changes before implementation.

## Docs to update

- `docs/workflow/status.md`
- this workpack and the active handoff
- `docs/corpus/knowledge/decisions/index.json`
- `docs/corpus/knowledge/decisions/q02-first-pass-runtime-contract-v1/decision.json`
- ADR-0045

## Trace/schema changes

None.  A future G3 comparison must retain existing sanitized provider traces,
signal bundles, and schema-v3 report fields; any new classification field
requires a separately scoped contract change.

## Decision-package impact

- `decision_id`: `q02-first-pass-runtime-contract-v1`.
- Q01/Q02 effect: freezes only the runtime instructions required to execute a
  generated script; it adds no feature interpretation or CAD operation helper.
- Q03/Q04 effect: preserves existing gates and distinguishes provider,
  sandbox path, import/API, output, and geometry outcomes before any repair.
- Evidence role: fixed-script compatibility evidence, discriminating control,
  negative control, and regression boundary.
- Knowledge disposition: planning only; no runtime experience card and no
  reusable modeling knowledge are created by this design.

## Compatibility constraints

- Default operation remains offline and credential-free.
- No provider request, prompt or runtime behavior change, executable manifest
  change, helper, IR, SDK, gate, probe, schema, or case asset is allowed.
- Any later provider-generated script runs only through `wsl-bwrap`.
- The M10-012 path result remains fixed-script compatibility evidence, not a
  generic production helper or a first-pass quality claim.

## Acceptance

```powershell
uv run python -m pytest tests\test_governance_audit.py tests\test_corpus_m4.py -q
uv run python -m ruff check .
uv run python tools/check_governance.py
```

- The decision package states the supported runtime facts, non-matching import
  control, unchanged gate authority, and a no-improvement stopping rule.
- The workpack states that a future hosted comparison is G3, development-only
  first, and separately subject to provider preflight and explicit approval.
- No runtime, provider, corpus, or code artifact is changed.

## Evidence reuse / guidance-card disposition

No runtime experience card.  This is a planning record and cannot be mounted,
retrieved, or injected into a runtime LLM context.

## Status transition

On design closure, update status, this workpack, the active handoff, decision
index, and ADR.  A completed design may propose, but cannot activate, a G3
hosted evaluation workpack.

## Closure rationale

The design is complete.  It records the causal boundary, controls, stopping
rule, and G3 authorization boundary without changing runtime behavior.  The
focused governance tests passed (7 passed), the directly relevant hosted
contract regressions passed (8 passed, 29 deselected), Ruff passed, and the
governance audit passed.  The decision package remains `planned`: this
design does not itself select or authorize the later hosted experiment.

## Out of scope

Provider calls, prompt implementation, model/provider comparison, external
downloads, reference scripts, production helpers, IR/SDK work, new gates,
benchmark claims, and held-out evaluation.

## Repair hypothesis and evaluation boundary

The supported mechanism is limited to an inaccessible host input path in two
direct external traces; `/input/model.step` corrected both fixed scripts while
an unavailable import remained a non-match.  A later hosted comparison may
test whether an explicit runtime contract improves execution readiness.  It
cannot claim modeling improvement unless executable/readable output and the
unchanged geometry gates improve on a separately authorized held-out split.
