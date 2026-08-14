# WP-M4-001: Case Corpus Manifest + Runner

- Status: done
- Milestone: M4
- Owner: unassigned

## Goal

Create the first manifest-driven case corpus workflow so the current Harness-first loop can be reviewed across small deterministic cases before adding hosted provider integration or new modeling abstractions.

## Scope

- Define a minimal case manifest schema for P0 cases.
- Register existing smoke fixtures: `box`, `cylinder`, and `block_with_hole`.
- Add a corpus runner that executes `ManualHarness` for each case and writes a compact report.
- Record per-case revision id, status, gate statuses, probe summaries, and failure type.
- Support optional fake-provider repair replay when a case has a reference replacement script.
- Keep all tests and default runs network-free.
- Document how to run the corpus review locally.

## Inputs

- `docs/architecture/v1/case-corpus-review.md`
- `docs/workpacks/done/WP-M1-001-brep-probe-tools.md`
- `docs/workpacks/done/WP-M2-001-cad-output-gates.md`
- `docs/workpacks/done/WP-M3-003-repair-loop-runner.md`
- `case-library/self-authored/`
- `brep2code/agent/`
- `brep2code/cli/`

## Code paths

| Path | Purpose |
|------|---------|
| `cases/` or `case-library/manifests/self-authored/` | case manifest and optional reference scripts |
| `brep2code/corpus/` | manifest loading, validation, runner, report helpers |
| `brep2code/cli/` | corpus command entry |
| `data/corpus-runs/` or `data/records/` | local run outputs |
| `tests/` | manifest and corpus runner tests |
| `docs/runbooks/` | local case corpus review command |

## Docs to update

| Path | Purpose |
|------|---------|
| `docs/modules/corpus.md` | corpus module boundary and entrypoints |
| `docs/modules/README.md` | module index status |
| `docs/architecture/v1/contracts/case-corpus.md` | manifest and compact report contract |
| `docs/runbooks/case-corpus-review.md` | local run instructions |
| `docs/workflow/README.md` | active/done status when workpack completes |

## Trace/schema changes

- Adds case manifest schema and corpus compact report schema.
- Does not change `signal_bundle.json`, provider traces, tool traces, or storage revision layout unless explicitly documented in `docs/architecture/v1/contracts/case-corpus.md`.

## Compatibility constraints

- Keep existing `run`, `probe`, and `repair` CLI behavior stable.
- Keep default corpus runs network-free and credential-free.
- Do not add hosted provider SDKs in this workpack.
- Do not introduce IR, SDK, CAD workplace, or new geometry gates beyond current M2 gates.

## Acceptance

- [x] Manifest schema can load and validate P0 cases without network.
- [x] Existing smoke fixtures are represented as cases.
- [x] Corpus runner executes each case through `ManualHarness`.
- [x] Report includes case id, tier, revision id, status, gate statuses, and failure classification.
- [x] Optional fake-provider repair replay is supported for cases with reference scripts.
- [x] Existing `run`, `probe`, and `repair` CLI paths remain usable.
- [x] `uv run python -m pytest` passes.
- [x] `uv run python -m ruff check .` passes.

## Result

- Added `brep2code/corpus/` with manifest loading, validation, runner, and compact report writing.
- Added P0 manifest at `case-library/manifests/self-authored/p0.json` for `box`, `cylinder`, and `block_with_hole`.
- Added local reference scripts for `cylinder` and `block_with_hole` fake-provider repair replay.
- Added CLI command:

```powershell
uv run python -m brep2code.cli corpus --manifest case-library\manifests\self-authored\p0.json --data-root data
```

- Verified:

```powershell
uv run python -m pytest
uv run python -m ruff check .
```

## Out of scope

- Hosted LLM integration.
- Large external dataset ingestion.
- Benchmark claims.
- New geometry gates beyond current M2 gates.
- Committing to IR, SDK, or CAD workplace.

## Follow-up workpacks

- `WP-M4-002-p1-parametric-case-expansion` for holes, chamfers, arrays, and boolean combinations.
- `WP-M4-003-review-report-and-abstraction-decision` for summarizing failures and deciding whether IR/SDK/CAD workplace is justified.