# WP-M135-002: Frozen Epoch Fresh Re-entry Preflight

- Status: blocked
- Milestone: M135
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G3

## Goal

Re-run the complete M134 frozen 18-condition epoch preflight after M136's
approved no-input fixed-script remediation, using unchanged cohort inputs and
fresh report/monitor identities. Request itemized hosted authorization only if
the entire fresh local preflight and independent G3 review pass.

## Scope

- Verify each frozen input/card/policy hash, split membership, order, and
  no-input `wsl-bwrap` fixed-script control.
- Verify fresh report/monitor paths, fixed serial 18-request accounting,
  provider/model configuration surface, executor, deadline, cap, and zero
  repair/retry policy without constructing a provider.
- Re-run fake-provider checkpoint/transcript lifecycle and record every local
  preflight result in a new M135-002 record.
- Prepare, but do not send, the itemized authorization payload if all checks
  and independent G3 review pass.

## Attribution question and sampling intent

Does the unchanged M134 cohort now satisfy the local, no-input execution and
accounting prerequisites for a single comparable epoch? This is a full frozen
cohort admission check, not provider evaluation. Stop on any preflight failure,
epoch-integrity fault, independent review, or explicit hosted authorization.

## Inputs

- `docs/workflow/m134-frozen-hosted-batch-epoch-policy.md`
- `docs/workflow/m135-frozen-epoch-preflight-blocked.md`
- `docs/workflow/m136-m135-no-input-sandbox-remediation-record.md`
- `docs/architecture/adr/0067-frozen-hosted-batch-epochs.md`
- `docs/architecture/adr/0068-frozen-epoch-checkpoint-and-transcript-contract.md`
- `docs/architecture/adr/0069-m135-remediation-and-terminal-review-rescheduling.md`

## Code paths

- `brep2code/agent/m135_epoch.py`, focused tests, and preflight-only helpers
  only when required to correct a newly reproducible local preflight defect.

## Docs to update

- `docs/workflow/status.md`
- this workpack and one active handoff
- a new `docs/workflow/m135-002-fresh-reentry-preflight.md` record
- relevant durable contract/runbook only if a lasting command or schema changes

## Trace/schema changes

No provider or outbound transcript schema change is intended. The fresh local
preflight record must contain hashes, condition accounting, command results,
fresh-path evidence, and no secret or raw provider content.

## Decision-package impact

- `decision_id`: no Q01--Q04 package; hosted evaluation governance re-entry.
- Q01/Q02 effect: no case, card, prompt, split, sequence, or observable change.
- Q03/Q04 effect: validates the frozen no-input execution/accounting boundary.
- Evidence role: full-cohort local preflight regression.
- Knowledge disposition: no reusable knowledge.

## Compatibility constraints

Default operation remains offline and credential-free. Retain all 18 condition
identities, hashes, order, treatment, provider/model policy, executor,
deadline, output cap, zero-repair/zero-retry policy, and no-input boundary.
Do not construct a provider, send data, issue a request, reuse M135-001 report,
monitor, request budget, or authorization, modify any prompt/card/model/provider,
or alter executable manifests.

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

Publish the fresh M135-002 preflight record with terminal results for every
required local control and fresh-path verification; pass all listed checks and
obtain Liaol's independent G3 review. Only then request—not issue—itemized
hosted authorization.

## Permitted stop conditions

Independent review; explicit hosted authorization; frozen-input drift;
out-of-scope dependency; or reproducible local preflight/validation blocker.
Partial implementation or validation is not a stop condition.

## Evidence reuse / guidance-card disposition

No reusable knowledge. The existing prismatic card remains only its frozen,
hash-pinned treatment input; all other conditions remain no-card.

## Status transition

Update `docs/workflow/status.md` first, then this workpack and the active
handoff. If blocked, archive this workpack with its new preflight record. M137
remains separately user-selected after a terminal authorized M135 epoch.

## Out of scope

Hosted execution or authorization issuance; condition addition/removal/reorder;
prompt/card/model/provider changes; repair/retry; case/manifest changes;
held-out evaluation; card promotion; runtime changes; or M137 terminal review.

## Blocked closure rationale (2026-08-12)

The complete credential-free test and validation suite passed, including the
full no-input `wsl-bwrap` control. The fresh local preflight is nevertheless
blocked because the actual M135 18-condition epoch CLI/monitor execution
surface is absent: `brep2code.agent.m135_epoch` has only checkpoint helpers
and no `brep2code.cli` command binds the frozen provider/model, deadline,
output cap, serial 18-request budget, report, and monitor contract together.
The detailed terminal evidence is recorded in
[`m135-002-fresh-reentry-preflight.md`](../../workflow/m135-002-fresh-reentry-preflight.md).
No provider was constructed, no data was sent, and no hosted authorization was
requested. A new user-selected G3 workpack is required before re-entry.
