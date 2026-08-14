---
type: review
related-project: Brep2Code
status: completed
---

> Historical review snapshot. Its backlog table records the M21 decision-time
> state; current work routing is controlled by
> [`docs/workflow/status.md`](../../workflow/status.md) and the current
> four-track roadmap.

# M21-003 Review: Cross-Family Sequence-Pair Governance

## Scope

This review closes the M20/M21 development-document loop and compares the
completed `prismatic-hole-v1` and `rounded-slot-v1` deterministic-oracle
families. It does not register, promote, move, or otherwise change any case
asset, executable manifest, provider input, training input, or runtime
resource.

## Evidence comparison

| Dimension | `prismatic-hole-v1` | `rounded-slot-v1` | Review finding |
|---|---|---|---|
| Frozen design before production | 9 rows, 6 development / 3 held-out, three family IDs | 6 rows, 3 development / 3 held-out, two family IDs | Both preserve family-isolated splits and prohibit substitutions. |
| Construction boundary | Base extrusion plus one circular through/blind/counterbore cut | Base extrusion plus a second composite rounded-slot profile and through cut | M21 independently exercises a profile dependency not present in M20. |
| Geometry and sequence evidence | All nine rows pass deterministic replay and exact canonical sequence checks | All six rows pass deterministic replay and exact four-operation dependency checks | Both satisfy the same three-layer evidence discipline. |
| Editability | Base-length plus hole/bore mutations pass | Base-length, slot-width, and straight-length mutations pass | Both show executable, semantically directional mutations. |
| Stability and negative controls | Counterbore producer is hash-stable; mismatch-sequence and split-leak controls reject | Offset-slot producer is hash-stable; semantic-degeneration and split-leak controls reject | M21 adds explicit composite-profile anti-degeneration evidence. |
| Provenance and scope | Self-authored deterministic reference | Self-authored deterministic reference | Neither family is native history, B-Rep-to-sequence inference, provider evidence, or a general IR. |

## Interpretation

The two independent families establish that the catalog → deterministic
candidate producer → three-layer audit → review discipline can preserve both
a circular-cut semantic family and a second-profile composite-cut family.
This is enough to propose a narrowly scoped `rounded-slot-v1` governance
promotion workpack.

It is not evidence for generic sequence recovery, automatic data mining,
training data admission, manifest admission, provider use, runtime retrieval,
or a general construction representation. The sample counts remain small and
all sequences are deterministic self-authored oracles.

## Document closure audit

- `docs/workflow/status.md` remains the only dynamic status authority.
- Completed workpacks and handoffs are in `done/` and `archive/`; active
  records are reserved for the current workpack.
- ADRs retain long-lived rationale, module/contract pages retain stable
  boundaries, and runbooks retain repeatable procedures.
- `document-governance.md` now records the document layers and the required
  closure/promotion distinction for future agents.

## Backlog disposition

| Workpack | Disposition | Reason |
|---|---|---|
| M10-002 geometry diagnostics | retain, deferred | Its three-case readable-output geometry-failure trigger is not met. |
| M10-004 narrow helper | retain, deferred | Its three directly attributable same-mechanism external-failure trigger is not met. |
| M11-001 IR shadow | retain, blocked | It requires two validated narrow helpers and script-prefix evidence. |
| M18-001 DeepCAD audit | retain, deferred | Fusion has no documented data-source coverage/representation blocker. |
| M19-002 guidance retrieval | retain, evidence-gated | No single mechanism has three independent direct evidence cards. |
| M19-003 runtime retrieval | retain, blocked | It depends on a successful, explicitly selected M19-002 review. |
| M21-004 rounded-slot promotion | proposed, backlog | This review satisfies the review prerequisite, but user selection and a separate ADR remain required before any promotion. |

## Governance disposition

Create `WP-M21-004` only as a backlog proposal. It may be selected by the user
to determine whether the three experimental `offset_rounded_slot` assets and
the six-record `rounded-slot-v1` metadata contract should receive the same
limited case-library governance treatment as M20. Until that workpack is
selected, the assets remain experimental and absent from the registry and all
manifests. No experience card is created.
