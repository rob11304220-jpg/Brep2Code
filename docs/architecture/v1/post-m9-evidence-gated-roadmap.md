---
type: roadmap
related-project: Brep2Code
version: v1
status: active
tags:
  - Brep2Code
  - v1
  - M9
  - evaluation
  - architecture-governance
---

# Post-M9 Evidence-Gated Roadmap

## Purpose

This roadmap governs the first architecture decision after M9-001 and its later cumulative-attribution continuation. It is not authorization to run a hosted provider and it does not replace [`docs/workflow/status.md`](../../workflow/status.md) as the current-work source of truth. [ADR-0009](../adr/0009-evidence-gated-post-m9-evolution.md) governs the original M9 route decision; [ADR-0010](../adr/0010-attribution-driven-repair-governance.md) governs post-M10-010 cumulative routing.

## Entry condition

M10 routing begins only when both M9 split reports are `completed` and were run with the unchanged provider/model, generation policy, executor, provider deadline, repair bound, case order, and existing gates. `running` and `interrupted` reports are partial evidence only. If an authorized batch is conclusively unavailable, M9 records a closure note and no aggregate routing decision is made.

## Route selection

| Evidence from completed M9 reports | One selected next workpack | Intended outcome |
|---|---|---|
| Every selected case has execution/readability evidence, at least three cases still have geometry failures not actionable from bbox, volume, and topology summaries | `WP-TRG-001` | Add deterministic, report-only geometry-delta diagnostics. |
| No attributable helper pattern reaches the threshold below, or the completed sample is insufficient to establish a stable pattern | `WP-M10-003` | Admit a small deterministic external batch and establish an offline baseline. |
| At least three external cases share one attributable OCP/API, parameter, or dependency-sequencing failure | `WP-TRG-002` | Propose one narrow helper with regression evidence. |

`WP-M10-001` performs the review and records exactly one selected route. If more than one condition appears true, select the narrow helper only when its attribution is direct and reproducible; otherwise select geometry diagnostics before changing the operation surface.

## Invariants

- M9 development and held-out execution are unchanged between splits and remain separately authorized.
- Existing gates remain the pass/fail authority. Geometry diagnostics are report-only until a later decision promotes them.
- External raw assets, reports, records, and traces remain ignored under `data/`; every new sample requires source identity, SHA-256, probe result, split, and license review before use.
- No external manifest has a `reference_script` or `first_pass_script` unless a future dedicated decision establishes a lawful, reproducible source.
- Default commands remain offline and credential-free. Nothing in this roadmap authorizes a provider call.

## Post-admission evaluation sequence

`WP-M10-003` was the route selected by M10-001. Its deterministic, offline admission was a prerequisite for, not an authorization of, the next hosted evaluation. The completed sequence progressed through M10-010, a third deterministic offline increment with a verified complete ignored local cache.  The current continuation is `WP-M10-011`, which verifies cumulative attribution before selecting any successor route. For the original selected route, the fixed order was:

1. `WP-M10-005` evaluates the newly admitted, hash/probe/sandbox-verified development manifest using an unchanged hosted first-pass policy.  Freeze that policy before separately authorized held-out execution.
2. `WP-M10-006` reviews only completed reports and their existing local evidence, then records whether the next route is report-only geometry diagnostics, one narrow helper, or another deterministic external increment.
3. Do not change prompt context, probe access, gates, helpers, IR, or the provider policy within either split.  A later context-policy comparison requires its own preregistered development-only workpack after this review.

This sequence is deliberately conditional: an authorized hosted evaluation may begin only after the required preflight succeeds and after the caller separately authorizes each split.  It does not reuse budget from a prior report or make a provider request by default.

## Cumulative attribution and repair routing after M10-010

[ADR-0010](../adr/0010-attribution-driven-repair-governance.md) supersedes the old automatic fallback of another increment after M10-010; it leaves the completed M9 route decision and M10-010 scope intact.  Each later review first updates the [M10 external attribution ledger](m10-external-attribution-ledger.md), then selects exactly one route:

| Evidence | Selected route | Required review record |
|---|---|---|
| At least three cases share one `direct` root cause | Narrow helper | Trace-supported common cause and non-match cases. |
| At least three executable/readable first-pass outputs have non-actionable geometry failures | Report-only geometry diagnostics | Why existing summaries cannot guide repair. |
| At least two external cases share one `direct` or `supported`, locally reproducible execution mechanism | Minimal offline repair experiment | Fixed-script reproduction, non-matching control, and unchanged gate evidence. |
| No condition above qualifies | Deterministic external increment | Attribution question, expected information gain, and stopping condition. |

Only `direct` evidence counts toward the narrow-helper threshold.  A static symptom cannot be promoted to `direct`; provider lifecycle results are not generated-script evidence.  An offline experiment can establish deterministic compatibility or observability only.  It cannot claim model improvement or alter production behavior.  Any prompt/context comparison is a separately preregistered development-only hosted workpack with fresh preflight and explicit authorization; held-out execution follows a development review and separate authorization.

## Evidence interpretation and reporting

Hosted reviews must present a conditional evidence funnel rather than a single aggregate success rate:

```text
selected cases
  -> readable input probe
  -> provider response received
  -> script exited and output STEP is readable
  -> existing geometry gates pass
  -> bounded repair passes (where attempted)
```

- State the denominator for every funnel stage, plus requests issued, provider deadline, and duration by split.
- A provider lifecycle failure has no attributable generated script; do not count it as a script, OCP/API, parameter, dependency-sequencing, or geometry failure.
- A script or output-readability failure has not reached geometry comparison; its skipped geometry gates are not geometry evidence.
- A repair pass is reported separately from the first-pass result.  It is evidence of one bounded recovery, not a replacement first-pass score.
- The auditable model context is limited to bounded probe data, the repair signal bundle, sanitized request/response messages, generated script updates, and execution traces.  The system neither stores nor evaluates unexposed internal reasoning or chain-of-thought.

`WP-M10-006` may classify completed-case evidence as provider lifecycle, Python/import, OCP/API, parameter/unit, operation dependency, export/readability, geometry mismatch, or unknown.  Each non-provider classification must cite a case and revision trace.  Fake-provider replay and expected fixed-scaffold controls remain Harness compatibility evidence, not hosted-model-quality evidence.

## Deferred abstractions

An IR may be explored only through `WP-TRG-003` after two validated helpers reveal the same operation-dependency or entity-reference model and script-level repair cannot preserve a correct prefix. The experiment is parallel-only: its smallest operation set is evaluated through the existing Harness and never replaces the production script path.

A full CAD SDK requires a new ADR after the IR experiment demonstrates, on preregistered cases, no loss of existing gate outcomes, lower repair burden, and more auditable traces. FEA, VLM judging, and multi-agent orchestration are not scheduled because they do not address the current single-solid B-Rep reconstruction evidence gap.

## Historical execution provenance

M10-001 through M10-012 are completed execution history. Their durable route
and evidence interpretation are held by [ADR-0009](../adr/0009-evidence-gated-post-m9-evolution.md),
[ADR-0010](../adr/0010-attribution-driven-repair-governance.md), the
[M10 external attribution ledger](m10-external-attribution-ledger.md),
[M34 decision review](m34-next-decision-gate-review.md), and the
[route-disposition index](../../workflow/workpack-route-disposition-index.md).
Open their completed workpacks only for acceptance detail or original
provenance; none is a current execution entry point.
