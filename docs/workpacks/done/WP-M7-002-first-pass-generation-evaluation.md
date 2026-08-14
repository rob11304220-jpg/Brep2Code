# WP-M7-002: First-Pass Generation Evaluation

- Status: done
- Milestone: M7
- Owner: unassigned

## Goal

Evaluate an LLM's initial B-Rep-to-CAD-script attempt separately from the default scaffold and the existing repair loop, producing reproducible and sanitized evidence for first-pass versus repair behavior.

## Scope

- Define a first-pass generation mode that supplies the bounded B-Rep probe context and writes an initial `build_sequence.py` before Harness execution.
- Record and report distinct primary-generation, repair, and local fake-provider replay outcomes.
- Version the prompt/policy, provider/model, executor, manifest, bounds, latency, request accounting, and failure classifications required to compare runs.
- Keep the default command path offline; document the hosted authorization and pre-submission review procedure.

## Inputs

- [M7 evaluation roadmap](../../architecture/v1/m7-evaluation-roadmap.md)
- [Case corpus contract](../../architecture/v1/contracts/case-corpus.md)
- [Repair loop contract](../../architecture/v1/contracts/repair-loop.md)
- Completed M7-001 acceptance evidence.

## Code paths

| Path | Purpose |
|------|---------|
| `brep2code/corpus/runner.py` | First-pass orchestration and report composition. |
| `brep2code/agent/` | Provider request policy and trace provenance. |
| `brep2code/cli/__init__.py` | Explicit mode selection and offline-safe preflight. |
| `tests/` | Deterministic fake-provider and authorization/report tests. |

## Docs to update

- Update the case-corpus and repair-loop contracts before changing mode or report semantics.
- Add a focused runbook for first-pass hosted evaluation and report review.
- Update status, handoff, module documentation, and this workpack when implementation starts or completes.

## Trace/schema changes

Hosted reports must distinguish `primary_generation`, `repair`, and `fake_provider_replay`, while retaining schema versioning and sanitized provenance. The exact wire schema is an implementation decision to be proposed in the contract before code changes.

## Compatibility constraints

- Existing P0/P1 manifest paths, offline corpus behavior, and fake-provider replay remain compatible.
- Hosted generation needs a new explicit authorization with provider/model, cases, rounds, timeout, and request or cost budget.
- Provider-generated scripts must use `wsl-bwrap`; no credentials, environment snapshots, or full responses may be recorded.

## Acceptance

- Deterministic tests distinguish first-pass generation, repair, and fake-provider replay in reports.
- Prompt/policy provenance and evaluation metadata serialize without secrets.
- Hosted preflight refuses missing authorization, insecure execution, or invalid bounds before a request.
- A completed, separately authorized small hosted run is reviewed before any aggregate claim.
- Full pytest and Ruff pass.

## Implementation evidence

- 2026-08-02: implemented explicit `corpus --first-pass`, manifest `first_pass_script`, bounded `probe_summary` context, schema-v3 `generation_policy`, and separate nullable `primary_generation`, `repair`, and `fake_provider_replay` case fields.
- Local fake first-pass requires a fixture before any case runs; `--first-pass --repair` keeps fake replay explicit through the separate `reference_script` field.
- Hosted preflight accounts for one first-pass request plus up to `max_rounds` repairs per case and refuses further generation after budget exhaustion. No hosted request was made during the preceding offline implementation stage.
- Verification: `uv run python -m pytest` — 58 passed in 122.99s; `uv run python -m ruff check .` — passed.
- 2026-08-02: P0 hosted first-pass command completed with `max_cases=3`, `max_rounds=1`, `request_budget=6`, a 120-second provider timeout, schema-v3 report status `completed`, and 4 requests used. Primary generation passed for `box` and `block_with_hole`; `cylinder` had `script_failure` then passed one hosted repair. The secure executor was `wsl-bwrap`. The report records `deepseek-v4-pro`, while the preceding authorization was for Flash. Retain this only as a scope-deviation engineering record; it is not accepted Flash evidence and does not satisfy the remaining acceptance.
- 2026-08-02: separately authorized P0 `deepseek-v4-pro` first-pass command completed and was reviewed. It used the same bounds, sent only the explicitly authorized bounded probe summaries, and recorded schema-v3 status `completed` with 4 requests. Primary generation passed for `box` and `cylinder`; `block_with_hole` had primary `script_failure` and passed one hosted repair. `wsl-bwrap` executed all provider-generated scripts. The ignored report is `data/corpus-runs/deepseek-p0-first-pass-pro-authorized-20260802.json`; it is accepted bounded engineering evidence, not a model-quality benchmark.

## Out of scope

- Broad model benchmark claims, automatic recurring hosted runs, and cost authority.
- New corpus fixtures or external dataset ingestion.
- IR, project CAD SDK, CAD workplace, new probes, or new gates.
