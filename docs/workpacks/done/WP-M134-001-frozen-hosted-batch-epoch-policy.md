# WP-M134-001: Frozen Hosted Batch Epoch Policy

- Status: done
- Milestone: M134
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

## Goal

Freeze one comparable, existing-case hosted batch epoch and separate
batch-integrity blockers from per-condition terminal observations.

## Scope

- Define the fixed 18-condition development cohort from the completed M120 and
  M123--M126 charters.
- Freeze a no-mid-epoch-change policy: one provider/model, outbound contract,
  API instruction, executor, gates, request order, deadline and output bound
  are selected before authorization and cannot change during the epoch.
- Define serial scheduling as one request in flight for accounting/monitoring,
  not a causal gate between families.
- Define per-condition continuation and the small set of batch-integrity stop
  rules; record the follow-on M135 and M136 workpack sequence.
- Add an ADR and align current routing/framing/charter documentation.

## Attribution question and sampling intent

Distinguish a single condition's hosted terminal class from an invalid or
uninterpretable epoch. The fixed cohort is four no-card family splits of three
rows each plus prismatic's three paired card/no-card rows: 18 condition
observations, no substitutions, no repair, and no mid-epoch program change.

## Inputs

- `docs/workflow/m120-prismatic-development-campaign-charter.md`
- `docs/workflow/m123-repeated-feature-development-campaign-charter.md`
- `docs/workflow/m124-axisymmetric-revolve-development-campaign-charter.md`
- `docs/workflow/m125-dependent-face-selection-development-campaign-charter.md`
- `docs/workflow/m126-multi-inner-loop-pocket-development-campaign-charter.md`
- M127--M129 terminal/remediation records and hosted terminal triage runbook

## Docs to update

- `docs/architecture/adr/0067-frozen-hosted-batch-epochs.md`
- `docs/workflow/m134-frozen-hosted-batch-epoch-policy.md`
- current framing, batch plan, four-track roadmap, terminal triage, status,
  this workpack and active handoff

## Trace/schema changes

None. No CLI, report schema, trace schema, storage layout, policy file,
provider configuration, manifest, case, card, or runtime change is permitted.

## Decision-package impact

- `decision_id`: no Q01--Q04 decision package applies; this is hosted
  evaluation-governance policy.
- Q01/Q02 effect: no observation, action, family grammar or card changes.
- Q03/Q04 effect: freezes how terminal evidence is classified and when the
  epoch, rather than one condition, stops.
- Evidence role: comparative development-only hosted evaluation planning.
- Knowledge disposition: no reusable knowledge until M136 independently
  reviews terminal reports.

## Compatibility constraints

Offline and credential-free. No provider construction/request, preflight,
authorization, report/monitor preparation, old-budget reuse, input access,
case/split/card/prompt/API instruction mutation, repair, manifest/runtime or
training change. Existing family charters remain inputs, not authorization.

## Acceptance

    uv run python -m ruff check .
    uv run python tools\check_governance.py
    git diff --check

## Owner completion boundary

Publish the frozen policy, ADR, route alignment and explicit M135/M136
sequence; pass acceptance and obtain Liaol's independent G2 review.

## Permitted stop conditions

Independent review, frozen-input drift, a documentation-authority conflict, or
a reproducible validation blocker.

## Evidence reuse / guidance-card disposition

The four no-card families remain no-card conditions. The prismatic card hash
is a fixed treatment input only; no card promotion or runtime retrieval change
follows. M134 itself records no reusable hosted result.

## Status transition

Update `docs/workflow/status.md` first, then this workpack and the active
handoff. M135/M136 remain future user-selected workpacks.

## Out of scope

Any hosted request, provider/model selection, preflight execution, itemized
authorization, batch implementation, report creation, retry/repair, family
charter modification, held-out campaign, runtime promotion, native-shell or
robustness work.

## Owner evidence (2026-08-12)

- Added ADR-0067 and the frozen `existing-family-development-v1` policy:
  four three-row no-card family conditions plus prismatic's three paired
  card/no-card rows, for exactly 18 development observations.
- The policy freezes serial scheduling without serial gating. Script/API,
  geometry/semantic/editability, and one lifecycle terminal are recorded per
  condition and continue; only predeclared integrity faults or two consecutive
  no-response lifecycle failures stop issuance.
- Aligned the four-track, five-family, framing, batch-plan and triage pages to
  name M135 (G3 preflight/authorized execution) then M136 (G2 terminal
  evidence review) as the only successors. Other routes remain deferred.
- Acceptance passed: Ruff, governance audit and `git diff --check`. Liaol's
  independent G2 review is required before closure.

## Independent G2 review and closure (2026-08-12)

Liaol independently approved the fixed 18-condition cohort, serial-scheduling
versus serial-gating distinction, epoch-integrity stop rules, no-mid-epoch
change boundary, and M135/M136 sequence. M134 closes as offline governance
only: it grants no preflight, provider, authorization, execution, repair,
held-out, card-promotion or runtime authority.
