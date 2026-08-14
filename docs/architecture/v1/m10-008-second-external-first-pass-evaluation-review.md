# M10-008 Second External First-Pass Evaluation Review

## Status

Completed on 2026-08-03. Both split-preserving reports reached `completed` under the unchanged `deepseek-v4-pro` / `first-pass-summary-v1` / `wsl-bwrap` policy. This is bounded Harness engineering evidence, not a model-quality or benchmark conclusion.

## Frozen policy and reports

| Split | Report | Cases | Repair bound | Provider deadline | Requests |
|---|---|---:|---:|---:|---:|
| Development | `abc-v00-m10-008-development-pro-authorized-20260803.json` | 2 | 1 | 120 s | 4 / 4 |
| Held-out | `abc-v00-m10-008-held-out-pro-authorized-20260803.json` | 1 | 1 | 120 s | 2 / 2 |

Both splits used the M10-007 manifests, bounded probe-summary context, existing gates, and separate explicit authorizations. Raw STEP assets, credentials, complete provider responses, traces, and reports remain local ignored data.

## Evidence funnel

| Split | Selected | Readable inputs | First-pass provider responses | First-pass executable/readable outputs | First-pass geometry passes | Repair passes |
|---|---:|---:|---:|---:|---:|---:|
| Development | 2 | 2 | 2 | 0 | 0 | 1 |
| Held-out | 1 | 1 | 1 | 0 | 0 | 1 |

All three first-pass scripts failed before creating an output STEP, so all geometry comparisons were skipped. `abc_v00_00000027` ended `repair_exhausted`; `abc_v00_00000030` and held-out `abc_v00_00000031` each passed after one repair.

## Local signal interpretation

The sanitized primary signal for `00000027` attempted to read a host Windows input path unavailable inside the sandbox. The held-out `00000031` recorded a generic STEP-read failure, while the input probe remained readable. `00000030` used an unavailable `OCP.Interface.Interface_Static_SetCVal` import. These are two path/STEP-read signals and one incompatible-import signal, not three directly reproducible cases of one OCP/API, parameter, or operation-sequencing defect. The prior M10-005 generic STEP-read signals remain insufficiently specific to reclassify under this review.

Repair success for `00000030` and `00000031` demonstrates bounded recovery for those individual cases; it does not establish a general fix.

## Decision boundary

M10-008 satisfies its evaluation acceptance: both authorized reports completed and this review preserves split boundaries. It does not itself authorize a helper, prompt, probe, gate, IR, SDK, or additional hosted request. Any next route requires a separate evidence/routing workpack.
