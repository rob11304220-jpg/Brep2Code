---
type: review
related-project: Brep2Code
status: completed
---

# M16 Review: Fusion 360 Local Control Manifests

## Result

M16 created two explicit, non-default local-only manifests:

- `fusion360-gallery-r1.0.1-m16-001-development-manifest.json` — two cases.
- `fusion360-gallery-r1.0.1-m16-001-held-out-manifest.json` — one case.

They are split-preserving local-development controls, not default fixtures,
benchmark inputs, corpus-run authorization, provider payloads or hosted
evaluation authorization.

## Offline audit

The audit loaded both manifests with `brep2code.corpus.manifest.load_case_manifest` and verified:

- all three repository-relative paths resolve under the ignored Fusion cache;
- SHA-256 values match the M14 selection record;
- development cases are in official `train`, and the held-out case is in
  official `test`;
- all three source families are distinct; and
- neither manifest declares `reference_script` or `first_pass_script`.

Existing M14 evidence remains the replay/gate evidence: every case had readable
input and output STEP and passed bbox, volume and topology gates.

## Boundary after M16

M17 is still a conditional backlog item. Before it can select any additional
Fusion case, a separate review must preregister its coverage question, sample
bound and stopping condition. This M16 result does not authorize a corpus run,
provider request, hosted execution, operation-mapping expansion or DeepCAD
acquisition.
