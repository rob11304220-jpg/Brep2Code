# WP-M41-001: Read-Only Governance Health

- Status: done
- Milestone: M41
- Owner: Codex
- Reviewer: user-approved implementation plan
- Risk tier: G1

## Goal

Provide a reproducible, offline snapshot of development-governance health.

## Scope

Add a Markdown/JSON command reporting lifecycle counts, ledger dispositions,
and current governance-audit status; document it and test its repository
snapshot behavior.

## Decision-package impact

- `decision_id`: none; development governance only.
- Q01/Q02/Q03/Q04 effect: none.
- Evidence role: process regression prevention.
- Knowledge disposition: no reusable runtime knowledge.

## Compatibility constraints

The command is read-only, uses no credentials, sends no data externally, and
makes no claim about Harness or provider performance.

## Acceptance

```powershell
uv run python tools/governance_health.py --format markdown
uv run python tools/governance_health.py --format json
uv run python tools/check_governance.py
uv run python -m pytest tests/test_governance_audit.py
uv run python -m ruff check .
```

## Closure rationale

ADR-0044 and the runbook define a small, reproducible health view without
creating a productivity score or dashboard service.

## Out of scope

Hosted telemetry, personal performance evaluation, and repository mutation.
