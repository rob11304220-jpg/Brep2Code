# WP-M9-001: ABC External STEP Hosted First-Pass Evaluation

- Status: done
- Milestone: M9
- Owner: unassigned

## Goal

Collect bounded, split-preserving engineering evidence for DeepSeek V4-Pro first-pass generation and one-round repair on the locally admitted ABC v00 samples.

## Scope

- Maintain explicit 8-case development and 4-case held-out manifests derived from M8-001's immutable selection order.
- Run an offline `wsl-bwrap` integrity/control preflight for each split before any hosted request.
- After separate explicit authorization for each split, run hosted `--first-pass` with at most one repair round per case, a 120-second provider deadline, and schema-v3 reports under ignored `data/corpus-runs/`.
- Review only completed reports; classify first-pass and repair outcomes without changing the model, policy, prompt, sample selection, or Harness implementation between splits.

## Inputs

- [M8 selection](../../corpus/external/abc-v00-m8-001-selection.json)
- [Development manifest](../../corpus/external/abc-v00-m9-001-development-manifest.json)
- [Held-out manifest](../../corpus/external/abc-v00-m9-001-held-out-manifest.json)
- [Case corpus contract](../../architecture/v1/contracts/case-corpus.md)
- [Provider runbook](../../runbooks/llm-provider-config.md)

## Code paths

- `docs/corpus/external/abc-v00-m9-001-*-manifest.json`
- `tests/test_corpus_m4.py`

## Docs to update

- `docs/workflow/status.md`, the active handoff, and this workpack for every status transition.
- `docs/architecture/v1/m9-abc-hosted-evaluation-review.md` after both reports are completed. If an authorized batch is conclusively unavailable, record only a closure note that no aggregate engineering conclusion is available.
- `docs/runbooks/case-corpus-review.md` only when a repeatable command or safety procedure changes.

## Trace/schema changes

No schema, trace, storage-layout, or CLI-interface change. Hosted first-pass uses the existing schema-v3 report and sanitized provider traces.

## Compatibility constraints

- Default commands remain offline and credential-free; no test downloads or discovers ABC assets.
- Raw ABC assets, records, traces, and reports remain ignored under `data/`.
- Hosted scripts use `wsl-bwrap`; no provider-generated script may use `unsafe-local`.
- Do not add helper, IR, SDK, CAD workplace, probe, gate, conversion, or fake-provider fixture.

## Acceptance

```powershell
uv run python -m pytest tests\test_corpus_m4.py
uv run python -m pytest
uv run python -m ruff check .
```

- Split manifests preserve the ordered 8/4 M8 selection, do not overlap, and contain no replay or first-pass fixture.
- Each local preflight verifies recorded SHA-256 values before running its explicit manifest with `--executor wsl-bwrap`; hash, input-probe, manifest, and sandbox failures block hosted execution.
- A separately authorized development run is completed with `deepseek-v4-pro`, `max-cases=8`, `max-rounds=1`, `request-budget=16`, and `provider-timeout=120`.
- A separately authorized held-out run repeats the unchanged policy with `max-cases=4`, `max-rounds=1`, `request-budget=8`, and `provider-timeout=120`.
- The M9 review distinguishes completed, interrupted, and running reports; it makes no benchmark claim and proposes a helper only for a repeated, attributable completed-case failure.

## Status transition

When done, move this workpack to `docs/workpacks/done/`, update status and handoff, and record review evidence. No ADR is expected unless later evidence supports a lasting architecture decision.

## Current evidence and authorization blocker

- 2026-08-02: all 12 local STEP files matched the M8 selection SHA-256 values.
- M9-002 established a 45-second bounded input summary path, kept the generated-output deadline at 15 seconds, and made unavailable input summaries explicit failures; see [ADR-0008](../../architecture/adr/0008-bounded-input-probe-timeout.md).
- The revalidated development and held-out reports completed with all 12 input summaries available and all scripts exiting 0 through `wsl-bwrap`. All 12 fixed-scaffold geometry failures are expected control evidence.
- 2026-08-02: an authorized development launch was externally stopped by the host command limit. Its atomic report is `running` with 0 completed cases and `requests_used: 0`; no provider request was issued. It is partial evidence and its budget cannot be reused.
- 2026-08-02: the separately authorized development retry completed under `deepseek-v4-pro` and `wsl-bwrap`, with 8/8 cases, one repair round, a 120-second provider deadline, and 12/16 requests used. The ignored schema-v3 report is `data/corpus-runs/abc-v00-m9-001-development-pro-retry-20260802.json`; it records 4 `script_failure` and 4 `provider_request` final outcomes, with one successful repair among four repair attempts. It is bounded development engineering evidence only.
- Held-out remains separately authorized only after a completed development report. Complete its authorization preflight and obtain new explicit approval before any request; preserve the provider/model, policy, executor, deadline, repair bound, and case order.
- 2026-08-02: the separately authorized held-out batch completed under the unchanged M9 policy: 4/4 cases and 5/8 requests, with one first-pass pass, one `script_failure`, two `provider_request` outcomes, and one failed repair. The ignored report is `data/corpus-runs/abc-v00-m9-001-held-out-pro-authorized-20260802.json`.
- M10-001 reviewed both completed reports and selected `WP-M10-003`; the results do not meet the helper attribution threshold or support geometry diagnostics.

## Out of scope

Hosted authorization itself, raw-data redistribution, model/provider comparison, prompt changes between splits, and implementation of any proposed helper.
