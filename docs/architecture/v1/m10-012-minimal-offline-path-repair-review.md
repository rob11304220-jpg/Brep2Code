# M10-012 Minimal Offline Sandbox-Path Repair Review

## Scope and boundary

This review uses fixed local scripts and the existing ABC v00 inputs only.  Every execution used `wsl-bwrap`; no provider request, prompt/context change, manifest change, production helper, probe, gate, schema, or CLI change occurred.  `00000031` is reused solely as an offline reproduction of existing evidence, not as a new hosted held-out evaluation.

## Fixed-script evidence

| Case | Script / ignored record | Result | Gate-level evidence |
|---|---|---|---|
| `00000027` | host path / `m10-012-path-27-baseline` revision `20260803T014458409602Z` | Expected failure: the unreadable `D:\\m10-012-host-only\\model.step` raises the fixed host-path STEP-read error. | Input readable; script exit/output existence/output readability fail; geometry gates skipped. |
| `00000027` | `/input/model.step` / `m10-012-path-27-treatment-retry` revision `20260803T014553767399Z` | Readable STEP output produced. | Script exit, output existence, input/output readability, volume, and topology pass.  Bbox remains fail at `0.00016` versus the existing `1e-05` tolerance. |
| `00000031` | host path / `m10-012-path-31-baseline` revision `20260803T014610186574Z` | Expected failure: the same fixed host-path STEP-read error. | Input readable; script exit/output existence/output readability fail; geometry gates skipped. |
| `00000031` | `/input/model.step` / `m10-012-path-31-treatment` revision `20260803T014620508178Z` | Readable STEP output produced. | All existing gates pass. |
| `00000030` | `/input/model.step` import control / `m10-012-import-30-treatment` revision `20260803T014631960725Z` | Expected non-match: `Interface_Static_SetCVal` raises the same unavailable-import error. | Input readable; no output; script/output gates fail and geometry gates skip. |

The first `00000027` treatment record (`m10-012-path-27-treatment`, revision `20260803T014522442524Z`) used an invalid fixture reference to `STEPControl_Writer.STEPControl_AsIs`.  It is retained as ignored local evidence but excluded from the conclusion; the retry changes only that local STEP writer API reference and uses the same input, executor, and `/input/model.step` path.

## Conclusion

The two independent direct path cases reproduce the same sandbox mechanism, and replacing only the input path with `/input/model.step` restores deterministic script execution and readable output.  The corrected-path import control still fails before STEP reading, so the intervention does not hide the unrelated import defect.  Existing geometry gates remain authoritative: the `00000027` round trip retains a strict bbox mismatch, while `00000031` passes every gate.

This is compatibility and repair-signal evidence for fixed scripts only.  It is not evidence of first-pass model improvement, does not establish a generic production path helper, and does not authorize a hosted development or held-out policy comparison.
