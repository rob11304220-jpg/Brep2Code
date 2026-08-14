# WP-M97-004: M97-003 Development Terminal Attribution Review

- Status: done
- Milestone: M97-004
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

## Goal

Audit the six M97-003 development conditions offline and classify the nominal
baseline failure from retained local evidence. Produce a review-ready evidence
package without issuing a request, changing a card/prompt, retrying capacity,
or reading held-out case inputs.

## Scope

- Inspect the terminal report plus the six development record revisions for
  execution, OCP API contract, gates, output/probe, provenance and sanitized
  provider lifecycle evidence.
- Compare actual outbound-context attestations and card/baseline boundaries,
  especially the nominal pair.
- Classify nominal baseline as a trace-supported local failure family, or
  explicitly `inconclusive` when retained evidence cannot distinguish causes.
- Write a compact content-free review artifact and update module/workflow docs
  only as needed to link the evidence.

## Attribution question and sampling intent

The question is whether the nominal baseline failure is attributable to a
retained local failure family rather than the fixed card/no-card treatment.
All six already-issued development conditions are the entire sample; stop once
their terminal artifacts are classified. No new samples, provider requests or
counterfactual reruns are permitted.

## Inputs

- `data/corpus-runs/m97-003-reference-guided-through-hole-development-calibration.json`
- six `data/records/m97-{card,baseline}-param_reference_guided_through_hole_development_*` records
- M97-003 policy, preflight and completed workpack

## Code paths

- Offline audit helper under `tools/` only if a deterministic compact summary
  cannot be produced from existing artifacts.

## Docs to update

- `docs/workflow/status.md`, this workpack and active handoff
- `docs/architecture/v1/four-track-program-roadmap.md` only if the route or
  evidence boundary changes; do not treat the result as M98 authority.

## Trace/schema changes

Additive, content-free local audit summary only. Do not copy provider payloads,
responses, reference scripts, raw STEP, local absolute paths or credentials
into tracked artifacts.

## Decision-package impact

- `decision_id`: M93/M94 reference-guided through-hole parameter variation.
- Q01/Q02 effect: none; audit verifies the already-frozen measured-fact path.
- Q03/Q04 effect: classifies terminal evidence without altering gates or repair.
- Evidence role: development-only attribution and negative-control evidence.
- Knowledge disposition: counterexample or no reusable knowledge; no card,
  runtime-retrieval or training promotion.

## Compatibility constraints

Default execution remains offline and credential-free. M97-003's report,
monitor, capacity, policy, card, prompt, model, endpoint, gates and case split
are immutable. M98 and all held-out case inputs are out of scope.

## Acceptance

```powershell
uv --cache-dir .uv-cache run python -m pytest tests\test_m96_reference_guided_through_hole_observation.py tests\test_observed_build_loop.py -q
uv --cache-dir .uv-cache run python -m ruff check .
uv --cache-dir .uv-cache run python tools\check_governance.py
git diff --check
```

Liaol independently reviews the six-condition summary, attribution boundary,
source-leak boundary and conclusion before closure.

## Evidence reuse / guidance-card disposition

Record only a counterexample or `no reusable knowledge`. This audit cannot
promote or mutate the existing card.

## Status transition

On closure update `status.md` first, then this workpack and handoff. Record the
review outcome and archive the workpack; no later workpack is automatically
selected.

## Closure rationale

Record the compact audit artifact, validation output and Liaol's independent
review. A classified nominal failure does not justify retry or held-out work.

## Owner audit record (2026-08-11)

[`m97-004-development-terminal-attribution-review.md`](../../workflow/m97-004-development-terminal-attribution-review.md)
records the six-condition audit. The nominal baseline is classified as a
generated-script OCP constructor-arity error: static import/API checks passed,
but runtime execution called `BRepPrimAPI_MakeBox` with an unsupported six
numeric-argument signature. It is ready for Liaol's independent G2 review.

Validation: the required M96/observed suite passed 42 tests in 138.268 seconds;
Ruff, governance audit and `git diff --check` passed.

## Independent G2 review and closure (2026-08-11)

Liaol approved closure after independently reviewing the six-condition summary,
terminal report accounting, nominal constructor-arity evidence and conclusion
boundary. The record remains a development-only API-use counterexample; no
retry, capacity reuse, card/prompt adjustment, held-out inspection or M98
transition is authorized.

## Out of scope

Provider request, retry, repair, capacity/report reuse, card/prompt/model
change, M98, held-out inspection, manifest mutation, runtime retrieval,
training input, external data or generic model ranking.

## Repair hypothesis and evaluation boundary

The retained nominal baseline trace may reveal a local script/API/sandbox/gate
failure family. This audit tests only that attribution hypothesis from terminal
evidence; it cannot separate stochastic model behavior from an unrecorded
counterfactual or establish a treatment effect.
