# Handoff: M178 Asymmetric Campaign CLI and Preflight

- **Date**: 2026-08-14
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M178-001-asymmetric-hosted-campaign-cli-and-preflight`

## Goal

Implement and offline-validate a fail-closed CLI/preflight contract for the
M176 30-case no-card main product and three-case hash-bound-card annex.

## Done

- M177 was deferred: its frozen inputs pass audit but the generic CLI cannot
  represent its dual-product contract.
- The user selected the bounded G2 M178 workpack.
- The accounting distinction is recorded: 102 interaction-completion slots,
  with at most 69 provider HTTP requests.

## In progress

- None. M178 is closed after Liaol's independent G2 approval.

## Next

- In a new session, read `status.md` and explicitly select a fresh G3 M177
  preflight workpack before invoking the M178 local preflight command.

## Decisions

- M178 does not revive M177 authorization. Any later execution needs a fresh
  G3 workpack, preflight and itemized user authorization.
- Report 102 completion slots separately from actual provider-request ceiling
  69; this avoids overstating billed/egressed requests.

## Blockers

- No active workpack. A new G3 M177 preflight selection and new itemized
  egress authorization are required before any hosted execution.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M178-001-asymmetric-hosted-campaign-cli-and-preflight.md` |
| Freeze | `docs/corpus/knowledge/m176-asymmetric-campaign-freeze-v1.json` |
| Qualification | `docs/corpus/knowledge/m175-asymmetric-cohort-qualification-v1.json` |
| CLI | `brep2code/cli/__init__.py` |

## Resume prompt

```
Continue Brep2Code M178: implement and offline-validate the fixed asymmetric
hosted campaign CLI/preflight contract. Read this handoff and the active
workpack. Do not construct a provider or issue a hosted request.
```
