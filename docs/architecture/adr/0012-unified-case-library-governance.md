# ADR-0012: Establish a Unified Development Case-Library Index

- **Status**: Accepted
- **Date**: 2026-08-03
- **Context**: The committed self-authored STEP fixtures and reference scripts are intentionally located under `tests/fixtures/`, external raw assets are intentionally ignored under `data/datasets/`, and execution evidence is intentionally ignored under `data/records/` and `data/corpus-runs/`.  These boundaries are correct, but developers currently need to cross-reference several locations to determine whether an input B-Rep has a reference sequence, an external source, or only runtime evidence.

## Decision

- Establish `docs/corpus/library/` as the tracked, development-only unified index for case sources, candidate datasets, asset roles, and planned admission order.
- Retain existing asset locations and manifests.  The library is a locator and governance layer, not a copied asset store, a Harness manifest, or a runtime prompt resource.
- Treat a case as a relationship among an input B-Rep, optional reference/ground-truth sequence, optional intermediate states, and optional execution evidence.  The index records the authoritative location for each role.
- Admit future datasets in the indexed candidate order only through a dedicated offline workpack: license and version review, small deterministic sample selection, asset-pair audit, and existing-Harness replay.  Download, provider use, and automatic fixture promotion remain out of scope.

## Rationale

Keeping committed fixtures in `tests/fixtures/` preserves current test paths and reproducibility; keeping third-party raw data ignored preserves license and redistribution boundaries.  A tracked index resolves the discoverability problem without turning development governance into Harness runtime input or requiring a premature general IR/dataset-ingestion subsystem.

## Consequences

- **Positive**: Every source has one discoverable catalog entry, a data-role declaration, and an explicit next-admission condition.
- **Positive**: Candidate datasets with construction history can be planned beside ABC without pretending that ABC has ground-truth sequences.
- **Negative**: The index adds a small maintenance obligation whenever a source or self-authored case family changes.
- **Mitigation**: The maintenance runbook and admission template make those updates explicit; a future validation command needs its own workpack.

## Alternatives Considered

| Alternative | Reason not selected |
|---|---|
| Move all fixtures and raw datasets into one physical directory | Breaks stable test paths and risks mixing tracked, ignored, and license-restricted assets. |
| Keep only per-dataset documents | Does not provide one machine-readable inventory or an admission queue. |
| Add a production dataset-ingestion module now | Expands Harness/runtime scope before the offline feasibility evidence exists. |
