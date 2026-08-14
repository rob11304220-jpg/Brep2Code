# WP-M148-001: Project Theory Map and Document Navigation

- Status: done
- Milestone: M148
- Trigger consumed: `WP-TRG-031`
- Owner: Codex
- Reviewer: not required (G1)
- Risk tier: G1

## Entry condition

M146's source-linked crosswalk is independently reviewed, M147 aligned the
deferred successor definitions, and the user selected TRG-031.

## Goal

Publish one compact project-level theory map that makes the development
knowledge system the primary human and Agent entry for verified and unknown
bounded B-Rep-to-modeling-sequence hypotheses.

## Scope

- Add one derived theory-map entry that reuses the M146 crosswalk's five views
  without repeating their contents or creating a new registry.
- Route readers in order from theory navigation to system/runtime architecture,
  evidence-asset management, and current workflow status.
- Add only stable links from the architecture overview and v1 navigation index.

## Decision-package impact

- `decision_id`: none; M148 adds navigation only.
- Q01/Q02 and Q03/Q04 effects: none.
- Evidence role: source-linked documentary navigation only.
- Knowledge disposition: no runtime knowledge, case disposition, or authority
  transfer.

## Compatibility constraints

The crosswalk, pipeline, case/governance records, and `status.md` retain their
existing authorities. Do not change `AGENTS.md`, case metadata, registry,
manifests, Harness/runtime behavior, provider configuration, or hosted scope.

## Acceptance

```powershell
python tools\audit_development_evidence_crosswalk.py
uv run python tools\check_governance.py
git diff --check
```

## Owner completion boundary

Publish the theory map, add its stable entry links, record the navigation and
authority boundary in the active handoff, and pass the acceptance commands.

## Closure rationale

Completed on 2026-08-13. Added `docs/architecture/v1/project-theory-map.md`
and linked it from the architecture overview and v1 index. The map routes
theory, system/runtime, evidence-asset, and current-task questions to their
existing authorities, while linking rather than duplicating M146's five views.
The crosswalk audit, governance audit, and `git diff --check` passed. No Agent,
case, runtime, provider, or hosted authority changed.

## Permitted stop conditions

User review; source-authority conflict; or a required Agent-routing, case,
runtime, or hosted change outside this package.

## Status transition

Update `docs/workflow/status.md` first, then this workpack and active handoff.
On closure, archive the handoff; do not activate a successor.

## Out of scope

Agent entry routing, case-evidence alignment, implementation-contract/code
changes, runtime projection, provider use, and hosted evaluation.
