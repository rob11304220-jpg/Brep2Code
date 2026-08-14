# WP-M135-004: Frozen Epoch Complete Hosted Preflight

- Status: done
- Milestone: M135
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G3

## Goal

Complete a fresh, credential-free local hosted preflight for M134's unchanged
18-condition epoch using M135-003's executable contract and entirely new
report/monitor identities. Request itemized hosted authorization only after
every local check and an independent G3 review pass.

## Scope

- Verify all frozen inputs, cards/policies, development split membership and
  order; run every no-card fixed script through no-input `wsl-bwrap`.
- Run `m135-epoch-preflight` with fresh `data/m135-004-preflight/` report and
  monitor paths; verify its 0/18 accounting and fixed executor/provider/model,
  deadline, output-cap and zero repair/retry boundary.
- Verify the static local DeepSeek configuration surface and secure executor
  availability without reading credentials or printing environment values.
- Verify the 18-request budget and actual CLI boundary without constructing a
  provider; inspect new paths for no reused `running`/`interrupted` checkpoint.
- Record all terminal local results and prepare—but do not send—the itemized
  authorization payload only after independent review.

## Attribution question and sampling intent

Can the exact frozen M134 cohort now enter a comparable single epoch under a
fully verifiable local execution boundary? This is an admission control, not a
provider or modeling evaluation. Stop on any integrity/preflight failure,
independent review or explicit hosted authorization.

## Inputs

- `docs/workflow/m134-frozen-hosted-batch-epoch-policy.md`
- `docs/workflow/m135-002-fresh-reentry-preflight.md`
- `docs/workflow/m135-003-frozen-epoch-cli-contract.md`
- `docs/architecture/adr/0067-frozen-hosted-batch-epochs.md`
- `docs/architecture/adr/0068-frozen-epoch-checkpoint-and-transcript-contract.md`
- `docs/runbooks/llm-provider-config.md`

## Code paths

- `brep2code/agent/m135_epoch.py`, `brep2code/cli/__init__.py` and focused
  tests only to correct a newly reproducible local preflight defect.

## Docs to update

- `docs/workflow/status.md`
- this workpack and one active handoff
- `docs/workflow/m135-004-complete-hosted-preflight.md`

## Trace/schema changes

No provider or outbound transcript schema change is intended. The local record
may contain only hashes, condition accounting, command outcomes, fixed-boundary
values and fresh-path evidence; it must contain no secrets, raw provider data,
raw STEP or absolute input paths.

## Decision-package impact

- `decision_id`: no Q01--Q04 package; hosted-evaluation governance re-entry.
- Q01/Q02 effect: no case, card, prompt, split, sequence or observable change.
- Q03/Q04 effect: validates the frozen execution/accounting boundary only.
- Evidence role: full-cohort local preflight regression.
- Knowledge disposition: no reusable knowledge.

## Compatibility constraints

Default operation remains offline and credential-free. Do not alter the frozen
cohort, input/card/policy hashes, order, provider/model, executor, deadline,
output cap, 18-request cap or zero repair/retry boundary. Do not construct a
provider, read credentials, send data, issue a request, modify manifests or
reuse any M135 report, monitor, budget or authorization.

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

Publish the M135-004 local preflight record with terminal results for all
controls and fresh-path evidence; pass every acceptance command and obtain
Liaol's independent G3 review. Only then request—not issue—itemized hosted
authorization.

## Permitted stop conditions

Independent review; explicit hosted authorization; frozen-input drift;
out-of-scope dependency; or reproducible local preflight/validation blocker.

## Evidence reuse / guidance-card disposition

No reusable knowledge. The existing prismatic card remains only its frozen
hash-pinned treatment input; all other conditions remain no-card.

## Status transition

Update `docs/workflow/status.md` first, then this workpack and the active
handoff. If blocked, archive this workpack with the local preflight record.

## Out of scope

Hosted execution or authorization issuance; provider construction; condition
addition/removal/reorder; prompt/card/model/provider changes; repair/retry;
case/manifest changes; held-out evaluation; card promotion; runtime changes;
or M137 terminal review.

## Owner-side completion rationale

The full credential-free preflight passed. M135-004 created and verified only
its fresh local 0/18 checkpoint and distinct monitor state, checked the public
configuration surface and local WSL availability, and passed the focused,
fast, full and Ruff gates. Terminal evidence is recorded in
[`m135-004-complete-hosted-preflight.md`](../../workflow/m135-004-complete-hosted-preflight.md).
No provider was constructed, credential read, data sent or request issued.
The workpack remains active solely for Liaol's independent G3 review; it cannot
prepare or request hosted authorization before that review.

## Independent review

Liaol approved the independent G3 review on 2026-08-12. The review accepted
the frozen cohort, M135-004-only 0/18 local checkpoint, distinct monitor
state, static configuration/executor checks and terminal offline evidence. It
does not grant hosted authorization. Any authorization preparation or execution
requires a new user-selected workpack and new report/monitor identities.
