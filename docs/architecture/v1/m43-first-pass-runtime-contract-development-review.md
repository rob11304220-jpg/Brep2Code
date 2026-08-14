# M43 First-Pass Runtime-Contract Development Review

## Status

Development execution completed on 2026-08-08 under the explicitly authorized
two-case scope.  This is development-only engineering evidence; held-out case
`abc_v00_00000031` was not requested or run.

## Frozen conditions

| Field | Value |
|---|---|
| Provider / model | DeepSeek `deepseek-v4-pro` |
| Cases | `abc_v00_00000027`, `abc_v00_00000030` |
| Executor | `wsl-bwrap` |
| First-pass context | bounded probe summary plus `/input/model.step`, `output/model.step`, installed `OCP` imports, and JSON replacement-script contract |
| Repair bound | one round per case |
| Request bound / used | 4 / 4 |
| Provider deadline | 120 seconds |
| Report | `data/corpus-runs/m43-runtime-contract-development-20260808.json` (ignored local artifact) |

Both inputs hash-matched the M10-007 selection and completed the local sandbox
control with readable input/output and a successful script exit.  The fixed
scaffold's geometry failures are expected controls.

## Evidence funnel

| Stage | Case 27 | Case 30 |
|---|---:|---:|
| Readable input | pass | pass |
| First-pass provider response | received | received |
| First-pass script / readable output | pass / pass | fail / no output |
| First-pass geometry pass | no: bbox only | no: skipped |
| One-round repair | fail | pass |

Case 27's first pass used `/input/model.step`, generated a readable STEP, and
matched volume and topology counts; its maximum bbox delta was `0.00016`, above
the existing `1e-05` tolerance.  Its repair ended at the one-round bound and
introduced an unavailable `OCP.Interface_Static` import.  Case 30's first pass
used an integer `0` where `STEPControl_Writer.Transfer` requires the typed
`STEPControl_StepModelType`; its repair produced a fully passing output.

No provider timeout occurred.  The batch demonstrates that the contract can
get a first-pass script through sandbox execution and readable output for one
of two development cases, but it does not establish a reliable first-pass
success rate, a general import/API repair, or B-Rep modeling improvement.

## Egress correction

The completed batch's local request traces showed that the pre-existing
`probe_summary.input` value exposed the local absolute path to the provider.
No raw STEP content was sent.  This was not intended as part of the derived
summary; ADR-0046 now removes it from every future first-pass request while
retaining `file_name` and geometry facts locally and in the outbound summary.
The correction cannot retroactively change M43's completed provider requests.

## Reviewer decision needed

The independent reviewer must decide whether this development result justifies
a separately authorized held-out run.  If selected, the held-out policy must
use the path-sanitized summary, the same model/executor/repair/deadline bound,
one case, a maximum of two requests, a new report path, a fresh preflight, and
explicit user authorization.  Do not interpret the development result as that
authorization.
