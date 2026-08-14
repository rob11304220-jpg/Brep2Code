# Handoff: M46 reconstruction-provenance gate implementation

- **Date**: 2026-08-08
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M46-001-reconstruction-provenance-gate-implementation`

## Goal

Implement M45's offline Q03 provenance classification and absent-input control
so that M44-style STEP round trips cannot be counted as reconstruction.

## Done

- M45 froze the `round_trip` / `independent_reconstruction` /
  `provenance_unknown` contract in ADR-0048.
- M46 has an independent-review, G2 implementation plan.
- Verified an `LD_PRELOAD` tracer in the actual `wsl-bwrap` runtime: it records
  Python, child-process, and OCP `STEPControl_Reader` access to
  `/input/model.step`.
- Added executor trace staging, coverage attestation, same-script absent-input
  control, and Harness provenance classification. A real local OCP round trip
  passes health gates and is classified `round_trip`; an independent local
  box scaffold passes the absent-input control and is classified
  `independent_reconstruction`.
- Added discriminating child-read, independent-construction, and fail-closed
  automated regressions; projected the versioned provenance object additively
  into schema-v3 corpus reports; and documented the verification procedure.
- Owner acceptance passed: 45 focused Harness/corpus tests, 7 governance
  tests, Ruff, governance audit, and `git diff --check`.
- Re-ran the child-process fixture: its expected missing-output health-gate
  failure is separate from provenance; two traced process IDs read the mounted
  input and the result is correctly `round_trip`.

## In progress

- Closed after Liaol's independent G2 review.

## Next

M46 is complete. Do not start a new workpack without explicit user selection.

## Decisions

- Geometry success remains Harness-health evidence only; provenance is
  separately fail-closed under ADR-0048.
- Liaol is the independent reviewer for this G2 workpack.

## Blockers

- No tracer feasibility blocker remains.  No hosted request is authorized.

## Key paths

| Kind | Path |
|------|------|
| Branch | `main` |
| Workpack | `docs/workpacks/active/WP-M46-001-reconstruction-provenance-gate-implementation.md` |
| Contract | `docs/corpus/knowledge/decisions/q03-reconstruction-provenance-v1/decision.json` |
| Executor | `brep2code/cad/executor.py` |

## Resume prompt

```
Independently review M46. Read the active workpack and ADR-0048, inspect
brep2code/cad/provenance_trace.c, executor.py, harness.py, and corpus/runner.py.
Verify the normal and absent-input evidence bundles under C:\tmp\brep2code-m46-verify,
then rerun the workpack acceptance commands. If the review approves scope,
evidence, and compatibility, mark the workpack done and archive this handoff.
```
