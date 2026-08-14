# WP-M127-001: Shared Hosted-Stability Re-entry

- Status: done
- Milestone: M127
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G3

## Goal

Select and complete one fresh, shared hosted-stability re-entry package that
either freezes an admissible stability-only hosted boundary and passes offline
preflight, or closes with an explicit blocked-by-hosted-stability conclusion.
This package may prepare a later authorization request, but it does not itself
grant provider authority.

## Scope

- Review the retained hosted-stability evidence chain, including M117, M118,
  the hosted terminal triage rules, and the current route documents, to decide
  whether one fresh re-entry boundary is supportable.
- Freeze exactly one stability-only development scope, outbound-content class,
  accounting bound, executor boundary, fresh policy namespace, and fresh
  report/monitor paths for a new shared re-entry candidate.
- Complete the read-only offline preflight for that candidate: hash/split
  checks, no-input executor check, non-secret provider configuration/model
  check, fake accounting validation, deadline/cap validation, and fresh-path
  validation.
- Record one interpretation table and authorization payload that separates
  lifecycle, script/API, sandbox/provenance, and downstream gate outcomes.
- If any prerequisite fails, stop and close this package with the exact unmet
  re-entry condition instead of issuing a request or widening scope.

## Attribution question and sampling intent

This package is intended to distinguish whether the project has enough retained
local evidence to justify one fresh shared hosted-stability re-entry candidate
after M118's terminal `missing_script_update` result. The expected information
gain is limited to re-entry admissibility and a preflight-ready hosted boundary;
it is not a new CAD capability claim, calibration estimate, or held-out route.
Stop after one frozen candidate boundary or one explicit blocked conclusion.

## Inputs

- `docs/workflow/status.md`
- `docs/workpacks/done/WP-M117-001-hosted-stability-reentry-evidence-review.md`
- `docs/workpacks/done/WP-M118-001-fresh-hosted-stability-preflight.md`
- `docs/workpacks/done/WP-M121-001-output-contract-trigger-clarification.md`
- `docs/architecture/v1/four-track-program-roadmap.md`
- `docs/architecture/v1/five-family-hosted-capability-roadmap.md`
- `docs/runbooks/hosted-campaign-charter-template.md`
- `docs/runbooks/hosted-terminal-triage.md`

## Code paths

- `src/**` or `tests/**` only if a fresh policy/checkpoint identity or focused
  fake-provider/preflight validation requires it
- `tools/check_governance.py`

## Docs to update

- `docs/workflow/status.md`
- this workpack
- active handoff under `docs/handoff/active/`
- one fresh preflight or route note under `docs/workflow/` or
  `docs/architecture/v1/` if this package freezes a new boundary
- `docs/workflow/hosted-experiment-registry.md` only after a later independently
  reviewed terminal run, not during offline preflight

## Trace/schema changes

No report schema, trace schema, or storage-layout change is planned by default.
If a fresh policy/checkpoint identity requires a contract update, record that
change explicitly before requesting authorization.

## Decision-package impact

- `decision_id`: hosted-stability re-entry after M118 terminal failure
- Q01/Q02 effect: no observable or constrained CAD-sequence hypothesis changes
  by default; this package freezes only the hosted boundary used to test shared
  stability.
- Q03/Q04 effect: may refine the re-entry stop rule, failure interpretation
  table, and fresh hosted accounting boundary.
- Evidence role: retained local evidence review plus one preflight-ready hosted
  boundary candidate
- Knowledge disposition: `no reusable knowledge` unless a later reviewed
  terminal run records a bounded hosted-stability conclusion

## Compatibility constraints

Default behavior remains offline and credential-free. Do not send data,
construct a provider, display credentials, prepare/monitor/execute a hosted
run, reuse M69/M72/M80/M89/M97/M118 reports or budgets, modify held-out scope,
change runtime guidance/card status, or infer provider/model/CAD quality from
retained terminal records. Any actual hosted request remains a separate step
that requires passing preflight, independent review, and explicit itemized user
authorization under this same bounded package.

## Acceptance

```powershell
uv run python -m pytest -m fast -q
uv run python -m pytest tests\test_agent_m3_provider_trace.py tests\test_observed_build_loop.py -q
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

The package must additionally record whether manifest/hash/configuration/
executor/accounting/deadline/fresh-path checks passed, and it must not request
authorization if any required check fails.

## Evidence reuse / guidance-card disposition

This package records `no reusable knowledge` unless it finishes with a frozen
offline preflight boundary that can later support one itemized authorization
request. Neither a retained card nor a retained successful request may be
promoted into runtime guidance or reusable hosted capacity here.

## Status transition

Update `docs/workflow/status.md` first, then this workpack and the active
handoff. If the package reaches a preflight-ready state, obtain Liaol's
independent G3 review before requesting itemized hosted authorization. If an
authorized run later occurs, record terminal evidence here, then obtain another
independent review before closure or archival.

## Closure rationale

Close only after recording either:

- a passed offline preflight with the exact frozen hosted boundary and review
  outcome; or
- a blocked conclusion with the exact unmet re-entry condition and retained
  evidence source.

This workpack does not close merely because a prior route document suggests a
future hosted direction.

## Out of scope

Direct activation of `TRG-005`; retries or in-place continuation of M118;
provider/model/endpoint expansion without fresh justification; held-out hosted
evaluation; family-scoped hosted campaigns; calibration claims; manifest/case
growth; dependency installation; or runtime promotion.

## Repair hypothesis and evaluation boundary

The working hypothesis is that M118's terminal `missing_script_update` should
be treated as a bounded output-contract or script-path failure class, not as a
general provider-lifecycle blocker. This package may test that hypothesis only
through retained evidence review and offline preflight controls. It cannot
claim that a future hosted pass would validate repair logic, card quality, or
portfolio readiness.

## Notes

- Shared hosted-stability remains the prerequisite route for later one-family
  hosted campaigns.
- For the four no-card families, completed M123 through M126 charters remain
  frozen preparation inputs only; they do not bypass this shared re-entry gate.

## Owner progress (2026-08-11)

- Added the fresh M127 command
  `reference-assisted-three-hole-plate-stability-reentry-smoke`, its focused
  CLI test, and frozen policy
  [`m127-three-hole-plate-stability-reentry-policy-v1.json`](../../corpus/registry/m127-three-hole-plate-stability-reentry-policy-v1.json)
  so the shared hosted-stability re-entry path has a fresh policy/accounting
  namespace rather than reusing M118.
- Recorded the owner-side offline preflight in
  [`m127-shared-hosted-stability-reentry-preflight.md`](../../workflow/m127-shared-hosted-stability-reentry-preflight.md).
  It freezes the M127 destination/model, egress class, development scope,
  request bound, token cap, deadline, secure executor boundary, and fresh
  report/monitor paths.
- Owner validation passed for the touched governance/doc surfaces and focused
  code paths: governance audit passed; Ruff passed in the repo virtualenv; the
  fresh M127 fake-provider `prepare -> execute` path reached terminal
  `completed` with `2/2` accounting under the M127 policy; and a separate
  local no-input `wsl-bwrap` replay of the checked-in `three_hole_plate`
  reference script passed sandbox/provenance and all existing geometry gates.
- Before the authorized terminal execution below, no hosted provider had been
  constructed and no hosted request had been issued. The package received
  Liaol's independent G3 review approval on 2026-08-11. The
  review confirmed the fresh M127 identity and paths, frozen request boundary,
  owner-side fake-accounting and no-input executor evidence, and the bounded
  interpretation/non-inference. The later itemized user authorization payload
  remains required and has been drafted in
  [`m127-shared-hosted-stability-reentry-preflight.md`](../../workflow/m127-shared-hosted-stability-reentry-preflight.md)
  . No hosted provider has been constructed and no hosted request issued.

## Authorized terminal execution (2026-08-11)

- Liaol approved the itemized M127 authorization boundary after the independent
  preflight review. The authorized execution used the fresh report path
  `data/corpus-runs/m127-three-hole-plate-stability-reentry.json` and reached
  terminal `completed` with `requests_used = 2` and `requests_remaining = 0`.
- The lifecycle completed within the frozen 300-second request deadline: the
  final provider response completed at 47.819 seconds after execution start;
  total end-to-end time was 49.231 seconds. This is not a timeout or lifecycle
  failure.
- The second generated script was rejected by the local build-script API
  contract before sandbox execution because line 8 imported unavailable
  `STEPControl_STEPModelType` from `OCP.STEPControl`. The terminal class is
  `script/API failure`; no output STEP was created.
- Sandbox/provenance and downstream geometry, semantic, and editability gates
  are `not evaluated` for this run because execution was contract-rejected.
  The run does not establish provider-wide stability, CAD capability, card
  efficacy, or readiness for another track.
- This M127 budget and report are consumed and terminal. Do not retry or repair
  in place. The next required step is Liaol's independent G3 terminal review,
  then a separately selected fresh package according to hosted terminal triage.

## Independent terminal G3 review and closure (2026-08-11)

Liaol independently approved closure after reviewing the authorized boundary,
terminal checkpoint, and owner record. The review confirmed fresh M127
accounting and report identity, exact `2/2` consumption, completion within the
frozen provider deadline, the static script/API classification, absence of
retry/repair, and `not evaluated` treatment for sandbox/provenance and
downstream gates. M127 closes as a terminal script/API failure. It grants no
provider-lifecycle, model, card, geometry, family-campaign, or reusable hosted
capacity claim. The next selected package is M128, an offline-only generated-
script OCP contract remediation.
