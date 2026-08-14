# WP-M17-005: Frame Selector Promotion Validation

- Status: done
- Milestone: M17
- Owner: unassigned

## Goal

Validate whether the M17-004 explicit Line3D replay-direction selector can be
promoted without regressing the fixed controls. This workpack begins with a
preregistered validation plan only; it does not itself authorize a parser or
replay implementation change.

## Candidate and fixed population

For one transformed Line3D outer loop with a zero-taper, one-sided distance
extrude, the candidate selector is:

1. Endpoint-order the existing Line3D segments, rejecting ambiguous or
   non-closing loops.
2. Choose the unique normalized sketch axis parallel to the ordered profile
   normal whose input-STEP bbox projected span equals the source extent
   magnitude after cm-to-mm normalization.
3. Select `+axis` when the transformed profile lies on the lower projection
   boundary and `-axis` when it lies on the upper boundary.

The fixed population is exhaustive and hash-locked: M14 development
`100243_9fb796fe_0005`, `100877_ac1e5a17_0001`; M17 development
`145540_a4f54d5f_0010`; and M17 held-out `41026_295d1dc8_0003`. No replacement,
scan extension, additional source or split change is permitted.

## Preregistered validation matrix

| Row | Cases | Replay mapping | Required result |
|---|---|---|---|
| Strict baseline | all four | existing strict listed-order / `z_axis` mapping | Preserve recorded baseline outcomes: three development pass, held-out fail. |
| Candidate treatment | all four | apply the candidate selector only when it resolves uniquely | Held-out passes bbox, volume and topology gates; all three development controls remain pass. |
| Selector rejection | any fixed case | ambiguity, no matching axis, non-boundary profile, or non-closing loop | Reject before STEP write; do not add a fallback axis or healing behavior. |

The candidate treatment may be implemented only after this workpack records the
exact code boundary and a focused offline test. It must remain restricted to
the existing single Sketch / single zero-taper NewBody extrude / Line3D outer
loop subset; Circle3D, inner loops, arcs, splines, Join/Cut and multiple
extrudes stay outside scope.

## Focused test and code boundary

`tests/test_fusion360_m17_line3d_selector.py` defines the selector contract
with synthetic, offline-only projection data: one unique lower-boundary
selection, one ambiguity rejection with no fallback, and one upper-boundary
negative-sign selection. The pure calculation is isolated in
`tools/fusion360_line3d_selector.py`; it neither reads source assets nor writes
STEP. The only candidate replay boundary for a later treatment is the Line3D
branch in `tools/replay_fusion360_m14.py:replay()`: after its existing subset
checks and endpoint ordering, and before `BRepBuilderAPI_MakePolygon` and
`BRepPrimAPI_MakePrism`. Strict listed-order / `z_axis` replay remains intact
until that candidate treatment is explicitly run against the preregistered
four-row matrix.

## Gates and stopping conditions

- Reuse existing bbox, volume and topology comparison gates unchanged.
- Promotion requires the candidate held-out result to pass every gate and all
  three Line3D development controls to retain every gate pass.
- Any gate regression, selector ambiguity, or mismatch against M17-004's
  source-linked evidence stops the workpack: restore strict replay, document
  the result, and do not expand samples, adjust gates, or select M18.
- A passing matrix is still not a general parser claim. It may only support a
  subsequent review of this explicit, hash-locked subset.

## Compatibility constraints

Offline only. No corpus run, provider request, hosted evaluation, new input,
manifest change, source scan, gate change, CLI/schema change, prompt/tool
change, runtime retrieval change or M18 work is permitted. Do not infer a
generic coordinate-frame system or add a fallback mapping.

## Acceptance

- The plan names the selector, all four SHA-256-linked cases, baseline and
  candidate matrix, existing gates, and stop conditions.
- Before implementation, a focused offline test defines unique selection,
  ambiguity rejection and boundary-sign behavior.
- If implementation is authorized within this workpack, the resulting local
  report records baseline and treatment outcomes for all four cases.
- Status, handoff, roadmap and corpus records remain consistent.

## Result

**Completed.** The focused selector contract passed 3/3 offline tests for
unique selection, ambiguity rejection without fallback, and boundary sign.
The ignored local four-case matrix reproduced the strict baseline (three
development passes and the fixed held-out failure), then passed bbox, volume
and topology gates for all four selector-treatment rows. The strict
`replay()` path remains the default; `replay_line3d_selector()` is a
candidate-only function invoked solely by
`tools/replay_fusion360_m17_selector.py` for this hash-locked matrix.

This is validation of the explicit fixed subset, not a generic parser or
mapping-policy promotion. It does not authorize a corpus run, provider use,
sample expansion, gate change, syntax expansion or M18.

## Out of scope

Production generalization beyond the fixed subset, new cases, external data,
DeepCAD, provider/hosted execution, corpus evaluation, LLM changes and M18.
