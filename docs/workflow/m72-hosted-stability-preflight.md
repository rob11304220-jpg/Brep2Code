# M72 Hosted Stability Preflight and Terminal Disposition

- **Date**: 2026-08-10
- **Workpack**: `WP-M72-001-bounded-deepseek-stability-experiment`
- **Mode**: preflight completed; one authorized request issued and stopped

## Fixed proposed experiment

| Field | Fixed value |
|---|---|
| Destination / provider / model | `https://api.deepseek.com` / DeepSeek / `deepseek-v4-pro` |
| Transport mode | M71-supported non-streaming Chat Completions JSON-object request; no `stream` field and no `max_output_chars` |
| Outbound content | The adapter's generic JSON-object system instruction plus each case's M48 path-free bounded observation transcript. It excludes raw STEP, local paths, filenames, reference scripts, documentation, traces, credentials, environment values, headers, and request-id values. |
| Cases | Development/P2 only: `param_additive_boss_low`, `param_rounded_slot_low`, `param_fillet_low` |
| Per-case bound | One first-pass request, `--max-rounds 0` (no repair), `--max-cases 1`, `--request-budget 1`, sequential execution |
| Total cap | At most 3 issued requests; no cost cap is asserted because the configured provider account pricing is not inspected locally |
| Provider deadline | 300 seconds per request |
| Generated execution | `wsl-bwrap`; no original STEP mount during generated build execution |
| Fresh reports | `data/corpus-runs/m72-param-additive-boss-low.json`, `data/corpus-runs/m72-param-rounded-slot-low.json`, `data/corpus-runs/m72-param-fillet-low.json` |

## Read-only checks

- Manifest: `case-library/manifests/self-authored/parametric-development.json`
  has SHA-256 `DC4C6E8F3302367A3B1082FAD602FE36FF2A59901E59079695DA75724892A593`.
- The selected rows are all `development` / P2 and map to the expected local
  inputs. Input SHA-256 values are:

  | Case | SHA-256 |
  |---|---|
  | `param_additive_boss_low` | `EBED3D6F6CDFED1F2531E8FB9FDD1F7AF9B0E384433A7CB4A8115890E476D6F0` |
  | `param_rounded_slot_low` | `F9FB195C2D805FB0DE57412E89B5348D4F59AECA5F6DB71195244A46992C825D` |
  | `param_fillet_low` | `B34BF66BB0B92F4BEFEF36197D8805D37EDBF0504C1380E000F5F9DD56F68902` |

- Fresh fake-provider controls using the checked-in reference scripts completed
  through `wsl-bwrap` for every selected case. Reports are stored under ignored
  `data/m72-preflight/`; each records sandbox backend `wsl-bwrap`, successful
  script exit, readable output, and passing geometry gates.
- The local configuration loaded without displaying a credential and selected
  `deepseek-v4-pro` at `https://api.deepseek.com`. `bwrap --version` reports
  `0.9.0`.
- Every intended M72 report path was absent before preflight, with no `running`
  or `interrupted` checkpoint. M54/M63/M64/M67/M69 reports and budget remnants
  are ineligible for reuse.
- `observed-development` rejects DeepSeek execution before provider
  construction when `--authorize-hosted` is absent. Its actual bound is
  `max_cases * (1 + max_rounds)`: the chosen `1 * (1 + 0)` permits exactly one
  request per independent report.
- `uv run python -m pytest tests\\test_agent_m3_repair_loop.py
  tests\\test_observed_build_loop.py -q` passed: 21 tests in 51.78s. Ruff and
  `git diff --check` passed.

## Risk disclosure and authorization gate

This preflight does not authorize egress. A run sends the bounded derivative
described above to DeepSeek's endpoint, up to three times. Each request may
wait for its full 300-second provider deadline; an interactive command window
may therefore be insufficient. Each independent report must be launched with
M70's durable monitor and has no retry or resume authority. A timeout,
lifecycle error, report-path violation, or budget violation stops the
experiment; it cannot trigger a new case, retry, deadline change, or M73.

To authorize, Liaol must explicitly approve the destination and outbound
content, provider/model, all three named development cases, the non-streaming
mode, zero repair rounds, 300-second per-request deadline, maximum three
requests, `wsl-bwrap`, and the three fresh report paths above.

## Authorized outcome

Liaol authorized the complete itemized scope on 2026-08-10. The first
independent request, `param_additive_boss_low`, was launched with its fresh
report and an M70 monitor. It reached terminal `interrupted` after its
300-second provider deadline:

- Report: `data/corpus-runs/m72-param-additive-boss-low.json`
- Classification: `provider_request_timeout`
- Accounting: one request issued; no remaining capacity in that report
- Lifecycle evidence: `worker_started` and `http_started` only; no response,
  generated-script execution or first-byte timing
- Elapsed: 300.029 seconds provider wait; 300.853 seconds end-to-end

The workpack's stopping rule therefore applies. The second and third cases
were not started, their reports remain unused, and this report's exhausted
budget cannot be reused. This result is lifecycle evidence only; it does not
identify a network, provider, model, prompt, CAD, or sandbox root cause.
