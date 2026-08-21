# Brep2Code v2

中文说明：[README.zh-CN.md](README.zh-CN.md)

Brep2Code turns a STEP/B-Rep task into a complete executable CAD script and
accepts the result only after independent geometry verification. The Active
Harness is the primary research protocol. The Fixed runner is retained only as
an explicit control; an Active failure never falls back to Fixed.

## Active Harness

The model is a bounded action policy inside the Harness, not the owner of the
run. On each turn it selects exactly one action that the controller currently
exposes:

- `probe`: request an allowlisted, path-free geometry observation;
- `retrieve`: request an approved SDK or general recipe projection when the
  experiment enables retrieval;
- `submit`: provide one complete deterministic `build.py`;
- `finish`: state that no further useful action is available.

The Harness owns state, internal limits, tool dispatch, immutable revisions,
checkpoints, and continuation. It exposes capabilities, not numeric budgets:
the provider sees the actions and tools available on the current turn, but not
controller usage, HTTP limits, retries, timeouts, prices, cost, authorization,
campaign policy, or secure-executor configuration.

`finish` is advisory. Only the verifier can mark a run successful after script
compatibility checking, secure execution, and the required geometry gates.

```text
validated B-Rep task
        |
        v
path-free observation -----> model selects one available action
        ^                              |
        |                 probe / retrieve / submit / finish
        |                              |
        +---- typed feedback <--- independent verifier
                                      |
                               verified output.step
```

The provider-visible task contains only the case identity and unit, observations,
currently available actions and tools, a coarse session phase, the selected CAD
backend contract, prior tool results, the current revision, and typed verifier
feedback. It never contains eval references, target solutions, private oracles,
repository files, host paths, environment variables, credentials, or undeclared
network access.

## Install and verify

```powershell
uv sync --dev
uv run brep2code env doctor
uv run brep2code cases validate
uv run pytest -q
uv run pytest --run-secure -q
uv run ruff check src tests
```

The default provider is deterministic and offline. A real provider requires an
explicit command selection and fresh authorization. Generated code executes
only through the configured WSL2/bubblewrap secure backend; the trusted local
executor is not a fallback for provider-generated code.

Inspect the available commands and their current arguments through the CLI:

```powershell
uv run brep2code --help
uv run brep2code active-run --help
uv run brep2code active-hosted-live-run --help
uv run brep2code stage1 report --help
```

Cases live under `cases/<split>/<case_id>`. Runtime loading permits only the
`smoke` and `train` splits. Evaluation cases and their private comparison data
remain Harness-only. Run artifacts are written below the selected run root as
an atomically updated `result.json` plus immutable revision directories.

## Research status

Stage 1, the frozen no-knowledge baseline, is complete. Its evidence developed
through several immutable experiment identities:

| Condition | Valid and interpretable | Geometry passed | Provider/Harness failures |
|---|---:|---:|---:|
| CadQuery, five-case phase | 48/50 | 17/50 | 2/50 |
| CadQuery, three comparable cases | 29/30 | 5/30 | 1/30 |
| OCP, three comparable cases | 27/30 | 18/30 | 3/30 |

The original schema-v6 diagnostic did not meet the Stage 1 exit threshold: OCP's
infrastructure failure rate was exactly 10%, while the frozen contract requires
a rate strictly below 10%. Those results and classifications remain historical
evidence and must not be selectively rerun or reclassified.

The current schema-v7 / provider-task-contract-v2 stabilization separates:

- model decisions, probes, submissions, and verifier-guided repairs;
- provider HTTP attempts, bounded protocol retries, tokens, and cost;
- secure execution time, resource, process, and output limits.

The 12-run stabilization condition then produced valid
artifacts and valid provider-visible projections. Nine passed geometry, two were
classified as generation failures before execution, and one as a geometry
failure. The cohort used 13 HTTP attempts, 14,903 tokens, and $0.007858275 with
no protocol retry. Its `protocol_stable` judgment established the prerequisite
for a replacement Stage 1 cohort; it did not itself change the exit judgment.

The mandatory research order remains:

1. Active no-knowledge baseline and protocol stabilization;
2. matched SDK and general-recipe retrieval ablations;
3. governed ingestion and retrieval of mature modeling datasets.

The former hosted-replication Stage 2 objective was absorbed into Stage 1 when
v3 completed the full hosted transport, accounting, artifact, projection, and
secure-execution path. Stage 2 now begins with knowledge retrieval, and Stage 3
retains the governed dataset work. Neither may begin before the preceding exit
criteria and a new experiment review are satisfied.
Capability labels and mechanism metadata may be used for reports and grouping,
but they are not the runtime script contract or the development roadmap.

`stage1-no-knowledge-v2` aborted after 41 valid terminal attempts when its 42nd
identity left a nonterminal provider-exchange checkpoint. It is historical
diagnostic evidence only and cannot be continued or selectively rerun. Its
replacement, `stage1-no-knowledge-v3`, used the same 50 CadQuery and 30 OCP
identities, schema v7, `active-v4-no-retrieval`, and unchanged thresholds under
execution protocol v3.
The complete run produced 80/80 valid attempts with no infrastructure,
artifact, or projection failure. CadQuery passed 15/50 geometries and OCP
passed 17/30; both phases passed the frozen validity and infrastructure gates,
so the current Stage 1 judgment is `complete: true` and `exit_ready: true`.
`stage2_authorized` remains false. Before any Stage 2 contract is created, the
SDK and recipe retrieval ablations require a separate review of knowledge
sources, leakage controls, matched conditions, scope, limits, and a fresh run
root.

## Project authorities

Code, tests, case metadata, and validated run artifacts are the evidence
authorities. Permanent design and workflow rules live only in:

- [Architecture](docs/architecture.md): control loop, contracts, visibility,
  verification, and artifact invariants;
- [Development](docs/development.md): change discipline, research stages,
  current evidence, and verification workflow;
- [Providers](docs/providers.md): provider configuration, transport,
  accounting, hosted authorization, and continuation rules.

CLI `--help` is the authority for command arguments. Run artifacts, rather than
permanent narrative documents, are the authority for individual executions.
