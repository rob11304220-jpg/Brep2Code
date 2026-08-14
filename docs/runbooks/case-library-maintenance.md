# Unified Case-Library Maintenance

## Purpose

Maintain a discoverable relationship between B-Rep inputs, optional construction sequences, intermediate states, executable manifests, and ignored runtime evidence without changing Harness runtime scope.

This runbook implements the maintainability contract in [ADR-0014](../architecture/adr/0014-case-library-maintainability-contract.md).  The library is a filesystem asset authority with checked-in JSON metadata; it is not a database and a case directory is not an implicit execution or provider authorization.

## Authority, identifiers, and lifecycle

- Keep `case_id` stable after registration.  Never recycle it for a materially different geometry or sequence.
- `case.json` is authoritative for identity, asset hash, reference-script declaration, and numerical baseline.  The self-authored registry is a pointer/routing index; manifests are executable selections only.
- Keep `schema_version` in metadata.  Add optional fields compatibly; a required-field change or reinterpretation needs an ADR and a migration/audit plan.
- Use lifecycle labels consistently: `active` for supported cases, `experimental` for workpack-scoped cases, `deprecated` for cases still needed by history but replaced for new work, and `archived` for retained non-default evidence.  Before changing a case away from `active`, record the rationale, replacement (if any), and affected manifests/case cards.
- Do not copy a committed case into another fixture tree.  If an old path must disappear, move it only after hashes, active references, manifests, and tests have been audited.

## Add or change a self-authored case

1. Create or update `case-library/self-authored/<case_id>/`. Keep `case.json` and `input.step` together; add `reference_build_sequence.py` when the case has a deterministic OCP reference.
2. Update the complete metadata in that `case.json` (fixture identity, SHA-256, reference-script status, numeric baseline, tier, and feature tags), then update the pointer entry in `docs/corpus/registry/self-authored.json`. Parameterized cases additionally require `family_id`, `data_split`, `variant`, and concrete parameters.
3. Keep each parameter family in exactly one `data_split`; use explicit development/held-out manifests instead of overloading P0--P3 difficulty tiers. Update the case card and add a case to an executable manifest only when the workpack explicitly requires execution.
4. Update `docs/corpus/library/catalog.json` only if the collection layout, family policy, or planned admission changes.  Do not duplicate every case entry there.
5. Run `uv run python tools/audit_case_library.py`; use `--replay` when reference scripts or baselines changed. Then run the focused manifest tests.

## Required offline validation

For every case-library change, run the hash/path/manifest/split audit.  Also run the focused tests for the affected manifests.  Run `--replay` whenever a reference script, expected geometry baseline, or geometry-generating dependency changes.  Before removing a legacy location, search active code and documentation for stale paths and run `git diff --check`.

Runtime records and reports may identify a `case_id`, manifest, and revision, but they are ignored evidence: never copy them into a case directory or treat them as a replacement fixture/baseline.

## Design and admit a new sequence-paired family

### Standing offline authorization boundary

When `docs/workflow/status.md` records a user standing authorization for
offline case governance, an agent may create and complete the bounded
design, production, review, and promotion workpacks needed to close a concrete
coverage gap. It must still record each workpack, freeze evidence before
production, and preserve all gates below. This is never authorization to alter
an executable manifest, Harness, provider, training, runtime, external-data
scope, or to make a hosted request.

Use this procedure only after a user has selected a bounded workpack. It is a
development-governance path, not authorization to create runtime inputs.

1. Read `docs/corpus/knowledge/coverage-matrix.json` and name one concrete
   coverage gap. State both the grammar boundary and what the family cannot
   claim; parameter-count growth is not a sufficient selection rationale.
2. Copy `docs/corpus/sequence-paired/family-intake-template.json` to a
   family-specific preregistration record. Before writing a producer or assets,
   replace every placeholder and freeze exact rows, template-family-isolated
   development/held-out splits, canonical sequence, oracle provenance,
   preconditions, semantic invariants, directional mutations, production
   checks, and rejection taxonomy.
3. Run `uv run python tools/audit_sequence_paired_intake.py <record>`. It
   checks the shared preregistration contract only. A passed intake audit is
   not a geometry result and does not make the record or its future assets
   active.
4. In a separately selected controlled-production workpack, generate only the
   frozen rows. Build twice in clean directories and compare normalized STEP
   SHA-256 values. Retain rejected candidates and their stable reason class;
   do not substitute a better-looking row.
5. Add a family-specific audit that checks existing geometry replay gates,
   exact sequence/dependencies, all declared editability mutations, and the
   family-specific semantic anti-degeneration invariants. Include negative
   controls for at least split leakage, sequence mismatch, and a meaningful
   semantic degeneration.
6. Keep passing outputs `experimental`. A separate review and, when lifecycle
   changes are proposed, a separately accepted ADR/workpack decide promotion.
   Promotion never implies executable-manifest, provider, training, or runtime
   admission.

Existing family-specific records retain their frozen schema. Add the reusable
`production_checks` and `rejection_taxonomy` fields only in a selected,
compatible migration; do not rewrite historical preregistration evidence just
to satisfy the newer template.

## Maintain the promoted prismatic-hole sequence pairs

ADR-0019 applies an additional, narrow rule to exactly the nine records named
by `docs/corpus/sequence-paired/prismatic-hole-v1-expansion.json`.  For those
records only, keep `sequence_pair.grammar_version`, oracle provenance, canonical
sequence, and declared mutations aligned with the expansion record.  A
counterbore record additionally keeps its local `candidate_sequence.json` in
exact agreement.  Run both `uv run python tools/audit_case_library.py --replay`
and `uv run python tools/audit_sequence_paired_prismatic_hole.py` after changing
one of these records or its reference script.  Do not apply this field to a new
family without an independently approved workpack and ADR.

## Maintain the promoted rounded-slot sequence pairs

ADR-0023 applies an additional, narrow rule to exactly the six records named
by `docs/corpus/sequence-paired/rounded-slot-v1-expansion.json`. For those
records only, keep `sequence_pair.grammar_version`, oracle provenance,
dependent canonical sequence, declared mutations, and local
`candidate_sequence.json` aligned with the expansion record. Run both
`uv run python tools/audit_case_library.py --replay` and
`uv run python tools/audit_sequence_paired_rounded_slot.py` after changing one
of these records or its reference script. Do not apply this field to a new
family without an independently approved workpack and ADR.

## Maintain the promoted multi-contour pocket sequence pairs

ADR-0024 applies an additional, narrow rule to exactly the six records named
by `docs/corpus/sequence-paired/multi-contour-pocket-v1-preregistration.json`.
For those records only, keep `sequence_pair.grammar_version`, oracle
provenance, nested-loop canonical sequence, declared mutations, and local
`candidate_sequence.json` aligned with preregistration. Run both
`uv run python tools/audit_case_library.py --replay` and
`uv run python tools/audit_sequence_paired_multi_contour_pocket.py` after
changing one of these records or its reference script. Do not apply this field
to a new family without an independently approved workpack and ADR.

## Maintain the promoted additive-boss dependent-cut sequence pairs

ADR-0027 applies an additional, narrow rule to exactly the six records named
by `docs/corpus/sequence-paired/additive-boss-dependent-cut-v1-preregistration.json`.
For those records only, keep `sequence_pair.grammar_version`, oracle
provenance, declared boss-to-blind-cut sequence, mutations, and local
`candidate_sequence.json` aligned with preregistration. Run both
`uv run python tools/audit_case_library.py --replay` and
`uv run python tools/audit_sequence_paired_additive_boss_dependent_cut.py`
after changing one of these records or its reference script. Do not interpret
the declared `boss.top_face` support as runtime face selection or apply this
metadata role to another family without an independently approved workpack and
ADR.

## Maintain the promoted face-selected dependent-cut sequence pairs

ADR-0029 applies only to the six records named by
`face-selected-dependent-cut-v1-preregistration.json`. Keep their frozen
seven-step sequence, including `SelectPlanarFace` with unique planar `+Z`
maximum-Z cardinality and `SketchCircle` consumption of that selector, aligned
with the preregistration record. Run `audit_case_library.py --replay` and
`audit_sequence_paired_face_selected_dependent_cut.py` after changing one of
these records or its reference script. Do not generalize this contract to
topological naming, arbitrary faces, or runtime selection.

## Maintain the promoted multi-inner-loop pocket sequence pairs

ADR-0031 applies only to the six records named by
`multi-inner-loop-pocket-v1-preregistration.json`. Keep their frozen outer +
two-inner-island sequence, deterministic oracle provenance, mutations, and
local `candidate_sequence.json` aligned with preregistration. Run
`audit_case_library.py --replay` and
`audit_sequence_paired_multi_inner_loop_pocket.py` after changing one of these
records or its reference script. Do not generalize this contract to arbitrary
loop counts, topology recognition, or runtime use.

## Admit a new external sequence-supervised source

1. Copy `docs/corpus/library/dataset-admission-template.json` to a source-specific, tracked selection record and register the dataset in `docs/corpus/external/registry.json`.
2. Record the upstream release, official source, license review, exact local ignored root, asset inventory, and whether the construction history is native, reconstructed, or a local deterministic reference.
3. Select a small deterministic subset.  Split by source design or parameter family, not merely by nearly identical derived files.
4. Hash every selected input; run the existing input probe.  If a reference sequence exists, replay it locally to a STEP output and compare it with existing gates before considering it a paired case.
5. Only after the offline workpack is complete may a separate workpack decide whether to add an explicit manifest.  Hosted use still requires the existing preflight and separate authorization.

## Interpret source types

| Source type | Permitted claim |
|---|---|
| Native sequence + final B-Rep | A source history provides supervised/reference evidence; it is not necessarily the only valid inverse. |
| Deterministic local reference + B-Rep | The script is a replay oracle for Harness compatibility, not source-ground-truth history. |
| B-Rep only | Geometry-equivalence and robustness only; do not claim sequence-recovery accuracy. |

## Never do implicitly

- Do not move committed fixtures merely to make the directory tree look uniform.
- Do not copy raw external data into Git, `tests/fixtures/`, or runtime LLM material.
- Do not turn a catalog entry into a default test, a manifest entry, or a hosted batch.
- Do not use exact source-history string match as the sole correctness criterion for B-Rep-to-program reconstruction.
