# WP-M17-003: Sketch-Frame Extrude-Direction Diagnostic

- Status: done
- Milestone: M17
- Owner: unassigned

## Goal

Test a finite, local coordinate-frame hypothesis for the fixed M17 held-out
case without widening the supported Fusion feature subset.

## Repair hypothesis and evaluation boundary

The held-out target STEP has a profile-plane bbox compatible with the existing
point transform, but its 101.6 mm extent lies along the transformed sketch
`y_axis`, not the current `z_axis`. M17-002 showed endpoint ordering alone is
insufficient. This experiment tests the conjunction of endpoint-continuous
Line3D ordering and a `y_axis` extrusion direction.

The treatment matrix is finite: listed-order/`z_axis` baseline,
endpoint-order/`z_axis`, listed-order/`y_axis`, endpoint-order/`y_axis`, and
endpoint-order/negative-`y_axis` sign control. The fixed held-out case remains
the only treatment target; M14/M17 passing cases are non-regression controls.

This experiment can establish a local representation mapping only. It cannot
claim a general Fusion parser, authorize a production change, replace the
held-out control, or introduce a new dataset.

## Scope

- Keep one transformed Line3D outer loop and one zero-taper one-sided NewBody
  distance extrude only.
- Generate ignored local diagnostic outputs and compare with existing bbox,
  volume and topology gates.
- Reject non-closing/ambiguous loops; do not heal other sketch defects.

## Compatibility constraints

No external download, manifest change, corpus run, provider request, hosted
evaluation, CLI/schema/gate/helper/IR/SDK/prompt change, curve-type expansion
or operation-surface expansion is permitted.

## Acceptance

- The report contains every preregistered treatment row and its existing gates.
- M14/M17 controls preserve gate outcomes under the chosen treatment if any.
- A result may be promoted only by a separate workpack after held-out and
  control evidence are recorded.

## Result

**Rejected.** Of the five preregistered held-out treatments, only
endpoint-continuous `ordered_y` passed bbox, volume and topology gates. The
same Line3D treatment made all three M14/M17 Line3D controls degenerate, each
with volume relative delta 1.0; the two Circle3D controls remained pass on
their unchanged strict path. The local direction mapping is therefore not
safe to generalize. Strict replay remains unchanged, and this workpack does
not authorize a parser change, a new manifest/corpus run, provider use, or
M18.

## Out of scope

Generic coordinate-system inference, arcs, splines, inner loops, Join/Cut,
multiple extrudes, corpus evaluation, provider use and DeepCAD admission.
