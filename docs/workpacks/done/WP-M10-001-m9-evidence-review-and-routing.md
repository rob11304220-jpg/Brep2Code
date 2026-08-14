# WP-M10-001: M9 Completed Evidence Review and Routing

- Status: done
- Milestone: M10
- Owner: unassigned

## Goal

Review only completed M9 development and held-out reports, apply the shared failure taxonomy, and record exactly one evidence-supported next route.

## Scope

- Verify both reports retain the unchanged M9 provider/model, policy, executor, deadline, repair bound, case order, and gates.
- Separate first-pass, repair, provider, execution, input/output probe, and geometry outcomes by split.
- Select exactly one M10 route under the post-M9 roadmap, or record a closure note when M9 cannot produce two completed reports.

## Inputs

- [M9 workpack](../done/WP-M9-001-abc-hosted-first-pass-evaluation.md)
- [M9 review template](../../architecture/v1/m9-abc-hosted-evaluation-review.md)
- [Post-M9 roadmap](../../architecture/v1/post-m9-evidence-gated-roadmap.md)
- Ignored M9 schema-v3 reports and sanitized traces.

## Code paths

None expected.

## Docs to update

- `docs/architecture/v1/m9-abc-hosted-evaluation-review.md`
- `docs/workflow/status.md`, the active handoff, and this workpack.
- The selected follow-on workpack only; do not activate more than one route.

## Trace/schema changes

None. Review existing schema-v3 reports only.

## Compatibility constraints

No hosted call, case rerun, prompt change, Harness change, helper, IR, or SDK is part of review. `running` and `interrupted` reports never support aggregate conclusions.

## Acceptance

- Both split reports are `completed`, or the review states that no aggregate conclusion is available.
- The review records per-split first-pass and repair outcomes, request accounting, duration, and sanitized failure classes.
- Exactly one route is selected using the roadmap trigger rules, or no route is selected after an unavailable-batch closure.

## Status transition

When done, update status and handoff, move this workpack to `done/`, and activate only the selected conditional workpack. A new ADR is required only if the evidence supports a lasting architectural decision beyond ADR-0009.

## Out of scope

Model comparison, benchmark claims, hosted authorization, provider reruns, and implementation work.

## Result

Completed on 2026-08-02. Both M9 schema-v3 split reports were `completed` under the unchanged policy and were reviewed in [`m9-abc-hosted-evaluation-review.md`](../../architecture/v1/m9-abc-hosted-evaluation-review.md). The evidence contains no direct, reproducible three-case OCP/API, parameter, or dependency-sequencing pattern and insufficient executable geometry-failure evidence for diagnostics. The sole selected route is `WP-M10-003`.
