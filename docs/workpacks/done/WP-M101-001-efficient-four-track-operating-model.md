# WP-M101-001: Efficient Four-Track Operating Model

- Status: done
- Milestone: M101
- Owner: Codex
- Reviewer: not required (G1)
- Risk tier: G1

## Goal

Turn the existing four evidence-gated tracks into an efficient operating model:
shared mechanism dossiers and readiness checks, batched offline family release,
independent card qualification, and low-frequency hosted campaigns.

## Scope

- Define the five development-side work products and their authorities.
- Update the four-track roadmap with the operating cadence and near-term,
  user-selectable package sequence.
- Add a concise ADR and a maintenance procedure for selecting/closing work
  without treating a roadmap as provider or runtime authorization.

## Attribution question and sampling intent

Distinguish workflow fragmentation from missing CAD/provider evidence. Stop
after documenting a bounded routing model over existing records; do not create
or promote a case, card, pack, manifest, runtime integration or hosted result.

## Inputs

- ADR-0056, ADR-0057, ADR-0059 and the four-track roadmap
- case portfolio, hosted experiment registry and current status

## Code paths

None. Documentation and governance only.

## Docs to update

- `docs/architecture/v1/four-track-program-roadmap.md`
- `docs/architecture/adr/0060-efficient-four-track-operating-model.md`
- `docs/runbooks/evidence-portfolio-maintenance.md`
- `docs/workflow/status.md`, this workpack and active handoff

## Trace/schema changes

None. No report, trace, registry, manifest, card or runtime schema changes.

## Decision-package impact

- `decision_id`: none; project operating-model documentation only.
- Q01/Q02 effect: no observable, card-selection, prompt or sequence change.
- Q03/Q04 effect: no gate, executor, diagnostic, repair or stopping change.
- Evidence role: routing/navigation only.
- Knowledge disposition: no reusable knowledge.

## Compatibility constraints

Default operation stays network-free and credential-free. Four tracks retain
their existing dependencies; a roadmap, cadence or dossier cannot select a
workpack, inspect held-out input, alter cards/prompts, grant hosted authority
or reuse a report budget.

## Acceptance

```powershell
uv run python tools\check_governance.py
git diff --check
```

## Evidence reuse / guidance-card disposition

No card, pack or runtime projection changes.

## Status transition

After acceptance, update `status.md` first, move this workpack to `done/`,
archive the active handoff, and leave future packages unselected.

## Closure rationale

- Added ADR-0060, which preserves the four tracks while defining the shared
  mechanism dossier, family release, card qualification, hosted campaign and
  readiness products.
- Updated the four-track roadmap with capacity rules, the M97-003/004 factual
  state, and a five-step candidate cadence that remains subject to explicit
  user selection.
- Extended portfolio maintenance so future workpacks apply the model without
  creating a parallel authority.
- Acceptance on 2026-08-11: `uv run python tools/check_governance.py` and
  `git diff --check` passed. No provider, case, manifest, card, policy,
  report, runtime or Harness change occurred.

## Out of scope

Any provider request, preflight, new case/family/card/pack, manifest change,
retrieval implementation, M98 selection, held-out inspection, or code change.
