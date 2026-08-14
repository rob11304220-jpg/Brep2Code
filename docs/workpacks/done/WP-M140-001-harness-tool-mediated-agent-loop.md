# WP-M140-001: Harness Tool-Mediated Agent Loop

- Status: done
- Milestone: M140
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2
- Trigger consumed: `WP-TRG-025`

## Goal

Implement the bounded Harness-owned agent turn loop: an LLM may request
declared Q01 probes or one explicitly selected guidance card, receive sanitized
tool results, emit a replacement script, and receive structured execution/gate
feedback.

## Scope

- Define provider-neutral tool-call/tool-result continuation semantics that
  compose with M139 prepared campaign identity.
- Expose only schema-bound, revision-scoped Q01 probes and explicitly selected
  guidance cards; enforce total/per-turn tool limits, byte/token caps and
  trace redaction.
- Execute scripts only through the restricted Harness, returning structured
  signal summaries rather than shell access or raw workspace data.
- Add fake-provider/local-sandbox tests for no-card, unavailable/wrong-card,
  malformed/over-budget calls, script generation, execution and gate feedback.
- Record the adopted boundary and update relevant contracts/runbooks; ReAct and
  Toolformer are research inputs, not evidence of CAD tool effectiveness.

## Compatibility constraints

- Offline and credential-free.  Do not construct a provider, read `.env`, send
  data or request hosted authorization.
- Keep the input B-Rep Harness-only.  No raw STEP, paths, reference scripts,
  held-out answers, arbitrary filesystem reads or shell access may reach the
  LLM.
- Preserve M135/M138 terminal evidence and M139 campaign/checkpoint semantics.
- Cards remain absent by default and are selected only by frozen ID/hash/role;
  no directory retrieval or automatic prompt injection.
- Do not define repair routing, case expansion/admission, runtime knowledge
  promotion or hosted execution; those remain TRG-026 through TRG-028/G3 work.

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

Publish the reviewed tool-turn contract, local fail-closed implementation and
validation evidence; update status, runbook/ADR as applicable and handoff;
then obtain Liaol's independent G2 review.  Do not request hosted authorization
as a completion substitute.

## Owner completion evidence

- Added `ToolTurnLoopRunner`: a fake-provider-only, fail-closed continuation
  loop that binds a fresh M139 checkpoint identity, dispatches one declared
  Q01 probe or selected hash-pinned card per turn, applies global turn/tool/
  result-byte bounds, then emits terminal execution/gate feedback without a
  repair continuation.
- Added the adopted contract at
  `docs/architecture/v1/contracts/harness-tool-turn-loop.md` and the focused
  offline check in `docs/runbooks/runtime-sandbox.md`.
- Focused check: `uv run python -m pytest tests\test_tool_turn_loop.py tests\test_agent_m3_tool_bridge.py tests\test_guidance_bridge.py -q` — `19 passed in 25.98s`.
- Full suite: `uv run python -m pytest tests -q` — `260 passed in 654.00s`.
  An earlier 484-second command window had no terminal result; the collected
  suite contains 260 tests, and the later independent 1200-second window
  completed successfully.
- `uv run python -m ruff check .` — passed.
- `uv run python tools\check_governance.py` — `Governance audit passed.`
- `git diff --check` — passed.

## Independent review and closure (2026-08-12)

Liaol approved the independent G2 review. The review confirmed that M140
keeps the B-Rep Harness-only, accepts only the fake provider, bounds declared
probe/card calls and result sizes, returns sanitized execution/gate feedback,
and does not construct a hosted provider or introduce repair routing. M140 is
therefore complete; it does not authorize hosted tool turns, provider changes,
card promotion or repair. `WP-TRG-026` is separately selected and consumed as
M141.

## Permitted stop conditions

Independent review; a reproducible conflict with M139 campaign/checkpoint
contracts; an out-of-scope dependency on repair policy; frozen input/resource
drift; or a reproducible local validation blocker.

## Status transition

Update `docs/workflow/status.md` first, then this workpack and the active
handoff.  On closure, archive the workpack and leave TRG-026 through TRG-028
deferred.
