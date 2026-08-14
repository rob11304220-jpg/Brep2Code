# WP-M173-001: Hosted Milestone Case and Reference Qualification

- Status: deferred
- Milestone: M173
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

## Entry condition

M172 independently froze the development-only 30-case, three-stratum reporting
charter. The user selected this workpack as M172's next route gate.

## Goal

Qualify and freeze exactly thirty development cases—ten per M172 stratum—with
auditable mechanism role, oracle/gates, split, counterexample, and explicit
no-card/card reference disposition before campaign inputs are frozen.

## Scope

- Inspect only development-governed case records and their metadata/provenance
  needed to assemble three ten-case strata.
- Publish a qualification dossier with one immutable row per case, its stratum,
  mechanism role, development split evidence, oracle/gates, counterexample,
  and explicit no-card or one-card disposition.
- Verify each selected card, if any, is explicit, hash-bound, role-compatible,
  absent by default, and not a retrieval/default-injection mechanism.
- Reject or replace candidates only before the cohort freezes; record the
  reason without widening case families or reading held-out assets.
- Add offline audits/tests for cardinality, split, duplicate prevention,
  reference boundary, and dossier schema; update durable case/route authority
  only as required by the qualified cohort.

## Decision-package impact

- Hypothesis ID: not applicable; development campaign-cohort qualification.
- Q01--Q04 decision: selects evidence inputs for a later frozen campaign but
  changes no tool, generation, gate, repair, or provider contract.
- Evidence role: development-only denominator/oracle/reference provenance.
- Counterexample: missing development split/oracle, duplicate row, unavailable
  card, unsupported role, hash drift, or any held-out dependency rejects a row.
- Stop rule: failure to qualify ten rows for a stratum, any needed schema/
  Harness/repair/provider change, or held-out access stops the workpack.
- Adoption boundary: qualified cohort only; no card effect, retrieval,
  provider, hosted, or execution claim.

## Compatibility constraints

Offline and credential-free. Do not inspect held-out assets; execute a hosted
campaign; modify Harness/tool schema, repair policy, provider/runtime behavior,
or existing frozen M96/M97/M170 artifacts; create directory search/retrieval;
or reuse a report/budget. Case files remain immutable unless an existing
metadata-governance contract explicitly permits the audited designation.

## Acceptance

Define focused offline dossier/audit tests before execution, then run relevant
tests, Ruff, applicable case/governance audits, `uv run python
tools\check_governance.py`, and `git diff --check`. Publish independent-review
evidence for all 30 rows and card dispositions.

## Owner completion boundary

Complete after the frozen 30-row development dossier, offline audit evidence,
and Liaol's independent G2 review. M174 may then freeze campaign inputs but no
provider request is authorized.

## Permitted stop conditions

Independent review, insufficient qualified development candidates, source/hash
drift, a required held-out access, or a required case/manifest/Harness/repair/
provider change.

## Blocked state

The initial metadata-only qualification pass is blocked before selecting any
row. `docs/corpus/case-portfolio.md` records that the sole CAD-action runtime
card, `vertical-cylinder-construction`, has direct evidence only for three
declared roles: `cylinder` final primitive, `block_with_hole` single boolean-cut
tool, and `three_hole_plate` repeated boolean-cut tool. M172 requires ten
distinct cases in S2 and ten distinct cases in S3, all with an explicit
hash-bound card. Thus the available card-qualified set is 3, while the frozen
charter requires 20 distinct card-qualified rows.

Do not reuse a case across strata, infer card eligibility from reference packs
or parameter families, or create/expand a card within M173. M174 is the
user-selected denominator redesign. Re-entry requires M174 to complete its
charter and registry reconciliation, then M173 must be replaced by a fresh
active qualification ledger reflecting the 30-case no-card main cohort and
separate three-role feasibility annex before campaign freeze.

## Out of scope

Hosted preflight or request, provider/model selection, campaign execution,
prompt tuning, retrieval, held-out use, generic case expansion, repair policy,
Harness/runtime schema changes, report/budget creation, and terminal review.
