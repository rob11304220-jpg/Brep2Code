# WP-M14-001: Fusion 360 Minimal Native-History Replay

- Status: done
- Milestone: M14

## Result

Three fixed, family-isolated official samples were replayed locally from native
Fusion JSON to STEP. The development-only tool supports only a transformed
Line3D outer polygon or one Circle3D, followed by a zero-taper one-sided
NewBody distance extrude with cm→mm scaling. All three passed existing bbox,
volume and topology comparisons. No manifest, Harness corpus, provider request,
or runtime change was made.

## Evidence

- [Selection record](../../corpus/external/fusion360-gallery-r1.0.1-m14-001-selection.json)
- Ignored report: `data/fusion360-gallery-m14-replay/report.json`
- `100877_ac1e5a17_0001` maps 0.15875 cm to 1.5875 mm.

## Out of scope

Join/Cut, multiple extrudes, arcs/splines, holes/inner loops, manifests and any
hosted use require separate workpacks.
