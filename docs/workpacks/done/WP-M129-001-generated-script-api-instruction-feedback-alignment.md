# WP-M129-001: Generated-Script API Instruction / Feedback Alignment

- Status: done
- Milestone: M129
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

## Goal

Audit the fixed provider-bound generated-script API instruction and the local
sanitized static-contract feedback after M127's unsupported OCP symbol failure.
Make the smallest offline-only alignment change that tells a script generator
to use installed OCP bindings and to avoid unavailable OCP symbols, while
retaining fail-closed local validation.

## Scope

- Locate every fixed provider-bound instruction that governs generated
  `build_sequence.py` imports and API usage for the reference-assisted path.
- Compare it against `build-script-api-v1` static rejection behavior for the
  M127 `OCP.STEPControl.STEPControl_STEPModelType` symbol.
- Make at most one compact instruction/feedback wording change; it may not
  contain local paths, raw STEP, reference scripts, prior provider responses,
  traces, report content, or credentials.
- Add deterministic local tests proving the fixed instruction includes the
  installed-binding/unsupported-symbol boundary and that a rejected script
  preserves the existing sanitized contract classification.

## Compatibility constraints

Offline and credential-free only. Do not construct a provider, invoke a
provider, prepare a hosted checkpoint, alter model/endpoint/token/deadline,
change cards, manifests, splits, reference scripts, `wsl-bwrap`, gates or
report schema, retry M127, or reuse its evidence paths/budget/authorization.
`WP-TRG-005` remains deferred; this package neither activates it nor claims a
local wording check proves hosted model behavior.

## Acceptance

```powershell
uv run python -m pytest tests\test_agent_m3_provider_trace.py tests\test_harness_m2.py tests\test_observed_build_loop.py -q
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

Record how the focused tests separately cover provider-bound instruction
content, static API rejection, and absence of downstream execution inference.

## Status transition

Update `docs/workflow/status.md` first, then this workpack and active handoff.
Liaol must independently review the exact outbound wording and test evidence
before closure. If alignment requires a card, manifest, prompt-family, provider
or hosted-boundary expansion, stop and record the blocker.

## Out of scope

Provider quality claims, hosted re-entry, repair issuance, prompt tuning beyond
the fixed API-contract wording, runtime-card changes, held-out work, and
activation of `TRG-005`.

## Owner evidence (2026-08-11)

- The fixed provider-bound system instruction previously required installed OCP
  bindings but did not explicitly require module and symbol availability. It
  now says: use only installed OCP modules and symbols; never `cadquery`,
  `OCC.Core`, or invented OCP names. The wording contains no path, input,
  reference-script, provider-response, trace, report, or credential content.
- The existing local fail-closed rejection remains the authority. Its first
  sanitized repair hint now uses the same installed-module/symbol boundary;
  the exact M127 symbol continues to classify as `unsupported_ocp_symbol`
  before executor invocation.
- Added deterministic assertions that the fixed instruction reaches the
  fake-provider system message and that an M127-symbol rejection has no
  executor call, provenance control, or downstream geometry inference.
- Acceptance passed: the focused provider-trace, harness, and observed-build
  suites passed 60 tests in 184.01 seconds; Ruff, governance audit, and
  `git diff --check` passed. No provider was constructed or requested.

## Review required

Liaol's independent G2 review must confirm that the new fixed instruction and
sanitized repair hint remain within the frozen outbound boundary, accurately
align with the fail-closed contract, and do not imply hosted quality or alter
any card, case, executor, or provider authority.

## Independent G2 review and closure (2026-08-11)

Liaol independently approved closure. The review confirmed that the fixed
instruction and sanitized repair hint remain within the frozen outbound
boundary, correctly align with the fail-closed installed OCP symbol contract,
and introduce no card, case, executor, provider, or hosted authority change.
M129 closes as offline output-contract instruction/feedback alignment only; it
does not establish hosted quality, activate `TRG-005`, or authorize a retry.
