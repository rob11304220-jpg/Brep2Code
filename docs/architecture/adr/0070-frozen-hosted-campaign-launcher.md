# ADR-0070: Separate Frozen Campaign Intent from Prepared Execution Checkpoint

- **Status**: Accepted
- **Date**: 2026-08-12

## Context

M135 proves that a frozen, hash-bound checkpoint can preserve attribution for a
specific 18-condition epoch, while the generic repair path can construct a
hosted provider without campaign-level accounting or a durable prepare phase.
Future work needs one reusable offline launcher without turning arbitrary CLI
arguments, case paths or cards into provider scope.

## Decision

Introduce a versioned **campaign spec** as immutable intent and a separate
atomic **prepared checkpoint** as local evidence that its inputs and execution
boundary passed preflight.  The spec binds registered case identity/input hash,
split authority, bounded Q01 transcript/hash, optional registered card/hash/
role, provider/model declaration, executor, deadline, token/request caps and
repair policy.  M139 admits only `repair_policy=none` and `max_rounds=0`.

`prepare` revalidates all local bindings, requires fresh distinct report and
monitor paths, creates the checkpoint and initializes the existing read-only
monitor.  Future `execute` must consume that unchanged checkpoint rather than
allowing case/card/budget overrides.  It remains a distinct G3 authority and
is not implemented or authorized by M139.

## Consequences

- A generic local preparation path can be tested without credentials, provider
  construction or egress.
- Raw STEP, repository paths, reference scripts and held-out answers remain
  outside the provider transcript boundary.
- A card is selected by registered ID plus content/index hash and role, not by
  a caller-controlled filesystem path.
- Repair, tool-turn orchestration, broad retrieval and hosted execution remain
  separate decisions; this adds initial setup work but avoids changing an
  experiment's treatment at execution time.
