# WP-M4-002: P1 Parametric Case Expansion

- Status: done
- Milestone: M4
- Owner: unassigned

## Goal

Expand the manifest-driven corpus beyond P0 smoke fixtures with a small set of self-authored P1 parametric STEP cases that expose holes, chamfers/fillets, arrays, and boolean combinations.

## Scope

- Add deterministic P1 STEP fixtures generated from local OpenCascade scripts.
- Add local reference scripts for every P1 case so fake-provider replay remains network-free.
- Add a P1 manifest using the existing M4-001 schema.
- Add tests that load the P1 manifest and run it through `CorpusRunner`.
- Document the local P1 corpus command.

## Inputs

- `docs/architecture/v1/case-corpus-review.md`
- `docs/workpacks/done/WP-M4-001-case-corpus-manifest-and-runner.md`
- `case-library/manifests/self-authored/p0.json`
- `case-library/self-authored/<case_id>/reference_build_sequence.py`
- `case-library/self-authored/`
- `brep2code/corpus/`

## Code Paths

| Path | Purpose |
|------|---------|
| `case-library/self-authored/` | Self-authored P1 STEP fixtures |
| `case-library/manifests/self-authored/p1.json` | P1 case manifest |
| `case-library/self-authored/<case_id>/reference_build_sequence.py` | Local reference replacement scripts |
| `tests/` | Manifest and corpus runner tests |
| `docs/runbooks/` | Local case corpus review command |

## Trace/schema Changes

- No changes to `signal_bundle.json`, provider traces, tool traces, storage layout, or corpus report schema.
- Reuses the M4-001 manifest schema.

## Compatibility Constraints

- Keep existing P0 manifest and tests stable.
- Keep default corpus runs network-free and credential-free.
- Do not add hosted provider SDKs.
- Do not introduce IR, SDK, CAD workplace, or new geometry gates.
- Keep P1 fixtures small enough for routine local tests.

## Acceptance

- [x] P1 manifest loads and validates without network.
- [x] P1 fixtures include chamfer/fillet, hole array, and boolean combination coverage.
- [x] Every P1 case has a local reference script.
- [x] Corpus runner executes P1 cases through `ManualHarness`.
- [x] Fake-provider replay can repair at least one P1 failing default run.
- [x] `uv run python -m pytest` passes.
- [x] `uv run python -m ruff check .` passes.

## Result

- Added P1 STEP fixtures:
  - `case-library/self-authored/filleted_block/input.step`
  - `case-library/self-authored/chamfered_block/input.step`
  - `case-library/self-authored/three_hole_plate/input.step`
  - `case-library/self-authored/box_cylinder_union/input.step`
- Added P1 manifest: `case-library/manifests/self-authored/p1.json`.
- Added local reference scripts for all P1 cases under `case-library/self-authored/<case_id>/reference_build_sequence.py`.
- Added corpus tests for P1 manifest loading, P1 runner execution, and P1 fake-provider replay.
- Verified P1 CLI smoke:

```powershell
uv run python -m brep2code.cli corpus --manifest case-library\manifests\self-authored\p1.json --data-root data --report data\corpus-runs\p1-smoke.json
```

The smoke command returns non-zero because all primary P1 default runs currently fail M2 geometry gates, which is expected evidence: the default `build_sequence.py` still emits the P0 box.

- Verified:

```powershell
uv run python -m pytest
uv run python -m ruff check .
```

## Out of Scope

- Hosted LLM integration.
- Large external dataset ingestion.
- Benchmark claims.
- New geometry gates beyond current M2 gates.
- Committing to IR, SDK, or CAD workplace.

## Follow-Up

- `WP-M4-003-review-report-and-abstraction-decision` should use P0/P1 corpus evidence to classify failures and decide whether new abstractions are justified.