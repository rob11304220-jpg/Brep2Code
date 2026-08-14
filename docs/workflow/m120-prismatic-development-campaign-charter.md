# Prismatic Development Campaign Charter

- Workpack: `WP-M120-001-prismatic-development-campaign-charter`
- Track owner: `reference-guided parameter variation`
- Campaign type: `single-family development`
- Date frozen: `2026-08-11`
- Status: `planning`

## Bounded question

Under the reviewed M115 development-only successor policy and a frozen three-row
development split, can the card treatment achieve a better declared end-to-end
terminal category than the no-card control without reusing M97 or M118
capacity?

Allowed conclusion:
- For the frozen three development rows only, terminal evidence may support one
  finite observed treatment advantage at the preregistered stage named by the
  M115 policy.

Explicit non-inference:
- No result may support held-out authority, generic parameter generalization,
  model capability, runtime knowledge, or a reusable project-level CAD claim.

## Finite case scope

- Scope shape: `frozen family development split`
- Fixed case ids / rows: `param_reference_guided_through_hole_development_low`,
  `param_reference_guided_through_hole_development_nominal`,
  `param_reference_guided_through_hole_development_high`
- Fixed split and order authority:
  `docs/corpus/sequence-paired/reference-guided-through-hole-variation-v1-preregistration.json`
  and `docs/corpus/registry/m115-prismatic-development-card-effect-policy-v1.json`
- Denominator: `3 rows x 2 paired conditions = 6 terminal condition observations`
- Replacement policy: `none`
- Stop rule: `complete all rows unless policy integrity fails or a frozen hosted stop rule terminalizes the campaign`

## Limited reference scope

- Q01 outbound facts: `m97-measured-through-hole-facts-v1` measured-fact
  transcript boundary: `base_bbox`, `cylindrical_cut.radius`,
  `cylindrical_cut.axis`, `cylindrical_cut.center_xy`,
  `cylindrical_cut.extent`
- Allowed pack/card/material: exact `single boolean-cut tool` derived card
  boundary with historical guidance index SHA-256
  `dfa731d597581b3b4d306782c1078c7de5b79672462229baaf5d7248fa230517`
  and card SHA-256
  `55341683e3e7df3e058a845193e34fba20b0650c0db28a31489ad5d343b60d30`,
  or `none` for the no-card control
- Allowed role or action boundary: one rectangular base plus one +Z
  cylindrical through-cut action under the M115 static API-admissibility
  classifier
- Forbidden outbound material:
  - raw STEP
  - local paths / filenames
  - full reference scripts
  - prior provider responses
  - held-out answers
  - post-result card or prompt edits

## Offline prerequisites

- Historical hosted-stability gate: superseded as an entry condition by the
  current three-case closed-loop route.
  Source: `docs/workflow/workpack-route-disposition-index.md` and
  `docs/architecture/v1/current-project-route.md`
- Dossier / family release / card qualification source:
  `docs/corpus/sequence-paired/reference-guided-through-hole-variation-v1-preregistration.json`,
  `docs/architecture/v1/four-track-program-roadmap.md`, and
  `docs/corpus/registry/m115-prismatic-development-card-effect-policy-v1.json`
- No-input secure-executor preflight source:
  `docs/workflow/m97-003-reference-guided-development-hosted-preflight.md`
- Applicable negative-control or counterexample source:
  `docs/workflow/m97-004-development-terminal-attribution-review.md`
- Fresh-policy authority:
  `docs/corpus/registry/m115-prismatic-development-card-effect-policy-v1.json`

The hosted-stability prerequisite is still unmet, so this charter stops before
preflight and authorization.

## Hosted execution boundary

- Destination: `https://api.deepseek.com` if a later G3 package explicitly
  retains the historical provider choice; otherwise re-freeze in that package
- Provider / model: `deepseek / deepseek-v4-pro` on the same condition
- Executor: `wsl-bwrap`
- Policy id: `m115-prismatic-development-card-effect-v1`
- Request shape: `family campaign`
- Maximum requests: `6`
- Retry / repair policy: `zero`
- Provider deadline: `120 seconds`
- Output cap / other transport bound: `none selected in this charter`
- Planned report path:
  `data/corpus-runs/m115-prismatic-development-card-effect-v1-m120-development-campaign-report.json`
- Planned monitor path:
  `data/monitor-runs/m115-prismatic-development-card-effect-v1-m120-development-campaign-monitor.json`

These fields are planning-only. A later G3 workpack must either retain them
unchanged through fresh preflight and itemized authorization or replace them
explicitly with a new frozen boundary.

## Preflight checklist

- [ ] Input SHA-256 values match the frozen case scope.
- [ ] Manifest / split / row membership matches the frozen scope.
- [ ] Q01 outbound transcript or measured-fact contract matches the frozen text/hash.
- [ ] Pack/card/index hashes match the frozen authority.
- [ ] Secure no-input `wsl-bwrap` control passed locally.
- [ ] Non-secret provider configuration and exact model selection are present.
- [ ] CLI accounting matches the planned request bound.
- [ ] Deadline and any output/token cap are valid and enforced locally.
- [ ] Report and monitor paths are fresh and absent before prepare.
- [ ] The campaign's interpretation table is frozen before authorization.

This checklist is intentionally unexecuted in M120 because the shared
hosted-stability gate remains unmet.

## Interpretation table

| Terminal outcome | Interpretation |
|---|---|
| `pass` / `full_success` | Finite success for that condition only; compare against its paired control using the M115 policy and no broader claim. |
| `provider timeout` / lifecycle failure | Unavailable or inconclusive for that condition; no treatment advantage and no reused capacity. |
| `script/API failure` | Finite failure at the declared static-API stage only; not a geometry or provider-quality claim. |
| `sandbox/provenance failure` | Finite executor-path failure only; no treatment or modeling inference. |
| `geometry/semantic/editability gate failure` | Finite downstream failure only; no treatment advantage unless the paired condition reaches a later declared stage under M115. |
| `interrupted` | partial evidence only; not a terminal campaign result |

## Authorization payload

Request approval only for:

- destination and model;
- exact outbound content class;
- exact case scope or family split;
- exact request cap;
- retry/repair bound;
- provider deadline;
- output/token cap if used;
- executor;
- fresh report/monitor paths.

M120 does not request authorization.

## Terminal review payload

After execution, record:

- requests issued / remaining;
- terminal lifecycle status;
- script/API result;
- sandbox/provenance result;
- geometry/semantic/editability gate states, using `not evaluated` where needed;
- one allowed conclusion;
- one explicit non-inference;
- registry/portfolio attachment target after independent review.

## Batch sequencing note

This campaign is part of a planned batch: `yes`

If yes:
- Batch name: `five-family hosted candidate sequence`
- Sequence position: `5 of 5`
- Shared framing source: `docs/architecture/v1/current-hosted-evaluation-framing.md`
- Independence rule: each campaign retains its own preflight, authorization,
  report/monitor paths, and terminal review

## Old-route noise check

- Historical route docs consulted:
  `docs/workflow/m97-reference-guided-development-hosted-preflight.md`,
  `docs/workflow/m97-003-reference-guided-development-hosted-preflight.md`,
  `docs/workflow/m112-parameter-variation-held-out-readiness-review.md`
- Why they are background only:
  they explain the prior M97/M112 route and its terminal boundaries, but they
  do not authorize provider use, report reuse, or revival of the old held-out
  trigger line.
- Current controlling records:
  `WP-M120-001`, `docs/corpus/registry/m115-prismatic-development-card-effect-policy-v1.json`,
  `docs/architecture/v1/current-hosted-evaluation-framing.md`,
  `docs/workpacks/deferred/WP-TRG-005-output-contract-and-repair-correctness.md`

## Next step

Stop and create no provider request from this charter. The next admissible move
is to satisfy the shared hosted-stability gate and then open a fresh
family-scoped G3 readiness/preflight package that either carries this charter
forward unchanged or explicitly supersedes it.
