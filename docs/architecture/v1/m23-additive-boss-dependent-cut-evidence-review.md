---
type: review
related-project: Brep2Code
status: completed
---

# M23-003 Review: Additive-Boss-Dependent-Cut Evidence

## Scope

This review compares the completed M23 experimental candidates with the M20--
M22 self-authored deterministic-oracle families. It neither promotes an asset
nor changes a manifest, provider, training input, runtime resource, parser,
helper, SDK, or IR.

## Evidence comparison

| Dimension | M20--M22 baseline | M23 addition | Review finding |
|---|---|---|---|
| Frozen rows and split | 21 total records with preregistered family-isolated splits | 6 rows, 3 centered development / 3 offset held-out | M23 preserves the same split discipline and no-substitution boundary. |
| Feature semantics | Subtractive holes, composite through slot, and blind annular pocket | One rectangular additive join followed by one blind circular cut | This is the first bounded add-then-subtract chain; it is not generic multi-extrude evidence. |
| Dependency | Base-to-profile/cut and two-loop-profile dependencies | Boss is the declared target/support for the later blind cut | The dependency is explicit in the oracle, but no B-Rep face identity selector was exercised. |
| Validation | Replay, exact sequence, editability, and family-specific anti-degeneration | Four mutations plus one-solid, base-extent, boss-height, and blind-cut-volume checks | The three-layer discipline continues to be reproducible. |
| Negative evidence | Sequence, split, profile, and containment controls | Base-targeted cut, missing/disconnected boss, through-cut, and split leak controls | M23 retains distinguishable failure modes rather than accepting geometrically simpler substitutions. |

## Knowledge disposition

The six records justify the bounded
`additive-boss-dependent-cut-v1` knowledge unit at `supported` evidence. It
states only the frozen axis-aligned base-to-joined-boss-to-blind-cut grammar.
The `boss.top_face` support is a declared deterministic-oracle dependency, not
runtime face discovery, a stable topological naming method, or evidence for an
edge-referenced feature.

Accordingly, the next technical gap is a deliberately narrow
`face-selected-dependent-cut-v1` design: it must make face-selection identity
observable and reject a wrong-face target. That design is not selected here.

## Governance disposition

Propose exactly one separately selectable successor: `WP-M23-004`, a scoped
governance-promotion review for the six frozen M23 records. If selected, it
must accept a dedicated ADR, audit every candidate against preregistration,
and decide only their limited active-library lifecycle. It must not create an
executable manifest or select the face-selected family.

No experience card is proposed: this is deterministic family evidence, not
three independent direct runtime mechanism cases.

## Boundaries

The priority route remains ordered: M23 governance disposition first, then a
separate user-selected face-selection design. Multiple feature families,
patterns, curves, external sources, and runtime changes remain out of scope.
