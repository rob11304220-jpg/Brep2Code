# WP-M29-002: Selector-Ambiguity Controlled Production

- Status: done
- Milestone: M29
- Owner: unassigned

## Goal

Produce and audit only the two frozen `selector-ambiguity-v1` twin-boss
candidate rows, testing that the unchanged selector stops at cardinality two.

## Trigger condition

M29-001 is complete and this workpack is explicitly selected under the
existing offline case-governance authorization. The preregistration hash,
row count, split isolation, and no-substitution rule must be rechecked before
candidate production.

## Scope

- Implement the candidate-only producer named in the preregistration.
- Produce each frozen row twice in clean directories and audit normalized STEP
  hash stability.
- Audit cardinality two before any dependent sketch/cut, and run the two
  required negative-control injections.
- Record a family-specific review that either creates a bounded Q01 observable
  unit/counterexample or records no reusable knowledge.

## Decision-package impact

- `decision_id`: `q01-selector-ambiguity-v1`.
- Q01/Q02 effect: test whether the unchanged predicate fail-closes at two
  candidates; no face is selected on the multi-candidate path.
- Q03/Q04 effect: retain ambiguity as a stop result, not a repair task.
- Evidence role: discriminating control and negative control; the existing
  face-selected family remains the unique-selector oracle.
- Knowledge disposition: decide after review only.

## Compatibility constraints

Offline-only. Candidate output remains experimental. Do not add a manifest,
provider input, training input, runtime resource, active case-library record,
selector helper, parser change, IR/SDK, gate, or CLI behavior.

## Acceptance

- Both frozen rows are hash-stable across clean-directory production.
- The predicate records cardinality exactly two in every twin-boss row.
- No selected-face-dependent sketch or cut is emitted after ambiguity.
- Wrong-face and coordinate-only injections are rejected.
- Existing unique oracle remains unchanged; JSON/audits and `git diff --check`
  pass.

## Evidence reuse / guidance-card disposition

No runtime experience card is expected. A passing fixed control cannot become
runtime selector guidance without independent direct runtime evidence.

## Completion

- Produced exactly two experimental candidates twice with stable normalized
  STEP hashes.
- Both rows recorded selector cardinality two and `ambiguous`; their frozen
  sequences stop before any dependent sketch or cut.
- Wrong-face and coordinate-only injections were rejected as preregistered.
- Focused tests (3), Ruff, intake audit, family audit, and `git diff --check`
  passed. The review created one bounded Q01 observable unit; candidates remain
  absent from the registry, manifests, provider, training, and runtime paths.

## Out of scope

Generic face selection, persistent naming, resolving an ambiguous target,
active-library promotion, manifest activation, hosted evaluation, and runtime
changes.
