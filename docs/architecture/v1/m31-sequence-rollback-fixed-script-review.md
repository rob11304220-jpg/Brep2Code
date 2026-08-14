# M31 Verified-Prefix Fixed-Script Rollback Review

## Result

Both preregistered nominal additive-boss rows—one development and one
held-out—passed the isolated rollback experiment. The baseline retained
`after-base.step`, `after-boss.step` and `after-cut.step`. A cut depth equal to
boss height was recorded as a suffix-only defect after the boss prefix. The
experiment then copied the verified `after-boss.step` artifact and regenerated
only the canonical cut suffix; all existing final geometry gates passed.

The early-defect control stops before an `after-boss.step` artifact exists and
therefore returns `unsupported` rather than attempting rollback.

## Critical artifact boundary

Writing the same in-memory boss shape twice does not reliably preserve a STEP
SHA-256 because exporter header metadata can differ. Thus a verified prefix is
the retained baseline artifact itself, not a geometrically equivalent
re-export. This is a necessary condition for the M31 claim.

## Boundary

The result is only an offline, fixed-reference artifact experiment. It does
not support automatic runtime rollback, repair of provider-generated scripts,
B-Rep history recovery, a public Harness trace schema, helper/IR/SDK work or a
change to any manifest, provider, parser or gate.
