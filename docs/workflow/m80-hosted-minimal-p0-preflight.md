# M80 Minimal P0 Hosted Preflight — Blocked

- **Date**: 2026-08-10
- **Workpack**: `WP-M80-001-minimal-p0-end-to-end-revalidation`
- **Mode**: local preflight only; no provider request issued

## Verified local boundary

| Field | Result |
|---|---|
| Prerequisite | M79 reviewed and accepted by Liaol. |
| Fixed input | P0 `box` in `case-library/manifests/self-authored/p0.json`; SHA-256 `C3C80420EAF7376DA5675EC1D5EA8FA93EF7A60F7EE24A516454C71E0797227C`. |
| Egress candidate | One path-free M48 `probe_summary` transcript only; current profile is 450 UTF-8 bytes, SHA-256 `92b3e13707dc2ad89e51651ed1960b10331742cb01f419331bfb059eacd7330b`. No raw STEP, path, file name, reference script, trace, credential, header or response content is proposed. |
| Control candidate | `provider-control-v1`; fixed user content `Return exactly OK.` plus the unchanged generic JSON-object adapter instruction; no local data. |
| Provider configuration | Non-secret check passed: DeepSeek `deepseek-v4-pro` at `https://api.deepseek.com`; API-key presence only was verified. |
| Executor | `wsl-bwrap` passed a local no-input box control with all required script/readability/bbox/volume/topology gates; bubblewrap `0.9.0`. |
| Request bound | Exactly two sequential requests total: one control, then one `observed-first-pass` box request; each has one-request capacity and zero repair. A later authorization would have to state one positive deadline (proposed: 120 seconds per request). |
| New paths | Proposed reports `data/corpus-runs/m80-deepseek-control.json` and `data/corpus-runs/m80-box-deepseek-observation-first-pass.json`, plus corresponding `data/monitor-runs/*.monitor.json`, are absent. |
| Authorization boundary | Both hosted CLI paths reject before provider construction when `--authorize-hosted` is absent. |

## Blocking monitor incompatibility

M70 monitor setup reads an already existing report that contains `run_status`.
Both current M80 commands write their first report only after the provider
worker returns or times out. Consequently no M70 monitor can observe the
in-flight control or box request. Creating a report manually would violate the
current command/report contract and would not be an authorized run.

M80 therefore fails its durable-monitor precondition. Do not request hosted
authorization, run the control, run `box`, or create/reuse a report capacity.

## Required re-entry

A separately selected G2 workpack must introduce an atomic pre-request
`running` checkpoint to `provider-control` and `observed-first-pass`, confirm
that M70 observes it without changing it, and add offline regression coverage.
It must not change the provider/model/endpoint, prompts, manifest, executor,
or M80 budget. After independent review, M80 needs a new preflight and fresh
report paths before a complete itemized G3 authorization may be requested.
