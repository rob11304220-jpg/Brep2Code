# ADR-0058: Remediate M97 Before Any Further Parameter-Variation Calibration

- **Status**: Accepted
- **Date**: 2026-08-10

> Historical decision snapshot. M97-003 and M97-004 subsequently completed;
> current M97/M98 routing is in
> [`four-track-program-roadmap.md`](../v1/four-track-program-roadmap.md) and
> [`docs/workflow/status.md`](../../workflow/status.md).
- **Context**: M97-001 used three hosted requests but did not produce a valid card/no-card calibration. Its actual provider context was generic `probe_summary`, not the frozen M96 measured-fact transcript; it omitted the low-row cylinder centre and radius. The card condition then generated an unsupported `OCP.gp.gp_DZ` import and a default `x=15` construction, while the next baseline request timed out. No baseline outcome exists.

## Decision

Insert M97-002, an offline G2 remediation, before any further G3 parameter-variation calibration. It must make the actual outbound context equal the M96 measured-fact contract, assert that contract before issuance, and verify a versioned supported OCP through-cut recipe and import-symbol failure classification. A future hosted calibration is a new workpack that re-freezes prompt/card/index hashes, CLI policy, deadline and paths, then obtains a separate preflight and itemized authorization. M98 remains blocked.

## Rationale

The existing evidence cannot estimate a card effect: it lacks both compliant parameter input and a baseline result. Reusing the report, remaining capacity, policy or authorization would turn a classified failure into an uncontrolled retry. Offline conformance testing is the smallest bounded change that can separate an implementation error from a provider/model result without inspecting held-out rows.

## Consequences

- **Positive**: future outbound contexts are auditable against the declared facts, and incompatible OCP symbols are classified earlier.
- **Negative**: any corrected prompt/card/recipe changes the experiment and invalidates direct comparison with M97-001.
- **Mitigation**: use only development rows in M97-002; freeze and authorize a later G3 package as a new experiment; retain M97-001 as counterexample evidence only.

## Alternatives Considered

| Alternative | Reason not selected |
|---|---|
| Continue M97-001 with its six unissued requests | The terminal report and authorization explicitly prohibit capacity reuse. |
| Run M98 held-out rows next | M97-001 did not produce a valid development comparison, and held-out tuning is prohibited. |
| Treat the failed card condition as a model result | The missing measured facts and invalid OCP import confound that interpretation. |
