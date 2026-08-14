# WP-M133-001: Hosted Route and Batch Navigation Alignment

- Status: done
- Milestone: M133
- Owner: Codex
- Reviewer: not required (G1)
- Risk tier: G1

## Goal

Align current routing documentation after M127--M129 and M132 so later agents
see one near-term hosted candidate and treat all other routes as deferred.

## Scope

- Replace stale M118-only hosted-stability wording with the latest M127
  script/API terminal result and the completed M128/M129 offline remediations.
- State that a fresh post-M129 shared-stability G3 re-entry is the only
  near-term hosted candidate, and that it starts with offline preflight.
- Mark family batch, native-shell evidence, robustness micro-family,
  reference-assisted construction, and parameter-variation work as deferred
  until separately user-selected after the shared gate is independently met.
- Preserve all existing workpack, report, budget, authorization, case, split,
  card, and policy boundaries.

## Compatibility constraints

Documentation and navigation only; offline and credential-free. No provider
construction/request, preflight execution, policy mutation, report reuse,
case/manifest/runtime/Harness change, or hosted authorization.

## Acceptance

    uv run python tools\check_governance.py
    git diff --check

## Owner completion boundary

Update every current hosted routing/index page named in the workpack, record
the single candidate/deferred rule, synchronize status and handoff, and pass
the acceptance commands.

## Permitted stop conditions

Reproducible documentation-authority conflict or an out-of-scope dependency.

## Status transition

Update `docs/workflow/status.md` first, then this workpack and the active
handoff. Archive the handoff after closure because no active workpack remains.

## Out of scope

Selecting or running the fresh G3 re-entry; any batch campaign; native-shell
implementation; robustness-family design; family charter change; provider,
runtime, manifest, case, or policy changes.

## Owner acceptance and closure (2026-08-12)

- Updated current-state, four-track, five-family, evaluation-framing, batch
  candidate, deferred-trigger, and milestone-history navigation to name M127
  as the latest hosted terminal record and M128/M129 as offline-only
  remediations.
- The sole near-term hosted candidate is a separately user-selected fresh
  post-M129 shared-stability G3 re-entry, beginning with offline preflight.
  Every family batch, native-shell evidence, robustness micro-family,
  reference-assisted extension, and parameter-variation package is explicitly
  deferred.
- `uv run python tools\check_governance.py` and `git diff --check` passed.
  M133 closes because all named navigation authorities now share the same
  priority rule; no runtime, provider, policy, case, or hosted change occurred.
