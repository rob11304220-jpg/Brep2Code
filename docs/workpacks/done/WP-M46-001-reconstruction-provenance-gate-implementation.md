# WP-M46-001: Q03 Reconstruction-Provenance Gate Implementation

- Status: done
- Milestone: M46
- Owner: Codex
- Reviewer: Liaol (user, independent reviewer)
- Risk tier: G2

## Goal

Implement the M45 provenance contract offline: classify a normal execution as
`round_trip`, `independent_reconstruction`, or `provenance_unknown`, and run a
same-script absent-input-mount control before any result can claim independent
reconstruction.

## Scope

- Add an executor-level, auditable input-access tracer that covers the
  supported Python process, OCP native calls, and child processes inside the
  `wsl-bwrap` sandbox.
- Add a second execution mode using the same immutable generated
  `build_sequence.py` but no `/input/model.step` mount.
- Extend `ExecutionResult`, execution JSON, `signal_bundle.json`, and
  schema-v3 corpus reports with an additive provenance result and paths to its
  local traces.
- Make normal-output geometry gates remain unchanged; derive provenance from
  access evidence plus the absent-input control rather than from geometry.
- Add M44's fixed reader-to-writer script as the `round_trip` regression, an
  independent construction fixture, and an unresolved/coverage-failure
  fail-closed fixture.
- Update the sandbox runbook and module documentation with the new offline
  verification command and interpretation.

## Attribution question and sampling intent

Does a passing geometry result originate from an executed read of the mounted
input STEP or from independent construction?  The fixed M44 script is the
positive counterexample.  Tests use only local fixtures and one existing local
STEP input; no corpus expansion or provider request is permitted.  Stop if the
tracer cannot be shown to observe `open`/`openat`-class access made by Python,
OCP and a child process under the actual `wsl-bwrap` runtime.

## Inputs

- `docs/corpus/knowledge/decisions/q03-reconstruction-provenance-v1/decision.json`
- `docs/architecture/adr/0048-reconstruction-provenance-gate-design.md`
- `docs/architecture/adr/0047-first-pass-round-trip-is-not-reconstruction.md`
- `data/records/corpus-abc_v00_00000031/revisions/20260808T022759497760Z/workspace/build_sequence.py`
- `brep2code/cad/executor.py`
- `brep2code/agent/harness.py`
- `brep2code/corpus/runner.py`

## Code paths

- `brep2code/cad/executor.py` — isolated tracer launch, trace collection,
  absent-input execution, and sandbox metadata.
- `brep2code/agent/harness.py` — deterministic provenance classification and
  additive signal-bundle fields.
- `brep2code/corpus/runner.py` and `brep2code/corpus/report.py` — additive
  schema-v3 report projection.
- `tests/test_harness_m2.py`, `tests/test_corpus_m4.py`, and new sandbox
  fixtures — direct, independent, child-process and fail-closed regressions.

## Docs to update

- `docs/workflow/status.md`
- this workpack and the active handoff
- `docs/runbooks/runtime-sandbox.md`
- `docs/modules/` index/documentation for executor and Harness paths, if those
  modules have registered documentation
- `docs/architecture/adr/0048-reconstruction-provenance-gate-design.md` only
  if implementation reveals a material contract change

## Trace/schema changes

Additive only.  Preserve existing `signal_bundle.json` fields and schema-v3
report fields.  Add a versioned `provenance` object containing result class,
normal-run input-access observation, absent-input control outcome, coverage
attestation, and sanitized local trace paths.  Do not store raw STEP bytes or
introduce provider-trace fields.  If a schema version bump is required, define
the backward-compatibility parser and report tests before changing it.

## Decision-package impact

- `decision_id`: `q03-reconstruction-provenance-v1`.
- Q01/Q02 effect: no new Q01 tool or Q02 prompt; build-script input access is
  measured separately from any future structured observation.
- Q03/Q04 effect: geometry-health gates remain unchanged; provenance is a
  separate fail-closed reconstruction classification.  Repair outputs remain
  diagnostic until a fresh normal run and control are available.
- Evidence role: M44 direct round-trip regression; independent constructor and
  child-process read are discriminating controls; missing tracer coverage is a
  negative/fail-closed control.
- Knowledge disposition: record M44 as a counterexample; do not create a
  runtime guidance card or claim CAD modeling knowledge.

## Compatibility constraints

Offline and credential-free.  Do not change the default executor, provider,
model, prompt, case manifests, input probe, geometry tolerances, CAD operation
surface, repair policy, runtime resource contract, or output locations.
`unsafe-local` must either report provenance unsupported or be explicitly
excluded from reconstruction claims; it must never silently claim independent
reconstruction.  The normal `wsl-bwrap` execution remains the only source of
geometry gates; the absent-input run is a control, not a second geometry
benchmark.

## Acceptance

```powershell
uv run python -m pytest tests\test_harness_m2.py tests\test_corpus_m4.py -q
uv run python -m pytest tests\test_governance_audit.py -q
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

- The exact M44 reader-to-writer fixture passes ordinary health gates but is
  classified `round_trip` with a recorded input-read trace.
- A local independently constructed fixture passes ordinary health gates and
  the absent-input control, and is classified `independent_reconstruction`.
- A child-process or native/OCP input read is detected and classified
  `round_trip`; a missing/failed coverage attestation is
  `provenance_unknown`.
- The same script, executed without `/input/model.step`, never gains an input
  mount and cannot overwrite or mutate normal-run artifacts.
- Existing report consumers and gate-status assertions remain compatible.

## Evidence reuse / guidance-card disposition

Counterexample and execution regression only.  M44 cannot be mounted as
runtime guidance, and a passing independent fixture does not establish generic
history recovery or editability.

## Status transition

Before implementation, record a local tracer feasibility result.  If it fails
to cover the specified runtime access routes, set this workpack `blocked` and
record the missing capability; do not weaken classification.  On successful
implementation and independent review, update status first, then this
workpack, the handoff, relevant module/runbook docs and ADR if needed, and run
all acceptance commands before moving the workpack to `done/`.

## Closure rationale

Implementation, owner acceptance, and Liaol's independent review on
2026-08-08 are complete. The normal `wsl-bwrap` OCP
round-trip run at `C:\tmp\brep2code-m46-verify\records\m46-provenance-round-trip\revisions\20260808T032014628402Z\signal_bundle.json`
passed ordinary health gates and classified `round_trip` with attested native
input access. The independent local box scaffold run at
`C:\tmp\brep2code-m46-verify\records\m46-provenance-independent\revisions\20260808T032054125534Z\signal_bundle.json`
passed health gates and the same-script absent-input control, classifying
`independent_reconstruction` with attestations for both runs.
The child-process fixture evidence at
`C:\tmp\brep2code-m46-verify\records\m46-provenance-child-read\revisions\20260808T032435833915Z\signal_bundle.json`
intentionally fails only its missing-output geometry gates, while recording
two process IDs accessing `/input/model.step` and classifying `round_trip`.

Owner acceptance on 2026-08-08:

```text
uv run python -m pytest tests\test_harness_m2.py tests\test_corpus_m4.py -q  # 45 passed
uv run python -m pytest tests\test_governance_audit.py -q                    # 7 passed
uv run python -m ruff check .                                                  # All checks passed
uv run python tools\check_governance.py                                       # Governance audit passed
git diff --check                                                               # passed
```

## Out of scope

Hosted/provider evaluation, egress, prompt/model changes, raw STEP transfer,
new corpus cases or manifests, Q01 feature recognition tools, new CAD helpers,
IR/SDK design, history-fidelity scoring, editability oracle, or a benchmark
claim.

## Repair hypothesis and evaluation boundary

M44 established a direct trace-supported mechanism: OCP reads
`/input/model.step`, transfers the resulting shape, and writes
`output/model.step`.  The implementation retains its normal health-gate pass
while classifying it as a non-reconstruction result.  The absent-input control
tests causal dependence on the mounted original; the tracer distinguishes a
verified read from unresolved access.  This work is offline only and cannot
authorize a later hosted run.
