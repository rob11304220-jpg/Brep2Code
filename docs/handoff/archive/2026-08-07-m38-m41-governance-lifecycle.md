# Handoff: M38--M41 governance lifecycle

- **Date**: 2026-08-07
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `none`

## Goal

Implement the approved M38--M41 plan: lifecycle/risk contract, enforceable
audit, controlled multi-agent review, and read-only governance health snapshot.

## Done

- Added `docs/workflow/task-lifecycle.md` and concise AGENTS routing.
- Extended governance audit and its focused tests for new active-task fields.
- Defined owner/contributor/reviewer protocol and recorded ADRs 0042--0044.
- Added `tools/governance_health.py` plus its runbook.

## In progress

- None.

## Next

- Wait for an evidence-ledger re-entry condition or a user-selected bounded decision package.

## Decisions

- Active workpacks require owner and risk tier; G2/G3 require independent review: [ADR-0042](../../architecture/adr/0042-task-lifecycle-risk-contract.md).
- Collaboration stays single-owner and bounded: [ADR-0043](../../architecture/adr/0043-controlled-multi-agent-review.md).
- Health reporting is offline and read-only: [ADR-0044](../../architecture/adr/0044-read-only-governance-health.md).

## Blockers

- None.

## Key paths

| Kind | Path |
|---|---|
| Workflow | `docs/workflow/task-lifecycle.md` |
| Audit | `tools/check_governance.py` |
| Health | `tools/governance_health.py` |
| Commands | `uv run python tools/check_governance.py`; `uv run python tools/governance_health.py --format markdown` |

## Resume prompt

```
Continue Brep2Code work from the post-M41 idle state.
Read docs/workflow/status.md and docs/workflow/evidence-ledger.json.
First action: select a user-authorized bounded decision package only if a re-entry condition is met.
```
