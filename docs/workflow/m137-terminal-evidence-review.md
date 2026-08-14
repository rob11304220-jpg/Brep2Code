# M137 Terminal Evidence Review

- **Date**: 2026-08-12
- **Workpack**: `WP-M137-terminal-evidence-review`
- **Evidence boundary**: completed M135-011 report, monitor and existing local revision artifacts only

## Accounting and terminality

The M135-011 report is `completed`; its monitor is `terminal`; accounting is
18 used / 0 remaining; and no integrity fault, repair or retry occurred.

| Terminal stage | Count | Conditions |
|---|---:|---|
| Full Harness success | 3 | All three dependent-face-selection no-card rows |
| Downstream gate failure | 11 | Repeated-feature (3), revolve (3), multi-inner-loop pocket (3), prismatic low/high no-card (2) |
| Sandbox execution failure | 1 | Prismatic nominal no-card |
| Static API inadmissible | 3 | All prismatic card rows |

The 11 downstream failures have existing script/Harness evidence. The
repeated-feature and multi-inner-loop rows consistently fail volume/topology
gates; revolve and prismatic low/high rows include bbox, volume and topology
failures. The nominal prismatic no-card script fails script exit/output gates.
These are condition-level gate outcomes, not a common causal diagnosis.

## Card boundary

All three card rows stopped before sandbox execution at M115 static API
admissibility. Their record directories contain no Harness revision or saved
generated script, because rejection occurred before Harness launch. The report
stores only `static_api_inadmissible`, not the classifier's standardized reason
or a safe structural summary. Thus the evidence cannot distinguish model
noncompliance with the fixed API/output contract from a deficiency in card
content, nor can it support a card update or a treatment-effect claim.

## Disposition

Do not modify the existing card or rerun/repair M135. The smallest justified
follow-up is a new offline M138 workpack that records the declared static API
rejection reason and a content-free script fingerprint/structural summary at
the pre-sandbox boundary. Any card revision or repair experiment needs a
separate design, fresh hashes, fresh report paths, preflight and authorization.
