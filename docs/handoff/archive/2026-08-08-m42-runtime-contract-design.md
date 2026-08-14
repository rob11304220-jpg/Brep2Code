# Handoff: M42 first-pass runtime-contract design

- **Date**: 2026-08-08
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M42-001-first-pass-runtime-contract-design`

## Goal

Finish the offline, design-only preregistration that distinguishes LLM
first-pass runtime-contract incompatibility from B-Rep modeling failure before
any separate hosted evaluation is considered.

## Done

- User selected the new bounded decision package.
- M42-001, `q02-first-pass-runtime-contract-v1`, and ADR-0045 were created.

## In progress

- None.  The design and its focused offline acceptance checks are complete.

## Next

- If the user selects the next phase, create a separate G3 development-only
  hosted evaluation workpack with an independent reviewer, then perform the
  required preflight before asking for provider authorization.

## Decisions

- M42 is G1 and offline design-only; any hosted evaluation is a later G3
  workpack with its own independent review and explicit authorization.
- The contract is constrained to path, output, import compatibility, and
  execution facts; it does not add feature semantics or a helper.
- ADR: [`ADR-0045`](../architecture/adr/0045-first-pass-runtime-contract-design.md).

## Blockers

- Hosted work remains intentionally unauthorized and unselected.

## Key paths

| Kind | Path |
|------|------|
| Branch | `main` |
| Files | `docs/workpacks/active/WP-M42-001-first-pass-runtime-contract-design.md`; `docs/corpus/knowledge/decisions/q02-first-pass-runtime-contract-v1/decision.json`; `docs/architecture/adr/0045-first-pass-runtime-contract-design.md` |
| Commands | `uv run python -m pytest tests\\test_governance_audit.py tests\\test_corpus_m4.py -q`; `uv run python tools/check_governance.py` |

## Resume prompt

```
Continue Brep2Code work: decide whether to select M42's separate G3 development-only hosted evaluation.
Read docs/handoff/active/2026-08-08-m42-runtime-contract-design.md.
First action: verify that user wants the hosted phase and identify an independent reviewer; then complete the hosted preflight without sending data.
```
