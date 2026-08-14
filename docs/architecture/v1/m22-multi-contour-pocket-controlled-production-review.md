---
type: review
related-project: Brep2Code
status: completed
---

# M22-002 Review: Multi-Contour Pocket Controlled Production

## Scope and result

M22-002 produced exactly the six rows frozen by M22-001: three
`multi_contour_pocket_centered` development candidates and three
`multi_contour_pocket_offset` held-out candidates. Each candidate was built
twice in clean directories; normalized STEP bytes and SHA-256 were stable.

All six experimental candidates passed deterministic geometry replay under
the existing bbox, volume, and topology gates. Each candidate matched the
exact four-operation oracle `SketchRect -> ExtrudeBase ->
SketchPocketLoops(outer, inner) -> CutPocket(blind)`, passed four
preregistered editability mutations, and retained the operation-contract
checks: strict loop containment, one connected solid, base extents, blind
annular removed volume, outer rim, and inner island semantics.

Focused controls reject a single-loop sequence, non-contained inner loop, and
family split leak. The family audit, focused tests, full 45-record
case-library replay audit, Ruff, and `git diff --check` passed.

## Interpretation

This is reproducible self-authored deterministic-oracle evidence for one
bounded nested-rectangle blind-pocket grammar. It does not demonstrate
arbitrary multi-contour recognition, curved loops, multiple islands,
face/edge references, native history, B-Rep-to-sequence recovery, or a
generic CAD-kernel operation contract.

## Governance disposition

The six candidates remain `experimental`, absent from the case registry and
all executable manifests. M22-003 is the separately selected review that may
update the knowledge matrix, create a bounded knowledge unit or counterexample,
and decide only one constrained successor. No runtime experience card is
created.
