# WP-M10-006: External Generation Failure Attribution Review

- Status: done
- Milestone: M10
- Owner: unassigned

## Goal

Review completed external first-pass evidence to produce reproducible, trace-linked failure attribution and select the next evidence-gated route without changing runtime behavior.

## Trigger condition

Both split reports and the sanitized review from completed `WP-M10-005` are available.  `running` and `interrupted` reports may inform an incident note but cannot support an aggregate route decision.

## Scope

- Analyze only existing corpus reports, generated scripts, `signal_bundle.json`, stdout/stderr, and sanitized revision traces from completed cases.
- Attribute every reviewed case to one primary category: provider lifecycle, Python/import, OCP/API, parameter/unit, operation dependency, export/readability, geometry mismatch, or unknown.
- Cite the case id, revision id, and local trace/signal path for each non-provider attribution; leave an outcome `unknown` when evidence does not support a narrower cause.
- Separate first-pass outcome, repair outcome, and fake-provider replay.  Do not present provider failures, expected fixed-scaffold controls, or fake replays as hosted-model-quality evidence.
- Publish a review that selects exactly one follow-up: `WP-M10-002` when at least three executable/readable cases have geometry failures not actionable from existing summaries; `WP-M10-004` when at least three completed external cases share one direct and reproducible OCP/API, parameter, or dependency-sequencing failure; otherwise another deterministic external increment under the existing M10-003 route.

## Inputs

- Completed `WP-M10-005` reports and evaluation review.
- [Post-M9 roadmap](../../architecture/v1/post-m9-evidence-gated-roadmap.md).
- [Case corpus contract](../../architecture/v1/contracts/case-corpus.md).
- [Signal bundle contract](../../architecture/v1/contracts/signal-bundle.md).

## Code paths

No production code path is selected.  The workpack is an offline evidence review; a later approved workpack owns any classifier, report-schema, probe, gate, helper, or prompt implementation.

## Docs to update

Create the attribution review, update status, handoff, and the workpack index when this workpack changes state.  Create an ADR only if the selected next route establishes a lasting architecture boundary not already governed by ADR-0009.

## Trace/schema changes

None.  The review consumes existing ignored local evidence and must not add classification fields to corpus reports, alter `signal_bundle.json`, retain full provider responses, or capture hidden reasoning.  A proposal to make classifications a durable report contract requires a separate workpack and ADR decision.

## Compatibility constraints

- No provider request, external download, fixture change, manifest change, prompt/context change, or runtime behavior change occurs in this review.
- Existing gates remain authoritative; skipped geometry gates are not geometry-failure evidence.
- All external raw assets, records, and traces remain local ignored data; the published review contains only sanitized identifiers and derived findings.

## Acceptance

- Every completed case is represented in the review, with first-pass and repair outcomes reported separately.
- Every non-provider classification has trace-supported case/revision evidence; unsupported claims are marked `unknown`.
- The final route selection explicitly checks the three-case geometry-diagnostics and narrow-helper thresholds and records why any unselected route did not qualify.
- Documentation links resolve and no production code, fixture, manifest, report schema, or external data is modified.

## Status transition

When complete, update `docs/workflow/status.md`, this workpack, the active handoff, `docs/workpacks/README.md`, and the attribution review.  Move this workpack to `done/` only after it records one selected next route.

## Implementation evidence

- Reviewed all three completed M10-005 cases without changing runtime behavior or retaining provider responses.
- The [attribution review](../../architecture/v1/m10-006-external-failure-attribution-review.md) records one provider-lifecycle result and two trace-supported unknown script failures; no geometry or direct helper threshold is met.
- Selected a second deterministic local external increment, now `WP-M10-007`.

## Out of scope

Hosted evaluation, provider reliability implementation, prompt experiments, reference scripts, automatic failure classifiers, report-schema changes, new probes or gates, helpers, IR, SDK, benchmark claims, FEA, VLM judging, and multi-agent orchestration.
