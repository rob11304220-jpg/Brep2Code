# WP-M145-001: Case-Evidence Mechanism and Difficulty Report

- Status: done
- Milestone: M145
- Owner: Codex
- Reviewer: not required (G1)
- Risk tier: G1

## Entry condition

M143 is independently reviewed. The user selected a documentation-only report
before considering any information-architecture consolidation.

## Goal

Publish one source-linked, human-readable matrix that describes the current
case evidence by design intent, bounded kernel/sequence mechanism,
entity-reference stability, dependency, parameter/split role, evidence
maturity, admission risk, and current decision gap.

## Scope

- Derive a read-only matrix from existing case portfolio, registry, knowledge
  operation/observable/execution units, decision packages, coverage matrix,
  and M142/M143 admission evidence.
- Explain why difficulty is multi-axis rather than a scalar tier, and identify
  the authority location for every type of statement.
- Identify the precise limitations of the present distributed documentation and
  register a later deferred trigger for a separate information-architecture
  workpack. Do not implement that architecture in M145.

## Compatibility constraints

This is documentation only. Do not modify fixtures, case metadata, registry,
split, manifest, Harness, runtime resources, provider/model configuration,
training data, or hosted scope. Do not inspect or execute held-out fixtures.

## Acceptance

```powershell
uv run python tools\check_governance.py
git diff --check
```

## Owner completion boundary

Publish the matrix/report with source links, boundaries, and deferred
architecture trigger; run acceptance checks.

## Implementation evidence

- Published `docs/corpus/case-evidence-mechanism-difficulty-report-v1.md`.
  It gives the six-axis vocabulary, a mechanism/design-intent matrix, the M143
  profile count snapshot, difficultly-versus-evidence examples, source-of-truth
  map, and a precise account of the distributed-expression gap.
- Registered `WP-TRG-030-development-evidence-information-architecture.md`.
  ADR-0074 requires a future user-selected G2 workpack to design any
  crosswalk/schema; M145 deliberately does not implement it.

## Closure

The documentation-only matrix and deferred architecture route were published
on 2026-08-12. Governance audit and `git diff --check` passed. M145 changes no
case, manifest, runtime, provider, or hosted authority.

## Permitted stop conditions

Review; a conflict among authoritative documentation that requires a separate
reconciliation; need for fixture/held-out access or any behavior change; or a
reproducible documentation validation blocker.

## Status transition

Update `docs/workflow/status.md` first, then this workpack and active handoff.
On closure, archive M145 and leave all successor triggers deferred until the
user selects one.

## Out of scope

Information-architecture implementation, case admission, runtime projection,
case production, generic difficulty claims, provider use, and hosted execution.
