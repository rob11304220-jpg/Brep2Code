# WP-M10-010: Third Deterministic External Corpus Increment

- Status: done
- Milestone: M10
- Owner: unassigned

## Goal

Prepare a complete ignored local cache of the already acquired ABC v00 archive, then admit one additional small external split by deterministic archive-member order and establish an offline `wsl-bwrap` control baseline without contacting a provider.

## Trigger condition

M10-009 reviewed six completed external cases. Neither the geometry-diagnostics nor narrow-helper threshold qualified, so the existing deterministic-increment route remains selected.

## Scope

- Extract only the existing local `abc_0000_step_v00.7z` archive into ignored `data/datasets/abc/v00/step/`, then write an ignored completion catalog only after archive hash, 10,000-member count, and listed byte-total verification.
- Continue the existing archive-member scan strictly after M10-007 cutoff `00000031`.
- Accept only inputs with a successful existing input probe and exactly one solid; record rejections, source identity, SHA-256, split, and license boundary.
- Form a 2-case development / 1-case held-out split when qualifying inputs permit.
- Run ignored local `wsl-bwrap` controls and verify each selected input hash, manifest membership, script exit, and input/output readability.

## Compatibility constraints

- No provider request, external download, reference or first-pass script, conversion, prompt/context, probe, gate, schema, fixture, runtime behavior change, full manifest, or default corpus enablement.
- Default commands remain offline and credential-free.
- Raw ABC assets remain local ignored data; repository documentation stores only permitted source identities, hashes, and derived baselines.
- Archive extraction is a local cache operation under ADR-0011, not selection, evaluation, redistribution, or provider authorization.

## Acceptance

- The ignored cache completion catalog proves archive hash, 10,000 extracted STEP members, and the archive-listed uncompressed byte total; without it the cache is treated as incomplete.
- A deterministic selection record documents scan order, accepted/rejected candidates, source identity, SHA-256, split, and license boundary.
- Both split controls complete under `wsl-bwrap`; selected inputs are readable and hashes match.
- Review records whether this increment alone changes no runtime behavior and does not authorize hosted evaluation.

## Implementation evidence

- The existing local archive was fully cached under ignored `data/datasets/abc/v00/step/` under ADR-0011.  Its ignored completion catalog verifies archive SHA-256 `52e6dd1b6fa38e3cd99af59b662370829129540030975919c3e256dce6ad1dbe`, 10,000 STEP members, and `13,703,699,417` bytes.
- Continued archive order through `00000032`--`00000035`; accepted 32/33/35 as the 2/1 split and recorded 34 as a three-solid rejection.  All selected hashes and existing input probes matched the tracked selection and manifests.
- Focused static audit passed.  Ignored development and held-out `wsl-bwrap` controls both completed: 3/3 script exits and input/output summaries passed; all fixed-scaffold geometry failures were expected controls.
- The [admission review](../../architecture/v1/m10-010-abc-external-increment-review.md) records the local-only boundary.  No provider request, runtime change, or hosted authorization occurred.
