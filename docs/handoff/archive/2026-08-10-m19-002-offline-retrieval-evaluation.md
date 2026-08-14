# Handoff: M19-002 development-only guidance retrieval evaluation

- **Date**: 2026-08-10
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M19-002-development-guidance-retrieval-evaluation`

## Goal

Compare a frozen no-card baseline with deterministic top-k=1 selection of the
M84-qualified `vertical-cylinder-construction` card, using only the three fixed
development cases and offline fixtures.

## Done

- M84 independently qualified the direct-evidence threshold and the user
  selected M19-002.
- Frozen scope: `cylinder`, `block_with_hole`, and `three_hole_plate`; no
  held-out input, provider, prompt, runtime mount, or production retrieval.
- Added a preregistered top-k=1 evaluator and audit. The treatment selects the
  one experimental card only for the three declared roles; the baseline is
  card-free. Both use unchanged fixed local controls.
- Result: treatment 3/3 expected selections (precision 1.0), unsupported-action
  rate 0, and both policies 3/3 readable output plus existing gate pass.
- Validation passed: 3 focused tests, fast suite 64 passed/130 deselected,
  full suite 194 passed in 183.88s, Ruff, governance audit, and diff check.

## In progress

- None.

## Next

- M19-002 is closed after Liaol's independent approval. The user separately
  selected M19-003; see its active handoff for the runtime integration scope.

## Decisions

- The card is an explicit evaluator input only; it is not mounted, injected,
  or retrieved by the Harness/runtime.
- A passing offline comparison can at most retain the result as experimental
  or support separately selecting M19-003; it makes no hosted/model claim.

## Blockers

- None for the offline evaluation. Any treatment regression is a stop signal,
  not a reason to alter cases, cards, or the evaluator policy.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M19-002-development-guidance-retrieval-evaluation.md` |
| Card | `runtime_resources/experience-cards/cards/vertical-cylinder-construction.json` |
| Qualification | `docs/corpus/reference-packs/m84-cylinder-construction-qualification-v1.json` |

## Resume prompt

```
Continue Brep2Code M19-002 offline retrieval evaluation.
Read docs/handoff/active/2026-08-10-m19-002-offline-retrieval-evaluation.md.
M19-002 is complete. Read docs/workflow/status.md before successor work. Its
offline result does not authorize hosted use; M19-003 remains limited to the
separately selected read-only runtime integration.
```
