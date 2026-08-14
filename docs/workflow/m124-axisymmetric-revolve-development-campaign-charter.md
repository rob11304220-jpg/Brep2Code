# Axisymmetric-Revolve Development Campaign Charter

- Workpack: `WP-M124-001-axisymmetric-revolve-development-campaign-charter`
- Track owner: `modeling-sequence coverage`
- Campaign type: `single-family development`
- Date frozen: `2026-08-11`
- Status: `planning`

## Bounded question

Under the frozen `revolve-v1` development split, can a no-card hosted run
preserve the declared stepped-radial profile, axis-relative bore, full
360-degree revolve extent and two-radius axisymmetric exterior without
broadening to a generic revolve or profile-recovery claim?

Allowed conclusion:
- For the three frozen development rows only, terminal evidence may support one
  finite result about whether this exact full-revolution stepped-radial family
  can be reconstructed under the declared no-card boundary.

Explicit non-inference:
- No result may support generic revolve recognition, signed-direction recovery,
  arbitrary profiles or axes, held-out authority, runtime knowledge, or a
  reusable project-level CAD capability claim.

## Finite case scope

- Scope shape: `frozen family development split`
- Fixed case ids / rows: `param_revolve_centered_low`,
  `param_revolve_centered_nominal`, `param_revolve_centered_high`
- Fixed split and order authority:
  `docs/corpus/sequence-paired/revolve-v1-preregistration.json` and
  `docs/architecture/adr/0064-revolve-family-governance.md`
- Denominator: `3 rows x 1 no-card condition = 3 terminal condition observations`
- Replacement policy: `none`
- Stop rule: `complete all rows unless policy integrity fails or a frozen
  hosted stop rule terminalizes the campaign`

## Limited reference scope

- Q01 outbound facts: one planar closed six-segment stepped-radial profile in
  the XZ plane, expressed only by `inner_radius`, `lower_outer_radius`,
  `upper_outer_radius`, `lower_height`, `upper_height`, and `z_min`; one
  declared axis line with origin `(axis_x, 0, z_min)` parallel to `+Z`; one
  full `360.0` degree extent; and the requirement that the profile remains
  entirely on the positive radial side of the declared axis
- Allowed pack/card/material: `none`
- Allowed role or action boundary: one constrained two-step construction
  matching `SketchSteppedRadialProfile(XZ, positive radial side) ->
  RevolveFace(axis parallel +Z, angle=360.0)`
- Forbidden outbound material:
  - raw STEP
  - local paths / filenames
  - full reference scripts
  - prior provider responses
  - held-out answers
  - post-result card or prompt edits

## Offline prerequisites

- Hosted-stability gate status: `unmet`
  Source: `docs/workpacks/deferred/WP-TRG-005-output-contract-and-repair-correctness.md`
  and `docs/architecture/v1/four-track-program-roadmap.md`
- Dossier / family release / card qualification source:
  `docs/corpus/sequence-paired/revolve-v1-preregistration.json`,
  `docs/architecture/v1/m107-revolve-family-evidence-review.md`,
  `docs/architecture/adr/0063-revolve-v1-design-freeze.md`,
  `docs/architecture/adr/0064-revolve-family-governance.md`
- No-input secure-executor preflight source:
  `docs/workflow/m118-fresh-hosted-stability-preflight.md`
- Applicable negative-control or counterexample source:
  `docs/corpus/sequence-paired/revolve-v1-preregistration.json`
- Fresh-policy authority:
  `docs/workflow/m124-axisymmetric-revolve-development-campaign-charter.md`

The hosted-stability prerequisite is still unmet, so this charter stops before
preflight and authorization.

## Hosted execution boundary

- Destination: `https://api.deepseek.com` if a later G3 package explicitly
  retains the historical provider choice; otherwise re-freeze in that package
- Provider / model: `deepseek / deepseek-v4-pro` on the same condition
- Executor: `wsl-bwrap`
- Policy id: `m124-axisymmetric-revolve-development-campaign-v1`
- Request shape: `family campaign`
- Maximum requests: `3`
- Retry / repair policy: `zero`
- Provider deadline: `120 seconds`
- Output cap / other transport bound: `none selected in this charter`
- Planned report path:
  `data/corpus-runs/m124-axisymmetric-revolve-development-campaign-report.json`
- Planned monitor path:
  `data/monitor-runs/m124-axisymmetric-revolve-development-campaign-monitor.json`

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

This checklist is intentionally unexecuted in M124 because the shared
hosted-stability gate remains unmet.

## Interpretation table

| Terminal outcome | Interpretation |
|---|---|
| `pass` / `full_success` | Finite success for that row only: the declared profile, axis-relative bore, full-revolution topology, and two-radius exterior remained interpretable within the frozen family boundary. |
| `provider timeout` / lifecycle failure | Unavailable or inconclusive for that row only; no family success claim and no reused capacity. |
| `script/API failure` | Finite failure at the declared profile-or-revolve API stage only; not a geometry or provider-quality claim. |
| `sandbox/provenance failure` | Finite executor-path failure only; no modeling or family-capability inference. |
| `geometry/semantic/editability gate failure` | Finite downstream failure only; do not broaden it into a generic revolve or axis/profile-recovery claim. |
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

M124 does not request authorization.

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
- Sequence position: `2 of 5`
- Shared framing source: `docs/architecture/v1/current-hosted-evaluation-framing.md`
- Independence rule: each campaign retains its own preflight, authorization,
  report/monitor paths, and terminal review

## Old-route noise check

- Historical route docs consulted:
  `docs/architecture/v1/five-family-hosted-capability-roadmap.md`,
  `docs/architecture/v1/current-hosted-batch-candidate-plan.md`
- Why they are background only:
  they explain family readiness and prior route alignment, but do not authorize
  provider use, report reuse, or automatic campaign activation.
- Current controlling records:
  `WP-M124-001`, `docs/workflow/m124-axisymmetric-revolve-development-campaign-charter.md`,
  `docs/architecture/v1/current-hosted-evaluation-framing.md`,
  `docs/workpacks/deferred/WP-TRG-005-output-contract-and-repair-correctness.md`

## Next step

Stop and create no provider request from this charter. The next admissible move
is to satisfy the shared hosted-stability gate and then open a fresh
family-scoped G3 readiness/preflight package that either carries this charter
forward unchanged or explicitly supersedes it.
