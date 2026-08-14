# Handoff: M83 reference-case taxonomy and candidate-pack contract

- **Date**: 2026-08-10
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M83-001-reference-case-taxonomy-and-pack-contract`

## Goal

Freeze a development-only P0/P1 taxonomy and machine-auditable candidate
reference-pack contract for seven selected self-authored cases. The artifact
describes bounded OCP construction patterns without making a source STEP,
full reference script, or development governance material runtime-visible.

## Done

- Restored the repository state: M82 is done and no active handoff remained.
- Activated the user-selected M83 workpack with Codex as owner and Liaol as
  independent G2 reviewer.
- Fixed the intended scope to the three P0 and four P1 cases already named in
  the roadmap; M19-002 remains evidence-gated by ADR-0016 and M84.
- Added the fixed candidate-pack contract, local audit, and regression tests.
  Each pack is declarative only and carries a content hash, source case record
  and input hash, OCP module summary, bounded outline, output requirement, and
  counterexample.
- Owner checks passed: reference-pack audit, 2 focused tests, full Ruff,
  case-library audit, runtime-guidance audit, governance audit, and diff check.

## In progress

- None.

## Next

- M83 is closed following Liaol's independent approval.
- M84 remains backlog until the user separately selects it; it must establish
  or reject three independent direct development cases for one mechanism.

## Decisions

- M83 is offline development curation only. It does not modify runtime,
  prompt, provider, executable manifests, or hosted budget.
- Candidate packs remain experimental and are not experience cards or
  retrieval material. ADR-0016 requires M84 to establish three independent
  direct development cases before M19-002 can start.

## Blockers

- None for M83. M19-002 remains blocked by M84's independent direct-evidence
  threshold.

## Key paths

| Kind | Path |
|---|---|
| Branch | `main` |
| Workpack | `docs/workpacks/active/WP-M83-001-reference-case-taxonomy-and-pack-contract.md` |
| Selection | `case-library/manifests/self-authored/p0.json`, `case-library/manifests/self-authored/p1.json` |
| Boundary | `docs/architecture/adr/0016-evidence-bounded-runtime-guidance-cards.md` |
| Commands | `uv run python tools/audit_case_library.py`; `uv run python tools/check_governance.py` |

## Resume prompt

```
Continue Brep2Code M83 reference-case taxonomy and candidate-pack contract.
Read docs/handoff/active/2026-08-10-m83-reference-case-taxonomy.md.
M83 is complete. Before beginning any successor, read docs/workflow/status.md;
M84 must be separately selected and may not treat M83 metadata as independent
direct evidence. Do not expose STEP or full reference scripts, alter
runtime/manifest/provider/prompt, or make any hosted request.
```
