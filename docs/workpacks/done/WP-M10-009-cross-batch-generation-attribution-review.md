# WP-M10-009: Cross-Batch Generation Attribution Review

- Status: done
- Milestone: M10
- Owner: unassigned

## Goal

Review all completed M10-005 and M10-008 external first-pass cases to determine whether any repeated generation failure has direct, reproducible, trace-linked attribution sufficient to select a next evidence-gated route.

## Scope

- Analyze only existing completed reports, generated scripts, `signal_bundle.json`, and sanitized stdout/stderr from the six selected external cases.
- Separate provider lifecycle, sandbox input-path use, Python/import, OCP/API, parameter/unit, operation dependency, export/readability, geometry, and unknown outcomes.
- Distinguish a static symptom from a trace-proven execution cause; count a helper-threshold case only when the same cause is directly shown in the generated revision and execution signal.
- Publish a sanitized review that checks the geometry-diagnostics and narrow-helper thresholds, then selects exactly one follow-up route.

## Compatibility constraints

- No provider request, external download, fixture or manifest change, prompt/context change, or runtime behavior change.
- Existing gates remain authoritative; skipped geometry gates are not geometry-failure evidence.
- Raw assets, complete provider responses, and credentials remain local ignored data; published findings use only derived, sanitized facts.

## Acceptance

- All six completed cases appear in the review with first-pass and repair outcomes separated.
- Every non-provider classification cites a case id, revision id, and local signal path; unsupported classifications remain `unknown`.
- The review records whether any single direct root cause reaches three cases and selects one route without changing production behavior.

## Completion evidence

- The [cross-batch review](../../architecture/v1/m10-009-cross-batch-generation-attribution-review.md) represents all six completed cases and separates first-pass from repair evidence.
- Zero first-pass cases reached geometry comparison. Two sandbox-path cases and one incompatible-import case have direct trace support, but no one cause reaches the three-case threshold.
- Selected `WP-M10-010` for a third deterministic external increment; no hosted request or production change occurred.
