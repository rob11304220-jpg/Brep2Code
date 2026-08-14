# WP-M178-001: Asymmetric Hosted Campaign CLI and Preflight

- Status: done
- Milestone: M178
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

## Entry condition

M176 froze a 30-case no-card main cohort and a three-case hash-bound-card
feasibility annex. M177's local preflight established that the generic
`observed-development` command cannot express that frozen contract. The user
explicitly selected this bounded G2 implementation package.

## Goal

Add an offline-only, fixed M176 campaign preparation and future-execute
admission surface. It must make the complete frozen contract inspectable and
fail closed before any future G3 provider construction or request.

## Scope

- Add a dedicated CLI/module contract for the M176 main and annex products;
  it must validate M175/M176 hashes, development-only main rows, the three annex
  roles and their sole registered hash-bound card, 4096 output tokens,
  120-second deadline, serial execution, one eligible source-only repair and
  fresh, distinct report/monitor identities.
- Record both accounting dimensions: 102 maximum interaction-completion slots
  (90 main + 12 annex) and no more than 69 actual provider HTTP requests
  (60 main + 9 annex). The latter remains within M176's authorized 102 upper
  ceiling but must not be represented as 102 issued requests.
- Add a local `prepare` checkpoint and future `execute` admission boundary.
  Preparation must not read credentials, construct a provider, create a
  Harness record, or issue a request. Execution must require a freshly
  prepared checkpoint and `--authorize-hosted`.
- Add focused tests and the necessary documentation/ADR. Tests may use only
  fake providers and temporary paths.

## Compatibility constraints

No change to M175 cohort membership, M176 frozen source values, runtime card
contents, generic `observed-development`, repair semantics, provider protocol,
manifest, held-out assets, or actual hosted execution. No `.env` value may be
read or printed. The new surface may not offer overrides for cohort, card,
model, token cap, deadline, repair/retry, executor, report identity, or
egress content.

## Acceptance

- Focused M178 contract/CLI tests cover a clean prepared checkpoint and each
  fail-closed boundary (hash/card/identity/accounting/authorization).
- `uv run ruff check brep2code tests` and the relevant offline validation
  selection pass.
- `uv run python tools/audit_m175_asymmetric_qualification.py`,
  `uv run python tools/audit_m176_campaign_freeze.py`, and
  `uv run python tools/check_governance.py` pass.
- Independent review by Liaol confirms no hosted/provider/credential action
  occurred and that the new CLI does not widen the frozen contract.

## Out of scope

Provider construction or request, egress authorization, M177 re-entry,
execution checkpoint creation under the M176 report identities, reference-card
or cohort changes, retry behavior, held-out access, runtime/Harness/provider
changes, and a terminal G3 review.

## Owner completion boundary

Publish the implementation, passing offline evidence, ADR and handoff, then
obtain Liaol's independent G2 review. Stop there: a successor G3 preflight and
fresh itemized egress authorization remain a separate user-selected package.

## Permitted stop conditions

Independent review; frozen hash/role/identity drift; a reproducible offline
test failure; or a requirement that would widen the frozen hosted contract.

## Status-transition plan

`active → review → done` after the listed evidence and independent review.
If a frozen input drifts or a required boundary cannot be represented without
widening it, move to `blocked` or `deferred` with the exact re-entry condition.

## Owner evidence

- Added `brep2code/asymmetric_campaign.py` and fixed CLI commands
  `m176-asymmetric-campaign-preflight` / `m176-asymmetric-campaign-admission`.
  The preflight writes only the four fresh local report/monitor identities;
  it never constructs a provider or reads credentials. Admission validates both
  still have zero issued requests and remain un-authorized.
- Added `tests/test_asymmetric_campaign.py`, including clean dual-product
  preparation, 102-vs-69 accounting, identity collision, and checkpoint-drift
  rejection, all against a temporary copied corpus.
- 2026-08-14 owner acceptance passed:
  `uv run pytest tests/test_asymmetric_campaign.py -q` (2 passed);
  `uv run ruff check brep2code/asymmetric_campaign.py brep2code/cli/__init__.py tests/test_asymmetric_campaign.py`;
  `uv run python -m py_compile brep2code/cli/__init__.py brep2code/asymmetric_campaign.py`;
  M175/M176 audits; `uv run python tools/check_governance.py`; and
  `git diff --check`.

## Review state

Owner-side scope is complete. This active workpack remains `active` while the
independent Liaol G2 review is pending, as required by the repository's active
workpack directory contract.

## Closure

Liaol independently approved the G2 review on 2026-08-14. Review confirmed the
implementation does not construct a provider, read credentials, issue a
request, alter M175/M176 membership, or widen the card/repair/model/deadline
boundary. M178 is closed. Its durable CLI contract is recorded in
[`docs/modules/cli.md`](../../modules/cli.md) and the accounting decision in
[`ADR-0085`](../../architecture/adr/0085-asymmetric-campaign-request-accounting.md).
The next possible action is a newly selected G3 M177 preflight; neither this
closure nor the prior M177 authorization authorizes execution.
