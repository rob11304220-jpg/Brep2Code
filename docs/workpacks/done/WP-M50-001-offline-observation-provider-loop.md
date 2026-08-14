# WP-M50-001: Offline Observation-to-Provider Loop and Semantic Fixes

- Status: done
- Milestone: M50
- Owner: Codex
- Reviewer: Liaol
- Risk tier: G2

## Goal

Make the M48 observation contract usable by an offline fake provider: bounded,
path-free Q01 envelopes form the sole provider context; the returned script
runs with no original STEP mount; the Harness records Q03/Q04 feedback. Repair
the per-session call-budget and provenance-report semantics found in review.

## Scope

- Enforce the eight-call budget independently for each observation session.
- Add an offline fake-provider observation/build runner with sanitized provider
  trace, no-input execution, transcript trace, and resulting signal bundle.
- Project a provenance eligibility field separately from geometry health in
  corpus results; retain existing `status` semantics.
- Add focused tests and test markers/selections only if necessary for a
  bounded fast/standard/sandbox feedback interface.

## Compatibility constraints

Offline and credential-free only. Existing `run`, `repair`, `corpus`, provider
defaults, manifests, gates, and hosted policy remain unchanged. The reference
script used by a fake provider is a local test control and is never provider
context. No DeepSeek construction or network request is allowed.

## Trace/schema changes

Additive observation-loop trace fields and additive corpus provenance
eligibility only. Update the tool bridge, provider trace, signal bundle, and
case-corpus contracts if their observable schemas change.

## Decision-package impact

- `decision_id`: `q01-q02-observation-build-separation-v1`.
- Q01/Q02 effect: implements offline tool-context-to-no-input-build handoff.
- Q03/Q04 effect: reports provenance eligibility separately; preserves gates.
- Evidence role: tool-boundary, no-input, and fake-provider regression evidence.
- Knowledge disposition: no reusable modeling knowledge.

## Acceptance

```powershell
uv run python -m pytest tests\test_agent_m3_tool_bridge.py tests\test_observed_build_loop.py tests\test_harness_m2.py tests\test_corpus_m4.py -q
uv run python -m pytest
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

## Acceptance evidence and interpretation

- Focused post-change regression: `26 passed in 24.78s` for governance,
  bridge, observed-build, and Harness tests; the original larger focus that
  included corpus tests exceeded the interactive 64-second command limit, so
  the full suite was run persistently.
- Final complete offline suite: `160 passed in 138.80s (0:02:18)`; no network
  provider was constructed or called.
- `uv run python -m ruff check .`, `uv run python tools\check_governance.py`,
  and `git diff --check` passed.

The fake provider now receives a bounded, path-free and filename-free M48
transcript, and its replacement script executes with no original-input mount.
This proves the local Harness information flow and traceability boundary, not
the quality of a hosted model or a general reconstruction claim. Geometry
health remains separate from `reconstruction_eligible`; a provenance-unknown
result cannot be interpreted as independently reconstructed.

The final suite's 138.80-second duration confirms that test feedback
segmentation is needed, but the correct fast/standard/sandbox partition should
be selected from measured duration data in a separate bounded G2 workpack,
rather than marking tests heuristically inside this semantic-change workpack.

## Proposed next direction for reviewer

If the reviewer accepts this scope and evidence, select a narrowly bounded G3
workpack for one existing self-authored case: secure `wsl-bwrap` execution,
one explicitly authorized provider/model request, fixed observation calls,
fixed deadline and request budget, and no repair or split expansion. Keep a
test-profiling/selection G2 workpack as the next quality-engineering route;
it does not block the semantic correctness of this offline loop.

## Closure rationale

Liaol approved the scope, evidence, and provenance/reporting interpretation on
2026-08-08. M50 closes with 160 passing offline tests and no hosted request.
The selected successor is a separately governed, single-case G3 secure smoke;
its provider request remains unauthorized until its own preflight completes.

## Status transition

Record acceptance output and Liaol's independent review. Update status first,
then this workpack and its handoff; archive on closure.

## Out of scope

Real provider use, hosted evaluation, prompt-policy experiment, external data,
manifest change, CAD SDK/IR, or a model-quality claim.
