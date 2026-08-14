# WP-M23-002: Additive-Boss-Dependent-Cut Controlled Production

- Status: done
- Milestone: M23
- Owner: unassigned

## Status transition

Selected by the user on 2026-08-05 after M23-001. This selection authorizes
only the frozen offline production and audit; it does not authorize a review,
promotion, manifest, provider, training, or runtime change.

## Goal

Produce and validate exactly the six preregistered
`additive-boss-dependent-cut-v1` candidates under the frozen M23-001 contract.

## Entry criteria

- M23-001 is completed and remains linked from workflow status.
- The user explicitly selects this workpack.

## Scope

- Produce only the six frozen rows with deterministic normalized STEP output
  and experimental candidate metadata.
- Audit geometry replay, exact sequence/dependency agreement, editability,
  boss/cut anti-degeneration invariants, hash stability, and split isolation.
- Retain stable rejection classes and negative controls.

## Acceptance

- Every candidate is generated twice into clean directories with byte-identical
  normalized STEP hashes.
- All six pass the scoped offline audit, or failures are retained without row
  replacement or grammar expansion.
- Focused tests, the family audit, Ruff, and `git diff --check` pass.

## Out of scope

Automatic admission, governance promotion, manifests, hosted evaluation,
training, runtime retrieval, face/edge references, parser expansion, helpers,
SDK, and IR.

## Result

Completed offline on 2026-08-05. The producer generated exactly the frozen six
experimental candidates and verified each twice in clean directories for
byte-identical normalized STEP output. All six passed the existing geometry
gates, exact six-operation dependency sequence, four editability mutations,
one-solid / base-extent / boss-height / blind-cut-volume invariants, and split
isolation. Focused tests passed 5, the family audit passed 6/6, Ruff and
`git diff --check` passed. The candidates remain unregistered and absent from
every manifest, provider, training, and runtime route.
