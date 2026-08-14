# WP-M3-004: Hosted Provider Integration

- Status: done
- Milestone: M3
- Owner: unassigned

## Goal

Connect the repair loop to DeepSeek V4 through one real hosted provider while keeping credentials out of source control and keeping the fake-provider path available.

## Scope

- Add the DeepSeek V4 provider implementation behind the M3 provider interface, defaulting to `deepseek-v4-pro`.
- Read configuration from environment variables or local ignored config.
- Document required env vars and secret handling.
- Add a smoke command/runbook for a credentials-backed local run.
- Keep tests network-free by default; use fake provider for CI/local unit tests.

## Inputs

- `docs/workpacks/done/WP-M3-001-llm-provider-trace-contract.md`
- `docs/workpacks/done/WP-M3-002-tool-calling-bridge.md`
- `docs/workpacks/done/WP-M3-003-repair-loop-runner.md`
- `docs/runbooks/dev-environment.md`
- `pyproject.toml`

## Code paths

| Path | Purpose |
|------|---------|
| `brep2code/agent/` | hosted provider implementation |
| `brep2code/cli/` | provider selection/config flags |
| `docs/runbooks/` | hosted provider setup and smoke run |
| `docs/modules/` | module boundary updates |
| `tests/` | network-free provider config tests |

## Acceptance

- [x] Provider can be selected/configured without hard-coded secrets.
- [x] Missing credentials fail with a clear local configuration error.
- [x] Unit tests remain network-free by default.
- [x] A manual hosted-provider smoke command is documented.
- [x] README, workflow, module docs, and handoff reflect M3 completion criteria.
- [x] `uv run python -m pytest` passes (37 passed on 2026-08-01).
- [x] `uv run python -m ruff check .` passes (2026-08-01).

## Progress (2026-08-01)

- [x] DeepSeek V4 adapter, local ignored `.env`, default `deepseek-v4-pro`, network-free tests, and configuration-error path implemented.
- [x] Credential smoke reached DeepSeek, parsed a structured replacement, recorded a sanitized provider summary, and executed provider-generated scripts only through `wsl-bwrap`.
- [x] Output probe now has a separate process and bounded timeout. A final `deepseek-v4-pro` smoke received the input B-Rep summary, generated an OCP `10×20×30` box script, and passed script, readable-output, bbox, volume, and topology gates through `wsl-bwrap`.

## Out of scope

- Fine-tuning or local model deployment.
- Supporting multiple hosted providers at once.
- Dataset-scale evaluation.
- Benchmark claims about model quality.
