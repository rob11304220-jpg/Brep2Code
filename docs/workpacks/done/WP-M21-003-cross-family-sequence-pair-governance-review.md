# WP-M21-003: Cross-Family Sequence-Pair Governance Review

- Status: done
- Milestone: M21
- Owner: Codex

## Goal

Close the M20/M21 development documentation loop and assess whether the two
completed deterministic-oracle families justify a separately selected,
restricted M21 governance-promotion workpack. This review does not promote
any asset.

## Result

- Completed the M20/M21 evidence comparison and documented its bounded result:
  both families satisfy the frozen catalog, deterministic-producer,
  three-layer-audit discipline; M21 independently exercises a second composite
  profile dependency and semantic anti-degeneration checks.
- Updated durable document governance to distinguish dynamic status, task
  evidence, long-lived decisions/constraints, operating procedures, code
  documentation, case governance, and research links.
- Recorded retain/defer/blocked dispositions for every existing backlog item.
- Created only a backlog proposal for M21-004. The three `offset_rounded_slot`
  assets remain experimental and absent from the registry and every manifest.
- `uv run python tools/audit_case_library.py --replay` passed for 42 records;
  `git diff --check` passed.

## Evidence reuse / guidance-card disposition

No runtime guidance card. This is development-governance evidence, not a
repeated direct runtime mechanism.

## Out of scope

M21 asset promotion, new ADR acceptance, case-library registration, executable
manifest changes, external dataset acquisition, hosted execution, provider
requests, model training, runtime retrieval, parser expansion, helper, or IR.
