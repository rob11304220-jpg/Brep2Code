# WP-M155-001: Runtime-and-Hosted Entry Boundary

- Status: done
- Milestone: M155
- Trigger consumed: `WP-TRG-038`
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

## Entry condition

M154 is complete and independently approved, and the user selected TRG-038.

## Goal

Freeze the entry boundary that any later runtime-projection or
hypothesis-to-hosted-evaluation route must satisfy before it may be selected.

## Scope

- State the required authority inputs for later runtime-projection and hosted
  routes: maintained authority map, reviewed implementation-contract status,
  source-linked evidence boundary, explicit prohibition list, and review
  trigger.
- Define what later routes must freeze separately rather than inherit by
  default, including runtime-projection form, egress-safe reference projection,
  campaign scope, and authorization text.
- Publish one compact boundary document that later `WP-TRG-028` and
  `WP-TRG-035` activations must cite before they may be selected.

## Decision-package impact

- `decision_id`: none; M155 defines route-entry conditions only.
- Q01/Q02 and Q03/Q04 effects: none.
- Evidence role: governance and route-entry boundary only.
- Knowledge disposition: no runtime, provider, manifest, or hosted authority
  change.

## Compatibility constraints

This package defines entry conditions only. It cannot create a runtime card,
reference pack, retrieval index, provider request, campaign charter, or hosted
authorization. It must preserve the distinction between development-side
knowledge, runtime projection, and provider-facing material.

## Acceptance

```powershell
uv run python tools\check_governance.py
python tools\audit_development_evidence_crosswalk.py
python tools\audit_case_evidence_relationships.py
git diff --check
```

## Owner completion boundary

Publish the compact runtime/hosted entry-boundary document, align route-facing
navigation to require it before later TRG-028/TRG-035 selection, and obtain
Liaol's independent G2 review.

## Current result

- Added
  `docs/architecture/v1/runtime-and-hosted-entry-boundary-v1.md` as the compact
  M155 entry-boundary record for later runtime-projection and
  hypothesis-to-hosted-evaluation selection.
- Froze one common pre-selection checklist: required authority inputs, later
  artifacts that must still be frozen separately, and inherited stop
  conditions.
- Updated deferred `WP-TRG-028` and `WP-TRG-035` so future activation packages
  must cite the M155 boundary document rather than implicitly inheriting route
  context.

## Validation record

Focused validation passed on 2026-08-13 with:

```powershell
uv run python tools\check_governance.py
python tools\audit_development_evidence_crosswalk.py
python tools\audit_case_evidence_relationships.py
git diff --check
```

`git diff --check` reported only existing LF/CRLF warnings.

## Independent review

- Liaol approved the independent G2 review on 2026-08-13.
- Review result: approved. The compact entry-boundary document, the explicit
  separation of later frozen artifacts, the deferred-route citation
  requirements, and the unchanged authority boundary were accepted without
  requesting any runtime or hosted capability widening.

## Closure rationale

M155 closes because the compact runtime/hosted entry-boundary document,
deferred-route wiring, validation record, and independent review are complete.
The work freezes only later selection conditions; it does not create any
runtime projection, provider-facing material, authorization text, or hosted
authority.

## Permitted stop conditions

Independent review; source-authority conflict; or a required runtime,
provider, hosted, or implementation change outside route-entry governance
documentation.

## Status transition

Update `docs/workflow/status.md` first, then this workpack and active handoff.
On closure, archive M155 and do not activate TRG-028 or TRG-035 automatically.

## Out of scope

Runtime projection implementation, campaign preflight, provider execution,
budget/deadline requests, and hosted result interpretation.
