# Offline Validation Planning

Use this runbook after a local code, documentation, corpus, or governance
change. It plans validation without selecting a provider or sending data
externally.

## Start with the current baseline

Read [`m53-test-feedback-baseline.md`](../workflow/m53-test-feedback-baseline.md)
before estimating a command window. Its measurements are observations, not CI
limits: re-measure when process-boundary tests, fixtures, or test layout
change. A command that exceeds the baseline is not a failure by itself.

The current local planning windows are 60 seconds for standalone `fast` or
`standard`, and eight minutes for standalone `sandbox` or full-suite commands.
They are intentionally independent: do not combine them into one outer limit.

Pytest markers divide the suite as follows:

| Marker | Purpose | Use |
|---|---|---|
| `fast` | Deterministic utility and metadata checks | First developer-feedback command. |
| `standard` | Credential-free checks without Harness/corpus process boundaries | Use when the changed area is covered and a quick broader check adds evidence. |
| `sandbox` | Harness, executor, or corpus integration that spawns local CAD/Python processes | Run separately only when it gives earlier, changed-boundary evidence. |
| no marker selection | Full suite, including sandbox tests | Run once for the final required full-suite gate. |

## Plan commands before launching them

1. Run `uv run python -m pytest -m fast -q` and changed-area tests first.
2. For a changed process/executor/Harness boundary, run the relevant sandbox
   selection as a separately bounded command when early integration feedback is
   useful.
3. When the workpack requires a full suite, run `uv run python -m pytest` once
   as its own command. Do not place a standalone full sandbox selection
   immediately before it solely for final coverage: the full suite includes it.
4. Run Ruff, governance, and `git diff --check` separately. Record each command
   and terminal result in the workpack.

Never concatenate long selections into one outer command deadline. If a command
exceeds its expected window, preserve its final output when possible; otherwise
record it as an environment/command-window limitation, rerun that one command
with an appropriate independent limit, and do not claim pass or fail without a
terminal result.

## Minimum command sets

| Change type | During implementation | Final gate |
|---|---|---|
| Documentation/governance | `fast` | Workpack-specific focused check, governance, diff check |
| Shared code outside process boundary | `fast` + changed-area tests | One full suite, Ruff, governance, diff check |
| Harness/executor/corpus boundary | `fast` + changed-area tests + useful sandbox selection | One full suite, Ruff, governance, diff check |

Hosted commands are outside this runbook. They retain their separate preflight,
authorization, durable-monitoring, and provider-deadline requirements.
