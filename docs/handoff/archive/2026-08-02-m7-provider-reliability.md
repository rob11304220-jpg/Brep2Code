# Handoff: M7-001 provider reliability and recovery

- **Date**: 2026-08-02
- **Subproject**: `brep2code`
- **Status**: `active`

## Goal

Complete M7-001's offline and loopback verification of provider deadline, cancellation/worker cleanup, request accounting, and corpus report recovery before any further hosted corpus evaluation.

## Done

- M0 through M6 are complete; M6 established bounded DeepSeek repair and its evidence boundary.
- Created the M7 roadmap and three evidence-ordered workpacks: M7-001 active, M7-002 first-pass generation backlog, and M7-003 self-authored corpus-expansion backlog.
- Updated the corpus contract and provider runbook to distinguish completed, interrupted, and running report evidence, and to require a fresh authorization for any future hosted request.

## In progress

- M7-001 is active. No provider reliability implementation or new hosted request has been performed in this documentation transition.

## Development-governance note

- Added a development-only case-governance framework under `docs/corpus/`: self-authored registry, seven human-readable case cards, catalog, external-dataset registry, and future sample-selection template. It does not alter Harness, runtime LLM material, manifests, fixtures, or M7-001/M7-003 status; see `docs/architecture/adr/0007-development-case-governance.md`.

## Next

- Read M7-001 and inspect existing provider worker, repair accounting, corpus checkpoint, and offline tests.
- Implement only the offline/loopback reliability coverage and required code changes; do not make a hosted request without new explicit authorization.
- Update the workpack, status page, and this handoff with acceptance evidence before promoting M7-002.

## Decisions

- M7 proceeds reliability first, then first-pass generation evaluation, then self-authored corpus expansion; see [`m7-evaluation-roadmap.md`](../../architecture/v1/m7-evaluation-roadmap.md).
- IR, project CAD SDK, and CAD workplace remain deferred until completed multi-case evidence satisfies the roadmap's escalation gate.
- Development-side case governance is separate from Harness/runtime material; see [ADR-0007](../../architecture/adr/0007-development-case-governance.md).

## Blockers

- None for offline/loopback work. Any real hosted validation requires new explicit provider/model, case/round, timeout, and request or cost budget authorization.

## Key paths

| Kind | Path |
|------|------|
| Branch | `main` |
| Active workpack | `docs/workpacks/active/WP-M7-001-provider-reliability-and-recovery.md` |
| Roadmap | `docs/architecture/v1/m7-evaluation-roadmap.md` |
| Corpus contract | `docs/architecture/v1/contracts/case-corpus.md` |
| Provider runbook | `docs/runbooks/llm-provider-config.md` |
| Commands | `uv run python -m pytest`; `uv run python -m ruff check .` |

## Resume prompt

```
Continue Brep2Code M7-001 provider reliability and recovery.
Read AGENTS.md, docs/handoff/active/2026-08-02-m7-provider-reliability.md, docs/workflow/status.md, and the active workpack.
First action: inspect the existing provider worker, corpus checkpoint, and offline tests; do not make a hosted request without explicit authorization.
```
