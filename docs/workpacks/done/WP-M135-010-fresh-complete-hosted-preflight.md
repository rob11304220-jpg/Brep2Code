# WP-M135-010: Fresh Complete Hosted Preflight

- Status: done
- Milestone: M135
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G3

## Goal

Complete a new credential-free, local-only hosted preflight for M134's frozen
18-condition M135 epoch after the reviewed request-to-terminal and serial
lifecycle contracts.

## Scope

- Create and inspect a newly named, distinct local report and monitor state
  with `m135-epoch-preflight`, zero issued requests and the fixed 18-condition
  policy values.
- Revalidate frozen input/transcript/card/request hashes, all-condition
  no-input fake lifecycle evidence, static DeepSeek configuration surface and
  local `wsl-bwrap` availability without reading credentials.
- Verify the actual CLI boundaries, fixed 18-request / zero repair / zero
  retry / 120-second deadline contract, fresh-path collision rejection and
  absence of re-usable running/interrupted M135 report paths.
- Record the required authorization parameters and risks without requesting or
  issuing authorization.

## Compatibility constraints

No provider construction, credential access, egress, request issuance,
cohort/card/prompt/model/provider change, retry, repair, manifest change or
reuse of prior M135 report, monitor, budget or authorization. The workpack is
local, credential-free admission control only.

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

Publish the terminal local preflight record and authorization-ready parameter
summary, pass all acceptance commands, and obtain Liaol's independent G3
review. Only then may the user be asked for explicit, itemized hosted
authorization in a separate step.

## Permitted stop conditions

Independent review; explicit hosted authorization; frozen-input drift;
out-of-scope dependency; or reproducible local preflight/validation blocker.

## Status transition

Update `docs/workflow/status.md` first, then this workpack and the active
handoff. Keep the active workpack's machine-readable status as `active` while
awaiting review.

## Out of scope

Hosted execution or authorization issuance; provider construction; credential
inspection; any request; repair/retry; new cases; held-out evaluation; card
promotion; and M137 terminal review.

## Owner completion evidence (2026-08-12)

Fresh paths `data/m135-010-preflight/epoch-report.json` and
`epoch-monitor.json` were absent before preparation and now contain the local
0 used / 18 remaining checkpoint, distinct monitor, all frozen condition
hashes, fixed executor/deadline/zero-repair/zero-retry boundary and
`provider_constructed: false`. The local provider configuration template and
`wsl.exe` surface were inspected without reading `.env` or environment values;
the M135 preflight CLI has no provider construction path. The local record and
authorization parameters are in
[`m135-010-fresh-complete-hosted-preflight.md`](../../workflow/m135-010-fresh-complete-hosted-preflight.md).

Owner-side acceptance passed: focused M135 `12 passed in 211.77s`; fast `66
passed`; full suite `250 passed in 597.94s` after one non-conclusive 600-second
outer-window timeout; Ruff, governance audit and diff check passed. Await
Liaol's independent G3 review. No provider was constructed, credential read,
authorization requested or data sent.

## Independent review and closure (2026-08-12)

Liaol approved the independent G3 review. The review accepted the fresh 0/18
checkpoint, frozen request/runner boundary, configuration/executor checks and
recorded offline validation. This closure grants no hosted execution authority;
any provider construction or request still needs the user's explicit,
itemized authorization.
