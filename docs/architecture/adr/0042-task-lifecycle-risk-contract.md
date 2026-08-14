# ADR-0042: Task Lifecycle Risk Contract

- **Status**: Accepted
- **Date**: 2026-08-07

## Context

The repository had workpack, handoff, and status conventions, but active-task
ownership, review expectations, and risk-dependent quality gates were not a
single enforceable contract.

## Decision

Define G0--G3 task risk tiers and require an owner for every active workpack,
an independent reviewer for G2/G3, and an active handoff linked to the active
workpack. Keep `status.md` as the state authority and make AGENTS a concise
router to this contract.

## Consequences

- Positive: task ownership and closure evidence are explicit without changing
  Harness behavior or provider authority.
- Negative: active-workpack creation has a few more required fields.
- Mitigation: templates, rules, and the governance audit provide the same
  vocabulary and diagnostics.
