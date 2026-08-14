# Handoff: M86 Multi-role Reference-assisted Offline Admission

- **Date**: 2026-08-10
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M86-001-multi-role-reference-assisted-offline-admission`

## Goal

Offline-admit the three M84-qualified roles of the frozen vertical-cylinder
guidance card through the M85 two-stage path.

## Done

- User selected this bounded, offline-only workpack after M85 closure.
- Scope is frozen to `cylinder`, `block_with_hole`, and `three_hole_plate`.
- Owner implementation and acceptance are complete: the selected role is
  carried into the first-stage request and bounded trace/signal metadata, and
  all three fake-provider cases pass unchanged execution and geometry gates.

## In progress

- Liaol independently approved M86 on 2026-08-10.

## Next

- M86 is closed. Any hosted expansion needs a new user-selected workpack,
  preflight, and explicit authorization.

## Decisions

- Existing evidence qualifies one card across three declared roles; it does
  not qualify unrelated cards or cases.
- Provider selection is constrained to a preregistered role and resolved by
  the Harness, rather than allowing arbitrary card or filesystem search.

## Blockers

- None. Hosted use remains out of scope for this closed workpack.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M86-001-multi-role-reference-assisted-offline-admission.md` |
| Guidance bridge | `brep2code/agent/guidance.py` |
| Runner | `brep2code/agent/observed_build.py` |

## Resume prompt

```
Continue M86 offline admission. Read the active handoff and workpack, then
complete role-to-card selection tests and G2 validation. Do not make hosted
requests.
```
