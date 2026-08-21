# Development

Build the smallest tested vertical slice from B-Rep input to executable CAD
script and validated output. Code, tests, case metadata, and validated run
artifacts are the project authorities. Run artifacts belong under `runs/` and
are not permanent documentation.

## Change discipline

Start from an observable problem and acceptance condition. Keep one slice to one
behavior change, its focused tests, and only the directly required schema, case
metadata, or documentation. Run Ruff and the relevant tests before treating the
slice as complete. Commit only when requested; when staged commits are requested,
commit each verified slice before beginning the next one.

Do not mix case expansion with unrelated CLI work, provider transport with
controller behavior, or a research-condition change with selective reruns of an
existing cohort. Preserve pre-existing worktree changes and keep them out of the
slice.

Changes to provider egress, credentials, model-visible projection, untrusted
execution, verifier authority, continuation, or accounting require focused
boundary tests. An architectural decision record is warranted only for a
costly-to-reverse cross-module decision.

Permanent documentation is limited to README and the three files under `docs/`.
Do not add workpacks, handoffs, route maps, progress logs, status ledgers, or
evidence ledgers. CLI syntax belongs to `--help`; individual execution facts
belong to validated artifacts.

## Active Harness development rules

Active is the primary protocol. Fixed is an optional control and never a
fallback or readiness dependency.

The controller, provider, submission pipeline, and verifier have separate
responsibilities. Preserve these invariants:

- the model selects one currently available action per decision;
- internal limits are projected as available actions and tools, never as
  numeric budgets or remaining capacity;
- provider HTTP attempts and protocol retries are separate from model
  decisions, submissions, executions, and repairs;
- compatibility rejection happens before secure execution and does not consume
  an execution attempt;
- every submission is a complete script in a new immutable revision;
- only the verifier can enter `SUCCEEDED`;
- hosted authorization and secrets never enter model context or saved results;
- provider-generated code never falls back to the trusted local executor.

Extend actions or tools fake-first. Add deterministic action-sequence tests,
projection tests, saved-result validation, and secure verifier artifacts before
using a new capability in a hosted cohort. Do not respond to a case-specific
failure by growing the permanent prompt. Put stable API knowledge in an approved
SDK projection, geometric uncertainty in a bounded probe, and acceptance logic
in the verifier.

Before changing a failure path, classify it as one of:

- provider transport, protocol, or accounting;
- controller action policy;
- compatibility or CAD generation;
- secure execution;
- geometry or topology verification;
- observation, probe, or approved knowledge projection.

Do not combine model control-policy failures with actual Harness failures in a
frozen experiment. A changed taxonomy requires a new versioned experiment.

## Research stages and candidate routes

The stages below are experiment boundaries, not implementation layers. A stage
is complete only when its exit evidence exists in code, tests, case metadata,
and validated run artifacts. Passing fake fixtures prove implementation behavior,
not research outcomes.

### Stage 1: Active no-knowledge baseline

Objective: measure whether a real provider can reconstruct low-difficulty
B-Reps using path-free observations, optional geometry probes, typed feedback,
compatibility checking, secure execution, and independent gates, without SDK or
recipe retrieval.

- Use `retrieval_policy=disabled`, zero retrieval capacity, the retrieval-free
  prompt, no retrieval tools, and no retrieval trace.
- Use the frozen runtime-visible order: `box`, `stage1_cylinder`,
  `block_with_hole`, `blind_hole_block`, and `filleted_box`.
- Keep the eval cylinder and every private comparison asset Harness-only.
- Treat `cadquery_v1` as the end-to-end baseline and `ocp_v1` as the low-level
  binding contrast; never fall back between them.
- Report first-shot and one-repair cohorts separately.
- Freeze provider/model, prompt, case hash, runtime fingerprint, verifier,
  backend, task-contract hash, limits, cohort and replicate identity, and
  failure classification.

Exit only when at least 90% of runs are valid and interpretable and the declared
infrastructure/provider/Harness failure rate is strictly below its frozen
threshold. Remaining failures should be explainable from actions, feedback, and
gates.

### Stage 2: local SDK and recipe knowledge prototype

Objective: estimate the causal value of bounded modeling knowledge without
turning retrieval into target-solution lookup.

- Treat the former hosted-replication Stage 2 objective as absorbed by the
  complete Stage 1 v3 cohort; do not repeat v3 under a new stage label.
- Reuse Stage 1 cases, verifier contracts, provider/model, prompt, controller
  limits, and hosted execution path wherever required for a matched comparison.
- Freeze record schema, catalog identity, provenance, backend version, safe
  projection, result bounds, and leakage rules before the experiment.
- Keep SDK symbol knowledge and general recipes as separate sources.
- Run matched `active_no_knowledge`, `active_sdk_only`, `active_recipe_only`,
  and `active_sdk_plus_recipe` conditions.
- Record retrieval relevance and use, post-retrieval submission success,
  incorrect guidance, final success delta, tokens, and cost.
- Never include case scripts, target parameters, private oracles, repository
  paths, or eval references.

Before creating a contract, review the knowledge sources, leakage audit,
matched no-knowledge control, provider/model, cohort, limits, authorization
scope, and fresh run root. Exit only when the ablation and metrics are stable
and produce an interpretable positive or negative result. Stage 1 `exit_ready`
does not itself authorize this work.

### Stage 3: mature modeling datasets

Objective: study scalable indexing, semantic retrieval, and strategy transfer
from governed modeling corpora.

- Establish license, provenance, kernel/CAD version, units, and normalization.
- Detect exact and near duplicates across train/eval boundaries.
- Prevent target-solution, parameter, script, and derived-geometry leakage.
- Represent multiple valid construction sequences without treating one as the
  unique answer; the verifier remains authoritative.
- Compare against matched Stage 1 and Stage 2 controls by mechanism and
  difficulty.

Declare exit criteria in a campaign or experiment contract before a large
import. Dataset availability alone never authorizes Stage 3.

The current candidate priority is:

| Route | Candidate | Score | Decision |
|---|---|---:|---|
| A | Small parameterized families with Active no-knowledge | 9.2 | Stage 1 foundation |
| B | Versioned SDK symbol projections | 8.7 | First Stage 2 knowledge condition |
| C | Human-curated general modeling recipes | 8.1 | Separate Stage 2 ablation before combination |
| D | Extract installed SDK documentation/API metadata | 7.5 | Scale only after B is stable |
| E | Import mature CAD/modeling datasets | 6.3 | Defer to Stage 3 |

Default order after Stage 1 is B and C as separate Stage 2 ablations, then D if
needed, followed by E only after Stage 2 produces interpretable evidence. If new
evidence changes this priority, update this table and the relevant stage
criteria in the same tested slice.

## Current evidence and next condition

The original schema-v6 Stage 1 diagnostic, five-case CadQuery phase, and
representative OCP contrast produced this historical result:

| Metric | CadQuery full phase | CadQuery comparable cases | OCP comparable cases |
|---|---:|---:|---:|
| Runs | 50 | 30 | 30 |
| Valid and interpretable | 48 | 29 | 27 |
| Geometry passed | 17 | 5 | 18 |
| Model decisions | 70 | 44 | 33 |
| Repairs | 20 | 14 | 3 |
| Tokens | 109274 | 70980 | 66735 |
| Cost (USD) | 0.054679935 | 0.035922735 | 0.037751475 |
| Provider/Harness failures | 2 | 1 | 3 |

CadQuery passed its frozen interpretability and infrastructure thresholds. OCP
improved the comparable geometry result from 5/30 to 18/30, including `box`
from 4/10 to 10/10 and `block_with_hole` from 1/10 to 8/10, while both profiles
remained 0/10 on `filleted_box`. OCP also produced 9/15 first-shot passes where
CadQuery produced 0/15.

OCP nevertheless had three infrastructure classifications in 30 runs: two
provider responses reached the frozen output ceiling without a valid action,
and one `finish_without_verifier` artifact was classified as `harness` by the
frozen classifier. Its 10% rate does not satisfy the strictly-below-10% exit
condition. Stage 1 therefore did not exit at that checkpoint. The later v3
replacement did not alter these artifacts or classifications; it established a
new current exit judgment under its own frozen identity.

Preserve all schema-v6 identities, artifacts, and classifications. Do not tune
their prompt, limits, tools, repair count, retrieval policy, fallback, or
taxonomy to make the result positive.

The subsequent admissible condition was a separately identified
protocol-stabilization cohort using schema v7, provider task-contract v2, and
`active-v4`. It tested the
orchestration correction that exposes only currently executable capabilities
and treats bounded provider protocol retry separately from a model decision or
CAD repair. It is not evidence of improved no-knowledge CAD capability and may
not replace or selectively rerun Stage 1 identities.

The frozen stabilization contract is
`cases/campaigns/stage1-active-v4-stabilization.json`. It declares 12 hosted
runs: `box` and `block_with_hole`, `first_shot` and `bounded_repair`, three
replicates each, `ocp_v1`, and retrieval disabled. Validate the contract before
authorization with `brep2code stage1 stabilization-validate`. Every live run
validates its saved provider request projection automatically; the standalone
`stabilization-projection` command supports audit, and `stabilization-report`
requires the complete identity set. A stable report never changes the frozen
Stage 1 exit judgment or authorizes Stage 2.

The hosted confirmation completed all 12 identities with no artifact or
projection validation failure. Nine runs passed, two were generation failures,
and one was a geometry failure. The cohort used 13 model requests and HTTP
attempts, 14,903 tokens, and $0.007858275; no protocol retry occurred. The saved
aggregate under the run root records `protocol_stable: true`,
`stage1_exit_changed: false`, and `stage2_authorized: false`.

For any new hosted cohort:

1. keep projection and protocol behavior covered by deterministic fake tests;
2. define a new experiment identity and complete cohort in advance;
3. run the read-only readiness gates;
4. obtain fresh authorization for the exact provider, model, case scope,
   outbound projection, limits, and new root;
5. validate and aggregate every planned artifact, including failures.

The attempted replacement baseline
`cases/campaigns/stage1-no-knowledge-v2.json` aborted after 41 valid terminal
attempts because identity 42 left a nonterminal provider-exchange checkpoint.
Its saved aborted report is diagnostic evidence only: it is incomplete, cannot
be continued or selectively rerun, does not change the Stage 1 exit, and does
not authorize Stage 2.

The replacement frozen baseline is
`cases/campaigns/stage1-no-knowledge-v3.json`. It contains the same 80 identities: the
five-case CadQuery baseline and the three-case OCP contrast, both with
first-shot and bounded-repair cohorts at five replicates. It preserves the 90%
valid-attempt threshold and the strictly-below-10% infrastructure threshold.
Execution protocol v3 normalizes bounded transport and response-read failures
into terminal provider failures while keeping request, response, and accounting
artifact failures fatal. Its readiness binds the stable protocol prerequisite,
the SHA-256-bound v2 aborted report, 20 fake baselines, a fresh root, both secure
backend versions, all 80 identities, the exact outbound projection, and maximum
authorization scope. Readiness does not read provider configuration, create
run artifacts, make requests, grant authorization, or authorize Stage 2.

The v3 cohort completed all 80 identities. CadQuery produced 50/50 valid
attempts and 15 geometry passes; OCP produced 30/30 valid attempts and 17
geometry passes. Both infrastructure failure rates were 0%, artifact and
projection validation had no failures, and the aggregate used 110 HTTP
attempts, 137,335 tokens, and $0.072397485. The frozen phase gates therefore
set the current Stage 1 judgment to `complete: true` and `exit_ready: true`;
`stage2_authorized` remains false.

The former hosted-replication Stage 2 objective is satisfied by the complete v3
path and is now part of Stage 1 history. The next admissible activity is a Stage
2 knowledge-retrieval scope review, not a provider run. It must define bounded
SDK and recipe sources as separate ablations, leakage controls, a matched
no-knowledge control, exit criteria, and the exact provider/model, prompt,
cohort, limits, authorization scope, and fresh run root. Only an approved
outcome of that review may introduce a Stage 2 contract or authorize execution.

## Verification workflow

Use the configured project environment and run the smallest relevant checks
first. The normal full order is:

```powershell
uv sync --dev
uv run brep2code env doctor
uv run brep2code cases validate
uv run pytest -q
uv run pytest --run-secure -q
uv run ruff check src tests
```

The secure suite requires WSL2, `Ubuntu-24.04`, and the configured runtime
containing Python, the selected CAD backend, `bwrap`, `prlimit`, and `timeout`.
`BREP2CODE_WSL_DISTRO` and `BREP2CODE_RUNTIME_ROOT` select portable host
settings and are never projected to the model.

Before a secure run, use the read-only checks:

```powershell
wsl.exe --status
wsl.exe -l -v
uv run brep2code env doctor
```

If the restricted environment reports WSL service or distro access failure,
request narrowly scoped external execution rather than weakening the sandbox.
If approval is unavailable, report the blocker and provide the corresponding
PowerShell command for manual execution. Unit tests and case validation may run
without WSL, but provider-generated code must never use the trusted local
executor as a workaround.
