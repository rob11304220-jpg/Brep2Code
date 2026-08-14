# M135-010 Fresh Complete Hosted Preflight

- **Date**: 2026-08-12
- **Workpack**: `WP-M135-010-fresh-complete-hosted-preflight`
- **Scope**: credential-free local preflight; no provider construction or egress

## Fresh local checkpoint

`data/m135-010-preflight/epoch-report.json` and its distinct
`epoch-monitor.json` were absent before preparation. `m135-epoch-preflight`
created the report with all 18 frozen conditions `not_issued`, 0 used / 18
remaining, `deepseek / deepseek-v4-pro`, `wsl-bwrap`, 120-second deadline,
no output-token cap, and zero repair/retry. The report records
`authorization: not_authorized` and `provider_constructed: false`; the monitor
is monitoring with the report's own distinct path. This newly prepared
checkpoint is local preflight evidence only and cannot be reused as a hosted
run or budget.

## Static boundary checks

The tracked `.env.example` declares only `DEEPSEEK_API_KEY`,
`DEEPSEEK_MODEL=deepseek-v4-pro`, and `DEEPSEEK_BASE_URL`; no `.env`,
credential or environment value was read. `wsl.exe` is locally available. The
M135 command does not accept a provider selection or authorization flag and
its implementation calls only `prepare_preflight_checkpoint`; its checkpoint
declares no provider constructed. M135-008/009 tests remain the all-condition
request/card/no-input runner and serial-accounting evidence.

## Authorization parameters, if a later request is made

No authorization is requested by this record. A later explicit request must
name: DeepSeek API destination; `deepseek / deepseek-v4-pro`; only the frozen,
path-free 18 development condition transcripts plus the bounded derived card
for the three card rows (never raw STEP or reference scripts); 18 cases, one
request per case, zero repair/retry, at most 18 requests; 120 seconds per
request; `wsl-bwrap`; and a new report/monitor identity, because this
preflight checkpoint is not reusable. The batch may exceed an interactive
command limit and therefore needs durable monitoring. Any such request is
subject to fresh independent review and explicit itemized user approval.
