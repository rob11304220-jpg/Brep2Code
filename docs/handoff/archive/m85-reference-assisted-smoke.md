# Handoff: M85 Reference-Assisted P0 Smoke

- **Date**: 2026-08-10
- **Subproject**: `brep2code`
- **Status**: `active`
- **Related workpack**: `WP-M85-001-reference-assisted-p0-hosted-smoke`

## Goal

Build and validate locally the fixed two-request `cylinder` reference-assisted
Harness path: a model request for one bounded guidance card followed by a
model-generated OCP build script.

## Done

- M19-003 bounded, revision-scoped guidance bridge is independently approved.
- M85 scope is fixed to `cylinder`, role `final primitive`, top-k one, two
  provider requests, and no repair/retry.

## In progress

- Await independent review of the implemented provider-neutral structured
  tool-call response and two-stage runner.

## Next

- Complete the read-only M85 hosted preflight: fixed input/card hashes, secure
  executor check, provider configuration presence check, fresh report/monitor
  paths, and explicit egress/budget disclosure.

## Decisions

- Use a provider-neutral JSON tool-call protocol before relying on a provider's
  native function-calling transport. This preserves Harness control and the
  existing JSON-object provider boundary.
- Local fake smoke passed with `cylinder`, the frozen card, two provider
  requests, no input mount, and all geometry gates. It is not hosted evidence.
- M85 `prepare`/`execute` records `0/2`, then `1/2` and `2/2` before the two
  provider boundaries; a terminal report cannot resume or retry either request.

## Blockers

- Hosted execution remains blocked on completed local acceptance, fresh hosted
  preflight, and explicit itemized user authorization.

## Key paths

| Kind | Path |
|---|---|
| Files | `brep2code/agent/provider.py`, `brep2code/agent/observed_build.py`, `brep2code/cli/__init__.py` |
| Workpack | `docs/workpacks/active/WP-M85-001-reference-assisted-p0-hosted-smoke.md` |
| Commands | `uv run python -m pytest`; `uv run python -m ruff check .`; `uv run python tools/check_governance.py` |

## Resume prompt

## Hosted execution update

- Authorized M85 execution terminalized `completed` with exactly two provider
  requests. The frozen guidance card was returned, and the generated script
  passed contract, `wsl-bwrap`, output and geometry gates without input access.
- Next action: Liaol independently reviews
  `data/corpus-runs/m85-cylinder-reference-assisted.json` and the revision
  traces before deciding closure; no retry or broader run is authorized.

```
Continue Brep2Code M85: implement and offline-validate the two-request
reference-assisted cylinder smoke. Read this handoff first.
```
