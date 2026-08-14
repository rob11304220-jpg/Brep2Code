# WP-M17-004: Fusion Line3D Frame-Evidence Audit

- Status: done
- Milestone: M17
- Owner: unassigned

## Goal

Determine whether the fixed Fusion Line3D evidence can distinguish a safe,
explicit replay-direction selector before any parser change or additional case
selection.

## Attribution question and sampling intent

M17-003 showed that endpoint-continuous `ordered_y` exactly reconstructs the
fixed held-out case but degenerates every existing Line3D control. The open
question is whether native-history transform, profile-loop or extent metadata
already contains a deterministic signal that separates the held-out mapping
from the three controls.

The population is fixed and exhaustive for this audit: M14 Line3D development
`100243_9fb796fe_0005` and `100877_ac1e5a17_0001`, M17 Line3D development
`145540_a4f54d5f_0010`, and M17 held-out `41026_295d1dc8_0003`. No source scan,
sample replacement or new dataset is allowed.

## Scope

- Emit an ignored local JSON/Markdown evidence table for all four cases.
- Record only existing JSON and STEP facts: sketch origin and normalized
  `x_axis`/`y_axis`/`z_axis`, handedness/dot-product checks, Line3D endpoint
  continuity and traversal orientation, extent sign/distance, and input STEP
  bbox extent projected onto each explicit signed sketch axis.
- Compare these fields with the already observed strict-`z_axis` and
  endpoint-ordered-`y_axis` gate outcomes; state which candidate selectors are
  contradicted, indistinguishable or supported by every fixed case.
- Produce a bounded decision: either nominate one explicitly stated selector
  for a separate promotion workpack, or state the smallest preregistered
  additional evidence needed to distinguish remaining hypotheses.

## Compatibility constraints

Offline only. Do not alter replay/parser behavior, gates, manifests, corpus
selection, fixtures, CLI/schema, prompts, LLM tools, provider settings or
runtime behavior. Do not run a treatment replay, corpus run, hosted request or
M18 audit in this workpack.

## Acceptance

- All four fixed Line3D cases have SHA-256-linked evidence rows.
- Every reported scalar is derived from existing local JSON/STEP material and
  names its source field or probe.
- The conclusion explicitly distinguishes evidence for a selector from a
  case-specific fit; it must not promote code.
- The report and status/handoff agree, JSON parses, and the audit tool passes
  Ruff if a Python tool is added.

## Result

**Completed.** The fixed, hash-linked four-case audit found a unique candidate
direction in every row: `+z_axis` for all three development controls and
`+y_axis` for held-out `41026_295d1dc8_0003`. The selector combines the
endpoint-ordered profile normal, the input STEP bbox span projected onto each
sketch axis, the source extent magnitude and the profile projection boundary.
The held-out case alone has non-continuous listed endpoints, so listed order is
not used as a direction selector.

This nominates a separately scoped promotion workpack only. It does not change
the parser or replay mapping: M17-003's unconditional `ordered_y` control
regression remains disqualifying. The ignored local evidence is reproducible
with `uv run python tools/audit_fusion360_m17_frame.py`; its JSON parses and
the tool passes Ruff.

## Status transition

On completion, update `docs/workflow/status.md`, this workpack, the active
handoff, `docs/workpacks/README.md`, and the Fusion roadmap/corpus records.
Write an ADR only if a lasting mapping-policy decision is actually adopted.

## Out of scope

Generic coordinate-frame inference, production parser changes, arcs, splines,
inner loops, Join/Cut, multiple extrudes, new Fusion selection, DeepCAD,
corpus evaluation, provider/hosted use, and LLM prompt/tool updates.
