# WP-M10-011: Attribution Ledger and Repair Governance

- Status: done
- Milestone: M10
- Owner: unassigned

## Goal

Establish the document-only cumulative attribution ledger and routing procedure that make external sampling serve a stated attribution question or minimal repair hypothesis.

## Trigger condition

`WP-M10-010` is completed with its deterministic 2/1 admission, verified ignored local cache, and offline controls.  This workpack does not reopen or enlarge M10-010.

## Scope

- Verify and publish the initial six-case ledger from M10-005/M10-008 completed evidence.
- Apply ADR-0010 to the evidence-gated roadmap, case-corpus review runbook, and workpack template.
- Register exactly one next candidate workpack from the ledger; the current candidate is the minimal offline sandbox-path/trace experiment.
- Record the development-only and independently authorized held-out boundary for any later hosted policy comparison.

## Compatibility constraints

- No provider request, external download, code, fixture, manifest, prompt/context, probe, gate, report schema, or runtime behavior change.
- Existing reports and revision traces remain the authoritative case evidence; the ledger stores only sanitized derived findings.
- Default commands remain offline and credential-free.

## Acceptance

- The ledger covers every completed M10-005/M10-008 external case with the required fields and only trace-supported `direct` classifications.
- Route selection records the attribution question, expected information gain, and stopping condition; it does not select unbounded corpus growth.
- Documentation, status, handoff, and indexes consistently name ADR-0010 and the next selected workpack.
- Documentation links resolve; no public runtime interface changes.

## Status transition

On activation, move this file to `active/` only after M10-010 is completed.  On completion, update status, handoff, the workpack index, ledger, roadmap, and any selected successor workpack.

## Completion

The ledger review confirmed that `00000027` and `00000031` are two `direct`, trace-supported instances of the same sandbox input-path mechanism.  This meets ADR-0010's two-case minimal offline experiment threshold, but not the three-case narrow-helper threshold.  `WP-M10-012` was selected and completed offline; see [its review](../../architecture/v1/m10-012-minimal-offline-path-repair-review.md).

## Out of scope

Executing a repair experiment, changing production behavior, hosted policy comparison, held-out execution, narrow helper implementation, geometry diagnostics, IR, SDK, or benchmark claims.
