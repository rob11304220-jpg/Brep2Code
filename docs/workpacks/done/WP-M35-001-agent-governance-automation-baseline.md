# WP-M35-001: Agent Governance Automation Baseline

- Status: done
- Milestone: M35
- Owner: Codex

## Goal

Make the existing agent-governance lifecycle mechanically checkable without
changing Harness, case libraries, runtime behavior, or hosted-provider policy.

## Scope

- Reconcile the completed M34 handoff with the no-active-workpack state.
- Add a dependency-free repository governance audit and focused tests.
- Add CI checks for formatting, tests, and governance consistency.
- Document the audit and record the lasting governance decision.

## Attribution question and sampling intent

No Q01--Q04 decision package applies. This is a bounded development-governance
change intended to distinguish repository-state drift from compliant task
lifecycle state; no case growth or modeling claim is involved.

## Code paths

- `tools/check_governance.py`
- `tests/test_governance_audit.py`
- `.github/workflows/ci.yml`

## Docs to update

- `docs/workflow/status.md`
- `docs/runbooks/governance-audit.md`
- `docs/architecture/adr/0039-agent-governance-automation-baseline.md`
- `docs/handoff/active/`

## Trace/schema changes

None. The audit reads Git-tracked governance documents only and produces
terminal diagnostics; it does not change runtime JSON, traces, reports, or
storage layout.

## Decision-package impact

- `decision_id`: none; no Q01--Q04 package applies.
- Q01/Q02 effect: none.
- Q03/Q04 effect: none.
- Evidence role: governance regression check.
- Knowledge disposition: no reusable runtime knowledge.

## Compatibility constraints

Default operation remains network-free. Existing CLI commands, fixtures,
manifests, runtime boundaries, provider controls, and deferred IR/SDK work
remain unchanged.

## Acceptance

```powershell
uv run python tools/check_governance.py
uv run python -m pytest tests/test_governance_audit.py
uv run python -m ruff check .
uv run python -m pytest
git diff --check
```

The focused tests must demonstrate failure for a completed active handoff and
for a mismatch between active workpacks and `status.md`.

## Evidence reuse / guidance-card disposition

No reusable runtime evidence.

## Status transition

On completion, update `docs/workflow/status.md`, archive the superseded M34
handoff, complete this workpack, and publish a new completion handoff. ADR-0039
records the persistent process decision.

## Completion

- Added `tools/check_governance.py` and three focused regression tests.
- Added CI for governance audit, Ruff, pytest, and `git diff --check`.
- Archived the completed M34 handoff and recorded ADR-0039 plus the governance
  audit runbook.
- Focused audit/tests and Ruff passed; full pytest and diff validation are the
  final completion checks.

## Out of scope

Harness code, case assets, corpus manifests, provider settings, hosted calls,
runtime prompts, helpers, IR, SDK, and external data.
