# Multi-Inner-Loop-Pocket Development Campaign Charter

- Workpack: `WP-M126-001-multi-inner-loop-pocket-development-campaign-charter`
- Track owner: `modeling-sequence coverage`
- Campaign type: `single-family development`
- Date frozen: `2026-08-11`
- Status: `planning`

## Bounded question

Under the frozen `multi-inner-loop-pocket-v1` development split, can a no-card
hosted run preserve the declared outer-loop and two-inner-island role
dependency, strict containment, and blind-pocket semantics without broadening
to a generic multi-contour or loop-count claim?

Allowed conclusion:
- For the three frozen development rows only, terminal evidence may support one
  finite result about whether this exact two-inner-island blind-pocket family
  can be reconstructed under the declared no-card boundary.

Explicit non-inference:
- No result may support generic multi-contour recognition, arbitrary loop
  counts or shapes, face/edge-referenced dependencies, held-out authority,
  runtime knowledge, or a reusable project-level CAD capability claim.

## Finite case scope

- Scope shape: `frozen family development split`
- Fixed case ids / rows: `param_multi_inner_loop_pocket_centered_low`,
  `param_multi_inner_loop_pocket_centered_nominal`,
  `param_multi_inner_loop_pocket_centered_high`
- Fixed split and order authority:
  `docs/corpus/sequence-paired/multi-inner-loop-pocket-v1-preregistration.json`
  and `docs/architecture/adr/0031-multi-inner-loop-pocket-governance.md`
- Denominator: `3 rows x 1 no-card condition = 3 terminal condition observations`
- Replacement policy: `none`
- Stop rule: `complete all rows unless policy integrity fails or a frozen
  hosted stop rule terminalizes the campaign`

## Limited reference scope

- Q01 outbound facts: one rectangular base top face; one axis-aligned
  rectangular outer loop strictly contained in that face; exactly two distinct
  axis-aligned rectangular inner loops (`inner_left`, `inner_right`) strictly
  contained in the outer loop and non-overlapping; positive clearances; and
  `0 < pocket_depth < base_height`
- Allowed pack/card/material: `none`
- Allowed role or action boundary: one constrained four-step construction
  matching `SketchRect -> ExtrudeBase(+Z) -> SketchPocketLoops(outer,
  inner_left, inner_right) -> CutPocket(blind,-Z)`
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
  `docs/corpus/sequence-paired/multi-inner-loop-pocket-v1-preregistration.json`,
  `docs/corpus/knowledge/operations/multi-inner-loop-pocket-v1.json`,
  `docs/architecture/v1/m26-multi-inner-loop-pocket-evidence-review.md`,
  `docs/architecture/adr/0030-multi-inner-loop-pocket-design.md`,
  `docs/architecture/adr/0031-multi-inner-loop-pocket-governance.md`
- No-input secure-executor preflight source:
  `docs/workflow/m118-fresh-hosted-stability-preflight.md`
- Applicable negative-control or counterexample source:
  `docs/corpus/knowledge/operations/multi-inner-loop-pocket-v1.json`
- Fresh-policy authority:
  `docs/workflow/m126-multi-inner-loop-pocket-development-campaign-charter.md`

The hosted-stability prerequisite is still unmet, so this charter stops before
preflight and authorization.

## Hosted execution boundary

- Destination: `https://api.deepseek.com` if a later G3 package explicitly
  retains the historical provider choice; otherwise re-freeze in that package
- Provider / model: `deepseek / deepseek-v4-pro` on the same condition
- Executor: `wsl-bwrap`
- Policy id: `m126-multi-inner-loop-pocket-development-campaign-v1`
- Request shape: `family campaign`
- Maximum requests: `3`
- Retry / repair policy: `zero`
- Provider deadline: `120 seconds`
- Output cap / other transport bound: `none selected in this charter`
- Planned report path:
  `data/corpus-runs/m126-multi-inner-loop-pocket-development-campaign-report.json`
- Planned monitor path:
  `data/monitor-runs/m126-multi-inner-loop-pocket-development-campaign-monitor.json`

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

This checklist is intentionally unexecuted in M126 because the shared
hosted-stability gate remains unmet.

## Interpretation table

| Terminal outcome | Interpretation |
|---|---|
| `pass` / `full_success` | Finite success for that row only: the declared outer/inner loop roles, strict containment, two-island retention, blind floor, and one-solid semantics remained interpretable within the frozen family boundary. |
| `provider timeout` / lifecycle failure | Unavailable or inconclusive for that row only; no family success claim and no reused capacity. |
| `script/API failure` | Finite failure at the declared multi-loop or blind-pocket API stage only; not a geometry or provider-quality claim. |
| `sandbox/provenance failure` | Finite executor-path failure only; no modeling or family-capability inference. |
| `geometry/semantic/editability gate failure` | Finite downstream failure only; do not broaden it into a generic multi-contour or loop-count claim. |
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

M126 does not request authorization.

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
- Sequence position: `4 of 5`
- Shared framing source: `docs/architecture/v1/current-hosted-evaluation-framing.md`
- Independence rule: each campaign retains its own preflight, authorization,
  report/monitor paths, and terminal review

## Old-route noise check

- Historical route docs consulted:
  `docs/architecture/v1/five-family-hosted-capability-roadmap.md`,
  `docs/architecture/v1/current-hosted-batch-candidate-plan.md`,
  `docs/corpus/knowledge/operations/multi-inner-loop-pocket-v1.json`
- Why they are background only:
  they explain family readiness and loop-role evidence, but do not authorize
  provider use, report reuse, or automatic campaign activation.
- Current controlling records:
  `WP-M126-001`, `docs/workflow/m126-multi-inner-loop-pocket-development-campaign-charter.md`,
  `docs/architecture/v1/current-hosted-evaluation-framing.md`,
  `docs/workpacks/deferred/WP-TRG-005-output-contract-and-repair-correctness.md`

## Next step

Stop and create no provider request from this charter. The next admissible move
is to satisfy the shared hosted-stability gate and then open a fresh
family-scoped G3 readiness/preflight package that either carries this charter
forward unchanged or explicitly supersedes it.
