# Self-Authored Case Assets

This is the committed physical home of the self-authored corpus. Each case is self-contained:

```text
case-library/
  self-authored/
    <case_id>/
      case.json                     # authoritative complete metadata
      input.step                     # target B-Rep
      reference_build_sequence.py    # optional deterministic OCP replay
  manifests/self-authored/
    p0.json ... p3.json              # explicit CorpusRunner inputs
  test-support/                      # non-case test helpers
```

`case.json` describes the fixture identity, provenance, expected geometry, tier, tags, unit, coordinate frame, and reference-script status. The root index at `docs/corpus/registry/self-authored.json` points to every case record; the development catalog and procedure are in `docs/corpus/library/`.

Do not place external raw datasets here. Keep those under ignored `data/datasets/<dataset>/<release>/` with their source-license boundary.
## M12 parameter families

`manifests/self-authored/parametric-development.json` and
`manifests/self-authored/parametric-held-out.json` expose the 18 M12 cases.
Their `family_id` and `data_split` fields are authoritative for parameter-family
isolation; P0--P3 remain difficulty tiers. Run
`uv run python tools/audit_case_library.py --replay` after changing an M12 case.
