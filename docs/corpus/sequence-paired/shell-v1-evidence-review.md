# Shell-v1 Evidence Review (M132)

## Scope and inputs

This offline review covers only the six M130-frozen and M131-produced
experimental records: three `shell_symmetric` development rows and three
`shell_asymmetric` held-out rows. It reviews the preregistration, candidate
metadata, deterministic producer, family audit, and focused regression test.
It creates no candidate, manifest, runtime, provider, training, or hosted
artifact.

## Evidence that remains supported

- The fixed six-row 3/3 family-isolated split, frozen parameters, and declared
  logical sequence pass the generic intake audit.
- The six experimental STEP assets retain recorded hashes and pass the family
  geometry replay, one-solid volume, top-opening, uniform-wall/bottom-wall,
  bounding-box, editability, and negative-control checks.
- The family audit and focused regression test pass for all six rows.
- No `param_shell_*` identifier is present in the corpus registry, and the
  candidate metadata continues to declare exclusion from manifest, provider,
  training, and runtime paths.

## Counterexample and evidence limit

The declared Q02 action is `MakeThickSolidInward`, but
`tools/audit_sequence_paired_shell.py` implements `build_shape` with an outer
box minus an inner box through `BRepAlgoAPI_Cut`. The generated reference
scripts call that same `build_shape` function. Therefore, the recorded logical
sequence and matching final STEP geometry do **not** demonstrate that a native
thick-solid/shell operation was executed, replayed, or edited.

This is not a geometry failure: the six candidates remain valid evidence for
the constrained final geometry, fixed split, and semantic checks. It is a
counterexample to interpreting those facts as proof of the named native shell
construction operation. The review cannot establish generic shell recognition,
feature-history recovery, arbitrary openings or thicknesses, or runtime use.

## Disposition

**Retain all six records as experimental; do not propose promotion.** A future
workpack may be selected only to produce and independently verify a native
shell/thick-solid construction against the frozen M130 semantic contract. It
must not treat this review as authorization to modify the existing rows,
manifest, runtime, provider, training, or hosted paths.

## Independent review (2026-08-12)

Liaol independently approved this evidence boundary and the experimental-only,
no-promotion disposition. The review adds no authority beyond the stated
offline conclusion.

## Acceptance evidence (2026-08-12)

    uv run python tools\audit_sequence_paired_intake.py docs\corpus\sequence-paired\shell-v1-preregistration.json
    # passed: shell-v1 preregistration

    uv run python tools\audit_sequence_paired_shell.py
    # passed: 6 records

    uv run python -m pytest tests\test_sequence_paired_shell.py
    # passed: 1 test

    uv run python -m ruff check .
    # passed: All checks passed

    git diff --check
    # passed
