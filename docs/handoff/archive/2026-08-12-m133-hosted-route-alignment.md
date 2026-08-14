# Handoff: M133 Hosted Route Alignment

- **Date**: 2026-08-12
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M133-001-hosted-route-and-batch-navigation-alignment`

## Goal

Align hosted-route and batch navigation after M127--M129 so one future G3
shared-stability re-entry is the only near-term hosted candidate.

## Done

- User selected documentation alignment; M133 lifecycle records were created.
- Updated all current hosted/batch routing pages to use M127--M129 as the
  current shared-gate evidence and defer every non-gate route.
- Governance and diff checks passed; M133 is closed.

## In progress

- None; M133 is closed.

## Next

- Wait for the user to select a new bounded package. The only near-term hosted
  candidate is the fresh post-M129 shared-stability G3 re-entry, beginning
  offline with preflight.

## Decisions

- Family batches and all other offline/hosted routes remain deferred until a
  fresh post-M129 shared-stability gate is independently satisfied.

## Blockers

- No active blocker for M133. Family batches and all other routes remain
  deferred until a fresh shared-stability run passes independent review.

## Key paths

| Kind | Path |
|------|------|
| Workpack | `docs/workpacks/active/WP-M133-001-hosted-route-and-batch-navigation-alignment.md` |
| Current state | `docs/workflow/status.md` |
| Hosted registry | `docs/workflow/hosted-experiment-registry.md` |

## Resume prompt

    Continue Brep2Code work: complete M133 hosted-route and batch navigation alignment.
    Read docs/handoff/active/2026-08-12-m133-hosted-route-alignment.md.
    First action: replace M118-only routing with M127--M129 and defer all non-gate routes.
