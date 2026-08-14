# WP-M80-001: Minimal P0 End-to-End Revalidation

- Status: done
- Milestone: M80
- Owner: Codex
- Reviewer: Liaol
- Risk tier: G3

## Goal

Establish the narrowest current-contract evidence that a simple P0 B-Rep can
travel through bounded observation, an authorized LLM call, generated
`build_sequence.py`, `wsl-bwrap` execution, and the existing STEP/geometry
gates.

## Preconditions

- M79 is accepted and supplies a reviewed `reproduction-profile-v1`.
- A new G3 preflight verifies the P0 `box` hash and membership, frozen profile,
  non-secret configuration, `wsl-bwrap`, two unused report paths, per-request
  deadline and the two-request maximum.
- The user separately authorizes destination, provider/model, control content,
  path-free `box` observation summary, mode, no-repair bound, deadline, budget,
  executor and report paths.

## Scope

Run sequentially, with durable M70 monitors:

1. One `provider-control` request using its fixed control content.
2. One P0 `box` observation-to-first-pass request with no repair, then execute
   the generated script only in `wsl-bwrap` and evaluate the existing gates.

Each report has one request capacity. Do not run the `box` call until the
control has a parseable successful terminal report.

## Minimal end-to-end gate

M80 passes only when both reports are terminal and parseable, neither issued
request ends in timeout/lifecycle error, the frozen profile matches both
reports, and `box` passes script exit, output readability, bbox, volume and
topology gates. The conclusion is limited to this one frozen P0 path.

## Stopping rule

Any timeout, lifecycle error, budget/report-path violation, unclassified
script error or geometry-gate failure stops the workpack. Do not retry, alter
the profile, add a case, start M73, or reuse capacity.

## Acceptance

Record both report paths and terminal result, then run the relevant offline
report/contract checks, Ruff, governance audit and `git diff --check`. G3
closure requires Liaol's independent review.

## Out of scope

General provider availability, repair, prompt comparison, P1/held-out cases,
model/endpoint change, external data, and model-quality or benchmark claims.

## Activation record

- Liaol selected M80 on 2026-08-10 after independently approving M79.
- Initial work is restricted to the required local preflight. No provider
  request, report capacity, or egress authorization is implied by activation.

## Read-only preflight and blocker

- M79 is accepted. P0 `box` remains in `p0.json`; its SHA-256 is
  `C3C80420EAF7376DA5675EC1D5EA8FA93EF7A60F7EE24A516454C71E0797227C`.
  The frozen one-call M48 observation profile is 450 UTF-8 bytes with digest
  `92b3e13707dc2ad89e51651ed1960b10331742cb01f419331bfb059eacd7330b`.
- A local no-input `wsl-bwrap` control passed script, readable-output, bbox,
  volume and topology gates. Non-secret configuration selects
  `deepseek-v4-pro` at `https://api.deepseek.com`; WSL reports bubblewrap
  `0.9.0` and `/usr/bin/python3`. Two proposed reports and two monitor-state
  paths are absent, so no old checkpoint or budget is in scope.
- The actual hosted CLIs refuse both control and box paths before provider
  construction without `--authorize-hosted`; no provider request occurred.
- **Stop condition:** M70 monitor setup requires an existing report containing
  `run_status`. `provider-control` and `observed-first-pass` first write their
  reports only after the provider call returns or times out. The monitor thus
  cannot observe either authorized request while it is in flight. M80 requires
  durable M70 monitors, so its preflight fails and no authorization request is
  permitted.
- Required re-entry: select a new bounded G2 workpack to add an atomic,
  fail-closed pre-request `running` checkpoint to both paths and cover it with
  monitor/report tests. It must not issue a provider request or alter M80's
  endpoint, prompt, case, executor, or budget. Then re-run a fresh M80
  preflight with new report paths and seek new itemized G3 authorization.

## Re-entry record

- Liaol approved M81 on 2026-08-10. The former monitor-lifecycle blocker is
  resolved by producer-owned `prepare`/`execute` checkpoints; M80 is
  reactivated for a completely fresh local preflight only.
- The prior M80 report paths, profile and authorization status are not reused.
  This re-entry must choose new report/monitor paths and re-check every G3
  preflight item before requesting authorization.

## M80-v2 read-only preflight

- [`m80-v2-hosted-minimal-p0-preflight.md`](../../workflow/m80-v2-hosted-minimal-p0-preflight.md)
  records the fresh input/profile/configuration/executor/report-path and
  prepare/monitor/execute checks. It passes locally and makes no provider
  request.
- The next action is a new itemized G3 authorization. It must cover both
  sequential requests, their v2 reports and monitor paths, the 120-second
  deadline, two-request cap, zero repair, and `wsl-bwrap`; prior M51--M72/M80
  paths, budgets and authorizations remain ineligible for reuse.

## Authorization

- On 2026-08-10, Liaol explicitly authorized the complete M80-v2 scope in
  `m80-v2-hosted-minimal-p0-preflight.md`: the DeepSeek endpoint/model, fixed
  control and path-free box-transcript egress, sequential zero-repair mode,
  120-second per-request deadline, two-request cap, `wsl-bwrap`, and all four
  fresh report/monitor paths. This authorization covers no retry, path, model,
  case, prompt or budget expansion.

## Authorized execution record

- Control prepared, received an M70 monitor, and reached parseable terminal
  `completed` within the authorized deadline. Its dedicated report records one
  issued request and no local-data egress.
- Only after that terminal result, box prepared and received its own M70
  monitor. It reached parseable terminal `completed` at the report lifecycle
  level with one issued request. The provider response returned in 22.900 s;
  the complete observed-build path took 31.256 s.
- The generated script then failed in `wsl-bwrap` with `ModuleNotFoundError:
  No module named 'cadquery'`. No `output/model.step` was created; script exit
  and output-readability gates failed, and bbox/volume/topology comparisons
  were skipped. The report/monitor lifecycle is successful evidence, but the
  M80 minimal end-to-end geometry gate fails.
- Stopping rule applies: both report capacities are consumed. Do not retry,
  adjust the profile, start repair, add a case, or enter M73. The owner must
  now run the offline closure checks and Liaol must independently review the
  report paths, accounting, stop disposition and limited interpretation.

## Owner acceptance record

- Terminal reports: `data/corpus-runs/m80-v2-deepseek-control.json` and
  `data/corpus-runs/m80-v2-box-deepseek-observation-first-pass.json`; their
  corresponding M70 monitor states are terminal. Each records exactly one
  issued request and zero remaining capacity.
- Post-run offline checks passed on 2026-08-10: focused provider/observed
  build/monitor regressions (30 passed in 47.08s), full Ruff, governance audit
  and `git diff --check`.
- Pending independent G3 review: Liaol must verify the authorization scope,
  report/monitor terminal states, one-request accounting, no-retry stop,
  generated-script failure classification and the limited conclusion.

## Independent review and closure

- Reviewer: Liaol
- Outcome: approved on 2026-08-10. The review confirms the complete
  authorization scope, sequential control-before-box ordering, terminal
  reports/monitors, one-request accounting, no-retry stop and the bounded
  generated-script compatibility classification.
- Closure rationale: M80 establishes that the current endpoint can return on
  both control and minimal box requests, but its box output does not meet the
  execution contract. It closes as a one-case no-retry failure; it does not
  authorize M73, repair, prompt changes, a new provider request or a model
  quality claim.
