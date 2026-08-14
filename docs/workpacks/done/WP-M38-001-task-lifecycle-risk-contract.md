# WP-M38-001: Task Lifecycle Risk Contract

- Status: done
- Milestone: M38
- Owner: Codex
- Reviewer: user-approved implementation plan
- Risk tier: G1

## Goal

Make active-task ownership, risk tiers, closure gates, and handoff linkage a
single development-governance contract.

## Scope

Add the lifecycle document, make AGENTS a concise task router, and update
workpack/handoff templates and rules. No Harness, case, manifest, provider,
runtime, external-data, or hosted change is permitted.

## Decision-package impact

- `decision_id`: none; development governance only.
- Q01/Q02/Q03/Q04 effect: none.
- Evidence role: process regression prevention.
- Knowledge disposition: no reusable runtime knowledge.

## Compatibility constraints

Default operation remains offline and credential-free. Existing archived
workpacks remain historical records and are not retroactively required to use
the new active-task fields.

## Acceptance

```powershell
uv run python tools/check_governance.py
uv run python -m ruff check .
```

## Closure rationale

`docs/workflow/task-lifecycle.md` defines G0--G3 gates; ADR-0042 records the
lasting decision. The contract is enforced for new active work only.

## Out of scope

Runtime agent behavior, provider requests, external data, and automatic task dispatch.
