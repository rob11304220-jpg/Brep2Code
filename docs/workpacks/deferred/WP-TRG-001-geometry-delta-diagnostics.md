# WP-TRG-001: Report-Only Geometry Delta Diagnostics

- Status: deferred
- Owner: unassigned

## Goal

Add deterministic, compact geometry-delta evidence to corpus reports so repair can distinguish where an executable output differs from its input without changing pass/fail gates.

## Trigger condition

At least three completed cases have passing execution and input/output readability evidence but geometry failures that bbox, volume, and topology summaries cannot make actionable.

## Scope

- Preserve existing bbox, volume, and topology gates as the only pass/fail authority.
- Add report-only signed bbox deltas, volume ratio, topology-count deltas, and deterministic sampled surface-distance summaries.
- Bound output size and expose compact directional/worst-region information suitable for repair feedback.
- Demonstrate repeatability on preregistered self-authored and external-local cases before any proposal to create a new gate.

## Inputs

- [Post-M9 roadmap](../../architecture/v1/post-m9-evidence-gated-roadmap.md)
- Completed evidence review and selected failure examples.
- [Case corpus contract](../../architecture/v1/contracts/case-corpus.md)

## Code paths

- `brep2code/brep/`
- `brep2code/corpus/`
- `tests/test_corpus_m4.py`

## Docs to update

Update the case-corpus contract, module documentation, runbook, status, handoff, and an ADR if report semantics become a lasting contract decision.

## Trace/schema changes

Expected corpus-report extension only. It must be versioned, non-sensitive, compact, and explicitly marked diagnostic; existing schema readers remain supported.

## Compatibility constraints

Default execution remains offline. No new pass/fail gate, provider call, external download, IR, SDK, VLM judge, FEA, or multi-agent path is introduced.

## Acceptance

- Repeated runs of every preregistered case produce stable diagnostic summaries under fixed sampling/tessellation settings.
- Existing gate statuses and default corpus behavior remain unchanged.
- Tests prove diagnostics are omitted or structured when an input/output artifact is unavailable.
- The completed review shows the diagnostic yields actionable repair information for the selected failure examples.

## Status transition

When done, update status, handoff, contracts, runbooks, and any required ADR before moving this workpack to `done/`.

## Out of scope

Promoting diagnostics to gates, changing geometry tolerances, provider evaluation, IR, SDK, or CAD workplace design.
