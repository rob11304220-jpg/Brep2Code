# WP-TRG-039: Closed-Loop Release Freeze

- Status: deferred
- Owner: unassigned
- Reviewer: independent reviewer required
- Risk tier: G2

## Entry condition

The user selects this workpack after M157 closure. The activation package must
cite the current status, M139 frozen-campaign launcher, M140 tool-turn
contract, M141 classified-repair policy, M19-003 guidance boundary, M155
runtime/hosted entry boundary, and this trigger. It remains offline,
development-only and credential-free.

## Goal

Freeze one reusable, fail-closed closed-loop Harness release for a later
three-case hosted evaluation: bounded Q01 tools and one explicit card, initial
script generation, restricted execution/gates, classified terminal feedback,
and at most one admitted source-only repair.

## Scope

- Freeze exactly `cylinder`, `block_with_hole`, and `three_hole_plate`, in that
  order, with registered hashes and development split authority. No held-out
  case, substitution, or new case is allowed.
- Freeze the corresponding one-card roles: `final primitive`, `single
  boolean-cut tool`, and `repeated boolean-cut tool`. Bind the existing
  `vertical-cylinder-construction` card by exact card/index hashes, one path,
  and its compatible role.
- Integrate only necessary M139/M140/M141 interfaces into one offline release
  contract and fake-provider path. Record observation/card calls, initial
  generation, classification, optional repair, successor execution, gates,
  request accounting and terminal reason.
- Freeze one declared Q01 observation call and one declared card call before
  initial generation: two provider tool-request completions, then one complete
  script completion, plus at most one repair-edit completion. Freeze those four
  maximum provider completions per case, Q01 schemas, tool/byte limits, OCP
  instruction, `wsl-bwrap` no-input executor, unchanged gates, deadline and
  output cap. Transcripts remain path-free and exclude raw STEP, reference
  scripts, raw gate logs, provider responses, credentials and held-out data.
- Allow at most one `source_only` edit after `static_api_contract`,
  `output_artifact`, or `execution_local`. Selector ambiguity,
  geometry/semantic/editability, sandbox/provenance, timeout, protocol and
  mixed/unknown terminate with zero repair. No retry, full replacement after
  feedback, sequence/IR edit, prompt/card change or case replacement.
- Add fake-provider coverage for direct pass, admitted repair, plateau and all
  fail-closed categories; do not construct a provider or issue a request.

## Attribution question and sampling intent

Distinguish whether the existing launcher, tool-turn and classified-repair
components form one auditable release before external execution. It adds no
efficacy sample or model/card claim. Stop if integration requires a new tool,
changed gate, broader card/retrieval behavior, repair route, case/manifest
change, or provider construction.

## Decision-package impact

- `decision_id`: none; release/campaign integration only.
- Q01/Q02 effect: freezes existing interfaces; no semantic change.
- Q03/Q04 effect: freezes M141 classification and stop policy; no new repair.
- Evidence role: offline regression and release-readiness evidence only.
- Knowledge disposition: no reusable knowledge or runtime-card promotion.

## Compatibility constraints

Default operation remains offline. Cards remain absent by default and are
returned only through the explicit hash-bound single-card bridge, never prompt
injected or directory-retrieved. M135 evidence, manifests, case lifecycle,
provider configuration, training, SDK/IR and held-out boundaries are unchanged.

## Acceptance

The activated package must define focused integration tests, Ruff, applicable
offline validation, runtime-guidance and governance audits, and diff check. It
must publish a reviewed release/dossier record naming frozen hashes, limits,
schemas and stop rules.

## Out of scope

Provider/hosted calls, credentials, new cards, retrieval, new or held-out
cases, model comparison, prompt tuning, gate changes, generic repair, and
sequence/IR editing.
