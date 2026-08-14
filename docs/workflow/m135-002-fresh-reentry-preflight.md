# M135-002 Frozen Epoch Fresh Re-entry Preflight — Blocked

- **Date**: 2026-08-12
- **Workpack**: `WP-M135-002-frozen-epoch-fresh-reentry-preflight`
- **Scope**: local, credential-free, no provider construction or egress
- **Disposition**: blocked before independent G3 review or hosted-authorization request

## Passing local controls

The unchanged frozen cohort passed the local controls that the current
implementation exposes:

| Control | Terminal result |
|---|---|
| Frozen cohort/hash and fake checkpoint lifecycle, including all 18 issued states | `uv run python -m pytest tests\\test_m135_epoch.py -q`: 5 passed in 94.18s |
| All twelve no-card fixed scripts in no-input `wsl-bwrap` | Included in the same 5/5 M135 test result |
| Fast offline regression | `uv run python -m pytest -m fast -q`: 66 passed, 177 deselected in 4.37s |
| Full offline suite | `uv run python -m pytest`: 243 passed in 431.45s |
| Static check | `uv run python -m ruff check .`: All checks passed |
| Governance audit | `uv run python tools\\check_governance.py`: Governance audit passed |
| Diff check | `git diff --check`: passed (line-ending warnings only) |

No provider was constructed. The tests use `FakeLLMProvider`; no credential,
provider response, raw STEP, or outbound transcript was read or sent.

## Fresh-path check

The newly proposed identities `data/m135-002/epoch-report.json` and
`data/m135-002/epoch-monitor.json` were absent at preflight. They were not
created, and no M135-001 report, monitor, request budget, or authorization was
used.

## Reproducible blocker

`brep2code.agent.m135_epoch` defines a frozen-condition loader and durable
checkpoint helpers, but repository search finds no M135 command in
`brep2code.cli`. The CLI exposes generic `corpus` and unrelated fixed campaign
commands only; it has no M135 18-condition epoch command and no M135 policy or
monitor-path parameters. Consequently this workpack cannot verify the actual
CLI execution boundary required by M134 and ADR-0068: the fixed provider/model,
deadline, output cap, report path, monitor path, serial 18-request budget, and
zero-repair/zero-retry behavior are not available together as an executable
surface.

This is a local implementation/preflight failure, not a provider failure. Do
not request hosted authorization, infer a model/deadline/output cap, or route
the generic corpus command around the missing frozen-epoch contract.

## Required re-entry

A user-selected, separately bounded G3 workpack is required to implement and
offline-validate the missing executable M135 epoch surface while retaining the
frozen cohort. It must use fresh report/monitor identities and then repeat the
entire credential-free preflight. Only a passing re-entry preflight plus an
independent G3 review could support a later itemized hosted-authorization
request.
