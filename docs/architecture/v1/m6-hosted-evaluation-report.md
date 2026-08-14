---
type: review
related-project: Brep2Code
version: v1
status: done
tags:
  - Brep2Code
  - v1
  - M6
  - corpus
  - hosted-provider
---

# M6 Review Report — Hosted Corpus Evaluation and Failure Taxonomy

## Evidence boundary

This report records bounded engineering evidence from one DeepSeek V4 Flash P0 run, partial/retried P1 execution, and one P1 timeout validation. It establishes behavior of the Harness, sandbox, reports, and recovery loop on this host. It is **not** a benchmark, a model-quality estimate, or evidence for general CAD reconstruction performance.

## Completed evidence

| Scope | Primary result | Hosted repair result | Request accounting | Evidence status |
|------|----------------|----------------------|-------------------|-----------------|
| P0 (`box`, `cylinder`, `block_with_hole`) | 1 / 3 pass | 2 / 2 failed cases pass after one round | 2 / 3 used | Complete schema-v2 report: `data/corpus-runs/deepseek-p0-flash-20260801.json` |
| P1 retry (`filleted_block`, `chamfered_block`, `three_hole_plate`) | 0 / 3 pass | 3 / 3 pass after one round | 3 / 4 used | Atomic `running` checkpoint: `data/corpus-runs/deepseek-p1-flash-retry-20260801.json` |
| P1 `box_cylinder_union` | geometry-gate failure | `provider_request_timeout` at 120 seconds | 1 request issued | Complete single-case report: `data/corpus-runs/deepseek-box-union-timeout-20260801.json` |

The first P1 batch was externally stopped before it wrote a report. It remains historical revision-level evidence only and is not included as a corpus aggregate.

## Failure taxonomy

| Category | Observed cases | Interpretation |
|----------|----------------|----------------|
| `geometry_gate` primary failure | P0: `cylinder`, `block_with_hole`; P1: all four cases | The default scaffold continues to emit the baseline box; scripts execute and produce readable STEP. This is expected coverage evidence, not a probe/backend/gate defect. |
| Repair pass | P0 failed cases; P1 `filleted_block`, `chamfered_block`, `three_hole_plate` | One bounded hosted round generated a gate-passing script on these cases. |
| `provider_request_timeout` | P1 `box_cylinder_union` | The initial and repair-prelude `wsl-bwrap` executions both completed in about one second. A request trace was written but no response trace appeared before the 120-second deadline. The bounded worker terminated the request and the report completed. |
| External process stop | Earlier P1 batch and P1 retry | Atomic checkpoints preserved completed cases but an external force-stop cannot write a terminal status. This is correctly represented as `running`, not as a false completion. |
| Request accounting defect | First single-case timeout report | A request that timed out was initially reported as `requests_used: 0`. The runner now increments accounting when issuing a request, including timeout/error paths. The original artifact is retained unchanged and must be read with this caveat. |

## M6 decisions

- Do not introduce a modeling IR, project CAD SDK, CAD workplace, new probe, or new geometry gate from this evidence.
- Keep the default corpus and fake-provider paths offline and deterministic.
- Retain explicit hosted authorization, `wsl-bwrap`, atomic checkpoints, and per-request provider deadlines as prerequisites for any future hosted evaluation.
- A future hosted batch must use a new explicit budget; it must not reuse an interrupted run's nominal remainder.

## Follow-up candidates

1. Investigate provider reliability and cancellation semantics with offline/loopback tests and separately authorized targeted requests.
2. Expand the corpus only after defining a reproducible evaluation budget and report policy.
3. Use failure evidence from additional completed reports—not this small sample alone—to justify any change to probes, gates, or modeling abstractions.

## Archive checklist

- Preserve the P0 complete report, the P1 running checkpoint, and the single-case timeout report under ignored `data/`.
- Link the relevant revision and trace paths, request counts, provider timeout, and test evidence.
- State the request-accounting correction and do not rewrite the historical timeout report.
- Confirm that reports and traces contain no credential markers before sharing any summary.
