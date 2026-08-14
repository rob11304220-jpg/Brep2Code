# Handoff: Shared Hosted-Stability Re-entry

- **Date**: 2026-08-11
- **Subproject**: `brep2code`
- **Status**: `active`
- **Related workpack**: `WP-M127-001-shared-hosted-stability-reentry`

## Goal

Freeze one fresh shared hosted-stability re-entry boundary, complete its
offline preflight, and either reach a preflight-ready G3 authorization request
or close with an explicit blocked-by-hosted-stability condition.

Terminal evidence is awaiting independent review.

## Done

- Added the hosted terminal triage runbook and linked it from the four-track
  roadmap and evidence-portfolio maintenance runbook.
- Selected and activated `WP-M127-001` as the next bounded package after the
  completed M123--M126 family-preparation queue and the terminal M118 run.

## In progress

- M127 completed its authorized two-request execution with fresh accounting:
  `2/2` requests were issued and the report reached `completed`.
- The terminal class is script/API failure: the generated script imported
  unavailable `STEPControl_STEPModelType` from `OCP.STEPControl`; sandbox,
  provenance, and downstream gates were not evaluated. The 47.819-second
  final provider response was within the frozen 300-second deadline.

## Next

- Obtain Liaol's independent G3 terminal review of the M127 report and confirm
  the `2/2` accounting, lifecycle/script-API separation, and not-evaluated
  downstream gates.
- After that review, use hosted terminal triage to select one fresh bounded
  output-contract or family-scoped remediation/re-entry package. Do not retry,
  repair, reuse M127 paths/budget, or widen this run.

## Decisions

- M118 and M127 are terminal and non-reusable. M127's `script/API failure`
  does not establish a provider lifecycle failure or a geometry conclusion.
- Hosted feedback may change only the next bounded package choice, not the
  frozen boundary of a finished run.

## Blockers

- Independent G3 terminal review is required before M127 can close or route a
  new package.

## Key paths

| Kind | Path |
|------|------|
| Workpack | `docs/workpacks/active/WP-M127-001-shared-hosted-stability-reentry.md` |
| Status | `docs/workflow/status.md` |
| M117 review | `docs/workpacks/done/WP-M117-001-hosted-stability-reentry-evidence-review.md` |
| M118 terminal package | `docs/workpacks/done/WP-M118-001-fresh-hosted-stability-preflight.md` |
| Triage runbook | `docs/runbooks/hosted-terminal-triage.md` |

## Resume prompt

```
Continue Brep2Code work: finish M127 shared hosted-stability re-entry.
Read docs/handoff/active/2026-08-11-m127-shared-hosted-stability-reentry.md.
First action: obtain Liaol's independent G3 terminal review of M127's completed
`2/2` report. Classify it only as script/API failure, retain downstream gates
as not evaluated, and do not retry or reuse its budget or paths.
```
