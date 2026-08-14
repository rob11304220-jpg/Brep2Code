# WP-M88-001: Reference-assisted Case Ladder and Workpack Allocation

- Status: done
- Milestone: M88
- Owner: Codex
- Reviewer: not required (G1)
- Risk tier: G1

## Goal

Freeze a bounded development-case ladder and the workpack allocation required
to test reference-assisted observation-to-build loops from the already
validated vertical-cylinder roles toward new mechanism families. This is a
planning and governance change only: it does not create a card, change the
Harness, or make a hosted request.

## Scope

- Record the evidence boundary of M85, M86, and M87.
- Allocate the next hosted smoke and each required offline card-qualification
  increment for the seven reference-packed P0/P1 cases.
- Define the admission boundary before any of the 68 active P2/P3 cases may
  enter this route.
- Keep M89 as the sole immediately selectable execution package.

## Attribution question and sampling intent

Distinguish reuse of an already-qualified card in a new declared role from a
new-card or new-mechanism claim. The first increment is one fixed
`three_hole_plate` case, selected because its `repeated boolean-cut tool` role
already passed M86 deterministic fake-provider admission. Stop at its terminal
result; no failure can be replaced by another case.

## Inputs

- `docs/workpacks/done/WP-M85-001-reference-assisted-p0-hosted-smoke.md`
- `docs/workpacks/done/WP-M86-001-multi-role-reference-assisted-offline-admission.md`
- `docs/workpacks/done/WP-M87-001-reference-assisted-p0-block-with-hole-hosted-smoke.md`
- `docs/corpus/reference-packs/reference-pack-contract-v1.json`
- `docs/corpus/registry/self-authored.json`

## Allocated ladder

The sequence is ordered by *incremental evidence readiness*, not only feature
geometry. `box` is geometrically simpler than repeated cuts but needs a new
card; `three_hole_plate` is therefore the next evidence increment because it
reuses an admitted role/card without broadening retrieval.

| Order | Proposed workpack | Risk | Fixed case/mechanism | Required outcome before next item |
|---|---|---:|---|---|
| completed | M85 | G3 | `cylinder` / final primitive | Two-request terminal pass. |
| completed | M87 | G3 | `block_with_hole` / single boolean cut | Two-request terminal pass. |
| 1 | M89 reference-assisted P1 repeated-cut hosted smoke | G3 | `three_hole_plate` / repeated boolean cut | Fresh preflight and one terminal two-request result using only `vertical-cylinder-construction`. |
| 2a | M90 box-construction card qualification | G2 | `box` / axis-aligned box primitive | Source-linked card, fixed role, negative controls, and fake-provider acceptance; no hosted request. |
| 2b | M91 box reference-assisted hosted smoke | G3 | `box` / axis-aligned box primitive | One fresh, terminal, no-retry hosted smoke of the M90-qualified role/card. |
| 3a | M92 additive-fuse card qualification | G2 | `box_cylinder_union` / additive boolean fuse | One source-linked additive-fuse card and fixed-role offline admission. |
| 3b | M93 additive-fuse hosted smoke | G3 | `box_cylinder_union` / additive boolean fuse | One fresh, terminal, no-retry hosted smoke. |
| 4a | M94 single-edge-fillet card qualification | G2 | `filleted_block` / verified-edge fillet | Edge-selection evidence and one source-linked card; ambiguity controls must fail closed. |
| 4b | M95 single-edge-fillet hosted smoke | G3 | `filleted_block` / verified-edge fillet | One fresh, terminal, no-retry hosted smoke. |
| 5a | M96 single-edge-chamfer card qualification | G2 | `chamfered_block` / verified-edge-and-face chamfer | Edge/face-reference evidence and one source-linked card; ambiguity controls must fail closed. |
| 5b | M97 single-edge-chamfer hosted smoke | G3 | `chamfered_block` / verified-edge-and-face chamfer | One fresh, terminal, no-retry hosted smoke. |
| 6 | M98 P2/P3 reference-pack taxonomy and sampling design | G1 | P2/P3 mechanism families | Freeze one mechanism-family sample, splits, reference-pack/card requirements, and stopping rule; no hosted request. |

P2/P3 admission is deliberately not preallocated case-by-case. M98 must first
cluster the active registry into bounded mechanism families, select one
development case per newly supported family, and create separate G2
qualification plus G3 smoke workpacks. Parameter variants are not independent
hosted substitutes for an unsuccessful nominal case.

## Post-M89 amendment

M89-001 reached a terminal request-specific timeout at the second provider
boundary. Before any retry or transition to the planned M90--M98 ladder, the
user selected `WP-M89-002-provider-lifecycle-observability-diagnosis` (G2,
offline only). It is a prerequisite diagnostic, not a replacement case or a
retry: it may add bounded transport timing and token-limit contract evidence,
but cannot alter M89-001's result or authorize hosted egress.

## Code paths

None. Future G2/G3 workpacks must name their exact Harness, CLI, card, test,
and report paths before implementation.

## Docs to update

- `docs/workflow/status.md`
- this workpack
- `docs/handoff/active/2026-08-10-reference-assisted-case-ladder.md`

## Trace/schema changes

None. Future hosted workpacks must retain the current two-request report,
selected role/card, index hash, sandbox/provenance, and geometry-gate trace
contract unless their own G2 workpack explicitly changes and validates it.

## Decision-package impact

- `decision_id`: none; bounded development planning.
- Q01/Q02 effect: no observation or sequence hypothesis changes; the plan
  constrains future tests to declared roles and source-linked cards.
- Q03/Q04 effect: no gate or repair disposition changes; all planned hosted
  smokes remain terminal on failure with zero retry and zero repair.
- Evidence role: planning index for future development regression evidence.
- Knowledge disposition: no reusable knowledge; no card is created or
  promoted by this workpack.

## Compatibility constraints

Default execution remains offline and credential-free. M85 stays fixed to
`cylinder`; M87 stays fixed to `block_with_hole`. This plan does not authorize
broad retrieval, manifest changes, prompt/model comparisons, provider use,
external data, repair, retry, or report-path reuse.

## Acceptance

```powershell
uv run python -m pytest -m fast -q
uv run python tools/check_governance.py
git diff --check
```

## Evidence reuse / guidance-card disposition

M89 may reuse only the already-qualified,
`vertical-cylinder-construction` card in its declared repeated-cut role. M90,
M92, M94, and M96 must each independently choose exactly one disposition:
source-linked experience card, counterexample, or no reusable evidence. A
qualification pass does not authorize hosted use; its paired G3 smoke requires
new preflight and explicit user authorization.

## Status transition

On closure, update `docs/workflow/status.md` first, archive the active
handoff if no workpack remains active, and move this file to `done/`. Record
the validation output and the user-selected next package. No ADR is required:
this workpack records an execution allocation, not a lasting architecture
decision.

## Closure rationale

The ladder and workpack allocation are frozen without behavioral or hosted
side effects. On 2026-08-10, `uv run python -m pytest -m fast -q` passed
(`64 passed, 141 deselected`), `uv run python tools/check_governance.py`
passed, and `git diff --check` passed. G1 owner review confirmed status,
workpack, and handoff alignment. M89 remains a user-selectable future package,
not an implied provider authorization.

## Out of scope

- Implementing M89 or any later package.
- Creating, editing, or promoting guidance cards.
- Changing CLI commands, contracts, manifests, gates, provider configuration,
  or runtime retrieval.
- Any hosted provider request or authorization request.

## Repair hypothesis and evaluation boundary

This is offline planning only. It makes no repair hypothesis and cannot claim
quality improvement or generalization. Each planned hosted comparison must
have its own trace-supported hypothesis, fixed case/card, preflight, explicit
authorization, fresh report path, and terminal stopping rule.

## Notes

M89 is intentionally the next candidate: it tests the third and last
offline-admitted role of the current card. The subsequent order broadens one
mechanism/card boundary at a time, separating offline qualification from
hosted evidence.
