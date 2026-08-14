# WP-M17-007: Restricted Line3D Default Mapping Policy

- Status: done
- Milestone: M17
- Owner: unassigned

## Goal

Review the completed M17-005/006 selector evidence and, if sufficient, adopt
one fail-closed default mapping for the already supported Fusion Line3D subset.

## Scope

- Use only the completed five development/two held-out selector rows.
- Make the selector the default only for one transformed Sketch,
  profile-plane start, one zero-taper one-sided NewBody distance extrude and
  one Line3D outer loop.
- Preserve Circle3D, existing gates, historical comparison support and all
  Harness/runtime/provider boundaries.

## Acceptance

- Record a lasting policy decision in an ADR and review.
- Reject Line3D replay without an input bbox, a unique axis or a supported
  closed loop; do not add a fallback.
- Re-run M14, M17, M17-005 and M17-006 offline matrices plus focused tests and
  Ruff.
- Update status, roadmap, workpack index, handoff and the evidence-reuse
  disposition.

## Result

Completed. ADR-0017 adopted the frozen selector as the narrow default and
retained `replay_strict()` for comparison only.  All required local matrices
passed.  No experience card was created because this parser-local mapping is
not runtime guidance.

## Out of scope

New Fusion syntax, other operations or curve types, fallback/healing,
Harness/CLI/corpus/provider changes, runtime retrieval, M18 and hosted work.
