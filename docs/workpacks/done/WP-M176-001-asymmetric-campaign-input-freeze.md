# WP-M176-001: Asymmetric Campaign Input Freeze

- Status: done
- Milestone: M176
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

## Entry condition

M175 independently approved the 30-row no-card main cohort and three-role
card feasibility annex. The user explicitly selected this G2 freeze with
DeepSeek V4 Pro, 4096 output tokens, 120-second request deadline, serial
execution, no retries, and a 102-completion hard cap.

## Goal

Freeze all offline-verifiable campaign inputs and operational bounds before a
separately selected G3 preflight/execution package is considered.

## Scope

- Publish a hash-bound campaign specification for M175's two unpooled evidence
  products, including development inputs, annex guidance, provider/model,
  output cap, completion arithmetic, deadline, executor, fixed order, report
  and monitor identities, outbound-content boundary, and epoch-integrity stop
  rule.
- Add an offline audit that recomputes the selected development input hashes,
  cohort/annex identities, guidance hashes, arithmetic, path freshness, and
  no-input executor declaration without constructing a provider or reading an
  environment file.
- Reserve fresh, distinct report and monitor paths as identifiers only; do not
  create a running checkpoint or consume capacity.

## Compatibility constraints

Offline and credential-free. Do not read `.env`, construct a provider, issue a
request, create/reuse report checkpoints, execute a campaign, access held-out
assets, change cases/cards/Harness/repair/runtime/provider behavior, or create
retrieval. The frozen maximum is 102 completions: main `30 × 3` plus annex
`3 × 4`; no retry or case substitution is allowed.

## Acceptance

Define focused offline freeze/audit coverage, then run relevant tests, Ruff,
runtime-guidance and governance audits, and `git diff --check`. Publish Liaol's
independent G2 review of the frozen bounds and egress boundary.

## Owner completion boundary

Publish the immutable freeze specification and passing offline audit evidence,
then obtain Liaol's independent G2 review. A G3 package is still not selected
or authorized by this closure.

## Owner completion evidence

- Published `docs/corpus/knowledge/m176-asymmetric-campaign-freeze-v1.json`.
  It binds the approved M175 dossier; the 30-case and three-case canonical
  metadata fingerprints; DeepSeek V4 Pro; 4096 tokens; 120-second deadline;
  serial/no-retry execution; 90 + 12 = 102 completion cap; `wsl-bwrap`
  no-input executor; outbound boundaries; stop classes; and four fresh report
  / monitor identities.
- Added `tools/audit_m176_campaign_freeze.py`. It validates all of those
  offline without reading `.env`, constructing a provider, creating a report,
  or sending data.

## Validation evidence

| Command | Terminal result |
|---|---|
| `uv run python tools\audit_m176_campaign_freeze.py` | prepared_offline: 30 main, 3 annex, cap 102 |
| `uv run python -m ruff check tools\audit_m176_campaign_freeze.py` | passed |
| `uv run python tools\audit_m175_asymmetric_qualification.py` | passed: 30 main rows, 3 annex rows |
| `uv run python tools\audit_runtime_guidance.py` | passed: live index has 5 cards |
| `uv run python tools\check_governance.py` | passed |
| `git diff --check` | passed; existing LF/CRLF warnings only |

## Review state

Owner-side freeze is complete. Await Liaol's independent G2 review of input
fingerprints, provider/model declaration, 102-cap arithmetic, 120-second
deadline, serial/no-retry rule, no-input executor, fresh report identities,
outbound boundary, and explicit absence of credentials/provider construction.

Liaol approved the independent G2 review on 2026-08-14. The frozen input
fingerprints, provider/model declaration, 102-cap arithmetic, deadline,
executor, report identities, outbound boundary, and credential-free offline
state were accepted. This approval does not grant hosted egress.

## Closure rationale

M176 closes because every offline-verifiable campaign input and operational
bound is frozen and independently reviewed. A fresh G3 package, successful
preflight, independent review, and itemized user authorization remain required
before any provider construction or request.

## Status transition

Update `status.md` first, then move this workpack to `done/` and archive the
handoff. Do not activate G3 without a new explicit user selection.

## Permitted stop conditions

Independent review, selected input/guidance hash drift, insufficient secure
executor/preflight inputs, report identity collision, or any required provider,
credential, hosted, case, manifest, Harness, or repair change.

## Out of scope

Provider configuration validation, `.env`, hosted preflight/execution,
authorization, cost purchase, report checkpoint creation, retries, prompt/model
adjustment, case/card expansion, held-out use, and terminal review.
