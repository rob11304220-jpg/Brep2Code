# Brep2Code v2

中文说明：[README.zh-CN.md](README.zh-CN.md)

Brep2Code turns a STEP/B-Rep case into an executable CAD build script and a
validated output model. The Active Harness is the primary research protocol.
The fixed runner remains an explicit legacy control for ablation and historical
comparison; Active failures never fall back to it.

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
uv run brep2code env doctor
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

The shared mechanism registry is cases/registry/mechanisms.json for the legacy
L0-L2 evaluation cohort. Those labels are optional research metadata, not a
runtime script contract. An open-ended task may omit mechanism, capability, and
sequence fields and provide a case-local `verifier.json` containing only its
target references, gates, repair policy, and reference projection policy.
The verifier pack keeps acceptance independent from the modeling sequence, so
multiple valid construction strategies can pass the same task.

`capability_level` remains useful for offline reports and campaign grouping. The
legacy T0/T1/T2 values are retained only as an explicit `compatibility_tier`
mapping.

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

Use `--retrieval-policy disabled --max-retrievals 0` for the strict
no-knowledge baseline. This selects a separate prompt, removes retrieval tools
from the action space, rejects retrieve actions as a Harness-policy failure, and
records a schema-v5 policy identity. Use `bounded_seed` only as an explicit
knowledge condition.

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

Hosted active checkpoints use schema version 5 to keep retrieval policy
identity, HTTP attempts, prompt/completion/total tokens, cost, prices, and
provider ceilings separate from controller usage. Continuation restores that
accounting and retains an interrupted request attempt as consumed. The
checkpoint contract alone does not add a hosted execution command.

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

The secure backend defaults to the `Ubuntu-24.04` distro and
`/opt/brep2code/runtime`. Override these portable host settings with
`BREP2CODE_WSL_DISTRO` and `BREP2CODE_RUNTIME_ROOT`; no host username is
compiled into the project. `brep2code env doctor` checks the configured backend
without network requests or artifacts. If the user-level uv cache has broken
ACLs, set a temporary `UV_CACHE_DIR` for diagnosis and repair its ACL separately
rather than weakening the secure executor.

For a per-shell override on an existing machine:

```powershell
$env:BREP2CODE_WSL_DISTRO = "Ubuntu-24.04"
$env:BREP2CODE_RUNTIME_ROOT = "/home/<wsl-user>/.brep2code-runtime"
uv run brep2code env doctor
```

These host variables come from the process environment, not the provider `.env`
file. Set them persistently through the operating system when appropriate.

The command writes immutable revision directories and an atomically updated
`result.json`. Provider-generated scripts execute through the required
`Ubuntu-24.04` WSL2/bubblewrap backend. That backend uses the dedicated
configured secure-runtime Python environment, clears ambient variables,
disables networking, exposes only `build.py` plus one writable `output.step`,
and bounds time, memory, processes, logs, and output size. The local executor
remains available only for trusted developer-authored scripts.

## Research progression

The implementation has completed a narrowly bounded hosted pilot and is in
post-pilot diagnostic refinement. That implementation milestone is not a
completed research baseline: the evidence program remains at Stage 1, measuring
the real provider's low-difficulty baseline without a knowledge base. Stage 2
then uses hosted Active reruns of the same cases to replicate that baseline and
validate the hosted transport and accounting path. These runs require
secure-backend readiness, explicit budgets, and fresh authorization.

The planned order is:

1. low-difficulty no-knowledge baseline;
2. hosted Active reruns of existing cases;
3. a small local SDK/recipe knowledge-base prototype;
4. mature modeling-dataset import, indexing, and semantic retrieval.

These are mandatory research stages, not a loose feature list. Stage 1 freezes
the Active no-knowledge baseline and a small diagnostic case family. Stage 2
measures the same cases through the real hosted Active path without changing the
knowledge condition. Stage 3 introduces versioned SDK and general recipe
projections through explicit ablations. Stage 4 studies mature datasets only
after provenance, normalization, duplication, leakage, and non-unique sequence
policies are in place. Detailed entry/exit criteria and the scored alternatives
A--E are authoritative in `docs/development.md` under **Research stages and
candidate routes**. A later agent must update those criteria when changing the
research order rather than silently starting a later route.

Do not enter stages 3 or 4 before stage 1 has produced interpretable results.
Stage 3 must first freeze the record format, safe projection boundary,
retrieval metrics, and ablation design. Stage 4 additionally requires
provenance, version normalization, near-duplicate control, target-solution
leakage checks, and treatment of non-unique modeling sequences.

Permanent design and workflow details live in `docs/architecture.md`,
`docs/development.md`, and `docs/providers.md`.

Active Harness development remains fake-first: extend actions or tools only
with deterministic action-sequence tests and secure verifier artifacts. The
`retrieve` action supports both the legacy exact OCP topic and a bounded
general SDK/recipe query. Its projection is answer-free and excludes target
solutions, repository files, private oracles, host paths, and secrets. The
single-case live path remains authorization-gated; any broader hosted execution
scope stays closed until its secure-backend readiness and exact authorization
boundary have focused tests. Readiness checks do not grant execution permission.
Do not use workpacks, status logs, or evidence ledgers to preserve this route;
schemas, tests, case metadata, and the permanent design rules are the
authorities.

DeepSeek has no implicit or credential-triggered path. Its explicit bounded
CLI and fresh authorization requirements are documented in `docs/providers.md`.
