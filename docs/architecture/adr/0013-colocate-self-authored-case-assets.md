# ADR-0013: Co-locate Self-Authored Case Assets and Metadata

- **Status**: Accepted
- **Date**: 2026-08-03
- **Context**: ADR-0012 established a locator index without moving assets. The self-authored corpus is still small (21 cases), and each case's input B-Rep, reference script, manifest entry, and detailed metadata remain physically separated. The user has explicitly requested a one-directory-per-case layout before the corpus grows.

## Decision

- This decision supersedes ADR-0012's retained-self-authored-fixture-location choice; ADR-0012's external-data and runtime-evidence boundaries remain in force.
- Move committed self-authored case assets to `case-library/self-authored/<case_id>/`.
- Each case directory contains `case.json`, `input.step`, and, when available, `reference_build_sequence.py`. `case.json` is the authoritative detailed metadata record for that case.
- Move executable self-authored manifests to `case-library/manifests/self-authored/`; update all manifests, tests, registry pointers, case cards, commands, and documentation to the new paths.
- Keep sandbox-only test helpers under `tests/fixtures/sandbox/`. Keep third-party raw data under ignored `data/datasets/<dataset>/<release>/`; it is not copied into the committed self-authored library.

## Rationale

The current corpus is small enough for a one-time, fully audited migration. Co-locating each case's geometry, deterministic construction reference, and complete metadata makes additions and maintenance less error-prone while preserving the separation between committed test assets, external licensed assets, and ignored runtime evidence.

## Consequences

- **Positive**: A single case directory is sufficient to inspect the exact B-Rep, available reference sequence, expected geometry, provenance, and tier.
- **Positive**: The library becomes the canonical location for future self-authored parameter families.
- **Negative**: Existing paths are intentionally changed, so tests, runbooks, manifests, and links must be updated together.
- **Mitigation**: Perform the migration mechanically, audit stale paths, verify every SHA-256, and run the complete test suite and Ruff.

## Alternatives Considered

| Alternative | Reason not selected |
|---|---|
| Retain only the locator index from ADR-0012 | Does not meet the requested per-case physical consolidation. |
| Copy assets into a new library while keeping old paths | Creates two fixture authorities and risks drift. |
| Move external raw datasets into the same tree | Violates source-license and Git-ignore boundaries. |
