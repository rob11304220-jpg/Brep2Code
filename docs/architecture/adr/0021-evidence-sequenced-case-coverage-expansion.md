# ADR-0021: Sequence Case-Coverage Expansion by Governance, Self-Authored Evidence, and External Validation

- **Status**: Accepted
- **Date**: 2026-08-04

## Context

The active self-authored library covers primitive, additive/subtractive,
fillet/chamfer, hole, slot, parameter-variation, and two deterministic-oracle
sequence-paired families. The next technical gaps are multi-contour sketch
topology and feature dependency. External sources provide complementary native
history or B-Rep-only evidence, but their license, vocabulary, and replay
compatibility can obscure those gaps if introduced before a controlled local
family establishes an auditable contract.

## Decision

Proceed in this order:

1. complete M21-004, the bounded governance decision for the already audited
   `rounded-slot-v1` records;
2. select M22-000 to establish the modeling knowledge system and coverage
   matrix before a new family is designed;
3. select M22-001 to preregister a self-authored multi-contour pocket family:
   `Sketch(outer + inner loop) -> ExtrudeBase -> CutPocket`;
4. run a separate M22-002 controlled-production/audit workpack and a separate
   M22-003 cross-family review before any governance promotion;
5. only after that review, select a self-authored dependency-focused family,
   such as an additive boss followed by a dependent cut; and
6. only after evidence exists for the dependency family, consider external
   routes in this order: constrained Fusion native-history validation, DeepCAD
   admission and deterministic replay, then BRep2Seq synthetic admission.

ABC remains B-Rep-only robustness material and may receive a small deterministic
increment only when the attribution route selects it. It is not a substitute
for sequence-supervised evidence.

## Consequences

- M21-004 is governance closure, not an implicit expansion of the grammar or
  a claim of general sequence recovery.
- Every new self-authored family continues to use ADR-0020's distinct design
  and controlled-production workpacks, family-isolated splits, deterministic
  replay, exact sequence/dependency evidence, editability mutations, and
  semantic anti-degeneration checks.
- M22-000 is a documentation and evidence-organization foundation. It does
  not convert development knowledge into runtime material or alter M19's
  retrieval threshold.
- No external download, asset selection, manifest activation, hosted/provider
  request, training input, parser/helper/SDK, or runtime change is authorized
  by this decision. Each external route needs its own selected workpack and
  applicable approval.
- Arc/spline profiles, multiple extrudes, Join/Cut, patterns, revolve/sweep/
  loft, multi-solid behavior, and near-degenerate parameter cases remain
  documented future coverage gaps; they are not automatically scheduled.
