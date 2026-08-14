# WP-M89-001: Reference-assisted P1 Three-hole-plate Hosted Smoke

- Status: done
- Milestone: M89
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G3

## Goal

Implement, offline-validate, and then—only after separate explicit
authorization—run one fixed P1 `three_hole_plate` observation-to-build smoke.
The first completion must request `repeated boolean-cut tool`; the Harness may
return only the frozen `vertical-cylinder-construction` guidance card before
the second completion produces an OCP build script.

## Entry criteria

- M86 is done and independently approved for the fixed `three_hole_plate` /
  `repeated boolean-cut tool` fake-provider role.
- M87 is terminal and independently reviewed; its evidence is not a budget or
  authorization for M89.
- The new fixed CLI path passes fake-provider, script-contract, secure
  executor, provenance, output, and geometry-gate acceptance.
- A fresh read-only preflight verifies input/manifest/card hashes, provider
  configuration presence, `wsl-bwrap`, unused report/monitor paths,
  two-request accounting, and deadline before authorization is requested.

## Scope

- Fixed development P1 `three_hole_plate` only; role `repeated boolean-cut
  tool`; top-k one; one card; exactly two provider requests; zero repair and
  zero retry.
- Add a command distinct from M85 and M87, keeping their case/role bindings
  permanently fixed.
- Keep the OCP API contract, `wsl-bwrap`, absent-input control, and output,
  bbox, volume, and topology gates unchanged.

## Attribution question and sampling intent

Test whether the already-qualified vertical-cylinder card supports its final
predeclared repeated-cut role under the constrained two-stage path. This is
one fixed development case, not a P1 benchmark. A timeout, tool-call error,
script failure, sandbox/provenance failure, or geometry failure is terminal;
it does not permit replacement, retry, repair, or progression to M90.

## Inputs

- `case-library/self-authored/three_hole_plate/input.step`
- `case-library/manifests/self-authored/p1.json`
- `runtime_resources/experience-cards/index.json`
- `runtime_resources/experience-cards/cards/vertical-cylinder-construction.json`
- `docs/corpus/reference-packs/m84-cylinder-construction-qualification-v1.json`

## Code paths

- `brep2code/cli/__init__.py`
- `tests/test_observed_build_loop.py`
- provider/guidance runner paths from M85/M86/M87 only as required

## Docs to update

- `docs/modules/cli.md`
- `docs/runbooks/llm-provider-config.md`
- `docs/workflow/status.md`
- active handoff and this workpack

## Trace/schema changes

No schema change. Reuse the current two-request durable report, selected role,
card ID/index hash, sandbox/provenance, and output/geometry gate fields.

## Decision-package impact

- `decision_id`: none; bounded development hosted validation.
- Q01/Q02 effect: tests one predeclared repeated-cut role-to-card selection
  followed by script generation; it does not establish general feature
  inference.
- Q03/Q04 effect: gates and terminal-on-failure disposition are unchanged.
- Evidence role: development regression and hosted lifecycle evidence.
- Knowledge disposition: no new card or reusable knowledge is created.

## Compatibility constraints

Default execution remains offline and credential-free. M85 remains fixed to
`cylinder`; M87 remains fixed to `block_with_hole`. No manifest/card mutation,
broad retrieval, external data, prompt comparison, model/endpoint change,
gate relaxation, retry, repair, or report-path reuse is permitted.

## Acceptance

```powershell
uv run python -m pytest -m fast -q
uv run python -m pytest tests/test_observed_build_loop.py -q
uv run python -m pytest
uv run python -m ruff check .
uv run python tools/check_governance.py
git diff --check
```

Hosted acceptance is separate: a fresh terminal report must show exactly two
issued requests and pass the script/API/sandbox, provenance, output, and
geometry gates. Failure closes M89 without another request.

## Evidence reuse / guidance-card disposition

Use only the existing source-linked `vertical-cylinder-construction` card in
its already-admitted `repeated boolean-cut tool` role. No card is authored,
promoted, ranked, or made broadly retrievable.

## Status transition

Record local acceptance and read-only preflight before requesting hosted
authorization. After a hosted terminal result and Liaol's independent G3
review, update `status.md` first, move this workpack to `done/`, and archive
the handoff. If authorization is not granted, retain the workpack with the
completed offline evidence and no provider request.

## Local acceptance and hosted preflight

- Added `reference-assisted-three-hole-plate-smoke`, a command separate from
  M85 and M87 and fixed to `three_hole_plate` / `repeated boolean-cut tool`.
  Its policy is `m89-reference-assisted-three-hole-plate-v1`; it rejects a
  different case or role, requires two requests, and preserves zero repair.
- 2026-08-10 owner checks: the new targeted test passed (`1 passed, 23
  deselected`); fast suite passed (`64 passed, 142 deselected`); full suite
  passed (`206 passed`); and Ruff passed. The standalone
  `tests/test_observed_build_loop.py -q` command exceeded its 60-second
  command window without a terminal result, so it is recorded as non-terminal
  rather than passing evidence; the later terminal full suite covers it.
- The fake-provider M89 command passed with two requests, the fixed role/card,
  and unchanged script/API, output, bbox, volume, and topology gates.
- A local `wsl-bwrap` `--build-without-input` preflight using the fixed
  reference script passed: sandbox/provenance coverage is true, no input
  access was recorded, the input mount was absent, and all output and geometry
  gates passed. The temporary local evidence root is
  `C:\\tmp\\brep2code-m89-preflight`.
- Read-only preflight: P1 `three_hole_plate` input SHA-256 is
  `34ef08fd81be048d1ba09066f21f162931d91a2001701f7ad737fb3722ae4418`;
  the P1 manifest contains exactly one matching case; the frozen guidance
  index SHA-256 is
  `dfa731d597581b3b4d306782c1078c7de5b79672462229baaf5d7248fa230517`;
  and the selected card SHA-256 is
  `55341683e3e7df3e058a845193e34fba20b0650c0db28a31489ad5d343b60d30`.
  Local configuration has exactly one key entry without exposing it and
  selects `deepseek-v4-pro`. Both planned paths are fresh:
  `data/corpus-runs/m89-three-hole-plate-reference-assisted.json` and
  `data/monitor-runs/m89-three-hole-plate-reference-assisted.monitor.json`.

## Hosted authorization required

Before any `prepare`/monitor/`execute` sequence, Liaol must explicitly approve
all of the following: destination `https://api.deepseek.com`; provider/model
DeepSeek `deepseek-v4-pro`; one development P1 `three_hole_plate` case with
the hash above; first-stage outbound bounded path-free observation transcript
and fixed instructions; second-stage outbound transcript plus the compact
`vertical-cylinder-construction` card; no raw STEP, local paths, filenames,
reference scripts, traces, or credentials; role `repeated boolean-cut tool`;
two sequential requests total, zero retry and zero repair; 300 seconds per
provider request; `wsl-bwrap` with no input mount; and the fresh report and
monitor paths above. The two provider waits plus local Harness work can exceed
an interactive command window, so execution must use the durable monitor. A
timeout or failed gate is terminal and consumes its issued-request budget.

## Hosted execution record

- Liaol explicitly authorized the exact recorded M89 scope on 2026-08-10. The
  fresh report was prepared, attached to the durable monitor, and executed
  once under that authorization.
- Terminal report:
  `data/corpus-runs/m89-three-hole-plate-reference-assisted.json`. It is
  `interrupted`, with `requests_used: 2` and `requests_remaining: 0`; no retry,
  repair, replacement case, or further provider request was attempted.
- Terminal diagnostic: `provider_request_timeout`, with last provider-worker
  phase `http_started`. The execute command returned after about 305 seconds.
  This records a request-specific timeout only; it does not attribute cause to
  the model, CAD script, sandbox, geometry, or network.
- Durable monitor:
  `data/monitor-runs/m89-three-hole-plate-reference-assisted.monitor.json`
  observed the terminal report as `interrupted` and requires review before any
  new authorized run.

## Independent review

- Reviewer: Liaol
- Status: approved on 2026-08-10.
- Required scope: verify the report's 2/2 accounting, fixed case/role/card/hash
  boundary, absence of retry/repair/replacement, and the limited timeout claim.
  The reviewer does not grant a new provider budget.

## Closure rationale

Liaol independently approved closure on 2026-08-10 after confirming the fixed
case/role/card/hash boundary, the terminal 2/2 request accounting, no
retry/repair/replacement, and the limited request-timeout interpretation. The
second provider boundary was reached only after the first guidance response
had completed; the terminal timeout occurred before any generated script,
Harness revision, sandbox execution, or geometry result existed. M89 is
therefore a controlled no-retry failure disposition, not evidence about CAD
correctness, reference-card quality, a model-wide issue, or a network root
cause. Any retry requires a new user-selected bounded G3 workpack, offline
diagnosis, a fresh report path, and new itemized authorization.

## Out of scope

Any other P1/P0 case, P2/P3 case, new card, retry/repair, M90+ activation,
M73 activation, or quality/generalization claim.

## Repair hypothesis and evaluation boundary

This is development-only hosted validation, preceded by offline evidence. It
does not test repair. The fixed repeated-cut role, one card, two-request
budget, no-input sandbox execution, and unchanged geometry gates isolate the
claim to one reference-assisted build attempt.
