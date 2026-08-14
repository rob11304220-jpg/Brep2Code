# WP-M44-001: First-Pass Runtime-Contract Held-Out Evaluation

- Status: done
- Milestone: M44
- Owner: Codex
- Reviewer: Liaol (user)
- Risk tier: G3

## Goal

Evaluate the frozen M43 runtime-contract policy once on held-out
`abc_v00_00000031`, using the path-sanitized probe-summary projection.

## Scope

- Complete a fresh preflight for the one held-out input and a new report path.
- Run DeepSeek `deepseek-v4-pro` through `wsl-bwrap` with first pass and at
  most one repair, no more than two requests, and a 120-second request deadline.
- Write a sanitized held-out review without changing the policy, context,
  gates, provider, model, executor, or sample.

## Compatibility constraints

- Only `file_name`, format/unit, bbox, topology counts, area, volume, case ID,
  and the M42 runtime contract may leave the workspace; raw STEP and local
  absolute paths may not leave it.
- No helper, IR, SDK, gate, manifest, asset, prompt expansion, or sample change.
- Existing schema-v3 reports and gate outcomes remain authoritative.

## Authorization record

The user explicitly authorized this held-out run on 2026-08-08: case
`abc_v00_00000031`; DeepSeek `deepseek-v4-pro`; path-sanitized bounded summary
and runtime contract; `wsl-bwrap`; first pass plus at most one repair; at most
two requests; 120 seconds per request.

## Acceptance

- Input hash, manifest membership, offline sandbox control, non-secret provider
  configuration, executor, request capacity, and unused report path pass fresh
  preflight.
- The completed report records one case and no more than two requests.
- The review states the evidence funnel and does not combine held-out outcome
  with development into a benchmark.

## Evidence

Fresh preflight passed with SHA-256
`b3869dc65446bfdd6d7c0136796f6b484e4a0661e2149bc9320033c60a7eb17c` and an
unused report path.  The completed held-out report used 1/2 requests: its
first-pass script and all existing gates passed, so repair did not run.  The
request trace confirms that the ADR-0046 projection omitted the local absolute
input path.  See `docs/architecture/v1/m44-first-pass-runtime-contract-held-out-review.md`.

## Closure rationale

The independent reviewer accepted the split-preserving conclusion: the held-out
pass is a STEP round-trip and execution-compatibility result, not a B-Rep-to-CAD
reconstruction success.  The generated script reads `/input/model.step` and
writes the same geometry to `output/model.step`, so existing bbox, volume, and
topology gates cannot establish modeling provenance or editability.  No further
provider request is selected.  Follow-up, if chosen, must design a bounded Q03
reconstruction-provenance gate.

## Out of scope

Any additional provider request, development retry, provider/model comparison,
raw response retention, external download, or production policy promotion.
