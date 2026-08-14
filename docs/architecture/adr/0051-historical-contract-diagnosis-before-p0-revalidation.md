# ADR-0051: Historical Contract Diagnosis Before P0 Revalidation

- **Status**: Accepted
- **Date**: 2026-08-10

## Context

M72's first authorized CAD observation request reached its 300-second provider
deadline after `http_started`. Its stopping rule correctly prevents retrying,
expanding samples, or entering M73. The existing M73--M78 route assumes M72
stability passes, but the next useful question is whether a measurable current
request contract differs from earlier bounded hosted evidence.

Historical privacy boundaries intentionally do not retain raw prompts or full
responses, so an exact textual replay cannot be claimed.

## Decision

Insert two bounded workpacks before M73:

1. M79 is an offline G2 historical-contract and drift diagnosis. It produces a
   reviewed structural equivalence/difference/unknown matrix and one frozen
   reproduction profile without issuing a provider request.
2. M80 is a G3 paired minimal P0 end-to-end revalidation. It may run only after
   M79, a new preflight, and itemized authorization. It runs a fixed provider
   control followed by one `box` B-Rep observation-to-STEP path, with one
   request each, durable monitors, no repair and fail-closed stopping.

M73's activation prerequisite changes from M72 stability success to M80's
minimal end-to-end gate. M76 re-baselines all P0 cases after M73, so its `box`
run remains a fresh post-contract-change baseline rather than a reused M80
result.

## Consequences

- **Positive**: Separates historical-drift diagnosis, provider lifecycle, and
  CAD correctness; establishes a narrow evidence gate for a simple B-Rep to
  generated-script to verified STEP path.
- **Negative**: M73--M78 are delayed and M80 cannot support a broad provider
  stability or model-quality claim.
- **Mitigation**: M79 records unknown fields explicitly; M80 retains existing
  preflight, one-request accounting, `wsl-bwrap`, atomic report and no-retry
  constraints.

## Alternatives Considered

| Alternative | Rejection reason |
|---|---|
| Start M73 after M72 timeout | Mixes output correctness with unresolved provider lifecycle behavior. |
| Put historical replay into M76--M78 | Conflates forward P0/P1 evaluation with diagnostic reproduction and bypasses their dependencies. |
| Retry M72 or expand its cases | Violates its fixed budget and stopping rule. |
