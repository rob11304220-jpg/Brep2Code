# ADR-0071: Stratify Case Admission Evidence Before Runtime Projection

- **Status**: Accepted
- **Date**: 2026-08-12

## Context

M142 validates one immutable admission record for the selector-ambiguity
mechanism. The existing library contains several modeling families and
evidence roles, but a raw inventory or a single pilot must not be mistaken for
a uniform admission standard or a runtime-knowledge authorization.

## Decision

Insert deferred `WP-TRG-029` after independently reviewed M142 and before
selection of `WP-TRG-028`. When explicitly selected, it will create a
development-side `admission-profile-v1` from existing authoritative metadata
and reviewed evidence. The profile classifies mechanism, reference stability,
dependency, split role, evidence maturity, and admission risk. It defines
minimum evidence and fail-closed conditions but does not admit assets,
override their lifecycle, or create runtime knowledge.

Individual immutable admission records remain the authority for case
admission. `WP-TRG-028` may only be selected after the reviewed profile
crosswalk and still derives and evaluates at most one minimal projection from
one reviewed record.

## Consequences

- Future admission pilots can be selected by an explicit decision gap and
  stated evidence deficit rather than by case count or an informal difficulty
  label.
- Existing held-out and split boundaries remain intact: the stratification is
  metadata/evidence-link based and cannot cause new inspection or execution.
- The route adds a G2 review gate before projection and makes no provider,
  runtime, manifest, retrieval, SDK, IR, or training change.
