# WP-M151-001: Successor Contract and Egress-Boundary Alignment

- Status: done
- Milestone: M151
- Owner: Codex
- Reviewer: not required (G1)
- Risk tier: G1

## Goal

Align deferred TRG-034 and TRG-035 with the completed M146 crosswalk and M150
case-evidence relationship layer, making implementation completeness and
egress-safe reference-projection gates explicit.

## Scope

- Require TRG-034 to freeze M146/M150 provenance and select only one hypothesis
  with a complete Q01--Q04 chain; otherwise stop for a new offline package.
- Require TRG-035 to consume a separately reviewed, hash-pinned egress-safe
  reference projection. M146/M150 documentation remains provenance and cannot
  itself be sent to a provider.
- Preserve all deferred/user-selection, G2/G3 review, preflight, and itemized
  hosted-authorization gates.

## Decision-package impact

- `decision_id`: none; changes deferred wording only.
- Q01/Q02 and Q03/Q04 effects: none.
- Evidence role: governance/navigation alignment only.
- Knowledge disposition: no runtime or egress authorization.

## Compatibility constraints

Do not activate TRG-034/035/028, modify the crosswalk or relationship mapping,
or change case metadata, manifests, Harness, provider, runtime, or hosted
configuration.

## Acceptance

```powershell
python tools\audit_case_evidence_relationships.py
python tools\audit_development_evidence_crosswalk.py
uv run python tools\check_governance.py
git diff --check
```

## Owner completion boundary

Publish aligned deferred definitions and record the unchanged authority boundary
in the active handoff.

## Closure rationale

Completed on 2026-08-13. TRG-034 now requires M146/M150 provenance, a complete
Q01--Q04 chain, and explicit implementation status. TRG-035 now requires a
separately reviewed, hash-pinned egress-safe reference projection; crosswalk
and case-evidence documents are provenance only. Both relationship audits,
governance audit, and `git diff --check` passed. No successor was activated.

## Permitted stop conditions

User review; source-authority conflict; or a required change outside deferred
route documentation.

## Status transition

Update status first, then workpack and handoff. On closure archive the handoff;
do not activate a successor.

## Out of scope

Implementation-contract code alignment, reference projection creation, hosted
preflight, provider request, or runtime projection.
