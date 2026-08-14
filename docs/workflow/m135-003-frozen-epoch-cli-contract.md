# M135-003 Frozen Epoch CLI and Monitor Contract

- **Date**: 2026-08-12
- **Workpack**: `WP-M135-003-frozen-epoch-cli-contract`
- **Scope**: offline-only; no credentials, provider construction or egress
- **Status**: owner-side implementation and validation passed; awaiting
  independent G3 review

## Delivered contract

`m135-epoch-preflight` is a dedicated CLI preparation command. It loads the
unchanged frozen 18-condition cohort, validates the tracked input hashes,
creates a fresh zero-request checkpoint, and creates a separate monitor-owned
state file. It has no provider or environment-file argument and does not
construct a provider.

The checkpoint fixes `deepseek / deepseek-v4-pro`, `wsl-bwrap`, a 120-second
provider deadline, 18 maximum requests, zero repair/retry, and no selected
token output cap. It records `authorization: not_authorized` and
`provider_constructed: false`. Report and monitor paths must both be fresh and
must differ.

## Offline evidence

| Command | Terminal result |
|---|---|
| `uv run python -m pytest tests\\test_m135_epoch.py -q` | 7 passed in 93.55s |
| `uv run python -m pytest -m fast -q` | 66 passed, 179 deselected in 4.54s |
| `uv run python -m pytest` | 245 passed in 432.63s |
| `uv run python -m ruff check .` | All checks passed |

The focused tests cover fixed contract values, 0/18 request accounting,
monitor state creation and rejection of report reuse, monitor reuse and
report/monitor path collision. No provider was constructed, no credential was
read, and no data was sent.

## Boundary

This contract repairs only M135-002's missing executable local surface. It is
not a complete fresh hosted preflight and does not authorize any request. A
later workpack must create new report/monitor identities, complete the full
credential-free preflight, receive independent G3 review, and then request
itemized hosted authorization before any provider construction.
