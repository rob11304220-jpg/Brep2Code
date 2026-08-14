# M10-005 External First-Pass Evaluation Review

## Status

Completed on 2026-08-03. Development and held-out reports each reached `run_status: completed` under the frozen `deepseek-v4-pro` / `first-pass-summary-v1` / `wsl-bwrap` policy. This is bounded Harness engineering evidence, not a model-quality or benchmark conclusion.

## Frozen policy and reports

| Split | Report | Cases | Repair bound | Provider deadline | Requests |
|---|---|---:|---:|---:|---:|
| Development | `abc-v00-m10-005-development-pro-authorized-20260802.json` | 2 | 1 | 120 s | 3 / 4 |
| Held-out | `abc-v00-m10-005-held-out-pro-authorized-20260803.json` | 1 | 1 | 120 s | 2 / 2 |

Both splits used the admitted M10-003 manifests, unchanged existing gates, the bounded probe-summary context, and separate explicit authorizations. Raw STEP assets, full provider responses, credentials, traces, and reports remain local ignored data.

## Evidence funnel

| Split | Selected | Readable inputs | First-pass provider responses | First-pass executable/readable outputs | First-pass geometry passes | Repair passes |
|---|---:|---:|---:|---:|---:|---:|
| Development | 2 | 2 | 1 | 0 | 0 | 1 |
| Held-out | 1 | 1 | 1 | 0 | 0 | 0 |

Development case `abc_v00_00000023` consumed one request and ended as `provider_request` at the 120-second request deadline, with no generated artifact to attribute. Development case `abc_v00_00000024` received a first-pass script but failed script execution/output creation; its single repair passed. Held-out case `abc_v00_00000026` received both first-pass and repair responses, but both execution attempts failed before output creation; repair stopped at the one-round bound (`repair_exhausted`). Geometry comparisons were skipped whenever no readable output existed, so there is no geometry-mismatch evidence.

## Decision

The completed reports satisfy M10-005's frozen, split-preserving evaluation requirement. They do not establish a benchmark result, a geometry-diagnostics trigger, or a direct repeated OCP/API, parameter, or operation-dependency pattern. The next step is the offline attribution review in M10-006.
