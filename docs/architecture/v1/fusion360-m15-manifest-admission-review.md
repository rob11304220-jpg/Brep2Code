---
type: review
related-project: Brep2Code
status: completed
---

# M15 Review: Fusion 360 Explicit Offline Manifest Admission

## Decision

Approve `WP-M16-001` to create and audit a non-default, local-only control
manifest containing the fixed M14 2 development/1 held-out cases. This decision
does not create the manifest or authorize a corpus run, provider request,
hosted evaluation, replay-syntax expansion, or any Harness behavior change.

## Evidence reviewed

| Case | Official split | Source family | SHA-256 | Replay / gates |
|---|---|---|---|---|
| `100243_9fb796fe_0005` | train / development | `100243_9fb796fe` | `6486124febad653fe2b20196b2f3eacedc358101eda27b8bc2218dcdf9fbe701` | input/output readable; bbox, volume and topology pass |
| `100877_ac1e5a17_0001` | train / development | `100877_ac1e5a17` | `a0bcadae74d5106fb637abe2ab96d765fb1b32db1a86eddfd159cfee672d249f` | input/output readable; bbox, volume and topology pass |
| `110043_b73b8beb_0000` | test / held-out | `110043_b73b8beb` | `66dc5f8b48de5a32202462ae710a4b9aa3e6d9e4588d55a90cd90de40fdd9447` | input/output readable; bbox, volume and topology pass |

The official split check confirms both development cases in `train` and the
held-out case in `test`; no source family appears in both splits. The selected
raw assets and replay outputs remain ignored, local, and bound by the recorded
non-commercial/no-redistribution terms.

## Manifest-contract assessment

The case-corpus contract requires an external manifest to be explicit,
local-development-only, backed by an ignored input root and a tracked selection
record containing source identity, SHA-256, license boundary and normalization.
M14/M15 provide those prerequisites. The manifest must not make these cases
default fixtures or provider inputs. It must have no `reference_script` or
`first_pass_script` without a separately approved contract decision.

## Next boundary

M16 must independently re-audit paths, hashes, official split membership and
source-family isolation before creating the manifest and running any permitted
offline control. M17 and M18 remain conditional backlog. Hosted use requires a
new workpack, preflight and split-specific explicit authorization.
