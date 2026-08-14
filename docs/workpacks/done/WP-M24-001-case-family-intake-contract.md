# WP-M24-001: Reusable Case-Family Intake Contract

- Status: done
- Milestone: M24
- Owner: Codex

## Goal

Turn the M20--M23 case-library expansion lessons into a reusable offline
contract that future development agents can apply before producing a new
sequence-paired family.

## Scope

- Add a copyable preregistration template and a generic contract audit.
- Add focused tests and a maintenance runbook section.
- Record the lasting governance decision in ADR-0026.

## Compatibility constraints

Default operation remains offline and credential-free. Existing family records,
specialized audits, case lifecycle, manifests, provider boundaries, and runtime
behavior remain unchanged.

## Acceptance

- [x] Generic audit accepts a complete M23-shaped frozen record and rejects
  split leakage, missing negative evidence, and duplicate operation IDs.
- [x] Runbook specifies the design, production, review, and promotion gates.
- [x] No candidate, manifest, provider, training, or runtime path changes.

## Evidence reuse / guidance-card disposition

No runtime experience card: the result is development-governance procedure,
not three independent direct runtime mechanism cases.

## Status transition

Updated workflow status, this completed workpack, ADR-0026, the maintenance
runbook, corpus entry documentation, and the active handoff.

## Out of scope

No M23 promotion, new family selection, external-data admission, generic
geometry audit, IR, parser/helper/SDK change, or hosted request.
