# Handoff: M89 Provider Lifecycle Diagnosis

- **Date**: 2026-08-10
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M89-002-provider-lifecycle-observability-diagnosis`

## Goal

Add offline-only, privacy-bounded response-lifecycle diagnostics after M89's
second request timed out, without retrying or changing CAD behavior.

## Done

- M89-001 is terminal `interrupted`, uses 2/2 requests, and was independently
  closed as a no-retry timeout disposition.
- User selected M89-002 to prepare diagnosis before considering any new retry.

## In progress

- None. Owner implementation and offline acceptance completed; Liaol approved
  M89-002's independent G2 review. No provider request was issued.

## Next

- Wait for the user to choose a new bounded workpack. A retry requires a new
  G3 proposal, report path, budget, and explicit authorization.

## Decisions

- Do not expose or retain reasoning content; use lifecycle timing and bounded
  structured output limits instead.
- Keep M90--M98 blocked behind this diagnosis and a later separate G3 choice.

## Blockers

- None. M89-002 is closed; M89-001's budget remains exhausted.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M89-002-provider-lifecycle-observability-diagnosis.md` |
| Prior report | `data/corpus-runs/m89-three-hole-plate-reference-assisted.json` |
| Provider | `brep2code/agent/provider.py` |
| Worker | `brep2code/agent/repair.py` |
| Contract | `docs/architecture/v1/contracts/llm-provider-trace.md` |
| ADR | `docs/architecture/adr/0053-provider-first-byte-and-token-cap-diagnostics.md` |

## Resume prompt

```
Continue Brep2Code after M89-002 provider lifecycle diagnosis.
Read docs/handoff/active/2026-08-10-m89-provider-lifecycle-diagnosis.md.
First action: read docs/workflow/status.md and wait for the user to choose a
new bounded workpack; do not retry M89-001.
```
