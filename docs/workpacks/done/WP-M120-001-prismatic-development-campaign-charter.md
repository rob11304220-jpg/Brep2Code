# WP-M120-001: Prismatic Development Campaign Charter

- Status: done
- Milestone: M120
- Owner: Codex
- Reviewer: not required (G1)
- Risk tier: G1

## Goal

Freeze one planning-only prismatic development campaign charter under the
completed M115 successor policy, without reopening hosted scope, selecting a
provider run, or creating preflight/authorization authority.

## Scope

- Draft one bounded single-family development campaign charter that names the
  finite development rows, limited reference scope, planned request accounting,
  interpretation table, and old-route demotion rules.
- Keep the charter explicitly below hosted-stability re-entry, preflight, and
  authorization; do not create a runnable G3 package.
- Update only current status and planning navigation needed to reflect that
  the charter now exists.

## Compatibility constraints

Offline and credential-free. No held-out input access, provider construction,
preflight, authorization, request, runtime change, manifest change, policy
mutation, report reuse, or trigger activation.

## Acceptance

```powershell
python tools\check_governance.py
git diff --check
```

## Status transition

Update `status.md` first, then record the charter, workpack, and handoff.
Close after governance audit and diff checks pass.

## Owner acceptance

- Added the planning-only charter
  [`m120-prismatic-development-campaign-charter.md`](../../workflow/m120-prismatic-development-campaign-charter.md),
  which freezes the bounded question, three development rows, limited
  measured-fact egress, M115 policy authority, planned report/monitor paths,
  interpretation table, and old-route noise check.
- Recorded that the shared hosted-stability gate remains unmet, so M120 stops
  before preflight and authorization. The charter is therefore a frozen input
  for a later fresh G3 readiness package, not a runnable campaign.
- Updated `status.md` and the current hosted candidate plan so the repository's
  next-step wording is consistent: prismatic charter drafting is complete, and
  `WP-TRG-005` remains the next shared gate if hosted progress is selected.

## Closure rationale

The next prismatic step is now single-valued: do not reopen policy design or
old held-out triggers; instead, satisfy shared hosted-stability prerequisites
and carry this charter into a fresh family-scoped G3 readiness package.

## Out of scope

Shared hosted-stability re-entry, provider/model selection authority,
campaign preflight, user authorization, development execution, held-out
campaign design, or runtime guidance promotion.
