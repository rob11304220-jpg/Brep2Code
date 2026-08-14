# Corpus Module

## Responsibility

`brep2code/corpus/` owns manifest-driven case review and the M6-001 hosted-evaluation boundary.

It should:

- load and validate small case manifests
- resolve repository-relative fixture and reference script paths
- run each case through `ManualHarness`
- optionally replay fake-provider repair when a case provides a reference replacement script
- in explicit `--first-pass` mode, generate the initial script from a bounded B-Rep summary and record it separately from repair/replay
- in explicit, bounded hosted mode, repair failed primary cases through the configured provider and secure executor
- atomically checkpoint compact corpus reports after every completed case, retaining partial evidence on handled interruption

## Boundary

The corpus module is not a dataset ingestion system and does not make benchmark claims. Default execution must not call hosted LLMs. Hosted evaluation is DeepSeek-only for M6-001, requires explicit CLI authorization plus case/round/request bounds, and must use `wsl-bwrap`; it should not download external data, define new CAD abstractions, or add geometry gates without a separately approved workpack.

## Public Entry

Implemented M4 entries:

| Entry | Purpose |
|-------|---------|
| `load_case_manifest(path)` | Load and validate case definitions |
| `CorpusRunner` | Execute manifest cases through the Harness |
| `write_corpus_report(...)` | Persist compact summary output |
| `python -m brep2code.cli corpus ...` | Run manifest-driven batch review |

Hosted evaluation adds `--provider deepseek --authorize-hosted --max-cases N --max-rounds N --request-budget N`; `--first-pass` is an explicit mode and uses `first_pass_script` fixtures with the local fake provider. First-pass reports use schema v3 while existing reports retain v1/v2 compatibility; see the provider runbook for the manual authorization gate.

## Runtime Paths

| Path | Use |
|------|-----|
| `case-library/manifests/self-authored/` | P0--P3 executable self-authored manifests |
| `case-library/self-authored/<case_id>/` | Complete self-authored case metadata, STEP input, and optional reference script |
| `case-library/test-support/` | Non-case corpus test helpers |
| `data/records/` | Per-case Harness records |
| `data/corpus-runs/` | Optional corpus-level reports |
| `docs/corpus/external/` | Tracked external-source selection metadata and explicit local manifests; not runtime material |
| `docs/corpus/library/` | Development-only locator for source/case relationships and candidate admission order; not runtime material |

## Contract

Manifest and report fields are defined in [`docs/architecture/v1/contracts/case-corpus.md`](../architecture/v1/contracts/case-corpus.md).

External manifests are opt-in local-development inputs. Their STEP files live only under ignored `data/datasets/`; ordinary corpus commands and tests neither download nor discover them.

The [unified case library](../corpus/library/README.md) deliberately indexes, rather than relocates, committed fixtures, ignored external assets, and ignored runtime evidence. It does not change the manifest resolver or make `brep2code/corpus/` a dataset-ingestion system.

M9-001 uses separate explicit 8-case development and 4-case held-out manifests for the M8 ABC selection. This is manifest-only governance: it does not add split-selection behavior to `CorpusRunner` or alter the hosted schema-v3 interface. Each hosted split remains separately authorized and uses the existing secure provider path.

M9-002 routes first-pass input summaries through the shared bounded probe helper before constructing a provider request. An unavailable input is an `input_probe_failure` with zero request use, rather than a provider failure or an unbounded pre-request operation.

## Acceptance

M4 should keep the default path network-free:

```powershell
uv run python -m brep2code.cli corpus --manifest case-library\manifests\self-authored\p0.json --data-root data
uv run python -m brep2code.cli corpus --manifest case-library\manifests\self-authored\p1.json --data-root data
uv run python -m brep2code.cli corpus --manifest case-library\manifests\self-authored\p2.json --repair --data-root data
uv run python -m brep2code.cli corpus --manifest case-library\manifests\self-authored\p3.json --repair --data-root data
uv run python -m pytest
uv run python -m ruff check .
```