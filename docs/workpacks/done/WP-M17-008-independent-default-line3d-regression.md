# WP-M17-008: Independent Default Line3D Regression

- Status: done
- Milestone: M17
- Owner: unassigned

## Goal

Test the M17-007 restricted default Line3D mapping on one additional,
preregistered family-isolated local population.

## Selection and stopping rule

Inspect only official-train positions 401--600 and official-test positions
201--400 in the existing Fusion cache. Exclude every source family used by
M14 through M17-006. Select the first two development and first one held-out
assets that satisfy the same structural subset: final STEP plus native JSON,
one transformed Sketch, profile-plane start, one zero-taper one-sided NewBody
distance extrude, and one outer Line3D loop. Do not prefilter on selector
success.

Run the current default `replay()` exactly once per selected asset. Stop and
record the first selector rejection, write failure or bbox/volume/topology gate
failure; do not replace a selected row, extend a window, add a fallback or
modify code. If a required slot is absent, stop and record it.

## Compatibility constraints

Offline only; no new download, parser syntax, gate, Harness, CLI, manifest,
corpus, provider, hosted, M18 or runtime-guidance change.

## Acceptance

- Track source order, split, family and SHA-256 for selected assets.
- An ignored local report records the default replay and existing gate outcome.
- Status, roadmap, workpack index and handoff record either completion or the
  first stopping condition.
- Run focused selector tests, the M17 frame audit and Ruff for changed files.

## Evidence reuse / guidance-card disposition

Record a counterexample or no reusable evidence. This parser-local regression
does not automatically create runtime guidance.

## Result

Completed. The fixed windows selected development source orders 406 and 446
and held-out source order 211, all from new families. The default replay passed
the existing bbox, volume and topology gates for all three rows; no stopping
condition occurred. This adds 2 development and 1 held-out confirmation rows
to the restricted default policy, without changing it. No runtime guidance
card was created because the result is parser-local regression evidence.

## Out of scope

Expanding support, changing M17-007, accumulating an unbounded sample,
Harness integration, M18 and hosted work.
