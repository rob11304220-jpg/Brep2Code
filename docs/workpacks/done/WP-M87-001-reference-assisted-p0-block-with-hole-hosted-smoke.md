# WP-M87-001: Reference-assisted P0 Block-with-hole Hosted Smoke

- Status: done
- Milestone: M87
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G3

## Goal

Implement, offline-validate, and then—only after separate explicit
authorization—run one fixed P0 `block_with_hole` observation-to-build smoke.
The model must first request `single boolean-cut tool`; the Harness may return
only the frozen `vertical-cylinder-construction` guidance card before the
second request produces an OCP build script.

## Entry criteria

- M86 is done and independently approved.
- The new fixed CLI path passes deterministic fake-provider, script-contract,
  secure-executor, provenance, output, and geometry-gate acceptance.
- A fresh preflight verifies the case/input hash, card/index hashes, local
  provider configuration presence, `wsl-bwrap`, unused report/monitor paths,
  two-request accounting, and deadline.
- Liaol separately authorizes the destination, egress content, provider/model,
  one case, selected role/card, exactly two requests, zero retry/repair,
  deadline, executor, and fresh report/monitor paths.

## Scope

- Fixed development P0 `block_with_hole` only; role `single boolean-cut tool`;
  top-k one; one card; two provider requests; zero repair and zero retry.
- Add a command distinct from M85 so M85 remains permanently restricted to
  `cylinder` / `final primitive`.
- Keep the existing OCP API contract, `wsl-bwrap`, absent-input control, and
  output/bbox/volume/topology gates unchanged.

## Attribution question and sampling intent

Test whether the already-qualified cylinder-construction card supports its
one distinct single-boolean-cut role under the same constrained two-stage
path. Stop after this one development P0 case; a failure is terminal and does
not authorize retry, a replacement case, `three_hole_plate`, or M73.

## Inputs

- `case-library/self-authored/block_with_hole/input.step`
- `runtime_resources/experience-cards/index.json`
- `runtime_resources/experience-cards/cards/vertical-cylinder-construction.json`
- `docs/corpus/reference-packs/m84-cylinder-construction-qualification-v1.json`

## Code paths

- `brep2code/cli/__init__.py`
- `tests/test_observed_build_loop.py`
- provider/guidance runner paths from M85/M86 as required

## Docs to update

- `docs/modules/cli.md`
- `docs/runbooks/llm-provider-config.md`
- `docs/workflow/status.md`
- active handoff and this workpack

## Trace/schema changes

No new schema. Reuse the existing two-request report and additive guidance
metadata, including selected role, card ID and index hash.

## Decision-package impact

- `decision_id`: none; bounded development hosted validation.
- Q01/Q02 effect: test one declared role-to-card selection followed by script
  generation; it does not establish general feature inference.
- Q03/Q04 effect: unchanged gates and terminal-on-failure rule.
- Evidence role: development regression plus hosted lifecycle evidence.
- Knowledge disposition: no new card or reusable knowledge is created.

## Compatibility constraints

M85 remains `cylinder` only. Default execution stays offline and credential
free. No manifest/card mutation, broader retrieval, external data, held-out
case, prompt comparison, model/endpoint change, gate relaxation, retry, or
report-path reuse is permitted.

## Acceptance

```powershell
uv run python -m pytest -m fast -q
uv run python -m pytest tests/test_observed_build_loop.py -q
uv run python -m pytest
uv run python -m ruff check .
uv run python tools/check_governance.py
git diff --check
```

Hosted acceptance, only after fresh preflight and explicit authorization,
requires a terminal parseable report and pass for the script/API/sandbox,
provenance, output and geometry gates. A failure closes the workpack without
another request.

## Evidence reuse / guidance-card disposition

Use only the existing source-linked `vertical-cylinder-construction` card and
its declared single-cut role. No new card is authored, promoted, ranked, or
made broadly retrievable.

## Status transition

Record local acceptance and preflight before requesting hosted authorization.
After a hosted terminal result and Liaol's independent G3 review, update
`status.md` first, move this workpack to `done/`, and archive the handoff.

## Local acceptance and hosted preflight

- Added `reference-assisted-block-with-hole-smoke`, a command separate from
  M85 and fixed to `block_with_hole` / `single boolean-cut tool`. Its report
  policy is `m87-reference-assisted-block-with-hole-v1`; it rejects another
  case or role, requires exactly two requests, and preserves zero repair.
- 2026-08-10 owner checks passed: fast suite (64 passed, 141 deselected),
  focused observed-build suite (23 passed), full suite (205 passed), Ruff,
  governance audit, and `git diff --check`.
- The fake-provider M87 command passed with two requests and the unchanged
  script/API, output, bbox, volume, and topology gates. A separate real
  `wsl-bwrap` `--build-without-input` preflight using the fixed local reference
  script passed: sandbox/provenance coverage is true, no input access was
  recorded, and all output and geometry gates passed.
- Read-only preflight: P0 `block_with_hole` input SHA-256 is
  `285fc4dc1775cbc30deb273ef367d19c946cd50b2e65ced371c7f7d9fb84d7ae`;
  the frozen guidance index SHA-256 is
  `dfa731d597581b3b4d306782c1078c7de5b79672462229baaf5d7248fa230517`;
  the selected card SHA-256 is
  `55341683e3e7df3e058a845193e34fba20b0650c0db28a31489ad5d343b60d30`.
  The P0 manifest contains exactly this case. Local configuration has one key
  entry without exposing it and selects `deepseek-v4-pro`. Both planned paths
  are fresh: `data/corpus-runs/m87-block-with-hole-reference-assisted.json`
  and `data/monitor-runs/m87-block-with-hole-reference-assisted.monitor.json`.

## Hosted authorization required

Before the `prepare`/monitor/`execute` sequence, Liaol must explicitly approve
all of the following: destination `https://api.deepseek.com`; provider/model
DeepSeek `deepseek-v4-pro`; one development P0 `block_with_hole` case with the
hash above; first-stage outbound bounded observation transcript and fixed
instructions; second-stage outbound transcript plus the compact
`vertical-cylinder-construction` card; no raw STEP, local paths, filenames,
reference scripts, traces, or credentials; role `single boolean-cut tool`;
two requests total, zero retry and zero repair; 300 seconds per provider
request; `wsl-bwrap` with no input mount; and the fresh report and monitor
paths above. The two provider waits plus local harness work can outlast a
short interactive window, so execution must use the durable monitor. A
timeout or failed gate is terminal and consumes its issued-request budget.

## Hosted execution record

- Liaol explicitly authorized the exact scope in this workpack on 2026-08-10.
  The fresh report was prepared, attached to the durable monitor, and executed
  once under that authorization.
- Terminal report: `data/corpus-runs/m87-block-with-hole-reference-assisted.json`.
  It is `completed`, used exactly 2/2 provider requests, and returned only
  `vertical-cylinder-construction` for `single boolean-cut tool`.
- Result: `pass`. The generated script passed the OCP API contract and all
  seven execution/output/geometry gates under `wsl-bwrap`; the input mount was
  absent, provenance classified the output as `independent_reconstruction`,
  and no input accesses were recorded. Provider wait was 179,913 ms and total
  elapsed time was 194,453 ms.
- The durable monitor reached terminal `completed`. No retry, repair, extra
  case, or broader card access was attempted.

## Independent review

- Reviewer: Liaol
- Outcome: approved on 2026-08-10.
- Review scope: verify the report's 2/2 accounting, fixed role/card/hash
  boundary, absence of input mount/access, unrelaxed seven gate results, and
  that closure does not imply generalization, another hosted budget, or M73.

## Closure rationale

Liaol independently approved the fixed M87 hosted evidence: the authorized
two-request development P0 run returned only the frozen card, passed the
unchanged secure-execution and geometry gates, and retained no input access.
This closes one single-boolean-cut smoke only. It does not authorize another
case, retry, card promotion, broad retrieval, a quality claim, or M73.

## Out of scope

`three_hole_plate`, P1, any additional P0 case, retry/repair, M73 activation,
or any quality/generalization claim.
