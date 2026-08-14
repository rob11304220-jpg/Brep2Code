# WP-M79-001: Historical Contract Drift Diagnosis

- Status: done
- Milestone: M79
- Owner: Codex
- Reviewer: Liaol
- Risk tier: G2

## Goal

Produce a deterministic, privacy-preserving comparison between the current M72
request contract and the available earlier hosted evidence. The result must
identify structural equivalence, observed difference, and irreducible unknowns
without replaying a provider request.

## Scope

- Compare case/input and manifest identities; provider/model/endpoint;
  non-streaming payload fields; system-instruction version or hash;
  observation policy/version, length and hash; deadline; executor; request
  accounting; report schema; and lifecycle-event taxonomy.
- Use only committed contracts plus sanitized local reports/traces already in
  scope. Do not recover, print, retain or infer raw prompts, responses,
  credentials or headers.
- Write a reviewed `reproduction-profile-v1` that freezes every observable
  field required for M80 and marks unavailable historic fields as `unknown`.

## Stopping rule

Stop at missing, malformed or incomparable evidence: record `unknown` rather
than synthesizing equivalence. M79 does not select a provider, issue a request,
change a prompt, alter a manifest, or authorize M80.

## Acceptance

```powershell
uv run python -m pytest tests\test_agent_m3_provider_trace.py tests\test_observed_build_loop.py -q
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

## Closure gate

An independent reviewer confirms the matrix distinguishes evidence from
unknowns and that the M80 profile contains no raw outbound content or authority
to reuse an old budget/report.

## Out of scope

Hosted requests, prompt rewrite, model/endpoint comparison, retry, CAD output
changes, causal claims about a timeout, and held-out evaluation.

## Activation record

- Liaol selected M79 on 2026-08-10. This workpack is the offline diagnostic
  requested before considering M80; it grants no provider, prompt, manifest,
  runtime, or hosted authority.
- The initial source and retained-evidence comparison is recorded in
  [`m79-historical-contract-drift-diagnosis.md`](../../workflow/m79-historical-contract-drift-diagnosis.md).
  Its `reproduction-profile-v1` is a proposal for a later preflight, not an
  authorization or a reusable request budget.

## Owner acceptance record

- The offline source/evidence matrix and `reproduction-profile-v1` distinguish
  source-level equivalence, observed case/report differences, and unavailable
  historical fields without recovering or printing raw outbound content.
- 2026-08-10 acceptance commands passed: focused provider/observed-loop tests
  (21 passed in 44.85s), `uv run python -m ruff check .`,
  `uv run python tools\check_governance.py`, and `git diff --check`.
- Pending independent review: Liaol must confirm that unknown historic fields
  remain unknown and that the profile grants no M80 or hosted authority.

## Independent review and closure

- Reviewer: Liaol
- Outcome: approved on 2026-08-10. The review accepts the evidence/unknown
  separation and confirms that `reproduction-profile-v1` contains no reusable
  report, budget, prompt content, or hosted authority.
- Closure rationale: M79 is complete as an offline structural diagnosis. It
  authorizes only the subsequent M80 read-only preflight; M80 still requires a
  fresh itemized G3 authorization before any provider request.
