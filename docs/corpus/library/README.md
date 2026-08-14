# Unified Case Library

This directory is the single **development-side index** for the case library. It
answers where each input B-Rep lives, whether a reference construction sequence
or intermediate states exist, whether the source is runnable, which *evidence
role* it serves, and what must happen before it can be admitted.

The development index in this directory is not a Harness manifest, a runtime LLM resource, or a provider payload. The committed self-authored assets themselves live in the sibling repository directory `case-library/`; `CorpusRunner` continues to consume explicit manifests.

## Asset roles and physical locations

| Role | Canonical location | Tracking / boundary |
|---|---|---|
| Self-authored case metadata, input B-Rep, reference script | `case-library/self-authored/<case_id>/` | committed, one directory per case |
| Executable corpus manifests | `case-library/manifests/self-authored/p0.json` through `p3.json` | committed Harness input |
| External raw B-Rep, source sequence, intermediate states | `data/datasets/<dataset>/<release>/` | ignored, source-license boundary |
| Selected external manifests and source identities | `docs/corpus/external/` | tracked development governance |
| Runtime records and reports | `data/records/`, `data/corpus-runs/` | ignored execution evidence |

The [catalog](catalog.json) is the machine-readable root index. Each self-authored `case.json` is authoritative for its identity and numerical baseline; [`../registry/self-authored.json`](../registry/self-authored.json) is a pointer index. External selections remain authoritative in [`../external/`](../external/).

## From governed assets to modeling knowledge

Asset governance answers where a case came from and whether it is valid to
maintain or execute. It does not by itself establish what the case teaches
about B-Rep interpretation or kernel-operation use. In the knowledge system a
case is evidence--an oracle, discriminating/negative control, regression,
OOD-robustness or native-history-validation asset--rather than a unit of
capability coverage. The separate
[modeling knowledge system](../../architecture/v1/modeling-knowledge-system.md)
links governed assets and reviewed evidence to an explicit
[coverage matrix](../knowledge/coverage-matrix.json). Its knowledge units may
link back to cases, but cannot change a case lifecycle, manifest, or runtime
authorization. Only compact, reviewed projections may later become experimental
[runtime experience cards](../../../runtime_resources/experience-cards/README.md).
The governing architecture and role definitions are in
[knowledge-base-architecture.md](../../architecture/v1/knowledge-base-architecture.md).

## Long-term maintainability contract

The case library is a versioned filesystem asset library, not a database or an automatic runtime corpus.  Its source-of-truth and lifecycle rules are defined by [ADR-0014](../../architecture/adr/0014-case-library-maintainability-contract.md).

| Concern | Required rule |
|---|---|
| Identity and authority | `case_id` is immutable.  `case-library/self-authored/<case_id>/case.json` owns the self-authored case identity, asset hashes, reference-script declaration, and geometry baseline. |
| Asset layout | Every active self-authored case has `case.json` and `input.step`; a deterministic reference script, intermediate states, and previews are optional roles declared by metadata.  No duplicate fixture becomes a second authority. |
| Routing and execution | The registry is a pointer/routing index.  A manifest is an explicit executable selection, not an inventory.  Directory presence alone never authorizes test discovery, hosted use, or provider input. |
| Lifecycle and compatibility | A case is `active`, `deprecated`, `archived`, or `experimental`.  Do not reuse an identifier; deprecate it with a replacement/rationale and preserve historical manifest/report references.  Extend metadata through a schema-versioned, backward-compatible change. |
| Split integrity | A parameter family belongs to one split only.  Development, held-out, regression, and experimental purposes must be declared rather than inferred from a difficulty tier. |
| External sources | Raw external assets stay in ignored `data/datasets/<dataset>/<release>/`; tracked selections record source version, license boundary, hashes, and admission evidence. |
| Evidence and validation | Hash, path, manifest, and split audits are required offline checks.  Replay is required when a deterministic reference or numerical baseline changes.  Ignored runtime evidence may link to a case but cannot redefine it. |

The library composition evolves through governed lifecycle records. Use each
`case.json` and the registry rather than this navigation page for the current
active membership or executable eligibility. Its current audit command is
`uv run python tools/audit_case_library.py`; add `--replay` after reference or
baseline changes.

## Relationship model

```text
case/source
  ├─ input_brep            required
  ├─ reference_sequence    optional (ground truth or deterministic reference)
  ├─ intermediate_states   optional
  ├─ execution_manifest    optional explicit Harness input
  └─ runtime_evidence      optional ignored records/reports
```

An ABC sample has `input_brep` but no source construction history.  A self-authored case normally has an input B-Rep and a deterministic OCP reference script.  A future sequence-supervised source must explicitly record whether its history is native ground truth, reconstructed, or merely a reference replay.

## Planned admission order

1. **Self-authored parameter families** — extend the existing P0--P3 ladder with family-level held-out splits and reference scripts.
2. **Fusion 360 Gallery Reconstruction** — first external sequence-supervised feasibility candidate; restrict the first audit to the sketch/extrude subset and retain its native-history provenance.
3. **DeepCAD** — second candidate; construction JSON requires deterministic local replay before its geometry can become a paired case.
4. **Brep2Seq synthetic data** — candidate for broader mechanical-feature coverage only after source-data licensing and representation compatibility are reviewed.
5. **ABC** — retain as B-Rep-only OOD robustness material; it is not a source of ground-truth construction sequences.

The active Fusion-first conditional route is recorded in the
[paired-data roadmap](../../architecture/v1/fusion360-paired-data-roadmap.md):
M15 review, then only conditionally M16 local control, M17 bounded expansion
inside the existing cache, and M18 DeepCAD admission audit.

The active Q02 sequence-paired pilot is separately recorded in the
[prismatic-hole route](../../architecture/v1/sequence-paired-prismatic-hole-roadmap.md).
It is a bounded development-side contract, not an additional manifest or a
replacement for this library's long-term authority rules.

ADR-0019 promotes M20's three `param_counterbore_*` assets into the active
library after their completed audit.  They remain deliberately absent from all
executable manifests; their scoped `sequence_pair` metadata is not a runtime
or automatic-admission route.

ADR-0023 promotes M21's three `param_offset_rounded_slot_*` assets and scopes
the six-record `rounded-slot-v1` metadata contract. They remain deliberately
absent from all executable manifests; their sequence-pair metadata is not a
runtime or automatic-admission route.

ADR-0024 promotes the six `param_multi_contour_pocket_*` assets and scopes the
six-record `multi-contour-pocket-v1` metadata contract. They remain deliberately
absent from all executable manifests; their sequence-pair metadata is not a
runtime or automatic-admission route.

ADR-0027, ADR-0029, ADR-0031, and ADR-0033 likewise govern the six frozen
additive-boss-dependent-cut, face-selected-dependent-cut,
multi-inner-loop-pocket, and oriented-rounded-slot records respectively. They
remain absent from executable manifests. Their reusable design projections are
located in [`../knowledge/`](../knowledge/README.md), not in these admission
rules.

No candidate is downloaded, selected, added to an executable manifest, or sent to a provider merely by appearing here.  Use [the admission template](dataset-admission-template.json) in an offline, dedicated workpack.

