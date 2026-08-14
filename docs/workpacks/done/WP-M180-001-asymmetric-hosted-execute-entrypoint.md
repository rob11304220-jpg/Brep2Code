# WP-M180-001: Asymmetric Hosted Execute Entrypoint

- Status: done
- Milestone: M180
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G3

## Goal

Add the sole fixed M179 DeepSeek execute entrypoint. It must revalidate fresh
admission before provider construction, accept no policy overrides, and remain
offline-testable with fakes; this package issues no hosted request.

## Scope

- Wire only the frozen M179 identities to `deepseek-v4-pro`, `wsl-bwrap`, 4096
tokens, 120-second deadline, serial/no retry, 33 cases and 69-request ceiling.
- Fail closed on authorization absence, checkpoint/hash/identity drift, and
non-frozen bounds; add fake-only tests and documentation.

## Boundaries

Outbound candidate: bounded Q01 facts for 30 main cases; those facts plus one
hash-bound returned card for three annex cases; destination `api.deepseek.com`.
No egress, credential disclosure, provider request, scope/policy change, or
held-out access occurs in this package.

## Acceptance

Focused fake tests, Ruff, full offline pytest, governance/diff checks, and
Liaol independent G3 review pass. A later user authorization remains required.

## Owner completion boundary

Publish offline evidence and await independent review; do not request or issue
hosted work.

## Owner completion evidence

- Added the sole `m180-asymmetric-campaign-execute` entrypoint.  It accepts no
  campaign-policy overrides, revalidates M179 dual admission before reading the
  env file, accepts only DeepSeek V4 Pro, and writes authorization before any
  provider construction.
- The serial adapter now uses the existing bounded Q01 observation, annex
  guidance-card, Harness-gate, and classified `source_only` repair surfaces.
  It checkpoints every issued provider request before provider work and keeps
  the 102 completion-slot and 69 HTTP-request dimensions separate per product.
- Fake-only coverage verifies dual-product 69-request accounting, 102-slot
  accounting, checkpoint-drift refusal, and authorization refusal.  No
  credential, provider construction, or request occurred.

## Validation evidence

| Command | Terminal result |
|---|---|
| `uv run python -m brep2code.cli m179-asymmetric-campaign-admission` | passed: fresh zero-request M179 candidate, 102 slots / 69 requests |
| `uv run python -m brep2code.cli m180-asymmetric-campaign-execute` | passed: refused without `--authorize-hosted` |
| `uv run pytest tests\test_asymmetric_campaign.py -q` | passed: 4 passed |
| `uv run ruff check brep2code tests` | passed |
| `uv run python -m pytest --durations=0 -q` | passed: 293 passed in 524.06 s |
| `uv run python tools\check_governance.py` and `git diff --check` | passed |

## Review state

Owner-side M180 scope is complete.  Await Liaol's independent G3 review of the
fixed provider boundary, checkpoint-before-request accounting, frozen
69-request/102-slot limits, fake-only evidence, and absence of provider or
credential action.  The review does not authorize hosted egress.

Liaol approved the independent G3 review on 2026-08-14.  Review confirmed the
fixed provider boundary, checkpoint-before-request accounting, frozen
69-request/102-slot limits, fake-only evidence, and absence of provider or
credential action.  This approval does not authorize hosted egress.

## Closure rationale

M180 closes because its sole offline execute-entrypoint scope and independent
review are complete.  Any provider construction or hosted request requires a
new, user-selected G3 execution workpack, fresh preflight, a new independent
review, and itemized user authorization.
