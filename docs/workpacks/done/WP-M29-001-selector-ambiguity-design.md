# WP-M29-001: Selector-Ambiguity Pair Design and Preregistration

- Status: done
- Milestone: M29
- Owner: Codex

## Goal

Freeze the smallest Q01 discriminating design that compares the existing
unique planar-face selector with a same-predicate, two-candidate fail-closed
control.

## Scope

- Reuse `face-selected-dependent-cut-v1` as the fixed unique-selector oracle.
- Preregister one centered development and one offset held-out twin-boss row.
- Freeze selector predicate, measurement convention, candidate cardinality,
  wrong-face and coordinate-tie-breaker negative controls, mutations, and
  rejection taxonomy.
- Create M29-002 only as a future separately selectable production proposal.

## Decision-package impact

- `decision_id`: `q01-selector-ambiguity-v1`.
- Q01/Q02 effect: cardinality is a measured selector fact; exactly one permits
  the bounded action and any other count stops before a dependent operation.
- Q03/Q04 effect: ambiguity is a fail-closed diagnostic, not a repair target.
- Evidence role: fixed oracle, discriminating control, and negative control.
- Knowledge disposition: planning evidence only; no observable unit is reviewed
  until controlled production and audit complete.

## Compatibility constraints

Offline-only. No asset, producer, registry, manifest, provider, training,
runtime, prompt, parser/helper/SDK, IR, gate, or CLI change.

## Acceptance

- The preregistration names every proposed row and preserves family-isolated
  splits.
- The unchanged predicate has cardinality one for the existing oracle and two
  for both planned controls; no tie-breaker is permitted.
- The negative controls require rejection before any downstream operation.
- JSON parsing and `git diff --check` pass.

## Evidence reuse / guidance-card disposition

No runtime experience card. This design is not evidence of runtime selector
behavior, persistent naming, or generic face recovery.

## Completion

- ADR-0037 and `selector-ambiguity-v1-preregistration.json` freeze the
  unchanged predicate, two family-isolated twin-boss rows, and required
  wrong-face/coordinate-only negative controls before any asset production.
- The generic sequence-paired intake auditor passed. No candidate directory,
  producer, registry, manifest, or runtime behavior was created or changed.
- M29-002 is recorded only as a separately selectable controlled-production
  proposal.

## Status transition

Update the decision package links, coverage matrix, status, handoff, and ADR.
Move this workpack to `done/` only after design validation; M29-002 remains a
separate future selection.

## Out of scope

Candidate production, selector implementation, selecting one ambiguous face,
dependent cuts on twin bosses, active-library admission, hosted evaluation, and
runtime changes.
