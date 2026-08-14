# WP-M16-001: Fusion 360 Local Control Manifest

- Status: done
- Milestone: M16
- Owner: unassigned

## Goal

If M15 approves, create and audit an explicit, non-default local-only 2
development/1 held-out control manifest for the three M14 replay-pass cases.

## Result

Created separate explicit development and held-out manifests. The local audit
parsed both files through `load_case_manifest`, resolved all three input paths,
matched every SHA-256 to the M14 selection record, confirmed the 2/1 official
train/test split and source-family isolation, and confirmed that neither
manifest contains `reference_script` or `first_pass_script`.

No corpus run was performed. The manifests remain non-default local-development
controls; they do not authorize hosted execution or provider input.

## Trigger condition

The completed M15 review explicitly approves the manifest. A deferral or
rejection closes this workpack without creating one.

## Scope

- Record the three source identities, SHA-256 values, official split membership
  and source-family isolation in an explicit manifest.
- Run only offline hash/path/probe/replay and fixed control checks required by
  the manifest contract.
- Keep the manifest non-default and separate development from held-out.

## Compatibility constraints

No provider request, hosted execution, default test discovery, replay-syntax
expansion, Harness/CLI/schema/gate/helper/IR/SDK/prompt change, or external
download is permitted.

## Acceptance

- All three manifest entries resolve below the ignored Fusion cache and match
  the M14 selection hashes.
- Official train/test membership and source-family isolation are auditable.
- Existing gates and replay evidence remain unchanged.
- Status, the Fusion admission record, catalog, and handoff agree.

## Out of scope

Corpus-quality claims, further sample selection, and any provider use.
