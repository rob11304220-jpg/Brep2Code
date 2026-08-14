# WP-M61-001: Validation Execution Planning

- Status: done
- Milestone: M61
- Owner: Codex
- Risk tier: G1

## Goal

Make the repository's M53 test markers, measured duration baseline, and
command-window discipline part of the standard workpack validation plan, so
agents obtain rapid feedback without accidentally serializing redundant long
test selections into one command deadline.

## Scope

- Turn the existing `fast`, `standard`, and `sandbox` marker definitions and
  M53 measured baseline into a short repeatable validation-planning procedure.
- Define the order: fast plus changed-area tests during implementation; a
  relevant sandbox selection only when it adds information; one final full
  suite rather than a redundant standalone sandbox run immediately before it.
- Require independently bounded commands with recorded results and an explicit
  response when observed duration exceeds the baseline.
- Add a validation-planning reference to the workpack creation/lifecycle path.

## Compatibility constraints

Documentation and workflow convention only. Do not change test behavior,
markers, dependencies, CI configuration, Harness/runtime behavior, provider
policy, hosted authorization, or corpus inputs.

## Acceptance

```powershell
uv run python -m pytest -m fast -q
uv run python tools\check_governance.py
git diff --check
```

## Status transition

Record the updated procedure, observed validation outputs, owner acceptance,
and closure rationale before archiving.

## Owner acceptance

- Added [`offline-validation-planning.md`](../../runbooks/offline-validation-planning.md), which routes marker-based feedback, process-boundary checks, full-suite final gates, independent command windows, and timeout reporting.
- Linked the planning rule from `task-lifecycle.md`, making M53's baseline and
  no-redundant-long-command rule part of workpack acceptance planning.
- Offline acceptance passed on 2026-08-09:
  - `uv run python -m pytest -m fast -q` — 58 passed, 111 deselected in 5.02s
  - `uv run python tools\check_governance.py` — passed
  - `git diff --check` — passed

## Closure rationale

M61 completed the bounded G1 workflow objective without changing test behavior
or relaxing any G2 gate. It records command windows and overlapping-suite
discipline so a timeout cannot be mistaken for a test outcome.

## Out of scope

Benchmarking, performance optimization, parallel test execution, changing
test markers, relaxing G2 quality gates, or treating a command timeout as a
test result.
