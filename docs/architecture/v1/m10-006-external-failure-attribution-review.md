# M10-006 External Generation Failure Attribution Review

## Scope and evidence boundary

This review uses only the completed M10-005 reports and their local sanitized revision evidence. It does not retain raw assets or full provider responses, make a model-quality claim, or change Harness behavior.

## Case attribution

| Case | Split | First-pass outcome | Repair outcome | Primary attribution | Local evidence |
|---|---|---|---|---|---|
| `abc_v00_00000023` | development | `provider_request` after one request | not applicable | provider lifecycle | No generated revision or executable artifact was recorded. |
| `abc_v00_00000024` | development | script exit/output failure | pass | unknown | Revision `20260802T161055849602Z`, `data/records/abc-v00-m10-005-development-pro-abc_v00_00000024/revisions/20260802T161055849602Z/signal_bundle.json`: readable input, sandboxed script exit 1, no output STEP, geometry gates skipped. The trace reports only a generic STEP-read exception, which is insufficient to attribute an OCP/API, parameter, or dependency defect. |
| `abc_v00_00000026` | held-out | script exit/output failure | failed after one round (`repair_exhausted`) | unknown | Revision `20260802T161902023265Z`, `data/records/abc-v00-m10-005-held-out-pro-abc_v00_00000026/revisions/20260802T161902023265Z/signal_bundle.json`: readable input, sandboxed script exit 1, no output STEP, geometry gates skipped. The trace has the same generic STEP-read exception and does not support a narrower attribution. |

The provider-lifecycle result is not evidence of generated CAD code. The two script failures are not geometry evidence because the output artifact was absent and all geometry comparisons were skipped. The generic exception appears in only two executable first-pass cases and lacks direct OCP/API, parameter/unit, or operation-dependency evidence.

## Route decision

Select another deterministic external corpus increment under the existing M10-003 route.

- `WP-M10-002` does not qualify: zero cases reached readable output and geometry comparison, below the three-case geometry-diagnostics threshold.
- `WP-M10-004` does not qualify: zero cases have a direct, reproducible OCP/API, parameter, or dependency-sequencing attribution, below the three-case narrow-helper threshold.
- The completed sample remains too small and too weakly attributable to change probes, gates, helpers, IR, SDK, prompt context, or execution policy.

The selected increment remains local-only and offline until a separate workpack records its deterministic admission and controls. No hosted request is authorized by this review.
