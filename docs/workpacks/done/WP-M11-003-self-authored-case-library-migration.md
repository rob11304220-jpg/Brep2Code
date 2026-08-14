# WP-M11-003: Self-Authored Case-Library Migration

- Status: done
- Milestone: M11
- Owner: unassigned

## Goal

Physically consolidate every committed self-authored case so that its complete metadata, input STEP, and optional deterministic reference script live in one canonical case directory.

## Scope

- Move the 21 committed self-authored STEP fixtures and associated reference scripts to `case-library/self-authored/<case_id>/`.
- Create a complete `case.json` beside each case's assets; convert the development registry to a pointer index.
- Move p0--p3 manifests to `case-library/manifests/self-authored/` and update all internal references, case cards, tests, commands, and documentation.

## Trace/schema changes

No runtime report or trace schema changes. Manifest paths change, but existing manifest fields and `CorpusRunner` behavior remain unchanged.

## Compatibility constraints

- Default commands stay offline.
- Raw external datasets, sandbox fixtures, provider policy, gates, CLI semantics, and record layout are unchanged.
- No duplicate old/new fixture assets remain after migration.

## Acceptance

- Every self-authored case directory has `case.json` and `input.step`; all except the default `box` baseline have a reference script.
- Every `case.json` SHA-256 matches its co-located `input.step`.
- All p0--p3 manifests resolve and all committed references point to the canonical case-library layout.
- `uv run python -m pytest` and `uv run python -m ruff check .` pass.

## Out of scope

External dataset download/admission, source-history translation, hosted evaluation, raw-data relocation, and changes to corpus schemas or gates.

## Completion

Completed offline on 2026-08-03. All 21 self-authored cases now have co-located `case.json` and `input.step`; 20 have `reference_build_sequence.py`, while `box` remains the documented default-scaffold baseline without one. P0--P3 manifests, tests, case cards, module docs, commands, and the pointer registry now target `case-library/`. The legacy self-authored `tests/fixtures/brep/` and `tests/fixtures/cases/` paths were removed after asset verification; sandbox fixtures remain in place. SHA-256 audit passed for every case; `uv run python -m pytest` reported 68 passed and `uv run python -m ruff check .` passed.
