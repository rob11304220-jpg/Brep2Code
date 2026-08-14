---
type: review
related-project: Brep2Code
status: completed
---

# M17-004 Review: Fusion Line3D Frame-Evidence Audit

## Fixed evidence

The audit remained offline and exhaustive over exactly four hash-linked Line3D
cases: M14 development `100243_9fb796fe_0005` and
`100877_ac1e5a17_0001`, M17 development `145540_a4f54d5f_0010`, and M17
held-out `41026_295d1dc8_0003`. It read existing native-history JSON and
input STEP bbox probes only; it did not run a replay treatment.

| Case | Listed loop | Ordered loop normal | Source extent | Matching STEP projection | Selected direction |
|---|---|---|---:|---|---|
| `100243_9fb796fe_0005` | continuous | `z_axis` | 200 mm | `z_axis` | `+z_axis` |
| `100877_ac1e5a17_0001` | continuous | `z_axis` | 1.5875 mm | `z_axis` | `+z_axis` |
| `145540_a4f54d5f_0010` | continuous | `z_axis` | 12.7 mm | `z_axis` | `+z_axis` |
| `41026_295d1dc8_0003` | non-continuous | `y_axis` | 1016 mm | `y_axis` | `+y_axis` |

All transforms are normalized orthonormal right-handed frames. The held-out
loop can be endpoint-ordered unambiguously, and the observed non-continuous
listed order does not itself select an extrusion direction.

## Candidate selector

Within the already supported one transformed Line3D outer-loop / zero-taper
one-sided distance-extrude subset, select the unique sketch axis meeting all
three conditions:

1. Its direction is parallel to the endpoint-ordered profile normal.
2. The input STEP bbox span projected on that axis equals the source extent
   magnitude after cm-to-mm normalization.
3. The transformed profile lies on a boundary of that projection; use the
   lower boundary for `+axis` and the upper boundary for `-axis`.

Every fixed case has exactly one match. This distinguishes `+y_axis` in the
held-out case while retaining `+z_axis` for all three development controls.

## Decision

Nominate the explicit selector for a **separate** promotion workpack only.
This is evidence for a bounded candidate, not a mapping-policy decision or a
parser change. M17-003 remains controlling non-regression evidence: the
unconditional `ordered_y` treatment repaired the held-out case but degenerated
all three Line3D controls. Any promotion workpack must retain these four
hash-locked cases, preregister the selector and existing gates, and preserve
the current strict replay until its controls pass.

The ignored, reproducible local evidence is written by
`uv run python tools/audit_fusion360_m17_frame.py` to
`data/fusion360-gallery-m17-frame-evidence/{report.json,report.md}`.
