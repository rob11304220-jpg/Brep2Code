# Handoff: unified self-authored case library

- **Date**: 2026-08-03
- **Subproject**: `brep2code`
- **Status**: done

## Goal

Create a maintainable development-side case library, then physically consolidate the small self-authored corpus before admitting any sequence-supervised external dataset.

## Done

- Added ADR-0012, `docs/corpus/library/` catalog and admission template, and a case-library maintenance runbook.
- Moved all 21 self-authored inputs to `case-library/self-authored/<case_id>/input.step`; each now has an authoritative co-located `case.json` and 20 have `reference_build_sequence.py`.
- Moved P0--P3 manifests to `case-library/manifests/self-authored/`, retained only non-case sandbox fixtures under `tests/fixtures/`, and updated tests, commands, case cards, registry pointers, and module docs.
- Recorded the relocation decision in [ADR-0013](../../architecture/adr/0013-colocate-self-authored-case-assets.md).
- Recorded the admission order: self-authored parameter families, Fusion 360 Gallery Reconstruction, DeepCAD, Brep2Seq synthetic, then ABC OOD robustness.
- Added M12-001: 18 self-authored parameter variants in six family-isolated development/held-out groups, plus offline hash/manifest/replay audit tooling.
- Added M12-002: Fusion 360 Gallery Reconstruction r1.0.1 documentation-only admission audit; no archive was downloaded, selected, manifested, or sent to a provider.
- Added ADR-0014 and expanded the case-library README/runbook with the long-term maintainability contract: immutable identifiers, explicit lifecycle, metadata evolution, split isolation, asset authority, offline audits, and external/runtime boundaries.
- Validated the new and governing JSON files with PowerShell `ConvertFrom-Json`; 21/21 SHA-256 checks, active-path audit, and `git diff --check` passed.
- Full offline validation: `uv run python -m pytest` — 68 passed in 105.88 s; `uv run python -m ruff check .` — passed.

## In progress

- No active workpack. No external candidate has been downloaded or admitted.

## Next

- Create a separate workpack only if archive acquisition is authorized: record its source SHA-256, preserve the official split, select a small deterministic single-body sketch/extrude subset, and prove local reference replay through existing gates.

## Decisions

- Self-authored assets are physically co-located per [ADR-0013](../../architecture/adr/0013-colocate-self-authored-case-assets.md); external raw assets remain locator-indexed and ignored per [ADR-0012](../../architecture/adr/0012-unified-case-library-governance.md).  [ADR-0014](../../architecture/adr/0014-case-library-maintainability-contract.md) defines their durable maintenance contract.
- A B-Rep-only source is not sequence-supervised; ABC remains OOD robustness material.

## Blockers

- No technical blocker. A future archive-acquisition workpack needs explicit user authorization before download; hosted use additionally requires the existing split-specific preflight and authorization.

## Key paths

| Kind | Path |
|---|---|
| Physical cases | `case-library/self-authored/` |
| Manifests | `case-library/manifests/self-authored/` |
| Catalog | `docs/corpus/library/catalog.json` |
| Procedure | `docs/runbooks/case-library-maintenance.md` |
| Decisions | `docs/architecture/adr/0012-unified-case-library-governance.md`; `docs/architecture/adr/0013-colocate-self-authored-case-assets.md` |
| Completed workpacks | `docs/workpacks/done/WP-M11-002-unified-case-library-governance.md`; `docs/workpacks/done/WP-M11-003-self-authored-case-library-migration.md`; `docs/workpacks/done/WP-M12-001-self-authored-parametric-families.md`; `docs/workpacks/done/WP-M12-002-fusion360-offline-admission-audit.md` |

## Resume prompt

```
Continue Brep2Code work: decide whether to authorize a separate Fusion 360 Gallery Reconstruction archive-acquisition workpack.
Read docs/handoff/active/2026-08-03-unified-case-library.md.
First action: do not download until the official archive identity, intended local-only scope, and license obligations are confirmed.
```
