---
type: review
related-project: Brep2Code
status: completed
---

# M17-003 Review: Sketch-Frame Extrude-Direction Diagnostic

## Hypothesis

The fixed held-out Line3D replay mismatch might require both endpoint-continuous
loop ordering and extrusion along the sketch `y_axis`, rather than `z_axis`.
The experiment was limited to five preregistered rows: listed/`z_axis`,
ordered/`z_axis`, listed/`y_axis`, ordered/`y_axis`, and ordered/negative-
`y_axis`.

## Result

| Held-out treatment | bbox | volume | topology | Result |
|---|---|---|---|---|
| listed/`z_axis` | fail | fail | fail | rejected |
| ordered/`z_axis` | fail | fail | fail | rejected |
| listed/`y_axis` | pass | fail | fail | rejected |
| ordered/`y_axis` | pass | pass | pass | candidate |
| ordered/negative-`y_axis` | fail | pass | pass | rejected |

The candidate passed the fixed held-out case exactly, but it did not preserve
the existing controls. Applying its Line3D treatment made the M14 two
development controls and M17 Line3D development control degenerate; all three
had volume relative delta 1.0. The M14 and M17 Circle3D controls, which do not
use Line3D ordering, retained their strict-baseline pass outcomes.

## Decision

Reject `ordered_y` as a general replay mapping. It is evidence of a
case-specific coordinate-frame difference, not authority to alter the strict
parser. The production replay, manifests, corpus settings, gates, providers
and M18 selection remain unchanged. The ignored local evidence is
`data/fusion360-gallery-m17-frame-diagnostic/report.json` and can be
regenerated with `uv run python tools/diagnose_fusion360_m17_frame.py`.
