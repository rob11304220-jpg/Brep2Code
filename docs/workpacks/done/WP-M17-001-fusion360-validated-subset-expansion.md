# WP-M17-001: Fusion 360 Validated-Subset Expansion

- Status: done
- Milestone: M17
- Owner: unassigned

## Goal

Extend paired B-Rep/native-history evidence only within the already cached,
locally replayable Fusion subset.

## Trigger condition

M16 is completed and its review shows that the local control manifest produces
useful, stable evidence. The workpack must preregister the coverage question,
sample bound, and stopping condition before selection.

## Attribution question and sampling intent

**Question:** Does the already validated native-history mapping remain
reproducible across additional source families and both supported profile
classes, without extending the operation surface?

**Fixed selection:** inspect at most the first 200 official `train` and the
first 200 official `test` identifiers in source order, excluding all M14 source
families. Select the first accepted Line3D polygon and the first accepted
Circle3D development cases, plus the first accepted held-out case. Acceptance
means the existing strict replay parser accepts the JSON and the final STEP is
present. Each selected case must have a source family distinct from every other
selected case. If a required slot is absent within its 200-item bound, stop and
record that outcome; do not extend the scan, select a replacement rule, or add
syntax support.

**Expected information gain:** distinguish whether the M14 replay result holds
for both currently supported profile classes across new official families, or
whether a deterministic incompatibility appears before expanding the corpus.

## Result

The bounded selection found all three preregistered slots. Both development
cases replayed and passed existing gates. The held-out Line3D case produced a
STEP but failed bbox, volume and topology gates because its listed Line3D curve
starts are not in a continuous loop order; the strict parser therefore formed a
degenerate face. Selection stopped as required: no replacement case, scan
extension, syntax change, corpus run or provider request was attempted.

## Decision

Do not expand the Fusion manifest and do not open M18. This is a narrow local
replay-mapping incompatibility, not evidence that Fusion lacks paired data or
that a second dataset would resolve it. Any future work on deterministic
Line3D-loop ordering must be separately scoped and must retain this failing
held-out control.

## Scope

- Select a small deterministic, source-family-isolated subset from the existing
  r1.0.1 cache.
- Preserve official train/test membership; record source identity, SHA-256,
  replay outcome, and existing geometry-gate outcome for every selected case.
- Support only the already evidenced one-Sketch/one zero-taper NewBody extrude
  mapping unless a separate workpack authorizes a new operation mapping.

## Compatibility constraints

The dataset remains local-only and non-default. No provider request, hosted
evaluation, new external download, or change to Harness behavior is permitted.

## Stopping condition

Stop and review when the next required coverage class needs Join/Cut, multiple
extrudes, arcs/splines, inner loops, or another unsupported representation.
Do not use unbounded case growth as a fallback.

## Out of scope

DeepCAD acquisition, replay-syntax expansion, benchmark claims, and provider
use.
