# WP-M12-001: Self-Authored Parametric Families

- Status: done
- Milestone: M12
- Owner: unassigned

## Goal

Extend the self-authored corpus with a small, reproducible parameter-family layer while separating development and held-out families.

## Result

- Added 18 cases under `case-library/self-authored/`: 6 families × low/nominal/high variants.
- Development families: `additive_boss`, `through_hole`, `rounded_slot`, and `fillet` (12 cases). Held-out families: `blind_hole` and `chamfer` (6 cases).
- Added explicit `family_id`, `data_split`, `variant`, and parameter fields to each authoritative `case.json` and to the two new manifests.
- Added `parametric-development.json` and `parametric-held-out.json`; P0--P3 retain difficulty-tier semantics.
- Added `tools/build_m12_parametric_cases.py` and `tools/audit_case_library.py`. The audit checks co-located assets, hashes, manifest/metadata agreement, family isolation, and optional reference-script replay against the stored geometry baseline.

## Acceptance

- [x] 18/18 cases co-locate metadata, STEP and reference script.
- [x] Each family appears in exactly one split.
- [x] Both manifests load offline through `CorpusRunner`'s existing loader.
- [x] Full reference replay passes bbox, volume and topology-count baselines.
- [x] No new Harness operation abstraction, hosted request, or default corpus batch was introduced.
