# WP-M139-001: Frozen Hosted Campaign Launcher

- Status: done
- Milestone: M139
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2
- Trigger consumed: `WP-TRG-024`

## Goal

Design and locally implement a reusable frozen-campaign launcher.  It must
freeze one registered B-Rep/case input, path-free Q01 egress contract, optional
explicit card, first-pass and repair limits, executor, budget/deadline and
fresh report/monitor identity before any provider can be constructed.

## Scope

- Define a versioned campaign-spec schema and prepared-checkpoint state machine
  (`draft -> prepared_offline -> authorized -> terminal`) with hash-bound
  identity.
- Reuse only safe existing concepts where possible: registered input/case hash,
  allowlisted Q01 facts, card ID/hash/role, `wsl-bwrap`, provider deadline,
  request accounting and durable monitoring.
- Implement local `prepare` validation for input/split membership, transcript
  and card hashes, request/repair arithmetic, fresh/distinct report-monitor
  paths, no-input executor control and non-secret provider configuration
  presence.
- Define the narrow `execute` admission contract, but keep it locally testable
  and fail closed: M139 must not construct a provider or issue a request.
- Add fake/local regression tests, focused contract/module documentation, a
  runbook procedure and an ADR if the selected launcher boundary is an
  architecture decision.

## Compatibility constraints

- Offline and credential-free: do not access `.env`, construct a provider,
  send data or request hosted authorization.
- Registered B-Rep input is Harness-only.  Provider-bound material may contain
  only hash-pinned, allowlisted Q01 facts; never raw STEP, paths, reference
  scripts, provider responses or held-out answers.
- A card is opt-in by declared ID, content/index hashes and applicability role;
  it is never an arbitrary path or directory retrieval.
- Preserve M135/M138 reports, hashes, policy, budget and terminal conclusions.
  M139 cannot retrofit or resume them.
- Do not implement tool-turn orchestration, autonomous retrieval, repair
  routing, corpus expansion, card promotion, SDK/IR selection or hosted
  execution; these belong to later workpacks.

## Acceptance

Before acceptance, select independently bounded commands under the offline
validation planning runbook and record terminal outputs here.  The minimum
closure gates are:

```powershell
uv run python -m pytest tests -q
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

## Owner completion boundary

Publish the reviewed campaign-spec/checkpoint contract, local fail-closed
prepare implementation and evidence; update status, runbook/ADR as applicable
and handoff; then obtain Liaol's independent G2 review.  Do not request hosted
authorization as a completion substitute.

## Owner progress (2026-08-12)

- Added ADR-0070, the launcher contract and a `campaign-prepare` local CLI.
- The implementation accepts only a registered development case, hash-pinned
  split authority and Q01 transcript, optional registered card, `wsl-bwrap`,
  DeepSeek V4 declaration, one request and zero repair.
- Focused tests passed: `3 passed in 5.40s`, then `3 passed in 1.65s`; focused
  Ruff passed.  `pytest -m fast` passed `66 passed, 188 deselected in 9.68s`;
  repository Ruff and governance audit passed.
- The required standalone full suite reached the outer 600-second command
  window (`exit 124`) without a pytest terminal result.  It is recorded as a
  command-window limitation, not a pass/fail.  A subsequent hidden,
  monitorable local run reached a terminal pass: `254 passed in 652.42s`.
- Final local validation is complete: focused campaign tests, fast tests,
  repository Ruff, governance audit and diff check passed.  Owner work is
  complete.

## Independent review and closure (2026-08-12)

Liaol approved independent G2 review after examining the campaign input and
checkpoint fail-closed boundaries, local-only CLI path, M135/M138 preservation,
and deferred successor route.  The review accepts the M139 offline launcher;
it does not authorize a provider, hosted execute path, repair, card promotion
or tool-turn orchestration.  TRG-025 is consumed separately as M140.

## Permitted stop conditions

Independent review; a reproducible conflict with existing M135/M138 contracts;
an out-of-scope dependency on the future tool-loop/repair policy; frozen-input
drift; or a reproducible local validation blocker.

## Status transition

Update `docs/workflow/status.md` first, then this workpack and the active
handoff.  On closure, archive the workpack and consume the TRG-024 route while
leaving TRG-025 through TRG-028 deferred.
