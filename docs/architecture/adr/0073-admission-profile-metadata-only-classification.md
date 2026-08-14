# ADR-0073: Classify Admission Evidence from Metadata Without Promoting Assets

- **Status**: Accepted
- **Date**: 2026-08-12

## Context

After M142, the library needs a way to compare mechanism-specific admission
evidence before considering any projection. A raw case count or informal
difficulty ladder would conceal selector ambiguity, split role, and evidence
maturity. M143 must also retain held-out isolation.

## Decision

Adopt `admission-profile-v1` as a metadata-only development-side crosswalk.
It classifies active self-authored records across modeling mechanism,
entity-reference stability, sequence dependency, parameter/split role, evidence
maturity, and admission risk. It defines four dispositions: `admit`,
`needs_evidence`, `fail_closed`, and `counterexample_only`.

Only an independently reviewed immutable admission record may support `admit`
for its exact scope. The profile maps M142's unique planar selector to that
bounded disposition and its twin-boss ambiguity to `fail_closed`. The audit
may read registry and `case.json` metadata plus reviewed documentary sources;
it must not open fixtures or scripts, or inspect held-out content.

## Consequences

- The inventory can expose lifecycle/split metadata drift before it is used as
  evidence; M144 reconciled the known ADR-0023 lifecycle declarations.
- Future pilots are selected by stated decision gaps and missing evidence, not
  by profile counts.
- The profile cannot change case lifecycle, admission, manifest, runtime,
  retrieval, SDK/IR, provider, training, or hosted authority.
