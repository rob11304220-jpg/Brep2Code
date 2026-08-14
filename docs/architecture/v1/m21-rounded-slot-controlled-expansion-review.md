---
type: review
related-project: Brep2Code
status: completed
---

# M21-002 Review: Rounded-Slot Controlled Expansion

## Scope and result

M21-002 executed exactly the six rows frozen by M21-001: the three existing
`rounded_slot` development variants and three new `offset_rounded_slot`
held-out experimental candidates.  The latter were produced twice by the
deterministic local producer; normalized STEP artifacts remained hash-stable.

All six passed deterministic geometry replay against their input STEP under
the existing bbox, volume, and topology gates.  Each passed the exact
four-operation `SketchRect -> ExtrudeBase -> SketchRoundedSlot -> CutThrough`
oracle and its three preregistered editability mutations.  Slot width and
straight-length mutations preserved the outer bbox while increasing removed
volume; base-length mutation increased the X extent and total volume.

Focused coverage rejects a rectangular-profile degeneration and a family split
leak.  Full offline validation passed: 88 pytest tests and Ruff.

## Interpretation

The three-layer contract is reproducible for one family that needs a second,
composite profile dependency.  It is stronger evidence than additional
prismatic-hole parameter variants, but it remains deterministic-oracle
evidence: it does not test provider generation, native-history recovery, or a
general B-Rep-to-sequence inverse.

## Governance disposition

Do not promote `rounded-slot-v1` metadata to the active case library yet.
The three new assets remain `experimental`, absent from the registry and every
manifest.  A separate governance review must compare M20 and M21 evidence,
including retained failure-taxonomy coverage, before proposing any ADR or
active-library admission.  No experience card was created.

M159 and ADR-0077 later restored this original experimental-only disposition
after a historical lifecycle promotion drift. The offset rows remain retained
candidate evidence, not active registry members.
