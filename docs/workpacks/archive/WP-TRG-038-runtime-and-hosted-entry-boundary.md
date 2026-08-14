# WP-TRG-038: Runtime-and-Hosted Entry Boundary

- Status: archive-only (consumed by M155; see docs/workflow/workpack-route-disposition-index.md)
- Owner: unassigned
- Reviewer: independent reviewer required
- Risk tier: G2

## Entry condition

`WP-TRG-037` is complete and independently reviewed or explicitly accepted,
and the user selects this package.

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

## Out of scope

Runtime projection implementation, campaign preflight, provider execution,
budget/deadline requests, and hosted result interpretation.
