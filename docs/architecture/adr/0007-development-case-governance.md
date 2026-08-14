# ADR-0007: Development Case Governance Is Separate from Harness Runtime

- **Status**: Accepted
- **Date**: 2026-08-02

## Context

The committed P0/P1 STEP fixtures need durable, human-readable provenance and maintenance information as the self-authored corpus grows. Existing corpus manifests are executable inputs for `CorpusRunner`; they are not a suitable development-governance catalog, and treating a catalog as runtime material would blur the boundary between development agents and the Harness-invoked LLM.

## Decision

- Establish `docs/corpus/` as the development-only entry point for case registration, human review cards, and external-dataset registration.
- Keep numerical self-authored fixture baselines and file identities in `docs/corpus/registry/self-authored.json`; keep human case cards and catalog separate but linked.
- Retain existing `case-library/manifests/self-authored/p0.json` and `p1.json` as unchanged execution manifests. Registration does not add a case to a runtime run.
- Register external datasets and future sample-selection metadata without downloading, redistributing, executing, or injecting data into Harness.

## Consequences

- Developers can inspect case purpose, dimensions, provenance and maintenance history without reading STEP or runtime artifacts.
- The governance catalog is not a Harness API, prompt resource, tool resource, gate, CLI input or runtime LLM context.
- New fixture validation automation or external-dataset ingestion needs a separate workpack and may not be inferred from this decision.
