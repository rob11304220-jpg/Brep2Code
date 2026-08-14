# WP-M105-001: Revolve Family Design Freeze

- Status: done
- Milestone: M105
- Owner: Codex
- Reviewer: Liaol
- Risk tier: G2

## Goal

Freeze one `revolve-v1` axisymmetric grammar before any candidate asset is
produced.

## Scope

Define profile, axis, direction, angle, rows/split, deterministic oracle, Q01
facts, allowed Q02 OCP action, geometry/semantic/editability gates and
wrong-axis/partial-angle/degenerate-profile controls. Use the family intake
contract and stop if the facts cannot be stated without broad parser or IR
work.

## Attribution question and sampling intent

Distinguish whether one bounded axisymmetric construction grammar can have its
minimum observable facts, deterministic oracle, split and counterexamples
frozen before production. The package stops with no design freeze if that
question requires broad parser or IR work; it does not sample or produce cases.

## Inputs

- `docs/corpus/sequence-paired/family-intake-template.json`
- Existing sequence-paired family design records and their audits
- `docs/architecture/v1/five-family-hosted-capability-roadmap.md`

## Docs to update

- The new `revolve-v1` family-intake/design-freeze artifact
- `docs/architecture/adr/0063-revolve-v1-design-freeze.md`
- `docs/workflow/status.md`, this workpack and its active handoff
- Only any directly affected portfolio navigation or architecture record

## Trace/schema changes

None expected. This work may create an offline design artifact but must not
change `signal_bundle.json`, provider/tool traces, manifests, storage layout,
CLI output or runtime resources.

## Decision-package impact

- `decision_id`: none yet; design freeze precedes a bounded Q01--Q04 package.
- Q01/Q02 effect: freezes proposed axis/profile facts and one constrained OCP
  action without implementing either runtime capability.
- Q03/Q04 effect: freezes proposed gates and stop rule without changing them.
- Evidence role: planned oracle and negative-control design only.
- Knowledge disposition: no reusable knowledge unless a later independent
  production/review package establishes it.

## Compatibility constraints

No candidate production, case admission, manifest/runtime/card change,
provider use, hosted authorization, or sweep/loft, shell or rib scope. Default
network-free behavior and all existing lifecycle authorities remain unchanged.

## Acceptance

```powershell
uv run python tools\audit_sequence_paired_intake.py docs\corpus\sequence-paired\revolve-v1-preregistration.json
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

## Owner acceptance

- 2026-08-11: `uv run python tools/audit_sequence_paired_intake.py
  docs/corpus/sequence-paired/revolve-v1-preregistration.json` passed.
- 2026-08-11: `uv run python -m pytest -m fast -q` passed (66 passed), and
  `uv run python -m ruff check .` passed.
- The preregistration freezes six rows: `revolve_centered` only in development
  and `revolve_offset` only in held_out. No producer output, case directory,
  manifest, provider request or runtime resource was created.

## Review required

Liaol must independently verify the bounded stepped-radial full-revolution
grammar, three/three family-isolated split, no-substitution rule, the
wrong-axis/partial-angle/degenerate-profile controls, the explicit
full-revolution direction boundary, no assets/manifest/provider/runtime
changes, and the recorded acceptance commands before closure.

## Independent review and closure

- Reviewer: Liaol
- Status: approved on 2026-08-11.
- Review scope: confirmed the bounded stepped-radial full-revolution grammar,
  three/three family-isolated split, no-substitution rule, declared negative
  controls, full-revolution direction boundary, passing acceptance evidence,
  and absence of assets, manifest, provider or runtime changes.
- Closure rationale: M105-001 freezes only a future controlled-production
  contract. It creates no direct-case evidence, runtime knowledge or hosted
  authority; any production remains separately user-selected.

## Status transition

Update `docs/workflow/status.md` first. After owner acceptance, obtain Liaol's
independent review before closure; then archive the handoff and move this
workpack to `done/`.

## Out of scope

Candidate production, case admission, manifest/runtime/card changes, provider
use, hosted authorization, sweep/loft, shell or rib.
