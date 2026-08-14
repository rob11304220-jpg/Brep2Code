# WP-ARCH-001: Development-Split Hosted Timeout Evidence

- Status: archived
- Owner: Codex
- Reviewer: Liaol
- Risk tier: G3

## Goal

Preserve the terminal timeout evidence from a formerly planned fixed
development-split evaluation. This archive is non-runnable; any future
development evaluation must be newly selected, newly numbered and follow the
current four-track route.
generation and at most one repair round per case through `wsl-bwrap`.

## Scope

- Freeze the candidate scope to all 12 rows in
  `case-library/manifests/self-authored/parametric-development.json`.
- Complete read-only hosted preflight: manifest membership, SHA-256 inputs,
  offline secure-executor evidence, non-secret provider configuration,
  M48-only egress path, CLI budget rule, report path, deadline and outer-run
  risk.
- If and only if preflight passes and the user later authorizes every bound,
  run first-pass generation and no more than one repair per case, reporting the
  two funnels separately.

## Attribution question and sampling intent

The fixed 12-row development split spans additive boss, through hole, rounded
slot, and fillet parametric families. It measures whether the frozen M48
observation-to-build contract reaches each existing geometry/provenance gate;
it does not select cases adaptively or establish held-out generalization.
Stop before authorization if any input, split, sandbox, transcript, or budget
preflight check fails.

## Inputs

- `case-library/manifests/self-authored/parametric-development.json` (12 fixed
  self-authored development rows).
- DeepSeek endpoint `https://api.deepseek.com`, model `deepseek-v4-pro` if
  later explicitly authorized.
- Outbound data must be only the frozen M48 bounded observation transcript;
  raw STEP, host paths, file names, reference scripts, native history, docs,
  and trace paths are forbidden.

## Code paths

- `brep2code/cli/__init__.py`
- `brep2code/agent/observed_build.py`
- `brep2code/corpus/runner.py`
- `brep2code/cad/executor.py`

## Docs to update

- `docs/workflow/status.md`
- this workpack and its active handoff
- `docs/runbooks/llm-provider-config.md` only if a verified command contract
  changes; no contract change is authorized by this workpack alone.

## Trace/schema changes

None planned. Existing provider lifecycle, execution, geometry-gate and
provenance fields must remain separate. Any multi-case M48 adapter or report
schema change requires a separately selected G2 workpack.

## Decision-package impact

- `decision_id`: `q01-q02-observation-build-separation-v1`.
- Q01/Q02 effect: tests the frozen observation-only generation boundary on a
  fixed development split, not a new observation or grammar hypothesis.
- Q03/Q04 effect: preserves existing gates and separately reports first-pass
  and bounded-repair outcomes.
- Evidence role: development-only hosted evaluation with negative no-input
  boundary evidence.
- Knowledge disposition: no reusable modeling knowledge unless a later review
  accepts a bounded evidence package.

## Compatibility constraints

Default operation remains offline and credential-free. No manifest, prompt,
provider, Harness, sandbox policy, external-data, held-out, or runtime change
is authorized. Existing `corpus --first-pass` uses its older `probe_summary`
policy and cannot be used if it would egress a file name rather than the M48
path-free transcript.

## Acceptance

```powershell
# Read-only preflight evidence must pass before authorization is requested.
uv run python -m pytest -m sandbox -q
uv run python -m pytest
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

If authorized after a passing preflight, the final command must use a new
report path, `--provider deepseek`, `--authorize-hosted`, the fixed manifest,
`--max-cases 12`, `--max-rounds 1`, request budget 24, a 120-second provider
deadline, and `wsl-bwrap`. It must never reuse a checkpoint or request budget.

## Evidence reuse / guidance-card disposition

No reusable evidence before a later independent review; evaluation output is
development-only evidence.

## Status transition

Preflight and authorization are distinct. Record all six hosted-preflight
checks before asking for authorization. Record any blocker rather than sending
data. Closure requires the authorized report or an explicit no-request
disposition, full offline gates, Liaol's independent review, then status,
workpack and handoff alignment.

## Closure rationale

Pending.

## Blocker disposition

M54 was blocked, not closed. M55 and M56 now close with independent review,
and the fresh input/configuration, WSL/bubblewrap, no-input, egress, budget,
and new-report-path checks pass. M54 is awaiting itemized user authorization;
it remains forbidden to use the old corpus first-pass route or issue a
provider request before that authorization.

## Hosted preflight result (no request issued)

- Fixed manifest: `parametric-development.json`, SHA-256
  `DC4C6E8F3302367A3B1082FAD602FE36FF2A59901E59079695DA75724892A593`.
  Its 12 exact input hashes are recorded in
  `docs/workflow/m54-hosted-preflight.md`.
- Local non-secret DeepSeek configuration entries for API key, model, and base
  URL are present; WSL exposes `/usr/bin/bwrap` and `/usr/bin/python3`.
- The local reference replay preflight completed under `wsl-bwrap`:
  `data/m54-preflight/reference-repair-wsl-bwrap.json` reports 12/12 repair
  passes and 12/12 reconstruction-eligible no-input controls. This verifies
  the local executor boundary only; it is not provider evidence.
- The intended hosted report path
  `data/corpus-runs/m54-parametric-development-deepseek-observation.json` is
  absent, so no checkpoint or budget would be reused.
- **Stop condition met:** equivalent fake `corpus --first-pass` preflight
  fails because all 12 rows lack `first_pass_script`; more importantly, the
  hosted multi-case `corpus --first-pass` route retains the older
  filename-bearing `probe_summary` policy. It cannot satisfy the M48
  path-free observation-only egress contract.
- Result: no authorization request is permitted and no provider request was
  issued. A separately selected G2 multi-case observation-only adapter is
  required before resuming this workpack.

## Fresh hosted preflight after M57 (no request issued)

- Destination if later authorized: `https://api.deepseek.com`, provider
  `deepseek`, model `deepseek-v4-pro`. Outbound content is restricted to the
  M48 path-free bounded observation transcript; raw STEP, paths, filenames,
  reference scripts, native history, docs, and trace paths remain forbidden.
- Fixed scope remains all 12 rows of `parametric-development.json`; the
  manifest SHA-256 is
  `DC4C6E8F3302367A3B1082FAD602FE36FF2A59901E59079695DA75724892A593` and
  all 12 input hashes match the recorded preflight values.
- The local non-secret provider configuration parses as DeepSeek
  `deepseek-v4-pro` at `https://api.deepseek.com` with a 120-second default
  deadline. No credential value was displayed.
- `wsl.exe` confirms executable `/usr/bin/bwrap` and `/usr/bin/python3`.
  The retained 12-case reference-repair preflight artifact is completed, and
  the current offline observed-development regression passed 9/9.
- The actual CLI bound for 12 cases and one repair round is
  `12 × (1 + 1) = 24` requests. The proposed fresh report path is
  `data/corpus-runs/m54-parametric-development-deepseek-observation-rerun-20260808.json`;
  it does not exist. The old path and its budget remain disallowed even though
  its terminal report is absent.
- Maximum provider wait is 24 × 120 seconds (48 minutes), excluding local
  execution. Any authorized batch must use durable monitoring rather than an
  interactive command deadline.
- Result: fresh preflight passes. It does not authorize a request; a new
  explicit authorization must cover the destination and egress, model, fixed
  12-case scope, one first pass plus at most one repair, 120-second deadline,
  24-request cap, and the new report path.

## Authorization

On 2026-08-08, Liaol explicitly authorized one new M54 batch to
`https://api.deepseek.com` using `deepseek-v4-pro`: the fixed 12-row
`parametric-development.json` split; only M48 path-free observation transcripts
as egress; one first pass and at most one repair per case; at most 24 requests;
120-second provider deadline; `wsl-bwrap` no-input execution; and new report
path `data/corpus-runs/m54-parametric-development-deepseek-observation.json`.
This authorization does not cover any other case, model, endpoint, path,
budget, retry, held-out run, or external data.

## Authorized run result

The first authorized request was issued on 2026-08-08 and exceeded its
120-second provider deadline. The worker was terminated. No retry was issued
and no remaining budget may be reused. The observed-development runner then
raised the timeout instead of writing its required `interrupted` checkpoint,
so the planned report path contains no usable terminal batch report. M54 stops
pending a separately selected offline G2 checkpoint/timeout recovery workpack
and, afterward, a new report path plus fresh itemized authorization.

## Fresh authorized run result

- Liaol authorized the fresh batch described in the preceding fresh preflight.
- The first request, for `param_additive_boss_low`, exceeded the authorized
  120-second provider deadline. The worker was terminated.
- The new report path
  `data/corpus-runs/m54-parametric-development-deepseek-observation-rerun-20260808.json`
  atomically records `run_status: interrupted`, `requests_used: 1`,
  `requests_remaining: 23`, and `ProviderRequestTimeoutError`.
- No case completed, no retry was issued, and no later case was started.
  This is provider-lifecycle evidence only, not a geometry or model-quality
  result. The remaining 23-request capacity is invalid for reuse.
- M54 returns to blocked. Any later run requires a new report path, fresh
  preflight, and new itemized hosted authorization.

## Out of scope

Provider calls before itemized authorization; held-out evaluation; external
inputs; adaptive case selection; raw input/reference-script egress; prompt or
manifest changes; and treating a development result as a generalization claim.

## Repair hypothesis and evaluation boundary

Development-only hosted evaluation. Repair is limited to one response after a
failed first pass and must retain the original gate evidence. The claimed
outcome is only the separately denominated first-pass and repair funnel on the
frozen development rows; it cannot establish held-out performance.
