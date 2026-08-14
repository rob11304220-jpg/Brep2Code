# WP-M175-001: Asymmetric Cohort and Annex Qualification

- Status: done
- Milestone: M175
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

## Entry condition

M174 closed the infeasible equal-card charter and the user confirmed this fresh
qualification workpack. The authoritative registry supplies 36 declared
development candidates for the 30-row no-card main cohort; the annex contains
only M170's three existing direct card roles.

## Goal

Freeze a 30-row development-only no-card main cohort and independently auditable
three-role card-assisted feasibility annex under M174's asymmetric charter.

## Scope

- Audit metadata/provenance for the 36 declared-development candidates and
  qualify exactly 30 distinct main-cohort rows with mechanism role, split,
  oracle/gates, counterexample, and explicit no-card disposition.
- Verify the three annex roles retain their explicit card identity, index/card
  hashes, role compatibility, and M170 release boundary without extending card
  eligibility.
- Publish schema-checked qualification material and focused offline audits for
  cardinality, uniqueness, development split, no-card main boundary, annex
  role/card boundary, and no pooled metrics.

## Decision-package impact

- Hypothesis ID: not applicable; development cohort and feasibility-annex
  qualification.
- Q01--Q04: selects evidence inputs only; no interface, execution, repair, or
  provider behavior changes.
- Evidence role: 30-row no-card denominator plus three-role card feasibility.
- Counterexample: duplicate or undeclared/held-out row, missing oracle/gate,
  inferred card eligibility, hash drift, pooled metric, or altered repair cap.
- Stop rule: fewer than 30 qualified development rows, a required held-out
  access, or need for any case/manifest/Harness/repair/provider change.
- Adoption boundary: qualification only; no manifest, campaign, provider, or
  hosted authorization.

## Compatibility constraints

Offline and credential-free. Do not inspect held-out assets, create a manifest,
issue provider requests, change cards/indexes/Harness/repair/provider/runtime,
or add retrieval. Case records and frozen M170/M96/M97 artifacts remain
immutable.

## Acceptance

Define focused qualification audit/tests, then run relevant tests, Ruff,
applicable case/governance audits, `uv run python tools\check_governance.py`,
and `git diff --check`. Record Liaol's independent G2 review.

## Owner completion boundary

Publish the frozen qualification dossier and acceptance evidence, then obtain
Liaol's independent G2 review. Only then may a separately selected campaign
input-freeze workpack be considered.

## Owner completion evidence

- Published `docs/corpus/knowledge/m175-asymmetric-cohort-qualification-v1.json`.
  It hash-binds the authoritative registry, fixes ten distinct three-row
  no-card mechanism groups, identifies the two excluded redundant baseline
  groups, and records the three-role unpooled annex with its card/index hashes.
- Added `tools/audit_m175_asymmetric_qualification.py`, which checks main
  cardinality/uniqueness, split, script availability, base oracle fields,
  group cardinality, annex cardinality/no-pooling, direct roles, and guidance
  hashes without reading a STEP or reference script.
- Updated the M174 charter and current route to name M175 as the replacement
  qualification ledger.

## Validation evidence

| Command | Terminal result |
|---|---|
| `uv run python tools\audit_m175_asymmetric_qualification.py` | passed: 30 main rows, 10 groups, 3 annex rows |
| `uv run python -m ruff check tools\audit_m175_asymmetric_qualification.py` | passed |

## Review state

Owner-side qualification is complete. Await Liaol's independent G2 review of
the cohort selection rationale, metadata-only boundary, no-card main cohort,
annex role/hash boundary, audit coverage, and unpooled reporting rule.

Liaol approved the independent G2 review on 2026-08-14. The 30-row cohort
selection rationale, metadata-only boundary, no-card main cohort, annex
role/hash boundary, audit coverage, and unpooled reporting rule were accepted.
This approval grants neither campaign execution nor provider/hosted authority.

## Closure rationale

M175 closes because it froze and independently reviewed an evidence-compatible
30-row no-card denominator plus an explicitly bounded three-role card annex.
Any campaign-input freeze remains a new selected package; no manifest or
provider activity follows from this closure.

## Status transition

Update `status.md` first, then move this workpack to `done/` and archive the
handoff. Do not activate campaign freeze without a new explicit user selection.

## Permitted stop conditions

Independent review, source/hash drift, insufficient qualified development rows,
a required held-out access, or a required case/manifest/Harness/repair/provider
change.

## Out of scope

Campaign manifest/input freeze, provider/model choice, hosted preflight or
execution, credentials, report/budget paths, prompt changes, retrieval,
held-out use, card projection, and terminal review.
