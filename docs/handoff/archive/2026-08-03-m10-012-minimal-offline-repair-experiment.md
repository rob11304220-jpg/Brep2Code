# Handoff: M10-012 minimal offline sandbox-path repair experiment

- **Date**: 2026-08-03
- **Subproject**: `brep2code`
- **Status**: `completed`

## Goal

Test the two direct sandbox input-path failures with fixed local scripts, preserving a non-matching import-failure control and all existing Harness evidence.

## Done

- `00000027` and `00000031` host-path baselines reproduced the expected unreadable-path failure through `wsl-bwrap`.
- Replacing only the input with `/input/model.step` produced readable output for both cases.  `00000031` passed all existing gates; `00000027` retained only a strict bbox delta of `0.00016` while its volume and topology gates passed.
- The `00000030` corrected-path control retained the unavailable `Interface_Static_SetCVal` import failure and generated no output.
- The review, ledger, roadmap, workpacks, workpack index, and status page record the bounded conclusion.  No provider request, runtime, CLI, manifest, schema, prompt, probe, gate, or production-helper change occurred.

## Next

No workpack is active.  Any future work must begin from `docs/workflow/status.md` and satisfy ADR-0010's evidence-gated routing.

## Key paths

- `docs/architecture/v1/m10-012-minimal-offline-path-repair-review.md`
- `docs/architecture/v1/m10-external-attribution-ledger.md`
- `tests/fixtures/sandbox/m10_012_*.py`
