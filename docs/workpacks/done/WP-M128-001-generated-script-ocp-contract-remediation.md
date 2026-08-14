# WP-M128-001: Generated-Script OCP Contract Remediation

- Status: done
- Milestone: M128
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

## Goal

Determine whether the existing generated-script API contract and its sanitized
feedback classify M127's unavailable OCP symbol precisely and fail closed;
then make the smallest offline-only contract or feedback remediation needed to
prevent that specific unsupported-symbol class from being ambiguous.

## Scope

- Reproduce M127's static rejection with a deterministic local fixture using
  `OCP.STEPControl.STEPControl_STEPModelType`.
- Inspect the installed OCP binding surface and generated-script contract to
  determine whether the symbol is already explicitly rejected, only implicitly
  rejected, or misclassified.
- Add or tighten the smallest contract rule and sanitized feedback needed for
  an unambiguous `unsupported_ocp_symbol` result; preserve fail-closed
  behavior.
- Add focused local regression tests that distinguish static script/API
  rejection from sandbox/provenance and geometry outcomes.
- Record the retained M127 terminal evidence as the trigger for this local
  remediation, without changing its interpretation or report.

## Compatibility constraints

This is offline, credential-free G2 work only. Do not construct a provider,
send data, prepare or execute a hosted run, retry M127, reuse its accounting
or paths, change model/endpoint/deadline/token policy, modify manifests,
splits, cards, prompts, reference scripts, `wsl-bwrap` policy, geometry gates,
or held-out scope. `WP-TRG-005` remains deferred: M128 is a narrow local
contract remediation, not its activation or a claim that local tests establish
hosted quality.

## Inputs

- `docs/workpacks/done/WP-M127-001-shared-hosted-stability-reentry.md`
- `docs/workflow/hosted-experiment-registry.md`
- `docs/runbooks/hosted-terminal-triage.md`
- `docs/workpacks/deferred/WP-TRG-005-output-contract-and-repair-correctness.md`
- generated-script API contract, static validation, and focused observed-build
  loop tests under `brep2code/**` and `tests/**`

## Acceptance

```powershell
uv run python -m pytest tests\test_harness_m2.py tests\test_agent_m3_provider_trace.py tests\test_observed_build_loop.py -q
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

Before acceptance, record how focused tests separately cover static API
classification, no sandbox execution/provenance claim after rejection, and no
downstream geometry inference.

## Status transition

Update `docs/workflow/status.md` first, then this workpack and active handoff.
Obtain Liaol's independent G2 review before closure. If remediation cannot be
made without widening prompts, cards, policy, provider or hosted scope, stop
and record the exact blocker rather than widening this package.

## Out of scope

Hosted re-entry; repair-loop issuance; prompt optimization; provider/model
changes; case growth; card promotion; runtime guidance changes; held-out
evaluation; CAD capability claims; and activation of `TRG-005`.

## Selection rationale

M127 completed its frozen lifecycle and was terminalized before sandbox
execution by a generated-script static OCP symbol violation. Hosted terminal
triage permits a fresh output-contract remediation package; M128 selects only
that offline branch and makes no inference from M127 beyond the fixed failure
class.

## Owner evidence (2026-08-11)

- The existing static contract already explicitly classifies
  `OCP.STEPControl.STEPControl_STEPModelType` as `unsupported_ocp_symbol`.
  No production contract change was required or made; the remediation is a
  focused regression coverage addition rather than a relaxation of the API
  boundary.
- Added a deterministic M127-symbol fixture in `tests/test_harness_m2.py`.
  It asserts the exact sanitized violation, no executor calls, contract-rejected
  termination, no provenance absent-input control run, and skipped bbox,
  volume, and topology gates. This keeps static API failure distinct from
  sandbox/provenance and downstream geometry evidence.
- Acceptance passed: `tests/test_harness_m2.py`,
  `tests/test_agent_m3_provider_trace.py`, and
  `tests/test_observed_build_loop.py` passed 60 tests in 186.09 seconds; Ruff,
  governance audit, and `git diff --check` also passed.
- The package remains offline. No provider was constructed, no request issued,
  and no M127 evidence path, budget, or authorization was reused.

## Review required

Liaol's independent G2 review must confirm that the exact fixture matches the
M127 terminal class, the contract remains fail-closed, no executor/provenance
or downstream-gate inference was introduced, and no hosted scope changed.

## Independent G2 review and closure (2026-08-11)

Liaol independently approved closure. The review confirmed the regression
fixture exactly matches M127's static OCP symbol class, preserves the existing
fail-closed contract, records no executor/provenance/downstream-gate inference
after rejection, and makes no hosted-scope change. M128 closes as a narrow
offline regression-coverage remediation. It does not activate `TRG-005` or
grant any provider, retry, repair, family-campaign, or reusable hosted
authority.
