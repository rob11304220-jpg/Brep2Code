# Brep2Code v2

中文说明：[README.zh-CN.md](README.zh-CN.md)

Brep2Code turns a STEP/B-Rep case into an executable CAD build script and a
validated output model. The fixed runner provides a bounded repair loop: it
assembles one observation context, requests one complete script per revision,
executes it, verifies it, and returns structured feedback for the next
revision.

The implemented active Harness adds a provider-neutral action loop through
`active-run`. A deterministic fake action provider can request bounded edge
probes or approved OCP references before submitting scripts to compatibility,
secure execution, and geometry gates. The same controller and verifier support
a narrowly bounded, fresh-root, single-runtime-case HTTPS path through
`active-hosted-live-run`; hosted continuation remains HTTP-stub-only and broader
hosted cohort expansion is not implemented. The action contract, controller,
verifier boundary, and separate budgets are defined in `docs/architecture.md`;
the implementation order is in `docs/development.md`.

The default provider is offline and no provider request is made by the
commands below.

## Install and verify

```powershell
uv sync --dev
uv run brep2code --help
uv run brep2code cases validate
uv run pytest -q
uv run pytest --run-secure -q
uv run ruff check src tests
```

Without `uv`, create a Python 3.12+ virtual environment and install the project
in editable mode:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -e .
.venv\Scripts\brep2code.exe cases validate
```

Cases are stored under `cases/<split>/<case_id>`. `case.json` and the STEP
SHA-256 are validated together; manifests under `cases/manifests` declare the
complete catalog. Runtime loading permits only the `smoke` and `train` splits.

The shared mechanism registry is cases/registry/mechanisms.json. Each case
also has a Harness-only dossier.json that binds geometry assets, modeling
knowledge, applicable gates, repair policy, and hosted budget without adding
any of those private fields to runtime observations. `capability_level` is the
sole L0-L6 semantic field used by cases, campaigns, and reports. The legacy
T0/T1/T2 values are retained only as an explicit `compatibility_tier` mapping.

The G1 mechanism campaign is validated without contacting a provider:

```powershell
uv run brep2code campaign validate --contract cases/campaigns/g1-mechanism-coverage.json
```

It binds case mechanisms, kernel properties, ordered construction sequences,
difficulty, capability levels, held-out scope, and explicit hosted-run bounds.
The `max_requests`, `max_total_tokens`, and `max_cost_usd` fields are campaign
aggregate ceilings. The corresponding `case_max_*` fields are independent
ceilings applied afresh to each runtime case.

G2 adds a local-only preflight and a serial batch Harness. Preflight does not
construct a provider; a batch run writes one campaign `result.json` plus one
isolated result tree per runtime case:

```powershell
uv run brep2code campaign preflight `
  --contract cases/campaigns/g1-mechanism-coverage.json `
  --run-root runs/g1-preflight
```

The batch `run` command is provider-explicit. Fake runs require exactly the
contract's six script slots; hosted runs require fresh authorization and the
declared provider limits. Each case gets its own result tree and accounting;
the campaign result only aggregates those independent case runs and does not
reuse a script or repair state from another case.

An offline repair smoke accepts one full script per bounded revision:

```powershell
uv run brep2code run --case-id box --run-root runs/box-smoke `
  --fake-script tests/fixtures/broken_box.py `
  --fake-script tests/fixtures/fixed_box.py --max-rounds 2
```

Inspect the offline active command and its explicit action and budget inputs:

```powershell
uv run brep2code active-preflight --help
uv run brep2code active-run --help
uv run brep2code active-continue --help
uv run brep2code active-validate --help
uv run brep2code active-hosted-preflight --help
uv run brep2code active-hosted-config-check --help
uv run brep2code active-hosted-readiness --help
uv run brep2code active-hosted-run --help
uv run brep2code active-hosted-live-run --help
uv run brep2code active-hosted-continue --help
uv run brep2code active-pilot-report --help
```

Each `--fake-action` file contains one JSON action envelope. The number of
files must equal `--max-model-requests`; probe, retrieval, submission,
execution, repair, token, and cost ceilings are declared independently. This
command remains offline at the provider boundary, although submitted scripts
still require the secure execution backend. Preflight validates the case,
action envelopes, independent ceilings, timeout, and fresh run root without
constructing a provider or creating artifacts. Saved-result validation
cross-checks terminal state, trace accounting, budget usage, sequential
revision artifacts, relative output names, and forbidden private fields.
Active sessions atomically checkpoint before provider and tool work and at
submission, repair, and terminal boundaries. An interrupted checkpoint remains
valid for audit with `terminal: false`; its continuation policy records the
requirements for bounded continuation. `active-continue` is fake-only and
accepts only a validated eligible checkpoint with the same case, provider/model,
total budgets, timeout, and revision root. It consumes only the remaining model
request slots and conservatively charges an interrupted execution before
continuing at the next action.

After a failed submission, an exactly unchanged repair is persisted as a typed
`unchanged_revision` failure and rejected before compatibility checking or secure
execution. It consumes the declared submission/repair capacity but preserves the
execution budget; a later bounded turn may change the script or retrieve an
allowlisted OCP reference before resubmitting.

The bounded `edge_candidates` probe reports unique session-local edge IDs,
geometry keys, curve parameters and parameter ranges, local tangents,
face-edge incidence, parallel and collinear groups, and local dihedral classes.
Analytic OCP inspection references remain available only through the explicit
`ocp_symbol` allowlist; they are not embedded into the system prompt.

The active hosted preflight, config-check, and unified readiness commands are
network-free checks. Unified readiness checks the fake baseline, saved
artifacts, initial or continuation root, bound budgets, fresh itemized
authorization, secure backend, and optional provider configuration. Preflight
validates the declared outbound projection, itemized fresh authorization,
controller and provider budget layers, and initial or continuation scope
without reading credentials. Config-check additionally reads local provider
configuration and reports only the endpoint host and bounded plan; it makes no
network request and creates no artifact. Neither command authorizes or exposes
hosted active execution.

Hosted active checkpoints use schema version 4 to keep HTTP attempts,
prompt/completion/total tokens, cost, prices, and provider ceilings separate
from controller usage. Continuation restores that accounting and retains an
interrupted request attempt as consumed. The checkpoint contract alone does not
add a hosted execution command.

`active-hosted-run` is currently an HTTP-stub-only vertical slice. It requires
unified readiness, a successful fake baseline, fresh itemized authorization, a
fresh run root, disabled thinking, provider/controller limits, and an explicit
local `--http-stub-response`. It exercises secure submission and saved-result
validation without making a hosted network request.

`active-hosted-live-run` is the separate real HTTPS slice for one fresh runtime
case and the explicitly selected DeepSeek model. It repeats unified readiness
with provider configuration enabled, requires every itemized authorization and
both budget layers, performs no provider fallback, bounds response bytes, and
records credential-free request/response artifacts under `provider-exchanges/`.
Invoking it is a new network action and therefore requires fresh authorization
for the exact case, model, limits, outbound projection, and run root.

`active-hosted-continue` is likewise HTTP-stub-only. Every continuation must
repeat all itemized authorization flags, preserve case/model/budgets/timeout,
prices, ceilings, and revision root, and restore both controller and provider
accounting. Interrupted HTTP and execution attempts remain conservatively
charged, and only the remaining model turns are available.

`active-pilot-report` aggregates five validated fake active results in the
fixed order `nominal`, `parameter_variation`, `failure_sensitive`, `controls`,
and `held_out`. It records action sequences, tool/submission/repair usage,
per-budget remaining capacity, terminal classifications, and a fixed-loop vs
active-loop comparison. A passing decision gate only makes the run eligible to
request one fresh hosted pilot authorization; it never grants authorization or
makes a network request.

The command writes immutable revision directories and an atomically updated
`result.json`. Provider-generated scripts execute through the required
`Ubuntu-24.04` WSL2/bubblewrap backend. That backend uses the dedicated
`/home/liaol/.brep2code-runtime` Python environment, clears ambient variables,
disables networking, exposes only `build.py` plus one writable `output.step`,
and bounds time, memory, processes, logs, and output size. The local executor
remains available only for trusted developer-authored scripts.

Permanent design and workflow details live in `docs/architecture.md`,
`docs/development.md`, and `docs/providers.md`.

Active Harness development remains fake-first: extend actions or tools only
with deterministic action-sequence tests and secure verifier artifacts. The
single-case live path remains authorization-gated; any broader hosted execution
scope stays closed until its secure-backend readiness and exact authorization
boundary have focused tests. Readiness checks do not grant execution permission.
Do not use workpacks, status logs, or evidence ledgers to preserve this route;
schemas, tests, case metadata, and the permanent design rules are the
authorities.

DeepSeek has no implicit or credential-triggered path. Its explicit bounded
CLI and fresh authorization requirements are documented in `docs/providers.md`.
