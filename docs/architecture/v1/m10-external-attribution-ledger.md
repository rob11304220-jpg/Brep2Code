---
type: evidence-ledger
related-project: Brep2Code
version: v1
status: active
tags:
  - Brep2Code
  - M10
  - attribution
  - repair-governance
---

# M10 External Attribution Ledger

## Purpose and rules

This is the cumulative, sanitized review record for completed external first-pass cases.  It is not a corpus-report schema, benchmark, or replacement for the underlying ignored reports and traces.  Update it before every post-admission routing decision.

Evidence levels are deliberately narrow:

| Level | Meaning | May count toward a narrow helper? |
|---|---|---|
| `direct` | The generated revision and execution trace directly show the claimed causal failure. | Yes |
| `supported` | Existing signals consistently suggest a mechanism but no execution trace proves that mechanism caused the failure. | No |
| `unknown` | Evidence is insufficient or cannot distinguish the claimed cause. | No |

A static symptom, including an unexecuted host path in a script, is not `direct`.  Provider lifecycle results are not generated-script evidence.  A repair pass remains separate bounded recovery evidence.

## Completed-case ledger

| Case / batch / split | First pass / repair | Primary attribution / level | Revision and local evidence | Unresolved question | Candidate repair hypothesis | Counterexample status |
|---|---|---|---|---|---|---|
| `00000023` / M10-005 / development | provider request timeout / n.a. | provider lifecycle / `unknown` | No generated revision or executable artifact; [M10-006 review](m10-006-external-failure-attribution-review.md) | Was the request service-side or transport lifecycle? | None; do not infer script remediation. | No generated script to compare. |
| `00000024` / M10-005 / development | script/output failure / pass | generic STEP-read / `unknown` | Revision `20260802T161055849602Z`; `data/records/abc-v00-m10-005-development-pro-abc_v00_00000024/revisions/20260802T161055849602Z/signal_bundle.json` | Does the generic exception conceal path, import, or API misuse? | Collect discriminating trace-supported evidence; no implementation hypothesis yet. | Repair passed but does not identify a cause. |
| `00000026` / M10-005 / held-out | script/output failure / repair exhausted | generic STEP-read / `unknown` | Revision `20260802T161902023265Z`; `data/records/abc-v00-m10-005-held-out-pro-abc_v00_00000026/revisions/20260802T161902023265Z/signal_bundle.json` | Same as `00000024`; are the two generic exceptions one mechanism? | Collect discriminating trace-supported evidence; no implementation hypothesis yet. | Repair exhausted; no causal contrast. |
| `00000027` / M10-008 / development | script/output failure / repair exhausted | sandbox input path / `direct` | Revision `20260802T234643142841Z`; `data/records/abc-v00-m10-008-development-pro-abc_v00_00000027/revisions/20260802T234643142841Z/signal_bundle.json`; [M10-009 review](m10-009-cross-batch-generation-attribution-review.md). | Resolved for fixed-script sandbox compatibility; no generated-script generalization follows. | M10-012 reproduced the host-path failure and made output readable with `/input/model.step`; [review](m10-012-minimal-offline-path-repair-review.md). | `00000030` remains non-matching: its import failure occurs first. |
| `00000030` / M10-008 / development | script/output failure / pass | unavailable Python/OCP import / `direct` | Revision `20260802T234750716049Z`; `data/records/abc-v00-m10-008-development-pro-abc_v00_00000030/revisions/20260802T234750716049Z/signal_bundle.json`; [M10-009 review](m10-009-cross-batch-generation-attribution-review.md). | Is this an isolated import choice or a recurrent compatibility family? | Collect another direct reproduction before proposing an import-compatibility experiment. | The host path present in this revision is not counted: import failure occurs first. |
| `00000031` / M10-008 / held-out | script/output failure / pass | sandbox input path / `direct` | Revision `20260802T235326233481Z`; `data/records/abc-v00-m10-008-held-out-pro-abc_v00_00000031/revisions/20260802T235326233481Z/signal_bundle.json`; [M10-009 review](m10-009-cross-batch-generation-attribution-review.md). | Resolved for fixed-script sandbox compatibility; no hosted held-out conclusion follows. | M10-012 reproduced the host-path failure and passed all existing gates with `/input/model.step`; [review](m10-012-minimal-offline-path-repair-review.md). | Repair uses `/input/model.step`; it is recovery evidence, not a first-pass counterexample. |

## Current routing implication

The two `direct` sandbox input-path cases met the eligibility threshold for the **minimal offline repair experiment**, and M10-012 has completed.  It confirms deterministic `/input/model.step` compatibility and retains the non-matching import failure, but it does not meet the three-case narrow-helper threshold or authorize a production helper.  No first-pass case reached readable geometry comparison, so report-only geometry diagnostics remain ineligible.  M10-010 remains a fixed offline admission workpack and was not retroactively expanded by this ledger.
