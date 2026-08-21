# Architecture

Brep2Code is a Harness-first program-synthesis system. It turns a validated
STEP/B-Rep task into a complete CAD program, executes that program in a bounded
environment, and accepts the generated model only through an independent
verifier. The model proposes actions; the Harness owns the run.

## System boundaries

The system has five distinct responsibilities:

1. **Experiment and operator policy** selects the case, provider, model,
   backend, knowledge condition, limits, cohort identity, and hosted
   authorization.
2. **Active controller** owns the state machine, derives the capabilities
   visible on each turn, dispatches actions, accounts controller usage, and
   checkpoints the session.
3. **Provider adapter** projects the bounded task to a model and returns one
   provider-neutral action. It separately owns transport attempts, protocol
   retries, token accounting, and cost accounting.
4. **Submission pipeline** persists a complete script, checks compatibility,
   executes it in the secure backend, and produces a candidate STEP artifact.
5. **Verifier** evaluates the candidate independently and is the only component
   that may declare success.

These responsibilities are intentionally not collapsed into a general-purpose
agent. Fixed generation remains an explicit experimental control and is never a
fallback from Active.

```text
experiment policy
       |
       v
Active controller -- capability projection --> provider/model
       ^                                          |
       |                                     one action
       |                                          |
       +---- tool result or typed feedback -------+
       |
       +---- submission --> compatibility --> secure execution --> verifier
                                                                  |
                                                           pass or feedback
```

## Active control loop

The controller starts from a path-free observation of the input B-Rep. On every
model turn it exposes only the actions and tools that are executable in the
current state. The model selects exactly one action envelope:

```json
{"action":"probe","probe":{"tool":"edge_candidates","arguments":{}}}
```

```json
{"action":"retrieve","retrieve":{"query":"topology-aware edge selection","scope":["sdk","recipe"],"limit":2}}
```

```json
{"action":"submit","submit":{"script":"complete build.py"}}
```

```json
{"action":"finish","finish":{"reason":"no further useful action is available"}}
```

The legacy exact retrieval form
`{"action":"retrieve","retrieve":{"topic":"TopoDS.Edge_s"}}` remains
valid for deterministic OCP binding diagnostics.

The controller owns the states `OBSERVING`, `PROBING`, `RETRIEVING`,
`SYNTHESIZING`, `EXECUTING`, `VERIFYING`, `REPAIRING`, and the terminal states
`SUCCEEDED`, `EXHAUSTED`, and `FAILED`. A tool result returns control to the
next model decision. A failed verified submission produces typed feedback for a
bounded repair. `finish` is advisory and cannot enter `SUCCEEDED`.

## Provider-visible projection

The provider-visible task contains only information needed to choose the next
CAD action:

- case identity and unit;
- initial path-free geometry observations;
- actions and tools executable on the current turn;
- a coarse `initial_attempt` or `repair` phase;
- selected backend, allowed import root, API summary, and export contract;
- session-local probe or retrieval results;
- the current complete revision, when one exists;
- typed compatibility, execution, or verifier feedback.

The following invariant is mandatory:

> Internal limits determine which capabilities are exposed. Numeric limits,
> usage, transport policy, cost, authorization, experiment governance, and
> executor configuration are never part of the provider-visible task.

In particular, the projection excludes controller budget values and remaining
capacity, HTTP ceilings and attempts, protocol retries, tokens, prices, cost,
timeouts, campaign totals, hosted authorization, checkpoint policy, WSL paths,
sandbox resource limits, and host configuration.

When a capability is unavailable, the controller removes its action and tool
from the projection. It does not ask the model to interpret or manage the
underlying numeric limit. The prompt examples are filtered by the same action
projection, so the task payload and system instructions cannot advertise
different capabilities.

The model also never receives eval references, target solutions, private
oracles, repository files, control scripts, host paths, environment variables,
credentials, or undeclared network access. Runtime values use case-relative or
path-free identities.

## Independent limit layers

Limits remain required for bounded and reproducible runs, but they belong to
separate owners:

- **Controller limits** bound model decisions, probes, retrievals, script
  submissions, executions, and verifier-guided repairs.
- **Provider limits** bound HTTP attempts, protocol retries, response size,
  tokens, cost, and request timeout.
- **Executor limits** bound wall time, memory, processes, filesystem exposure,
  logs, output size, and network access.

A model decision is not an HTTP attempt. A provider protocol retry is not a new
model decision, CAD submission, execution, or verifier-guided repair. A script
rejected by compatibility checking is a generation counterexample and does not
consume an execution attempt. These distinctions must remain visible in saved
accounting and failure classification.

## Backend and task contract

Each run selects exactly one backend profile. `ocp_v1` freezes
`cadquery-ocp==7.9.3.1.1`; `cadquery_v1` freezes `cadquery==2.8.0`. A run never
falls back between profiles.

The provider task contract binds the selected package and version, allowed
imports, API and export summaries, required `output.step`, retrieval policy,
action surface, tool surface, and stable safety restrictions. Its canonical
SHA-256 is stored in Active results and checked on continuation.

Frozen schema-v6 results bind task-contract v1 and the `active-v3` prompt.
Current schema-v7 results bind task-contract v2 and `active-v4`, which implement
the capability-only turn projection. The old results remain valid evidence;
the new contract does not retroactively change their experiment identity.

## Submission and verification

Every `submit` action supplies one complete deterministic script. The submission
pipeline creates a new immutable revision and:

1. rejects an unchanged repair after a failed revision;
2. applies backend-specific compatibility checks;
3. verifies that execution is currently allowed;
4. runs the script through the configured WSL2/bubblewrap backend;
5. requires a bounded `output.step`;
6. inspects the result and dispatches the task's required gates.

Compatibility failures, execution failures, and geometry failures are converted
to typed feedback. Only a candidate that executed and passed every required gate
may produce `SUCCEEDED`.

The secure executor clears ambient variables, disables networking, exposes only
the revision input and bounded output, and enforces time, memory, process, log,
and output limits. These protections are Harness guarantees; their operational
details are not model reasoning inputs. If the secure backend is unavailable,
provider-generated code is not run through the trusted local executor.

## Task, verifier, and asset contracts

Cases live under `cases/<split>/<case_id>` and appear exactly once in a split
manifest. Runtime loading accepts only `smoke` and `train`; the Harness owns
evaluation loading.

A task may contain optional mechanism and capability metadata for reporting,
but the runtime contract is the target geometry plus its verifier pack. The
verifier defines target references, required gates, repair policy, and reference
projection policy without prescribing one unique modeling sequence. Multiple
valid programs may therefore pass the same task.

Assets have distinct visibility:

- input STEP and safe derived observations support model reasoning;
- verifier references and gate oracles remain Harness-only;
- controls support tests and evaluation but never enter runtime prompts;
- dossier and campaign policy configure evaluation and are not projected
  wholesale;
- retrieved SDK or recipe records are answer-free projections and must not
  contain target scripts, target parameters, private oracles, or host paths.

## Artifacts and continuation

A session owns an atomically updated `result.json` and sequential immutable
revision directories. Artifacts record the selected task and backend contract,
retrieval condition, controller trace and usage, provider accounting when
applicable, terminal state, stop reason, and validation results. Secrets and
authorization are never persisted.

The Harness checkpoints before provider and tool work and at submission,
repair, and terminal boundaries. A nonterminal checkpoint may continue only
when its saved result validates and the case, provider/model, total controller
limits, provider limits, timeout, retrieval policy, backend contract, and
revision root remain consistent. Interrupted provider or execution attempts are
charged conservatively. Hosted continuation requires fresh authorization; it
never inherits permission from the checkpoint.

Code, tests, case metadata, and validated run artifacts are the evidence
authorities. CLI `--help` owns command syntax; architecture documentation does
not duplicate every flag or individual run history.
