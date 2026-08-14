# WP-M37-001: Governance Skills and Collaboration

- Status: done
- Milestone: M37
- Owner: Codex

## Goal

Make recurring development-governance workflows reusable and define safe
boundaries for parallel development work.

## Scope

- Add four concise project Skills for workpack review, offline validation,
  hosted preflight, and evidence review.
- Add a single-owner collaboration protocol.
- Record the lasting governance decision.

## Decision-package impact

- `decision_id`: none; development governance only.
- Q01/Q02/Q03/Q04 effect: none.
- Evidence role: process regression prevention.
- Knowledge disposition: no reusable runtime knowledge.

## Compatibility constraints

No change to Harness, cases, manifests, provider configuration, hosted
authority, runtime prompts, helpers, IR, or SDK.

## Acceptance

```powershell
python C:\Users\Liaol\.codex\skills\.system\skill-creator\scripts\quick_validate.py .cursor\skills\workpack-create-review
python C:\Users\Liaol\.codex\skills\.system\skill-creator\scripts\quick_validate.py .cursor\skills\offline-validation
python C:\Users\Liaol\.codex\skills\.system\skill-creator\scripts\quick_validate.py .cursor\skills\hosted-preflight
python C:\Users\Liaol\.codex\skills\.system\skill-creator\scripts\quick_validate.py .cursor\skills\evidence-review
uv run python tools\check_governance.py
```

## Completion

Four validated Skills and the collaboration protocol were added. No runtime or
hosted authority was changed.
