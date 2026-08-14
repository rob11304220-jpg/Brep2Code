# WP-M19-003: Bounded Runtime Guidance Retrieval Integration

- Status: done
- Milestone: M19
- Owner: Codex
- Reviewer: Liaol
- Risk tier: G2

## Goal

Integrate a versioned, bounded experience-card retrieval path into one runtime
revision only after M19-002 demonstrates development-split benefit without
gate regressions.

## Entry criteria

- M19-002 is completed and its review explicitly selects this workpack.
- The reviewed retrieval contract fixes card-index version/hash, top-k limit,
  request schema, response size limit, visibility boundary, and failure mode.
- A threat/boundary review confirms that no secrets, development governance
  documents, ignored traces, or unrestricted file paths are exposed.

## Scope

- Add one explicit, read-only Harness tool or selected resource interface that
  returns only matching card fields needed for the current revision.
- Keep card access opt-in and versioned per record/revision; record the index
  hash and returned card IDs in trace metadata.
- Add deterministic tests for top-k bounds, unavailable/invalid index failure,
  source-link preservation, and the no-card baseline.

## Trace/schema changes

This workpack may extend the runtime tool contract and trace metadata only.
It must update the relevant contract and module documentation before code is
merged.  It must not change the meaning of existing gates or provider reports.

## Compatibility constraints

Default runtime behavior remains unchanged when no guidance bundle/tool is
selected.  Cards stay read-only and cannot bypass sandbox, tool schemas,
probes, gates, provider authorization, or output validation.  No hosted call
is authorized by this workpack.

## Acceptance

- The runtime can retrieve at most the preregistered top-k card subset for one
  explicit revision and records exactly which card IDs were returned.
- No-card invocations preserve current behavior and tests.
- Invalid or unavailable guidance fails closed without exposing broad files.
- Development-only evaluation is repeated against M19-002's frozen baseline;
  any gate regression rejects integration.
- A review explicitly decides whether separate held-out validation is justified.

## Status transition

Update `docs/workflow/status.md`, this workpack, active handoff, contracts,
module docs, the guidance runbook, and ADRs if the runtime boundary changes.

## Owner acceptance record

- Added `GuidanceCardBridge`, an explicit revision-scoped tool that is absent
  by default and returns at most one compact, selected card. It verifies frozen
  index/card hashes, permits only declared roles, preserves source links, and
  never searches a directory or exposes raw case assets.
- Integrated explicit bundle/call inputs into `ManualHarness.run`. Its additive
  signal-bundle metadata and `guidance_calls.jsonl` trace retain only revision
  ID, index hash, returned card ID, and compact status/error fields.
- Invalid, unavailable, drifted, or undeclared index/card state fails closed;
  no-card invocations preserve the existing runtime behavior and gates.
- 2026-08-10 owner checks passed: 6 focused bridge tests; repeated M19-002
  fixed controls (3/3 selection/readability/gate pass); fast suite (64 passed,
  136 deselected); full suite (200 passed in 186.45s); full Ruff; governance
  audit; and `git diff --check`.
- Pending independent G2 review by Liaol: verify the response/trace boundary,
  default no-card path, failure modes, and that no held-out/hosted claim or
  broader file access has been introduced.

## Independent review and closure

- Reviewer: Liaol
- Outcome: approved on 2026-08-10.
- Closure rationale: The opt-in revision-scoped interface preserves the no-card
  default, verifies its fixed bundle, fails closed, and records bounded trace
  metadata without exposing development assets. M85 remains a separately
  authorized G3 smoke; no hosted request has been made.

## Out of scope

Hosted prompt comparison, automatic card promotion, model fine-tuning, broad
repository search, loading development documents, and held-out use without a
separate selected workpack and authorization where applicable.
