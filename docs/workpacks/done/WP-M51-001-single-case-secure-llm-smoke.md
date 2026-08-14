# WP-M51-001: Single-Case Secure Real-LLM Smoke

- Status: done
- Milestone: M51
- Owner: Codex
- Reviewer: Liaol
- Risk tier: G3

## Goal

After a successful hosted preflight and explicit user authorization, send one
bounded M48 observation transcript for the existing self-authored `box` case
to the configured provider, execute its returned script only through
`wsl-bwrap` with no original STEP mount, and record a non-generalizing smoke
report.

## Scope

- Read-only preflight: selected input SHA-256, manifest/split scope,
  `wsl-bwrap` availability and no-input control, local non-secret provider
  configuration and model selection, CLI/report boundary, budget and deadline.
- On later explicit authorization only: one first-pass provider request, no
  repair, one fixed case, one generated script, secure no-input execution, and
  a compact report.

## Compatibility constraints

The provider receives only the M48 bounded observation transcript for `box`;
no raw STEP bytes, host path, file name, reference script, history, docs, or
trace path may leave the local machine. No external data, split expansion,
repair, prompt comparison, manifest change, IR/SDK, or model-quality claim.

## Trace/schema changes

No planned schema change. Use existing observation, provider, execution,
provenance, and report contracts; record the preflight and any request in a
new report path.

## Decision-package impact

- `decision_id`: `q01-q02-observation-build-separation-v1`.
- Q01/Q02 effect: one provider consumes the frozen observation-only contract.
- Q03/Q04 effect: retain existing gates and provenance eligibility; no repair.
- Evidence role: secure hosted smoke and negative no-input control.
- Knowledge disposition: no reusable modeling knowledge without a later review.

## Acceptance

- Preflight records all required inputs and receives explicit authorization
  before a provider request.
- Exactly one request is issued only after authorization; its deadline is
  bounded and its generated script runs only in `wsl-bwrap` without input.
- Report distinguishes provider lifecycle, build health, and provenance.
- Liaol independently reviews output before closure.

## Preflight result

Completed read-only checks on 2026-08-08:

- Fixed case is `box` in self-authored P0; SHA-256 is
  `C3C80420EAF7376DA5675EC1D5EA8FA93EF7A60F7EE24A516454C71E0797227C`.
  The isolated input probe passed (STEP, bbox `0/0/0` to `10/20/30`, 6 faces,
  volume 6000).
- Local WSL has `/usr/bin/bwrap` and the configured isolated runtime Python.
  Existing M48 no-input control remains the relevant offline executor evidence.
- Planned report path `data/corpus-runs/m51-box-deepseek-observation-first-pass.json`
  does not exist, so no prior running/interrupted checkpoint is being reused.
- Local DeepSeek configuration check failed because `DEEPSEEK_API_KEY` is not
  configured. No credential value was read into a trace or report.
- The existing hosted `corpus --first-pass` path sends its older
  `probe_summary` policy, including `file_name`, rather than the M48
  observation transcript. It therefore cannot be used for this workpack's
  observation-only egress contract.

No provider request is authorized or issued. Before seeking authorization, a
separately bounded G2 adapter must connect the M48 transcript to secure hosted
first-pass execution, and the local credential must be configured outside the
repository without disclosure to Codex.

M52 is complete and the user confirms local credential configuration. Resume
with a fresh read-only provider configuration check, then request itemized
authorization before any request.

## Status transition

Preflight alone does not close this workpack. If authorization is not granted,
record that no request was issued and retain/close only with user direction.
After an authorized smoke, record acceptance, reviewer result, status, and
handoff in that order.

## Closure rationale

Liaol authorized and independently approved one DeepSeek `deepseek-v4-pro`
first-pass request for the fixed `box` input. The M48 observation-only request
produced a readable STEP through `wsl-bwrap` with no input mount; bbox, volume,
and topology gates passed with zero delta. Report:
`data/corpus-runs/m51-box-deepseek-observation-first-pass.json`. This is one
secure smoke result only, not a generalization or model-quality claim.

## Out of scope

Any second request, repair round, held-out run, external input, case change,
provider/model change after authorization, or claim beyond one smoke case.
