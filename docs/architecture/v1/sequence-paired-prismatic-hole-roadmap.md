---
type: roadmap
related-project: Brep2Code
version: v1
status: active
tags:
  - Brep2Code
  - sequence-paired
  - prismatic-hole
  - case-library
---

# Sequence-Paired Case-Coverage Route

## Purpose

This route shifts the primary Q02 evidence source from repeated B-Rep-only
external retries to a bounded, sequence-supervised benchmark.  It preserves
ABC as OOD execution/robustness material and preserves the restricted Fusion
replay route; neither is automatically expanded or activated by this document.

The first supported family is:

```text
Sketch(planar outer profile) -> Extrude(base) -> CutCylinder(through | blind | counterbore)
```

It is deliberately not a claim of general feature recognition or generic CAD
history recovery.

## Pilot evidence contract

Each paired pilot case must record a versioned canonical sequence, its oracle
provenance, a deterministic OCP replay, input/output STEP hashes, declared
family and split, and the parameters used by editability checks.  Source history
may be native ground truth or a self-authored deterministic oracle; the two
statuses must never be conflated.

The pilot evaluates all three layers below.  A geometry-only pass is not a
sequence-correctness pass.

| Layer | Required evidence | Pilot pass criterion |
|---|---|---|
| Geometry | output STEP readable; existing bbox, volume, topology gates | all existing gates pass |
| Sequence | canonical operation kinds, parameters, and dependency edges compared with the declared oracle | exact agreement under the pilot's documented normalization |
| Editability | preregistered changes to base dimensions, hole radius, or hole depth | replay stays executable and the documented observables change as predicted |

## Workpack sequence

1. **M20-001 foundation (done)** — define the pilot grammar and metadata,
   create a small family-isolated paired seed set, deterministic replay/audit,
   and the three-layer review evidence.  It is offline only.
2. **M20 review (done)** — the M20-001 review found the pilot coherent enough
   for a separately scoped expansion, but not for governance promotion.
3. **M20-002 controlled expansion (done)** — retained the grammar and expanded
   to a preregistered 6 development / 3 held-out set.  The producer may generate
   candidates but cannot self-admit them.
4. **M20-003 governance promotion (done)** — under ADR-0019, promoted only
   the validated nine-record metadata contract and three counterbore assets to
   the active library; executable manifests and runtime remain unchanged.
5. **M21-001 cross-family design (done)** — ADR-0020 froze the
   `rounded-slot-v1` capability matrix, exact six-row split, semantic
   anti-degeneration predicates, rejection taxonomy, and stability checks
   before candidate production.
6. **M21-002 rounded-slot controlled expansion (done)** — all six frozen rows
   passed offline geometry, exact sequence, editability, and anti-degeneration
   evidence; the three new assets remain experimental and unadmitted.
7. **M21-003 cross-family governance review (done)** — the two completed
   deterministic-oracle families support only a separately selected, restricted
   M21-004 promotion proposal; no M21 asset changed lifecycle.
8. **M21-004 rounded-slot governance promotion (done)** — ADR-0023 accepted
   the family-specific governance boundary; no executable-manifest, provider,
   training, or runtime route was added.
9. **M22-000 modeling knowledge foundation (done)** — the coverage matrix and
   bounded knowledge-unit contract are complete; it created no case assets or
   runtime retrieval.
10. **M22-001 multi-contour pocket design (done)** — preregistered the six
    `multi-contour-pocket-v1` rows and an evidence-seeking operation-contract
    draft; it created no candidate assets.
11. **M22-002 controlled production (done)** — the six frozen rows passed
    controlled production and validation; they remain experimental and
    unadmitted.
12. **M22-003 dependency review (done)** — created the bounded
    `multi-contour-pocket-v1` knowledge unit and selected only a governance
    proposal; no asset changed lifecycle.
13. **M22-004 multi-contour pocket governance promotion (done,
    offline-only)** — ADR-0024 promoted only the six audited records to active
    case-library governance; executable manifests and runtime remain unchanged.
14. **M23-001 additive-boss-dependent-cut design (done, offline-only)** —
    ADR-0025 froze one six-row boss-to-blind-cut dependency grammar before any
    candidate production.
15. **M23-002--004 additive-boss dependent-cut production, review and
    promotion (done, offline-only)** — the six frozen rows completed controlled
    production and evidence review; ADR-0027 promoted only the reviewed family
    to active governance cases without manifest or runtime admission.
16. **M25--M27 later isolated family routes (done, offline-only)** —
    face-selected dependent cut, multi-inner-loop pocket, and oriented rounded
    slot each completed their separately bounded design/production/review/
    promotion lifecycle. Their evidence remains family-scoped and does not
    authorize generic selection, manifests, provider input or runtime use.
17. **M90 repeated-feature pattern route (done, offline-only)** — ADR-0055
    promoted six audited records for one four-instance rectangular-grid
    through-cut grammar to active governance cases. They remain absent from
    executable manifests, provider inputs and runtime resources.
18. **External validation (conditional)** — only after self-authored
    dependency evidence, consider constrained Fusion validation, then DeepCAD
    deterministic-replay admission, then BRep2Seq synthetic admission.
19. **IR decision (conditional)** — consider a runtime IR only after repeated
    cross-family evidence shows that scripts cannot preserve a correct prefix
    without the same structured dependency representation.

## Promotion to long-term case-library governance

M20-001 itself creates a pilot contract only.  Its completion review may
propose a separate governance workpack and ADR only if all preregistered pilot
cases, including family-isolated held-out cases, pass all three evidence layers
and the audit is deterministic.

The later governance decision must require:

- a versioned sequence grammar and backward-compatible metadata evolution;
- immutable case IDs, source/oracle provenance, hashes, split/family records,
  deterministic OCP replay and retained rejected-case reasons;
- audited candidate production, with no automatic manifest, provider, training,
  or evaluation admission; and
- geometry, sequence, and editability evidence for every case inside each
  promoted family.

These are not global requirements yet.  Outside promoted families, ADR-0014
and the existing case-corpus contract remain authoritative.

## Boundaries

- Default execution remains offline and credential-free; this route sends no
  provider request and does not authorize one.
- No Harness, CLI, gate, corpus-report schema, runtime-resource, prompt,
  parser, SDK, or general IR change is implied.
- Fusion support remains limited by ADR-0017; ABC remains B-Rep-only OOD
  material.
- Source licenses and raw external assets remain in their existing boundaries.
- Development and held-out families are selected before implementation evidence
  is reviewed; no post-hoc replacement is allowed.
- ADR-0020 requires a design/preregistration workpack separate from controlled
  production for every later family.

## Related records

- [ADR-0018](../adr/0018-sequence-paired-prismatic-hole-pilot.md)
- [ADR-0020](../adr/0020-two-phase-cross-family-sequence-pair-expansion.md)
- [Rounded-slot design](rounded-slot-sequence-pair-design.md)
- [M21-003 review](m21-cross-family-sequence-pair-governance-review.md)
- [ADR-0021](../adr/0021-evidence-sequenced-case-coverage-expansion.md)
- [ADR-0022](../adr/0022-modeling-knowledge-system.md)
- [Knowledge-system architecture](modeling-knowledge-system.md)
- [M22-001 design](multi-contour-pocket-sequence-pair-design.md)
- [M22-002 review](m22-multi-contour-pocket-controlled-production-review.md)
- [M22-003 review](m22-cross-family-dependency-review.md)
- [ADR-0024](../adr/0024-multi-contour-pocket-sequence-pair-governance.md)
- [ADR-0025](../adr/0025-additive-boss-dependent-cut-design.md)
- [M23-001 design](additive-boss-dependent-cut-sequence-pair-design.md)
- [M25--M27 priority route](case-family-expansion-priorities.md)
- [M90 review](m90-repeated-feature-pattern-evidence-review.md)
- [ADR-0055](../adr/0055-repeated-feature-pattern-governance.md)
- [M20-002 completion review](m20-prismatic-hole-controlled-expansion-review.md)
- [M20-003 completion review](m20-prismatic-hole-governance-promotion-review.md)
- [Case-library contract](../../corpus/library/README.md)
- [Fusion paired-data route](fusion360-paired-data-roadmap.md)
