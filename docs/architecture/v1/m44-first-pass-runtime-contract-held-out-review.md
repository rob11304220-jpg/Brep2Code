# M44 First-Pass Runtime-Contract Held-Out Review

## Status

The separately authorized held-out run completed on 2026-08-08.  This report
keeps the one-case held-out outcome separate from M43 development evidence and
does not form a benchmark claim.

## Frozen policy

| Field | Value |
|---|---|
| Case | `abc_v00_00000031` |
| Provider / model | DeepSeek `deepseek-v4-pro` |
| Executor | `wsl-bwrap` |
| Context | path-sanitized bounded probe summary plus M42 runtime contract |
| Repair bound | one round |
| Request bound / used | 2 / 1 |
| Provider deadline | 120 seconds |
| Report | `data/corpus-runs/m44-runtime-contract-held-out-20260808.json` (ignored local artifact) |

Fresh preflight confirmed the recorded SHA-256, manifest membership, local
provider configuration entry, unused report path, and `wsl-bwrap` control.  The
control had readable input/output and successful execution; its scaffold
geometry failure was expected control evidence.

## Held-out evidence funnel

| Stage | Result |
|---|---|
| Readable input | pass |
| First-pass provider response | received |
| Script exit / readable output | pass / pass |
| bbox, volume, topology gates | pass / pass / pass |
| Repair | not needed |

The first-pass script re-exported the input STEP through installed OCP bindings
and passed every existing output and geometry gate.  It used one request and
returned in 60.70 seconds, below the configured 120-second provider deadline.
This is one held-out success under the frozen runtime-contract policy; it does
not establish general B-Rep-to-CAD reconstruction, feature-history recovery,
or generic editability.

## Egress verification

The local request trace contains the case identifier; `file_name`; format/unit;
bbox; topology counts; area; volume; and the runtime contract.  It contains no
local absolute `input` path and no raw STEP content.  The provider response
trace remains locally sanitized.

## Combined interpretation

M43 development had no first-pass all-gate pass (one executable/readable
near-miss and one script failure later repaired); M44 held-out had one
first-pass all-gate pass.  However, the held-out script reads the mounted input
STEP and re-exports it.  Its gate pass therefore establishes STEP round-trip
and execution compatibility, not B-Rep-to-CAD reconstruction, feature-history
recovery, or editability.  The sample is insufficient for a success-rate,
model-quality, helper, or runtime-policy conclusion.  No further provider run
is selected by this review; a later Q03 provenance-gate design must prevent or
classify direct input re-export before it can count a reconstruction success.
