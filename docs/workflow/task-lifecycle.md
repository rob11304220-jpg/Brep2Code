# Task Lifecycle and Risk Tiers

`status.md` is the current-state authority. A workpack scopes and accepts one
bounded change; a handoff preserves resumable context. Neither a backlog item
nor an evidence-ledger record authorizes implementation, runtime changes, or
hosted requests.

## States

`backlog → active → review → done` is the normal path. `blocked` and
`deferred` retain the blocker or re-entry condition instead of silently
remaining active. The repository currently stores review work inside the
active workpack; its reviewer and closure rationale make that transition
explicit without adding a second active directory.

## Required active-workpack fields

Every active workpack declares `Status`, `Milestone`, `Owner`, `Risk tier`,
scope, compatibility constraints, acceptance commands, out-of-scope items,
an owner-completion boundary, permitted stop conditions, and a status-transition plan. G2 and G3 also declare an independent
`Reviewer`. An active handoff names its related workpack.

| Tier | Change class | Minimum closure gate |
|---|---|---|
| G0 | prose-only correction with no behavioral claim | owner and `git diff --check` |
| G1 | governance, rules, workflow, or documentation convention | owner, governance audit, focused checks |
| G2 | shared code, Harness, corpus, gate, schema, or manifest | independent reviewer, governance audit, Ruff, relevant tests |
| G3 | provider, hosted egress, external data, credentials, or runtime authority | G2 gates, hosted preflight, and explicit user authorization |

The reviewer must not be the owner. They verify scope, evidence boundaries,
acceptance output, and status/handoff alignment; they do not grant provider or
runtime authority.

## Continuous owner execution

After the user selects an active workpack, its owner continues through all
in-scope owner-side work until the recorded owner-completion boundary is met.
Permitted stop conditions are only independent review, explicit external or
hosted authorization, frozen-input drift, an out-of-scope dependency, or a
reproducible blocker. Planning, workpack creation, partial implementation, and
partial validation are not stop conditions. This continuity does not select a
successor workpack or relax G3 authorization.

## Validation planning

Before running acceptance, select independently bounded commands using the
[offline validation planning runbook](../runbooks/offline-validation-planning.md)
and the current M53 duration baseline. A workpack must not concatenate
redundant long test selections under one outer deadline. Record each terminal
result; a command-window timeout is neither a passing nor failing test result.

## Closure

Close only after recording the acceptance output or artifact paths and a brief
closure rationale in the workpack. Update `status.md` first, then the
workpack and handoff. Archive a completed handoff when no active workpack
remains.
