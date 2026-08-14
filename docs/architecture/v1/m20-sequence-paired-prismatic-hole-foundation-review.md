---
type: review
related-project: Brep2Code
status: completed
---

# M20-001 Review: Sequence-Paired Prismatic-Hole Foundation

## Scope and result

M20-001 preregistered three existing self-authored cases without copying their
STEP assets: development `block_with_hole` (through) and
`counterbored_plate` (counterbore), plus family-isolated held-out
`blind_hole_block` (blind).  The seed record preserves their case-record paths,
input hashes, split, family, and the normalized `prismatic-hole-v1` sequence.

The offline audit passed all three cases.  For each, deterministic OCP replay
produced a readable STEP with zero bbox delta, zero volume delta, and exact
solid/shell/face/edge counts against its committed input.  Each case also
passed two preregistered mutations: base-length change altered the X extent and
increased volume; hole radius or depth change preserved the outer bbox and
decreased volume.  The focused suite passed 5 tests; the full repository suite
passed 80 tests and Ruff passed.

## Interpretation

The pilot contract is coherent enough to support a separately scoped,
controlled-expansion proposal.  It has demonstrated that the three layers can
be represented and checked offline for this restricted family.

It does **not** validate B-Rep-to-sequence inference, a provider-generated
sequence, a native-history translation, or a generic construction-history
claim.  All three oracles are reviewed normalizations of self-authored OCP
reference scripts.  Exact sequence agreement currently proves candidate/oracle
comparison semantics through focused tests; it is not a model-quality result.

## Governance disposition

Do not promote the pilot metadata, three-layer evidence, or candidate producer
to the global case-library contract.  A later workpack must first preregister a
larger controlled expansion, retain whole-family held-out cases, include the
same audit, and separately review producer/admission governance.  Until then,
ADR-0014 remains the only long-term case-library contract.

No experience card was created: the result is a restricted development-side
foundation, not reusable runtime evidence under ADR-0016.
