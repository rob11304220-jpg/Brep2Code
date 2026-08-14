# WP-M15-001: Fusion Explicit Offline Manifest Admission Review

- Status: done
- Milestone: M15
- Owner: unassigned

## Goal

Review the completed M14 three-case native-history replay evidence and decide
whether an explicit local-only control manifest is warranted.

## Outcome

**Approved for M16 only.** The three M14 cases may proceed to the separately
preregistered M16 local-control-manifest workpack. This review creates no
manifest and does not authorize a corpus run, provider use, feature-support
expansion, or a new external dataset.

## Review evidence

| Split | Cases | Result |
|---|---|---|
| Development | `100243_9fb796fe_0005`, `100877_ac1e5a17_0001` | Both are in the official `train` list; their source families differ; SHA-256 matches M14; input/output probes and bbox, volume, topology gates pass. |
| Held-out | `110043_b73b8beb_0000` | It is in the official `test` list and its source family differs from both development cases; SHA-256 matches M14; input/output probes and bbox, volume, topology gates pass. |

The inputs, JSON history, and replay outputs remain ignored local assets under
the recorded non-commercial/no-redistribution boundary. The corpus contract
permits an external manifest only as an explicit local-development input; it
does not make it a default fixture or provider payload.

## Next boundary

Only `WP-M16-001` may create the approved explicit 2/1 local-only control
manifest. It must re-audit paths, hashes, official split and source-family
isolation before any offline control. M17 and M18 remain conditional backlog;
hosted use remains unapproved.

## Scope

- Inspect the M14 selection record, ignored replay report, license boundary and
  manifest contract.
- Choose exactly one outcome: approve a 2/1 explicit offline control manifest,
  defer it with documented evidence, or reject it with a bounded reason.

## Compatibility constraints

No manifest is created until this review concludes. No corpus run, provider
request, replay-syntax expansion, Harness/CLI/schema/gate/helper/IR/SDK/prompt
change, or external download is authorized.

## Acceptance

- A review records the evidence, outcome and next boundary separately for
  development and held-out.
- Status, handoff and admission record agree with the result.

## Out of scope

Hosted use, performance claims, additional samples, Join/Cut, multiple
extrudes, arcs/splines, inner loops, and default test discovery.
