# WP-M85-001: Reference-Assisted P0 Hosted Smoke

- Status: done
- Milestone: M85
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G3

## Goal

Implement and then verify one frozen P0 `cylinder` observation-to-build
request. The model must request the single permitted revision-scoped guidance
card before it generates a script, and the secure executor must apply the
unchanged output and geometry gates.

## Entry criteria

- M19-003 completed with independent review and no development gate regression.
- Local fake-provider coverage proves the fixed two-request state machine,
  including the guidance fail-closed and provider-accounting paths.
- A fresh hosted preflight verifies the selected `cylinder` P0 input/hash, pack
  index/card hash, top-k limit, provider/model, secure executor, report/monitor
  paths, deadline, and unused two-request budget.
- The user explicitly authorizes destination, egress content, provider/model,
  case, reference-pack index/top-k, two-request/no-retry policy, deadline,
  budget, executor, and report paths.

## Scope

- Fixed P0 `cylinder` only; fixed guidance role `final primitive`; fixed
  `vertical-cylinder-construction` card; index/card hashes and `top-k=1`.
- Request 1 may only return that guidance-tool request. Harness validates and
  dispatches it locally; request 2 may only return a replacement script.
- Record per-request lifecycle/accounting, selected card/index hash, script
  contract, sandbox result, provenance, and unchanged geometry gates.

## Compatibility constraints

Exactly two provider requests, one guidance call, zero repair rounds and zero
retries. No prompt comparison, case expansion, pack mutation, held-out use,
model/endpoint change, gate relaxation, or budget/report-path reuse.

## Acceptance

Offline acceptance includes deterministic two-stage fake-provider coverage,
invalid guidance/tool-call rejection, hash-drift rejection, request accounting,
and existing contract/gate regressions. Hosted acceptance, if separately
authorized, requires terminal parseable lifecycle evidence plus P0
script/API/sandbox/output/geometry gates. A failure stops the workpack and
creates no authorization for repair or a broader batch.

## Local implementation record

- Added the provider-neutral `tool_call` response field and a fixed two-stage
  runner path: first completion requests the sole permitted card, then the
  second completion produces the replacement script.
- Added `reference-assisted-smoke`, restricted to `cylinder`, `final
  primitive`, budget two and zero repair. Fake-provider smoke passed the full
  script/API/output/geometry gate chain with two recorded provider requests.
- Added `--phase prepare|execute` for the M85 command. The fresh durable report
  begins at `0/2`, checkpoints immediately before each issued provider request
  at `1/2` and `2/2`, then terminalizes without any resume/retry path.
- 2026-08-10 local checks passed: governance audit; 34 focused tests; Ruff;
  `git diff --check`. A previous full suite run reached 200 passing tests before
  two governance assertions exposed the new handoff's missing backticks; that
  format defect is fixed and covered by the subsequent focused governance run.

## Remaining review / hosted gate

- Liaol must independently review the provider response boundary, the exact
  first-call validator, trace/report accounting and default no-hosted behavior.
- User authorized and completed one fixed hosted smoke on 2026-08-10. Its
  terminal report is `data/corpus-runs/m85-cylinder-reference-assisted.json`:
  `completed`, two requests used, frozen card returned, and OCP/
  `wsl-bwrap`/output/bbox/volume/topology gates passed with no input access.

## Independent review and closure

- Reviewer: Liaol
- Outcome: approved on 2026-08-10.
- Closure rationale: The fixed `cylinder` smoke used exactly the separately
  authorized two-request budget, recorded the frozen guidance card, and passed
  the unrelaxed OCP contract, secure-executor, output and geometry gates. This
  closes M85 only; it does not establish a quality claim, authorize retry, or
  unlock M73.

## Out of scope

Any quality/generalization claim, P1 evaluation, automatic retrieval tuning,
or M73 activation.
