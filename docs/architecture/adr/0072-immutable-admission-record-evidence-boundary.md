# ADR-0072: Keep Admission Records Immutable and Evidence-Only

- **Status**: Accepted
- **Date**: 2026-08-12

## Context

M142 needs a reviewable record that binds a bounded selector mechanism to its
source evidence without treating a replayable asset, held-out control, or
modeling sequence as runtime knowledge.

## Decision

Adopt immutable admission-record v1. The selector-ambiguity pilot binds its
decision, preregistration, production review, observable, repair policy, and
development oracle/control with SHA-256. Held-out evidence is documentary and
hash-pinned only; the auditor must not read, hash, replay, or execute a
held-out fixture. The record states a stable fail-closed taxonomy and explicit
non-projection prohibitions.

## Consequences

- Review can pin the exact record digest and detect source drift locally.
- A reviewed record can support a later user-selected decision but cannot
  promote a case or authorize manifest, runtime, retrieval, provider, or
  hosted use.
- Future records need a new version or independently reviewed revision when
  their source evidence or scope changes.
