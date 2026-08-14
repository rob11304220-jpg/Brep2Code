# Test Feedback Segmentation

M53 keeps the full offline suite as the CI and closure gate while providing
three local, credential-free feedback selections.

## Commands

```powershell
# Fast deterministic unit and metadata feedback.
uv run python -m pytest -m fast -q

# Regular local verification, excluding process-backed Harness/corpus checks.
uv run python -m pytest -m standard -q

# Process-backed Harness, executor, and corpus integration boundary.
uv run python -m pytest -m sandbox -q

# Complete acceptance gate; this is the CI command and is never replaced.
uv run python -m pytest
```

## Membership rules

- `fast` is a subset of `standard`: deterministic tool-bridge, selector,
  governance, preregistration, and metadata tests with no CAD execution,
  corpus replay, or provider worker loop.
- `standard` contains every non-`sandbox` test. It includes the fast subset
  plus offline producer/audit tests that are useful for normal local changes.
- `sandbox` contains tests in the Harness, B-Rep probe, corpus runner, repair
  loop, and observed-build modules. They cross the local process boundary by
  executing CAD/Python workers or replaying a corpus case. The marker names a
  security-sensitive execution boundary; it does **not** claim that every test
  invokes WSL bubblewrap.

Membership is centralized in `tests/conftest.py`. Adding a test to an
execution-boundary module automatically gives it the `sandbox` marker;
otherwise it is `standard`. Add a module to `FAST_MODULES` only when the test
remains deterministic and avoids the execution boundary.

## CI invariant

`.github/workflows/ci.yml` runs `uv run python -m pytest` with no marker.
Marker selections are development feedback paths only and cannot substitute
for the full-suite result.
