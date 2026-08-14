# ADR-0025: Preregister an Additive-Boss-Dependent-Cut Family Before Production

- **Status**: Accepted
- **Date**: 2026-08-05

## Context

The completed M22 family established a frozen two-loop profile dependency but
did not test an additive feature that becomes the explicit target for a later
cut. The coverage matrix still leaves downstream feature dependencies open.

ADR-0020 requires design/preregistration and controlled production to remain
separate. The external Q02 Zero-to-CAD case note at
`D:\paper\Projects\Brep2Code-research\cases\q02\ataeiZerotoCADAgenticSynthesis2026-案例.md`
supports this catalog-before-producer separation; it does not authorize its
agentic mining or training workflow here.

## Decision

Create M23-001 as an offline design-and-preregistration workpack for exactly
six `additive-boss-dependent-cut-v1` rows. The sole grammar is:

`SketchRect(base) → ExtrudeBase → SketchRect(boss) → ExtrudeBoss(join) → SketchCircle(cut) → CutCylinder(blind)`.

It freezes three centered development and three offset held-out family-isolated
rows, a deterministic-oracle provenance, geometry/sequence/editability checks,
semantic anti-degeneration predicates, rejection taxonomy, and producer
stability requirements. M23-001 may create planning records only. A separate,
user-selected M23-002 is required before candidate production.

## Consequences

- The project tests one additional explicit dependency chain without claiming
  face/edge-referenced history or B-Rep-to-sequence recovery.
- No case asset, executable manifest, provider input, training input, runtime
  resource, parser, helper, SDK, or IR changes in M23-001.
- A passing future producer remains experimental until a separately selected
  review and governance decision.
