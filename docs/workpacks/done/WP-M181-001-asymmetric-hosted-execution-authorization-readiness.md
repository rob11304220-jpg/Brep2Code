# WP-M181-001: Asymmetric Hosted Execution Authorization Readiness

- Status: done
- Milestone: M181
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G3

## Goal

Bring the fixed M179/M180 33-case asymmetric campaign to a fresh, independently
reviewed authorization-ready state, then stop and present the exact itemized
egress authorization.  This package issues no provider request.

## Scope

- Revalidate the M175 cohort, M179 inherited hashes, existing zero-request
  dual checkpoint admission, `wsl-bwrap` availability, and DeepSeek local
  configuration availability without reading or displaying a credential.
- Recompute the fixed outbound boundary and authorization packet: destination
  `https://api.deepseek.com`; `deepseek-v4-pro`; 30 main Q01-only cases plus
  three annex Q01-plus-one-card cases; serial/no retry; 4096 output tokens;
  120-second request deadline; 102 completion slots; 69 HTTP requests; and
  M179 report/monitor identities.
- Run only offline preflight/admission commands and audits, record sanitized
  evidence, and obtain Liaol's independent G3 review.
- Present the exact user authorization text after review.  Stop before any
  provider construction, credential access, checkpoint authorization mutation,
  or request.

## Decision-package impact

- Hypothesis ID: not applicable; fixed hosted-execution authorization readiness.
- Q01--Q04: revalidate the already frozen Q01/card/Q02/Q03/Q04 boundary only.
- Evidence role: local admission evidence; it establishes neither model quality
  nor a provider result.
- Counterexample: hash, checkpoint, executor, configuration-presence,
  accounting, identity, or packet-boundary drift rejects the authorization
  request.
- Stop rule: independent review, any failed preflight, frozen-input drift, or
  a request to alter egress/content/cohort/repair/model/deadline/budget.
- Adoption boundary: a passing packet permits only a user authorization
  request; it does not itself authorize provider construction or egress.

## Compatibility constraints

Offline and credential-safe.  A preflight may inspect configuration only to
return boolean presence/fixed-model validity; it must not print, persist, or
otherwise expose a credential or configuration value, construct a provider,
issue a request, change reports/monitors, access held-out assets, or change
cases, cards, prompts, model, token cap, deadline, repair/retry policy,
executor, Harness, or runtime behavior.

## Acceptance

- M175 and M179 audits plus `m179-asymmetric-campaign-admission` pass.
- Boolean-only local provider configuration and `wsl.exe` availability checks
  pass without exposing values.
- The authorization packet has one immutable hash and all itemized fields.
- Governance/diff checks pass and Liaol records independent G3 review.

## Owner completion boundary

Publish the passing sanitized preflight evidence and reviewed authorization
packet, then request the user's itemized egress authorization.  Stop there.

## Closure rationale

The M181 readiness packet, fresh admission, local preflight, and independent
review completed, and the user supplied the requested itemized authorization.
Before provider construction, M180's case-local early-stop behavior was found
incompatible with the user's complete-denominator requirement.  M182 is the
separately selected remediation; the M181 packet and authorization are not
reusable for it.

## Owner completion evidence

- `uv run python tools\audit_m175_asymmetric_qualification.py` passed: 30
  main rows, 10 mechanism groups, and three annex rows.
- `uv run python -m brep2code.cli m179-asymmetric-campaign-admission` passed:
  `fresh_execute_admission_candidate`, zero issued requests, 102 completion
  slots, and 69 provider HTTP requests.
- Boolean-only local checks passed: DeepSeek API-key configuration is present;
  no environment model/base-url override exists; `.env` model/base-url are the
  fixed value or default; and `wsl.exe` is available.  No value was printed or
  persisted, no provider was constructed, and no request was issued.
- Frozen authorization packet:
  `docs/corpus/knowledge/m181-asymmetric-hosted-authorization-packet-v1.json`,
  SHA-256 `1d6c84a2f41ac4467cbded2eeeb7682f5d1c03e66bc9285b64c827138a868a3c`.
- `uv run python tools\check_governance.py` and `git diff --check` passed.

## Review state

Owner-side M181 readiness is complete.  Await Liaol's independent G3 review of
the M179 admission evidence, boolean-only configuration check, executor,
packet hash, exact egress boundary, accounting, and absence of credential
exposure/provider construction/egress.  The review does not authorize egress.

Liaol approved the independent G3 review on 2026-08-14.  Review confirmed the
M179 zero-request admission evidence, boolean-only configuration check,
executor, packet hash, exact egress boundary, accounting, and absence of
credential exposure/provider construction/egress.  This approval does not
authorize egress.

## Permitted stop conditions

Independent review; any preflight/hash/checkpoint/configuration/executor
failure; frozen-input drift; or a required policy/runtime/provider change.

## Out of scope

Provider construction, credential access, egress, report authorization
mutation, hosted execution, result interpretation, retries, held-out use, and
the TRG-042 long-term lifecycle improvement.
