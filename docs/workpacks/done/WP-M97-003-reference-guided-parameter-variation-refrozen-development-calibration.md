# WP-M97-003: Reference-Guided Parameter-Variation Re-frozen Development Calibration

- Status: done
- Milestone: M97-003
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G3

## Goal

Create a new, development-only paired calibration experiment after M97-002,
freeze its corrected observation contract and execution policy, complete a
read-only hosted preflight, and request itemized authorization only if every
preflight gate passes. This workpack never reuses M97-001 capacity, policy,
report, monitor or authorization.

## Scope

- Freeze a new M97-003 policy that names only the three preregistered M94
  development rows, the M97 measured-fact transcript contract, the current
  guidance index/card hashes, recipe/API-contract version, exact CLI policy,
  zero repair/retry rule, provider deadline and fresh report/monitor paths.
- Verify the current development input hashes, split membership, M97 outbound
  context, fake-provider accounting and local no-input `wsl-bwrap` control.
- Complete the required non-secret DeepSeek configuration and secure-executor
  checks, validate the actual nine-request bound, and prove that the new report
  and monitor destinations are absent or not reusable checkpoints.
- Present a single itemized authorization request only after the read-only
  preflight is recorded as passing.

## Attribution question and sampling intent

This bounded paired development experiment distinguishes a card/no-card result
under the repaired measured-fact/API path from M97-001's implementation
failure. It has exactly three existing development rows, six paired conditions,
nine maximum issued requests, zero repair and zero retry. Stop at the first
terminal provider or Harness outcome; it cannot claim model capability or
parameter generalization and cannot select or inspect held-out rows.

## Inputs

- `docs/corpus/sequence-paired/reference-guided-through-hole-variation-v1-m96-policy.json`
- M97-002 completed workpack and ADR-0058
- three existing M94 development rows only
- current guidance index/card and M97 measured-fact/OCP-recipe contracts

## Code paths

- `brep2code/cli/__init__.py`
- `brep2code/agent/m97_observation.py`
- `brep2code/agent/m97_recipe.py`
- focused M96/M97 tests only if policy enforcement needs implementation changes

## Docs to update

- new frozen M97-003 policy and its preflight evidence document
- `docs/architecture/v1/reference-guided-parameter-variation-design.md`
- `docs/architecture/v1/four-track-program-roadmap.md`
- `docs/modules/cli.md`, `docs/workflow/status.md`, this workpack and active handoff

## Trace/schema changes

Additive only: a new content-free policy/preflight record and fresh report/
monitor paths. Do not write raw STEP, local paths, reference scripts, hashes,
provider payloads, credentials, prompts or responses into provider-bound
traces. Existing report schema and Harness gates remain unchanged.

## Decision-package impact

- `decision_id`: M93/M94 reference-guided through-hole parameter variation.
- Q01/Q02 effect: freezes M97-002's measured Q01 facts as the only Q02 input;
  it adds no CAD IR or operation grammar.
- Q03/Q04 effect: preserves OCP API, provenance, output, bbox, volume and
  topology gates, plus zero-repair/zero-retry stopping.
- Evidence role: a fresh development-only paired calibration, conditional on
  later itemized authorization; no held-out or reusable knowledge evidence.
- Knowledge disposition: no reusable knowledge until an independently reviewed
  terminal experiment; M97-001 remains a counterexample.

## Compatibility constraints

Default execution stays offline and credential-free. No existing CLI command,
manifest, card, runtime retrieval, training input, held-out row, provider
endpoint or Harness gate may change. Provider use needs a separate explicit
authorization after preflight; DeepSeek remains selected only by explicit
`--provider deepseek` and executes only with no-input `wsl-bwrap`.

## Acceptance

```powershell
uv --cache-dir .uv-cache run python -m pytest tests\test_m96_reference_guided_through_hole_observation.py tests\test_observed_build_loop.py -q
uv --cache-dir .uv-cache run python -m ruff check .
uv --cache-dir .uv-cache run python tools\check_governance.py
git diff --check
```

Preflight must also record passing hash/split/context/no-input/config/executor/
budget/fresh-path checks before authorization is requested. Independent G3
review is required after any authorized terminal run.

## Evidence reuse / guidance-card disposition

No reusable evidence is created by preflight. The existing card is not
promoted or mutated; its hash is merely a newly frozen experimental input.

## Status transition

Record the new policy and preflight before requesting authorization. After a
terminal authorized run, update `status.md` first, then this workpack and the
handoff, and obtain Liaol's independent G3 review. A timeout, failure or
interruption closes only this new package and never permits capacity reuse.

## Closure rationale

Record all preflight facts, itemized authorization (if obtained), terminal
request accounting and independent G3 review. Passing preflight alone does not
authorize a request or close the workpack.

## Read-only preflight (2026-08-10)

[`m97-003-reference-guided-development-hosted-preflight.md`](../../workflow/m97-003-reference-guided-development-hosted-preflight.md)
records passing development-only input hash, context, no-input WSL,
non-secret configuration, budget/deadline and fresh-path checks. It grants no
provider authority; itemized user authorization remains required.

## Authorized execution record (2026-08-10)

- Liaol authorized the exact preflight scope: DeepSeek V4 Pro, the three
  development rows, measured-fact/derived-card egress, nine maximum requests,
  120-second deadline, zero repair/retry, no-input `wsl-bwrap`, and one fresh
  `prepare` → monitor → `execute` lifecycle.
- The fresh report reached `completed` with 9/9 requests issued and none
  remaining. Card conditions passed for low, nominal and high (3/3); baseline
  passed for low/high and failed for nominal (2/3). No repair, retry, later
  run, held-out row or M97-001 capacity reuse occurred.
- This is development-only terminal evidence. It remains subject to Liaol's
  independent G3 review and cannot support a capability, generalization,
  held-out or M98 claim.

## Independent G3 review and closure (2026-08-11)

Liaol approved closure after independently reviewing the M97-003 policy,
read-only preflight, itemized authorization, terminal report, 9/9 accounting,
no-input boundary and unchanged gates. The 3/3 card versus 2/3 baseline result
is retained only as development-only terminal evidence. No retry, capacity
reuse, card/prompt adjustment, held-out evaluation or M98 transition is
authorized.

## Out of scope

M98, held-out inspection/evaluation, M97-001 capacity/report/monitor reuse,
prompt or card tuning after any result, retries, repairs, manifest mutation,
runtime retrieval, training input, external data or provider request before
new itemized authorization.

## Repair hypothesis and evaluation boundary

M97-002 removed the transcript/API confounds. A later authorized M97-003 run
therefore measures only the fixed card/no-card comparison under measured facts
and supported OCP imports. It remains a development-only hosted experiment;
its terminal outcome cannot make a held-out, capability or generalization claim.
