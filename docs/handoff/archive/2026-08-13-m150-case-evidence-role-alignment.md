# Handoff: M150 Case-Evidence Role Alignment

- **Date**: 2026-08-13
- **Subproject**: `brep2code`
- **Status**: `done` (archived after independent approval)
- **Related workpack**: `WP-M150-001-case-evidence-role-alignment`

## Goal

Create a source-linked companion mapping from selected existing case and
documentary evidence to M146 hypothesis IDs and evidence roles, without
changing case/source authority or accessing fixtures/scripts.

## Done

- M146 crosswalk, M148 theory map, and M149 entry routing are complete.
- User selected TRG-033; M150 is active with Liaol as independent reviewer.
- Completed the owner-side companion mapping, navigation, deterministic audit,
  and maintenance guidance. The mapping has 14 relationships and records only
  reviewed source links; held-out relationships are documentary-only and omit
  held-out case IDs, asset paths, metadata, parameters, hashes, and sequences.

## In progress

- None. M150 is closed and archived after Liaol's independent G2 approval.

## Next

- Wait for explicit user selection of TRG-034, TRG-035, or the independent
  TRG-028 route. Do not activate a successor automatically.

## Decisions

- Held-out evidence is documentary-only. The relationship layer stores no
held-out fixture path, raw metadata, parameters, hashes, or sequences.
- Family-level reviewed links are preferable to unsupported per-case inference.
- The rollback hypothesis is intentionally unmapped because its existing
  evidence is a fixed-script execution boundary, not case-evidence material.
- Liaol approved M150's independent G2 review. The pytest outer-deadline
  timeout remains recorded as non-terminal historical validation evidence.

## Blockers

- None.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M150-001-case-evidence-role-alignment.md` |
| Crosswalk | `docs/corpus/knowledge/development-evidence-crosswalk-v1.json` |
| Mapping | `docs/corpus/knowledge/case-evidence-relationships-v1.json` |
| Navigation | `docs/corpus/knowledge/case-evidence-relationships-v1.md` |
| Audit | `tools/audit_case_evidence_relationships.py` |
| Admission record | `docs/corpus/knowledge/admissions/selector-ambiguity-v1.json` |

## Resume prompt

M150 is complete. Read `docs/workflow/status.md` and wait for an explicitly
selected bounded successor. Do not reactivate M150 or infer case, runtime,
provider, or hosted authority from its companion mapping. The recorded full
pytest timeout remains non-terminal historical validation evidence.
