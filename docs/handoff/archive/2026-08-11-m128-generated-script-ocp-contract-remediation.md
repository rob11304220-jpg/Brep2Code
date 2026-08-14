# Handoff: Generated-Script OCP Contract Remediation

- **Date**: 2026-08-11
- **Subproject**: `brep2code`
- **Status**: `active`
- **Related workpack**: `WP-M128-001-generated-script-ocp-contract-remediation`

## Goal

Complete one narrow offline G2 remediation for the generated-script OCP API
contract after M127's independently reviewed terminal script/API failure.

## Done

- M127 is closed after independent G3 terminal review. Its fresh report reached
  `completed` with `2/2` requests consumed; the final generated script was
  rejected for unavailable `OCP.STEPControl.STEPControl_STEPModelType`.
- The M127 registry row preserves lifecycle completion, script/API failure, and
  not-evaluated sandbox/provenance/downstream gates separately.
- M128 has been selected as the next bounded offline package; it does not grant
  provider or hosted authority and does not activate `TRG-005`.
- M128 owner work is complete: the existing contract was confirmed to classify
  M127's exact unavailable STEPControl symbol; one focused fail-closed
  regression fixture was added. The focused suite passed 60 tests, and Ruff,
  governance audit and diff check passed.

## Next

- Obtain Liaol's independent G2 review of the exact M127-symbol regression,
  fail-closed contract boundary, no-executor/no-downstream-inference evidence,
  and offline scope.
- If approved, close M128 and archive this handoff. If the review finds a
  missing prerequisite, record the exact blocker without widening into hosted
  work or activating `TRG-005`.

## Boundaries

- Do not read or display credentials, construct a provider, issue hosted work,
  retry M127, or reuse its report, monitor, budget or authorization.
- Do not change prompts, cards, manifest/split, reference scripts, executor
  policy or geometry gates. If any is required, stop and record the blocker.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M128-001-generated-script-ocp-contract-remediation.md` |
| Status | `docs/workflow/status.md` |
| M127 evidence | `docs/workpacks/done/WP-M127-001-shared-hosted-stability-reentry.md` |
| Terminal triage | `docs/runbooks/hosted-terminal-triage.md` |

## Resume prompt

```
Continue Brep2Code M128 generated-script OCP contract remediation.
Read docs/handoff/active/2026-08-11-m128-generated-script-ocp-contract-remediation.md.
First action: locate the static OCP symbol contract validation, reproduce the
M127 unsupported-symbol rejection locally, and keep all work offline.
```
