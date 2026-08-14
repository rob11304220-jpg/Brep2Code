# M10-009 Cross-Batch Generation Attribution Review

## Scope and boundary

This review combines the six completed external cases from M10-005 and M10-008. It consumes only ignored local reports, generated revisions, and sanitized signals. It makes no benchmark claim and does not modify provider policy, prompts, Harness behavior, probes, gates, helpers, IR, SDK, fixtures, manifests, or external data.

## Case attribution

| Case | Split | First-pass outcome | Repair outcome | Primary attribution | Evidence boundary |
|---|---|---|---|---|---|
| `00000023` | M10-005 development | provider request timeout | n/a | provider lifecycle | No generated revision was recorded. |
| `00000024` | M10-005 development | STEP-read script/output failure | pass | unknown | Readable input, no output STEP, and only a generic STEP-read exception; no direct source cause. |
| `00000026` | M10-005 held-out | STEP-read script/output failure | repair exhausted | unknown | Readable input, no output STEP, and only a generic STEP-read exception; no direct source cause. |
| `00000027` | M10-008 development | script/output failure | repair exhausted | sandbox input path | Revision `20260802T234643142841Z` passes a host Windows path to the STEP reader; the sandbox trace records its resulting STEP-read failure. |
| `00000030` | M10-008 development | script/output failure | pass | Python/OCP import | Revision `20260802T234750716049Z` imports unavailable `OCP.Interface.Interface_Static_SetCVal`; execution stops at that import. A host path is statically present but is not counted as an executed cause. |
| `00000031` | M10-008 held-out | script/output failure | pass | sandbox input path | Revision `20260802T235326233481Z` passes a host Windows path to the STEP reader; the sandbox trace records a STEP-read failure while the input probe is readable. |

All non-provider cases had a readable input but no readable first-pass output, so existing geometry comparisons were skipped. The three repair passes (`00000024`, `00000030`, `00000031`) are bounded recovery evidence only; they do not replace first-pass outcomes. In each successful repair revision, the script uses `/input/model.step` and no longer passes a host path to the reader.

## Threshold checks

| Candidate route | Threshold | Observed evidence | Result |
|---|---|---|---|
| Geometry diagnostics (`WP-M10-002`) | At least 3 executable/readable first-pass outputs with non-actionable geometry failure | 0 executable/readable first-pass outputs | Does not qualify. |
| Narrow helper (`WP-M10-004`) | At least 3 external cases sharing one direct and reproducible OCP/API, parameter, or dependency-sequencing cause | 2 directly trace-proven sandbox-path cases; 1 direct unavailable-import case; 2 generic STEP-read cases remain unknown | Does not qualify. |

The third statically observed host-path pattern (`00000030`) is not counted because its import failure prevents showing that the path caused that execution. Treating it as a third direct path failure would exceed the evidence.

## Route selection

Select a third deterministic external corpus increment, `WP-M10-010`. It extends evidence under the unchanged local admission and offline-control policy. It does not authorize hosted evaluation or any production change.
