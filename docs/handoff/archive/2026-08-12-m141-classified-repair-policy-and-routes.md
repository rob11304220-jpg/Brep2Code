# Handoff: M141 Classified Repair Policy and Routes

- **Date**: 2026-08-12
- **Subproject**: `brep2code`
- **Status**: `complete`
- **Related workpack**: `WP-M141-001-classified-repair-policy-and-routes`

## Goal

Implement and locally validate a fail-closed repair router that classifies
sanitized M140 terminal feedback into one bounded edit scope, request limit and
plateau/stop rule.

## Done

- M140's offline Harness tool-turn loop passed independent G2 review and is
  archived. It is the signal/tool contract predecessor for this work.
- User selected TRG-026; it is now active as M141 G2 with Liaol as independent
  reviewer.
- Implemented `brep2code.agent.repair_policy` and its M141 contract. It admits
  only bounded fake-provider source edits for deterministic static API/output
  and local execution failures; all selector, sequence/IR, geometry,
  editability, sandbox/provenance, timeout and ambiguous paths stop closed.

## In progress

- None. Liaol completed the independent G2 review and approved M141 closure.
- Focused policy tests (5), adjacent repair/tool-turn tests (19), fast suite
  (66), fresh full suite (265), Ruff, governance and diff checks passed. The
  first full-suite outer window timed out at 484.1s without a pytest result;
  its independent rerun completed in 667.99s.

## Next

- No successor workpack is active. The user may separately select `WP-TRG-027`.

## Decisions

- M141 is offline and credential-free. It may use local fake providers but may
  not construct a provider or issue hosted requests.
- No frozen M135/M139 campaign is repaired in place. Any hosted repair needs a
  later selected G3 package, fresh preflight, authorization and report/monitor.
- Repair routing must build on M140's Harness feedback; it must not bypass the
  restricted Harness or gain raw input/workspace access.

## Blockers

- None.

## Key paths

| Kind | Path |
|------|------|
| Workpack | `docs/workpacks/active/WP-M141-001-classified-repair-policy-and-routes.md` |
| M140 loop | `brep2code/agent/tool_turn.py` |
| Existing repair loop | `brep2code/agent/repair.py` |
| Harness signal | `brep2code/agent/harness.py` |
| M140 contract | `docs/architecture/v1/contracts/harness-tool-turn-loop.md` |

## Resume prompt

```
Continue Brep2Code work: implement M141's offline classified repair policy.
Read docs/handoff/active/2026-08-12-m141-classified-repair-policy-and-routes.md.
First action: map M140 terminal feedback and existing repair outcomes into a
fail-closed classification vocabulary before changing code.
```
