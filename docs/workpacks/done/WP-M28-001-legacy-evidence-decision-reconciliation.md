# WP-M28-001: Legacy Evidence and Decision Reconciliation

- Status: done
- Milestone: M28
- Owner: Codex

## Goal

Reclassify existing development evidence into the ADR-0035 Harness decision
base without changing cases, executable manifests, Harness behavior, provider
policy, runtime retrieval, or training inputs.

## Scope

- Maintain the legacy-evidence disposition index and backfill the bounded M10
  fixed-script execution unit.
- Add implementation-side decision packages for literature-supported gaps that
  are not already represented.
- Reconcile coverage, architecture entry points, current status, and handoff.

## Decision-package impact

- `decision_id`: reconciliation of all current packages; add planned Q01/Q03/Q04 packages.
- Q01/Q02 effect: classify existing cases without treating feature labels as knowledge.
- Q03/Q04 effect: preserve the M10 fixed-script diagnostic as a bounded execution boundary.
- Evidence role: inventory-only; no new oracle, control, regression, OOD, or native-history asset.
- Knowledge disposition: reviewed unit, reviewed boundary, or retained no-reusable-knowledge entry for every legacy evidence family.

## Compatibility constraints

Default execution remains offline. No case lifecycle, fixture, manifest,
provider, runtime-resource mount, prompt, helper, IR/SDK, gate, trace, schema,
or CLI behavior changes.

## Acceptance

- Every existing evidence family has one disposition in
  `docs/corpus/knowledge/evidence-disposition.json`.
- Every planned research gap has one decision package with a compatible
  workpack trigger or is explicitly deferred.
- JSON files parse; documented links resolve; `git diff --check` passes.

## Evidence reuse / guidance-card disposition

No new runtime card. Existing cards gain only a development-side source link
through the disposition index and remain experimental.

## Completion

- Added ADR-0036 and `evidence-disposition.json` with explicit dispositions
  for the M20--M27 units, pre-M20 self-authored assets, external controls,
  M10 fixed-script evidence, and M19 card foundation.
- Added a bounded Q03/Q04 execution unit for the M10 sandbox-path result.
- Added or reconciled planned decision packages for blind/through
  observability, independent editability validation, and sequence rollback;
  local geometry feedback is explicitly deferred because WP-M10-002 remains
  ineligible.
- Updated coverage, knowledge/architecture indexes, maintenance procedure,
  status, and handoff. JSON parsing and `git diff --check` passed.

## Status transition

Update the knowledge index, coverage matrix, architecture entry point, status,
and active handoff. ADR-0036 records the lasting governance rule.

## Out of scope

Selecting or producing a new case family, changing M10-002's eligibility by
fiat, runtime retrieval, hosted evaluation, or any executable behavior.
