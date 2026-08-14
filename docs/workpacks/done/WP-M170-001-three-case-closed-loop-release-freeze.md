# WP-M170-001: Three-Case Closed-Loop Release Freeze

- Status: done
- Milestone: M170
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2
- Trigger consumed on closure: `WP-TRG-039`

## Goal

Freeze and independently review one offline, fail-closed Harness release that
composes bounded Q01 tools, one explicit hash-bound card, initial generation,
restricted execution/gates, classified feedback, and at most one admitted
source-only repair. It is the release gate for the selected hosted-capability
milestone, not its 30-case campaign.

## Scope

- Freeze exactly `cylinder`, `block_with_hole`, and `three_hole_plate`, in that
  order, with their registered development/split/input identities.
- Bind `final primitive`, `single boolean-cut tool`, and `repeated boolean-cut
  tool` to the existing `vertical-cylinder-construction` card and index hashes.
- Integrate only M139, M140, M141, M19-003, and M155 boundaries into one
  offline release/dossier and fake-provider path.
- Freeze one Q01 completion, one card completion, one initial-script completion,
  and at most one eligible source-only edit per case: at most four completions.
- Confirm fake-provider coverage for direct pass, admitted repair, plateau, and
  all fail-closed categories. Do not construct a provider or issue a request.

## Attribution question and sampling intent

Determine whether existing components form one immutable release before the
larger denominator is designed. These three cases are release fixtures only;
they do not estimate milestone success or select the later case cohort.

## Inputs

- ADR-0078 and ADR-0082.
- M139/M140/M141 contracts, M19-003 guidance boundary, M155 entry boundary.
- `WP-TRG-039-closed-loop-release-freeze.md`.

## Code paths

Only existing launcher, tool-turn, repair-router, trace, and test paths needed
to compose the release. A new tool, gate, manifest, card, retrieval interface,
provider construction, or repair route is a stop condition.

## Docs to update

The release/dossier record, an existing contract/runbook only for an
integration clarification, this workpack, `status.md`, and active handoff.

## Trace/schema changes

No unreviewed schema widening. Retain sanitized tool/card calls, generation,
classification, repair eligibility/attempt/outcome, execution/gates,
completion accounting, and terminal reason.

## Decision-package impact

- Decision ID: none; release integration only.
- Q01/Q02: existing interfaces are frozen without semantic change.
- Q03/Q04: existing gates, classification, one-edit cap, and stop policy freeze.
- Evidence role: offline release-readiness regression; no knowledge promotion.

## Compatibility constraints

Offline and credential-free. Raw STEP, paths, reference scripts, gate logs,
provider responses, credentials, held-out data, retrieval, model/prompt change,
case substitution, and report-path reuse remain prohibited.

## Acceptance

Define focused integration tests, then run applicable offline validation, Ruff,
runtime-guidance and governance audits, and `git diff --check`. Publish an
independently reviewed dossier naming hashes, schemas, limits, executor,
deadline, completion arithmetic, repair classes, and stop rules.

## Owner completion boundary

Complete after offline dossier/acceptance evidence and Liaol's independent G2
review. A hosted request is never a completion substitute.

## Permitted stop conditions

Independent review, frozen-input drift, reproducible validation blocker, or
out-of-scope dependency. Unexpected feedback requires a newly scoped and
explicitly user-selected workpack that returns to this gate or the next planned
route gate.

## Evidence reuse / guidance-card disposition

The card is one explicit hash-bound tool result, not prompt injection, a
reference script, directory lookup, or later-cohort authority.

## Status transition

Update `status.md` first. On accepted closure, move this ledger to `done/`,
archive consumed TRG-039, update handoff, and claim the milestone-charter
successor under the user's 2026-08-14 route selection; assign its M-number then.

## Independent review

Liaol independently accepted the focused M170 evidence on 2026-08-14: the
three-case/fake-provider tests, Ruff, governance audit, and diff check pass;
the five full-suite failures are confined to historical M96/M97 guidance-index
hash assertions.  The selected `vertical-cylinder-construction` card hash is
unchanged, and M170 neither changes nor consumes those historical policies.
The failures remain recorded and are not treated as resolved by this review.

## Closure rationale

M170 closes as an offline three-case release gate because its bounded
acceptance evidence passed independent review without scope widening.  The
scope-external M96/M97 index drift is remediated by separately selected M171
before the route proceeds to its next unmet named successor.

## Validation evidence

| Command | Terminal result |
|---|---|
| `uv run python -m pytest tests\\test_m170_closed_loop_release.py tests\\test_tool_turn_loop.py tests\\test_m141_classified_repair_policy.py -q` | 13 passed in 22.32s |
| `uv run python -m ruff check brep2code\\agent\\closed_loop_release.py brep2code\\agent\\__init__.py tests\\test_m170_closed_loop_release.py` | passed |
| `uv run python tools\\check_governance.py` | passed |
| `git diff --check` | passed |
| `uv run python -m pytest tests -q` | 283 passed, 5 failed in 442.93s; all five failures are M96/M97 guidance-hash drift (`tests/test_m96_reference_guided_through_hole_observation.py` and `tests/test_observed_build_loop.py`), outside M170's changed paths. |

The full-suite result was a reproducible scope-external blocker pending review.
Independent review accepted focused M170 evidence while preserving the five
failures as an explicit M171 remediation obligation.  Do not change the
historical M96/M97 policy/card hashes within this workpack.

## Durable conclusion and route disposition

ADR-0082 and `current-project-route.md` own the durable decision; this ledger
retains release execution and acceptance provenance.

## Out of scope

Provider/hosted requests, credentials, new cases/cards, retrieval, held-out
use, model comparison, prompt tuning, gate changes, generic repair, sequence/IR
edits, and selection or execution of the 30-case campaign.

## Repair hypothesis and evaluation boundary

Only the existing one-edit `source_only` policy is exercised with a fake
provider. Geometry/semantic, selector, editability, sandbox/provenance,
timeout, protocol, mixed, and unknown outcomes remain terminal.

## Notes

User-selected continuous route after M170:

1. M171 historical M96/M97 guidance-index fixture remediation (G2; explicitly
   selected after M170 closure)
2. `hosted-milestone-claim-and-denominator-charter` (G1)
3. `hosted-milestone-case-and-reference-qualification` (G2)
4. `hosted-milestone-campaign-freeze` (G2)
5. `hosted-milestone-30-case-execution` (G3)
6. `hosted-milestone-terminal-review` (G2)

Automatic claiming applies only after the prior acceptance boundary and only to
this sequence. For G3 it permits offline preparation/review only; fresh
itemized hosted authorization is mandatory before any provider request.
