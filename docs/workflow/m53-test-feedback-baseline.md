# M53 Offline Test Feedback Baseline

- **Refreshed**: 2026-08-09 by M62
- **Full command**: `uv run python -m pytest --durations=0 -q`
- **Full result**: 169 passed in 190.77s (Windows local offline environment).

The duration report identifies the multi-case observed-development check as
the dominant call at 19.92s. Corpus runner/replay checks follow at 11.12–15.08s;
observation-only repair and repair-loop checks take 5.11–6.47s. Those
process-backed modules form the `sandbox` selection. The remaining checks form
`standard`; the deterministic metadata and utility subset forms `fast`.

This is a local performance observation, not a CI timeout or performance
guarantee. Re-measure after changes to the process boundary or test layout.

## M53 selection verification

| Command | Result |
|---|---|
| `uv run python -m pytest -m fast -q` | 58 passed, 111 deselected in 4.47s |
| `uv run python -m pytest -m standard -q` | 92 passed, 77 deselected in 12.40s |
| `uv run python -m pytest -m sandbox -q` | 77 passed, 92 deselected in 180.26s |
| `uv run python -m pytest --durations=0 -q` | 169 passed in 190.77s |

## Planning interpretation

Use 60 seconds for a standalone `fast` or `standard` command and eight minutes
for a standalone `sandbox` or full-suite command in this local environment.
These are planning windows, not test or CI limits. M60 separately observed
324 seconds for sandbox and 340 seconds for the full suite under a more loaded
environment, so a command that exceeds the M62 measurement must retain its own
terminal result rather than being classified from duration alone.
