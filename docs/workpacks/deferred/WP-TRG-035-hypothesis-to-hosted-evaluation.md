# WP-TRG-035: Hypothesis-to-Hosted Evaluation

- Status: deferred
- Owner: unassigned
- Reviewer: independent reviewer required
- Risk tier: G3

## Entry condition

The user selects one M146 `hypothesis_id` with reviewed development evidence,
the M146 crosswalk and M150 case-evidence audits pass, their ID/SHA-256
snapshots and selected relationship IDs are frozen, and an explicitly designed
comparison states the hypothesis's evidence and adoption boundary. The package
also requires a separately reviewed, hash-pinned **egress-safe reference
projection** with an explicit outbound schema/allowlist. M146/M150 material is
campaign provenance only and cannot itself be provider input. A new activation
package must cite
`docs/architecture/v1/runtime-and-hosted-entry-boundary-v1.md`, complete
hosted preflight, and obtain itemized authorization before any provider
request.

## Goal

Evaluate whether one reviewed, bounded reference hypothesis improves an LLM's
behavior in a fixed Q01--Q04 campaign, relative to declared comparison arms.

## Scope

- Freeze the M146 crosswalk ID/SHA-256, M150 mapping ID/SHA-256, selected
  relationship IDs, `hypothesis_id`, case/split scope, permitted Q01 egress,
  egress-safe reference-projection ID/SHA-256/schema, Q02 action scope, Q03
  gate, Q04 feedback, comparison arms, request or cost ceiling, rounds,
  deadline, and report path.
- Perform required local preflight and independently review the campaign before
  requesting user authorization.
- Interpret results only within the frozen campaign; distinguish reference
  utility from case replay or general B-Rep-to-sequence capability. M146/M150
  development-side material is campaign provenance, never provider or runtime
  authorization.
- Reuse the M155 entry-boundary document as a selection gate only: it fixes the
  required authority inputs and separate-freeze obligations, but does not
  substitute for the egress-safe reference projection or itemized hosted
  authorization.

## Compatibility constraints

No raw STEP, local paths, reference scripts, held-out answers, arbitrary
repository access, or unrestricted retrieval may leave the Harness. Existing
provider, manifest, runtime, and admission authorities remain unchanged unless
a separately selected package explicitly changes one.
The activation package must show whether a reviewed implementation-contract
mapping is required for the selected hypothesis; absence of one is a stop
condition unless a separately reviewed campaign design proves it is not needed.
Documentary evidence may justify why a hypothesis is selected, but cannot be
used as provider reference material or substitute for the egress-safe
reference projection.

## Acceptance

The activated package must define its exact acceptance commands, report schema,
and authorization text after preflight. At minimum it requires the applicable
G2 checks, hosted-preflight evidence, independent review, explicit itemized
authorization, and a terminal report.

## Out of scope

Broad hosted benchmarking, training/fine-tuning, generic retrieval, automatic
runtime promotion, and changing unrelated Harness capabilities.
