# WP-M122-001: Family Hosted Preparation Route Alignment

- Status: done
- Milestone: M122
- Owner: Codex
- Reviewer: not required (G1)
- Risk tier: G1

## Goal

Rewrite the default next-work wording so the project prioritizes preparing the
family/mechanism campaigns it actually intends to run with hosted evaluation,
rather than continuing blocked hosted-stability triggers as the default queue.

## Scope

- Update status and route documents to state the new preparation-first rule.
- Add deferred family-specific charter-draft triggers for the four no-card
  five-family candidates.
- Record limited adaptive slack rules for switching among already prepared
  families without reopening frozen family scope.

## Compatibility constraints

Documentation and route governance only. No provider construction, preflight,
authorization, request, trigger activation, case/split mutation, or runtime
change.

## Acceptance

```powershell
python tools\check_governance.py
git diff --check
```

## Status transition

Update `status.md` first, then route documents, deferred trigger index, and
handoff. Close after governance audit and diff checks pass.

## Owner acceptance

- Updated the status page and the hosted planning/roadmap pages so the default
  next packages are the four family-specific charter-draft triggers, not the
  still-unmet hosted-stability trigger chain.
- Added `WP-TRG-020` through `WP-TRG-023` as the current no-card family
  preparation queue for repeated feature pattern, axisymmetric revolve,
  dependent face selection, and multi-inner-loop pocket.
- Recorded adaptive slack as queue-order flexibility only: the project may
  switch among already prepared families later, but must not mutate a frozen
  family charter inside that switch.

## Closure rationale

The route now reflects the real execution strategy: prepare the cases and
mechanism families intended for later hosted runs, and treat hosted-stability
re-entry as a separate future decision instead of the default next work.

## Out of scope

Drafting any one family charter, re-entering hosted stability, or authorizing
any hosted campaign.
