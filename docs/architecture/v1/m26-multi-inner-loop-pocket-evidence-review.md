---
type: review
related-project: Brep2Code
status: completed
---

# M26-003 Review: Multi-Inner-Loop Pocket Evidence

## Result

M26 produced exactly three centered development and three offset held-out
deterministic-oracle candidates. All six are hash-stable and passed existing
geometry replay gates, the exact four-operation outer-plus-two-inner-loop
sequence, six directional editability mutations, blind removed-volume and
outer-extent invariants, one-solid checks, and family-isolated splits.

## Interpretation

The evidence supports only the frozen rectangular `multi-inner-loop-pocket-v1`
grammar: one outer loop, exactly two non-overlapping contained inner islands,
and one blind cut. It extends M22's single-inner-island grammar but does not
establish arbitrary loop count/geometry, rotated or curved profiles, generic
multi-contour recognition, face/edge references, native history,
B-Rep-to-sequence recovery, runtime guidance, or IR.

## Disposition

Select only M26-004, a separate family-specific governance-promotion proposal.
The candidates remain experimental and outside the registry and every
executable manifest pending that workpack and its ADR.
