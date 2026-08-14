---
type: review
related-project: Brep2Code
status: completed
---

# M17-002 Review: Line3D Loop-Ordering Offline Repair

## Hypothesis

The held-out M17 Line3D curve list is non-continuous. The experiment tested
whether ordering the existing segments by matching endpoints, including segment
reversal, would repair the strict replay without accepting another curve type
or operation.

## Result

Rejected. The treatment wrote a readable STEP but did not repair geometry:

| Evidence | Strict baseline | Endpoint-order treatment |
|---|---:|---:|
| bbox max delta | 1016 mm | 1016 mm |
| volume relative delta | 1.0 | 1.0 |
| topology total absolute delta | 13 | 11 |

M14's three controls and M17's two development controls all remained gate-pass.
The experiment then restored the original strict replay implementation and
regenerated the baseline M17 report.

## Decision

Non-continuous Line3D order is an observed symptom, not a sufficient root
cause. Do not promote the treatment, change parser behavior, expand manifests,
replace the held-out control, or open M18. Any future investigation must be
separately scoped around coordinate-frame/extrude-direction semantics and must
retain this held-out case as a control.
