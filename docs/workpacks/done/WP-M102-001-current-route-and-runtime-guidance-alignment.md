# WP-M102-001: Current Route and Runtime Guidance Alignment

- Status: done
- Milestone: M102
- Owner: Codex
- Reviewer: not required (G1)
- Risk tier: G1

## Goal

Remove current-documentation noise that contradicts the completed M19 guidance
bridge, M97-003/004 route state, or current provider-integration governance,
while preserving historical evidence and all runtime/provider boundaries.

## Scope

- Correct runtime-resource, experience-card and guidance-runbook descriptions
  of the explicit opt-in M19-003 bridge and default no-card behavior.
- Correct current roadmaps, workpack navigation and parameter-variation design
  pages that still describe M19 or M97-003 as future/backlog.
- Clarify the generic G3 provider-workpack rule without changing provider
  behavior, dependencies or authorization.
- Add current-status navigation to selected completed historical records only;
  do not rewrite their original conclusions.

## Attribution question and sampling intent

Distinguish inaccurate current routing from valid historical evidence. Stop
after the documented state agrees with completed workpacks, code/module
documentation and `status.md`; do not sample, reinterpret reports or change a
technical contract.

## Inputs

- M19-002/M19-003 and M97-003/M97-004 completed workpacks
- current runtime guidance code/module docs, four-track route and status page

## Code paths

None. Documentation/rule wording only.

## Docs to update

- `runtime_resources/README.md`, `runtime_resources/experience-cards/README.md`
- the bounded cylinder experience card and runtime-guidance runbook
- current routes/navigation, selected historical navigation banners, and the
  Python-domain rule
- `docs/workflow/status.md`, this workpack and active handoff

## Trace/schema changes

None. No runtime-resource, card, report, trace, policy, CLI or manifest schema
change.

## Decision-package impact

- `decision_id`: none; documentation/rule alignment only.
- Q01/Q02 effect: no observation, card-selection, prompt or sequence change.
- Q03/Q04 effect: no gate, sandbox, diagnostic or repair change.
- Evidence role: navigation and boundary correction only.
- Knowledge disposition: no reusable knowledge change.

## Compatibility constraints

The guidance bridge remains explicit, revision-scoped, hash-bound and absent
by default. Existing card contents, runtime behavior, provider/model choices,
M98 policy, report budgets and all hosted authorization requirements remain
unchanged.

## Acceptance

```powershell
uv run python tools\check_governance.py
git diff --check
```

## Evidence reuse / guidance-card disposition

No card is promoted, broadened or semantically changed. Wording may clarify
the existing opt-in bridge and default-disabled state only.

## Status transition

After acceptance, update `status.md` first, move this workpack to `done/`,
archive the active handoff, and leave future packages unselected.

## Closure rationale

- Corrected current runtime-resource, experience-card and guidance-runbook
  wording to document the completed M19-003 explicit bridge and default
  no-card behavior. The hash-pinned cylinder card itself remains byte-stable;
  the README now directs agents to the current bridge boundary.
- Updated current M19 and M97/M98 route text, corrected stale workpack
  navigation, and added historical-snapshot navigation to ADR-0058 and the
  completed M21 review.
- Replaced the completed-M3-004-specific Python rule with a generic
  user-selected G3 provider-integration boundary.
- Acceptance on 2026-08-11: `uv run python tools/audit_runtime_guidance.py`,
  `uv run python tools/check_governance.py`, and `git diff --check` passed.
  No code, card content, runtime behavior, provider setting, policy, manifest
  or hosted request changed.

## Out of scope

Code, card applicability/evidence, runtime retrieval behavior, provider SDKs,
hosted preflight/request, M98 selection, held-out inspection, policy/manifest
or report changes.
