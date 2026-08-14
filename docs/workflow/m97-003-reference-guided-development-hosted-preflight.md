# M97-003 Reference-Guided Development Hosted Preflight

- **Date**: 2026-08-10
- **Workpack**: `WP-M97-003-reference-guided-parameter-variation-refrozen-development-calibration`
- **Mode**: read-only local preflight complete; hosted execution is not authorized.

## Fixed proposed scope

- **Destination/model**: `https://api.deepseek.com`, DeepSeek `deepseek-v4-pro`.
- **Rows**: exactly the three preregistered M94 development rows: low,
  nominal and high. Held-out rows are neither read as case inputs nor eligible
  for execution.
- **Egress**: card condition sends a path-free M97 measured-fact transcript to
  request exactly `single boolean-cut tool`, then the same transcript plus the
  compact locally derived card for script generation. Baseline sends only that
  transcript for script generation. The contexts are 387, 388 and 388 UTF-8
  bytes and contain only `base_bbox`, `cylindrical_cut.radius`, `axis`,
  `center_xy` and `extent`; raw STEP, paths, scripts, source hashes, provider
  payloads, credentials and previous reports are excluded.
- **Bound**: nine maximum sequential issued requests (two card plus one
  baseline per row), zero repair, zero retry, 120 seconds per request, and
  no-input `wsl-bwrap` execution.
- **Fresh paths**: report
  `data/corpus-runs/m97-003-reference-guided-through-hole-development-calibration.json`
  and monitor state
  `data/monitor-runs/m97-003-reference-guided-through-hole-development-calibration.monitor.json`.
  Both were absent at preflight.

## Read-only evidence

- New policy [`reference-guided-through-hole-variation-v1-m97-003-policy.json`](../corpus/sequence-paired/reference-guided-through-hole-variation-v1-m97-003-policy.json)
  is `frozen_before_authorization` and pins M96 policy, prompt, guidance,
  context/API recipe, model/endpoint, budget, deadline, gates and fresh paths.
- Current low/nominal/high input SHA-256 values matched policy. Actual M97
  context derivation/validation passed for all rows; source-leak and held-out
  derivation controls fail closed, and low-row values remain radius 2,
  centre [9,10], extent through.
- Local M97 no-input `wsl-bwrap` control passed (1 test, 24.53 s). Focused new
  policy plus fake-accounting tests passed (2 tests, 25.92 s).
- Non-secret configuration verification selected `deepseek`,
  `deepseek-v4-pro`, and `https://api.deepseek.com`; WSL reports Ubuntu-24.04
  / WSL 2. No credential or environment snapshot was displayed.
- The interactive outer window may be shorter than the 18-minute worst-case
  provider budget. A durable monitor must attach after `prepare` and before
  `execute`; no checkpoint is created until authorization exists.

## Authorization required

This passing preflight does not authorize a request. Authorization must approve
the destination and derived egress, provider/model, three development rows,
nine-request maximum, 120-second deadline, zero retry/repair, no-input
`wsl-bwrap`, and one fresh `prepare` → monitor → `execute` lifecycle. It may
not authorize M97-001 reuse, held-out evaluation, M98 or another run.

## Authorization and terminal disposition

Liaol explicitly authorized the complete scope above on 2026-08-10. One fresh
checkpoint was prepared, observed by the durable monitor and executed. The
terminal report is `completed` with 9/9 requests issued: card conditions 3/3
pass and baseline conditions 2/3 pass. No retry, repair, capacity reuse,
held-out row or additional provider request is authorized; independent G3
review remains required.
