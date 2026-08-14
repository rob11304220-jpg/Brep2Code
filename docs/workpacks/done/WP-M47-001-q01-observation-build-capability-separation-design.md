# WP-M47-001: Q01 Observation / Build Capability-Separation Design

- Status: done
- Milestone: M47
- Owner: Codex
- Reviewer: not required (G1)
- Risk tier: G1

## Goal

Design the smallest runtime contract through which an LLM can inspect an input
STEP using structured Q01 tools, infer a construction plan, and write a Q02
build script that has no original-STEP read capability during execution.

## Scope

- Define two capabilities and their boundary: an observation plane that may
  query B-Rep facts, and a build plane that may construct/export geometry but
  cannot read `/input/model.step`.
- Freeze a minimal on-demand Q01 tool surface and JSON response bounds:
  global summary, entity lookup, topology/adjacency relations, and bounded
  measurement queries.  Do not send raw STEP text to the LLM.
- Define a traceable exchange format from observations to the generated
  `build_sequence.py`, including query logs, response hashes, and declared
  uncertainty/unsupported outcomes.
- Specify how M46 provenance classification and existing geometry gates apply
  to a tool-assisted generated script.
- Define a fixed offline fixture matrix and stopping rules for a later G2
  implementation.

## Attribution question and sampling intent

Can an LLM receive enough bounded, recorded B-Rep facts to write a script
without relying on the mounted original STEP?  This design distinguishes
observation-based reconstruction from raw-file round trip.  It does not claim
that a particular model understands feature history, add examples, or run a
provider.  Stop if the existing probe API cannot supply a proposed fact without
unbounded traversal or leaking a reference history label.

## Inputs

- `docs/architecture/v1/runtime-boundaries.md`
- `docs/architecture/adr/0048-reconstruction-provenance-gate-design.md`
- `docs/corpus/knowledge/decisions/q03-reconstruction-provenance-v1/decision.json`
- `brep2code/agent/tools/brep.py`
- `brep2code/brep/probes.py`
- `brep2code/agent/repair.py`

## Code paths

Design only.  A later implementation may change Q01 tool adapters, runtime
context assembly, executor mounts, traces, and focused tests, but this
workpack changes none of them.

## Docs to update

- `docs/workflow/status.md` when selected
- this workpack and an active handoff when selected
- a new Q01/Q02 decision package and ADR if the selected design becomes a
  durable capability contract

## Trace/schema changes

None.  The design must propose additive observation-query and capability
attestation traces without changing the existing signal bundle or corpus
schemas.

## Decision-package impact

- `decision_id`: proposed `q01-q02-observation-build-separation-v1`.
- Q01/Q02 effect: permits only recorded structured B-Rep observation before
  script execution; it excludes raw STEP access from the build capability.
- Q03/Q04 effect: M46 provenance is required for any reconstruction claim;
  Q04 receives only sanitized execution/provenance signals.
- Evidence role: a future direct round-trip negative control, tool-boundary
  regression, and independently constructed fixture.
- Knowledge disposition: design only; no runtime guidance card.

## Compatibility constraints

Offline, no credential, no provider request, no raw STEP egress, no case or
manifest change, no CAD helper/IR/SDK, and no prompt implementation.  M46 must
first close successfully; a blocked M46 blocks this workpack.

## Acceptance

- The contract names each tool, its bounded input/output schema, access plane,
  trace, timeout and unsupported disposition.
- It shows that the executed build script has no original-STEP capability while
  Q01 observation remains auditable.
- It defines a fixed local fixture matrix and does not use reference scripts
  as LLM inputs.
- `uv run python tools/check_governance.py` and `git diff --check` pass.

## Evidence reuse / guidance-card disposition

No reusable evidence; this is a capability design.

## Status transition

Select only after M46 is done and the user chooses this bounded G1 design.
Create an active handoff, then update status before moving this workpack to
`active/`.  A resulting G2 implementation must be a separate workpack with an
independent reviewer.

## Closure rationale

The design is complete. ADR-0049, the planned Q01/Q02 decision package, and
the planned capability contract freeze the four-tool surface, limits, local
trace exchange, build-capability attestation, M46 interaction, fixture matrix,
and stopping rules without changing runtime behavior. Decision JSON parsing,
the governance audit, and `git diff --check` passed. Any implementation still
requires explicit selection of a separate G2 workpack.

## Out of scope

Tool implementation, provider/model comparison, hosted evaluation, prompt
changes, feature-history labels, reference-script injection, raw STEP access
from the build script, or an editability claim.
