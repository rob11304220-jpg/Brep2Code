# Handoff: M149 Agent Entry and Document Routing

- **Date**: 2026-08-13
- **Subproject**: `brep2code`
- **Status**: `done` (archived after G1 closure)
- **Related workpack**: `WP-M149-001-agent-entry-and-document-routing`

## Goal

Add hypothesis-aware task routing to Agent, human, and workflow entry documents
without changing theory, case, runtime, provider, or hosted authority.

## Done

- M146 crosswalk and M148 theory map are complete.
- User selected TRG-032; M149 is active.

## In progress

- None. M149 is closed.

## Next

- Wait for explicit user selection of TRG-033, TRG-034, TRG-035, or the
  separate TRG-028 route. Do not activate a successor automatically.

## Decisions

- `hypothesis_id` is a routing/scoping field, not an implementation or runtime
  authorization. `status.md` and an active workpack remain execution authority.
- The three entry documents now share task-type routing without duplicating the
  M146 crosswalk or altering its source authorities.

## Blockers

- None.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M149-001-agent-entry-and-document-routing.md` |
| Theory map | `docs/architecture/v1/project-theory-map.md` |
| Crosswalk | `docs/corpus/knowledge/development-evidence-crosswalk-v1.md` |

## Resume prompt

M149 is complete. Read `docs/workflow/status.md` and wait for explicit user
selection of a bounded successor. Do not infer authority from routing fields.
