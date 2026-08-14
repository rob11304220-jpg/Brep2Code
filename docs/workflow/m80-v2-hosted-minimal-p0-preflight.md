# M80-v2 Minimal P0 Hosted Preflight — Awaiting Authorization

- **Date**: 2026-08-10
- **Workpack**: `WP-M80-001-minimal-p0-end-to-end-revalidation`
- **Mode**: read-only local preflight; no provider request issued

## Fixed sequential plan

| Step | Destination/model | Outbound content | Bound and deadline | Fresh report / monitor |
|---|---|---|---|---|
| Control | `https://api.deepseek.com`, DeepSeek `deepseek-v4-pro` | Fixed `provider-control-v1` text `Return exactly OK.` plus generic JSON-object instruction; no local data. | One request, zero repair, 120 seconds. | `data/corpus-runs/m80-v2-deepseek-control.json` / `data/monitor-runs/m80-v2-deepseek-control.monitor.json` |
| Box | Same destination/model | One M48 path-free `probe_summary` transcript for P0 `box`; current profile: 450 UTF-8 bytes, SHA-256 `ee5b4b7841bc06c549b084cfe3ed62b5b0e8aad1a533d8cfdcb26a00aae0ccc5`. No raw STEP, host path, filename, reference script, history, docs, trace, credential, header or provider response. | One first-pass request, zero repair, 120 seconds; generated script executes only in `wsl-bwrap` without original STEP mount. | `data/corpus-runs/m80-v2-box-deepseek-observation-first-pass.json` / `data/monitor-runs/m80-v2-box-deepseek-observation-first-pass.monitor.json` |

The maximum is exactly two sequential issued requests. No cost cap is claimed
because account pricing was not inspected. The box command cannot start unless
the control has a parseable terminal `completed` report without a lifecycle or
timeout error.

## Read-only checks

- M79 and M81 are independently accepted. M81's focused prepare/monitor/execute
  regression passed again: 22 tests in 46.25 seconds.
- `box` remains a P0 member of `p0.json`; input SHA-256 is
  `C3C80420EAF7376DA5675EC1D5EA8FA93EF7A60F7EE24A516454C71E0797227C`.
- A fresh no-input `wsl-bwrap` box control passed script, readable STEP, bbox,
  volume and topology gates. The executor reports bubblewrap `0.9.0`.
- Non-secret configuration check selects `deepseek-v4-pro` at
  `https://api.deepseek.com`; only API-key presence was checked.
- All four report/monitor paths in the table are absent. No running or
  interrupted checkpoint, report capacity or historic authorization is reused.
- Both hosted CLI paths reject without `--authorize-hosted` before provider
  construction. The producer-owned `--phase prepare` / M70 monitor / `--phase
  execute` sequence is the required launch lifecycle.

## Risk and authorization gate

Each request may occupy its complete 120-second deadline; local preparation,
monitoring and box execution add overhead. Run each phase with the durable M70
monitor; it neither retries nor resumes. A timeout, lifecycle error, malformed
or non-terminal control report, report-path violation, script error or geometry
gate failure stops M80 immediately without retry or profile adjustment.

This preflight does not authorize egress. To authorize M80, Liaol must approve
the exact destination and two outbound-content boundaries, provider/model,
single control then single `box` scope, non-streaming JSON-object mode, zero
repair, 120-second deadline per request, two-request total cap, `wsl-bwrap`,
and all four report/monitor paths listed above.

## Authorized outcome

Liaol authorized the full listed scope on 2026-08-10. The control report
reached terminal `completed` with one request and its M70 monitor terminalized
normally. The box request was then issued once, through the frozen profile and
its own monitor. It also received a response and reached a terminal parseable
report without timeout or lifecycle error.

The box generated script failed at `wsl-bwrap` execution because it imported
`cadquery`, which is not installed in the execution environment. No STEP output
was produced, so script-exit and output-readability gates failed and the
geometry comparisons were unavailable. This is a bounded generated-script
compatibility failure, not evidence of endpoint failure, provider-wide
availability, prompt causality, or model quality. Both capacities are consumed;
M80 stops with no retry, repair or M73 progression.
