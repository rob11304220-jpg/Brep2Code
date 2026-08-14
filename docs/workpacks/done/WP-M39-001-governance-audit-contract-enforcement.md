# WP-M39-001: Governance Audit Contract Enforcement

- Status: done
- Milestone: M39
- Owner: Codex
- Reviewer: user-approved implementation plan
- Risk tier: G1

## Goal

Enforce the new active-task contract with dependency-free local audit checks
and focused regression tests.

## Scope

Require active workpacks to declare owner and risk tier; require an
independent reviewer for G2/G3; require an active handoff linked to an active
workpack. Add positive and negative regression coverage.

## Decision-package impact

- `decision_id`: none; development governance only.
- Q01/Q02/Q03/Q04 effect: none.
- Evidence role: process regression prevention.
- Knowledge disposition: no reusable runtime knowledge.

## Compatibility constraints

The audit reads local governance files only. It does not inspect credentials,
execute Harness workspaces, or contact providers.

## Acceptance

```powershell
uv run python tools/check_governance.py
uv run python -m pytest tests/test_governance_audit.py
uv run python -m ruff check .
```

## Closure rationale

The audit now rejects unowned or unclassified active work and missing or
self-reviewing G2/G3 reviewers, while preserving archived historical records.

## Out of scope

Manifest, provider, runtime, corpus, and hosted changes.
