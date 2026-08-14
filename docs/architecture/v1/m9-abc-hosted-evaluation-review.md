# M9-001 ABC Hosted First-Pass Evaluation Review

## Status

Completed on 2026-08-02. Separately authorized development and held-out reports both reached `run_status: completed` under the unchanged M9 policy. This is bounded Harness engineering evidence, not a model-quality or benchmark conclusion.

## Evaluation boundary

The M8-selected ABC v00 files remain local research-only assets. This review reports bounded Harness engineering evidence, not model quality or a benchmark result. It must not include raw STEP assets, credentials, environment snapshots, or full provider responses.

## Required evidence

1. Offline SHA-256, manifest, input-probe, and `wsl-bwrap` control preflight for each split.
2. A completed schema-v3 development report using `deepseek-v4-pro`, 8 cases, one repair round, a 16-request maximum, and a 120-second provider deadline.
3. A separately authorized completed schema-v3 held-out report using the same provider and unchanged generation policy, with 4 cases and an 8-request maximum.

## Offline preflight evidence

On 2026-08-02, all 12 selected local files matched the M8 SHA-256 record. M9-002 found that the two former timeouts were dominated by STEP loading and adopted the bounded 45-second input summary deadline in [ADR-0008](../adr/0008-bounded-input-probe-timeout.md), while retaining the 15-second output deadline. The revalidated ignored development and held-out reports both reached `run_status: completed` through `wsl-bwrap`; all 12 input summaries and all generated scripts succeeded. All 12 fixed-scaffold geometry failures are expected control evidence. Input-probe readiness is no longer a blocker.

## Completed hosted evidence

| Split | Report | Unchanged policy | First-pass outcome | Repair outcome | Requests | Primary duration |
|---|---|---|---|---|---:|---:|
| Development (8) | `abc-v00-m9-001-development-pro-retry-20260802.json` | `deepseek-v4-pro`, `wsl-bwrap`, one repair round, 120-second provider deadline | 0 pass; 4 `script_failure`; 4 `provider_request` | 1 pass; 3 fail (`repair_exhausted`) | 12 / 16 | 741.81 s |
| Held-out (4) | `abc-v00-m9-001-held-out-pro-authorized-20260802.json` | Same provider, generation policy, executor, repair bound and deadline | 1 pass; 1 `script_failure`; 2 `provider_request` | 0 pass; 1 fail (`repair_exhausted`) | 5 / 8 | 305.66 s |

All selected inputs had the required readable-input evidence. Among first-pass responses that reached Harness execution, the five `script_failure` results failed script exit/output creation or readability, so bbox, volume and topology comparisons were skipped; the one held-out first-pass pass met the existing output and geometry gates. The six `provider_request` outcomes are provider lifecycle results, not evidence of an OCP/API, parameter, dependency-sequencing, geometry-gate, or input-probe defect. No raw STEP asset, credential, environment snapshot, or full provider response is recorded here.

## Review method

Report first-pass gate outcomes, post-repair outcomes, request count, duration, and sanitized failure types separately by split. Treat `running` and `interrupted` reports as partial evidence only. Do not modify the prompt, Harness, gates, case order, split membership, provider model, executor, timeout, or repair bound between the development review and held-out execution.

## Decision rule

Do not introduce a helper, IR, SDK, CAD workplace, probe, or gate from a single case, timeout, or isolated geometry failure. A later narrow-helper workpack requires repeated, attributable OCP/API boilerplate, parameter, or dependency-sequencing evidence across completed cases.

## Decision

The review selected the completed M10-003 deterministic external corpus
increment; its durable attribution interpretation is in the
[M10 external attribution ledger](m10-external-attribution-ledger.md) and the
[Post-M9 Evidence-Gated Roadmap](post-m9-evidence-gated-roadmap.md).

The M9 reports do not establish the required direct, reproducible three-case OCP/API, parameter, or dependency-sequencing pattern for a narrow helper. They also do not support report-only geometry diagnostics: only one first-pass output reached all geometry gates, while script failures had skipped geometry comparisons and provider-request outcomes had no attributable generated artifact. The completed sample is therefore insufficient to establish a stable modeling-failure pattern; the roadmap selects a small deterministic, offline external increment before proposing a helper, IR, SDK, probe, or new gate.
