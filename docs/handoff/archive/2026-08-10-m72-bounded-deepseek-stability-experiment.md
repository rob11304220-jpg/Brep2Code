# Handoff: M72 bounded DeepSeek stability experiment

- **Date**: 2026-08-10
- **Subproject**: `brep2code`
- **Status**: `done` (closed after independent review)
- **Related workpack**: `WP-M72-001-bounded-deepseek-stability-experiment`

## Goal

Perform a fresh, bounded G3 provider-lifecycle stability experiment only after
a successful local preflight and itemized user authorization.

## Done

- M70 and M71 are closed, and Liaol selected M72.
- M72 is active with Codex as owner and Liaol as independent reviewer.

## In progress

- None.

## Next

- Retain the no-retry disposition. Any future lifecycle study requires a new
  workpack, new preflight, new reports and new itemized authorization.

## Decisions

- M71's supported non-streaming JSON-object transport is the only eligible
  mode; streaming and `max_output_chars` remain unsupported.
- No old report, request budget, or authorization may be reused.
- The first authorized request timed out at the fixed 300-second deadline;
  M72 stops rather than retrying or advancing to the other cases.

## Blockers

- None. Liaol approved M72 closure on 2026-08-10.

## Key paths

| Kind | Path |
|------|------|
| Workpack | `docs/workpacks/active/WP-M72-001-bounded-deepseek-stability-experiment.md` |
| Provider runbook | `docs/runbooks/llm-provider-config.md` |
| Development manifest | `case-library/manifests/self-authored/parametric-development.json` |
| Preflight | `docs/workflow/m72-hosted-stability-preflight.md` |
| Terminal report | `data/corpus-runs/m72-param-additive-boss-low.json` |

## Resume prompt

```
M72 is closed as a no-retry provider-lifecycle timeout disposition.
Read docs/workflow/m72-hosted-stability-preflight.md for the bounded evidence.
First action: do not resume or retry M72; select a new bounded workpack only if a new question is authorized.
```
