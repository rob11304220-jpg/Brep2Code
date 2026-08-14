# WP-M7-001: Provider Reliability and Recovery

- Status: done
- Milestone: M7
- Owner: unassigned

## Goal

Establish reproducible offline and loopback evidence for hosted-provider request lifecycle behavior before any further hosted corpus evaluation. Clarify provider deadlines, cancellation, worker cleanup, request accounting, and corpus report recovery without changing the default offline CLI behavior.

## Scope

- Add or strengthen offline/loopback fault-injection coverage for timeout, provider error, worker termination, duplicate or failed request accounting, and report checkpoint behavior.
- Verify controlled interruption and document the distinct meaning of `running`, `completed`, and handled `interrupted` reports; retain the existing external-force-stop boundary.
- Confirm that default corpus and fake-provider replay make no network request and that provider-generated scripts remain bound to `wsl-bwrap`.
- Update the case-corpus contract and provider runbook with the accepted failure, recovery, and review procedure.

## Inputs

- [M6 hosted evaluation report](../../architecture/v1/m6-hosted-evaluation-report.md)
- [M7 evaluation roadmap](../../architecture/v1/m7-evaluation-roadmap.md)
- [Case corpus contract](../../architecture/v1/contracts/case-corpus.md)
- [LLM provider configuration runbook](../../runbooks/llm-provider-config.md)

## Code paths

| Path | Purpose |
|------|---------|
| `brep2code/agent/provider.py` | Bounded hosted completion and worker lifecycle, if changes are required. |
| `brep2code/agent/repair.py` | Provider request accounting and structured repair errors, if changes are required. |
| `brep2code/corpus/runner.py` | Checkpoint, report-status, and failure-classification behavior. |
| `tests/test_corpus_m4.py` | Offline/loopback reliability and recovery coverage. |

## Docs to update

- `docs/workflow/status.md`, this workpack, and the active handoff at every status transition.
- `docs/architecture/v1/contracts/case-corpus.md` and `docs/runbooks/llm-provider-config.md` when accepted lifecycle or recovery behavior changes.
- Write an ADR only if implementation establishes a new lasting timeout or cancellation architecture boundary; this planning workpack does not itself create one.

## Trace/schema changes

No new report schema is planned. Preserve schema-v2 hosted evaluation metadata and its sanitized trace references. If implementation changes a lifecycle field or failure classification, update the case-corpus contract and add compatibility tests. Never persist credentials, environment snapshots, or complete provider responses.

## Compatibility constraints

- Default commands remain network-free, credential-free, and deterministic.
- `--repair` remains the local fake-provider replay mode and is mutually exclusive with hosted mode.
- Hosted requests remain opt-in and require explicit authorization, positive case/round/request bounds, a timeout, valid configuration, and a secure executor.
- No real hosted request is in scope. A targeted hosted validation needs a new explicit authorization stating provider/model, cases, rounds, timeout, and cost or request budget.
- Do not introduce an IR, project CAD SDK, CAD workplace, new probe, or geometry gate.

## Acceptance

- Loopback/offline tests cover timeout, provider error, bounded worker termination, request issuance accounting, checkpoint replacement, and controlled interruption.
- Tests distinguish completed case checkpoints from a false aggregate completion after external termination.
- Tests prove the default corpus and fake-provider paths make no hosted request; hosted selection continues to require `wsl-bwrap`.
- Reports and traces contain no credential markers or full provider responses.
- `uv run python -m pytest` and `uv run python -m ruff check .` pass, with any execution-window limitation documented alongside actual test output.

## Completion evidence

- 2026-08-02: added deterministic process-double coverage for provider timeout termination and join, loopback provider-failure accounting, hosted checkpoint request accounting, external-force-stop checkpoint semantics, and default/fake-provider offline guards.
- Focused verification: `uv run python -m pytest tests/test_corpus_m4.py -q` — 25 passed in 78.37s; `uv run python -m ruff check tests/test_corpus_m4.py` — passed.
- Final verification: `uv run python -m pytest` — 54 passed in 105.26s; `uv run python -m ruff check .` — passed.
- No production behavior changed: the existing worker deadline, issued-request accounting, atomic checkpointing, and `wsl-bwrap` hosted guard satisfied the new coverage.

## Status transition

When completed, move this file to `docs/workpacks/done/`, update `docs/workflow/status.md`, create/update the active handoff, and promote M7-002 only after reviewing the completed acceptance evidence.

## Out of scope

- Real hosted evaluation, model comparison, or benchmark claims.
- First-pass generation implementation or report fields.
- New corpus fixtures or external dataset ingestion.
- Modeling IR, project CAD SDK, or CAD workplace.
