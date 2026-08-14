# Handoff: M140 Harness Tool-Mediated Agent Loop

- **Date**: 2026-08-12
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M140-001-harness-tool-mediated-agent-loop`

## Goal

Implement and locally validate the bounded Harness-owned tool-turn loop that
allows an LLM to request declared probes or one explicit card, generate a
script, then receive structured Harness feedback.

## Done

- M139 frozen hosted campaign launcher completed with independent G2 approval.
- TRG-025 is now active as M140; M139's campaign/checkpoint contract remains
  the preparation/identity boundary.

## In progress

- None. Owner implementation and independent G2 review are complete.

## Next

- M141 separately consumes TRG-026 for classified repair policy and routes.

## Decisions

- M140 is offline and credential-free.  It may use fake providers and local
  sandbox tests only; provider construction and hosted execution remain out of
  scope.
- M140 must not turn existing direct guidance injection into unrestricted card
  retrieval, nor add repair policy before TRG-026.
- `ToolTurnLoopRunner` ends after the first generated script's structured
  Harness feedback. It records only campaign identity, limits and payload
  hashes in its terminal turn trace; it does not invoke a later repair turn.
- Liaol approved M140's independent G2 review. The completed workpack does not
  authorize hosted tool turns, provider changes, card promotion or repair.

## Blockers

- None.

## Key paths

| Kind | Path |
|------|------|
| Workpack | `docs/workpacks/active/WP-M140-001-harness-tool-mediated-agent-loop.md` |
| Launcher | `brep2code/campaign.py` |
| Observation loop | `brep2code/agent/observed_build.py` |
| Tool bridge | `brep2code/agent/tools.py` |
| Guidance bridge | `brep2code/agent/guidance.py` |
| Provider contract | `brep2code/agent/provider.py` |
| M140 loop | `brep2code/agent/tool_turn.py` |
| M140 contract | `docs/architecture/v1/contracts/harness-tool-turn-loop.md` |

## Resume prompt

```
Continue Brep2Code work: implement M141's offline classified repair policy.
Read the active M141 handoff and workpack. First action: map M140 terminal
feedback fields to a fail-closed repair classification vocabulary before code.
```
