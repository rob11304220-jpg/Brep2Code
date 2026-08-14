# WP-M40-001: Controlled Multi-Agent Review

- Status: done
- Milestone: M40
- Owner: Codex
- Reviewer: user-approved implementation plan
- Risk tier: G1

## Goal

Turn the single-owner baseline into a usable small-team collaboration and
review protocol.

## Scope

Define owner, contributor, and reviewer responsibilities; exclusive paths;
conflict handling; and closure evidence. Record the durable policy in ADR-0043.

## Decision-package impact

- `decision_id`: none; development governance only.
- Q01/Q02/Q03/Q04 effect: none.
- Evidence role: process regression prevention.
- Knowledge disposition: no reusable runtime knowledge.

## Compatibility constraints

No scheduler, shared runtime memory, provider authority, or external service
is added.

## Acceptance

```powershell
uv run python tools/check_governance.py
uv run python -m ruff check .
```

## Closure rationale

The protocol supports bounded parallel inspection and independent review while
leaving lifecycle and high-risk paths to one owner.

## Out of scope

Large-scale autonomous agent dispatch and runtime collaboration.
