# M63 Hosted Preflight — Awaiting Authorization

- **Date**: 2026-08-09
- **Workpack**: `WP-M63-001-m54-fresh-hosted-preflight-and-decision-gate`
- **Mode**: read-only; no provider request issued

## Proposed hosted batch

| Item | Preflight value |
|---|---|
| Destination | `https://api.deepseek.com` |
| Provider/model | DeepSeek `deepseek-v4-pro` |
| Outbound content | M48 path-free bounded observation transcripts only; no raw STEP, local path, filename, reference script, docs, trace, credential, or environment value |
| Cases | 12 development rows in `case-library/manifests/self-authored/parametric-development.json` |
| Rounds | One first pass plus at most one repair per case |
| Request cap | 24 (`12 × (1 + 1)`) |
| Per-request deadline | 120 seconds |
| Executor | `wsl-bwrap`, no original STEP mount during generated build execution |
| New report path | `data/corpus-runs/m63-parametric-development-deepseek-observation.json` |

## Read-only checks

- Manifest SHA-256 is
  `DC4C6E8F3302367A3B1082FAD602FE36FF2A59901E59079695DA75724892A593`;
  all 12 rows remain `development`. Every selected input hash matches the
  recorded identity table in [`m54-hosted-preflight.md`](m54-hosted-preflight.md).
- The local non-secret provider configuration parses as `deepseek-v4-pro` at
  `https://api.deepseek.com` with a 120-second timeout. No credential value was
  displayed or written.
- WSL confirms executable `/usr/bin/bwrap` and `/usr/bin/python3`. M56's
  offline multi-case `wsl-bwrap` control and M60's lifecycle checkpoint
  projection remain covered by the current offline tests.
- The `observed-development` CLI requires `--authorize-hosted`, validates a
  positive request budget bounded by `max_cases × (1 + max_rounds)`, and
  refuses a provider timeout below one second before provider construction.
- The proposed M63 report path does not exist; it has no `running` or
  `interrupted` checkpoint. M54's earlier reports and their nominal remaining
  budgets are not eligible for reuse.

## Risk and monitoring boundary

At the maximum bound, provider waits alone can total 48 minutes, excluding
local observations and sandbox executions. M62's local test baseline recommends
independent eight-minute windows for sandbox/full test commands; it does not
bound a hosted batch. Any authorized hosted run must use durable monitoring,
not an interactive command deadline.

## Authorization gate

This preflight does not authorize egress. A new authorization must explicitly
approve the destination and outbound content above, DeepSeek
`deepseek-v4-pro`, the fixed 12-case scope, one first pass plus at most one
repair, 24-request cap, 120-second per-request deadline, `wsl-bwrap`, and the
new M63 report path. It must not be read as authorization to reuse M54's prior
budget or to conduct a connectivity probe.

## Authorized run outcome

On 2026-08-09, the user supplied the required itemized authorization and the
fresh M63 batch was launched with exactly the preflight values above. Its first
case, `param_additive_boss_low`, issued one provider request. The request
reached the 120-second deadline and atomically wrote the proposed report as
`interrupted` with `requests_used=1`, `requests_remaining=23`, zero completed
cases, and non-sensitive lifecycle diagnostics showing `worker_started` then
`http_started`. This records a provider-request timeout only; it is not model,
geometry, or sandbox quality evidence. The nominal 23 requests are not
reusable, and the next decision is Liaol's independent review.
