# Handoff: current route and runtime guidance alignment

- **Date**: 2026-08-11
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M102-001-current-route-and-runtime-guidance-alignment`

## Goal

Align current documentation and rules with the completed M19 bridge and
M97-003/004 route state, preserving historical evidence and runtime boundaries.

## Done

- User selected the bounded G1 documentation-alignment package.
- Aligned current runtime guidance, M19/M97 routes and provider-rule wording.
- Runtime-guidance audit, governance audit and diff check passed.

## In progress

- None; M102-001 is complete.

## Next

1. Archive this completed handoff with M102-001.
2. Await user selection of the next bounded package.

## Decisions

- Existing opt-in guidance retrieval remains explicit and default-disabled;
  documentation must not describe it as absent.
- Hash-pinned card content is not edited for wording-only alignment; current
  bridge behavior is documented in the runtime-resource README/runbook.

## Blockers

- None.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M102-001-current-route-and-runtime-guidance-alignment.md` |
| Current state | `docs/workflow/status.md` |
| Runtime guidance | `runtime_resources/experience-cards/`, `docs/runbooks/runtime-guidance-cards.md` |
| Acceptance | `uv run python tools/check_governance.py`; `git diff --check` |

## Resume prompt

```
Continue Brep2Code work: select the next bounded package after M102-001.
Read docs/handoff/active/2026-08-11-current-route-runtime-guidance-alignment.md.
First action: read docs/workflow/status.md and select a package from the
four-track cadence; do not select M98 or issue a provider request by default.
```
