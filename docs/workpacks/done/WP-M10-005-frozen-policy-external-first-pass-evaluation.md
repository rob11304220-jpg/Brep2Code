# WP-M10-005: Frozen-Policy External First-Pass Evaluation

- Status: done
- Milestone: M10
- Owner: unassigned

## Goal

Produce split-preserving, bounded hosted first-pass evidence for the external manifests admitted by completed `WP-M10-003`, without changing the generation policy or treating the result as a benchmark.

## Trigger condition

`WP-M10-003` is completed and its selected development and held-out manifests have hash, input-probe, and `wsl-bwrap` offline-control evidence.  This workpack remains blocked until the caller separately authorizes each hosted split.

## Current evidence and authorization blocker

- M10-003 completed its deterministic 2-case development and 1-case held-out admission. All selected files hash-match and the two ignored `wsl-bwrap` controls completed with readable inputs/outputs and successful script exits; fixed-scaffold geometry failures are expected control evidence.
- Development preflight is complete: local `deepseek-v4-pro` configuration entry and `wsl-bwrap` availability are confirmed, the 2-case `--first-pass` budget maximum is 4 requests (`2 × (1 + 1)`), and `data/corpus-runs/abc-v00-m10-005-development-pro-authorized-20260802.json` is unused. No provider request was issued. The CLI source confirms a missing `--authorize-hosted` flag returns before configuration or network use; the environment safety layer declined an execution-path confirmation because it contained hosted arguments.
- The separately authorized development run completed as schema-v3 with the frozen policy and used 3/4 requests: one first-pass `provider_request`, one first-pass `script_failure`, and one repair pass. Held-out preflight now confirms its single selected hash, the same non-secret `deepseek-v4-pro` configuration, `wsl-bwrap`, one repair round, 120-second deadline, 2-request capacity, and an unused report path. It remains unauthorized and has issued no request.

## Scope

- Run the development manifest first using the unchanged provider/model, `first-pass-summary-v1` generation policy, `wsl-bwrap` executor, provider deadline, repair bound, case order, and existing gates.
- Freeze those conditions after the development review, then run the held-out manifest only under the same conditions.
- Before each split, complete the hosted preflight: verify input SHA-256, manifest membership, offline control, non-secret provider configuration, executor availability, CLI budget bound, and a new unused report path.
- Obtain separate explicit authorization for each split covering provider/model, bounded derived outbound content, case scope, rounds, provider deadline, and request or cost budget.
- Write completed schema-v3 reports and one sanitized review that reports the evidence funnel by split: readable inputs, provider responses, executable/readable outputs, geometry-gate passes, repair passes, requests issued, and duration.

## Inputs

- Completed `WP-M10-003` selection records, manifests, and offline controls.
- [Post-M9 roadmap](../../architecture/v1/post-m9-evidence-gated-roadmap.md).
- [Case corpus contract](../../architecture/v1/contracts/case-corpus.md).
- [LLM provider configuration runbook](../../runbooks/llm-provider-config.md).

## Code paths

- `brep2code/corpus/`
- `brep2code/agent/`
- `tests/test_corpus_m4.py`

## Docs to update

Create a sanitized evaluation review and update status, handoff, the workpack index, and the active handoff when this workpack changes state.  Update a runbook or contract only if the implementation changes a repeatable procedure or a documented interface.

## Trace/schema changes

None expected.  Use the existing schema-v3 separation of `primary_generation`, `repair`, and `fake_provider_replay`; the review derives its funnel from existing report fields and local traces.  Do not add full provider responses, credentials, environment snapshots, external reference scripts, or first-pass fixtures.

## Compatibility constraints

- Default commands remain offline and credential-free.
- Provider-generated scripts execute only through `wsl-bwrap`.
- Existing gates remain the pass/fail authority; no prompt, context, probe, gate, helper, IR, SDK, or case-order change is permitted between development and held-out execution.
- `running` and `interrupted` reports are partial evidence only and do not reuse budget.  A provider lifecycle failure is reported separately and is not attributed to generated CAD code or geometry.

## Acceptance

- Development and held-out reports each reach `completed` under the frozen policy, or an authorization/preflight failure is recorded without issuing an unapproved request.
- The review states denominators, request counts, provider deadline, duration, first-pass outcomes, and repair outcomes separately by split.
- Every hosted request has an authorization record and a fresh report path; all reviewed trace material is sanitized.
- Existing offline tests and lint pass after any implementation change:

```powershell
uv run python -m pytest
uv run python -m ruff check .
```

## Status transition

When complete, update `docs/workflow/status.md`, this workpack, the active handoff, `docs/workpacks/README.md`, and the evaluation review.  Then move this workpack to `done/`; do not activate `WP-M10-006` until both split reports are completed.

## Implementation evidence

- The separately authorized development and held-out schema-v3 reports both completed under frozen `deepseek-v4-pro`, bounded probe-summary, `wsl-bwrap`, one-repair-round, and 120-second provider-deadline policy.
- Development used 3/4 requests: one provider lifecycle result, one first-pass script failure, and one repair pass. Held-out used 2/2 requests: a first-pass script failure followed by a one-round `repair_exhausted` result.
- The sanitized [evaluation review](../../architecture/v1/m10-005-external-first-pass-evaluation-review.md) reports split denominators and evidence funnel without a benchmark claim.

## Out of scope

Provider calls without explicit authorization, external downloads, prompt/context experiments, reference scripts, report-schema changes, new probes or gates, helpers, IR, SDK, benchmark claims, FEA, VLM judging, and multi-agent orchestration.
