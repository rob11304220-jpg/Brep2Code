---
type: review
related-project: Brep2Code
status: completed
---

# M17-005 Review: Fusion Line3D Frame Selector Promotion Validation

## Fixed validation

M17-005 remained offline and used exactly the four hash-linked Line3D cases
from M17-004: development `100243_9fb796fe_0005`,
`100877_ac1e5a17_0001`, `145540_a4f54d5f_0010`, and held-out
`41026_295d1dc8_0003`. No sample, split, manifest, source scan, gate or
feature subset changed.

The focused pure-selector test passed 3/3 cases: a unique lower-boundary
choice, an ambiguity rejection without a fallback, and an upper-boundary
negative sign. The ignored local matrix written by
`uv run python tools/replay_fusion360_m17_selector.py` reproduced the
preregistered strict baseline and then applied the explicit selector.

| Mapping | Development (3) | Held-out | Result |
|---|---:|---:|---|
| strict listed-order / `z_axis` | 3/3 gate pass | gate fail | Preserved baseline |
| endpoint-ordered selector | 3/3 gate pass | gate pass | Passed bbox, volume, topology |

## Decision

The profile-normal / STEP-projection / extent-boundary selector is validated
only for this explicit four-case subset. The default strict `replay()` path is
unchanged. `replay_line3d_selector()` is candidate-only and is called only by
the fixed local matrix tool; it has no fallback and rejects ambiguous,
non-boundary or unsupported input.

This result is not a generic Fusion parser or mapping-policy decision. It does
not authorize a corpus run, provider or hosted execution, new cases, manifests,
syntax, gates, prompt/tool changes or M18. Any possible further promotion must
be selected by a separate review/workpack.
