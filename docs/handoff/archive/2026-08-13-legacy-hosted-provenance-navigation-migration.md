# Handoff: Legacy hosted provenance navigation migration

- **Date**: 2026-08-13
- **Subproject**: `brep2code`
- **Status**: `active`
- **Related workpack**: `WP-M169-001-legacy-hosted-provenance-navigation-migration`

## Goal

Migrate legacy hosted route links and verify the remaining provenance exception
set.

## Done

- M168 migrated the case/sequence historical roadmap cluster, reducing direct
  completed/archive links from 57 to 37.

## In progress

- Migrate post-M9, M9 and M69 legacy hosted links.

## Next

- Map their historical conclusions to stable evidence and route authorities.
- Audit the final retained direct-link set against the citation contract.

## Decisions

- A terminal-report or decision-evidence link is retained only when it is the
  original immutable provenance needed by its stable record.

## Blockers

- None.

## Key paths

| Kind | Path |
|------|------|
| Files | `docs/architecture/v1/post-m9-evidence-gated-roadmap.md` |
| Files | `docs/workflow/hosted-experiment-registry.md` |
| Commands | `uv run python tools/check_governance.py`; `git diff --check` |

## Resume prompt

```
Continue Brep2Code work: complete M169 legacy hosted provenance navigation migration.
Read docs/handoff/active/2026-08-13-legacy-hosted-provenance-navigation-migration.md.
First action: migrate the 13 legacy hosted route links and audit retained exceptions.
```
