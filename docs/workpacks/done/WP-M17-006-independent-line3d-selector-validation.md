# WP-M17-006: Independent Line3D Selector Validation

- Status: done
- Milestone: M17
- Owner: unassigned

## Goal

Test the frozen M17-005 Line3D selector on a small, independent Fusion
population before considering any change to the strict default replay path.

## Attribution question and sampling intent

**Question:** Does the unchanged profile-normal / STEP-projection /
extent-boundary selector retain existing geometry-gate outcomes on unseen,
source-family-isolated Line3D cases from the already cached Fusion release?

**Pre-registered selection:** inspect at most official-train source-order
positions 201--400 and official-test source-order positions 1--200, skipping every
case and source family used in M14 through M17-005. Select the first two
strict-subset-accepted Line3D development cases from distinct source families
and the first one strict-subset-accepted Line3D held-out case from a third
family. Each requires final STEP and native JSON, a single Sketch, a single
zero-taper one-sided NewBody distance extrude, and one outer Line3D loop. If a
slot is absent within either fixed bound, or strict selector inputs reject, stop
and record that outcome; do not extend the scan, replace the rule, add syntax
or alter the selector.

**Expected information gain:** distinguish a four-case-local selector fit from
a frozen mapping that retains its result on independently selected Line3D
families. The original M17-005 four cases are excluded from both selection and
gate counting.

## Validation matrix

| Row | Selected cases | Mapping | Required outcome |
|---|---|---|---|
| Strict baseline | all selected | existing listed-order / `z_axis` replay | Record gates without treating a failure as selector evidence. |
| Frozen selector | all selected | endpoint ordering plus unchanged M17-005 selector | Every selected row passes existing bbox, volume and topology gates. |
| Rejection | any selected candidate | selector ambiguity, no match, non-boundary profile, or non-closing loop | Reject before STEP write and stop; no fallback or healing. |

## Compatibility constraints

Offline only; use only the existing ignored local Fusion cache. Do not change
the selector, strict default replay, gates, manifests, CLI/schema, corpus,
provider/hosted behavior, prompts/tools, or M18. No new download or source
dataset is permitted.

## Acceptance

- A tracked selection record contains source order, official split, family,
  SHA-256 and subset-admission result for every selected row.
- An ignored local report records strict and selector gate outcomes.
- Every frozen-selector row passes the unchanged three geometry gates, or the
  workpack stops and records the first failure without a replacement.
- Status, roadmap, corpus records and handoff agree; tests, Ruff and JSON
  parsing pass for changed code and records.

## Result

**Completed.** The deterministic selection record chose train positions 215
and 242 as two development families and test position 31 as a held-out family;
all are disjoint from M14--M17-005 and from each other. The frozen selector
passed bbox, volume and topology gates for all three rows. Strict replay passed
the first development and held-out rows, but failed volume and topology gates
for development `136900_4fe212e6_0010`; the frozen selector passed that row.

This adds 2 development and 1 held-out independent observations to M17-005's
fixed four, but does not promote the selector to default replay. A separate
mapping-policy review is required before any such decision.

## Status transition

On completion, update this workpack, `docs/workflow/status.md`, the active
handoff, the Fusion roadmap, corpus records and `docs/workpacks/README.md`.
Write an ADR only if a default mapping-policy decision is adopted.

## Out of scope

Promoting the selector to the default parser, new replay syntax, source scans
outside the pre-registered window, manifest/corpus/provider use, hosted work,
DeepCAD, M18 and generic coordinate-frame inference.
