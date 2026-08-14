# WP-M137: Terminal Evidence Review

- Status: done
- Milestone: M137
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

## Goal

Review only the completed M135-011 terminal evidence, preserving its frozen
cohort boundary and identifying whether existing sanitized traces support any
narrow attribution or only an observability follow-up.

## Scope

- Verify report/monitor terminality, 18/18 accounting, zero repair/retry and
  condition-level terminal distribution.
- Inspect existing local revision artifacts without changing them; distinguish
  static API, sandbox and downstream gate stages.
- Record family-local observations, nonclaims and the minimal M138 static API
  rejection-observability candidate.

## Compatibility constraints

Read-only review. Do not construct a provider, read credentials, issue a
request, alter prompts/cards/gates/cohort, add repair, or rerun M135.

## Acceptance

```powershell
uv run python tools\check_governance.py
git diff --check
```

## Owner completion boundary

Publish the evidence review and obtain Liaol's independent G2 review.

## Out of scope

Card update, repair policy, M138 implementation, hosted execution, held-out
evaluation, prompt/gate/runtime changes.

## Owner completion evidence (2026-08-12)

The terminal report and monitor confirm 18/18 accounting, completion and zero
repair/retry. Existing signal bundles support the downstream-gate grouping;
card rows have no stored script/Harness revision because static rejection
precedes sandbox launch. The bounded review and M138 disposition are recorded
in [`m137-terminal-evidence-review.md`](../../workflow/m137-terminal-evidence-review.md).

## Independent review and closure (2026-08-12)

Liaol approved the independent G2 review. The review accepted the terminal
accounting, stage-separated evidence boundary and disposition: no card update
or repair is justified from M135 alone; M138 is a separate observability-only
follow-up.
