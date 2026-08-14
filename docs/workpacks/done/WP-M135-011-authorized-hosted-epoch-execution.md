# WP-M135-011: Authorized Hosted Epoch Execution

- Status: done
- Milestone: M135
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G3

## Goal

Perform M134's fixed 18-condition hosted epoch only after a new local
preflight, independent review, and the user's explicit itemized authorization.

## Scope

- Create and validate M135-011-only fresh local report/monitor preflight
  paths, fixed input/request/card/runner contracts, static configuration
  surface, executor availability and no-reuse rules.
- Present the precise destination, egress boundary, provider/model, condition
  scope, one-request/zero-repair/zero-retry policy, deadline, request budget,
  durable-monitoring plan and risks for explicit user authorization.
- Only after that authorization, construct the selected provider and issue the
  frozen serial epoch through the no-input Harness path, persist checkpoints,
  and retain sanitized evidence.

## Compatibility constraints

Until the user explicitly approves every authorization item, do not construct
a provider, access credentials, send data, issue a request, or start the
epoch. Use only the 18 frozen development conditions, path-free transcript and
three bounded card injections; never send raw STEP or reference scripts. Keep
the fixed `deepseek / deepseek-v4-pro`, `wsl-bwrap`, 120-second deadline,
18-request cap and zero repair/retry policy. Use M135-011-only fresh report
and monitor paths.

## Authorization gate

Before provider construction, the user must explicitly approve: destination
and outbound content; `deepseek / deepseek-v4-pro`; all 18 frozen development
conditions; one request each / no retries / no repair; 120-second deadline;
18-request maximum; and the new report/monitor paths. A generic “approve” or
workpack selection alone does not pass this gate.

## Itemized authorization (2026-08-12)

The user explicitly approved all six stated items: DeepSeek API destination;
`deepseek / deepseek-v4-pro`; the 18 frozen path-free development transcripts
and three bounded card injections (no raw STEP, reference scripts, absolute
paths or credentials); one request per condition and 18 maximum; zero
repair/retry, 120-second deadline and no-input `wsl-bwrap`; and M135-011-only
fresh report/monitor paths with durable monitoring. This authorization applies
only to this workpack and does not authorize changes to the frozen boundary.

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

If authorized, publish the terminal epoch report, monitor evidence and
sanitized condition accounting, pass applicable acceptance gates and obtain
Liaol's independent G3 review. If authorization is not given, record the
authorization boundary without provider construction or egress.

## Permitted stop conditions

Explicit hosted authorization; independent review; frozen-input drift;
out-of-scope dependency; or reproducible local preflight/validation blocker.

## Status transition

Update `docs/workflow/status.md` first, then this workpack and the active
handoff. Keep the workpack in `active` while awaiting authorization or review.

## Out of scope

Any cohort, prompt, card, model, provider, executor, deadline, output-cap,
repair/retry, manifest, held-out, card-promotion or M137 change.

## Terminal result and independent review (2026-08-12)

Liaol approved the independent G3 review. The M135-011 report completed at
18/18 requests with no retry, repair or epoch-integrity fault: three
dependent-face-selection no-card conditions were `full_success`; 11 other
no-card conditions were `downstream_gate_failed`; the prismatic nominal
no-card condition was `sandbox_execution_failed`; and all three prismatic
card conditions were `static_api_inadmissible`. These are frozen cohort,
condition-level Harness observations only. They do not establish model
capability, family-level generalization, a card effect, or a reason to modify
the prompt, card, gates, cohort or runtime.
