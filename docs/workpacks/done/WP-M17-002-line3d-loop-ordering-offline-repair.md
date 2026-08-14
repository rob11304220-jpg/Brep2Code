# WP-M17-002: Line3D Loop-Ordering Offline Repair

- Status: done
- Milestone: M17
- Owner: unassigned

## Goal

Test whether deterministic endpoint-based ordering of a supported `Line3D`
outer loop repairs the M17 held-out degenerate-face mismatch without widening
the Fusion operation surface.

## Repair hypothesis and evaluation boundary

`41026_295d1dc8_0003` is direct, locally reproducible evidence: its strict
one-Sketch/one zero-taper NewBody extrude JSON is accepted, but its listed
Line3D curve starts are non-continuous. The current replay builds a polygon in
that listed order and produces a degenerate face. The treatment may reorder
only existing Line3D segments by matching endpoints, including reversing a
segment when necessary; it must reject ambiguous or non-closing loops.

The fixed held-out case is the treatment case. The pre-treatment M17 report is
the baseline. M14's Line3D and Circle3D cases plus M17's two development cases
are non-regression controls. This experiment can establish local replay
compatibility only; it cannot claim model improvement, authorize a corpus run,
or alter production Harness behavior.

## Scope

- Keep the accepted feature class unchanged: one transformed outer profile,
  Line3D polygon or single Circle3D, then one zero-taper one-sided NewBody
  distance extrude with cm-to-mm normalization.
- Re-run M14 and M17 fixed selections through the offline replay tools and
  existing bbox, volume and topology gates.
- Record the treatment and controls in a review.

## Compatibility constraints

No new case selection, manifest change, corpus run, provider request, hosted
evaluation, external download, CLI/schema/gate/helper/IR/SDK/prompt change, or
curve-type/operation-surface expansion is permitted.

## Acceptance

- The held-out treatment produces a readable STEP and passes existing gates.
- M14 and M17 non-treatment controls preserve their existing gate outcomes.
- A malformed or ambiguous Line3D loop is rejected rather than guessed.
- Status, selection/report evidence, handoff and review agree.

## Result

**Rejected.** Endpoint ordering did not repair the held-out case: bbox max
delta remained 1016 mm and volume relative delta remained 1.0; topology delta
changed only from 13 to 11. The M14 three-case regression controls and the M17
two development cases retained their pass outcomes. The strict baseline tool
was restored after the experiment. The pre-treatment and restored-baseline
reports remain ignored local evidence; treatment metrics are recorded in the
review before its transient output was replaced by the restored baseline.

The non-continuous curve list is therefore an observed symptom, not a
sufficient root cause. No parser change, manifest change, corpus run, provider
request or data-source switch follows from this experiment.

## Out of scope

Arcs, splines, inner loops, Join/Cut, multiple extrudes, generic sketch
healing, provider evaluation, and source-dataset expansion.
