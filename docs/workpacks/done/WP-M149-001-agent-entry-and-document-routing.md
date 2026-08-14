# WP-M149-001: Agent Entry and Document Routing

- Status: done
- Milestone: M149
- Trigger consumed: `WP-TRG-032`
- Owner: Codex
- Reviewer: not required (G1)
- Risk tier: G1

## Entry condition

M148 is complete and the user selected TRG-032. The M146 crosswalk and M148
theory map are the existing development-side theory-navigation layer.

## Goal

Route humans and coding agents to the appropriate theory, system/runtime,
evidence-asset, workflow, and hosted materials for their task without changing
any source authority or authorization boundary.

## Scope

- Add concise task-type routing to `AGENTS.md`, `README.md`, and
  `docs/workflow/README.md`.
- Require new case, code, or evaluation proposals to identify a relevant M146
  `hypothesis_id`, or explicitly state why none applies, plus the applicable
  Q01--Q04 decision, evidence role, counterexample, stop rule, and adoption
  boundary.
- Preserve `status.md` as the only execution authority and existing G3 hosted
  authorization/preflight requirements.

## Decision-package impact

- `decision_id`: none; M149 changes entry routing only.
- Q01/Q02 and Q03/Q04 effects: none.
- Evidence role: navigation and proposal-scoping only.
- Knowledge disposition: no runtime knowledge, case disposition, or authority
  transfer.

## Compatibility constraints

Routing documentation cannot grant implementation, case-production, runtime,
provider, or hosted authority. Do not alter crosswalk source hashes or
relationships, case metadata, registry, manifests, Harness behavior, or
runtime/provider configuration.

## Acceptance

```powershell
python tools\audit_development_evidence_crosswalk.py
uv run python tools\check_governance.py
git diff --check
```

## Owner completion boundary

Publish concise task-type routing and proposal fields in all three entry
documents, record the authority boundary in the active handoff, and pass
acceptance.

## Closure rationale

Completed on 2026-08-13. `AGENTS.md`, `README.md`, and
`docs/workflow/README.md` now share a task-type routing model for theory,
system/runtime, evidence assets, work selection, and hosted requests. New
proposals record a relevant hypothesis ID or explicit non-applicability, plus
bounded decision/evidence fields where applicable. Crosswalk audit, governance
audit, and `git diff --check` passed. No source authority or execution scope
changed.

## Permitted stop conditions

User review; source-authority conflict; or a required case, code, runtime, or
hosted change outside routing documentation.

## Status transition

Update `docs/workflow/status.md` first, then this workpack and active handoff.
On closure, archive the handoff; do not activate a successor.

## Out of scope

Theory-map content, case-evidence alignment, implementation-contract/code
changes, runtime projection, provider use, and hosted evaluation.
