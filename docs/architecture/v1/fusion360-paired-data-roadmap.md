---
type: roadmap
related-project: Brep2Code
version: v1
status: active
tags:
  - Brep2Code
  - Fusion360
  - case-library
  - paired-data
---

# Fusion-first Paired-Data Route

## Purpose

This route turns the completed M14 native-history replay evidence into a
bounded, sequence-supervised case-library decision. It supplements the
case-library admission order; `docs/workflow/status.md` remains the source of
truth for the current work.

## Current evidence

M12 reviewed Fusion 360 Gallery Reconstruction r1.0.1's source and license;
M13 verified the ignored local archive/cache; and M14 replayed a fixed,
source-family-isolated 2 development/1 held-out subset from native JSON to
STEP. All three cases passed existing bbox, volume, and topology gates.

That evidence is limited to one Sketch followed by one zero-taper NewBody
extrude, with a transformed Line3D outer polygon or one Circle3D and cm-to-mm
normalization. It does not establish support for Join/Cut, multiple extrudes,
arcs/splines, inner loops, or hosted evaluation.

## Conditional route

1. **M15 review** — completed: it approved M16 only, while creating neither a
   Fusion manifest nor a corpus run.
2. **M16 local control** — completed: separate development/held-out manifests
   passed path, hash, official split/family-isolation and no-script-fixture
   checks. They remain non-default and receive no provider data.
3. **M17 bounded Fusion expansion** — M17-001 completed and stopped at its
   fixed bound: two development cases passed, while the held-out Line3D case
   exposed a replay mismatch. M17-002's separate endpoint-ordering experiment
   did not repair it. M17-003's only held-out passing row (`ordered_y`)
   regressed all three Line3D controls, so the strict replay remains unchanged.
   M17-004 is completed: its fixed four-case audit nominated a combined
   profile-normal / STEP-projection / extent-boundary selector for a separate
   promotion workpack, but did not change replay behavior. M17-005 completed
   its preregistered validation: the strict baseline retained three
   development passes and the held-out failure, while the candidate selector
   passed all existing gates for the same fixed four cases. Strict replay
   remains the default; no replacement, scan extension or operation expansion
   is allowed. M17-006 then selected a preregistered, independent 2
   development/1 held-out Line3D population from the existing cache. The
   frozen selector passed all three rows, including one development row where
   strict replay failed volume and topology gates. M17-007 then adopted that
   frozen, fail-closed selector as the default only for the already supported
   Line3D subset: one transformed Sketch, profile-plane start, one zero-taper
   one-sided NewBody distance extrude, and one outer loop. Circle3D retains
   its strict path; ambiguous or unsupported Line3D input rejects. This is
   not generic Fusion parser support or a Harness/runtime behavior change.
   M17-008 then independently confirmed the unchanged default on two further
   development families and one held-out family. The cumulative result is
   seven development and three held-out gate passes, still within the same
   restricted mapping boundary.
4. **M18 DeepCAD audit** — not selected. The M17 mismatch is a narrow local
   replay-mapping issue, not evidence that Fusion lacks a paired-data source;
   a second dataset would not answer it.

## Position in the coverage route

Under ADR-0021, further Fusion selection is not the immediate next action.
First close M21-004 and establish self-authored multi-contour and dependency
evidence. Only a later, explicitly selected external-validation workpack may
extend Fusion within its already supported boundary; DeepCAD admission follows
that work, and BRep2Seq synthetic admission follows DeepCAD. This order does
not authorize a download, scan, manifest change, or provider request.

## Boundaries

- A manifest is an explicit selection, not automatic activation, fixture
  discovery, provider authorization, or a benchmark claim.
- External raw data and derived replay artifacts stay ignored under `data/`
  and remain subject to their source licenses.
- Any hosted execution needs its own preregistered workpack, successful
  preflight, and separate explicit authorization for development and held-out
  splits.
- ABC remains B-Rep-only OOD robustness material; it cannot replace a native
  history source for paired-data evidence.

## Related records

- [M15 review record](fusion360-m15-manifest-admission-review.md)
- [M16 review record](fusion360-m16-local-control-review.md)
- [M17 review record](fusion360-m17-bounded-expansion-review.md)
- [M17-002 review record](fusion360-m17-loop-ordering-repair-review.md)
- [M17-003 review record](fusion360-m17-frame-diagnostic-review.md)
- [M17-004 review record](fusion360-m17-frame-evidence-audit-review.md)
- [M17-005 review record](fusion360-m17-selector-promotion-validation-review.md)
- [M17-006 review record](fusion360-m17-independent-line3d-selector-validation-review.md)
- [M17-006 selection](../../corpus/external/fusion360-gallery-r1.0.1-m17-006-selection.json)
- [M17-007 review record](fusion360-m17-restricted-default-mapping-review.md)
- [M17-008 selection](../../corpus/external/fusion360-gallery-r1.0.1-m17-008-selection.json)
- [M14 selection](../../corpus/external/fusion360-gallery-r1.0.1-m14-001-selection.json)
- [case-library admission order](../../corpus/library/README.md)
