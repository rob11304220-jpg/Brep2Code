# ADR-0014: Define the Maintainability Contract for the Development Case Library

- **Status**: Accepted
- **Date**: 2026-08-03

## Context

ADR-0012 created a development-side index and ADR-0013 consolidated self-authored assets into one directory per case.  The library now has both the migrated capability ladder and parameter-family cases.  Its next growth steps need explicit rules for authority, lifecycle, split isolation, validation, and source boundaries so that a larger library does not drift into duplicated fixtures or unreviewed runtime inputs.

## Decision

- Keep the filesystem as the asset authority: `case-library/self-authored/<case_id>/case.json` owns self-authored identity, asset hashes, reference-script declaration, and numerical baseline.  The registry remains a routing/pointer index; manifests remain explicit executable selections.
- Require an immutable `case_id`, a versioned metadata contract, declared asset roles, and an explicit lifecycle.  Retire or replace a case through metadata and documentation rather than silently reusing its identifier.
- Keep parameter families wholly within one declared split.  External sources remain separately licensed, ignored raw data; their tracked records are locators and admission evidence, not copied fixtures.
- Treat hash, manifest, split, path, and optional replay checks as required offline validation.  Runtime records/reports may reference a case but never become its fixture authority.
- Do not add a database now.  JSON metadata plus validation remains the transparent source of truth; reconsider an index database only when library scale or query/concurrency needs cannot be met by the checked-in index and audit tooling.

## Consequences

- **Positive**: Case additions and deprecations have a predictable, auditable path while keeping Harness input explicit.
- **Positive**: Data-license, split-isolation, and historical-evidence boundaries remain visible in the repository layout.
- **Cost**: Maintainers must update metadata, routing records, and validation evidence together.
- **Guardrail**: The maintenance runbook specifies the required update and validation sequence.
