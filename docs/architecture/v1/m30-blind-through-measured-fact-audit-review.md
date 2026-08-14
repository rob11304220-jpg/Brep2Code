# M30 Blind/Through Measured-Fact Audit Review

## Result

The offline M30 reporter classified all three frozen through development
records and all three frozen blind held-out records without consuming their
reference-script variant as an input. It measured the single cylindrical face,
its +Z axis, face-edge-face adjacency, and adjacent planar XY footprints. The
three counterbore controls have two cylindrical faces and therefore returned
`unsupported` before any extent decision.

## Bounded observable

| Measured terminal facts | Result |
|---|---|
| One local planar footprint and one exterior-sized planar footprint | `blind` |
| Two exterior-sized planar footprints | `through` |
| Different cylinder count, axis, terminal cardinality or footprint pattern | `unsupported` |

The local-footprint bound is 1.25 times the measured cylinder diameter. It is
a frozen M30 convention, not a general geometry tolerance or feature rule.

## Boundary

This is a development-side offline audit, not a public probe expansion. It
does not establish generic cylindrical-feature recognition, non-+Z axes,
multiple cylinders, imported trimming behavior, original CAD history, runtime
guidance, a helper, manifest use, provider input, or a repair action.
