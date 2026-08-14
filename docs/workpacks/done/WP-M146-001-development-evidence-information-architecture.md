# WP-M146-001: Development-Evidence Information Architecture

- Status: done
- Milestone: M146
- Trigger consumed: `WP-TRG-030`
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

## Entry condition

M145 delivered the reviewed mechanism/difficulty/evidence/gap report. The user
selected the deferred information-architecture route to make those expressions
navigable without changing their existing authorities.

## Goal

Implement a source-linked development-side evidence crosswalk with stable IDs,
ownership, derived human navigation, and deterministic drift audit. It must
show mechanism, multi-axis difficulty, evidence maturity, admission risk and
decision gaps without becoming a second case registry or runtime resource.

## Confirmed architecture guide

M146 keeps the existing three architectures, but assigns them distinct entry
roles instead of treating case management as the project-level theory map:

| Architecture | Role after M146 | Primary question |
|---|---|---|
| Harness Q01--Q04 pipeline | system/runtime architecture | How does the system inspect a B-Rep, generate a script, gate it, and return bounded feedback? |
| case and governance records | evidence-asset management architecture | Which controlled asset supports a claim, under which lifecycle, split, hash, and review boundary? |
| development knowledge system | primary theory-navigation architecture | Which bounded B-Rep-to-modeling-sequence hypotheses have been evidenced, and where are their limits? |

The crosswalk must be one shared relationship layer over existing authoritative
sources, with compact derived views rather than five new registries or parallel
directory trees.  Its primary node is a **bounded modeling hypothesis**, not a
case, feature label, or difficulty score.  A hypothesis links, where present:

```text
capability question -> Q01 observables -> constrained Q02 sequence/binding
-> Q03 gate -> Q04 diagnostic, repair, or stop condition
-> positive/negative evidence -> coverage gap -> adoption status
```

The derived navigation may present the following five views of those same
relations:

1. **Capability-question view**: Q01--Q04 subproblems and verified/unknown
   boundaries.
2. **Bounded-modeling-hypothesis view**: observation prerequisites, operation
   semantics, entity-reference rule, dependency order, parameter boundary,
   counterexample, and unsupported generalization.
3. **Evidence view**: source-linked oracle, discriminating, negative-control,
   regression, and documentary held-out evidence, including maturity and
   admission-risk labels.
4. **Evaluation-design view**: the declared path from a hypothesis to an
   offline or future hosted evaluation: allowed Q01 facts, Q02 action scope,
   Q03/Q04 interpretation, comparison, and conclusion boundary.  M146 may
   navigate already-declared material only; it must not design, run, or
   authorize a hosted experiment.
5. **Adoption-boundary view**: development-side usability versus any separately
   reviewed runtime-card, helper, IR, SDK, manifest, provider, or training
   proposal.  No link in this view grants adoption authority.

The six analytical dimensions are not coequal project registries: geometry /
sketch topology, kernel-operation semantics, entity-reference stability,
sequence dependency, and parameter robustness describe a bounded modeling
hypothesis; evidence/governance maturity describes confidence in that claim and
its permitted use.  The existing design-intent labels are human navigation
facets only, never capability assertions or sources of authority.

## Confirmed follow-on route (planning only)

This route records the user-confirmed sequencing after M146.  The route is
registered as deferred workpacks below, but is not an active queue and does not
authorize any successor; each stage requires fresh user selection, a bounded
scope, and the applicable risk/review gate.

| Order | Prospective bounded package | Purpose | Required boundary |
|---:|---|---|---|
| 1 | `WP-TRG-031` project theory map and document navigation (G1) | Make the development knowledge system the human/Agent theory entry, while retaining pipeline as system entry and case/governance records as evidence-asset entry. | Publish links and routing only; do not move authority or rewrite source records. |
| 2 | `WP-TRG-032` Agent entry and document routing (G1) | Update `AGENTS.md`, `README.md`, and document entry guidance so task type selects theory, runtime, governance, or workflow material in that order. | Agents must not infer implementation, provider, case, or hosted authority from navigation. |
| 3 | `WP-TRG-033` case-evidence role alignment (G2) | Link current cases to the bounded hypotheses they support/refute and to oracle, discriminating, negative-control, regression, or documentary roles. | Preserve `case.json`/registry ownership of identity, split, hash, lifecycle, and manifest facts; do not inspect held-out fixtures. |
| 4 | `WP-TRG-034` capability-contract code alignment (one or more G2 packages) | Align Q01 observable, Q02 action, Q03 gate, and Q04 diagnostic/stop contracts and tests to selected hypothesis IDs. | One package per bounded capability; no helper, IR, SDK, runtime-card, or generic feature claim without a separate proposal. |
| 5 | `WP-TRG-035` hypothesis-to-hosted evaluation (G3, if selected) | Test whether one reviewed, bounded reference hypothesis helps an LLM under a fixed campaign and comparison. | Separate package, offline preflight, independent review, and itemized hosted authorization; no inference from case replay alone. |

Every later proposal must state the chain
`hypothesis ID -> Q01--Q04 contract -> evidence roles -> counterexample and
stop rule -> adoption boundary`.  The crosswalk may expose this chain, but it
does not grant any of the downstream authority.  `WP-TRG-028` remains a
separate deferred runtime-projection route and is not superseded by this plan.

## Scope

- Define a versioned crosswalk schema linking case metadata, reviewed knowledge
  units, decision packages, coverage dimensions, and admission records by
  stable source IDs/paths, centered on bounded modeling hypotheses.
- Publish one compact generated-or-maintained human navigation view and a
  deterministic audit for source existence, source hashes where declared,
  crosswalk referential integrity, authority/non-projection boundaries, and
  absence of fixture/script access.
- Document ownership, update order, drift disposition, and migration boundary.
- Record only relationships, controlled display labels, and declared source
  hashes where needed; source fields such as lifecycle, split, admission
  disposition, manifest state, or runtime eligibility must remain in their
  existing authorities.

## Compatibility constraints

No fixture or held-out inspection/execution, case production, lifecycle/split
change, manifest/Harness/runtime/provider change, training, retrieval, SDK/IR,
or hosted execution. The crosswalk is a development-side derived view only;
`case.json`, registry, knowledge units, decision packages, coverage matrix and
admission records remain authoritative for their own fields.

## Decision-package impact

- `decision_id`: none; this work cross-links existing packages only.
- Q01/Q02 and Q03/Q04 effects: none; it changes no observable, hypothesis,
  gate, repair route, or stopping rule.
- Evidence role: navigation over existing evidence only.
- Knowledge disposition: no reusable runtime knowledge.

## Trace/schema changes

May add a development-side crosswalk schema/artifact and its audit. It must not
change signal bundles, provider/tool traces, manifests/reports, storage layout,
or CLI JSON.

## Acceptance

```powershell
uv run python -m pytest tests -q --ignore tests/test_m29_selector_ambiguity.py
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

## Owner completion boundary

Publish the schema, source-linked crosswalk, navigation view, audit, update
guidance and validation evidence; obtain Liaol's independent G2 review.

## Owner implementation evidence

- Added `docs/corpus/knowledge/development-evidence-crosswalk-v1.json`: a
  versioned relationship layer centered on five bounded modeling hypotheses.
  It preserves source authorities, records declared source hashes, and forbids
  fixture/script/runtime paths and all adoption projection.
- Added `docs/corpus/knowledge/development-evidence-crosswalk-v1.md`: the five
  required derived views (capability question, hypothesis, evidence,
  evaluation-design boundary, and adoption boundary).
- Added `tools/audit_development_evidence_crosswalk.py`, and linked its update
  order to `docs/runbooks/modeling-knowledge-maintenance.md`. The audit checks
  source existence/hash drift, stable relationship IDs, non-projection scope,
  and forbidden source paths without reading case-library assets, fixtures,
  scripts, held-out inputs, or runtime resources.
- Validation: crosswalk audit, Python compilation, Ruff, governance audit, and
  `git diff --check` passed on 2026-08-13. The required full pytest command
  `uv run python -m pytest tests -q --ignore tests/test_m29_selector_ambiguity.py`
  produced no test output and reached the 180-second outer deadline; it is a
  recorded timeout, neither a pass nor a failure.

## Independent review

- Liaol approved the independent G2 review on 2026-08-13 after checking the
  source-authority preservation, five derived views, non-projection boundary,
  deterministic audit, and validation record.
- Review result: approved. Crosswalk audit, Ruff, governance audit, and
  `git diff --check` passed. The full pytest timeout remains recorded as a
  non-terminal validation limitation and was not represented as a passing run.

## Closure rationale

M146 closes because its bounded documentary crosswalk, navigation, audit, and
maintenance guidance are complete and independently approved. No source
authority, runtime boundary, fixture, script, manifest, provider, or hosted
scope changed. Any successor remains deferred until explicitly selected.

## Permitted stop conditions

Independent review; reproducible source-authority conflict; need for fixture
or held-out access, lifecycle/manifest/runtime/provider change, hosted
authority, or reproducible local validation blocker.

## Status transition

Update `docs/workflow/status.md` first, then this workpack and active handoff.
On closure archive M146 and leave TRG-028 deferred until user-selected.

## Out of scope

Second case registry, automatic admission/promotion, generic difficulty score,
runtime projection, case production, provider use, training, and hosted work.
M146 also does not create a hosted evaluation design, change the Q01--Q04
pipeline, or reorganize authoritative source directories.  A durable
architecture decision beyond this workpack requires its own ADR when the
implementation boundary is known.
