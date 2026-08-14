# WP-TRG-041: Repair and Interaction Policy Calibration

- Status: deferred
- Owner: unassigned
- Reviewer: independent reviewer required
- Risk tier: G2

## Entry condition

`WP-TRG-040` has a completed, independently reviewed terminal report from the
unchanged TRG-039 release, and the user selects this workpack. The report must
retain per-case tool/completion accounting, classification, normalized failure
signature, repair eligibility/attempt/outcome and terminal reason. This is an
offline evidence-review and policy-design package; it cannot issue a provider
request or reuse a historical hosted budget.

## Goal

Decide whether the observed closed-loop evidence justifies retaining M141's
one-edit source-only policy, changing the attempt count for exactly one
admitted source-level class, or opening a separately bounded prerequisite for
a currently prohibited class. Also decide whether the frozen Q01/card tool
interaction budget is sufficient, excessive, or needs a separately tested
change.

## Scope

- Reproduce the frozen three-case report's terminal accounting and build a
  compact policy-evidence table: class count, first-pass pass rate, eligible
  repair count, attempted count, conversion count, changed-signature count,
  plateau count, provider/protocol failure count and tool/completion use.
- Compare only predeclared candidate dispositions:
  1. retain one `source_only` attempt;
  2. permit a second `source_only` attempt for `execution_local` only when the
     first successor has a changed normalized failure signature; or
  3. reject the increase and retain the existing cap.
  The review must not broaden more than one class or route in the same package.
- Treat `static_api_contract` as one attempt unless trace evidence identifies a
  distinct, repeated, non-plateau source-level mechanism. Treat
  `output_artifact` as one attempt unless an independently reproducible local
  output-contract diagnosis exists.
- For geometry/semantic, selector ambiguity or editability, record only the
  missing prerequisite: respectively a source-linked local geometry locator,
  a reviewed unique selector observation, or an independent editability
  oracle. Do not enable a repair route in this workpack.
- Assess the fixed interaction shape separately: required versus unused Q01
  and card calls, tool errors, result-size/turn-limit stops, and whether a
  change would improve information availability without enlarging egress. A
  candidate change must be one of: retain the declared Q01-plus-card sequence;
  omit a demonstrably unused declared call; or add one predeclared bounded Q01
  tool call. It cannot add free-form reasoning, filesystem/shell access,
  automatic retrieval, a second card, or prompt injection.
- Publish a reviewed policy recommendation and, if a change is selected,
  specify a fresh successor campaign with a new denominator, hashes, budget,
  report/monitor paths and G3 authorization gate. Do not implement or run that
  successor here.

## Attribution question and sampling intent

Distinguish a genuine local repair/interaction signal from random provider
variation. The expected information gain is whether one additional attempt or
one tool-budget adjustment is justified for one named failure mechanism. Stop
with `retain` when the three-case report has no eligible failures, insufficient
same-class evidence, any unaccounted request/trace, platform/protocol cause,
or a non-matching control that does not reproduce the proposed mechanism.

## Decision-package impact

- `decision_id`: none; this is evidence-based policy calibration.
- Q01/Q02 effect: may recommend, but not implement, one future bounded tool
  budget/schema change; it cannot alter observation or action semantics.
- Q03/Q04 effect: may recommend a future attempt cap for one admitted class or
  state one missing prerequisite for a prohibited class; it changes no active
  gate or repair behavior.
- Evidence role: terminal hosted evidence review plus local fixed-script and
  non-matching-control evidence where available.
- Knowledge disposition: record a counterexample or no reusable knowledge;
  no card, retrieval, provider, SDK/IR or runtime promotion follows.

## Compatibility constraints

M141 remains the active implementation authority until a future selected and
reviewed implementation workpack changes it. No provider is constructed; raw
inputs, scripts, credentials, full responses, held-out material and arbitrary
repository content remain outside the review/export boundary. Historical
campaigns cannot be resumed or repaired in place.

## Acceptance

The activated package must reproduce report accounting, audit relevant trace
schemas, run applicable policy/unit checks, Ruff and governance audit, and
publish a decision record with the exact evidence, counterexample, stop rule
and successor boundary. Any selected policy change requires an ADR.

## Out of scope

Hosted reruns, budget reuse, implementation of a new repair route, more than
one additional repair attempt, generic regeneration, geometry/selector/
editability repair, new cards, retrieval, case growth, held-out use, model or
prompt comparison, and changes to the frozen TRG-039/040 reports.
