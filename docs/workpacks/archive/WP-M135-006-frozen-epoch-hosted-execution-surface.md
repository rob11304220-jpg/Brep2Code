# WP-M135-006: Frozen Epoch Hosted Execution Surface

- Status: blocked
- Milestone: M135
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G3

## Goal

Implement and offline-validate the fail-closed executable surface for M134's
frozen 18-condition epoch: fixed outbound context, serial one-request
lifecycle, authorization gate, durable checkpoint/monitor behavior and fixed
deadline/output/retry limits.

## Scope

- Add dedicated M135 prepare/execute lifecycle commands. Execute must reject
  missing explicit authorization, wrong provider/model/budget/deadline, stale
  or reused report/monitor identities and any frozen-contract drift before
  provider construction.
- Derive and hash a path-free, raw-STEP-free outbound payload for every frozen
  condition; append the existing hash-pinned card only to prismatic card rows.
- Exercise all 18 serial requests and terminal classifications through a fake
  provider offline. DeepSeek execution remains gated and is never invoked.
- Update durable CLI/report contracts and tests; record local evidence.

## Attribution question and sampling intent

Can the frozen cohort be executed only under the exact, reviewable boundary
that a user would later authorize? This is offline implementation evidence, not
provider or family evaluation.

## Inputs

- `docs/workflow/m134-frozen-hosted-batch-epoch-policy.md`
- `docs/workflow/m135-005-itemized-authorization-preparation.md`
- `docs/architecture/adr/0067-frozen-hosted-batch-epochs.md`
- `docs/architecture/adr/0068-frozen-epoch-checkpoint-and-transcript-contract.md`
- `docs/runbooks/llm-provider-config.md`

## Code paths

- `brep2code/agent/m135_epoch.py`, `brep2code/cli/__init__.py`, focused tests,
  and durable contracts/runbook only as required by the new command.

## Docs to update

- `docs/workflow/status.md`, this workpack, one active handoff and
  `docs/workflow/m135-006-frozen-epoch-hosted-execution-surface.md`
- `docs/architecture/v1/contracts/case-corpus.md` and
  `docs/runbooks/llm-provider-config.md`

## Trace/schema changes

Add only compact, hash-pinned outbound payload metadata and per-condition
lifecycle fields. Never persist credentials, raw STEP, local absolute paths,
raw provider output or outbound text.

## Decision-package impact

- `decision_id`: no Q01--Q04 package; hosted-evaluation execution governance.
- Q01/Q02 effect: no cases, splits, prompts, cards or sequences change.
- Q03/Q04 effect: makes M134's frozen accounting/authorization boundary
  executable and fail-closed.
- Evidence role: offline lifecycle and regression evidence.
- Knowledge disposition: no reusable knowledge.

## Compatibility constraints

Default operation is offline and credential-free. Do not invoke DeepSeek,
read credentials, send data, alter cohort/order/hash/provider/model/executor,
change 120-second deadline/no output cap/18-request/zero repair-retry bounds,
or reuse prior M135 report/monitor/budget/authorization.

## Acceptance

```powershell
uv run python -m pytest tests\test_m135_epoch.py -q
uv run python -m pytest -m fast -q
uv run python -m pytest
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

## Owner completion boundary

Publish the executable contract and M135-006 local evidence; pass acceptance
and obtain Liaol's independent G3 review. A later fresh preflight and explicit
itemized user authorization remain required before any hosted execution.

## Permitted stop conditions

Independent review; explicit hosted authorization; frozen-input drift;
out-of-scope dependency; or reproducible local blocker.

## Evidence reuse / guidance-card disposition

No reusable knowledge. Prismatic cards remain frozen treatment inputs only.

## Status transition

Update status first, then workpack and handoff. Run governance audit after
lifecycle edits.

## Out of scope

Any hosted request, provider construction, credential access, case/prompt/card
changes, repair/retry, held-out work, runtime promotion or M137 review.

## Blocked closure rationale

The workpack added the deterministic, path-free transcript hash layer and
validated it offline, but the actual M135 execute lifecycle remains absent.
Without an `ObservedBuildLoopRunner` integration, authorization gate and
per-condition terminal checkpoints, this cannot be an executable hosted
surface. See [`m135-006-frozen-epoch-hosted-execution-surface.md`](../../workflow/m135-006-frozen-epoch-hosted-execution-surface.md).
