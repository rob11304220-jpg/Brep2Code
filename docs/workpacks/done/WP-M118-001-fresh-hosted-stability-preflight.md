# WP-M118-001: Fresh Hosted-Stability Preflight

- Status: done
- Milestone: M118
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G3

## Goal

Freeze and complete offline preflight for one fresh, stability-only,
development-only two-request experiment. It tests lifecycle and API-admissible
end-to-end completion under one fixed bounded-output reference-assisted mode;
it is not an M115 calibration and creates no provider request before a later
itemized authorization.

## Frozen proposed boundary

- Destination/model: `https://api.deepseek.com`, DeepSeek `deepseek-v4-pro`.
- Development scope: only existing `three_hole_plate` in the checked-in P1
  development manifest; no held-out input.
- Egress: first a path-free bounded observation transcript plus fixed
  instructions; then that transcript plus the fixed
  `vertical-cylinder-construction` card. No raw STEP, local path, filename,
  reference script, prior report, response, header, trace or credential.
- Execution: two sequential requests, zero repair/retry, `wsl-bwrap` with no
  input mount, a 4096 maximum-output-token cap and 300-second deadline per
  request. Any timeout, lifecycle failure, static API rejection, sandbox
  failure or gate failure is terminal and does not advance to calibration.
- Fresh accounting: M118 policy namespace and fresh report/monitor paths;
  M69/M72/M80/M89/M97 paths, budgets, reports, monitors and authorizations are
  terminal and cannot be reused.

## Scope

- Add only the fresh M118 policy/checkpoint identity necessary to enforce the
  frozen boundary with fake-provider tests.
- Verify development manifest/hash, card/index hashes, no-input `wsl-bwrap`
  reference replay, non-secret provider configuration/model availability,
  actual two-request accounting, deadline/cap validation and fresh report/
  monitor paths.
- Write the read-only preflight record. It must state the required itemized
  authorization but must not prepare, monitor, execute or construct a provider.

## Compatibility constraints

Default operation remains offline and credential-free. Do not send data,
construct a provider, read/display credentials, run `prepare`/monitor/execute,
modify existing historical policy/report/monitor/budget/authorization, alter
cards/prompts/cases/splits/manifests/sandbox/gates, access held-out inputs,
reuse M97, start calibration, or infer provider/model/card quality.

## Acceptance

```powershell
uv run python -m pytest -m fast -q
uv run python -m pytest tests\test_agent_m3_provider_trace.py tests\test_observed_build_loop.py -q
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

The preflight must additionally record passing manifest/hash/no-input/config/
executor/accounting/deadline/fresh-path checks. If any fails, do not request
authorization.

## Status transition

Record owner preflight evidence, then obtain Liaol's independent G3 review.
Only then request explicit user authorization that confirms every proposed
hosted-boundary item. After a terminal authorized run, record accounting and
obtain another independent review before closure.

## Owner preflight evidence (2026-08-11)

- Added the M118-only CLI/checkpoint identity
  `reference-assisted-three-hole-plate-stability-smoke` and frozen policy
  [`m118-three-hole-plate-stability-policy-v1.json`](../../corpus/registry/m118-three-hole-plate-stability-policy-v1.json).
  It requires exactly two requests, zero repair, 4096 output tokens and the
  M118 policy namespace; M89 accounting cannot satisfy it.
- The read-only preflight record is
  [`m118-fresh-hosted-stability-preflight.md`](../../workflow/m118-fresh-hosted-stability-preflight.md).
  Input/manifest and guidance hashes match the frozen policy; non-secret
  configuration booleans, fresh report/monitor paths, fake two-request
  checkpoint and no-input WSL replay passed. The WSL replay retained a local
  `.wslconfig` warning while sandbox/provenance and all gates passed.
- Acceptance passed: M118 plus provider-trace focused tests (11 passed), fast
  suite (66 passed), standalone observed-build suite (36 passed in 137.74
  seconds), Ruff, governance audit and `git diff --check`.
- No actual provider object, real checkpoint, monitor, authorization or hosted
  request was created. Liaol's independent G3 review is required before asking
  for itemized hosted authorization.

## Independent G3 review (2026-08-11)

Liaol independently approved the offline M118 scope and preflight. The review
confirmed fresh policy/accounting isolation, the exact development-only input
and guidance hashes, fake two-request accounting, no-input WSL evidence,
non-secret configuration check, fresh paths, acceptance output and the retained
WSL warning. This approval grants no provider construction, checkpoint,
monitor, request, retry, repair, calibration or held-out authority. The package
now awaits the user's itemized hosted authorization.

## Itemized hosted authorization (2026-08-11)

Liaol explicitly authorized the complete M118 boundary: the DeepSeek endpoint
and `deepseek-v4-pro`; the declared path-free first and card-augmented second
egress; only the fixed development `three_hole_plate` row; exactly two
sequential requests; zero retry and repair; 4096 output tokens; 300 seconds
per request; no-input `wsl-bwrap`; and the two fresh M118 report/monitor
paths. This authorization grants no alternative model, endpoint, case, card,
prompt, path, additional budget, calibration or held-out authority.

## Authorized execution and owner terminal record (2026-08-11)

- The fresh report was prepared, observed by its fresh durable monitor, and
  executed once under the authorized M118 boundary. The monitor observed the
  terminal report; it was then torn down without changing the report.
- The terminal checkpoint at
  `data/corpus-runs/m118-three-hole-plate-stability.json` records policy
  `m118-three-hole-plate-stability-v1`, `completed`, `requests_used: 2` and
  `requests_remaining: 0`. The report-level accounting is authoritative; no
  further request capacity exists.
- The result is `provider_error` with `missing_script_update`. No executable
  replacement script was available for static API classification, sandbox
  execution, provenance or geometry gates; those stages are not evaluated.
  This fails M118's stability gate and is a terminal no-retry/no-repair stop.
- Sanitized timing retained in the report: first response byte at 63,581 ms,
  completion at 104,405 ms, provider wait 101,074 ms and end-to-end 104,405
  ms. These describe only this bounded run and do not identify provider,
  network, model or card cause.
- Post-run focused policy/provider-trace tests passed (11), as did Ruff and
  `git diff --check`. Liaol's independent terminal G3 review is required
  before closure.

## Independent terminal G3 review and closure (2026-08-11)

Liaol independently approved closure. The review confirmed the exact user
authorization, fresh M118 policy/report/monitor boundary, prepared-to-terminal
lifecycle, authoritative 2/2 accounting, sanitized terminal classification,
monitor handoff, absence of retry/repair and the fact that no executable script
existed for downstream gates. M118 closes as a failed stability gate and grants
no calibration, replacement request, provider/model change, case expansion,
held-out activity or reusable hosted capacity.

## Out of scope

Any provider request before explicit authorization; M115 card-effect
calibration; held-out evaluation; retries, repairs, expanded samples, endpoint
or model changes, token-cap tuning, dependency installation, runtime guidance
promotion or general claims.
