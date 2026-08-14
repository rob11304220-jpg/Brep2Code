# WP-M48-001: Q01 Structured Observation Runtime Implementation

- Status: done
- Milestone: M48
- Owner: Codex
- Reviewer: Liaol
- Risk tier: G2

## Goal

Implement the frozen M47 observation/build capability contract and validate it
offline against fixed fixtures under M46 provenance classification.

## Scope

- Implement only the M47-selected bounded Q01 tools and their sanitized,
  revision-scoped traces.
- Assemble a short tool-facing LLM context; expose no raw STEP bytes or host
  path.
- Remove the original STEP mount from the executed build-script capability in
  the tool-assisted evaluation mode.
- Add local fixture regressions for valid observation, unsupported query,
  direct-round-trip denial, and independent build provenance.

## Attribution question and sampling intent

Does the fixed tool contract supply recorded geometric facts while preventing
the executed script from obtaining the original STEP?  Use only M47-frozen
fixtures; do not substitute cases after seeing results.

## Inputs

- Completed M46 workpack and reviewer evidence.
- Completed M47 decision package and ADR.

## Code paths

Expected: `brep2code/agent/tools/brep.py`, `brep2code/brep/`, runtime context
assembly, `brep2code/cad/executor.py`, `brep2code/agent/harness.py`, corpus
report projection, fixtures and focused tests.  Exact paths are frozen by M47.

## Docs to update

Status, active handoff, M47 decision/ADR where implementation confirms the
contract, runtime sandbox runbook, tool/module documentation, and schema docs
if additive traces require them.

## Trace/schema changes

Potential additive query/provenance fields only; preserve existing consumers.
Define schema versioning and backward compatibility before implementation.

## Decision-package impact

- `decision_id`: `q01-q02-observation-build-separation-v1`.
- Q01/Q02 effect: implements M47's bounded observation-to-script contract.
- Q03/Q04 effect: requires M46 provenance and retains geometry gates.
- Evidence role: tool-boundary, round-trip negative and independent-build
  regressions.
- Knowledge disposition: no reusable modeling knowledge without later review.

## Compatibility constraints

Offline and credential-free.  No hosted call, manifest/case expansion, raw
STEP egress, CAD helper/IR/SDK, generic history claim, or editability claim.

## Acceptance

```powershell
uv run python -m pytest tests\test_agent_m3_tool_bridge.py tests\test_harness_m2.py tests\test_corpus_m4.py -q
uv run python -m pytest tests\test_governance_audit.py -q
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

Independent reviewer approval is required.

## Evidence reuse / guidance-card disposition

No guidance card unless a later evidence review explicitly selects one.

## Status transition

May be selected only after M47 is done and an independent reviewer is named.

## Closure rationale

Owner implementation, acceptance, and Liaol's independent review on
2026-08-08 are complete. The implementation adds path-free observation
envelopes, revision-scoped observation query/context traces, a 12 KB context
guard, an additive observation report field, and the opt-in no-input build
mode. The file-based WSL box control at
`C:\tmp\brep2code-m48-verify-cli\records\m48-no-input-build\revisions\20260808T034019331108Z\signal_bundle.json`
passed health gates with no `/input/model.step` mount and
`independent_reconstruction` provenance. Owner acceptance: 55 focused tests,
Ruff, governance audit, and `git diff --check` passed.

## Out of scope

Hosted LLM evaluation.  A later G3 workpack, with fresh preflight and explicit
authorization, is required before testing a provider/model.
