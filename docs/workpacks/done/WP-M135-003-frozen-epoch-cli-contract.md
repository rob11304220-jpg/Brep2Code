# WP-M135-003: Frozen Epoch CLI and Monitor Contract

- Status: done
- Milestone: M135
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G3

## Goal

Implement the local, credential-free executable surface required to preflight
M134's unchanged 18-condition development epoch: one explicit CLI command that
binds its frozen policy, serial request accounting, report identity and
monitoring interface without constructing a hosted provider or issuing a
request.

## Scope

- Add a dedicated M135 CLI/preflight path that accepts only the frozen epoch
  policy and validates the 18 ordered condition identities, hashes, splits,
  executor, serial cap, zero-repair/zero-retry boundary, report path and
  monitor path.
- Keep the path offline and fake-provider-testable; it must reject hosted
  execution unless a later explicit authorization path is separately selected.
- Make report and monitor identities explicit, fresh and mechanically checked
  before any provider construction.
- Add focused tests for CLI argument validation, freshness, checkpoint/monitor
  lifecycle and rejection of policy or accounting drift.
- Record implementation evidence and obtain independent G3 review. A complete
  fresh hosted preflight remains a later task after this workpack closes.

## Attribution question and sampling intent

Does the existing frozen M134 cohort have an executable local contract that
can preserve its 18-condition denominator and accounting boundary? This work
adds no cases and does not evaluate provider quality. Stop on any frozen-input
drift, executable-boundary failure, independent review, or explicit hosted
authorization.

## Inputs

- `docs/workflow/m134-frozen-hosted-batch-epoch-policy.md`
- `docs/workflow/m135-002-fresh-reentry-preflight.md`
- `docs/architecture/adr/0067-frozen-hosted-batch-epochs.md`
- `docs/architecture/adr/0068-frozen-epoch-checkpoint-and-transcript-contract.md`
- `docs/runbooks/llm-provider-config.md`

## Code paths

- `brep2code/agent/m135_epoch.py`
- `brep2code/cli/__init__.py`
- `brep2code/storage/` and monitor integration only when needed for the
  explicit M135 report/monitor contract
- `tests/test_m135_epoch.py` and focused CLI/monitor tests

## Docs to update

- `docs/workflow/status.md`
- this workpack and one active handoff
- `docs/workflow/m135-003-frozen-epoch-cli-contract.md`
- `docs/runbooks/llm-provider-config.md` and the relevant contract document if
  the command, report schema or monitor lifecycle becomes durable

## Trace/schema changes

The M135 checkpoint may gain only local contract fields required to bind a
fresh report and monitor identity. It must not record credentials, raw provider
content, raw STEP, absolute input paths, or outbound transcripts. Any durable
schema or CLI JSON change requires a contract update and focused regression
tests.

## Decision-package impact

- `decision_id`: no Q01--Q04 package; local hosted-evaluation governance
  readiness only.
- Q01/Q02 effect: no observable, case, card, prompt, split or sequence change.
- Q03/Q04 effect: makes the frozen execution/accounting boundary executable
  and fail-closed before a later hosted preflight.
- Evidence role: offline regression and contract evidence.
- Knowledge disposition: no reusable knowledge.

## Compatibility constraints

Default operation remains offline and credential-free. Existing CLI commands
must remain compatible; M135 must not select or construct a provider, read or
print credentials, send data, alter executable manifests, change the frozen
cohort/order/card/prompt/provider/model, issue repair/retry, or reuse any
M135-001/M135-002 report, monitor, budget or authorization. Hosted execution,
authorization and M137 terminal review remain out of scope.

## Acceptance

```powershell
uv run python -m pytest tests\test_m135_epoch.py -q
uv run python -m pytest -m fast -q
uv run python -m pytest
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

## Owner completion boundary

Publish the executable offline M135 CLI/monitor contract and M135-003 evidence
record; pass every acceptance command and obtain Liaol's independent G3 review.
Only then may a separately selected workpack perform a new complete hosted
preflight; this workpack never requests authorization.

## Permitted stop conditions

Independent review; explicit hosted authorization; frozen-input drift;
out-of-scope dependency; or reproducible local implementation/validation
blocker.

## Evidence reuse / guidance-card disposition

No reusable knowledge. The existing prismatic card stays a frozen treatment
input, and all other frozen conditions remain no-card.

## Status transition

Update `docs/workflow/status.md` first, then this workpack and the active
handoff. If the executable contract passes, retain this workpack for
independent G3 review; if blocked, archive it with the terminal evidence
record. Run the governance audit after lifecycle-record edits.

## Out of scope

Hosted execution or authorization issuance; any provider construction or
credential access; condition addition/removal/reorder; prompt/card/model/
provider changes; repair/retry; case/manifest changes; held-out evaluation;
card promotion; runtime promotion; and M137 terminal review.

## Closure rationale

Owner-side implementation is complete. `m135-epoch-preflight` prepares only a
fresh local 0/18 checkpoint and distinct monitor state while binding the
frozen provider/model identifiers, executor, 120-second deadline, no selected
token cap and zero repair/retry policy. Focused tests, fast regression, full
suite and Ruff passed; the evidence record is
[`m135-003-frozen-epoch-cli-contract.md`](../../workflow/m135-003-frozen-epoch-cli-contract.md).
No provider was constructed, no credential was read, and no data was sent.
The workpack awaits Liaol's independent G3 review; it cannot request hosted
authorization.

## Independent review

Liaol approved the independent G3 review on 2026-08-12. The review accepted
the local-only fail-closed command boundary, frozen contract values, fresh-path
rejection tests and recorded offline acceptance evidence. It grants no hosted
authorization; M135-004 is a separately selected full local preflight.
