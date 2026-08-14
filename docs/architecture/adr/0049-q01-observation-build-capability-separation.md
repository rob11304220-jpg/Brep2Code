# ADR-0049: Separate Q01 Observation from Q02 Build Capability

- **Status**: Accepted
- **Date**: 2026-08-08

## Context

The existing bounded B-Rep bridge can inspect a record input through summary,
topology, entity, and sampling calls, while the M46 provenance gate prevents a
script that reads `/input/model.step` from being counted as reconstruction.
Those controls do not yet define which component may read the original STEP,
what an LLM may retain from its observation, or how a later build execution is
shown to lack the original-file capability.

## Decision

Adopt a two-capability runtime contract for a future separately selected G2
implementation:

1. The **Q01 observation plane** may resolve the selected record input only
   through four bounded structured tools: `probe_summary`, `probe_topology`,
   `probe_entity`, and `sample_entity`. It returns schema-versioned facts,
   never raw STEP bytes, host paths, full overflow traces, reference scripts,
   or history labels. Each call has a bounded request, response, deadline,
   unsupported result, and digest-recorded local trace.
2. The **Q02 build plane** receives only the generated `build_sequence.py`,
   an opaque observation-session identifier, and the recorded structured
   observation transcript or its bounded summary. Its normal `wsl-bwrap`
   execution has no `/input/model.step` mount and cannot call observation
   tools. It retains only writable `output/` and `intermediates/` paths.
3. Any reconstruction classification keeps ADR-0048's normal trace,
   no-read, and same-script absent-input control requirements. Existing
   geometry gates remain health evidence, not construction provenance.

The exact schemas, fixed fixture matrix, trace fields, and fail-closed
conditions are recorded in decision package
`q01-q02-observation-build-separation-v1`.

## Consequences

This defines a narrow, auditable input-information route without adding a CAD
operation SDK, fixed IR, runtime prompt, provider call, or implementation.
If the current probe bridge cannot provide a proposed fact within its fixed
bounds, a later implementation must return `unsupported`; it must not widen
traversal, expose a local overflow trace, or give the build script raw input
access. This ADR authorizes neither a G2 implementation nor any hosted run.
