# WP-M135-005: Frozen Epoch Itemized Authorization Preparation

- Status: blocked
- Milestone: M135
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G3

## Goal

Prepare a complete, evidence-linked, itemized authorization request for the
unchanged M134 18-condition epoch using new report/monitor identities, without
constructing a provider, accessing credentials, sending data or issuing any
hosted request.

## Scope

- Reconcile the executable M135 boundary with every authorization item:
  destination and outbound content class, provider/model, fixed cohort/order,
  serial 18-request budget, zero repair/retry, `wsl-bwrap`, 120-second
  deadline, no selected output cap and fresh report/monitor identities.
- Verify that the actual executable command has a complete fail-closed mapping
  to those values; a generic or local-only command cannot substitute for an
  executable hosted boundary.
- Inspect only new planned M135-005 paths for existing checkpoints; do not
  create a report or monitor state in this workpack.
- Publish the itemized authorization text only if every reconciliation check
  passes and Liaol completes independent G3 review. It must request approval,
  not initiate execution.

## Attribution question and sampling intent

Can a user make an informed, bounded authorization decision for the exact
frozen cohort? This is authorization readiness only, not provider evaluation.
Stop on any unmatched executable or egress boundary, identity drift,
independent review or explicit authorization.

## Inputs

- `docs/workflow/m134-frozen-hosted-batch-epoch-policy.md`
- `docs/workflow/m135-003-frozen-epoch-cli-contract.md`
- `docs/workflow/m135-004-complete-hosted-preflight.md`
- `docs/runbooks/llm-provider-config.md`
- `docs/architecture/adr/0067-frozen-hosted-batch-epochs.md`
- `docs/architecture/adr/0068-frozen-epoch-checkpoint-and-transcript-contract.md`

## Code paths

- Read-only inspection of `brep2code/agent/m135_epoch.py` and
  `brep2code/cli/__init__.py`; code changes are out of scope. A missing
  executable hosted boundary is a blocker requiring a separately selected
  implementation workpack.

## Docs to update

- `docs/workflow/status.md`
- this workpack and one active handoff
- `docs/workflow/m135-005-itemized-authorization-preparation.md`

## Trace/schema changes

None. No report, monitor state, provider trace, outbound transcript or runtime
artifact is created by this workpack.

## Decision-package impact

- `decision_id`: no Q01--Q04 package; hosted-evaluation authorization readiness.
- Q01/Q02 effect: no observable, case, card, prompt, split or sequence change.
- Q03/Q04 effect: verifies that the declared authorization boundary maps to an
  executable contract before any request.
- Evidence role: governance reconciliation.
- Knowledge disposition: no reusable knowledge.

## Compatibility constraints

Default operation remains offline and credential-free. Do not alter the frozen
cohort, hashes, order, model/provider, executor, deadline, output cap, budget
or retry boundary; do not read credentials, construct a provider, send data,
issue a request, alter manifests or reuse any M135 report, monitor, budget or
authorization.

## Acceptance

```powershell
uv run python -m pytest tests\test_m135_epoch.py -q
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

## Owner completion boundary

Publish a M135-005 reconciliation record that either contains a complete
itemized authorization request or a reproducible blocker; pass acceptance and
obtain Liaol's independent G3 review. Only an explicit itemized user response
to a complete request can authorize a later execution workpack.

## Permitted stop conditions

Independent review; explicit hosted authorization; frozen-input drift;
out-of-scope dependency; or reproducible local boundary blocker.

## Evidence reuse / guidance-card disposition

No reusable knowledge. The existing prismatic card remains a frozen treatment
input and all other conditions remain no-card.

## Status transition

Update `docs/workflow/status.md` first, then this workpack and the active
handoff. If blocked, archive this workpack with its reconciliation record.

## Out of scope

Hosted execution or authorization issuance; provider construction; credential
access; report/monitor creation; condition addition/removal/reorder;
prompt/card/model/provider changes; repair/retry; case/manifest changes;
held-out evaluation; runtime changes; or M137 terminal review.

## Blocked closure rationale

Repository inspection proves the required executable hosted M135 surface is
absent. `m135-epoch-preflight` is explicitly local-only and lacks provider
construction, an execute phase, outbound-content contract and 18-condition
hosted lifecycle. Consequently no itemized authorization request can honestly
be tied to executable enforcement. The terminal record is
[`m135-005-itemized-authorization-preparation.md`](../../workflow/m135-005-itemized-authorization-preparation.md).
No provider was constructed, credential read, report created, data sent or
request issued. A new user-selected G3 implementation workpack is required.
