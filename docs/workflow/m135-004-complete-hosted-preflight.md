# M135-004 Complete Frozen Epoch Hosted Preflight

- **Date**: 2026-08-12
- **Workpack**: `WP-M135-004-frozen-epoch-complete-hosted-preflight`
- **Scope**: local, credential-free; no provider construction or egress
- **Status**: passed locally and approved by independent G3 review

## Frozen boundary and fresh paths

The unchanged M134 cohort is 18 ordered development conditions: twelve no-card
conditions followed by six prismatic card/no-card conditions. The M135-004
local command created new, previously absent paths:

- report: `data/m135-004-preflight/epoch-report.json`
- monitor: `data/m135-004-preflight/epoch-monitor.json`

The report is a local `prepared` checkpoint only: `requests_used: 0`,
`requests_remaining: 18`, `authorization: not_authorized`, and
`provider_constructed: false`. The distinct monitor state observes it locally.
No previous M135 report, monitor, budget or authorization was reused.

## Fixed local contract

| Field | Verified value |
|---|---|
| Provider / model identity | `deepseek / deepseek-v4-pro` |
| Endpoint configuration surface | `https://api.deepseek.com` in tracked `.env.example` |
| Secure executor | `wsl-bwrap`; `wsl.exe` available locally |
| Provider deadline | 120 seconds |
| Output cap | none selected (`null`) |
| Request cap | 18; serial checkpoint starts at 0/18 |
| Repair / retry | zero / zero |
| Credential boundary | `.env` was not read; only tracked `.env.example` was inspected |

`m135-epoch-preflight --help` exposes only `--report`, `--monitor-state` and
`--stale-after`; it has no provider, authorization, credential or execution
argument. The command is therefore a local execution-boundary check, not a
hosted command.

## Terminal local evidence

| Control | Terminal result |
|---|---|
| Fresh CLI checkpoint and monitor preparation | `prepared_offline`; 0 used / 18 remaining; monitor `monitoring` |
| Frozen input hashes, fake 18-condition lifecycle and no-input `wsl-bwrap` controls | `uv run python -m pytest tests\\test_m135_epoch.py -q`: 7 passed in 92.14s |
| Fast offline regression | `uv run python -m pytest -m fast -q`: 66 passed, 179 deselected in 4.41s |
| Full offline suite | `uv run python -m pytest`: 245 passed in 441.17s |
| Static check | `uv run python -m ruff check .`: All checks passed |

No provider was constructed, no credential was read, no request was issued and
no raw STEP, provider response or outbound transcript left the local machine.

## Review and authorization boundary

The owner-side preflight passes but grants no hosted authority. Liaol must
complete independent G3 review. Only after that review may the user consider a
separately selected follow-up workpack to prepare an itemized authorization
request; it must use new report/monitor paths because this preflight's report
is already a local `running` preparation artifact.

## Independent review

Liaol approved the independent G3 review on 2026-08-12. The approval covers
only the stated local contract and evidence. It neither authorizes provider
construction nor approves egress, an endpoint call, a request budget, or epoch
execution.
