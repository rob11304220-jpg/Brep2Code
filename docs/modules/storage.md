# Storage Module

## Responsibility

`brep2code/storage/` owns the local record and revision directory layout used by the M0 harness.

It creates:

- `data/records/<record_id>/record.json`
- `data/records/<record_id>/input/`
- `data/records/<record_id>/revisions/<rev_id>/workspace/`
- `workspace/intermediates/`
- `workspace/output/`
- `revisions/<rev_id>/traces/`

## Boundary

Storage only manages paths and JSON persistence. It does not execute scripts, validate CAD geometry, call LLMs, or define a modeling schema.

## Public Entry

- `brep2code.storage.RecordStore`
- `brep2code.storage.RecordPaths`
- `brep2code.storage.RevisionPaths`

## M0 Acceptance

Run:

```powershell
python -m brep2code.cli run --record demo
```

Then check that `record.json`, `workspace/build_sequence.py`, `execution.json`, `signal_bundle.json`, and trace files exist under `data/records/demo/`.
