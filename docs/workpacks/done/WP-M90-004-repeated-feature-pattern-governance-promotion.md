# WP-M90-004: Repeated-Feature Pattern Governance Promotion

- Status: done
- Milestone: M90
- Owner: unassigned
- Reviewer: Liaol (independent)
- Risk tier: G2

## Goal

If M90-003 recommends it, promote the exact reviewed six-case family into the
governed self-authored library under a new narrow ADR.

## Activation condition

M90-003 must be independently approved with a family-scoped promotion proposal.

## Scope

Update only lifecycle metadata and development-side governance/knowledge
references. Keep cases out of executable manifests and runtime resources.

## Compatibility constraints

No provider, hosted request, manifest, Harness, training or runtime change.

## Acceptance

Run family audit, case-library replay audit, Ruff, governance audit,
`git diff --check`, and independent review.

## Evidence reuse / guidance-card disposition

Governed family-scoped library evidence only; no runtime experience card.

## Status transition

Update status, write the required ADR, close and archive after independent review.

## Out of scope

Manifest admission, hosted evaluation, provider stability claims or generic pattern claims.

## Result and independent review

ADR-0055 promotes exactly the reviewed six records on 2026-08-10. Case
metadata, reference scripts, candidate sequences and registry pointers are
present; all remain out of executable manifests and runtime resources. Liaol
approved the scoped G2 promotion after replay, family and governance checks.
