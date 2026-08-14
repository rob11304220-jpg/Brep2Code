# WP-TRG-032: Agent Entry and Document Routing

- Status: deferred
- Owner: unassigned
- Reviewer: not required
- Risk tier: G1

## Entry condition

`WP-TRG-031` is complete and independently reviewed or explicitly accepted,
and the user selects this package.

## Goal

Make `AGENTS.md`, `README.md`, and document routing guide humans and coding
agents to the appropriate theory, pipeline, governance, and workflow entry for
their task.

## Scope

- Add task-type routing that distinguishes theory/experiment design,
  Harness/runtime changes, case/governance work, workflow selection, and hosted
  requests.
- Require new case, code, or evaluation proposals to name a relevant M146
  `hypothesis_id` (or explicitly state why none applies), Q01--Q04 decision,
  evidence role, counterexample, stop rule, and adoption boundary where
  applicable.
- Route theory questions to the crosswalk, system behavior to the Q01--Q04
  pipeline/contracts, asset facts to case/governance authorities, and task
  selection to `status.md` and an active workpack. A crosswalk link is never
  an implementation or authorization route.
- Preserve `status.md` as execution authority and source records as field-level
  authorities.

## Compatibility constraints

Routing documentation cannot grant implementation, case-production, provider,
runtime, or hosted authority. It must continue to require the existing
workpack lifecycle and G3 authorization rules.

## Acceptance

```powershell
uv run python tools\check_governance.py
python tools\audit_development_evidence_crosswalk.py
git diff --check
```

## Out of scope

Theory-map content changes, case alignment, code changes, new runtime resources,
and hosted work.
